"""Generate the profile README SVGs (Swiss International, theme-adaptive):
  assets/header-v2.svg  - type + rotating wireframe icosahedron (SMIL-baked 3D)
  assets/marquee-v2.svg - thin scrolling text strip, inset to the header grid
  assets/chip-*.svg     - link buttons matching the banner typography
Transparent backgrounds; ink/bone flips with prefers-color-scheme."""
import math

STYLE = """<style>
    :root { --ink: #12120F; }
    @media (prefers-color-scheme: dark) { :root { --ink: #ECEAE3; } }
    .ink { fill: var(--ink); }
    .mut { fill: var(--ink); fill-opacity: 0.5; }
    .rule { stroke: var(--ink); }
    .faint { stroke: var(--ink); stroke-opacity: 0.09; }
    .wire { stroke: var(--ink); fill: none; }
    .box { stroke: var(--ink); stroke-opacity: 0.4; fill: none; }
  </style>"""

MARGIN, WIDTH = 64, 1000
INNER = WIDTH - 2 * MARGIN  # 872

# --- icosahedron ---------------------------------------------------------
p = (1 + 5 ** 0.5) / 2
V = [(-1, p, 0), (1, p, 0), (-1, -p, 0), (1, -p, 0),
     (0, -1, p), (0, 1, p), (0, -1, -p), (0, 1, -p),
     (p, 0, -1), (p, 0, 1), (-p, 0, -1), (-p, 0, 1)]
norm = math.sqrt(1 + p * p)
V = [(x / norm, y / norm, z / norm) for x, y, z in V]

EDGES = set()
for i in range(12):
    d = sorted(range(12), key=lambda j: sum((V[i][k] - V[j][k]) ** 2 for k in range(3)))
    for j in d[1:6]:
        EDGES.add((min(i, j), max(i, j)))
EDGES = sorted(EDGES)

CX, CY, R = 800, 196, 138
TILT = 0.42
FRAMES = 72

def frame_path(t):
    a = 2 * math.pi * t
    ca, sa = math.cos(a), math.sin(a)
    ct, st = math.cos(TILT), math.sin(TILT)
    pts = []
    for x, y, z in V:
        x1, z1 = x * ca + z * sa, -x * sa + z * ca
        y1 = y * ct - z1 * st
        pts.append((round(CX + R * x1, 1), round(CY + R * y1, 1)))
    return " ".join(f"M{pts[i][0]} {pts[i][1]}L{pts[j][0]} {pts[j][1]}" for i, j in EDGES)

values = ";".join(frame_path(i / FRAMES) for i in range(FRAMES + 1))

grid = "".join(
    f'<line class="faint" x1="{MARGIN + i * (INNER / 12):.1f}" y1="30" x2="{MARGIN + i * (INNER / 12):.1f}" y2="370" stroke-width="1"/>'
    for i in range(13))

banner = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="400" viewBox="0 0 {WIDTH} 400" font-family="Helvetica, Arial, sans-serif" role="img" aria-label="Luke Zhang. Mechatronics Engineering, University of Waterloo. Code, design, music.">
  {STYLE}
  {grid}

  <text class="mut" x="{MARGIN}" y="58" font-size="12" letter-spacing="2">LZ·0826</text>
  <text class="mut" x="{WIDTH - MARGIN}" y="58" font-size="12" letter-spacing="2" text-anchor="end">43.4643° N, 80.5204° W</text>

  <path class="wire" stroke-width="1.4" stroke-linecap="round">
    <animate attributeName="d" dur="16s" repeatCount="indefinite" calcMode="linear" values="{values}"/>
  </path>

  <text class="ink" x="{MARGIN}" y="182" font-size="96" font-weight="bold" letter-spacing="-3">Luke</text>
  <text class="ink" x="{MARGIN}" y="272" font-size="96" font-weight="bold" letter-spacing="-3">Zhang</text>

  <line class="rule" x1="{MARGIN}" y1="308" x2="520" y2="308" stroke-width="1.5"/>

  <text class="ink" x="{MARGIN}" y="342" font-size="14.5" letter-spacing="3">MECHATRONICS ENGINEERING, UNIVERSITY OF WATERLOO</text>
  <text class="ink" x="{MARGIN}" y="368" font-size="14.5" letter-spacing="3">CODE / DESIGN / MUSIC</text>

  <text class="mut" x="{WIDTH - MARGIN}" y="368" font-size="12" letter-spacing="2" text-anchor="end">GRID 12 / ORTHO 0.42</text>
</svg>'''

# --- marquee (inset to the header's content box) -------------------------
PHRASE = "CODE ✦ DESIGN ✦ MUSIC ✦ " * 7
SEG = 1250  # textLength pins the rendered width so the loop is seamless
marquee = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="56" viewBox="0 0 {WIDTH} 56" font-family="Helvetica, Arial, sans-serif" role="img" aria-label="code, design, music">
  {STYLE}
  <clipPath id="win"><rect x="{MARGIN}" y="0" width="{INNER}" height="56"/></clipPath>
  <line class="rule" x1="{MARGIN}" y1="1" x2="{WIDTH - MARGIN}" y2="1" stroke-width="1" stroke-opacity="0.35"/>
  <line class="rule" x1="{MARGIN}" y1="55" x2="{WIDTH - MARGIN}" y2="55" stroke-width="1" stroke-opacity="0.35"/>
  <g clip-path="url(#win)">
    <g>
      <text class="mut" x="{MARGIN}" y="34" font-size="13" letter-spacing="4" textLength="{SEG}" lengthAdjust="spacingAndGlyphs">{PHRASE}</text>
      <text class="mut" x="{MARGIN + SEG}" y="34" font-size="13" letter-spacing="4" textLength="{SEG}" lengthAdjust="spacingAndGlyphs">{PHRASE}</text>
      <animateTransform attributeName="transform" type="translate" from="0 0" to="-{SEG} 0" dur="30s" repeatCount="indefinite"/>
    </g>
  </g>
</svg>'''

# --- link chips ----------------------------------------------------------
def chip(label):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="170" height="44" viewBox="0 0 170 44" font-family="Helvetica, Arial, sans-serif" role="img" aria-label="{label.lower()}">
  {STYLE}
  <rect class="box" x="0.5" y="0.5" width="169" height="43" stroke-width="1"/>
  <text class="ink" x="85" y="27" font-size="12.5" letter-spacing="3" text-anchor="middle">{label} ↗</text>
</svg>'''

files = {
    "assets/header-v2.svg": banner,
    "assets/marquee-v2.svg": marquee,
    "assets/chip-portfolio.svg": chip("PORTFOLIO"),
    "assets/chip-linkedin.svg": chip("LINKEDIN"),
    "assets/chip-email.svg": chip("EMAIL"),
}
for name, svg in files.items():
    with open(name, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"{name}: {len(svg) / 1024:.1f} KB")
