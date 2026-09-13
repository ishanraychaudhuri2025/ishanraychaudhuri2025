#!/usr/bin/env python3
"""Generate self-contained GitHub stats SVGs without a third-party stats host."""
from __future__ import annotations

import html
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from typing import Any

USER = "ishanraychaudhuri2025"
W = 500
H = 240

THEMES = {
    "dark": {
        "bg": "#0B0B0F", "panel": "#111116", "stroke": "#3B1118",
        "red": "#C8102E", "gold": "#D4AF37", "text": "#F5F5F5", "muted": "#A8A8B0", "dim": "#5F5F69",
    },
    "light": {
        "bg": "#FFFFFF", "panel": "#F5F5F5", "stroke": "#E0C8CE",
        "red": "#C8102E", "gold": "#A16D00", "text": "#111116", "muted": "#5E626B", "dim": "#9CA3AF",
    },
}


def api(path: str, token: str) -> Any:
    """Call GitHub's API with retries for rate limits, transient HTTP errors and network hiccups."""
    url = "https://api.github.com" + path
    last_error: Exception | None = None

    for attempt in range(4):
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "ishan-profile-stats",
        }
        if token:
            headers["Authorization"] = f"Bearer {token}"

        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                return json.load(response)
        except urllib.error.HTTPError as exc:
            last_error = exc
            if exc.code not in {408, 429, 500, 502, 503, 504}:
                raise
            retry_after = exc.headers.get("Retry-After")
            if retry_after and retry_after.isdigit():
                delay = min(30, int(retry_after))
            else:
                delay = 2 ** attempt
            time.sleep(delay)
        except (urllib.error.URLError, TimeoutError, ConnectionError) as exc:
            last_error = exc
            time.sleep(2 ** attempt)

    if last_error:
        raise RuntimeError(f"GitHub API request failed after retries: {path}: {last_error}") from last_error
    raise RuntimeError(f"GitHub API request failed: {path}")


def count_search_issues(q: str, token: str) -> int:
    encoded = urllib.parse.quote(q, safe="")
    try:
        return int(api(f"/search/issues?q={encoded}&per_page=1", token).get("total_count", 0))
    except Exception:
        return 0


def count_search_commits(q: str, token: str) -> int:
    encoded = urllib.parse.quote(q, safe="")
    try:
        return int(api(f"/search/commits?q={encoded}&per_page=1", token).get("total_count", 0))
    except Exception:
        return 0


def collect(token: str) -> dict[str, Any]:
    user = api(f"/users/{USER}", token)
    repos = api(f"/users/{USER}/repos?per_page=100&type=owner&sort=pushed", token)
    repos = [r for r in repos if not r.get("fork")]

    stars = sum(int(r.get("stargazers_count", 0)) for r in repos)
    languages: Counter[str] = Counter()
    for repo in repos:
        try:
            langs = api(f"/repos/{repo['full_name']}/languages", token)
            for lang, amount in langs.items():
                languages[lang] += int(amount)
        except Exception:
            continue

    return {
        "repos": len(repos),
        "stars": stars,
        "followers": int(user.get("followers", 0)),
        "commits": count_search_commits(f"author:{USER}", token),
        "prs": count_search_issues(f"author:{USER} is:pr", token),
        "issues": count_search_issues(f"author:{USER} is:issue", token),
        "languages": dict(languages),
    }


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def shell(t: dict[str, str], title: str) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(title)}">',
        f'<rect width="{W}" height="{H}" rx="14" fill="{t["bg"]}"/>',
        f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="13" fill="{t["panel"]}" stroke="{t["stroke"]}"/>',
        f'<text x="24" y="32" fill="{t["red"]}" font-size="13" font-weight="700" font-family="ui-monospace,SFMono-Regular,Menlo,monospace">{esc(title.upper())}</text>',
        f'<path d="M150 28 H476" stroke="{t["stroke"]}" stroke-dasharray="2 7"/>',
    ]


def stat_icon(kind: str, x: int, y: int, color: str) -> str:
    """Small solid-red outline icons placed beside each stat heading."""
    common = f'fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"'
    if kind == "repo":
        body = f'<rect x="-7" y="-8" width="14" height="16" rx="2" {common}/><path d="M-4 -4 H4 M-4 0 H4 M-4 4 H1" {common}/>'
    elif kind == "star":
        body = f'<path d="M0 -9 L2.5 -2.8 L9 -2.4 L4 1.8 L5.6 8 L0 4.7 L-5.6 8 L-4 1.8 L-9 -2.4 L-2.5 -2.8 Z" fill="{color}" stroke="none"/>'
    elif kind == "followers":
        body = f'<circle cx="-3" cy="-4" r="3.2" {common}/><path d="M-9 7 C-9 2.5 -6.5 0.5 -3 0.5 C0.5 0.5 3 2.5 3 7" {common}/><circle cx="5" cy="-2" r="2.4" {common}/><path d="M4 2 C7 2.3 9 4.2 9 7" {common}/>'
    elif kind == "commit":
        body = f'<circle cx="-6" cy="-6" r="2.5" {common}/><circle cx="-6" cy="6" r="2.5" {common}/><circle cx="6" cy="0" r="2.5" {common}/><path d="M-3.5 -6 H1 C4  -6 4 -3 4 0 C4 3 1 6 -3.5 6" {common}/>'
    elif kind == "pr":
        body = f'<circle cx="-5.5" cy="-6" r="2.5" {common}/><circle cx="5.5" cy="6" r="2.5" {common}/><path d="M-5.5 -3.5 V4 C-5.5 6 0 6 3 6" {common}/><path d="M2 0 L5.5 0 L5.5 -6" {common}/><path d="M2 -3.5 L5.5 0 L2 3.5" {common}/>'
    else:  # issue
        body = f'<circle cx="0" cy="0" r="8" {common}/><path d="M0 -4 V1" {common}/><circle cx="0" cy="4.5" r="0.8" fill="{color}" stroke="none"/>'
    return f'<g transform="translate({x} {y})">{body}</g>'


