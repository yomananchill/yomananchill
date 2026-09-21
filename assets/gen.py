#!/usr/bin/env python3
"""
Profile art system for github.com/yomananchill.
Hand-authored animated SVGs, one shared palette + type + motion vocabulary.
No external fonts (monospace generic). Animation via SMIL so it survives
GitHub's image proxy. Run: python3 gen.py  -> writes ../out/*.svg
"""
import os, random, html

OUT = os.path.join(os.path.dirname(__file__), "..", "out")
os.makedirs(OUT, exist_ok=True)

# ---- palette -------------------------------------------------------------
BG0="#070a11"; BG1="#0b0f17"; BG2="#0f1524"; PANEL="#0c111c"
VIO="#7E37F9"; LIL="#B48EF7"; PINK="#E568C4"; CYAN="#38f9d7"; BLU="#38bdf8"
RED="#ff5470"; AMB="#f5a623"; YEL="#ffd056"
INK="#e6edf3"; MUT="#8b93a7"; FAINT="#5b6784"; LINE="#1c2333"
MONO='"JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, Consolas, monospace'

def esc(s): return html.escape(str(s), quote=True)
def w(name, body): open(os.path.join(OUT,name),"w").write(body); return len(body)

DEFS_COMMON = f'''
  <linearGradient id="title" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{VIO}"/><stop offset=".5" stop-color="{LIL}"/><stop offset="1" stop-color="{PINK}"/>
  </linearGradient>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{BG0}"/><stop offset="1" stop-color="{BG2}"/>
  </linearGradient>
  <radialGradient id="glow" cx=".5" cy=".42" r=".6">
    <stop offset="0" stop-color="{VIO}" stop-opacity=".33"/><stop offset="1" stop-color="{VIO}" stop-opacity="0"/>
  </radialGradient>
  <filter id="neon" x="-40%" y="-40%" width="180%" height="180%">
    <feGaussianBlur stdDeviation="2.6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="soft" x="-30%" y="-30%" width="160%" height="160%">
    <feGaussianBlur stdDeviation="6"/>
  </filter>
'''

