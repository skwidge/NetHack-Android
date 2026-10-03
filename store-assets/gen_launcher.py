"""Render the adaptive launcher icon layers from the store icon design.

Layers are drawn on a 432px canvas (108dp at xxxhdpi). The visible area of an
adaptive icon is the central 72dp (288px), which maps to the 512px store icon,
so everything is scaled by 288/512. Run from the repo root.
"""
import math, os, subprocess
from PIL import Image, ImageDraw

RES = 'sys/android/app/res'
TMP = 'store-assets/build'
C = 432; K = 288 / 512; MID = C / 2
FONT = 'font-family="DejaVu Sans Mono" font-weight="bold"'
os.makedirs(TMP, exist_ok=True)

def at(fill, glow):
    f = ' filter="url(#glow)"' if glow else ''
    return (f'<text x="{MID}" y="{MID}" dy="0.36em" {FONT} font-size="{340*K:.1f}" '
            f'fill="{fill}" text-anchor="middle"{f}>@</text>')

GLOW = f'''<filter id="glow" filterUnits="userSpaceOnUse" x="0" y="0" width="{C}" height="{C}">
  <feGaussianBlur in="SourceAlpha" stdDeviation="{16*K:.1f}" result="b"/>
  <feFlood flood-color="#ff9a2e" flood-opacity="0.85"/>
  <feComposite in2="b" operator="in" result="g"/>
  <feMerge><feMergeNode in="g"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>'''

def background():
    dots = []
    step = 54 * K
    n = int(MID // step) + 1
    for i in range(-n, n + 1):
        for j in range(-n, n + 1):
            x = MID + i * step; y = MID + j * step
            d = math.hypot(x - MID, y - MID) / K
            if d < 180: continue
            op = max(0.0, 0.75 - (d - 180) / 260)
            if op < 0.05: continue
            dots.append(f'<text x="{x:.1f}" y="{y + 15*K:.1f}" fill-opacity="{op:.2f}">.</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{C}" height="{C}">
<defs><radialGradient id="t" cx="50%" cy="50%" r="{62*512/432*K:.1f}%">
  <stop offset="0" stop-color="#4a3216"/><stop offset="0.5" stop-color="#1c140b"/>
  <stop offset="1" stop-color="#0b0907"/></radialGradient></defs>
<rect width="{C}" height="{C}" fill="url(#t)"/>
<g {FONT} font-size="{44*K:.1f}" fill="#b8a27c" text-anchor="middle">{"".join(dots)}</g>
</svg>'''

LAYERS = {
    'background': background(),
    'foreground': f'<svg xmlns="http://www.w3.org/2000/svg" width="{C}" height="{C}"><defs>{GLOW}</defs>{at("#fff3d6", True)}</svg>',
    'monochrome': f'<svg xmlns="http://www.w3.org/2000/svg" width="{C}" height="{C}">{at("#ffffff", False)}</svg>',
}
DENS = {'mdpi': 1, 'hdpi': 1.5, 'xhdpi': 2, 'xxhdpi': 3, 'xxxhdpi': 4}

full = {}
for name, svg in LAYERS.items():
    src = f'{TMP}/{name}.svg'; png = f'{TMP}/{name}.png'
    open(src, 'w').write(svg)
    subprocess.run(['inkscape', src, '--export-text-to-path', '--export-type=png',
                    f'--export-filename={png}', '-w', str(C), '-h', str(C)],
                   check=True, capture_output=True)
    full[name] = Image.open(png).convert('RGBA')

for dens, s in DENS.items():
    d = f'{RES}/mipmap-{dens}'; os.makedirs(d, exist_ok=True)
    for name, im in full.items():
        im.resize((round(108 * s),) * 2, Image.LANCZOS).save(f'{d}/ic_launcher_{name}.png', optimize=True)
    # Legacy icon for API 24-25: the visible 72dp, as a rounded square at 48dp
    comp = Image.alpha_composite(full['background'], full['foreground'])
    crop = comp.crop((72, 72, 360, 360))
    size = round(48 * s)
    icon = crop.resize((size, size), Image.LANCZOS)
    mask = Image.new('L', (size * 4, size * 4), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size * 4 - 1, size * 4 - 1), radius=size * 4 * 0.18, fill=255)
    icon.putalpha(mask.resize((size, size), Image.LANCZOS))
    icon.save(f'{d}/ic_launcher.png', optimize=True)