def make_stats(data: dict[str, Any], theme: str) -> str:
    t = THEMES[theme]
    parts = shell(t, "GitHub Stats")
    items = [
        ("Repositories", data["repos"], "repo"), ("Stars", data["stars"], "star"),
        ("Followers", data["followers"], "followers"), ("Commits", data["commits"], "commit"),
        ("Pull Requests", data["prs"], "pr"), ("Issues", data["issues"], "issue"),
    ]
    positions = [(24, 75), (260, 75), (24, 130), (260, 130), (24, 185), (260, 185)]
    for (label, value, icon), (x, y) in zip(items, positions):
        parts.append(stat_icon(icon, x + 7, y - 5, t["red"]))
        parts.append(f'<text x="{x + 22}" y="{y}" fill="{t["muted"]}" font-size="11" font-family="ui-monospace,SFMono-Regular,Menlo,monospace">{esc(label)}</text>')
        parts.append(f'<text x="{x + 22}" y="{y+25}" fill="{t["text"]}" font-size="22" font-weight="700" font-family="ui-monospace,SFMono-Regular,Menlo,monospace">{esc(value)}</text>')
    parts.append(f'<text x="24" y="228" fill="{t["gold"]}" font-size="9.5" font-family="ui-monospace,SFMono-Regular,Menlo,monospace">generated by GitHub Actions</text>')
    parts.append('</svg>')
    return ''.join(parts)


def make_langs(data: dict[str, Any], theme: str) -> str:
    t = THEMES[theme]
    parts = shell(t, "Top Languages")
    langs = sorted(data["languages"].items(), key=lambda kv: kv[1], reverse=True)[:8]
    total = sum(v for _, v in langs) or 1
    bar_x, bar_y, bar_w, bar_h = 24, 56, 452, 12
    cursor = bar_x
    for idx, (_, amount) in enumerate(langs):
        frac = amount / total
        width = max(2, bar_w * frac)
        if idx == 0:
            color = t["red"]
        elif idx == 1:
            color = t["gold"]
        else:
            color = f'rgba(200,16,46,{max(0.25, 0.82 - idx*0.07):.2f})'
        parts.append(f'<rect x="{cursor:.1f}" y="{bar_y}" width="{width:.1f}" height="{bar_h}" fill="{color}"/>')
        cursor += width

    y = 91
    for idx, (lang, amount) in enumerate(langs):
        pct = amount / total * 100
        color = t["red"] if idx == 0 else (t["gold"] if idx == 1 else t["muted"])
        parts.append(f'<circle cx="28" cy="{y-4}" r="4" fill="{color}"/>')
        parts.append(f'<text x="42" y="{y}" fill="{t["text"]}" font-size="11.5" font-family="ui-monospace,SFMono-Regular,Menlo,monospace">{esc(lang)}</text>')
        parts.append(f'<text x="450" y="{y}" text-anchor="end" fill="{t["muted"]}" font-size="11.5" font-family="ui-monospace,SFMono-Regular,Menlo,monospace">{pct:.1f}%</text>')
        y += 17
        if y > 210:
            break
    parts.append(f'<text x="24" y="229" fill="{t["gold"]}" font-size="9.5" font-family="ui-monospace,SFMono-Regular,Menlo,monospace">calculated from GitHub language bytes</text>')
    parts.append('</svg>')
    return ''.join(parts)


def main() -> None:
    token = os.environ.get("GITHUB_TOKEN", "")
    if not token:
        raise SystemExit("GITHUB_TOKEN is required")
    data = collect(token)
    out = os.environ.get("OUTPUT_DIR", "assets")
    os.makedirs(out, exist_ok=True)
    for theme in ("dark", "light"):
        with open(os.path.join(out, f"stats-{theme}.svg"), "w", encoding="utf-8") as handle:
            handle.write(make_stats(data, theme))
        with open(os.path.join(out, f"langs-{theme}.svg"), "w", encoding="utf-8") as handle:
            handle.write(make_langs(data, theme))


if __name__ == "__main__":
    main()
