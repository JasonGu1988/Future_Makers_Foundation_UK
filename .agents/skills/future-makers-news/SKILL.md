---
name: future-makers-news
description: Draft, edit, preview, or publish a news article for the Future Makers Foundation static website using its JSON content model. Use for Future Makers news updates, not for unrelated site changes.
---

# Future Makers news

Work in the repository containing `build.py`. Read `AGENTS.md`, `README.md`, `examples/news-post.json`, and a recent `content/news/` entry before editing.

1. Check for an existing article on the topic. Ground the proposed copy in the owner's approved facts and sources. Resolve missing names, dates, claims, image permissions or credits before publication.
2. Create or edit `content/news/YYYY/<slug>.json`. Keep the path and `uri` identical apart from `.json`. Use `displayDate` (`YYYY-MM-DD`) for the public date and `postDate` (UTC timestamp) for sorting. Keep `section` as `news`. The builder requires `published: true` to preview a new article, so keep unapproved drafts local and unpushed.
3. Add only approved images to `source/uploads/`. Reference them as `/uploads/<filename>` in the article body, list them in `images`, and give each image descriptive alt text. Preserve existing article URLs and unrelated content.
4. Run `python3 build.py --bundle-uploads`. Review the generated article, latest home-page cards, full news index, local links and images. Check the mobile layout if visual changes or unusual content warrant it.
5. Show the owner the draft and preview when requested. A draft in this public Git repository must stay uncommitted and unpushed until publication is authorized. Publishing requires updating the hosted static files and then synchronizing this source repository; verify the live URL and GitHub commit.

Do not touch Craft CMS or a database. Keep hosting credentials outside the repository and chat. `NEWS_UPDATE_PROMPT.md` is the owner's reusable request template; `README.md` explains the build and hosting boundary.
