import random
random.seed(7)
W,H = 860,280
KATA = "アカサタナハマヤラワイキシチニヒミリヰウクスツヌフムユルグズヅブプ"
HEX = "0123456789abcdef"
cols = 43
colw = W/cols
rows = 15
rowh = 20

def esc(c):
    return {"&":"&amp;","<":"&lt;",">":"&gt;"}.get(c,c)

parts = []
parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace">')
parts.append('''<defs>
  <linearGradient id="title" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#7E37F9"/><stop offset="0.5" stop-color="#B48EF7"/><stop offset="1" stop-color="#E568C4"/>
  </linearGradient>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#0b0f17"/><stop offset="1" stop-color="#0f1524"/>
  </linearGradient>
  <radialGradient id="glow" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="#7E37F9" stop-opacity="0.35"/><stop offset="1" stop-color="#7E37F9" stop-opacity="0"/>
  </radialGradient>
  <filter id="neon" x="-40%" y="-40%" width="180%" height="180%">
    <feGaussianBlur stdDeviation="3.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
</defs>''')
parts.append(f'<rect width="{W}" height="{H}" fill="url(#sky)"/>')
parts.append(f'<ellipse cx="{W/2}" cy="{H/2}" rx="{W/2}" ry="{H/1.6}" fill="url(#glow)"/>')

# matrix rain columns
parts.append('<g font-size="15" font-weight="500">')
for c in range(cols):
    x = round(c*colw + 3, 1)
    dur = round(random.uniform(4.5, 9.5), 2)
    begin = round(random.uniform(-9, 0), 2)
    span = rows*rowh + H
    chars = []
    for r in range(rows):
        ch = random.choice(KATA) if random.random()<0.6 else random.choice(HEX)
        y = r*rowh
        # head char brighter
        op = 0.85 if r==rows-1 else round(0.10 + 0.20*(r/rows), 2)
        fill = "#38f9d7" if r==rows-1 else ("#7E37F9" if random.random()<0.5 else "#3a4f7a")
        chars.append(f'<text x="{x}" y="{y}" fill="{fill}" opacity="{op}">{esc(ch)}</text>')
    inner = "".join(chars)
    parts.append(
        f'<g transform="translate(0,-{rows*rowh})">{inner}'
        f'<animateTransform attributeName="transform" type="translate" '
        f'from="0,-{rows*rowh}" to="0,{H}" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/></g>'
    )
parts.append('</g>')

# scanlines
parts.append(f'<rect width="{W}" height="{H}" fill="url(#scan)" opacity="0"/>')

# center glass panel
pw,ph = 560,120
px,py = (W-pw)/2, (H-ph)/2
parts.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="14" fill="#0b0f17" opacity="0.68" stroke="#7E37F9" stroke-opacity="0.5"/>')
# prompt line
parts.append(f'<text x="{W/2}" y="{py+42}" text-anchor="middle" font-size="15" fill="#5b6784">yomananchill@0xmanan:~$ <tspan fill="#38f9d7">whoami</tspan></text>')
# title
parts.append(f'<text x="{W/2}" y="{py+82}" text-anchor="middle" font-size="44" font-weight="800" fill="url(#title)" filter="url(#neon)" letter-spacing="1">security researcher</text>')
# cursor blink + subtitle
parts.append(f'<text x="{W/2}" y="{py+108}" text-anchor="middle" font-size="13" fill="#8b93a7">reads other people’s code until it breaks '
             f'<tspan fill="#E568C4">█<animate attributeName="opacity" values="1;1;0;0" dur="1s" repeatCount="indefinite"/></tspan></text>')

parts.append('</svg>')
open("banner.svg","w").write("\n".join(parts))
print("bytes:", len(open("banner.svg","rb").read()))
