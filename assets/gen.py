#!/usr/bin/env python3
"""
Profile art for github.com/yomananchill  -  phosphor-terminal theme.
Green-on-black CRT: scanlines, phosphor glow, monospace, block cursor.
One warm amber reserved for high-severity accents. Animation via SMIL so it
survives GitHub's image proxy. No external fonts.  python3 gen.py -> ../out/*.svg
"""
import os, random, html

OUT = os.path.join(os.path.dirname(__file__), "..", "out")
os.makedirs(OUT, exist_ok=True)

# ---- phosphor palette ----------------------------------------------------
BG   = "#080b08"   # tube black, faint green cast
BG2  = "#0a0f0a"
PANEL= "#0a0e0a"
GRN  = "#8ce39a"   # bright phosphor
GRN2 = "#4fae63"   # mid
DIM  = "#356b43"   # dim traces
FAINT= "#20402a"   # scanline / faint text
INK  = "#c8f2cf"   # brightest text
MUT  = "#5f8f6b"
LINE = "#152418"
AMBER= "#e8b84b"   # the one warm accent (high severity)
AMBER2="#c99a3a"
MONO = '"JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, Consolas, monospace'

def esc(s): return html.escape(str(s), quote=True)
def wf(name, body): open(os.path.join(OUT,name),"w").write(body); return len(body)

def defs():
    return f'''
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{BG}"/><stop offset="1" stop-color="{BG2}"/>
  </linearGradient>
  <radialGradient id="vig" cx=".5" cy=".5" r=".75">
    <stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".55"/>
  </radialGradient>
  <radialGradient id="glow" cx=".5" cy=".42" r=".6">
    <stop offset="0" stop-color="{GRN}" stop-opacity=".10"/><stop offset="1" stop-color="{GRN}" stop-opacity="0"/>
  </radialGradient>
  <filter id="phos" x="-30%" y="-30%" width="160%" height="160%">
    <feGaussianBlur stdDeviation="1.4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="soft"><feGaussianBlur stdDeviation="5"/></filter>
  <pattern id="scan" width="3" height="3" patternUnits="userSpaceOnUse">
    <rect width="3" height="1" fill="#000" fill-opacity=".22"/>
  </pattern>
'''

def scanline(W,H,rx=0):
    return f'<rect width="{W}" height="{H}" rx="{rx}" fill="url(#scan)" pointer-events="none"/>'

