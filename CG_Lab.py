"""
The Glowing Neon Sign Mandala
==============================
Replicates the reference image: a neon sign mandala on a dark brick-wall
background, using only Python's turtle and math modules.

Color palette (matching the photo):
  - Electric cyan  (#00E5FF) — outer star outline, inner circle, centre flower
  - Glowing gold   (#FFE033) — lotus petal rings, inner rim
  - Neon green     (#39FF14) — decorative arcs, vein lines, small accents
  - White          (#FFFFFF) — thin glow overlay on every stroke

Structure (8-fold symmetry throughout):
  1. Brick-wall background (dark navy rectangles)
  2. Outer 8-point cyan star
  3. Large gold lotus petals  (8 petals)
  4. Cyan rim circle
  5. Inner gold petal ring    (8 petals, rotated 22.5°)
  6. Gold inner circle
  7. Green vein lines through each outer petal
  8. Green decorative U-arcs between star tips
  9. Centre 5-petal cyan flower
 10. Bright white centre dot
"""

import turtle
import math
screen = turtle.Screen()
screen.setup(width=820, height=820)
screen.title("The Glowing Neon Sign Mandala")
screen.tracer(0, 0)

def make_pen():
    t = turtle.Turtle()
    t.speed(0)
    t.hideturtle()
    t.penup()
    return t

bg   = make_pen()   # brick wall
pen  = make_pen()   # all mandala drawing

CYAN  = "#00E5FF"
GOLD  = "#FFE033"
GREEN = "#39FF14"
WHITE = "#FFFFFF"
NAVY  = "#0d1a3a"
BRICK = "#0f2045"
MORTAR= "#0a1830"

def neon_stroke(t, color, glow_color, thick, thin):
    """Draw the current path twice: thick neon color then thin white glow."""
    t.pensize(thick)
    t.pencolor(color)
   

def goto(t, x, y):
    t.penup(); t.goto(x, y); t.pendown()

def move(t, x, y):
    t.penup(); t.goto(x, y)

