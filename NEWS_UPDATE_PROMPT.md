# Reusable prompt: publish a Future Makers Foundation news update

Copy the text below into a new Codex chat. Replace the bracketed fields and attach any approved photos. If you want a draft only, remove the final publishing sentence.

---

Please add a news update to this **static Future Makers Foundation website**. Read `AGENTS.md` and `.agents/skills/future-makers-news/SKILL.md` first. Use the existing site design and news format. The public site is published from generated static files; do not edit Craft CMS or its database.

**Headline or topic:** [insert]

**Public date:** [day month year]

**Approved facts and source material:** [paste notes, links, or an approved draft]

**People and organisations that may be named:** [insert exact names and roles]

**Photos:** [attach files or give local paths, captions, credits, and confirmation that they may be published]

**Link or call to action, if any:** [insert or write “none”]

Write a clear, concise article for a UK charity. Use “Future Makers Foundation” for current activities; retain historical names only when they are part of a verified historical fact or source title. Do not invent quotes, figures, outcomes, endorsements, sponsorship claims, or future commitments. If an essential fact or photo permission is unclear, flag it for me instead of guessing. Give every published image useful alternative text.

Check whether this story already exists. Create one new article file under `content/news/YYYY/` using the existing JSON format and a matching URL slug. Set the visible date from the public date I supplied, keep the article in the correct news order, and make the homepage latest-news cards and news index update automatically. Preserve all existing articles and their URLs. Leave historical legacy pages alone.

Build the static preview, check the article, news index, homepage card, images, and mobile layout, and show me the preview and the exact proposed copy. **Wait for my approval before uploading the new article to the public site or pushing it to this public GitHub repository.** After I approve, build and deploy the static output through the existing IONOS setup, update the GitHub backup, then verify the live article URL and GitHub commit. Keep credentials out of chat and out of the public website files.

---

The editable site and build notes are in [README.md](README.md). The sample article structure is in [examples/news-post.json](examples/news-post.json).
