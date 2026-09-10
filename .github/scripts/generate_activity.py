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
    end = date.today()
    start = end - timedelta(days=400)
    url = f"https://github.com/users/{USER}/contributions?from={start.isoformat()}&to={end.isoformat()}"
    html = get(url)
    cells = re.findall(
        r'<td[^>]*data-date=["\'](\d{4}-\d{2}-\d{2})["\'][^>]*data-level=["\'](\d)["\'][^>]*>',
        html, re.I
    )
    if not cells:
        cells = re.findall(
            r'<td[^>]*data-level=["\'](\d)["\'][^>]*data-date=["\'](\d{4}-\d{2}-\d{2})["\'][^>]*>',
            html, re.I
        )
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
    run_start = None
    previous = None
    run = 0
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
    anchor = today if today in active else (
        today - timedelta(days=1) if today - timedelta(days=1) in active else None
    )
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
        bg, label, text, accent, gold, muted = "#0B0B0F", "#A8A8B0", "#FFFFFF", "#C8102E", "#D4AF37", "#777B85"
    else:
        bg, label, text, accent, gold, muted = "#FFFFFF", "#5E626B", "#111116", "#C8102E", "#A87800", "#8A8F98"

    cs, ce = fmt_range(current_start, current_end), fmt_range(longest_start, longest_end)
    fire = "M 1.5 0.67 C 1.5 0.67 2.24 3.32 2.24 5.47 C 2.24 7.53 0.89 9.2 -1.17 9.2 C -3.23 9.2 -4.79 7.53 -4.79 5.47 L -4.76 5.11 C -6.78 7.51 -8 10.62 -8 13.99 C -8 18.41 -4.42 22 0 22 C 4.42 22 8 18.41 8 13.99 C 8 8.6 5.41 3.79 1.5 0.67 Z M -0.29 19 C -2.07 19 -3.51 17.6 -3.51 15.86 C -3.51 14.24 -2.46 13.1 -0.7 12.74 C 1.07 12.38 2.9 11.53 3.92 10.16 C 4.31 11.45 4.51 12.81 4.51 14.2 C 4.51 16.85 2.36 19 -0.29 19 Z"

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="195" viewBox="0 0 1180 195">
<style>
@keyframes fadein {{from {{opacity:0}} to {{opacity:1}}}}
@keyframes pop {{0% {{font-size:3px;opacity:.15}} 80% {{font-size:34px;opacity:1}} 100% {{font-size:28px;opacity:1}}}}
@keyframes ring {{from {{stroke-dashoffset:214;opacity:.2}} to {{stroke-dashoffset:0;opacity:1}}}}
@keyframes iconin {{0% {{opacity:0;transform:translateY(5px)}} 100% {{opacity:1;transform:translateY(0)}}}}
</style>
<defs>
  <clipPath id="outer"><rect width="1180" height="195" rx="12"/></clipPath>
  <mask id="mask"><rect width="1180" height="195" fill="white"/><ellipse cx="590" cy="23" rx="11" ry="14" fill="black"/></mask>
</defs>
<g clip-path="url(#outer)">
  <rect x="0.5" y="0.5" width="1179" height="194" rx="12" fill="{bg}" stroke="{FRAME_RED}"/>
  <line x1="393.33" y1="28" x2="393.33" y2="167" stroke="{accent}" stroke-width="1"/>
  <line x1="786.67" y1="28" x2="786.67" y2="167" stroke="{accent}" stroke-width="1"/>

  <!-- LEFT / ACTIVE DAYS -->
  <g font-family="Segoe UI,Ubuntu,sans-serif" text-anchor="middle">
    <g transform="translate(196.67 47)" fill="none" stroke="{accent}" stroke-width="2" opacity="0" style="animation:iconin .45s ease-out forwards .05s">
      <rect x="-9" y="-7" width="18" height="16" rx="2"/><line x1="-9" y1="-2" x2="9" y2="-2"/>
      <line x1="-5" y1="-11" x2="-5" y2="-5"/><line x1="5" y1="-11" x2="5" y2="-5"/>
      <circle cx="-4" cy="2" r="1" fill="{accent}" stroke="none"/><circle cx="1" cy="2" r="1" fill="{accent}" stroke="none"/><circle cx="6" cy="2" r="1" fill="{accent}" stroke="none"/>
    </g>
    <text x="196.67" y="76" fill="{accent}" font-size="30" font-weight="700" style="opacity:0;animation:pop .55s linear forwards .15s">{active_days}</text>
    <text x="196.67" y="112" fill="{text}" font-size="14" font-weight="700" style="opacity:0;animation:fadein .45s linear forwards .3s">Active Days</text>
    <text x="196.67" y="140" fill="{muted}" font-size="12" style="opacity:0;animation:fadein .45s linear forwards .4s">last 400 days</text>
    <rect x="175" y="151" width="43" height="4" rx="2" fill="{accent}" opacity=".8" style="opacity:0;animation:fadein .35s linear forwards .48s"/>
  </g>

  <!-- CENTER / CURRENT STREAK -->
  <g mask="url(#mask)">
    <circle cx="590" cy="58" r="34" fill="none" stroke="{accent}" stroke-width="5" stroke-dasharray="214" stroke-dashoffset="214" style="animation:ring .7s ease-out forwards .15s"/>
  </g>
  <g transform="translate(590 12)" opacity="0" style="animation:iconin .45s ease-out forwards .28s">
    <path d="{fire}" fill="{gold}"/>
  </g>
  <text x="590" y="67" text-anchor="middle" fill="{text}" font-family="Segoe UI,Ubuntu,sans-serif" font-size="28" font-weight="700" style="opacity:0;animation:pop .55s linear forwards .32s">{current}</text>
  <g font-family="Segoe UI,Ubuntu,sans-serif" text-anchor="middle">
    <text x="590" y="111" fill="{text}" font-size="14" font-weight="700" style="opacity:0;animation:fadein .45s linear forwards .5s">Current Streak</text>
    <text x="590" y="140" fill="{muted}" font-size="12" style="opacity:0;animation:fadein .45s linear forwards .58s">{cs}</text>
    <rect x="566" y="151" width="48" height="4" rx="2" fill="{gold}" opacity=".85" style="opacity:0;animation:fadein .35s linear forwards .65s"/>
  </g>

  <!-- RIGHT / LONGEST STREAK -->
  <g font-family="Segoe UI,Ubuntu,sans-serif" text-anchor="middle">
    <g transform="translate(983.33 47)" fill="none" stroke="{gold}" stroke-width="2" opacity="0" style="animation:iconin .45s ease-out forwards .12s">
      <path d="M-8 6 L-6 -3 L-1 0 L2 -8 L8 1 L4 2 L7 7 Z" fill="{gold}" stroke="none"/>
    </g>
    <text x="983.33" y="76" fill="{gold}" font-size="30" font-weight="700" style="opacity:0;animation:pop .55s linear forwards .2s">{longest}</text>
    <text x="983.33" y="112" fill="{text}" font-size="14" font-weight="700" style="opacity:0;animation:fadein .45s linear forwards .35s">Longest Streak</text>
    <text x="983.33" y="140" fill="{muted}" font-size="12" style="opacity:0;animation:fadein .45s linear forwards .45s">{ce}</text>
    <rect x="959" y="151" width="48" height="4" rx="2" fill="{gold}" opacity=".85" style="opacity:0;animation:fadein .35s linear forwards .55s"/>
  </g>
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
