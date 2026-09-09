#!/usr/bin/env python3
"""Build a self-contained GitHub-profile activity frame.

GitHub can sanitize or fail to load nested external SVG/image references.
The generated activity SVG therefore inlines the downloaded streak, stats,
language and snake SVGs into one document.
"""
from __future__ import annotations

import re
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
        return (
            f"{STREAK_BASE}?user={USER}&hide_border=true&background=0B0B0F&stroke=C8102E"
            "&ring=C8102E&fire=D4AF37&currStreakLabel=FFFFFF&sideLabels=A8A8B0"
            "&currStreakNum=FFFFFF&sideNums=FFFFFF&dates=777B85&titleColor=C8102E&card_width=1180"
        )
    return (
        f"{STREAK_BASE}?user={USER}&hide_border=true&background=FFFFFF&stroke=C8102E"
        "&ring=C8102E&fire=D4AF37&currStreakLabel=111116&sideLabels=5E626B"
        "&currStreakNum=111116&sideNums=111116&dates=9CA3AF&titleColor=C8102E&card_width=1180"
    )


def inline_svg(content: str, x: int, y: int, width: int, height: int) -> str:
    """Turn a complete child SVG into a nested SVG positioned inside the frame."""
    content = content.strip()
    return re.sub(
        r"<svg\b[^>]*>",
        f'<svg x="{x}" y="{y}" width="{width}" height="{height}" preserveAspectRatio="none">',
        content,
        count=1,
        flags=re.IGNORECASE,
    )


def make_frame(theme: str) -> str:
    bg = "#06080B" if theme == "dark" else "#F5F5F5"
    streak = (ASSETS / f"streak-{theme}.svg").read_text(encoding="utf-8")
    stats = (ASSETS / f"stats-{theme}.svg").read_text(encoding="utf-8")
    langs = (ASSETS / f"langs-{theme}.svg").read_text(encoding="utf-8")
    snake = (ASSETS / f"activity-snake-{theme}.svg").read_text(encoding="utf-8")

    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="670" viewBox="0 0 1180 670" '
        'role="img" aria-label="GitHub streak, stats, languages and contribution snake">',
        f'<rect x="1" y="1" width="1178" height="668" rx="16" fill="{bg}" stroke="#C8102E" stroke-width="2"/>',
        inline_svg(streak, 16, 16, 1148, 178),
        inline_svg(stats, 26, 202, 550, 240),
        inline_svg(langs, 604, 202, 550, 240),
        inline_svg(snake, 26, 458, 1128, 170),
        '</svg>',
    ]
    return "".join(parts)


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    for theme in ("dark", "light"):
        write(ASSETS / f"streak-{theme}.svg", fetch(streak_url(theme)))
        write(ASSETS / f"activity-snake-{theme}.svg", fetch(SNAKE_BASE + f"snake-{theme}.svg"))
        write(ASSETS / f"profile-activity-{theme}.svg", make_frame(theme))


if __name__ == "__main__":
    main()
