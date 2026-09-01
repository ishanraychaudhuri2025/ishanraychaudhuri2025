#!/usr/bin/env python3
"""Generate the animated red/black/gold projects panel."""
from __future__ import annotations

import html
import json
import math
import os
import sys

W = 1180
CARD_W = 578
CARD_H = 168
GAP = 14
FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"

THEMES = {
    "dark": {
        "BG": "#0B0B0F", "PANEL": "#111116", "BAR": "#09090C", "RED": "#C8102E",
        "GOLD": "#D4AF37", "TEXT": "#F5F5F5", "MUTED": "#A8A8B0", "DIM": "#5F5F69",
        "STROKE": "rgba(200,16,46,0.42)", "PILL": "rgba(200,16,46,0.12)", "PILL_STROKE": "rgba(212,175,55,0.42)",
    },
    "light": {
        "BG": "#F5F5F5", "PANEL": "#FFFFFF", "BAR": "#EFEFEF", "RED": "#C8102E",
        "GOLD": "#A16D00", "TEXT": "#111116", "MUTED": "#5E626B", "DIM": "#9CA3AF",
        "STROKE": "rgba(200,16,46,0.28)", "PILL": "rgba(200,16,46,0.06)", "PILL_STROKE": "rgba(161,109,0,0.38)",
    },
}


def esc(value):
    return html.escape(str(value), quote=True)


def wrap(text, width=58):
    words = str(text or "").split()
    lines, current = [], ""
    for word in words:
        candidate = (current + " " + word).strip()
        if len(candidate) <= width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
        if len(lines) == 2:
            break
    if current and len(lines) < 2:
        lines.append(current)
    if len(lines) == 2 and " ".join(lines) != " ".join(words):
        lines[-1] = lines[-1][: max(1, len(lines[-1]) - 1)] + "…"
    return lines


def panel(projects, theme):
    t = THEMES[theme]
    rows = max(1, math.ceil(len(projects) / 2))
    height = 58 + rows * (CARD_H + GAP) + 6
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{height}" viewBox="0 0 {W} {height}" font-family="{FONT}" role="img" aria-label="Ishan projects">',
        f'<rect width="{W}" height="{height}" fill="{t["BG"]}"/>',
        f'<text x="5" y="24" fill="{t["RED"]}" font-size="13">PROJECTS</text>',
        f'<path d="M92 20 H1175" stroke="{t["STROKE"]}" stroke-dasharray="2 7"/>',
    ]
    for idx, project in enumerate(projects):
        x = 5 + (idx % 2) * (CARD_W + GAP)
        y = 40 + (idx // 2) * (CARD_H + GAP)
        begin = 0.25 + idx * 0.12
        repo = esc(project.get("repo", ""))
        name = esc(project.get("name", "Project"))
        parts += [
            f'<a href="https://github.com/{repo}" target="_blank">',
            f'<g transform="translate({x},{y})" opacity="0">',
            f'<animate attributeName="opacity" from="0" to="1" dur="0.45s" begin="{begin:.2f}s" fill="freeze"/>',
            f'<rect width="{CARD_W}" height="{CARD_H}" rx="12" fill="{t["PANEL"]}" stroke="{t["STROKE"]}">',
            f'<animate attributeName="stroke" values="{t["STROKE"]};{t["PILL_STROKE"]};{t["STROKE"]}" dur="5s" repeatCount="indefinite"/></rect>',
            f'<rect width="{CARD_W}" height="30" rx="12" fill="{t["BAR"]}"/><rect y="18" width="{CARD_W}" height="12" fill="{t["BAR"]}"/>',
            f'<text x="16" y="19" font-size="10" fill="{t["MUTED"]}"><tspan fill="{t["RED"]}">●</tspan> {repo}</text>',
            f'<text x="18" y="65" font-size="17" font-weight="700" fill="{t["TEXT"]}">{name}<tspan fill="{t["RED"]}">_</tspan></text>',
        ]
        for line_no, line in enumerate(wrap(project.get("description", ""))):
            parts.append(f'<text x="18" y="{88 + line_no * 16}" font-size="11" fill="{t["MUTED"]}">{esc(line)}</text>')

        tx = 18
        for tag in (project.get("tags") or [])[:3]:
            tw = max(52, len(tag) * 6.5 + 18)
            parts += [
                f'<rect x="{tx:.0f}" y="118" width="{tw:.0f}" height="18" rx="9" fill="{t["PILL"]}" stroke="{t["PILL_STROKE"]}"/>',
                f'<text x="{tx + tw/2:.0f}" y="131" text-anchor="middle" font-size="9.5" fill="{t["GOLD"]}">{esc(tag)}</text>',
            ]
            tx += tw + 7

        stars = int(project.get("stars", 0) or 0)
        parts.append(f'<text x="18" y="156" font-size="11" fill="{t["MUTED"]}"><tspan fill="{t["GOLD"]}">★</tspan> {stars}</text>')
        langs = project.get("languages") or {}
        total = sum(langs.values())
        if total:
            top = sorted(langs.items(), key=lambda kv: kv[1], reverse=True)[:3]
            legend = " · ".join(f"{esc(k)} {v/total*100:.0f}%" for k, v in top)
            parts.append(f'<text x="{CARD_W-18}" y="156" text-anchor="end" font-size="10" fill="{t["MUTED"]}">{legend}</text>')
        else:
            parts.append(f'<text x="{CARD_W-18}" y="156" text-anchor="end" font-size="10" fill="{t["DIM"]}">metadata pending</text>')
        parts.append('</g></a>')
    parts.append('</svg>')
    return "".join(parts)


def main():
    source = sys.argv[1] if len(sys.argv) > 1 else "merged.json"
    output = sys.argv[2] if len(sys.argv) > 2 else "out"
    with open(source, encoding="utf-8") as handle:
        projects = json.load(handle)
    os.makedirs(output, exist_ok=True)
    for theme in ("dark", "light"):
        with open(os.path.join(output, f"projects-{theme}.svg"), "w", encoding="utf-8") as handle:
            handle.write(panel(projects, theme))
    print(f"generated {len(projects)} project cards")


if __name__ == "__main__":
    main()