# =========================================================================
# 1. HERO
# =========================================================================
def hero():
    W,H = 1000,320
    KATA="アカサタナハマヤラワイキシチニヒミリヰウクスツヌフムユルグズヅブプペポォ"
    HEX="0123456789abcdef"
    random.seed(11)
    p=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family=\'{MONO}\'>']
    p.append(f'<defs>{DEFS_COMMON}'
             f'<clipPath id="frame"><rect width="{W}" height="{H}" rx="16"/></clipPath></defs>')
    p.append(f'<g clip-path="url(#frame)">')
    p.append(f'<rect width="{W}" height="{H}" fill="url(#sky)"/>')
    p.append(f'<ellipse cx="{W/2}" cy="{H*0.44}" rx="{W*0.55}" ry="{H*0.8}" fill="url(#glow)"/>')

    # synthwave grid floor
    p.append(f'<g stroke="{VIO}" stroke-opacity=".18" stroke-width="1">')
    horizon=H*0.72
    for i in range(1,9):
        y=horizon+(H-horizon)*(i/9)**1.7
        p.append(f'<line x1="0" y1="{y:.1f}" x2="{W}" y2="{y:.1f}"/>')
    for i in range(-10,11):
        x=W/2+i*70
        p.append(f'<line x1="{W/2}" y1="{horizon}" x2="{x:.1f}" y2="{H}"/>')
    p.append('</g>')

    # matrix rain
    cols=50; colw=W/cols; rows=17; rowh=19
    p.append('<g font-size="14" font-weight="500">')
    for c in range(cols):
        x=round(c*colw+2,1); dur=round(random.uniform(5,11),2); begin=round(random.uniform(-11,0),2)
        chars=[]
        for r in range(rows):
            ch=random.choice(KATA) if random.random()<0.62 else random.choice(HEX)
            head=(r==rows-1)
            op = 0.9 if head else round(0.06+0.16*(r/rows),2)
            fill = CYAN if head else (VIO if random.random()<0.5 else "#33436e")
            chars.append(f'<text x="{x}" y="{r*rowh}" fill="{fill}" opacity="{op}">{esc(ch)}</text>')
        p.append(f'<g transform="translate(0,-{rows*rowh})">{"".join(chars)}'
                 f'<animateTransform attributeName="transform" type="translate" '
                 f'from="0,-{rows*rowh}" to="0,{H}" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/></g>')
    p.append('</g>')

    # scan sweep
    p.append(f'<rect x="-160" y="0" width="160" height="{H}" fill="{CYAN}" opacity="0.05">'
             f'<animate attributeName="x" values="-160;{W}" dur="6s" repeatCount="indefinite"/></rect>')

    # HUD panel
    pw,ph=640,150; px,py=(W-pw)/2,(H-ph)/2-6
    p.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="16" fill="{BG1}" opacity=".72" '
             f'stroke="{VIO}" stroke-opacity=".55"/>')
    p.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="16" fill="none" '
             f'stroke="{VIO}" stroke-opacity=".25" filter="url(#soft)"/>')
    cx=W/2
    p.append(f'<text x="{cx}" y="{py+34}" text-anchor="middle" font-size="14" fill="{FAINT}">'
             f'yomananchill@0xmanan:~$ <tspan fill="{CYAN}">whoami</tspan>'
             f'<tspan fill="{PINK}"> _<animate attributeName="fill-opacity" values="1;1;0;0" dur="1s" repeatCount="indefinite"/></tspan></text>')
    # glitchy title (3 offset copies)
    ty=py+82
    p.append(f'<g font-size="46" font-weight="800" letter-spacing="1">')
    p.append(f'<text x="{cx+1.5}" y="{ty}" text-anchor="middle" fill="{PINK}" opacity=".55">security researcher'
             f'<animate attributeName="opacity" values=".0;.55;.0;.35;.0" dur="7s" repeatCount="indefinite"/></text>')
    p.append(f'<text x="{cx-1.5}" y="{ty}" text-anchor="middle" fill="{CYAN}" opacity=".45">security researcher'
             f'<animate attributeName="opacity" values=".0;.0;.45;.0;.25;.0" dur="7s" repeatCount="indefinite"/></text>')
    p.append(f'<text x="{cx}" y="{ty}" text-anchor="middle" fill="url(#title)" filter="url(#neon)">security researcher</text>')
    p.append('</g>')
    p.append(f'<text x="{cx}" y="{py+112}" text-anchor="middle" font-size="13" fill="{MUT}">'
             f'reads other people’s code until it breaks</text>')
    # status pills
    p.append(f'<g font-size="11" font-weight="700">')
    p.append(f'<rect x="{px+18}" y="{py+ph-30}" width="128" height="20" rx="10" fill="{VIO}" opacity=".14"/>'
             f'<circle cx="{px+30}" cy="{py+ph-20}" r="3.5" fill="{CYAN}">'
             f'<animate attributeName="opacity" values="1;.3;1" dur="1.6s" repeatCount="indefinite"/></circle>'
             f'<text x="{px+40}" y="{py+ph-16}" fill="{CYAN}">STATUS: ACTIVE</text>')
    p.append(f'<text x="{px+pw-18}" y="{py+ph-16}" text-anchor="end" fill="{FAINT}">'
             f'BENGALURU · IN · loc 0x0M4N</text>')
    p.append('</g>')

    p.append('</g></svg>')
    return "\n".join(p)

