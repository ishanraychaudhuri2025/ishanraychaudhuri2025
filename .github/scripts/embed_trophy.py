from pathlib import Path
import re

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

    # Remove any standalone legacy cabinet image first. This is important
    # because older revisions could contain an image before the old group.
    svg = re.sub(
        r'\s*<image\b[^>]*\bid=["\']trophy-cabinet["\'][^>]*/>\s*',
        '\n',
        svg,
        flags=re.DOTALL | re.IGNORECASE,
    )

    # The trophy cabinet is always the final generated block in these SVGs.
    # Remove everything from the first legacy cabinet group to </svg>, then
    # append exactly one direct reference to the repository PNG.
    marker = '<g id="trophy-cabinet"'
    start = svg.lower().find(marker.lower())
    end = svg.lower().rfind('</svg>')

    if start >= 0:
        if end <= start:
            raise SystemExit(f'{name}: malformed SVG around trophy cabinet')
        svg = svg[:start].rstrip() + '\n\n' + new_image + '\n' + svg[end:]
    else:
        if end < 0:
            raise SystemExit(f'{name}: missing closing svg tag')
        svg = svg[:end] + '\n' + new_image + '\n' + svg[end:]

    path.write_text(svg, encoding='utf-8')

print('Embedded exactly one direct reference to trophy.png in dark.svg and light.svg')
