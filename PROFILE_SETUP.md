# Ishan GitHub Profile Setup

This repository is the profile README repository for `ishanraychaudhuri2025`.

## Theme

The profile uses a **2008-inspired red / white / black visual system**:

- Deep red: `#C8102E`
- Near-black: `#07090D`
- White: `#FFFFFF`
- Accent gold: `#D4AF37`

The main motif is a red field with white strips containing the black mark. Gold is only an accent.

## 1. Hero logo animation

The old profile-photo visual inside `VISUAL.MAP` has been replaced with the uploaded black mark converted into a vector and animated in red.

Files:

- `assets/united-mark.svg` — reusable black vector mark
- `assets/united-logo-red-animation.svg` — standalone red animated version
- `dark.svg` — dark-mode hero with animated red mark
- `light.svg` — light-mode hero with the same animated red mark

The hero also contains a **white horizontal block in the red top bar** with the black mark and red `08` text.

## 2. White stripe beside VISUAL.MAP

The separator beside the visual panel remains exactly `20px` wide and `420px` high. It is now white with the black mark centered vertically, instead of carrying rotated text.

This is intentionally the same length and thickness as the previous separator.

## 3. Signature stripe

`assets/signature-stripe.svg` is the horizontal white stripe under the hero. It contains the black mark and the text:

`BUILD • BREAK • DEBUG • LEARN`

The text and `08` are red.

`README.md` loads this asset directly with a cache-busting query parameter.

## 4. Profile image

The previously uploaded profile picture remains in:

`assets/profile-picture.jpg`

and its embedded SVG version remains in:

`assets/profile-picture.svg`

The current hero intentionally uses the **red animated mark** instead of the profile photo inside `VISUAL.MAP`, per the latest design change.

## 5. GitHub stats

The profile generates its own stats cards through `.github/scripts/generate_stats.py` and `.github/workflows/stats.yml`.

Generated files:

- `assets/stats-dark.svg`
- `assets/stats-light.svg`
- `assets/langs-dark.svg`
- `assets/langs-light.svg`

## 6. Contribution snake

`.github/workflows/snake.yml` generates both theme variants every 12 hours and on pushes to `main`.

The snake remains primarily red with small gold highlights.

## 7. Projects panel

`projects.json` controls the featured repositories. `.github/workflows/projects.yml` fetches live repository metadata and publishes the generated project panels to the `projects` branch.

## 8. Cache-busting

The README uses `?v=20260901-logo2` on the new SVG URLs so an older GitHub CDN copy is less likely to hide the latest changes.

When testing, open the raw SVG directly first. Confirm that the new red/white/black source is present before judging the rendered profile.

## 9. Permissions

Open **Settings → Actions → General → Workflow permissions** and select **Read and write permissions** so workflows can publish generated assets.

## 10. Maintenance

Edit source SVGs, scripts, workflow files, and `projects.json`; do not manually edit generated `output` or `projects` branch artifacts.

Never commit personal access tokens or other secrets.
