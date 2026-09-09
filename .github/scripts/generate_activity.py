#!/usr/bin/env python3
"""Build a GitHub-profile activity frame using local SVG assets only.

GitHub sanitizes/blocks externally hosted SVGs when they are nested inside
another SVG. This script downloads the streak and snake assets into the repo,
then composes them with the locally generated stats/language cards.
"""
from __future__ import annotations

import os
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / "assets"
USER = "ishanraychaudhuri2025"

STREAK_BASE = "https://streak-stats.demolab.com/"
SNAKE_BASE = (
    "https://raw.githubusercontent.com/ishanraychaudhuri2025/"
    "ishanraychaudhuri2025/output/"
)


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "ishan-profile-activity"})
    with urllib.request.urlopen(req, timeout=30) as response:
        return response.read().decode("utf-8")


def write(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def streak_url(theme: str) -> str:
    if theme == "dark":
        params = (
            f"?user={USER}&hide_border=true&background=0B0B0F&stroke=C8102E"
            "&ring=C8102E&fire=D4AF37&currStreakLabel=FFFFFF"
            "&sideLabels=A8A8B0&currStreakNum=FFFFFF&sideNums=FFFFFF"
            "&dates=777B85&titleColor=C8102E&card_width=1180"
        )
    else:
        params = (
            f"?user={USER}&hide_border=true&background=FFFFFF&stroke=C8102E"
            "&ring=C8102E&fire=D4AF37&currStreakLabel=111116"
            "&sideLabels=5E626B&currStreakNum=111116&sideNums=111116"
            "&dates=9CA3AF&titleColor=C8102E&card_width=1180"
        )
    return STREAK_BASE + params


def frame(theme: str) -> str:
    if theme == "dark":
        bg = "#06080B"
    else:
        bg = "#F5F5F5"

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="670" viewBox="0 0 1180 670" role="img" aria-label="GitHub streak, stats, languages and contribution snake">
  <rect x="1" y="1" width="1178" height="668" rx="16" fill="{bg}" stroke="#C8102E" stroke-width="2"/>
  <image href="streak-{theme}.svg" x="16" y="16" width="1148" height="170" preserveAspectRatio="none"/>
  <image href="stats-{theme}.svg" x="26" y="200" width="550" height="240" preserveAspectRatio="none"/>
  <image href="langs-{theme}.svg" x="604" y="200" width="550" height="240" preserveAspectRatio="none"/>
  <image href="activity-snake-{theme}.svg" x="26" y="458" width="1128" height="170" preserveAspectRatio="none"/>
</svg>'''


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    for theme in ("dark", "light"):
        write(ASSETS / f"streak-{theme}.svg", fetch(streak_url(theme)))
        write(ASSETS / f"activity-snake-{theme}.svg", fetch(SNAKE_BASE + f"snake-{theme}.svg"))
        write(ASSETS / f"profile-activity-{theme}.svg", frame(theme))


if __name__ == "__main__":
    main()