def draw_brick_wall():
    """Fill canvas with a dark navy brick pattern."""
    W, H = 820, 820
    bw, bh, gap = 70, 28, 3
    bg.penup()
    bg.goto(-W//2, -H//2)
    bg.fillcolor(NAVY)
    bg.begin_fill()
    for _ in range(2):
        bg.forward(W); bg.left(90)
        bg.forward(H); bg.left(90)
    bg.end_fill()
  
    rows = H // (bh + gap) + 2
    cols = W // (bw + gap) + 2
    for row in range(rows):
        y_bot = -H//2 + row * (bh + gap)
        offset = (bw // 2) if row % 2 == 1 else 0
        for col in range(-1, cols + 1):
            x_left = -W//2 + col * (bw + gap) - offset
            bg.goto(x_left, y_bot)
            bg.fillcolor(BRICK)
            bg.begin_fill()
            bg.pendown()
            bg.pensize(1.5)
            bg.pencolor(MORTAR)
            for side, length in [(0, bw), (90, bh), (0, bw), (90, bh)]:
                bg.forward(length); bg.left(90)
            bg.end_fill()
            bg.penup()

def draw_outer_star(cx, cy, outer_r, inner_r, rot_deg, color, glow, thick, thin):
    """
    8-fold star: vertices alternate between outer_r and inner_r.
    Drawn twice (thick colour + thin white) to simulate neon glow.
    """
    for width, col in [(thick, color), (thin, glow)]:
        pen.pensize(width)
        pen.pencolor(col)
        pts = []
        for i in range(16):
            a = math.radians(rot_deg + i * 22.5)
            r = outer_r if i % 2 == 0 else inner_r
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        move(pen, pts[0][0], pts[0][1])
        pen.pendown()
        for x, y in pts[1:]:
            pen.goto(x, y)
        pen.goto(pts[0][0], pts[0][1])
        pen.penup()

def draw_petal_ring(cx, cy, ring_r, petal_h, petal_w_ratio,
                    n_petals, rot_offset, color, glow, thick, thin):
    """
    n_petals ellipses arranged in a ring.  Each ellipse centre sits at ring_r
    from (cx,cy).  The long axis points radially outward.
    petal_h  = semi-major axis (length along radius)
    petal_w_ratio = semi-minor / semi-major  (controls fatness)
    """
    for width, col in [(thick, color), (thin, glow)]:
        pen.pensize(width)
        pen.pencolor(col)
        for i in range(n_petals):
            a_deg = rot_offset + i * (360 / n_petals)
            a = math.radians(a_deg)
            # Centre of this petal ellipse
            px = cx + ring_r * math.cos(a)
            py = cy + ring_r * math.sin(a)
            # We approximate the ellipse with a smooth polygon (60 steps)
            b = petal_h               # semi-major (radial direction)
            c = petal_h * petal_w_ratio  # semi-minor (tangential)
            move(pen, px + b * math.cos(a), py + b * math.sin(a))
            pen.pendown()
            steps = 60
            for s in range(steps + 1):
                theta = s * 2 * math.pi / steps
                # Local ellipse coords (major along 'a', minor perp)
                ex = b * math.cos(theta)
                ey = c * math.sin(theta)
                # Rotate local coords by 'a' and translate to (px, py)
                gx = px + ex * math.cos(a) - ey * math.sin(a)
                gy = py + ex * math.sin(a) + ey * math.cos(a)
                pen.goto(gx, gy)
            pen.penup()

def draw_circle(cx, cy, r, color, glow, thick, thin):
    """Perfect circle, neon glow double-pass."""
    for width, col in [(thick, color), (thin, glow)]:
        pen.pensize(width)
        pen.pencolor(col)
        move(pen, cx, cy - r)
        pen.setheading(0)
        pen.pendown()
        pen.circle(r)
        pen.penup()

def draw_vein_lines(cx, cy, r_start, r_end, n, rot_offset, color, glow, thick, thin):
    """Radial line from r_start to r_end for each of n angles."""
    for width, col in [(thick, color), (thin, glow)]:
        pen.pensize(width)
        pen.pencolor(col)
        for i in range(n):
            a = math.radians(rot_offset + i * (360 / n))
            x1 = cx + r_start * math.cos(a)
            y1 = cy + r_start * math.sin(a)
            x2 = cx + r_end   * math.cos(a)
            y2 = cy + r_end   * math.sin(a)
            move(pen, x1, y1)
            pen.pendown()
            pen.goto(x2, y2)
            pen.penup()

def draw_decorative_arcs(cx, cy, ring_r, arc_r, n, rot_offset, color, glow, thick, thin):
    """
    Small U-shaped (180°) arcs placed between each outer star point,
    opening inward toward the centre.
    """
    for width, col in [(thick, color), (thin, glow)]:
        pen.pensize(width)
        pen.pencolor(col)
        for i in range(n):
            a_deg = rot_offset + i * (360 / n)
            a     = math.radians(a_deg)
            ax = cx + ring_r * math.cos(a)
            ay = cy + ring_r * math.sin(a)
           
            perp_a = a + math.pi / 2
            sx = ax + arc_r * math.cos(perp_a)
            sy = ay + arc_r * math.sin(perp_a)
            move(pen, sx, sy)
            pen.setheading(a_deg + 180)
            pen.pendown()
            pen.circle(arc_r, 180)
            pen.penup()

def draw_centre_flower(cx, cy, petal_ring_r, petal_r, n_petals, color, glow, thick, thin):
    """
    n_petals small circles whose centres are at petal_ring_r from (cx,cy).
    Each circle has radius petal_r.  The circles slightly overlap the centre.
    """
    for width, col in [(thick, color), (thin, glow)]:
        pen.pensize(width)
        pen.pencolor(col)
        for i in range(n_petals):
            a = math.radians(-90 + i * (360 / n_petals))
            px = cx + petal_ring_r * math.cos(a)
            py = cy + petal_ring_r * math.sin(a)
            move(pen, px, py - petal_r)
            pen.setheading(0)
            pen.pendown()
            pen.circle(petal_r)
            pen.penup()

def draw_centre_dot(cx, cy, r, color):
    pen.pensize(1)
    pen.pencolor(color)
    move(pen, cx, cy - r)
    pen.setheading(0)
    pen.begin_fill()
    pen.fillcolor(color)
    pen.pendown()
    pen.circle(r)
    pen.end_fill()
    pen.penup()

def draw_mandala():
    CX, CY = 0, 0   # canvas centre

    # Layer 1 — Brick wall background
    draw_brick_wall()

    # Layer 2 — Outer 8-point cyan star  (outer=220, inner=148)
    draw_outer_star(CX, CY, outer_r=218, inner_r=148, rot_deg=90,
                    color=CYAN,  glow=WHITE, thick=3.5, thin=1.0)

    # Layer 3 — Large gold lotus petals (8 petals, centred at r=158)
    draw_petal_ring(CX, CY, ring_r=0, petal_h=158, petal_w_ratio=0.38,
                    n_petals=8, rot_offset=90,
                    color=GOLD, glow=WHITE, thick=3.0, thin=0.9)

    # Layer 4 — Cyan rim circle (r=168)
    draw_circle(CX, CY, r=168, color=CYAN, glow=WHITE, thick=3.2, thin=0.9)

    # Layer 5 — Inner gold petal ring (8 petals, rotated 22.5°, r=108)
    draw_petal_ring(CX, CY, ring_r=0, petal_h=108, petal_w_ratio=0.40,
                    n_petals=8, rot_offset=90 + 22.5,
                    color=GOLD, glow=WHITE, thick=2.8, thin=0.8)

    # Layer 6 — Gold inner circle (r=82)
    draw_circle(CX, CY, r=82, color=GOLD, glow=WHITE, thick=3.0, thin=0.9)

    # Layer 7 — Green vein lines through outer petals
    draw_vein_lines(CX, CY, r_start=30, r_end=210, n=8, rot_offset=90,
                    color=GREEN, glow=WHITE, thick=2.0, thin=0.6)

    # Layer 8 — Green decorative U-arcs between star tips
    draw_decorative_arcs(CX, CY, ring_r=200, arc_r=19,
                         n=8, rot_offset=90 + 22.5,
                         color=GREEN, glow=WHITE, thick=2.2, thin=0.65)

    # Layer 9 — Cyan inner circle (r=56)
    draw_circle(CX, CY, r=56, color=CYAN, glow=WHITE, thick=2.8, thin=0.8)

    # Layer 10 — Centre 5-petal cyan flower
    draw_centre_flower(CX, CY, petal_ring_r=26, petal_r=20, n_petals=5,
                       color=CYAN, glow=WHITE, thick=2.2, thin=0.65)

    # Layer 11 — Bright white centre dot
    draw_centre_dot(CX, CY, r=7, color=WHITE)


if __name__ == "__main__":
    screen.bgcolor(NAVY)
    draw_mandala()
    screen.update()        # single flush — instant display
    turtle.exitonclick()   # window stays open until clicked