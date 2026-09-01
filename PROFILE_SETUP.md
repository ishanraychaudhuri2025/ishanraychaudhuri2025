# GitHub Profile Setup

This repository is the profile README repository for `ishanraychaudhuri2025`. GitHub displays a profile README when the public repository name exactly matches the username and the root contains `README.md`.

The profile is intentionally structured like the reference profile: theme-aware hero banner, streak card, stats cards, contribution snake, animated projects panel, and social badges.

## 1. Repository settings

Open this repository on GitHub and go to **Settings → Actions → General**.

Under **Workflow permissions**, choose **Read and write permissions** and save.

This permission is required because the workflows publish generated SVGs to the `output` and `projects` branches.

## 2. Hero banner

`README.md` loads `dark.svg` for dark mode and `light.svg` for light mode.

The banner currently uses your existing animated portrait asset from:

`https://raw.githubusercontent.com/IshanRayC/IshanRayC/main/assets/portrait.svg`

That keeps the profile repo lightweight and avoids duplicating the multi-megabyte portrait SVG.

To generate a new banner locally, use the existing banner generator from the companion workspace repository, or replace the `<image>` reference in `dark.svg` and `light.svg` with a new generated asset. Keep the banner source files as the source of truth rather than editing the rendered SVG by hand.

## 3. GitHub stats — recommended self-hosting

The visual profile is wired to the standard `github-readme-stats` API so it can render immediately. For a production setup matching the reference architecture, self-host the stats service.

### Create the GitHub token

1. GitHub → **Settings → Developer settings → Personal access tokens → Tokens (classic)**.
2. Generate a token with the `repo` scope.
3. A long-lived/no-expiration token can be used for the stats deployment.
4. Copy it immediately.
5. Treat it like a password. Never commit it, put it in `README.md`, or paste it into chat.

### Deploy the stats service

1. Fork `https://github.com/anuraghazra/github-readme-stats`.
2. Sign into Vercel with GitHub and choose the free Hobby plan.
3. Import your fork as a new Vercel project.
4. Leave the normal build settings unchanged.
5. Add the environment variable `PAT_1` with your token as its value.
6. Deploy.
7. Verify the generated `/api?username=ishanraychaudhuri2025&show_icons=true` endpoint.
8. Replace `https://github-readme-stats.vercel.app` in `README.md` with your own Vercel deployment URL.

The README uses `hide_rank=true` because the rank is heavily influenced by repository stars/followers and can be misleading for newer profiles; the reference implementation deliberately hides it.

## 4. Contribution snake

The workflow at `.github/workflows/snake.yml` runs:

- every 12 hours
- on pushes to `main`
- manually via **Actions → Generate Contribution Snake → Run workflow**

It generates both light and dark SVGs and publishes them to the `output` branch.

Important: the first workflow run must succeed before the snake image can render from the `output` branch.

The dark palette intentionally begins with a visible slate empty-cell colour (`#2d3343`) so the grid remains visible against GitHub dark mode.

## 5. Projects panel

`projects.json` controls which six projects appear and their order.

The workflow at `.github/workflows/projects.yml`:

1. reads `projects.json`
2. fetches live stars, language bytes, and recent push time from GitHub
3. generates theme-aware `projects-dark.svg` and `projects-light.svg`
4. publishes them to the `projects` branch

To change the panel, edit only `projects.json`. The README does not need to change.

Keep project descriptions short enough to fit two lines in the generated cards.

## 6. Testing and cache debugging

When an asset appears unchanged:

1. Open its raw GitHub URL and add a query such as `?v=999`.
2. Check the actual SVG source for the expected colour or content.
3. Confirm that the latest GitHub Actions run is green.
4. Check whether GitHub is showing the dark or light asset you intended.

GitHub/CDN caching can make an already-correct asset appear stale for a while. Browser refresh alone does not always clear GitHub's CDN cache.

## 7. Maintenance

Do not store PATs or other secrets in this repository.

Do not commit `merged.json` or generated branch output back into `main`; the Actions workflows generate those artifacts for you.

Keep the source configuration (`projects.json`, workflow files, and generator scripts) under version control.

The profile's generated assets are intentionally separated from the source files so the README stays small and readable.
