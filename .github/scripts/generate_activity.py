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


def grp(s, transform):
    return f'<g transform="{transform}">{unwrap(s)}</g>'


def fetch_contributions():
    end = date.today()
    start = end - timedelta(days=400)
    url = f"https://github.com/users/{USER}/contributions?from={start.isoformat()}&to={end.isoformat()}"
    html = get(url)
    cells = re.findall(r'<td[^>]*data-date=["\'](\d{4}-\d{2}-\d{2})["\'][^>]*data-level=["\'](\d)["\'][^>]*>', html, re.I)
    if not cells:
        cells = re.findall(r'<td[^>]*data-level=["\'](\d)["\'][^>]*data-date=["\'](\d{4}-\d{2}-\d{2})["\'][^>]*>', html, re.I)
        cells = [(d, level) for level, d in cells]
    if not cells:
        raise RuntimeError("Could not parse GitHub contribution calendar")
    return {day: int(level) for day, level in cells}


def streak_metrics(levels):
    days = sorted(date.fromisoformat(day) for day in levels)
    active = {day for day in days if levels[day.isoformat()] > 0}
    active_days = len(active)
    if not active:
        return 0, 0, 0, None, None, None, None

    longest = 0
    longest_start = longest_end = None
    run = 0
    run_start = None
    previous = None
    for day in days:
        if day in active and (previous is None or day == previous + timedelta(days=1)):
            if run == 0:
                run_start = day
            run += 1
        elif day in active:
            run = 1
            run_start = day
        else:
            run = 0
            run_start = None
        if run > longest:
            longest = run
            longest_start, longest_end = run_start, day
        previous = day

    today = date.today()
    anchor = today if today in active else (today - timedelta(days=1) if today - timedelta(days=1) in active else None)
    current = 0
    current_start = current_end = None
    if anchor is not None:
        current_end = anchor
        current = 1
        while anchor - timedelta(days=current) in active:
            current += 1
        current_start = anchor - timedelta(days=current - 1)

    return active_days, current, longest, current_start, current_end, longest_start, longest_end


def fmt_range(start, end):
    if not start or not end:
        return "no active streak"
    if start == end:
        return start.strftime("%b %-d")
    if start.year == end.year and start.month == end.month:
        return f"{start.strftime('%b %-d')} - {end.strftime('%-d')}"
    return f"{start.strftime('%b %-d')} - {end.strftime('%b %-d')}"


def streak_card(theme, active_days, current, longest, current_start, current_end, longest_start, longest_end):
    if theme == "dark":
        bg, text, accent, gold, muted = "#0B0B0F", "#FFFFFF", "#C8102E", "#D4AF37", "#777B85"
    else:
        bg, text, accent, gold, muted = "#FFFFFF", "#111116", "#C8102E", "#A87800", "#8A8F98"

    cs = fmt_range(current_start, current_end)
    ce = fmt_range(longest_start, longest_end)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="195" viewBox="0 0 1180 195">
