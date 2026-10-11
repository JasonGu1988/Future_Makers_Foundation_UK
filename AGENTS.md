# Working on the Future Makers Foundation site

This repository is the editable source for the static site at https://futuremakers.org.uk/. It is also public. Read `README.md` for the project layout and build commands.

## Site structure

- `build.py` turns `content/`, `templates/` and `source/` into `dist/`.
- `content/news/YYYY/<slug>.json` holds one published news article per file. `examples/news-post.json` shows the format.
- `templates/` controls the page layout; `source/` holds styles, JavaScript and media.
- `dist/` and `dist-preview/` are generated and ignored by Git. The live site is hosted separately; a GitHub push does not deploy it.

## Editorial rules

- Use “Future Makers Foundation” for current activities. Use historical names only when they are accurate historical facts or part of a source title.
- Use only supplied or verified facts. Do not invent quotes, outcomes, figures, affiliations, endorsements or commitments.
- Confirm that names and photos may be published. Give published images useful alternative text and preserve any required credit.
- Preserve existing article URLs and leave archive pages alone unless the request explicitly concerns them.
- Never commit credentials, database exports, private records, unused legacy media or an unapproved draft to this public repository.

## News updates

For a news article, follow [the news skill](.agents/skills/future-makers-news/SKILL.md). The owner can use [the copy-and-fill prompt](NEWS_UPDATE_PROMPT.md) to supply material. Create articles from [the JSON template](examples/news-post.json).

Build and inspect the article, home page, news index, images and mobile layout. If the user requested a draft or preview, keep it local. When publication is authorized, update the live site and the public GitHub source, then verify both. Do not assume that a GitHub push publishes the website.