# =========================================================================
# HERO
# =========================================================================
def hero():
    W,H=1000,300
    HEX="0123456789abcdef"; GL="01<>/\\[]{}=+*.:$#"
    random.seed(23)
    p=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family=\'{MONO}\'>']
    p.append(f'<defs>{defs()}<clipPath id="fr"><rect width="{W}" height="{H}" rx="14"/></clipPath></defs>')
    p.append(f'<g clip-path="url(#fr)">')
    p.append(f'<rect width="{W}" height="{H}" fill="url(#sky)"/>')
    p.append(f'<ellipse cx="{W/2}" cy="{H*0.44}" rx="{W*0.5}" ry="{H*0.85}" fill="url(#glow)"/>')

    # green code rain (monochrome, dim so the panel reads on top)
    cols=52; colw=W/cols; rows=16; rowh=19
    p.append('<g font-size="13">')
    for c in range(cols):
        x=round(c*colw+2,1); dur=round(random.uniform(6,13),2); begin=round(random.uniform(-13,0),2)
        cells=[]
        for r in range(rows):
            ch=random.choice(HEX) if random.random()<0.55 else random.choice(GL)
            head=(r==rows-1)
            op=0.62 if head else round(0.04+0.11*(r/rows),3)
            fill=GRN if head else (GRN2 if random.random()<0.4 else DIM)
            cells.append(f'<text x="{x}" y="{r*rowh}" fill="{fill}" opacity="{op}">{esc(ch)}</text>')
        p.append(f'<g transform="translate(0,-{rows*rowh})">{"".join(cells)}'
                 f'<animateTransform attributeName="transform" type="translate" from="0,-{rows*rowh}" to="0,{H}" '
                 f'dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/></g>')
    p.append('</g>')

    # CRT terminal window
    pw,ph=660,150; px,py=(W-pw)/2,(H-ph)/2-4
    p.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="10" fill="#060806" opacity=".82" stroke="{GRN2}" stroke-opacity=".45"/>')
    p.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="10" fill="none" stroke="{GRN}" stroke-opacity=".18" filter="url(#soft)"/>')
    # titlebar dots
    for i,cc in enumerate([DIM,DIM,GRN2]):
        p.append(f'<circle cx="{px+18+i*16}" cy="{py+16}" r="4" fill="{cc}"/>')
    p.append(f'<text x="{px+pw-16}" y="{py+20}" text-anchor="end" font-size="11" fill="{FAINT}">tty1 - 80x24</text>')
    cx=W/2
    p.append(f'<text x="{cx}" y="{py+52}" text-anchor="middle" font-size="14" fill="{MUT}">'
             f'yomananchill@0xmanan:~$ <tspan fill="{GRN}">whoami</tspan></text>')
    ty=py+96
    p.append(f'<text x="{cx}" y="{ty}" text-anchor="middle" font-size="42" font-weight="800" letter-spacing="1" '
             f'fill="{GRN}" filter="url(#phos)">security researcher</text>')
    p.append(f'<text x="{cx}" y="{py+124}" text-anchor="middle" font-size="13" fill="{MUT}">'
             f'the layer under the application '
             f'<tspan fill="{GRN}">█<animate attributeName="fill-opacity" values="1;1;0;0" dur="1s" repeatCount="indefinite"/></tspan></text>')

    p.append(scanline(W,H))
    p.append(f'<rect width="{W}" height="{H}" fill="url(#vig)"/>')
    # flicker
    p.append(f'<rect width="{W}" height="{H}" fill="{GRN}" opacity="0">'
             f'<animate attributeName="opacity" values="0;0;0.015;0;0.008;0" dur="5s" repeatCount="indefinite"/></rect>')
    p.append('</g></svg>')
    return "\n".join(p)

# =========================================================================
# DISCLOSURE RECORD
# =========================================================================
def sev_color(sev):
    return {"critical":AMBER,"high":GRN,"medium":GRN2}[sev]

