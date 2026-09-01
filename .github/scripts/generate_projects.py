#!/usr/bin/env python3
"""Generate an animated, theme-aware projects panel from merged.json."""
import html, json, math, os, sys

W = 1180
CARD_W = 578
CARD_H = 168
GAP = 14
FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"

THEMES = {
    "dark": {
        "BG": "#0A101F", "PANEL": "#0C1426", "BAR": "#0B1222", "CYAN": "#22D3EE",
        "VIOLET": "#A78BFA", "GREEN": "#10B981", "TEXT": "#F8FAFC", "MUTED": "#94A3B8",
        "DIM": "#475569", "STROKE": "rgba(34,211,238,0.28)", "PILL": "rgba(124,58,237,0.28)",
        "PILL_STROKE": "rgba(167,139,250,0.45)",
    },
    "light": {
        "BG": "#F8FAFC", "PANEL": "#FFFFFF", "BAR": "#F1F5F9", "CYAN": "#0891B2",
        "VIOLET": "#7C3AED", "GREEN": "#059669", "TEXT": "#0F172A", "MUTED": "#475569",
        "DIM": "#94A3B8", "STROKE": "rgba(8,145,178,0.30)", "PILL": "rgba(124,58,237,0.10)",
        "PILL_STROKE": "rgba(124,58,237,0.35)",
    },
}


def esc(value):
    return html.escape(str(value), quote=True)


def wrap(text, width=55):
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
    if len(lines) == 2 and len(" ".join(lines)) < len(" ".join(words)):
        lines[-1] = lines[-1][:-1] + "…"
    return lines


def panel(projects, theme):
    t = THEMES[theme]
    rows = max(1, math.ceil(len(projects) / 2))
    height = 58 + rows * (CARD_H + GAP) + 6
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{height}" viewBox="0 0 {W} {height}" font-family="{FONT}" role="img" aria-label="Ishan projects">',
        f'<rect width="{W}" height="{height}" fill="{t["BG"]}"/>',
        f'<text x="5" y="24" fill="{t["CYAN"]}" font-size="13">PROJECTS</text>',
        f'<path d="M92 20 H1175" stroke="{t["STROKE"]}" stroke-dasharray="2 7"/>',
    ]
    for idx, p in enumerate(projects):
        x = 5 + (idx % 2) * (CARD_W + GAP)
        y = 40 + (idx // 2) * (CARD_H + GAP)
        begin = 0.25 + idx * 0.12
        repo = esc(p.get("repo", ""))
        name = esc(p.get("name", "Project"))
        parts += [
            f'<a href="https://github.com/{repo}" target="_blank">',
            f'<g transform="translate({x},{y})" opacity="0">',
            f'<animate attributeName="opacity" from="0" to="1" dur="0.45s" begin="{begin:.2f}s" fill="freeze"/>',
            f'<rect width="{CARD_W}" height="{CARD_H}" rx="12" fill="{t["PANEL"]}" stroke="{t["STROKE"]}"/>',
            f'<rect width="{CARD_W}" height="30" rx="12" fill="{t["BAR"]}"/><rect y="18" width="{CARD_W}" height="12" fill="{t["BAR"]}"/>',
            f'<text x="16" y="19" font-size="10" fill="{t["MUTED"]}"><tspan fill="{t["CYAN"]}">●</tspan> {repo}</text>',
            f'<text x="18" y="65" font-size="17" font-weight="700" fill="{t["TEXT"]}">{name}<tspan fill="{t["CYAN"]}">_</tspan></text>',
        ]
        lines = wrap(p.get("description", ""))
        for i, line in enumerate(lines):
            parts.append(f'<text x="18" y="{88 + i*16}" font-size="11" fill="{t["MUTED"]}">{esc(line)}</text>')

        tx = 18
        for tag in (p.get("tags") or [])[:3]:
            tw = max(52, len(tag) * 6.5 + 18)
            parts += [
                f'<rect x="{tx:.0f}" y="118" width="{tw:.0f}" height="18" rx="9" fill="{t["PILL"]}" stroke="{t["PILL_STROKE"]}"/>',
                f'<text x="{tx + tw/2:.0f}" y="131" text-anchor="middle" font-size="9.5" fill="{t["VIOLET"]}">{esc(tag)}</text>',
            ]
            tx += tw + 7

        stars = int(p.get("stars", 0) or 0)
        parts.append(f'<text x="18" y="156" font-size="11" fill="{t["MUTED"]}"><tspan fill="{t["CYAN"]}">★</tspan> {stars}</text>')
        langs = p.get("languages") or {}
        total = sum(langs.values()) or 0
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
    src = sys.argv[1] if len(sys.argv) > 1 else "merged.json"
    out = sys.argv[2] if len(sys.argv) > 2 else "out"
    with open(src, encoding="utf-8") as f:
        projects = json.load(f)
    os.makedirs(out, exist_ok=True)
    for theme in ("dark", "light"):
        with open(os.path.join(out, f"projects-{theme}.svg"), "w", encoding="utf-8") as f:
            f.write(panel(projects, theme))
    print(f"generated {len(projects)} project cards")


if __name__ == "__main__":
    main()
