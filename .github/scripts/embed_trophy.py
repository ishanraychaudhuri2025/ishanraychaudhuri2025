from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'trophy.png'
X, Y, W, H = 940, 124, 202, 442

if not SOURCE.exists():
    raise SystemExit('root trophy.png is missing')

# trophy.png is the exact cabinet image supplied by the user.
# Do not redraw, trace, crop, recolor, or add badges.
new_image = (
    f'<image id="trophy-cabinet" x="{X}" y="{Y}" width="{W}" height="{H}" '
    f'preserveAspectRatio="xMidYMid meet" href="trophy.png"/>'
)

for name in ('dark.svg', 'light.svg'):
    path = ROOT / name
    svg = path.read_text(encoding='utf-8')
    marker = '<g id="trophy-cabinet"'
    start = svg.lower().find(marker.lower())

    if start >= 0:
        end = svg.lower().rfind('</svg>')
        if end <= start:
            raise SystemExit(f'{name}: malformed SVG around trophy cabinet')
        svg = svg[:start].rstrip() + '\n\n' + new_image + '\n' + svg[end:]
    else:
        idx = svg.lower().rfind('</svg>')
        if idx < 0:
            raise SystemExit(f'{name}: missing closing svg tag')
        svg = svg[:idx] + '\n' + new_image + '\n' + svg[idx:]

    path.write_text(svg, encoding='utf-8')

print('Embedded the exact repository trophy.png in dark.svg and light.svg')
