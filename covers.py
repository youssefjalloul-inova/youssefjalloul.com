"""Code-drawn cover illustrations for Insights articles and pages.

Every cover shares one frame (ink ground, grid, glow, corner brackets) so the
cast reads as one universe. Characters: Toastie (toaster), Ding (microwave),
Frosty (fridge), plus props for specific stories.
"""

EYE = '#FF3B2F'
LIME = '#C6F432'
SKY = '#4CC3FF'
ORANGE = '#FF7A2F'
INK = '#0A0B0E'
STEEL = '#2A2F3A'
EDGE = '#5A6170'


def frame(inner, glow=SKY, label=''):
    lab = f'<text x="64" y="574" font-family="JetBrains Mono,monospace" font-size="18" letter-spacing="3" fill="#7D8492">{label}</text>' if label else ''
    return f'''<svg class="cover" viewBox="0 0 1200 630" role="img" aria-label="{label.title() or 'Illustration'}" xmlns="http://www.w3.org/2000/svg">
<defs>
<radialGradient id="cg" cx="70%" cy="30%" r="70%"><stop offset="0" stop-color="{glow}" stop-opacity=".28"/><stop offset="1" stop-color="{glow}" stop-opacity="0"/></radialGradient>
<pattern id="cgrid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#fff" stroke-opacity=".05"/></pattern>
<linearGradient id="cgr" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{SKY}"/><stop offset="1" stop-color="{LIME}"/></linearGradient>
</defs>
<rect width="1200" height="630" fill="{INK}"/><rect width="1200" height="630" fill="url(#cgrid)"/><rect width="1200" height="630" fill="url(#cg)"/>
<g fill="none" stroke="url(#cgr)" stroke-width="6"><path d="M40 110V40h70M1090 40h70v70M1160 520v70h-70M110 590H40v-70"/></g>
{inner}
{lab}
</svg>'''


def eyes(cx, cy, gap=40, r=11):
    return f'<g class="c-eye"><circle cx="{cx-gap/2}" cy="{cy}" r="{r}" fill="{EYE}"/><circle cx="{cx+gap/2}" cy="{cy}" r="{r}" fill="{EYE}"/><circle cx="{cx-gap/2}" cy="{cy}" r="{r*2.2}" fill="{EYE}" opacity=".15"/><circle cx="{cx+gap/2}" cy="{cy}" r="{r*2.2}" fill="{EYE}" opacity=".15"/></g>'


def brows(cx, cy, gap=40):
    return f'<path d="M{cx-gap/2-18} {cy-24} L{cx-gap/2+12} {cy-14} M{cx+gap/2+18} {cy-24} L{cx+gap/2-12} {cy-14}" stroke="#F3F4F6" stroke-width="7" stroke-linecap="round"/>'


def toaster(x, y, s=1.0):
    return f'''<g transform="translate({x} {y}) scale({s})">
<g class="c-pop"><rect x="-95" y="-150" width="80" height="120" rx="18" fill="#C98A4B" stroke="#8A5A2B" stroke-width="5"/><rect x="15" y="-150" width="80" height="120" rx="18" fill="#C98A4B" stroke="#8A5A2B" stroke-width="5"/>
<path d="M-75 -120h40M35 -120h40" stroke="#8A5A2B" stroke-width="5" stroke-linecap="round"/></g>
<rect x="-160" y="-70" width="320" height="190" rx="52" fill="{STEEL}" stroke="{EDGE}" stroke-width="6"/>
<path d="M-100 -70v-6M100 -70v-6" stroke="{EDGE}" stroke-width="10"/>
<rect x="160" y="-10" width="26" height="70" rx="10" fill="{EDGE}"/>
{eyes(0, 25, 70, 13)}{brows(0, 25, 70)}
<path d="M-40 80 Q0 60 40 80" stroke="#F3F4F6" stroke-width="7" fill="none" stroke-linecap="round"/>
</g>'''


