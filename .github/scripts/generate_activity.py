#!/usr/bin/env python3
from pathlib import Path
from datetime import date, timedelta
import re
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
A = ROOT / "assets"
USER = "ishanraychaudhuri2025"
SNAKE = "https://raw.githubusercontent.com/ishanraychaudhuri2025/ishanraychaudhuri2025/output/"
FRAME_RED = "#4A0E18"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "ishan-profile-activity"})
    with urllib.request.urlopen(req, timeout=30) as h:
        return h.read().decode()


def unwrap(s):
    m = re.match(r"<svg\b[^>]*>(.*)</svg>\s*$", s.strip(), re.I | re.S)
    if not m:
        raise ValueError("invalid SVG")
    return m.group(1)


def grp(s, t):
    return f'<g transform="{t}">{unwrap(s)}</g>'


def fetch_contributions():
    """Read GitHub's public contribution calendar instead of using a third-party streak API."""
    end = date.today()
    start = end - timedelta(days=400)
    url = f"https://github.com/users/{USER}/contributions?from={start.isoformat()}&to={end.isoformat()}"
    html = get(url)

    cells = re.findall(
        r'<td[^>]*data-date=["\'](\d{4}-\d{2}-\d{2})["\'][^>]*data-level=["\'](\d)["\'][^>]*>',
        html,
        flags=re.I,
    )
    if not cells:
        cells = re.findall(
            r'<td[^>]*data-level=["\'](\d)["\'][^>]*data-date=["\'](\d{4}-\d{2}-\d{2})["\'][^>]*>',
            html,
            flags=re.I,
        )
        cells = [(d, level) for level, d in cells]

    if not cells:
        raise RuntimeError("Could not parse GitHub contribution calendar")

    return {day: int(level) for day, level in cells}


def streak_metrics(levels):
    days = sorted(date.fromisoformat(day) for day in levels)
    active = {day for day in days if levels[day.isoformat()] > 0}
    if not active:
        return 0, 0, 0

    active_days = len(active)
    longest = 0
    run = 0
    previous = None

    for day in days:
        if day in active and (previous is None or day == previous + timedelta(days=1)):
            run += 1
        elif day in active:
            run = 1
        else:
            run = 0
        longest = max(longest, run)
        previous = day

    today = date.today()
    anchor = today if today in active else (
        today - timedelta(days=1) if today - timedelta(days=1) in active else None
    )

    current = 0
    if anchor is not None:
        current = 1
        while anchor - timedelta(days=current) in active:
            current += 1

    return active_days, current, longest


def streak_card(theme, active_days, current, longest):
    if theme == "dark":
        bg = "#0B0B0F"
        label = "#A8A8B0"
        text = "#F5F5F5"
        accent = "#C8102E"
        gold = "#D4AF37"
        muted = "#777B85"
    else:
        bg = "#FFFFFF"
        label = "#5E626B"
        text = "#111116"
        accent = "#C8102E"
        gold = "#A87800"
        muted = "#8A8F98"

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="195" viewBox="0 0 1180 195">'
        f'<rect x="0.5" y="0.5" width="1179" height="194" rx="12" fill="{bg}" stroke="{FRAME_RED}"/>'
        f'<text x="30" y="34" fill="{accent}" font-size="13" font-weight="700" font-family="ui-monospace,SFMono-Regular,Menlo,monospace">GITHUB ACTIVITY</text>'
        f'<path d="M185 30 H1150" stroke="{FRAME_RED}" stroke-dasharray="2 7"/>'
        f'<g font-family="ui-monospace,SFMono-Regular,Menlo,monospace">'
        f'<text x="75" y="78" fill="{label}" font-size="11">ACTIVE DAYS</text>'
        f'<text x="75" y="124" fill="{text}" font-size="30" font-weight="700">{active_days}</text>'
        f'<text x="75" y="151" fill="{muted}" font-size="10">last 400 days</text>'
        f'<text x="470" y="78" fill="{label}" font-size="11">CURRENT STREAK</text>'
        f'<text x="470" y="124" fill="{text}" font-size="30" font-weight="700">{current}</text>'
        f'<text x="470" y="151" fill="{muted}" font-size="10">consecutive days</text>'
        f'<text x="825" y="78" fill="{label}" font-size="11">LONGEST STREAK</text>'
        f'<text x="825" y="124" fill="{gold}" font-size="30" font-weight="700">{longest}</text>'
        f'<text x="825" y="151" fill="{muted}" font-size="10">consecutive days</text>'
        f'</g></svg>'
    )


def frame(theme):
    bg = "#06080B" if theme == "dark" else "#F5F5F5"
    streak = (A / f"streak-{theme}.svg").read_text()
    stats = (A / f"stats-{theme}.svg").read_text()
    langs = (A / f"langs-{theme}.svg").read_text()
    snake = (A / f"activity-snake-{theme}.svg").read_text()
    ssx, ssy = 1148 / 1180, 178 / 195
    sx, sy = 1128 / 880, 170 / 192

    return "".join([
        '<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="670" viewBox="0 0 1180 670" role="img" aria-label="GitHub activity, stats, languages and contribution snake">',
        '<defs><clipPath id="frameClip"><rect x="1" y="1" width="1178" height="668" rx="16"/></clipPath></defs>',
        f'<rect x="1" y="1" width="1178" height="668" rx="16" fill="{bg}" stroke="{FRAME_RED}" stroke-width="2"/>',
        '<g clip-path="url(#frameClip)">',
        grp(streak, f"translate(16 16) scale({ssx:.8f} {ssy:.8f})"),
        grp(stats, "translate(26 202) scale(1.1 1)"),
        grp(langs, "translate(604 202) scale(1.1 1)"),
        grp(snake, f"translate({26 + 16 * sx:.8f} {458 + 32 * sy:.8f}) scale({sx:.8f} {sy:.8f})"),
        '</g></svg>',
    ])


def main():
    A.mkdir(exist_ok=True)
    active_days, current, longest = streak_metrics(fetch_contributions())

    for theme in ("dark", "light"):
        (A / f"streak-{theme}.svg").write_text(
            streak_card(theme, active_days, current, longest)
        )
        snake = get(SNAKE + f"snake-{theme}.svg")
        (A / f"activity-snake-{theme}.svg").write_text(snake)
        (A / f"profile-activity-{theme}.svg").write_text(frame(theme))


if __name__ == "__main__":
    main()