def record():
    rows=[
        ("CVE-2026-1462","keras-team/keras","Deserialization","8.8","critical"),
        ("CVE-2026-1117","parisneo/lollms","Broken Access Control","8.2","critical"),
        ("CVE-2025-6209","run-llama/llama_index","Path Traversal","7.5","high"),
        ("CVE-2026-2393","mlflow/mlflow","SSRF","7.1","high"),
        ("CVE-2025-6210","run-llama/llama_index","Path Traversal","6.2","medium"),
    ]
    W=1000; padx=26; top=88; rh=58; H=top+rh*len(rows)+64
    p=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family=\'{MONO}\'>']
    p.append(f'<defs>{defs()}</defs>')
    p.append(f'<rect width="{W}" height="{H}" rx="12" fill="{PANEL}" stroke="{LINE}"/>')
    p.append(f'<rect width="{W}" height="{H}" rx="12" fill="url(#glow)"/>')
    p.append(f'<text x="{padx}" y="40" font-size="18" font-weight="800" fill="{INK}">'
             f'<tspan fill="{GRN2}">~/</tspan> disclosure record</text>')
    p.append(f'<text x="{padx}" y="62" font-size="12" fill="{MUT}">identifiers assigned to me · 13 writeups on the record · all fixed upstream</text>')
    p.append(f'<text x="{W-padx}" y="40" text-anchor="end" font-size="11.5" fill="{FAINT}">$ sort -k5 -rn cve.log</text>')
    p.append(f'<line x1="{padx}" y1="{top-14}" x2="{W-padx}" y2="{top-14}" stroke="{LINE}"/>')
    barx=690; barw=W-padx-barx-56
    for i,(cve,proj,cls,cvss,sev) in enumerate(rows):
        y=top+i*rh; cy=y+rh/2; col=sev_color(sev)
        p.append(f'<circle cx="{padx+7}" cy="{cy}" r="4.5" fill="{col}"/>'
                 f'<circle cx="{padx+7}" cy="{cy}" r="4.5" fill="none" stroke="{col}" stroke-opacity=".6">'
                 f'<animate attributeName="r" values="4.5;11;4.5" dur="3.2s" begin="{i*0.4}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="stroke-opacity" values=".6;0;.6" dur="3.2s" begin="{i*0.4}s" repeatCount="indefinite"/></circle>')
        p.append(f'<text x="{padx+24}" y="{cy-3}" font-size="16" font-weight="700" fill="{INK}">{cve}</text>')
        p.append(f'<text x="{padx+24}" y="{cy+15}" font-size="11.5" fill="{DIM}">{esc(proj)}</text>')
        p.append(f'<text x="358" y="{cy-3}" font-size="13" fill="{GRN}">{esc(cls)}</text>')
        p.append(f'<text x="358" y="{cy+15}" font-size="10.5" fill="{MUT}">{sev.upper()}</text>')
        frac=float(cvss)/10.0
        p.append(f'<rect x="{barx}" y="{cy-5}" width="{barw}" height="7" rx="3.5" fill="#060806" stroke="{LINE}"/>')
        p.append(f'<rect x="{barx}" y="{cy-5}" width="0" height="7" rx="3.5" fill="{col}">'
                 f'<animate attributeName="width" values="0;{barw*frac:.0f}" dur="1.1s" begin="{0.2+i*0.15}s" fill="freeze" calcMode="spline" keySplines="0 0 .2 1"/></rect>')
        p.append(f'<text x="{W-padx}" y="{cy+4}" text-anchor="end" font-size="15" font-weight="700" fill="{col}">{cvss}</text>')
        if i<len(rows)-1:
            p.append(f'<line x1="{padx}" y1="{y+rh}" x2="{W-padx}" y2="{y+rh}" stroke="{LINE}" stroke-opacity=".7"/>')
    fy=top+rh*len(rows)+28
    p.append(f'<line x1="{padx}" y1="{fy-18}" x2="{W-padx}" y2="{fy-18}" stroke="{LINE}"/>')
    p.append(f'<text x="{padx}" y="{fy+6}" font-size="12" fill="{MUT}">8 more on the record, including finds tracked upstream under another reporter’s id.</text>')
    p.append(f'<text x="{W-padx}" y="{fy+6}" text-anchor="end" font-size="12" font-weight="700" fill="{GRN}">yomananchill.github.io →</text>')
    p.append(scanline(W,H,12))
    p.append('</svg>')
    return "\n".join(p)

# =========================================================================
# LOADOUT
# =========================================================================
def chip(x,y,label,fg,pad=11,fs=12,h=24):
    wd=len(label)*fs*0.62+pad*2
    return (f'<g><rect x="{x}" y="{y}" width="{wd:.0f}" height="{h}" rx="4" fill="{fg}" fill-opacity=".08" '
            f'stroke="{fg}" stroke-opacity=".45"/>'
            f'<text x="{x+wd/2:.0f}" y="{y+h/2+4}" text-anchor="middle" font-size="{fs}" font-weight="600" fill="{fg}">{esc(label)}</text></g>'), wd

def flow(x0,y0,items,maxw,gap=9,lh=34):
    out=[]; x=x0; y=y0
    for label,fg in items:
        g,wd=chip(x,y,label,fg)
        if x+wd>x0+maxw:
            x=x0; y+=lh; g,wd=chip(x,y,label,fg)
        out.append(g); x+=wd+gap
    return "\n".join(out), y