def microwave(x, y, s=1.0):
    return f'''<g transform="translate({x} {y}) scale({s})">
<rect x="-200" y="-130" width="400" height="260" rx="34" fill="{STEEL}" stroke="{EDGE}" stroke-width="6"/>
<rect class="c-hum" x="-170" y="-100" width="240" height="200" rx="22" fill="#14171D" stroke="{EDGE}" stroke-width="5"/>
{eyes(-50, -10, 80, 14)}{brows(-50, -10, 80)}
<path d="M-90 55 h80" stroke="#F3F4F6" stroke-width="7" stroke-linecap="round"/>
<circle cx="135" cy="-80" r="14" fill="{EYE}"/><path d="M110 -20h50M110 20h50M110 60h50" stroke="{EDGE}" stroke-width="8" stroke-linecap="round"/>
</g>'''


def fridge(x, y, s=1.0):
    return f'''<g transform="translate({x} {y}) scale({s})">
<rect x="-120" y="-230" width="240" height="460" rx="34" fill="{STEEL}" stroke="{EDGE}" stroke-width="6"/>
<path d="M-120 -60h240M80 -190v80M80 -20v110" stroke="{EDGE}" stroke-width="8" stroke-linecap="round"/>
{eyes(-20, -140, 70, 13)}{brows(-20, -140, 70)}
<path d="M-55 -100 q35 -14 70 0" stroke="#F3F4F6" stroke-width="7" fill="none" stroke-linecap="round"/>
<rect x="-85" y="20" width="110" height="70" rx="6" fill="#F3F4F6" transform="rotate(-6 -30 55)"/>
<path d="M-70 40h70M-70 56h55M-70 72h62" stroke="#0A0B0E" stroke-width="5" transform="rotate(-6 -30 55)"/>
</g>'''


def bubble(x, y, text, w=None, color=LIME):
    w = w or (len(text) * 19 + 60)
    return f'''<g transform="translate({x} {y})"><rect x="0" y="0" width="{w}" height="74" rx="37" fill="{color}"/><path d="M40 70 L28 104 L72 72Z" fill="{color}"/>
<text x="{w/2}" y="48" text-anchor="middle" font-family="Inter Tight,Inter,sans-serif" font-weight="800" font-size="32" fill="{INK}">{text}</text></g>'''


def doc(x, y, rot=0, s=1.0):
    return f'''<g transform="translate({x} {y}) rotate({rot}) scale({s})"><rect x="-60" y="-80" width="120" height="160" rx="10" fill="#F3F4F6"/><path d="M-40 -50h80M-40 -26h80M-40 -2h60M-40 22h74M-40 46h50" stroke="#9AA1AD" stroke-width="7" stroke-linecap="round"/>
<rect x="-50" y="-74" width="64" height="18" rx="4" fill="{EYE}"/><text x="-18" y="-60" text-anchor="middle" font-family="JetBrains Mono,monospace" font-size="12" font-weight="700" fill="#fff">SECRET</text></g>'''


def house(x, y, s=1.0):
    return f'''<g transform="translate({x} {y}) scale({s})"><path d="M-220 -20 L0 -200 L220 -20" fill="none" stroke="url(#cgr)" stroke-width="16" stroke-linejoin="round" stroke-linecap="round"/>
<rect x="-170" y="-40" width="340" height="250" rx="18" fill="#12151B" stroke="{EDGE}" stroke-width="6"/>
<rect x="-70" y="40" width="140" height="120" rx="16" fill="{STEEL}" stroke="{LIME}" stroke-width="6"/>
<path d="M-50 40v-24M0 40v-24M50 40v-24M-50 160v24M0 160v24M50 160v24M-70 70h-24M-70 130h-24M70 70h24M70 130h24" stroke="{LIME}" stroke-width="6" stroke-linecap="round"/>
<text x="0" y="114" text-anchor="middle" font-family="Inter Tight,sans-serif" font-weight="800" font-size="40" fill="{LIME}">AI</text>
<circle cx="120" cy="-2" r="12" fill="{LIME}"/></g>'''