# =========================================================================
# 2. DISCLOSURE KILL-LOG
# =========================================================================
def record():
    rows=[
        ("CVE-2026-1462","keras-team/keras","Deserialization","8.8",RED,"critical"),
        ("CVE-2026-1117","parisneo/lollms","Broken Access Control","8.2",RED,"critical"),
        ("CVE-2025-6209","run-llama/llama_index","Path Traversal","7.5",AMB,"high"),
        ("CVE-2026-2393","mlflow/mlflow","SSRF","7.1",AMB,"high"),
        ("CVE-2025-6210","run-llama/llama_index","Path Traversal","6.2",YEL,"medium"),
    ]
    W=1000; padx=26; top=86; rh=58; H=top+rh*len(rows)+66
    p=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family=\'{MONO}\'>']
    p.append(f'<defs>{DEFS_COMMON}</defs>')
    p.append(f'<rect width="{W}" height="{H}" rx="16" fill="{PANEL}" stroke="{LINE}"/>')
    p.append(f'<rect width="{W}" height="{H}" rx="16" fill="url(#glow)" opacity=".5"/>')
    # header
    p.append(f'<text x="{padx}" y="42" font-size="19" font-weight="800" fill="{INK}">~/ '
             f'<tspan fill="url(#title)">disclosure record</tspan></text>')
    p.append(f'<text x="{padx}" y="64" font-size="12" fill="{MUT}">identifiers assigned to me · 13 writeups published · every one fixed upstream</text>')
    p.append(f'<text x="{W-padx}" y="42" text-anchor="end" font-size="12" fill="{FAINT}">grep -r CVE ~/record | sort -k5 -rn</text>')
    # column ticks
    p.append(f'<line x1="{padx}" y1="{top-12}" x2="{W-padx}" y2="{top-12}" stroke="{LINE}"/>')
    barx=680; barw=W-padx-barx-64
    for i,(cve,proj,cls,cvss,col,sev) in enumerate(rows):
        y=top+i*rh; cy=y+rh/2
        p.append(f'<g>')
        # severity dot + pulse
        p.append(f'<circle cx="{padx+8}" cy="{cy}" r="5" fill="{col}"/>'
                 f'<circle cx="{padx+8}" cy="{cy}" r="5" fill="none" stroke="{col}" stroke-opacity=".7">'
                 f'<animate attributeName="r" values="5;12;5" dur="3s" begin="{i*0.4}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="stroke-opacity" values=".7;0;.7" dur="3s" begin="{i*0.4}s" repeatCount="indefinite"/></circle>')
        p.append(f'<text x="{padx+26}" y="{cy-3}" font-size="16" font-weight="700" fill="{INK}">{cve}</text>')
        p.append(f'<text x="{padx+26}" y="{cy+15}" font-size="11.5" fill="{FAINT}">{esc(proj)}</text>')
        p.append(f'<text x="360" y="{cy-3}" font-size="13" fill="{LIL}">{esc(cls)}</text>')
        p.append(f'<text x="360" y="{cy+15}" font-size="10.5" fill="{FAINT}">{sev.upper()}</text>')
        # cvss bar (animated fill)
        frac=float(cvss)/10.0
        p.append(f'<rect x="{barx}" y="{cy-5}" width="{barw}" height="8" rx="4" fill="{BG0}" stroke="{LINE}"/>')
        p.append(f'<rect x="{barx}" y="{cy-5}" width="0" height="8" rx="4" fill="{col}">'
                 f'<animate attributeName="width" values="0;{barw*frac:.0f}" dur="1.1s" begin="{0.2+i*0.15}s" fill="freeze" calcMode="spline" keySplines="0 0 .2 1"/></rect>')
        p.append(f'<text x="{W-padx}" y="{cy+4}" text-anchor="end" font-size="15" font-weight="700" fill="{col}">{cvss}</text>')
        if i<len(rows)-1:
            p.append(f'<line x1="{padx}" y1="{y+rh}" x2="{W-padx}" y2="{y+rh}" stroke="{LINE}" stroke-opacity=".6"/>')
        p.append('</g>')
    # footer
    fy=top+rh*len(rows)+30
    p.append(f'<line x1="{padx}" y1="{fy-18}" x2="{W-padx}" y2="{fy-18}" stroke="{LINE}"/>')
    p.append(f'<text x="{padx}" y="{fy+6}" font-size="12" fill="{MUT}">'
             f'8 more published in full on the record, including finds tracked upstream under another reporter’s id.</text>')
    p.append(f'<text x="{W-padx}" y="{fy+6}" text-anchor="end" font-size="12" font-weight="700" fill="{CYAN}">yomananchill.github.io →</text>')
    p.append('</svg>')
    return "\n".join(p)

# =========================================================================
# 3. LOADOUT (arsenal + clearances)
# =========================================================================
def chip(x,y,label,fg,pad=11,fs=12,h=24):
    tw=len(label)*fs*0.62; wd=tw+pad*2
    g=(f'<g>'
       f'<rect x="{x}" y="{y}" width="{wd:.0f}" height="{h}" rx="{h/2}" fill="{fg}" fill-opacity=".12" stroke="{fg}" stroke-opacity=".5"/>'
       f'<text x="{x+wd/2:.0f}" y="{y+h/2+4}" text-anchor="middle" font-size="{fs}" font-weight="600" fill="{fg}">{esc(label)}</text>'
       f'</g>')
    return g, wd

def flow(x0,y0,items,maxw,gap=9,lh=34,**kw):
    out=[]; x=x0; y=y0
    for label,fg in items:
        g,wd=chip(x,y,label,fg,**kw)
        if x+wd>x0+maxw:
            x=x0; y+=lh
            g,wd=chip(x,y,label,fg,**kw)
        out.append(g); x+=wd+gap
    return "\n".join(out), y

