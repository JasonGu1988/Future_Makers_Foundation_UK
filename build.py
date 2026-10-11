#!/usr/bin/env python3
"""Build the Future Makers Foundation site as plain HTML, CSS, JS, and media."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from html import escape
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import shutil
from urllib.parse import unquote, urlsplit, urlunsplit
from xml.sax.saxutils import escape as xml_escape
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
TEMPLATES = ROOT / "templates"
SOURCE = ROOT / "source"
STATIC_PAGES = {
    "about": ("About us", "Meet Future Makers Foundation and its trustees and directors."),
    "programmes": ("Our work", "Explore the foundation’s work with the Royal Albert Hall and Jigsaw4u."),
    "artists": ("Artists", "Read the three artist stories supported by the foundation."),
    "news": ("News", "Updates and stories from Future Makers Foundation."),
    "support": ("Support us", "Partner with and contact Future Makers Foundation."),
}
ASSETS = (
    "crescendo-header.png",
    "crescendo-stacked.png",
    "jigsaw4u-approved.png",
    "royal-albert-hall-approved.png",
    "yu-hang-performance-2.jpg",
)
PUBLISHED_DOMAIN = "https://futuremakers.org.uk"
DISPLAY_TIMEZONE = ZoneInfo("America/Los_Angeles")


def display_date(value: str, format_string: str) -> str:
    # The legacy export stores UTC; this matches the date displayed by Craft staging.
    date = datetime.fromisoformat(value).replace(tzinfo=timezone.utc)
    return date.astimezone(DISPLAY_TIMEZONE).strftime(format_string)


def entry_display_date(entry: dict, format_string: str) -> str:
    # New articles can specify their intended public calendar date directly.
    if entry.get("displayDate"):
        return datetime.strptime(entry["displayDate"], "%Y-%m-%d").strftime(format_string)
    return display_date(entry["postDate"], format_string)


def load_entries() -> list[dict]:
    entries = []
    seen = set(STATIC_PAGES)
    for path in sorted(CONTENT.rglob("*.json")):
        entry = json.loads(path.read_text(encoding="utf-8"))
        uri = entry.get("uri", "")
        expected = CONTENT / f"{uri}.json"
        if expected != path or not re.fullmatch(r"[a-z0-9][a-z0-9/_-]*", uri):
            raise ValueError(f"Content path and URI disagree: {path}")
        if uri in seen:
            raise ValueError(f"Duplicate page URI: {uri}")
        seen.add(uri)
        for field in ("title", "postDate", "body", "section"):
            if not isinstance(entry.get(field), str):
                raise ValueError(f"Missing {field}: {path}")
        if entry.get("published") is not True:
            raise ValueError(f"Unpublished content must not be in the static build: {path}")
        if entry["section"] not in ("pages", "successStories", "news"):
            raise ValueError(f"Unknown section: {path}")
        datetime.fromisoformat(entry["postDate"])
        if "displayDate" in entry:
            datetime.strptime(entry["displayDate"], "%Y-%m-%d")
        if re.search(r"<\s*(script|iframe|object)\b|\bon\w+\s*=|javascript:", entry["body"], re.I):
            raise ValueError(f"Unsafe HTML in: {path}")
        entries.append(entry)
    return entries


def card(entry: dict) -> str:
    date = entry_display_date(entry, "%-d %b %Y").upper()
    title = escape(entry["title"])
    uri = escape(entry["uri"], quote=True)
    return (
        f'<a class="news-card" href="/{uri}">'
        f'<span class="news-card-date">{date}</span><strong>{title}</strong>'
        '<span class="news-card-more">Read story <b aria-hidden="true">↗</b></span></a>'
    )


def description(entry: dict) -> str:
    summary = entry.get("summary", "").strip()
    if not summary:
        summary = re.sub(r"<[^>]+>", " ", entry["body"])
        summary = re.sub(r"\s+", " ", summary).strip()
    return summary[:158].rstrip()


def detail_content(entry: dict) -> str:
    title = escape(entry["title"])
    summary = entry.get("summary", "").strip()
    summary_html = f"<p>{escape(summary)}</p>" if summary else ""
    body = entry["body"].replace("{entry:26:url}", "/about-us/subpage-1")
    if "{entry:" in body:
        raise ValueError(f"Unresolved legacy entry link: {entry['uri']}")
    if entry["section"] == "news":
        date = entry_display_date(entry, "%-d %B %Y")
        intro = f'<a class="ya-link" href="/news">← All news</a><header class="page-intro"><span class="eyebrow">{date}</span><h1>{title}</h1></header>'
    elif entry["section"] == "successStories":
        intro = f'<a class="ya-link" href="/artists">← All artists</a><header class="page-intro"><span class="eyebrow">Artist story</span><h1>{title}</h1>{summary_html}</header>'
    else:
        intro = f'<header class="page-intro"><span class="eyebrow">From our archive</span><h1>{title}</h1>{summary_html}</header>'
    return f'<article class="wrap section-space">{intro}<div class="article-body">{body}</div></article>'


def rewrite_urls(html: str, base: str, preview: bool, page_uris: set[str]) -> str:
    """Prefix preview links; production keeps legacy extensionless page URLs."""
    def replace_attr(match: re.Match) -> str:
        before, value, after = match.groups()
        if not value.startswith("/"):
            return match.group(0)
        parts = urlsplit(value)
        path = "/" + parts.path.lstrip("/")
        if path == "/":
            new_path = f"{base}/" if preview else "/"
        elif path.startswith("/uploads/"):
            # The standalone dev root serves its own copy of these uploads.
            new_path = path
        elif path.lstrip("/") in page_uris:
            new_path = f"{base}{path}.html" if preview else path
        else:
            new_path = f"{base}{path}" if preview else path
        return f"{before}{urlunsplit(('', '', new_path, parts.query, parts.fragment))}{after}"

    return re.sub(r'((?:href|src)=")([^"]+)(")', replace_attr, html)


def render(layout: str, body: str, title: str, meta: str, active: str,
           base: str, preview: bool, page_uris: set[str]) -> str:
    page = (layout.replace("@@CONTENT@@", body)
                  .replace("@@TITLE@@", escape(title))
                  .replace("@@DESCRIPTION@@", escape(meta, quote=True))
                  .replace("@@ROBOTS@@", "noindex,nofollow" if preview else "index,follow"))
    if active:
        page = page.replace(f'class="" href="/{active}"', f'class="active" href="/{active}"')
    page = re.sub(r"©\s*20\d{2}\s+Future Makers", f"© {datetime.now().year} Future Makers", page)
    return rewrite_urls(page, base, preview, page_uris)


class Links(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for key, value in attrs:
            if key in ("href", "src") and value:
                self.links.append(value)


def validate_output(out: Path, preview: bool, base: str) -> None:
    for page in out.rglob("*.html"):
        html = page.read_text(encoding="utf-8")
        if "@@" in html or "dev.futuremakers.org.uk" in html or "{entry:" in html:
            raise ValueError(f"Template placeholder or staging URL in {page}")
        parser = Links()
        parser.feed(html)
        for url in parser.links:
            parts = urlsplit(url)
            if parts.scheme or parts.netloc or not parts.path.startswith("/"):
                continue
            path = unquote(parts.path)
            if path.startswith("/uploads/"):
                target = SOURCE / path.lstrip("/") if preview else out / path.lstrip("/")
            else:
                if preview:
                    if not path.startswith(base + "/"):
                        raise ValueError(f"Preview link escaped its base: {page}: {url}")
                    path = path[len(base):]
                if path == "/":
                    target = out / "index.html"
                elif not preview and not Path(path).suffix:
                    target = out / f"{path.lstrip('/')}.html"
                else:
                    target = out / path.lstrip("/")
            if not target.is_file():
                raise ValueError(f"Broken local link in {page}: {url} -> {target}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preview", action="store_true", help="Build for /static-preview/ on the current staging domain")
    parser.add_argument("--bundle-uploads", action="store_true", help="Copy source/uploads media files into production output")
    args = parser.parse_args()
    out = ROOT / ("dist-preview" if args.preview else "dist")
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    base = "/static-preview" if args.preview else ""

    entries = load_entries()
    page_uris = set(STATIC_PAGES) | {entry["uri"] for entry in entries}
    news = sorted((entry for entry in entries if entry["section"] == "news"),
                  key=lambda entry: entry["postDate"], reverse=True)
    layout = (TEMPLATES / "layout.html").read_text(encoding="utf-8")

    for name, (title, meta) in [("home", ("Home", "Future Makers Foundation supports young people through the arts and education.")), *STATIC_PAGES.items()]:
        body = (TEMPLATES / f"{name}.html").read_text(encoding="utf-8")
        if name == "home":
            body = body.replace("@@NEWS_CARDS@@", "\n".join(card(entry) for entry in news[:3]))
        elif name == "news":
            body = body.replace("@@NEWS_CARDS@@", "\n".join(card(entry) for entry in news))
        filename = "index.html" if name == "home" else f"{name}.html"
        page = render(layout, body, title, meta, "" if name == "home" else name,
                      base, args.preview, page_uris)
        (out / filename).write_text(page, encoding="utf-8")

    for entry in entries:
        uri = entry["uri"]
        active = "news" if entry["section"] == "news" else "artists" if entry["section"] == "successStories" else ""
        page = render(layout, detail_content(entry), entry["title"], description(entry),
                      active, base, args.preview, page_uris)
        target = out / f"{uri}.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(page, encoding="utf-8")

    for filename in ("styles.css", "styles-v2.css", "artist-slider.js", "favicon.png"):
        shutil.copy2(SOURCE / filename, out / filename)
    (out / "assets").mkdir()
    for filename in ASSETS:
        shutil.copy2(SOURCE / "assets" / filename, out / "assets" / filename)
    if args.bundle_uploads:
        if args.preview:
            raise ValueError("The side-by-side preview shares the existing /uploads directory")
        shutil.copytree(SOURCE / "uploads", out / "uploads")

    if args.preview:
        (out / "robots.txt").write_text("User-agent: *\nDisallow: /static-preview/\n")
    else:
        urls = ["/"] + [f"/{uri}" for uri in sorted(page_uris)]
        sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        sitemap += "".join(f"  <url><loc>{xml_escape(PUBLISHED_DOMAIN + url)}</loc></url>\n" for url in urls)
        sitemap += "</urlset>\n"
        (out / "sitemap.xml").write_text(sitemap, encoding="utf-8")
        (out / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {PUBLISHED_DOMAIN}/sitemap.xml\n")
        (out / ".htaccess").write_text(
            "Options -MultiViews -Indexes\nDirectorySlash Off\nDirectoryIndex index.html\nErrorDocument 404 /404.html\n"
            "<IfModule mod_rewrite.c>\nRewriteEngine On\nRewriteOptions AllowNoSlash\nRewriteBase /\n"
            "RewriteCond %{HTTPS} !=on [OR]\nRewriteCond %{HTTP_HOST} !^futuremakers\\.org\\.uk$ [NC]\n"
            "RewriteRule ^ https://futuremakers.org.uk%{REQUEST_URI} [R=301,L]\n"
            "RewriteCond %{REQUEST_FILENAME} !-f\n"
            "RewriteCond %{REQUEST_FILENAME}.html -f\nRewriteRule ^(.+)$ $1.html [L]\n</IfModule>\n"
        )
    not_found = render(layout, '<section class="page-intro wrap"><h1>Page not found.</h1><p>That page is unavailable. <a href="/">Return home</a>.</p></section>',
                       "Page not found", "The requested page is unavailable.", "", base, args.preview, page_uris)
    (out / "404.html").write_text(not_found, encoding="utf-8")

    validate_output(out, args.preview, base)
    count = len(list(out.rglob("*.html")))
    print(f"Built {count} HTML pages, including {len(news)} published news posts and {len(entries)} archive entries, in {out}")
    print("Full media bundle:" if args.bundle_uploads else "Media files referenced from standalone dev /uploads:",
          len(list((out / "uploads").iterdir())) if args.bundle_uploads else len(list((SOURCE / "uploads").iterdir())))


if __name__ == "__main__":
    main()