def brain(x, y, s=1.0):
    return f'''<g transform="translate({x} {y}) scale({s})"><path d="M-150 20c-60 0-70-90-20-110 0-60 70-90 110-60 30-50 110-40 120 10 60-10 100 50 70 100 40 40 0 110-60 100-20 50-110 50-130 10-50 20-110-10-90-50z" fill="#F2A7B8" stroke="#B5687C" stroke-width="7"/>
<path d="M-80 -50c30 10 30 50 0 70M10 -80c-20 40 10 70 40 70M60 40c-30 0-50 30-30 60M-110 60c20-10 50 0 60 20" fill="none" stroke="#B5687C" stroke-width="7" stroke-linecap="round"/>
<path d="M150 120 C 230 160, 250 240, 340 230" fill="none" stroke="{EDGE}" stroke-width="12" stroke-linecap="round"/>
<g transform="translate(360 228)"><rect x="-10" y="-30" width="60" height="60" rx="10" fill="{STEEL}" stroke="{EDGE}" stroke-width="5"/><path d="M50 -14h30M50 14h30" stroke="{EDGE}" stroke-width="9" stroke-linecap="round"/></g>
<text x="250" y="320" font-family="JetBrains Mono,monospace" font-size="26" fill="{EYE}" font-weight="700">UNPLUGGED</text></g>'''


def tablets(x, y, s=1.0):
    t = lambda tx, lines: f'<g transform="translate({tx} 0)"><path d="M-110 200V-120a110 110 0 0 1 220 0V200z" fill="#B9B3A6" stroke="#7E776A" stroke-width="7"/>' + ''.join(f'<text x="-70" y="{-90+i*52}" font-family="Inter Tight,sans-serif" font-weight="800" font-size="34" fill="#4A453C">{l}</text>' for i, l in enumerate(lines)) + '</g>'
    return f'''<g transform="translate({x} {y}) scale({s})">{t(-125, ['I', 'II', 'III', 'IV', 'V'])}{t(125, ['VI', 'VII', 'VIII', 'IX', 'X'])}
<g transform="translate(0 -40) rotate(-14)"><rect x="-260" y="-26" width="520" height="52" rx="10" fill="{EYE}"/><text x="0" y="12" text-anchor="middle" font-family="JetBrains Mono,monospace" font-weight="700" font-size="30" fill="#fff">&#8212; NO EM DASHES &#8212;</text></g></g>'''


def spiral(x, y, s=1.0):
    path = 'M0 0' + ''.join(f' a{r} {r} 0 0 1 {(-1)**i * 2*r} 0' for i, r in enumerate(range(8, 150, 12)))
    return f'''<g transform="translate({x} {y}) scale({s})"><rect x="-170" y="-150" width="340" height="300" rx="70" fill="{STEEL}" stroke="{EDGE}" stroke-width="6"/>
<path d="M0 -150v-50" stroke="{EDGE}" stroke-width="10"/><circle cx="0" cy="-212" r="16" fill="{ORANGE}"/>
<g class="c-spin" transform="translate(-70 -10)"><path d="{path}" fill="none" stroke="{LIME}" stroke-width="6" transform="scale(.42)"/></g>
<g class="c-spin" transform="translate(70 -10)"><path d="{path}" fill="none" stroke="{LIME}" stroke-width="6" transform="scale(.42)"/></g>
<path d="M-50 90 q50 30 100 0" stroke="#F3F4F6" stroke-width="8" fill="none" stroke-linecap="round"/></g>
<g transform="translate({x+260} {y-150})"><path d="M0 0 l40 -70 30 0 -10 50 40 0 -60 80 10 -60z" fill="{LIME}"/></g>'''


def desert(x, y, s=1.0):
    return f'''<g transform="translate({x} {y}) scale({s})"><circle cx="230" cy="-170" r="90" fill="{ORANGE}" opacity=".9"/>
<path d="M-460 160 C -300 60, -160 70, 0 140 S 300 90, 460 150 V260 H-460Z" fill="#C9A06A"/>
<path d="M-460 210 C -260 150, -120 170, 60 220 S 340 170, 460 200 V260 H-460Z" fill="#A87F4B"/>
''' + ''.join(f'<rect x="{-300+i*130}" y="{-40 - (i%2)*60}" width="100" height="{200+(i%2)*60}" rx="8" fill="{STEEL}" stroke="{EDGE}" stroke-width="5"/>' + ''.join(f'<rect x="{-284+i*130}" y="{-20-(i%2)*60+k*34}" width="68" height="14" rx="4" fill="{SKY if (i+k)%3 else LIME}" opacity=".85"/>' for k in range(5)) for i in range(5)) + '</g>'


