# Ishan GitHub Profile Setup

This is the profile README repository for `ishanraychaudhuri2025`.

## Theme

The visible profile uses a **2008-inspired Manchester United visual language** rather than violet:

- Deep red: `#C8102E`
- Near-black: `#07090D`
- White: `#FFFFFF`
- Accent gold: `#D4AF37`

The key motif is **red + white vertical stripe + black mark**, with gold used sparingly for highlights. It is a visual interpretation, not an official club asset reproduction.

## 1. Profile image

The exact profile picture supplied for this profile has been uploaded to:

`assets/profile-picture.jpg`

An embedded SVG copy is also available at:

`assets/profile-picture.svg`

The hero uses the embedded version so it does not depend on GitHub's external avatar image loading.

## 2. Hero banner

`README.md` loads `dark.svg` in dark mode and `light.svg` in light mode.

The hero now contains a red top bar, a white stripe separator, and the uploaded profile image. The layout remains responsive and avoids the broken external-avatar behavior from the old version.

## 3. GitHub stats

The profile generates its own stats cards through `.github/scripts/generate_stats.py` and `.github/workflows/stats.yml`.

Generated files:

- `assets/stats-dark.svg`
- `assets/stats-light.svg`
- `assets/langs-dark.svg`
- `assets/langs-light.svg`

This avoids depending on the public `github-readme-stats` Vercel instance for the main cards.

The workflow runs on pushes to `main`, every 6 hours, and manually through **Actions → Generate Profile Stats → Run workflow**.

## 4. Contribution snake

`.github/workflows/snake.yml` generates the light and dark snake every 12 hours and on pushes to `main`.

The snake stays primarily red, with small gold highlights for the strongest contribution levels. Violet has been removed.

Generated files are published to the `output` branch as `snake-light.svg` and `snake-dark.svg`.

## 5. Projects panel

`projects.json` controls the six featured repositories.

`.github/workflows/projects.yml` fetches live repository data and publishes the generated theme variants to the `projects` branch.

## 6. Cache-busting while testing

The README appends `?v=20260901` to raw SVG URLs. This is deliberate: GitHub's CDN can keep an older copy after a successful commit.

When debugging an asset, open its raw URL directly and verify the current source before judging the rendered README.

## 7. Permissions

Open **Settings → Actions → General → Workflow permissions** and make sure workflows have **Read and write permissions** so they can publish generated assets.

## 8. Maintenance

Change source files and generators, not generated branch artifacts.

Never commit personal access tokens or other secrets.
