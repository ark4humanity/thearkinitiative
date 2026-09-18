# The Ark Initiative — website source

Static site for The Ark Initiative. No framework, no build step, no dependencies.

## Deploy (Cloudflare Pages)

- **Framework preset:** None
- **Build command:** *(leave blank)*
- **Build output directory:** `/` (repo root)
- **Root directory:** `/` (repo root)

Connect this repo in Cloudflare Pages → "Connect to Git" and deploy. Every push
to `main` redeploys automatically.

## Structure

- `index.html` — Home (vision, material vocabulary, the animal cast)
- `library.html` — Research Library (index of the 11 essays)
- `essays/` — full-text essay pages (11)
- `videos.html` — the five videos, streamed from Google Drive (not committed)
- `play.html` — Garden Defense playtest link
- `field-reports.html` — field reports and source sheets
- `about.html` — the Ark, the organization, pillars, material doctrine
- `css/style.css`, `js/main.js` — shared styles and scripts
- `img/` — optimized JPEGs (~3.2 MB total). The large video files live on
  Google Drive and are embedded via preview links, never committed.
- `build_site.py` — the generator that produced these pages; kept for reference
  (paths inside are specific to the author's workstation).

## Notes

- Media files: images are committed; videos are Drive-hosted and must have
  "Anyone with the link can view" sharing to play for the public.
- The site makes no nonprofit/tax-status claims; keep it that way.
