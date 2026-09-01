# Ishan GitHub Profile Setup

This repository is the profile README repository for `ishanraychaudhuri2025`. The visible layout follows the same architecture as the reference profile you selected: theme-aware hero, full-width streak, side-by-side stats, contribution snake, animated projects panel, and social badges.

## Theme

The profile now uses a **2008-inspired Manchester United-style palette** rather than violet:

- Red: `#C8102E`
- Black: `#0B0B0F`
- White: `#F5F5F5`
- Gold: `#D4AF37`

This is a visual color theme, not an official club asset or logo reproduction.

## 1. Repository permissions

Open this repository → **Settings → Actions → General**.

Under **Workflow permissions**, select **Read and write permissions** and save.

The snake, projects, and stats workflows publish generated files and therefore need write access.

## 2. Hero banner

`README.md` loads `dark.svg` in GitHub dark mode and `light.svg` in GitHub light mode.

The hero uses the same profile-picture source currently used by your GitHub account, so the image stays clear instead of rendering the old multi-megabyte animated portrait as a tiny raster fallback.

The two SVGs are source files and should be edited through the generator/source pipeline rather than manually editing a rendered derivative.

## 3. GitHub stats — no broken third-party cards

The previous setup used the public `github-readme-stats.vercel.app` instance. That service is best-effort and can hit rate limits or traffic spikes. This profile therefore generates its own cards with GitHub Actions.

This profile now uses `.github/scripts/generate_stats.py` with `.github/workflows/stats.yml`. The workflow queries GitHub using the built-in `GITHUB_TOKEN` and writes:

- `assets/stats-dark.svg`
- `assets/stats-light.svg`
- `assets/langs-dark.svg`
- `assets/langs-light.svg`

No personal access token is stored in the repository and no Vercel deployment is required.

The workflow refreshes every 6 hours, on pushes to `main`, and manually from **Actions → Generate Profile Stats → Run workflow**.

## 4. Contribution snake

`.github/workflows/snake.yml` generates both theme variants every 12 hours and on pushes to `main`.

The dark palette uses visible empty cells and red/gold contribution levels so the grid remains readable against the black background.

Generated files are published to the `output` branch as:

- `snake-dark.svg`
- `snake-light.svg`

The README reads these files from that branch.

## 5. Projects panel

`projects.json` controls the six featured repositories and their order.

`.github/workflows/projects.yml` fetches live repository data and runs `.github/scripts/fetch_data.py` plus `.github/scripts/generate_projects.py`. The generated theme variants are published to the `projects` branch.

To change the projects shown on the profile, edit only `projects.json`.

## 6. Why some things may still appear unchanged

GitHub aggressively caches raw assets and profile images.

When testing a change, first open the raw SVG and add a harmless query string such as `?v=999`. Verify that the source contains the new color or content. Then check the latest Actions run and confirm you are viewing the intended dark/light theme.

A browser refresh alone does not necessarily invalidate GitHub's CDN copy.

## 7. Workflow checklist

The expected `main` workflows are:

- `Generate Contribution Snake`
- `Generate Projects Panel`
- `Generate Profile Stats`

A green run should produce the corresponding generated files. The profile README should not need manual edits when contributions, languages, stars, or project metadata change.

## 8. Maintenance

Keep `projects.json`, workflow files, and generator scripts under version control.

Do not commit PATs or other secrets.

Do not manually edit generated SVGs in the `output` or `projects` branches; change the source workflow/script instead.
