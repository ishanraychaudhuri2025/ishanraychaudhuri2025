from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'trophy.png'
X, Y, W, H = 940, 124, 202, 442

if not SOURCE.exists():
    raise SystemExit('root trophy.png is missing')

# The uploaded trophy.png already contains the complete cabinet artwork:
# outer red border, transparent background, and all eight trophies.
# We embed that exact repository image by reference; no redraw, tracing,
# badge generation, cropping, recoloring, or other image transformation.
new_group = (
    f'<image id="trophy-cabinet" x="{X}" y="{Y}" width="{W}" height="{H}" '
    f'preserveAspectRatio="xMidYMid meet" href="trophy.png"/>'
)

for name in ('dark.svg', 'light.svg'):
    path = ROOT / name
    svg = path.read_text(encoding='utf-8')

    # Remove all previous trophy implementations, whether old vector groups,
    # embedded raster images, or generated variants.
    svg = re.sub(r'\s*<g\s+id="trophy-cabinet"[^>]*>.*?</g>\s*', '\n', svg, flags=re.DOTALL | re.IGNORECASE)
    svg = re.sub(r'\s*<image\s+id="trophy-cabinet"[^>]*/>\s*', '\n', svg, flags=re.DOTALL | re.IGNORECASE)
    svg = re.sub(r'\s*<image\s+[^>]*trophy-cabinet[^>]*/>\s*', '\n', svg, flags=re.DOTALL | re.IGNORECASE)

    idx = svg.lower().rfind('</svg>')
    if idx < 0:
        raise SystemExit(f'{name}: missing closing svg tag')

    svg = svg[:idx] + '\n' + new_group + '\n' + svg[idx:]
    path.write_text(svg, encoding='utf-8')

print('Embedded exactly the repository trophy.png into dark.svg and light.svg')
