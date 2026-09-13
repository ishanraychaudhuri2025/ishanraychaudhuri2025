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


def calendar_icon(accent):
    return f'''<g transform="translate(196.67 34) scale(0.78)">
  <defs>
    <linearGradient id="calendarRed" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#FF4A3D"/>
      <stop offset="0.55" stop-color="{accent}"/>
      <stop offset="1" stop-color="#8F0B20"/>
    </linearGradient>
  </defs>
  <ellipse cx="0" cy="29" rx="25" ry="4" fill="#000000" opacity="0.12"/>
  <rect x="-28" y="-18" width="56" height="48" rx="7" fill="url(#calendarRed)"/>
  <rect x="-28" y="-18" width="56" height="16" rx="7" fill="#FF4038"/>
  <rect x="-28" y="-10" width="56" height="8" fill="#E5232E"/>
  <rect x="-23" y="-1" width="46" height="26" rx="3" fill="#FFFFFF"/>
  <g fill="none" stroke="#E5232E" stroke-width="1.7">
    <path d="M-12 -6 V-20"/><path d="M0 -6 V-20"/><path d="M12 -6 V-20"/>
  </g>
  <g fill="#E5232E">
    <circle cx="-19" cy="5" r="1.7"/><circle cx="-7" cy="5" r="1.7"/><circle cx="5" cy="5" r="1.7"/><circle cx="17" cy="5" r="1.7"/>
    <circle cx="-19" cy="14" r="1.7"/><circle cx="-7" cy="14" r="1.7"/><circle cx="5" cy="14" r="1.7"/><circle cx="17" cy="14" r="1.7"/>
  </g>
  <g fill="#FFFFFF">
    <circle cx="-12" cy="-18" r="5"/><circle cx="0" cy="-18" r="5"/><circle cx="12" cy="-18" r="5"/>
  </g>
  <g fill="#E5232E">
    <circle cx="-12" cy="-18" r="2"/><circle cx="0" cy="-18" r="2"/><circle cx="12" cy="-18" r="2"/>
  </g>
</g>'''


def trophy_icon(gold):
    return f'''<g transform="translate(983.33 34) scale(0.78)">
  <ellipse cx="0" cy="29" rx="27" ry="4" fill="#000000" opacity="0.12"/>
  <path d="M-10 -20 H10 V-3 C10 7 5 14 0 17 C-5 14 -10 7 -10 -3 Z" fill="{gold}"/>
  <path d="M-10 -15 H-22 V-5 C-22 6 -15 13 -7 13 V7 C-12 6 -15 2 -15 -4 H-10 Z" fill="{gold}"/>
  <path d="M10 -15 H22 V-5 C22 6 15 13 7 13 V7 C12 6 15 2 15 -4 H10 Z" fill="{gold}"/>
  <path d="M-3 15 H3 V23 H-3 Z" fill="{gold}"/>
  <rect x="-18" y="22" width="36" height="8" rx="3" fill="{gold}"/>
</g>'''


def streak_card(theme, active_days, current, longest, current_start, current_end, longest_start, longest_end):
    if theme == "dark":
        bg, text, accent, gold, muted = "#0B0B0F", "#FFFFFF", "#C8102E", "#D4AF37", "#777B85"
    else:
        bg, text, accent, gold, muted = "#FFFFFF", "#111116", "#C8102E", "#A87800", "#8A8F98"

    current_range = fmt_range(current_start, current_end)
    longest_range = fmt_range(longest_start, longest_end)
    fire = "M 1.5 0.67 C 1.5 0.67 2.24 3.32 2.24 5.47 C 2.24 7.53 0.89 9.2 -1.17 9.2 C -3.23 9.2 -4.79 7.53 -4.79 5.47 L -4.76 5.11 C -6.78 7.51 -8 10.62 -8 13.99 C -8 18.41 -4.42 22 0 22 C 4.42 22 8 18.41 8 13.99 C 8 8.6 5.41 3.79 1.5 0.67 Z M -0.29 19 C -2.07 19 -3.51 17.6 -3.51 15.86 C -3.51 14.24 -2.46 13.1 -0.7 12.74 C 1.07 12.38 2.9 11.53 3.92 10.16 C 4.31 11.45 4.51 12.81 4.51 14.2 C 4.51 16.85 2.36 19 -0.29 19 Z"

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="195" viewBox="0 0 1180 195">
<defs>
  <clipPath id="outer"><rect width="1180" height="195" rx="12"/></clipPath>
  <mask id="ringMask"><rect width="1180" height="195" fill="white"/><ellipse cx="590" cy="32" rx="13" ry="18" fill="black"/></mask>