def magnifier(x, y, s=1.0):
    return f'''<g transform="translate({x} {y}) scale({s})"><circle cx="-40" cy="-30" r="150" fill="#12151B" stroke="url(#cgr)" stroke-width="22"/>
<path d="M70 80 L200 210" stroke="{EDGE}" stroke-width="44" stroke-linecap="round"/>
<text x="-40" y="10" text-anchor="middle" font-family="Inter Tight,sans-serif" font-weight="800" font-size="120" fill="{LIME}">A</text>
<text x="-40" y="80" text-anchor="middle" font-family="JetBrains Mono,monospace" font-size="22" fill="#7D8492">THE ANSWER</text></g>'''


def couch(x, y, s=1.0):
    return f'''<g transform="translate({x} {y}) scale({s})"><rect x="-260" y="40" width="520" height="130" rx="40" fill="#5B3A6E"/><rect x="-300" y="0" width="80" height="170" rx="36" fill="#6E4885"/><rect x="220" y="0" width="80" height="170" rx="36" fill="#6E4885"/>
<rect x="-210" y="-80" width="420" height="140" rx="40" fill="#6E4885"/>
<g transform="translate(-40 -10)"><circle cx="0" cy="-60" r="70" fill="#F2C9A0"/><path d="M-30 -60h20M10 -60h20" stroke="#3A2A20" stroke-width="7" stroke-linecap="round"/><path d="M-20 -25 q20 10 40 0" stroke="#3A2A20" stroke-width="6" fill="none"/>
<rect x="-90" y="10" width="180" height="90" rx="30" fill="{SKY}"/></g>
<g transform="translate(150 -40) rotate(10)"><rect x="-55" y="-90" width="110" height="180" rx="16" fill="{STEEL}" stroke="{EDGE}" stroke-width="5"/><text x="0" y="-30" text-anchor="middle" font-family="Inter Tight,sans-serif" font-weight="800" font-size="30" fill="{LIME}">AI</text><path d="M-30 0h60M-30 24h60M-30 48h40" stroke="#9AA1AD" stroke-width="6"/></g>
<text x="-200" y="-140" font-family="Inter Tight,sans-serif" font-weight="800" font-size="56" fill="#7D8492">z z z</text></g>'''


def agents(x, y, s=1.0):
    nodes = [(-250, -120), (-60, -200), (150, -140), (260, 40), (60, 120), (-170, 110), (0, -20)]
    lines = ''.join(f'<path d="M0 -20 L{nx} {ny}" stroke="{EDGE}" stroke-width="5"/>' for nx, ny in nodes[:-1])
    dots = ''.join(f'<g transform="translate({nx} {ny})"><rect x="-46" y="-40" width="92" height="80" rx="20" fill="{STEEL}" stroke="{[SKY, LIME, ORANGE][i % 3]}" stroke-width="5"/><circle cx="-14" cy="-4" r="7" fill="{[SKY, LIME, ORANGE][i % 3]}"/><circle cx="14" cy="-4" r="7" fill="{[SKY, LIME, ORANGE][i % 3]}"/><path d="M-14 18h28" stroke="#F3F4F6" stroke-width="5" stroke-linecap="round"/></g>' for i, (nx, ny) in enumerate(nodes[:-1]))
    return f'''<g transform="translate({x} {y}) scale({s})">{lines}{dots}<g transform="translate(0 -20)"><rect x="-80" y="-60" width="160" height="120" rx="26" fill="{LIME}"/><text x="0" y="16" text-anchor="middle" font-family="Inter Tight,sans-serif" font-weight="800" font-size="44" fill="{INK}">BLDR</text></g></g>'''


