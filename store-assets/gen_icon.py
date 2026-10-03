import math
dots=[]
for y in range(40,512,54):
  for x in range(40,512,54):
    d=math.hypot(x-256,y-256)
    if d<180: continue
    op=max(0.0,0.75-(d-180)/260)
    if op<0.05: continue
    dots.append(f'<text x="{x}" y="{y}" fill-opacity="{op:.2f}">.</text>')
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">
  <defs>
    <radialGradient id="torch" cx="50%" cy="50%" r="62%">
      <stop offset="0" stop-color="#4a3216"/>
      <stop offset="0.5" stop-color="#1c140b"/>
      <stop offset="1" stop-color="#0b0907"/>
    </radialGradient>
    <filter id="glow" filterUnits="userSpaceOnUse" x="0" y="0" width="512" height="512">
      <feGaussianBlur in="SourceAlpha" stdDeviation="16" result="b"/>
      <feFlood flood-color="#ff9a2e" flood-opacity="0.85"/>
      <feComposite in2="b" operator="in" result="g"/>
      <feMerge><feMergeNode in="g"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <rect width="512" height="512" fill="url(#torch)"/>
  <g font-family="DejaVu Sans Mono" font-weight="bold" font-size="44" fill="#b8a27c" text-anchor="middle">
    {"".join(dots)}
  </g>
  <text x="256" y="256" dy="0.36em" font-family="DejaVu Sans Mono" font-weight="bold" font-size="340"
        fill="#fff3d6" text-anchor="middle" filter="url(#glow)">@</text>
</svg>'''
open('icon.svg','w').write(svg)
