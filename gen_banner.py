"""Generate banner.svg: Swiss International / Bauhaus poster with a
rotating wireframe icosahedron baked as an SMIL path animation."""
import math

W, H = 1200, 480
BONE, INK = "#ECEAE3", "#0A0A0A"
RED, BLUE, YELLOW = "#E63329", "#1D4ED8", "#F2B705"

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
assert len(EDGES) == 30

CX, CY, R = 930, 208, 150
TILT = 0.42  # fixed tilt around X so the spin axis isn't boring-vertical
FRAMES = 72

def frame_path(t):
    a = 2 * math.pi * t
    ca, sa = math.cos(a), math.sin(a)
    ct, st = math.cos(TILT), math.sin(TILT)
    pts = []
    for x, y, z in V:
        # spin around Y, then tilt around X, orthographic drop of z
        x1, z1 = x * ca + z * sa, -x * sa + z * ca
        y1, z2 = y * ct - z1 * st, y * st + z1 * ct
        pts.append((round(CX + R * x1, 1), round(CY + R * y1, 1)))
    return " ".join(f"M{pts[i][0]} {pts[i][1]}L{pts[j][0]} {pts[j][1]}" for i, j in EDGES)

values = ";".join(frame_path(i / FRAMES) for i in range(FRAMES + 1))

# --- poster --------------------------------------------------------------
grid = "".join(
    f'<line x1="{80 + i * (1040 / 12):.1f}" y1="40" x2="{80 + i * (1040 / 12):.1f}" y2="{H - 40}" stroke="{INK}" stroke-opacity="0.08" stroke-width="1"/>'
    for i in range(13))

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Helvetica, Arial, sans-serif">
  <rect width="{W}" height="{H}" fill="{BONE}"/>
  {grid}

  <!-- bauhaus primaries -->
  <circle cx="{CX}" cy="{CY}" r="118" fill="{YELLOW}"/>
  <rect x="554" y="294" width="46" height="46" fill="{BLUE}"/>
  <path d="M1096 372 L1140 372 L1118 334 Z" fill="{RED}"/>

  <!-- rotating icosahedron (3D baked into SMIL frames) -->
  <path fill="none" stroke="{INK}" stroke-width="1.6" stroke-linecap="round">
    <animate attributeName="d" dur="14s" repeatCount="indefinite" calcMode="linear" values="{values}"/>
  </path>

  <!-- type -->
  <text x="80" y="188" font-size="118" font-weight="bold" letter-spacing="-4" fill="{INK}">Luke</text>
  <text x="80" y="298" font-size="118" font-weight="bold" letter-spacing="-4" fill="{INK}">Zhang<tspan fill="{RED}">.</tspan></text>

  <line x1="80" y1="340" x2="600" y2="340" stroke="{INK}" stroke-width="2"/>

  <text x="80" y="376" font-size="17" letter-spacing="3" fill="{INK}">MECHATRONICS ENGINEERING, UNIVERSITY OF WATERLOO</text>
  <text x="80" y="404" font-size="17" letter-spacing="3" fill="{INK}">CODE / DESIGN / MUSIC</text>

  <!-- swiss furniture -->
  <text x="80" y="72" font-size="12" letter-spacing="2" fill="{INK}" fill-opacity="0.55">LZ·0826</text>
  <text x="{W - 80}" y="72" font-size="12" letter-spacing="2" fill="{INK}" fill-opacity="0.55" text-anchor="end">43.4643° N, 80.5204° W</text>
  <text x="{W - 80}" y="{H - 52}" font-size="12" letter-spacing="2" fill="{INK}" fill-opacity="0.55" text-anchor="end">GRID 12 / ORTHO 0.42</text>
</svg>'''

with open("banner.svg", "w", encoding="utf-8") as f:
    f.write(svg)
print(f"banner.svg written, {len(svg) / 1024:.0f} KB, {len(EDGES)} edges x {FRAMES} frames")