def leak(x, y, s=1.0):
    return f'''<g transform="translate({x} {y}) scale({s})">{doc(-160, -40, -8, 1.3)}{doc(-40, -70, 6, 1.3)}
<g transform="translate(150 -20)"><rect x="-90" y="-120" width="180" height="230" rx="24" fill="{STEEL}" stroke="{EDGE}" stroke-width="6"/><rect x="-60" y="-90" width="120" height="70" rx="10" fill="#14171D"/>
<text x="0" y="-45" text-anchor="middle" font-family="JetBrains Mono,monospace" font-size="20" fill="{LIME}">PASTE</text>
<path d="M-60 10h120M-60 40h120M-60 70h80" stroke="#9AA1AD" stroke-width="7" stroke-linecap="round"/></g>
<path d="M60 -10 C 90 -40, 100 -40, 60 -60" stroke="{EYE}" stroke-width="7" fill="none" stroke-dasharray="4 12" stroke-linecap="round"/>
<g fill="{SKY}"><path d="M140 140 q10 22 0 30 q-10 -8 0 -30z"/><path d="M180 160 q10 22 0 30 q-10 -8 0 -30z"/><path d="M110 175 q10 22 0 30 q-10 -8 0 -30z"/></g></g>'''


def coins(x, y, s=1.0):
    return f'''<g transform="translate({x} {y}) scale({s})">''' + ''.join(f'<g transform="translate({cx} {cy})"><ellipse cx="0" cy="0" rx="70" ry="22" fill="#B8860B"/><rect x="-70" y="-30" width="140" height="30" fill="#D4A017"/><ellipse cx="0" cy="-30" rx="70" ry="22" fill="#F2C94C"/><text x="0" y="-22" text-anchor="middle" font-family="Inter Tight,sans-serif" font-weight="800" font-size="22" fill="#8A6508">AI</text></g>' for cx, cy in [(-180, 120), (-180, 80), (-180, 40), (0, 120), (0, 80), (0, 40), (0, 0), (0, -40), (180, 120), (180, 80)]) + '<g transform="translate(140 -150)"><rect x="-60" y="-50" width="120" height="100" rx="18" fill="#12151B" stroke="url(#cgr)" stroke-width="6"/><path d="M-40 -50v-20M0 -50v-20M40 -50v-20M-40 50v20M0 50v20M40 50v20" stroke="#7BE0C9" stroke-width="6"/><text x="0" y="12" text-anchor="middle" font-family="JetBrains Mono,monospace" font-size="26" fill="#7BE0C9" font-weight="700">GPU</text></g></g>'


ART = {
    'toaster': lambda: toaster(760, 360, 1.25) + bubble(330, 150, 'Sure, stranger!', 330),
    'microwave': lambda: microwave(760, 330, 1.2) + bubble(260, 120, 'Ding! Yours?', 300, ORANGE),
    'fridge': lambda: fridge(820, 330, 1.0) + bubble(260, 150, 'I keep receipts.', 360, SKY),
    'trio': lambda: toaster(300, 380, .8) + microwave(640, 360, .75) + fridge(960, 330, .78),
    'house': lambda: house(760, 360, 1.1) + bubble(220, 140, 'Home grown.', 290),
    'leak': lambda: leak(700, 330, 1.05),
    'brain': lambda: brain(560, 300, 1.0),
    'tablets': lambda: tablets(640, 330, .95),
    'spiral': lambda: spiral(640, 330, 1.0),
    'desert': lambda: desert(640, 330, 1.0),
    'magnifier': lambda: magnifier(640, 320, 1.0) + bubble(120, 120, 'SEO? Cute.', 280, ORANGE),
    'couch': lambda: couch(640, 360, 1.0),
    'agents': lambda: agents(640, 330, 1.0),
    'coins': lambda: coins(560, 340, 1.0) + bubble(760, 110, 'Teraflops > tokens', 380),
}


_n = [0]


def cover(key, label=''):
    glow = {'toaster': ORANGE, 'fridge': SKY, 'microwave': ORANGE, 'leak': EYE, 'house': LIME, 'desert': ORANGE, 'coins': ORANGE}.get(key, SKY)
    _n[0] += 1
    u = f'{key}{_n[0]}'
    svg = frame(ART[key](), glow, label)
    for i in ('cgrid', 'cgr', 'cg'):
        svg = svg.replace(f'id="{i}"', f'id="{i}-{u}"').replace(f'url(#{i})', f'url(#{i}-{u})')
    return svg
