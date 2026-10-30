# LaughMyWay public website

This is the source for the existing public GitHub Pages site at <https://laughmywaycomedy.github.io/>. The design uses the supplied LaughMyWay microphone logo without modifying it, with its black, vermilion, cream, and cyan palette. The old site is preserved in Git history before this redesign.

## Update the catalog

Only add videos that are already public on the LaughMyWay YouTube channel. Edit `content/videos.json` with the public YouTube ID, exact title, local cover asset, and concise description. The initial ten IDs and titles were checked against YouTube's oEmbed endpoint on October 30, 2026. Put landscape film covers and portrait Short covers in `assets/`.

Run `python build.py` to regenerate `index.html`. Commit both the catalog and generated page. The five film links use `youtube.com/watch?v=...`; the five Short links use `youtube.com/shorts/...`. The channel link is `UCHXKAN03_utA3CvBsZUZpcg`.

## Check before publishing

Run a local static server from this directory:

```text
python -m http.server 8788 --bind 127.0.0.1
```

In another terminal, run `python check_site.py`. This requires Playwright (`python -m pip install playwright`) and a Chromium browser. It checks all four routes, local links, image loads, the ten real video IDs, mobile overflow at 390 px and 320 px, and writes desktop/mobile screenshots to `../laughmyway_site_qa/` outside the checkout.

Publish by pushing the reviewed commit to `main` in `LaughMyWayComedy/laughmywaycomedy.github.io`. GitHub Pages serves the repository root. Keep `/privacy/`, `/terms/`, and `/publisher/` intact. The privacy and terms retain their earlier material language; the privacy notice now also names the locally hosted font files. Their visual shell matches the new site. The publisher page explains the owner-operated desktop tool and its OAuth use.

## Assets and behavior

The logo and covers are first-party assets supplied by the creator's local production packages. Fonts are hosted locally; the corresponding SIL Open Font License files are in `assets/fonts/`. The site has no third-party embed, analytics, form, or runtime script. Watch and subscribe controls link directly to YouTube, and contact opens email. The design respects reduced-motion preferences.
