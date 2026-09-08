from pathlib import Path
import base64
import re

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / '.github' / 'trophy-cabinet-source.b64'
ASSET = ROOT / 'assets' / 'trophy-cabinet.webp'
X, Y, W, H = 950, 132, 180, 323

b64 = ''.join(SOURCE.read_text(encoding='utf-8').split())
data = base64.b64decode(b64, validate=True)
ASSET.write_bytes(data)

image = f'<image id="trophy-cabinet" x="{X}" y="{Y}" width="{W}" height="{H}" preserveAspectRatio="xMidYMid meet" href="data:image/webp;base64,{base64.b64encode(data).decode()}"/>'
pattern = re.compile(r'\s*<image\s+id="trophy-cabinet"[^>]*/>', re.IGNORECASE)

for name in ('dark.svg', 'light.svg'):
    path = ROOT / name
    svg = path.read_text(encoding='utf-8')
    svg = pattern.sub('', svg)
    if '</svg>' not in svg:
        raise SystemExit(f'{name}: missing closing svg tag')
    svg = svg.replace('</svg>', image + '\n</svg>')
    path.write_text(svg, encoding='utf-8')

print(f'Embedded trophy cabinet into dark.svg and light.svg; asset bytes={len(data)}')