</defs>
<g clip-path="url(#outer)">
  <rect x="0.5" y="0.5" width="1179" height="194" rx="12" fill="{bg}" stroke="{FRAME_RED}"/>
  <line x1="393.33" y1="28" x2="393.33" y2="170" stroke="{accent}" stroke-width="1"/>
  <line x1="786.67" y1="28" x2="786.67" y2="170" stroke="{accent}" stroke-width="1"/>

  {calendar_icon(accent)}
  <text x="196.67" y="94" text-anchor="middle" fill="{accent}" font-family="Segoe UI,Ubuntu,sans-serif" font-size="30" font-weight="700">{active_days}</text>
  <text x="196.67" y="124" text-anchor="middle" fill="{accent}" font-family="Segoe UI,Ubuntu,sans-serif" font-size="14" font-weight="700">Active Days</text>
  <text x="196.67" y="148" text-anchor="middle" fill="{muted}" font-family="Segoe UI,Ubuntu,sans-serif" font-size="12">last 400 days</text>
  <rect x="172" y="158" width="49" height="4" rx="2" fill="{accent}"/>

  <g mask="url(#ringMask)"><circle cx="590" cy="71" r="40" fill="none" stroke="{accent}" stroke-width="5"/></g>
  <g transform="translate(590 19.5)" stroke-opacity="0"><path d="{fire}" fill="{gold}"/></g>
  <text x="590" y="80" text-anchor="middle" fill="{text}" font-family="Segoe UI,Ubuntu,sans-serif" font-weight="700" font-size="28">{current}</text>
  <text x="590" y="140" text-anchor="middle" fill="{gold}" font-family="Segoe UI,Ubuntu,sans-serif" font-weight="700" font-size="14">Current Streak</text>
  <text x="590" y="166" text-anchor="middle" fill="{muted}" font-family="Segoe UI,Ubuntu,sans-serif" font-weight="400" font-size="12">{current_range}</text>

  {trophy_icon(gold)}
  <text x="983.33" y="94" text-anchor="middle" fill="{gold}" font-family="Segoe UI,Ubuntu,sans-serif" font-size="30" font-weight="700">{longest}</text>
  <text x="983.33" y="124" text-anchor="middle" fill="{gold}" font-family="Segoe UI,Ubuntu,sans-serif" font-size="14" font-weight="700">Longest Streak</text>
  <text x="983.33" y="148" text-anchor="middle" fill="{muted}" font-family="Segoe UI,Ubuntu,sans-serif" font-size="12">{longest_range}</text>
  <rect x="958" y="158" width="51" height="4" rx="2" fill="{gold}"/>
</g>
</svg>'''


def frame(theme):
    bg = "#06080B" if theme == "dark" else "#F5F5F5"
    streak = (A / f"streak-{theme}.svg").read_text()
    stats = (A / f"stats-{theme}.svg").read_text()
    langs = (A / f"langs-{theme}.svg").read_text()
    snake = (A / f"activity-snake-{theme}.svg").read_text()
    scale = 1148 / 1180
    sx, sy = 1128 / 880, 170 / 192
    return "".join([
        '<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="670" viewBox="0 0 1180 670" role="img" aria-label="GitHub activity, stats, languages and contribution snake">',
        '<defs><clipPath id="frameClip"><rect x="1" y="1" width="1178" height="668" rx="16"/></clipPath></defs>',
        f'<rect x="1" y="1" width="1178" height="668" rx="16" fill="{bg}" stroke="{FRAME_RED}" stroke-width="2"/>',
        '<g clip-path="url(#frameClip)">',
        grp(streak, f"translate(16 16) scale({scale:.8f})"),
        grp(stats, "translate(26 210) scale(1.1 1)"),
        grp(langs, "translate(604 210) scale(1.1 1)"),
        grp(snake, f"translate({26 + 16 * sx:.8f} {458 + 32 * sy:.8f}) scale({sx:.8f} {sy:.8f})"),
        '</g></svg>',
    ])


def main():
    A.mkdir(exist_ok=True)
    metrics = streak_metrics(fetch_contributions())
    for theme in ("dark", "light"):
        (A / f"streak-{theme}.svg").write_text(streak_card(theme, *metrics), encoding="utf-8")
        snake = get(SNAKE + f"snake-{theme}.svg")
        (A / f"activity-snake-{theme}.svg").write_text(snake, encoding="utf-8")
        rendered = frame(theme)
        (A / f"profile-activity-{theme}.svg").write_text(rendered, encoding="utf-8")
        (A / f"profile-activity-final-{theme}.svg").write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    main()