def loadout():
    W=1000; padx=26; colgap=30; colw=(W-padx*2-colgap)/2
    langs=[("Python",VIO),("C",CYAN),("C++",PINK),("Go",BLU),("Rust",LIL),("Bash",CYAN)]
    tools=[("Burp Suite",RED),("Ghidra",VIO),("Semgrep",CYAN),("CodeQL",BLU),("Frida",PINK),("Docker",BLU),("Linux",LIL)]
    offense=[("CRTO",VIO),("CRT",PINK),("CRTA",LIL),("PT1",PINK),("eJPT",BLU),("ACP",CYAN)]
    defense=[("CNSP",CYAN),("CAP",VIO)]
    Lx=padx; Rx=padx+colw+colgap
    cap=lambda x,y,t: f'<text x="{x}" y="{y}" font-size="10.5" font-weight="700" letter-spacing="1.5" fill="{FAINT}">{t}</text>'
    # left column
    lang_g,ly=flow(Lx,72,langs,colw)
    tool_g,ty=flow(Lx,ly+52,tools,colw)
    # right column
    off_g,oy=flow(Rx,72,offense,colw)
    def_g,dy=flow(Rx,oy+52,defense,colw)
    H=max(ty,dy)+34
    p=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family=\'{MONO}\'>']
    p.append(f'<defs>{DEFS_COMMON}</defs>')
    p.append(f'<rect width="{W}" height="{H}" rx="16" fill="{PANEL}" stroke="{LINE}"/>')
    p.append(f'<rect width="{W}" height="{H}" rx="16" fill="url(#glow)" opacity=".4"/>')
    p.append(f'<line x1="{Rx-colgap/2}" y1="20" x2="{Rx-colgap/2}" y2="{H-20}" stroke="{LINE}"/>')
    p.append(f'<text x="{Lx}" y="40" font-size="16" font-weight="800" fill="{INK}">~/ <tspan fill="url(#title)">arsenal</tspan></text>')
    p.append(f'<text x="{Rx}" y="40" font-size="16" font-weight="800" fill="{INK}">~/ <tspan fill="url(#title)">clearances</tspan> <tspan font-size="11" fill="{FAINT}">· 8 held</tspan></text>')
    p.append(cap(Lx,60,"LANGUAGES")); p.append(lang_g)
    p.append(cap(Lx,ly+40,"TOOLING")); p.append(tool_g)
    p.append(cap(Rx,60,"OFFENSIVE")); p.append(off_g)
    p.append(cap(Rx,oy+40,"DEFENSIVE")); p.append(def_g)
    p.append('</svg>')
    return "\n".join(p)

# =========================================================================
# 4. SCOPE marquee (codebases under the lens)
# =========================================================================
def scope():
    names=["Chromium","Wireshark","llama.cpp","Redis","LibreOffice","ClamAV","OpenThread",
           "PowerShell","Protobuf","RE2","Brotli","oFono"]
    W=1000; H=52
    seq=" ".join(f"{n} //" for n in names)+"   "
    line=(seq*2)
    p=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family=\'{MONO}\'>']
    p.append(f'<defs>{DEFS_COMMON}'
             f'<linearGradient id="fade" x1="0" y1="0" x2="1" y2="0">'
             f'<stop offset="0" stop-color="{PANEL}"/><stop offset=".06" stop-color="{PANEL}" stop-opacity="0"/>'
             f'<stop offset=".94" stop-color="{PANEL}" stop-opacity="0"/><stop offset="1" stop-color="{PANEL}"/></linearGradient>'
             f'<clipPath id="sc"><rect width="{W}" height="{H}" rx="12"/></clipPath></defs>')
    p.append(f'<rect width="{W}" height="{H}" rx="12" fill="{PANEL}" stroke="{LINE}"/>')
    p.append(f'<g clip-path="url(#sc)">')
    startx=150
    tw=len(seq)*13*0.6
    p.append(f'<g font-size="13" fill="{MUT}" transform="translate({startx},0)">'
             f'<text x="0" y="31">{esc(line)}'
             f'<animateTransform attributeName="transform" type="translate" from="{startx},0" to="{startx-tw:.0f},0" dur="26s" repeatCount="indefinite"/></text></g>')
    p.append(f'<rect width="{W}" height="{H}" fill="url(#fade)"/>')
    # label sits on an opaque plate so the marquee slides cleanly behind it
    p.append(f'<rect x="0" y="0" width="132" height="{H}" rx="12" fill="{PANEL}"/>')
    p.append(f'<circle cx="20" cy="26" r="4" fill="{CYAN}"><animate attributeName="opacity" values="1;.25;1" dur="1.4s" repeatCount="indefinite"/></circle>')
    p.append(f'<text x="32" y="31" font-size="12" font-weight="700" letter-spacing="1" fill="{CYAN}">SCANNING</text>')
    p.append(f'<line x1="132" y1="12" x2="132" y2="{H-12}" stroke="{LINE}"/>')
    p.append('</g></svg>')
    return "\n".join(p)

for nm,fn in [("hero",hero),("record",record),("loadout",loadout),("scope",scope)]:
    b=w(f"{nm}.svg", fn()); print(f"{nm}.svg  {b}b")
print("done ->", os.path.abspath(OUT))