<defs><clipPath id="outer"><rect width="1180" height="195" rx="12"/></clipPath></defs>
<g clip-path="url(#outer)">
  <rect x="0.5" y="0.5" width="1179" height="194" rx="12" fill="{bg}" stroke="{FRAME_RED}"/>
  <line x1="393.33" y1="28" x2="393.33" y2="170" stroke="{accent}" stroke-width="1"/>
  <line x1="786.67" y1="28" x2="786.67" y2="170" stroke="{accent}" stroke-width="1"/>

  <!-- ACTIVE DAYS: approved design -->
  <g transform="translate(196.67 40)" fill="none" stroke="{accent}" stroke-width="2">
    <rect x="-11" y="-8" width="22" height="18" rx="3"/>
    <line x1="-11" y1="-2" x2="11" y2="-2"/>
    <line x1="-6" y1="-12" x2="-6" y2="-5"/>
    <line x1="6" y1="-12" x2="6" y2="-5"/>
    <circle cx="-5" cy="4" r="1.2" fill="{accent}" stroke="none"/>
    <circle cx="0" cy="4" r="1.2" fill="{accent}" stroke="none"/>
    <circle cx="5" cy="4" r="1.2" fill="{accent}" stroke="none"/>
  </g>
  <text x="196.67" y="82" text-anchor="middle" fill="{accent}" font-family="Segoe UI,Ubuntu,sans-serif" font-size="30" font-weight="700">{active_days}</text>
  <text x="196.67" y="112" text-anchor="middle" fill="{text}" font-family="Segoe UI,Ubuntu,sans-serif" font-size="14" font-weight="700">Active Days</text>
  <text x="196.67" y="139" text-anchor="middle" fill="{muted}" font-family="Segoe UI,Ubuntu,sans-serif" font-size="12">last 400 days</text>
  <rect x="174" y="151" width="45" height="4" rx="2" fill="{accent}" opacity="0.9"/>

  <!-- CURRENT STREAK: compact classic ring + centered flame -->
  <circle cx="590" cy="68" r="34" fill="none" stroke="{accent}" stroke-width="5"/>
  <path d="M590 17 C590 11 594 8 594 4 C600 11 600 18 597 22 C596 24 594 25 592 25 C586 25 582 21 582 16 C582 12 584 9 587 6 C587 11 589 13 590 17 Z" fill="{gold}"/>
  <path d="M591 13 C591 10 593 8 593 6 C596 11 596 15 594 18 C593 19 592 20 591 20 C589 20 587 18 587 16 C587 14 588 12 590 11 C590 12 591 13 591 13 Z" fill="#FFE7A3"/>
  <text x="590" y="77" text-anchor="middle" fill="{text}" font-family="Segoe UI,Ubuntu,sans-serif" font-size="28" font-weight="700">{current}</text>
  <text x="590" y="116" text-anchor="middle" fill="{text}" font-family="Segoe UI,Ubuntu,sans-serif" font-size="14" font-weight="700">Current Streak</text>
  <text x="590" y="143" text-anchor="middle" fill="{muted}" font-family="Segoe UI,Ubuntu,sans-serif" font-size="12">{cs}</text>
  <rect x="566" y="153" width="48" height="4" rx="2" fill="{gold}" opacity="0.9"/>

  <!-- LONGEST STREAK: fully filled trophy -->
  <g transform="translate(983.33 41)" fill="{gold}">
    <path d="M-8 -6 H8 V1 C8 7 4 11 0 11 C-4 11 -8 7 -8 1 Z"/>
    <path d="M-8 -3 H-13 V1 C-13 6 -10 9 -6 9 H-4 V5 H-6 C-8 5 -9 3 -9 0 H-8 Z"/>
    <path d="M8 -3 H13 V1 C13 6 10 9 6 9 H4 V5 H6 C8 5 9 3 9 0 H8 Z"/>
    <rect x="-2.5" y="11" width="5" height="6" rx="1"/>
    <rect x="-8" y="17" width="16" height="3" rx="1.5"/>
  </g>
  <text x="983.33" y="82" text-anchor="middle" fill="{gold}" font-family="Segoe UI,Ubuntu,sans-serif" font-size="30" font-weight="700">{longest}</text>
  <text x="983.33" y="112" text-anchor="middle" fill="{text}" font-family="Segoe UI,Ubuntu,sans-serif" font-size="14" font-weight="700">Longest Streak</text>
  <text x="983.33" y="139" text-anchor="middle" fill="{muted}" font-family="Segoe UI,Ubuntu,sans-serif" font-size="12">{ce}</text>
  <rect x="959" y="151" width="48" height="4" rx="2" fill="{gold}" opacity="0.9"/>
</g>
</svg>'''


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
    metrics = streak_metrics(fetch_contributions())
    for theme in ("dark", "light"):
        (A / f"streak-{theme}.svg").write_text(streak_card(theme, *metrics))
        snake = get(SNAKE + f"snake-{theme}.svg")
        (A / f"activity-snake-{theme}.svg").write_text(snake)
        (A / f"profile-activity-{theme}.svg").write_text(frame(theme))


if __name__ == "__main__":
    main()