def loadout():
    W=1000; padx=26; colgap=30; colw=(W-padx*2-colgap)/2
    langs=[("Python",GRN),("C",GRN),("C++",GRN),("Go",GRN),("Rust",GRN),("Bash",GRN)]
    tools=[("Burp Suite",GRN2),("Ghidra",GRN2),("Semgrep",GRN2),("CodeQL",GRN2),("Frida",GRN2),("Docker",GRN2),("Linux",GRN2)]
    offense=[("CRTO",GRN),("CRT",GRN),("CRTA",GRN),("PT1",GRN),("eJPT",GRN),("ACP",GRN)]
    defense=[("CNSP",AMBER),("CAP",AMBER)]
    Lx=padx; Rx=padx+colw+colgap
    cap=lambda x,y,t: f'<text x="{x}" y="{y}" font-size="10.5" font-weight="700" letter-spacing="1.5" fill="{DIM}">{t}</text>'
    lang_g,ly=flow(Lx,72,langs,colw); tool_g,ty=flow(Lx,ly+52,tools,colw)
    off_g,oy=flow(Rx,72,offense,colw); def_g,dy=flow(Rx,oy+52,defense,colw)
    H=max(ty,dy)+34
    p=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family=\'{MONO}\'>']
    p.append(f'<defs>{defs()}</defs>')
    p.append(f'<rect width="{W}" height="{H}" rx="12" fill="{PANEL}" stroke="{LINE}"/>')
    p.append(f'<rect width="{W}" height="{H}" rx="12" fill="url(#glow)"/>')
    p.append(f'<line x1="{Rx-colgap/2}" y1="20" x2="{Rx-colgap/2}" y2="{H-20}" stroke="{LINE}"/>')
    p.append(f'<text x="{Lx}" y="40" font-size="16" font-weight="800" fill="{INK}"><tspan fill="{GRN2}">~/</tspan> arsenal</text>')
    p.append(f'<text x="{Rx}" y="40" font-size="16" font-weight="800" fill="{INK}"><tspan fill="{GRN2}">~/</tspan> clearances <tspan font-size="11" fill="{DIM}">· 8 held</tspan></text>')
    p.append(cap(Lx,60,"LANGUAGES")); p.append(lang_g)
    p.append(cap(Lx,ly+40,"TOOLING")); p.append(tool_g)
    p.append(cap(Rx,60,"OFFENSIVE")); p.append(off_g)
    p.append(cap(Rx,oy+40,"DEFENSIVE")); p.append(def_g)
    p.append(scanline(W,H,12))
    p.append('</svg>')
    return "\n".join(p)

# =========================================================================
# SCOPE marquee
# =========================================================================
def scope():
    names=["Chromium","Wireshark","llama.cpp","Redis","LibreOffice","ClamAV","OpenThread",
           "PowerShell","Protobuf","RE2","Brotli","oFono"]
    W=1000; H=50
    seq=" ".join(f"{n} //" for n in names)+"   "; line=seq*2
    p=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family=\'{MONO}\'>']
    p.append(f'<defs>{defs()}'
             f'<linearGradient id="fade" x1="0" y1="0" x2="1" y2="0">'
             f'<stop offset="0" stop-color="{PANEL}"/><stop offset=".07" stop-color="{PANEL}" stop-opacity="0"/>'
             f'<stop offset=".93" stop-color="{PANEL}" stop-opacity="0"/><stop offset="1" stop-color="{PANEL}"/></linearGradient>'
             f'<clipPath id="sc"><rect width="{W}" height="{H}" rx="10"/></clipPath></defs>')
    p.append(f'<rect width="{W}" height="{H}" rx="10" fill="{PANEL}" stroke="{LINE}"/>')
    p.append(f'<g clip-path="url(#sc)">')
    startx=150; tw=len(seq)*13*0.6
    p.append(f'<g font-size="13" fill="{MUT}" transform="translate({startx},0)"><text x="0" y="30">{esc(line)}'
             f'<animateTransform attributeName="transform" type="translate" from="{startx},0" to="{startx-tw:.0f},0" dur="28s" repeatCount="indefinite"/></text></g>')
    p.append(f'<rect width="{W}" height="{H}" fill="url(#fade)"/>')
    p.append(f'<rect x="0" y="0" width="132" height="{H}" fill="{PANEL}"/>')
    p.append(f'<circle cx="20" cy="25" r="4" fill="{GRN}"><animate attributeName="opacity" values="1;.2;1" dur="1.4s" repeatCount="indefinite"/></circle>')
    p.append(f'<text x="32" y="30" font-size="12" font-weight="700" letter-spacing="1" fill="{GRN}">SCANNING</text>')
    p.append(f'<line x1="132" y1="11" x2="132" y2="{H-11}" stroke="{LINE}"/>')
    p.append(scanline(W,H,10))
    p.append('</g></svg>')
    return "\n".join(p)

for nm,fn in [("hero",hero),("record",record),("loadout",loadout),("scope",scope)]:
    print(nm, wf(f"{nm}.svg", fn()),"b")
print("done ->", os.path.abspath(OUT))
