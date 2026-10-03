MAP = [
  "-----------           ",
  "|.........|    ####   ",
  "|...$.....+#####  #   ",
  "|.....@...|       #   ",
  "|......d..|     --+---",
  "|.........|     |....|",
  "|...>.....|     |.F..|",
  "-----------     |....|",
  "                ------",
]
FS=32; CW=FS*0.602; LH=40; X0=572; Y0=102
col={'-':'#8d877c','|':'#8d877c','.':'#6f6250','#':'#5f5a52','+':'#b07a3a',
     '$':'#ffd84a','>':'#c8c2b5','d':'#f2efe6','F':'#5ee05a','@':'#fff3d6'}
lit=lambda r,c: r<=7 and c<=10
out=[]
for r,line in enumerate(MAP):
  for c,ch in enumerate(line):
    if ch==' ': continue
    x=X0+c*CW+CW/2; y=Y0+r*LH
    op = 1.0 if lit(r,c) else 0.55
    f = ' filter="url(#glow)"' if ch=='@' else ''
    out.append(f'<text x="{x:.1f}" y="{y}" fill="{col[ch]}" fill-opacity="{op}"{f}>{ch}</text>')
ax=X0+6*CW+CW/2; ay=Y0+3*LH-11
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="500" viewBox="0 0 1024 500">
  <defs>
    <radialGradient id="bg" cx="{ax/1024:.3f}" cy="{ay/500:.3f}" r="75%" gradientUnits="objectBoundingBox">
      <stop offset="0" stop-color="#4a3216"/>
      <stop offset="0.35" stop-color="#1c140b"/>
      <stop offset="1" stop-color="#0b0907"/>
    </radialGradient>
    <filter id="glow" filterUnits="userSpaceOnUse" x="0" y="0" width="1024" height="500">
      <feGaussianBlur in="SourceAlpha" stdDeviation="6" result="b"/>
      <feFlood flood-color="#ff9a2e" flood-opacity="0.8"/>
      <feComposite in2="b" operator="in" result="g"/>
      <feMerge><feMergeNode in="g"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="tglow" filterUnits="userSpaceOnUse" x="0" y="0" width="1024" height="500">
      <feGaussianBlur in="SourceAlpha" stdDeviation="10" result="b"/>
      <feFlood flood-color="#ff9a2e" flood-opacity="0.45"/>
      <feComposite in2="b" operator="in" result="g"/>
      <feMerge><feMergeNode in="g"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <rect width="1024" height="500" fill="url(#bg)"/>
  <g font-family="DejaVu Sans Mono" font-weight="bold" font-size="{FS}" text-anchor="middle">
    {"".join(out)}
  </g>
  <text x="70" y="250" font-family="DejaVu Sans Mono" font-weight="bold" font-size="92" fill="#fff3d6" filter="url(#tglow)">NetHack</text>
  <text x="74" y="304" font-family="Fira Sans" font-size="28" fill="#c9b898">The classic roguelike dungeon crawl</text>
</svg>'''
open('feature.svg','w').write(svg)
