#!/usr/bin/env python3
"""Rebuild the small GitHub-compatible vector accents. Standard library only."""
from pathlib import Path
from random import Random

OUT = Path(__file__).resolve().parent
rng = Random(22)
parts = ['''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="108" viewBox="0 0 1200 108" role="img" aria-labelledby="title">
<title id="title">Night shift. Code, curiosity, repeat.</title>
<style>@media(prefers-reduced-motion:reduce){.bar{animation:none!important}}.bar{transform-box:fill-box;transform-origin:center bottom;animation:eq 1.8s ease-in-out infinite alternate}@keyframes eq{from{transform:scaleY(.35)}to{transform:scaleY(1)}}</style>
<rect x="1" y="1" width="1198" height="106" rx="8" fill="#151521" stroke="#34304a"/>
<rect x="1" y="1" width="4" height="106" rx="2" fill="#bca6ef"/>
<g font-family="monospace"><text x="32" y="41" font-size="12" letter-spacing="3" fill="#bca6ef">NIGHT SHIFT</text>
<text x="32" y="76" font-size="21" fill="#eee8f4">code, curiosity, repeat.</text>
<text x="1158" y="40" text-anchor="end" font-size="11" letter-spacing="2" fill="#b4a9c5">LO-FI MODE</text></g>''']
for i in range(38):
    height=rng.randint(9,39)
    parts.append(f'<rect class="bar" x="{746+i*11}" y="{82-height}" width="4" height="{height}" rx="1" fill="{["#9cdfcd","#bca6ef","#d89ab4"][i%3]}" style="animation-delay:-{rng.random()*3:.2f}s"/>')
parts.append('</svg>')
(OUT/'night-mode.svg').write_text('\n'.join(parts))
(OUT/'divider.svg').write_text('''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="16" viewBox="0 0 1200 16"><path d="M0 8h530m140 0h530" stroke="#454056"/><path d="m573 8 5-5 5 5-5 5Zm21 0 5-5 5 5-5 5Zm21 0 5-5 5 5-5 5Z" fill="#bca6ef"/></svg>''')
