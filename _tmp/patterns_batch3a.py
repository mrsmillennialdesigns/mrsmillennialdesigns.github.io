#!/usr/bin/env python3
"""Seamless patterns batch 3a: Princess Castle, Line Art Cat, Line Art Dog.
3600x3600, 3x supersample, full opacity, PIL built-in primitives."""

from PIL import Image, ImageDraw, ImageFont
import math
import random
import os

CANVAS = 3600
IMG_DIR = '/Users/alexhosage/Desktop/mmd-website/img'
PATTERNS_DIR = os.path.join(IMG_DIR, 'patterns')
os.makedirs(PATTERNS_DIR, exist_ok=True)


def place_seamless(canvas, element, x, y, cs):
    ew, eh = element.size
    px, py = int(x - ew/2), int(y - eh/2)
    for ox in [-cs, 0, cs]:
        for oy in [-cs, 0, cs]:
            nx, ny = px + ox, py + oy
            if nx + ew > 0 and nx < cs and ny + eh > 0 and ny < cs:
                canvas.paste(element, (nx, ny), element)


def create_product_images(lid, pattern):
    pattern.convert('RGB').save(os.path.join(IMG_DIR, f'{lid}_0.jpg'), 'JPEG', quality=95)
    pattern.save(os.path.join(PATTERNS_DIR, f'{lid}-clean.png'), 'PNG')

    tile_size = 1800
    tile = pattern.resize((tile_size, tile_size), Image.LANCZOS)
    tiled = Image.new('RGB', (CANVAS, CANVAS), (255, 255, 255))
    tiled.paste(tile, (0, 0))
    tiled.paste(tile, (tile_size, 0))
    tiled.paste(tile, (0, tile_size))
    tiled.paste(tile, (tile_size, tile_size))
    draw = ImageDraw.Draw(tiled)
    draw.line([(tile_size, 0), (tile_size, CANVAS)], fill=(200, 200, 200), width=3)
    draw.line([(0, tile_size), (CANVAS, tile_size)], fill=(200, 200, 200), width=3)
    try:
        font = ImageFont.truetype('/System/Library/Fonts/Avenir Next.ttc', 32)
        lw, lh = 500, 60
        lx, ly = (CANVAS - lw)//2, (CANVAS - lh)//2
        draw.rounded_rectangle([lx, ly, lx+lw, ly+lh], radius=12, fill=(255,255,255,230))
        draw.text((lx+50, ly+12), "Seamless Tile Repeat", font=font, fill=(100,85,85))
    except:
        pass
    tiled.save(os.path.join(IMG_DIR, f'{lid}_1.jpg'), 'JPEG', quality=95)

    mockup = Image.new('RGB', (CANVAS, CANVAS), (245, 240, 235))
    pad = 200
    pat_s = pattern.resize((CANVAS-2*pad, CANVAS-2*pad), Image.LANCZOS)
    md = ImageDraw.Draw(mockup)
    md.rectangle([pad+8, pad+8, CANVAS-pad+8, CANVAS-pad+8], fill=(200,195,190))
    mockup.paste(pat_s.convert('RGB'), (pad, pad))
    md.rectangle([pad, pad, CANVAS-pad, CANVAS-pad], outline=(180,175,170), width=3)
    mockup.save(os.path.join(IMG_DIR, f'{lid}_2.jpg'), 'JPEG', quality=95)
    print(f"    {lid} — 3 product images done")


