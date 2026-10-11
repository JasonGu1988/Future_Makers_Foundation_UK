# Future Makers Foundation website

Source for the static website at [futuremakers.org.uk](https://futuremakers.org.uk/). Future Makers Foundation is a UK charity supporting opportunities for young artists and creative people.

The site uses plain HTML, CSS and JavaScript. Python 3.10+ builds the pages from editable templates and JSON content. It does not require Craft CMS, PHP, plugins or a database.

## What is here

- `content/` — published news, artist stories and archive pages
- `templates/` — page layouts and sections
- `source/` — styles, JavaScript, logos and images used by published pages
- `examples/news-post.json` — template for a new article
- `build.py` — generates the website and checks local links and images
- `NEWS_UPDATE_PROMPT.md` — reusable instructions for drafting a news update
- `AGENTS.md` — project context and editorial rules for AI coding assistants
- `.agents/skills/future-makers-news/SKILL.md` — task guidance for adding news

Generated output (`dist/` and `dist-preview/`), deployment archives, private credentials, database exports and unused legacy media are deliberately excluded from this repository. The files here are sufficient to build the published pages.

## Build locally

From this repository's root, run:

```sh
python3 build.py --bundle-uploads
```

To inspect the home page locally, run `python3 -m http.server 8000 --directory dist` and open `http://localhost:8000/`. The built-in server serves other pages at their `.html` paths; the production build includes an Apache `.htaccess` file for the site's extensionless URLs, along with `sitemap.xml`, `robots.txt` and a 404 page. To make the side-by-side editorial preview instead, run `python3 build.py --preview`; its links are configured for `/static-preview/` and its media URLs expect a separate `/uploads/` directory on the preview host.

## Add a news story

1. Copy `examples/news-post.json` to `content/news/YYYY/your-short-headline.json`. Set `uri` to the matching path, such as `news/2026/your-short-headline`.
2. Add the headline, summary, body and date. Use `displayDate` (`YYYY-MM-DD`) for the date readers see and `postDate` (UTC timestamp) for article order. The builder requires `published: true` for a local preview, so keep drafts local and unpushed until approved.
3. Put any approved photo in `source/uploads/`, reference it as `/uploads/filename.jpg`, add the filename to `images`, and give it descriptive alternative text. Check consent and image rights before publishing.
4. Build and review the article, home page and news index. Deploy the generated `dist/` files to the hosting provider after approval.

The latest news cards and full news index update automatically. For a copy-and-fill brief, use [NEWS_UPDATE_PROMPT.md](NEWS_UPDATE_PROMPT.md); AI assistants can also follow [the news skill](.agents/skills/future-makers-news/SKILL.md).

## Publishing and rights

This repository is a public showcase and source backup. It does not deploy automatically; the live site is hosted separately. Do not commit credentials, database exports, private records or unpublished media.

No open-source license is granted. The foundation's name, logos, writing and images are included for presentation of this website; some images or partner marks may have separate owners. Contact [jing@futuremakers.org.uk](mailto:jing@futuremakers.org.uk) before reusing any material.
