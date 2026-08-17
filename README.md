# Site source

Hugo + PaperMod, deployed to GitHub Pages by GitHub Actions on every push to `main`.
No software to install — everything can be done in the browser.

## First-time setup

1. Create a **public** repo named exactly `jacobbuildmodel.github.io`.
2. Upload the contents of this folder (see SETUP notes below about the `.github` folder).
3. Repo → **Settings → Pages → Build and deployment → Source: GitHub Actions**.
4. Wait ~2 min. Site is live at `https://jacobbuildmodel.github.io`.

## Publishing a brief

1. Go to `content/briefs/` in the repo → open `TEMPLATE.md` → **Copy raw file**.
2. **Add file → Create new file**, name it `content/briefs/2026-08-24.md`, paste, edit.
3. Set `draft: false` and the correct `date:`. Commit.
4. Actions builds and publishes automatically.

## Where to edit what

| I want to change… | File |
|---|---|
| Site name, author, menu | `hugo.toml` |
| Homepage intro text | `hugo.toml` → `[params.homeInfoParams]` |
| Umami analytics ID | `hugo.toml` → `[params.analytics.umami]` |
| Buttondown newsletter | `hugo.toml` → `[params.newsletter]` |
| Method page | `content/process.md` |
| About / Disclaimer | `content/about.md`, `content/disclaimer.md` |
| Post structure | `content/briefs/TEMPLATE.md` |
| Colours, badges, tables | `assets/css/extended/custom.css` |

## Source-tier badges

Write `{{< tag "hard-flow" >}}` in any post. Recognised: `hard-co`, `company-prelim`, `hard-flow`,
`consensus`, `price-proxy`, `cong-disc`, `spec`, `verified`, `inferred`, `speculative`.
Any other value still renders, just with default styling.