# =============================================================================
# 11. PRINCESS CASTLE PRINT
# =============================================================================
def draw_castle(d, cx, cy, ss, wall_color, roof_color, accent_color):
    """Cute fairy tale castle: main tower, side towers, flags, windows."""
    lighter = tuple(min(255, c+25) for c in wall_color)

    # Main tower (center, tallest)
    tw = ss * 0.12
    th = ss * 0.30
    d.rounded_rectangle([cx-tw, cy-th*0.5, cx+tw, cy+th*0.4],
                        radius=ss*0.015, fill=(*wall_color, 255))

    # Main tower roof (triangle)
    rh = th * 0.3
    d.polygon([(cx-tw*1.3, cy-th*0.5), (cx, cy-th*0.5-rh), (cx+tw*1.3, cy-th*0.5)],
              fill=(*roof_color, 255))

    # Flag on top
    flag_h = ss * 0.04
    flag_w = ss * 0.05
    flag_y = cy - th*0.5 - rh
    d.line([(cx, flag_y), (cx, flag_y - flag_h*1.5)],
           fill=(100, 90, 80, 255), width=max(2, ss//200))
    d.polygon([(cx, flag_y - flag_h*1.5), (cx+flag_w, flag_y - flag_h),
               (cx, flag_y - flag_h*0.5)], fill=(*accent_color, 255))

    # Side towers
    for side in [-1, 1]:
        stx = cx + side * tw * 2.2
        stw = tw * 0.7
        sth = th * 0.7
        d.rounded_rectangle([stx-stw, cy-sth*0.3, stx+stw, cy+th*0.4],
                            radius=ss*0.01, fill=(*wall_color, 255))

        # Side tower roof (triangle)
        srh = sth * 0.25
        d.polygon([(stx-stw*1.2, cy-sth*0.3), (stx, cy-sth*0.3-srh),
                   (stx+stw*1.2, cy-sth*0.3)], fill=(*roof_color, 255))

        # Side tower window (small arch)
        wr = stw * 0.4
        wy = cy - sth * 0.05
        d.ellipse([stx-wr, wy-wr, stx+wr, wy+wr], fill=(*lighter, 255))
        d.rectangle([stx-wr, wy, stx+wr, wy+wr*1.2], fill=(*lighter, 255))

    # Connecting walls between towers
    for side in [-1, 1]:
        wall_x1 = cx + side * tw
        wall_x2 = cx + side * tw * 1.5
        d.rectangle([min(wall_x1, wall_x2), cy+th*0.1,
                     max(wall_x1, wall_x2), cy+th*0.4],
                    fill=(*wall_color, 255))
        # Crenellations (small rectangles on top of wall)
        cw = (max(wall_x1, wall_x2) - min(wall_x1, wall_x2)) / 3
        for i in range(3):
            if i % 2 == 0:
                cx2 = min(wall_x1, wall_x2) + i * cw
                d.rectangle([cx2, cy+th*0.05, cx2+cw, cy+th*0.1],
                            fill=(*wall_color, 255))

    # Main door (arched)
    dw = tw * 0.55
    dh = th * 0.18
    dy = cy + th * 0.4 - dh
    d.rectangle([cx-dw, dy, cx+dw, cy+th*0.4], fill=(*accent_color, 255))
    d.ellipse([cx-dw, dy-dw, cx+dw, dy+dw], fill=(*accent_color, 255))

    # Main window (round)
    main_wr = tw * 0.35
    main_wy = cy - th * 0.15
    d.ellipse([cx-main_wr, main_wy-main_wr, cx+main_wr, main_wy+main_wr],
              fill=(*lighter, 255))
    # Cross in window
    d.line([(cx-main_wr*0.7, main_wy), (cx+main_wr*0.7, main_wy)],
           fill=(*wall_color, 255), width=max(2, ss//200))
    d.line([(cx, main_wy-main_wr*0.7), (cx, main_wy+main_wr*0.7)],
           fill=(*wall_color, 255), width=max(2, ss//200))


def draw_crown(d, cx, cy, ss, color):
    """Small crown."""
    cw = ss * 0.14
    ch = ss * 0.10
    # Base band
    d.rounded_rectangle([cx-cw, cy, cx+cw, cy+ch*0.4], radius=ss*0.01,
                        fill=(*color, 255))
    # Three points
    point_w = cw * 0.3
    for i, px in enumerate([-0.6, 0, 0.6]):
        tip_x = cx + cw * px
        tip_y = cy - ch * (0.6 if i == 1 else 0.4)
        d.polygon([(tip_x-point_w, cy), (tip_x, tip_y), (tip_x+point_w, cy)],
                  fill=(*color, 255))
        # Gem dot on tip
        gr = point_w * 0.3
        d.ellipse([tip_x-gr, tip_y+gr*0.5, tip_x+gr, tip_y+gr*2.5],
                  fill=(255, 255, 255, 255))


def draw_heart_small(d, cx, cy, ss, color):
    """Tiny heart."""
    hr = ss * 0.06
    d.ellipse([cx-hr*1.5, cy-hr*1.2, cx-hr*0.05, cy+hr*0.1], fill=(*color, 255))
    d.ellipse([cx+hr*0.05, cy-hr*1.2, cx+hr*1.5, cy+hr*0.1], fill=(*color, 255))
    d.polygon([(cx-hr*1.45, cy-hr*0.2), (cx+hr*1.45, cy-hr*0.2),
               (cx, cy+hr*1.5)], fill=(*color, 255))


def draw_star_4pt(d, cx, cy, r, color):
    """4-point sparkle star."""
    pts = []
    for i in range(8):
        angle = math.pi * i / 4 - math.pi/2
        rr = r if i % 2 == 0 else r * 0.3
        pts.append((cx + rr * math.cos(angle), cy + rr * math.sin(angle)))
    d.polygon(pts, fill=(*color, 255))


def create_princess_castle():
    print("  Princess Castle...")
    random.seed(111)
    canvas = Image.new('RGB', (CANVAS, CANVAS), (252, 245, 255))

    castle_palettes = [
        ((230, 200, 220), (200, 140, 180), (240, 180, 200)),   # pink castle
        ((200, 210, 235), (150, 160, 200), (180, 190, 230)),   # blue castle
        ((225, 215, 200), (190, 160, 140), (220, 190, 170)),   # cream castle
        ((215, 200, 230), (170, 140, 190), (210, 180, 220)),   # lavender castle
        ((240, 220, 200), (200, 150, 130), (235, 190, 170)),   # peach castle
    ]

    cols, rows = 5, 4
    sx, sy = CANVAS / cols, CANVAS / rows

    for row in range(rows):
        for col in range(cols):
            x = col * sx + sx/2 + random.randint(-20, 20)
            y = row * sy + sy/2 + random.randint(-15, 15)
            if row % 2:
                x += sx / 2

            wc, rc, ac = random.choice(castle_palettes)
            size = random.randint(520, 600)

            ss = size * 3
            layer = Image.new('RGBA', (ss, ss), (0, 0, 0, 0))
            d = ImageDraw.Draw(layer)
            draw_castle(d, ss/2, ss/2, ss, wc, rc, ac)

            layer = layer.resize((size, size), Image.LANCZOS)
            place_seamless(canvas, layer, x, y, CANVAS)

    # Scatter crowns, hearts, and stars
    accent_items = ['crown', 'heart', 'star']
    accent_colors = [(240, 200, 100), (240, 170, 190), (200, 180, 230),
                     (180, 210, 230), (230, 200, 160)]
    for _ in range(30):
        asize = random.randint(100, 160)
        ax = random.randint(0, CANVAS)
        ay = random.randint(0, CANVAS)
        ss2 = asize * 3
        al = Image.new('RGBA', (ss2, ss2), (0, 0, 0, 0))
        ad = ImageDraw.Draw(al)
        ac = random.choice(accent_colors)
        atype = random.choice(accent_items)
        if atype == 'crown':
            draw_crown(ad, ss2/2, ss2/2, ss2, ac)
        elif atype == 'heart':
            draw_heart_small(ad, ss2/2, ss2/2, ss2, ac)
        else:
            draw_star_4pt(ad, ss2/2, ss2/2, ss2*0.25, ac)
        al = al.rotate(random.uniform(-15, 15), resample=Image.BICUBIC, expand=False)
        al = al.resize((asize, asize), Image.LANCZOS)
        place_seamless(canvas, al, ax, ay, CANVAS)

    return canvas


# =============================================================================
# 12. MODERN ONE LINE ART CAT
# =============================================================================
def draw_line_art_cat(d, cx, cy, ss, line_color, line_width):
    """Minimalist one-line-style cat using connected curves and lines."""
    lw = max(3, line_width)

    # We'll draw a sitting cat profile using arcs, lines, and ellipses
    # All strokes only (outline), no fills — modern line art style

    # Body outline (large oval, just outline)
    bw = ss * 0.18
    bh = ss * 0.22
    body_cy = cy + ss * 0.05
    d.ellipse([cx-bw, body_cy-bh, cx+bw, body_cy+bh],
              outline=(*line_color, 255), width=lw)

    # Head (circle on top-right of body)
    hr = ss * 0.11
    hx = cx + bw * 0.3
    hy = cy - bh * 0.65
    d.ellipse([hx-hr, hy-hr, hx+hr, hy+hr],
              outline=(*line_color, 255), width=lw)

    # Ears (two triangles on top of head)
    ear_h = hr * 0.7
    ear_w = hr * 0.45
    for side in [-1, 1]:
        ex = hx + side * hr * 0.55
        ey = hy - hr * 0.75
        d.line([(ex-ear_w*side*0.3, hy-hr*0.5), (ex, ey)],
               fill=(*line_color, 255), width=lw)
        d.line([(ex, ey), (ex+ear_w*side*0.8, hy-hr*0.4)],
               fill=(*line_color, 255), width=lw)

    # Eyes (two small dots)
    er = hr * 0.06
    for side in [-1, 1]:
        ex = hx + side * hr * 0.35
        ey = hy - hr * 0.05
        d.ellipse([ex-er, ey-er, ex+er, ey+er], fill=(*line_color, 255))

    # Nose (tiny triangle)
    nr = hr * 0.07
    nx = hx + hr * 0.05
    ny = hy + hr * 0.15
    d.polygon([(nx, ny+nr), (nx-nr, ny-nr*0.5), (nx+nr, ny-nr*0.5)],
              fill=(*line_color, 255))

    # Whiskers
    wl = hr * 0.5
    for side in [-1, 1]:
        for angle_off in [-0.15, 0, 0.15]:
            wx1 = hx + side * hr * 0.3
            wy1 = hy + hr * 0.2
            wx2 = wx1 + side * wl
            wy2 = wy1 + wl * angle_off
            d.line([(wx1, wy1), (wx2, wy2)], fill=(*line_color, 255), width=max(1, lw//2))

    # Tail (curved line from back of body)
    tail_pts = []
    for t in range(20):
        frac = t / 19
        tx = cx - bw * 0.8 - ss * 0.08 * frac
        ty = body_cy + bh * 0.3 - ss * 0.15 * frac - ss * 0.08 * math.sin(frac * math.pi)
        tail_pts.append((tx, ty))
    for i in range(len(tail_pts)-1):
        d.line([tail_pts[i], tail_pts[i+1]], fill=(*line_color, 255), width=lw)

    # Front paws (two small arcs at bottom)
    for side in [-0.3, 0.3]:
        px = cx + bw * side
        py = body_cy + bh * 0.85
        pr = bw * 0.15
        d.arc([px-pr, py-pr*0.5, px+pr, py+pr*0.5],
              start=0, end=180, fill=(*line_color, 255), width=lw)

    # Neck connection line
    d.line([(hx-hr*0.3, hy+hr*0.8), (cx+bw*0.1, body_cy-bh*0.7)],
           fill=(*line_color, 255), width=lw)
    d.line([(hx+hr*0.5, hy+hr*0.7), (cx+bw*0.5, body_cy-bh*0.5)],
           fill=(*line_color, 255), width=lw)


def create_line_art_cat():
    print("  Line Art Cat...")
    random.seed(112)
    canvas = Image.new('RGB', (CANVAS, CANVAS), (255, 253, 250))

    line_colors = [
        (60, 55, 50),     # charcoal
        (100, 85, 75),    # warm brown
        (80, 80, 95),     # blue-gray
        (120, 90, 80),    # terracotta
        (70, 85, 70),     # forest
    ]

    cols, rows = 6, 6
    sx, sy = CANVAS / cols, CANVAS / rows

    for row in range(rows):
        for col in range(cols):
            x = col * sx + sx/2 + random.randint(-30, 30)
            y = row * sy + sy/2 + random.randint(-25, 25)
            if row % 2:
                x += sx / 2

            lc = random.choice(line_colors)
            size = random.randint(380, 460)
            flip = random.choice([-1, 1])

            ss = size * 3
            layer = Image.new('RGBA', (ss, ss), (0, 0, 0, 0))
            d = ImageDraw.Draw(layer)
            draw_line_art_cat(d, ss/2, ss/2, ss, lc, ss//120)

            if flip < 0:
                layer = layer.transpose(Image.FLIP_LEFT_RIGHT)

            layer = layer.resize((size, size), Image.LANCZOS)
            place_seamless(canvas, layer, x, y, CANVAS)

    # Scatter tiny paw prints
    for _ in range(25):
        psize = random.randint(60, 100)
        px = random.randint(0, CANVAS)
        py = random.randint(0, CANVAS)
        ss2 = psize * 3
        pl = Image.new('RGBA', (ss2, ss2), (0, 0, 0, 0))
        pd = ImageDraw.Draw(pl)
        pc = random.choice(line_colors)
        # Paw pad
        pad_r = ss2 * 0.15
        pd.ellipse([ss2/2-pad_r, ss2/2-pad_r*0.3, ss2/2+pad_r, ss2/2+pad_r*1.2],
                   fill=(*pc, 255))
        # Toe beans
        toe_r = pad_r * 0.35
        for toe_x, toe_y in [(-0.6, -1.0), (0, -1.3), (0.6, -1.0)]:
            tx = ss2/2 + pad_r * toe_x
            ty = ss2/2 + pad_r * toe_y
            pd.ellipse([tx-toe_r, ty-toe_r, tx+toe_r, ty+toe_r], fill=(*pc, 255))
        pl = pl.rotate(random.uniform(-20, 20), resample=Image.BICUBIC, expand=False)
        pl = pl.resize((psize, psize), Image.LANCZOS)
        place_seamless(canvas, pl, px, py, CANVAS)

    return canvas


# =============================================================================
# 13. MODERN ONE LINE ART DOG
# =============================================================================
def draw_line_art_dog(d, cx, cy, ss, line_color, line_width):
    """Minimalist one-line-style dog using connected curves and lines."""
    lw = max(3, line_width)

    # Body (horizontal oval outline)
    bw = ss * 0.22
    bh = ss * 0.14
    body_cy = cy + ss * 0.05
    d.ellipse([cx-bw, body_cy-bh, cx+bw, body_cy+bh],
              outline=(*line_color, 255), width=lw)

    # Head (circle, front of body)
    hr = ss * 0.10
    hx = cx + bw * 0.65
    hy = cy - bh * 0.4
    d.ellipse([hx-hr, hy-hr, hx+hr, hy+hr],
              outline=(*line_color, 255), width=lw)

    # Snout/muzzle (smaller circle overlapping bottom of head)
    mr = hr * 0.55
    mx = hx + hr * 0.35
    my = hy + hr * 0.35
    d.ellipse([mx-mr, my-mr, mx+mr, my+mr],
              outline=(*line_color, 255), width=lw)

    # Nose (filled dot)
    nr = hr * 0.1
    nx = mx + mr * 0.3
    ny = my - mr * 0.15
    d.ellipse([nx-nr, ny-nr, nx+nr, ny+nr], fill=(*line_color, 255))

    # Eye (dot)
    er = hr * 0.06
    ex = hx + hr * 0.15
    ey = hy - hr * 0.15
    d.ellipse([ex-er, ey-er, ex+er, ey+er], fill=(*line_color, 255))

    # Floppy ears (curved lines drooping from top of head)
    for side in [-1, 1]:
        ear_start_x = hx + side * hr * 0.6
        ear_start_y = hy - hr * 0.7
        ear_mid_x = ear_start_x + side * hr * 0.5
        ear_mid_y = hy + hr * 0.1
        ear_end_x = ear_start_x + side * hr * 0.2
        ear_end_y = hy + hr * 0.4

        # Draw ear as connected line segments (approximating curve)
        pts = []
        for t in range(15):
            frac = t / 14
            # Quadratic bezier approximation
            px = (1-frac)**2 * ear_start_x + 2*(1-frac)*frac * ear_mid_x + frac**2 * ear_end_x
            py = (1-frac)**2 * ear_start_y + 2*(1-frac)*frac * ear_mid_y + frac**2 * ear_end_y
            pts.append((px, py))
        for i in range(len(pts)-1):
            d.line([pts[i], pts[i+1]], fill=(*line_color, 255), width=lw)

    # Neck connection
    d.line([(hx-hr*0.6, hy+hr*0.6), (cx+bw*0.2, body_cy-bh*0.8)],
           fill=(*line_color, 255), width=lw)

    # Legs (4 simple lines with paw circles)
    leg_positions = [(-0.6, 0), (-0.2, 0), (0.25, 0), (0.6, 0)]
    for lp_x, _ in leg_positions:
        lx = cx + bw * lp_x
        ly_top = body_cy + bh * 0.7
        ly_bot = body_cy + bh * 1.4
        d.line([(lx, ly_top), (lx, ly_bot)], fill=(*line_color, 255), width=lw)
        # Paw (small circle)
        paw_r = bh * 0.1
        d.ellipse([lx-paw_r, ly_bot-paw_r*0.5, lx+paw_r, ly_bot+paw_r*0.5],
                  outline=(*line_color, 255), width=lw)

    # Tail (curved upward from back)
    tail_pts = []
    for t in range(15):
        frac = t / 14
        tx = cx - bw * 0.85 - ss * 0.05 * frac
        ty = body_cy - bh * 0.2 - ss * 0.12 * frac + ss * 0.03 * math.sin(frac * math.pi * 1.5)
        tail_pts.append((tx, ty))
    for i in range(len(tail_pts)-1):
        d.line([tail_pts[i], tail_pts[i+1]], fill=(*line_color, 255), width=lw)

    # Tongue (tiny)
    tongue_r = mr * 0.2
    d.ellipse([mx+mr*0.1-tongue_r, my+mr*0.5, mx+mr*0.1+tongue_r, my+mr*0.5+tongue_r*2],
              fill=(200, 130, 130, 255))


def create_line_art_dog():
    print("  Line Art Dog...")
    random.seed(113)
    canvas = Image.new('RGB', (CANVAS, CANVAS), (255, 253, 250))

    line_colors = [
        (60, 55, 50),     # charcoal
        (100, 85, 75),    # warm brown
        (80, 80, 95),     # blue-gray
        (120, 90, 80),    # terracotta
        (70, 85, 70),     # forest
    ]

    cols, rows = 5, 5
    sx, sy = CANVAS / cols, CANVAS / rows

    for row in range(rows):
        for col in range(cols):
            x = col * sx + sx/2 + random.randint(-30, 30)
            y = row * sy + sy/2 + random.randint(-25, 25)
            if row % 2:
                x += sx / 2

            lc = random.choice(line_colors)
            size = random.randint(460, 540)
            flip = random.choice([-1, 1])

            ss = size * 3
            layer = Image.new('RGBA', (ss, ss), (0, 0, 0, 0))
            d = ImageDraw.Draw(layer)
            draw_line_art_dog(d, ss/2, ss/2, ss, lc, ss//120)

            if flip < 0:
                layer = layer.transpose(Image.FLIP_LEFT_RIGHT)

            layer = layer.resize((size, size), Image.LANCZOS)
            place_seamless(canvas, layer, x, y, CANVAS)

    # Scatter tiny bone shapes
    for _ in range(20):
        bsize = random.randint(80, 130)
        bx_pos = random.randint(0, CANVAS)
        by_pos = random.randint(0, CANVAS)
        ss2 = bsize * 3
        bl = Image.new('RGBA', (ss2, ss2), (0, 0, 0, 0))
        bd = ImageDraw.Draw(bl)
        bc = random.choice(line_colors)
        # Mini bone outline
        bone_w = ss2 * 0.3
        bone_h = ss2 * 0.06
        knob_r = ss2 * 0.06
        bd.rounded_rectangle([ss2/2-bone_w, ss2/2-bone_h, ss2/2+bone_w, ss2/2+bone_h],
                             radius=bone_h, outline=(*bc, 255), width=max(2, ss2//100))
        for side_x in [-1, 1]:
            for side_y in [-1, 1]:
                kx = ss2/2 + side_x * (bone_w - knob_r * 0.3)
                ky = ss2/2 + side_y * knob_r * 0.5
                bd.ellipse([kx-knob_r, ky-knob_r, kx+knob_r, ky+knob_r],
                           outline=(*bc, 255), width=max(2, ss2//100))
        bl = bl.rotate(random.uniform(-30, 30), resample=Image.BICUBIC, expand=False)
        bl = bl.resize((bsize, bsize), Image.LANCZOS)
        place_seamless(canvas, bl, bx_pos, by_pos, CANVAS)

    # Scatter hearts
    heart_colors = [(200, 130, 130), (180, 150, 130), (150, 140, 160)]
    for _ in range(12):
        hsize = random.randint(50, 80)
        hx_pos = random.randint(0, CANVAS)
        hy_pos = random.randint(0, CANVAS)
        ss2 = hsize * 3
        hl = Image.new('RGBA', (ss2, ss2), (0, 0, 0, 0))
        hd = ImageDraw.Draw(hl)
        hc = random.choice(heart_colors)
        # Tiny filled heart
        hhr = ss2 * 0.2
        hd.ellipse([ss2/2-hhr*1.5, ss2/2-hhr*1.2, ss2/2-hhr*0.05, ss2/2+hhr*0.1],
                   fill=(*hc, 255))
        hd.ellipse([ss2/2+hhr*0.05, ss2/2-hhr*1.2, ss2/2+hhr*1.5, ss2/2+hhr*0.1],
                   fill=(*hc, 255))
        hd.polygon([(ss2/2-hhr*1.45, ss2/2-hhr*0.2), (ss2/2+hhr*1.45, ss2/2-hhr*0.2),
                    (ss2/2, ss2/2+hhr*1.5)], fill=(*hc, 255))
        hl = hl.resize((hsize, hsize), Image.LANCZOS)
        place_seamless(canvas, hl, hx_pos, hy_pos, CANVAS)

    return canvas


# =============================================================================
# MAIN
# =============================================================================
def main():
    patterns = [
        ('8800000021', 'Princess Castle', create_princess_castle),
        ('8800000022', 'Line Art Cat', create_line_art_cat),
        ('8800000023', 'Line Art Dog', create_line_art_dog),
    ]
    for lid, name, builder in patterns:
        print(f"[{lid}] {name}")
        pat = builder()
        create_product_images(lid, pat)
    print("\nBatch 3a done!")


if __name__ == '__main__':
    main()
