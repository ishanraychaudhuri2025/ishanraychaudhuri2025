from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'assets' / 'trophy-cabinet.svg'
X, Y, W, H = 950, 128, 180, 323

source = SOURCE.read_text(encoding='utf-8')
match = re.fullmatch(r'\s*<svg\b[^>]*>(.*)</svg>\s*', source, flags=re.DOTALL | re.IGNORECASE)
if not match:
    raise SystemExit('trophy-cabinet.svg is not a valid self-contained SVG')
inner = match.group(1).strip()

# Remove any previous generated trophy group, then insert the vector artwork.
old = re.compile(r'\s*<g id="trophy-cabinet"[^>]*>.*?</g>\s*', flags=re.DOTALL | re.IGNORECASE)
new_group = (
    f'<g id="trophy-cabinet" transform="translate({X} {Y}) scale({W/150:.6f} {H/269:.6f})">'
    f'{inner}</g>'
)

for name in ('dark.svg', 'light.svg'):
    path = ROOT / name
    svg = path.read_text(encoding='utf-8')
    svg = old.sub('\n', svg)
    if '</svg>' not in svg.lower():
        raise SystemExit(f'{name}: missing closing svg tag')
    idx = svg.lower().rfind('</svg>')
    svg = svg[:idx] + '\n' + new_group + '\n' + svg[idx:]
    path.write_text(svg, encoding='utf-8')

print('Embedded transparent vector trophy cabinet into dark.svg and light.svg')
