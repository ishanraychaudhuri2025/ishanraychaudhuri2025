from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]

for name in ("dark.svg", "light.svg"):
    path = ROOT / name
    text = path.read_text(encoding="utf-8")

    # Remove the generated trophy cabinet group, if present.
    text = re.sub(
        r'\s*<g\s+id=["\']trophy-cabinet["\'][^>]*>.*?</g>\s*',
        '\n',
        text,
        flags=re.DOTALL | re.IGNORECASE,
    )

    # Remove the direct PNG image reference used by the later implementation.
    text = re.sub(
        r'\s*<image\s+id=["\']trophy-cabinet["\'][^>]*/>\s*',
        '\n',
        text,
        flags=re.DOTALL | re.IGNORECASE,
    )

    path.write_text(text, encoding="utf-8")

print("Removed all trophy cabinet markup from dark.svg and light.svg")
