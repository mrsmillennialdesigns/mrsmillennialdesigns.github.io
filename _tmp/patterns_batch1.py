#!/usr/bin/env python3
"""Seamless patterns batch 1: Dark Academia, Unicorn, Boho Wildflower, Axolotl, Dinosaur Bones.
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
# 1. DARK ACADEMIA
# =============================================================================
def draw_book(d, cx, cy, ss, color, accent):
    """A simple book: rectangle body with spine accent and pages."""
    bw = ss * 0.30
    bh = ss * 0.40
    # Book body
    d.rounded_rectangle([cx-bw, cy-bh, cx+bw, cy+bh], radius=ss*0.03, fill=(*color, 255))
    # Spine line
    spine_w = bw * 0.15
    d.rectangle([cx-bw, cy-bh, cx-bw+spine_w, cy+bh], fill=(*accent, 255))
    # Pages (white lines)
    page_x = cx + bw * 0.2
    for i in range(3):
        py = cy - bh*0.5 + bh * 0.33 * i
        d.line([(page_x, py), (cx+bw*0.8, py)], fill=(240, 235, 225, 255), width=max(2, ss//200))


def draw_potion(d, cx, cy, ss, liquid_color):
    """Potion bottle: rounded rect body + thin neck + round stopper."""
    # Bottle body
    bw = ss * 0.18
    bh = ss * 0.28
    d.rounded_rectangle([cx-bw, cy-bh*0.2, cx+bw, cy+bh],
                        radius=ss*0.06, fill=(210, 220, 215, 255))
    # Liquid inside (bottom half)
    liq_top = cy + bh * 0.15
    d.rounded_rectangle([cx-bw+ss*0.02, liq_top, cx+bw-ss*0.02, cy+bh-ss*0.02],
                        radius=ss*0.04, fill=(*liquid_color, 255))
    # Neck
    nw = bw * 0.45
    nh = bh * 0.35
    d.rectangle([cx-nw, cy-bh*0.2-nh, cx+nw, cy-bh*0.15], fill=(210, 220, 215, 255))
    # Cork/stopper
    cw = nw * 1.2
    ch = nh * 0.35
    d.rounded_rectangle([cx-cw, cy-bh*0.2-nh-ch, cx+cw, cy-bh*0.2-nh+ch*0.3],
                        radius=ss*0.02, fill=(180, 140, 100, 255))
    # Shine highlight
    hr = bw * 0.2
    d.ellipse([cx-bw+ss*0.04, cy-bh*0.05, cx-bw+ss*0.04+hr, cy-bh*0.05+hr*2.5],
              fill=(235, 240, 238, 255))


def draw_frog(d, cx, cy, ss, color):
    """Cute frog: oval body, big eyes, little legs."""
    body_w = ss * 0.28
    body_h = ss * 0.22
    # Body
    d.ellipse([cx-body_w, cy-body_h*0.5, cx+body_w, cy+body_h], fill=(*color, 255))
    # Eyes (two bumps on top)
    eye_r = body_w * 0.28
    for side in [-1, 1]:
        ex = cx + side * body_w * 0.55
        ey = cy - body_h * 0.45
        d.ellipse([ex-eye_r, ey-eye_r, ex+eye_r, ey+eye_r], fill=(*color, 255))
        # White of eye
        wr = eye_r * 0.7
        d.ellipse([ex-wr, ey-wr, ex+wr, ey+wr], fill=(255, 255, 255, 255))
        # Pupil
        pr = eye_r * 0.35
        d.ellipse([ex-pr+side*pr*0.2, ey-pr, ex+pr+side*pr*0.2, ey+pr], fill=(30, 30, 30, 255))
    # Mouth (smile)
    d.arc([cx-body_w*0.4, cy+body_h*0.1, cx+body_w*0.4, cy+body_h*0.7],
          start=0, end=180, fill=(30, 50, 30, 255), width=max(2, ss//180))
    # Front legs
    for side in [-1, 1]:
        lx = cx + side * body_w * 0.8
        ly = cy + body_h * 0.6
        d.ellipse([lx-body_w*0.15, ly-body_h*0.12, lx+body_w*0.15, ly+body_h*0.12],
                  fill=(*color, 255))


def draw_mushroom(d, cx, cy, ss, cap_color):
    """Cute mushroom: ellipse cap with dots, rectangle stem."""
    cap_w = ss * 0.28
    cap_h = ss * 0.20
    stem_w = cap_w * 0.35
    stem_h = cap_h * 1.1
    # Stem
    d.rounded_rectangle([cx-stem_w, cy-cap_h*0.1, cx+stem_w, cy+stem_h],
                        radius=ss*0.03, fill=(245, 235, 220, 255))
    # Cap
    d.ellipse([cx-cap_w, cy-cap_h*1.2, cx+cap_w, cy+cap_h*0.15], fill=(*cap_color, 255))
    # Dots on cap
    dot_r = cap_w * 0.1
    positions = [(-0.4, -0.55), (0.3, -0.6), (0, -0.85), (-0.2, -0.35), (0.45, -0.35)]
    for px, py in positions:
        dx = cx + cap_w * px
        dy = cy + cap_h * py
        d.ellipse([dx-dot_r, dy-dot_r, dx+dot_r, dy+dot_r], fill=(255, 245, 235, 255))


def create_dark_academia():
    print("  Dark Academia...")
    random.seed(101)
    canvas = Image.new('RGB', (CANVAS, CANVAS), (245, 237, 224))

    book_colors = [
        ((45, 74, 62), (90, 50, 70)),     # dark green, plum spine
        ((91, 58, 107), (180, 140, 100)),  # deep purple, gold spine
        ((120, 85, 65), (160, 120, 80)),   # leather brown, tan spine
        ((201, 160, 176), (140, 100, 120)), # muted pink, darker spine
    ]
    potion_liquids = [(140, 80, 160), (80, 160, 120), (180, 120, 80), (100, 140, 180)]
    frog_colors = [(100, 150, 100), (120, 160, 110), (80, 130, 90)]
    mushroom_colors = [(180, 80, 70), (160, 100, 120), (140, 80, 130)]

    cols, rows = 7, 7
    sx, sy = CANVAS / cols, CANVAS / rows
    element_types = ['book', 'potion', 'star', 'frog', 'mushroom']

    for row in range(rows):
        for col in range(cols):
            x = col * sx + sx/2 + random.randint(-30, 30)
            y = row * sy + sy/2 + random.randint(-30, 30)
            if row % 2:
                x += sx / 2

            etype = random.choice(element_types)
            size = random.randint(320, 420)
            rotation = random.uniform(-15, 15)

            ss = size * 3
            layer = Image.new('RGBA', (ss, ss), (0, 0, 0, 0))
            d = ImageDraw.Draw(layer)
            cx, cy = ss/2, ss/2

            if etype == 'book':
                body_c, spine_c = random.choice(book_colors)
                draw_book(d, cx, cy, ss, body_c, spine_c)
            elif etype == 'potion':
                draw_potion(d, cx, cy, ss, random.choice(potion_liquids))
            elif etype == 'frog':
                draw_frog(d, cx, cy, ss, random.choice(frog_colors))
            elif etype == 'mushroom':
                draw_mushroom(d, cx, cy, ss, random.choice(mushroom_colors))
            else:  # star
                color = random.choice([(212, 168, 83), (201, 160, 176), (91, 58, 107)])
                r_outer = ss * 0.3
                r_inner = r_outer * 0.4
                star_rot = random.uniform(0, math.pi/5)
                pts = []
                for i in range(10):
                    angle = math.pi * i / 5 - math.pi/2 + star_rot
                    r = r_outer if i % 2 == 0 else r_inner
                    pts.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
                d.polygon(pts, fill=(*color, 255))

            layer = layer.rotate(rotation, resample=Image.BICUBIC, expand=False)
            layer = layer.resize((size, size), Image.LANCZOS)
            place_seamless(canvas, layer, x, y, CANVAS)

    return canvas


# =============================================================================
# 2. WATERCOLOR UNICORN
# =============================================================================
def draw_unicorn(layer, cx, cy, ss, body_color, mane_colors):
    """Cute unicorn: oval body, head, horn, legs, mane, tail."""
    d = ImageDraw.Draw(layer)

    # Body (horizontal oval)
    bw = ss * 0.28
    bh = ss * 0.18
    d.ellipse([cx-bw, cy-bh, cx+bw, cy+bh], fill=(*body_color, 255))

    # Head (smaller circle, front-upper)
    hw = bh * 0.75
    hx = cx + bw * 0.75
    hy = cy - bh * 0.6
    d.ellipse([hx-hw, hy-hw, hx+hw, hy+hw], fill=(*body_color, 255))
    # Neck connection
    d.polygon([(cx+bw*0.4, cy-bh*0.5), (hx-hw*0.3, hy+hw*0.4),
               (hx-hw*0.1, hy+hw*0.8), (cx+bw*0.2, cy)], fill=(*body_color, 255))

    # Horn (golden triangle)
    horn_h = hw * 1.3
    horn_w = hw * 0.2
    d.polygon([(hx, hy-hw-horn_h), (hx-horn_w, hy-hw*0.5), (hx+horn_w, hy-hw*0.5)],
              fill=(230, 195, 90, 255))

    # Ear
    ear_h = hw * 0.5
    d.polygon([(hx-hw*0.3, hy-hw*0.7), (hx-hw*0.55, hy-hw-ear_h*0.6),
               (hx-hw*0.05, hy-hw*0.5)], fill=(*body_color, 255))

    # Eye
    er = hw * 0.12
    d.ellipse([hx+hw*0.2-er, hy-er, hx+hw*0.2+er, hy+er], fill=(40, 35, 50, 255))
    # Eye shine
    sr = er * 0.4
    d.ellipse([hx+hw*0.2-er+sr, hy-er+sr*0.5, hx+hw*0.2-er+sr*2.5, hy-er+sr*2],
              fill=(255, 255, 255, 255))

    # Legs (4 rectangles)
    leg_w = bw * 0.12
    leg_h = bh * 1.0
    leg_positions = [-0.5, -0.15, 0.2, 0.55]
    for lp in leg_positions:
        lx = cx + bw * lp
        ly = cy + bh * 0.6
        d.rounded_rectangle([lx-leg_w, ly, lx+leg_w, ly+leg_h],
                           radius=leg_w*0.8, fill=(*body_color, 255))
        # Hoof
        d.ellipse([lx-leg_w*1.1, ly+leg_h-leg_w, lx+leg_w*1.1, ly+leg_h+leg_w*0.3],
                  fill=(200, 185, 170, 255))

    # Mane (small colored ellipses along neck)
    mane_positions = [(cx+bw*0.3, cy-bh*0.9), (cx+bw*0.5, cy-bh*1.1),
                      (cx+bw*0.65, cy-bh*1.2), (hx-hw*0.5, hy-hw*0.5)]
    for i, (mx, my) in enumerate(mane_positions):
        mc = mane_colors[i % len(mane_colors)]
        mr = bh * 0.35
        d.ellipse([mx-mr*0.7, my-mr, mx+mr*0.7, my+mr*0.3], fill=(*mc, 255))

    # Tail (cascading ellipses)
    tx = cx - bw * 0.9
    ty = cy - bh * 0.2
    for i in range(3):
        tc = mane_colors[i % len(mane_colors)]
        tr = bh * 0.4
        d.ellipse([tx-tr*0.5-i*bh*0.15, ty+i*bh*0.3-tr*0.5,
                   tx+tr*0.5-i*bh*0.15, ty+i*bh*0.3+tr*0.5], fill=(*tc, 255))


def create_unicorn():
    print("  Watercolor Unicorn...")
    random.seed(102)
    canvas = Image.new('RGB', (CANVAS, CANVAS), (250, 245, 255))

    body_colors = [
        (255, 240, 245),  # white-pink
        (245, 240, 255),  # white-lavender
        (240, 250, 245),  # white-mint
        (255, 245, 235),  # warm cream
    ]
    mane_palettes = [
        [(255, 160, 180), (180, 160, 240), (160, 220, 200), (255, 200, 120)],
        [(240, 140, 160), (160, 180, 240), (200, 160, 230), (255, 190, 140)],
        [(255, 180, 200), (140, 200, 220), (220, 180, 240), (200, 230, 160)],
    ]
    star_colors = [(255, 200, 120), (255, 180, 200), (180, 200, 240), (200, 180, 240)]

    # Main unicorn grid
    cols, rows = 5, 5
    sx, sy = CANVAS / cols, CANVAS / rows

    for row in range(rows):
        for col in range(cols):
            x = col * sx + sx/2 + random.randint(-30, 30)
            y = row * sy + sy/2 + random.randint(-30, 30)
            if row % 2:
                x += sx / 2

            bc = random.choice(body_colors)
            mp = random.choice(mane_palettes)
            size = random.randint(500, 600)
            flip = random.choice([-1, 1])

            ss = size * 3
            layer = Image.new('RGBA', (ss, ss), (0, 0, 0, 0))
            draw_unicorn(layer, ss/2, ss/2, ss, bc, mp)

            if flip < 0:
                layer = layer.transpose(Image.FLIP_LEFT_RIGHT)

            layer = layer.resize((size, size), Image.LANCZOS)
            place_seamless(canvas, layer, x, y, CANVAS)

    # Scatter small stars between unicorns
    for _ in range(40):
        sx2 = random.randint(80, 130)
        x = random.randint(0, CANVAS)
        y = random.randint(0, CANVAS)
        ss2 = sx2 * 3
        sl = Image.new('RGBA', (ss2, ss2), (0, 0, 0, 0))
        sd = ImageDraw.Draw(sl)
        sc = random.choice(star_colors)
        r_out = ss2 * 0.35
        r_in = r_out * 0.4
        rot = random.uniform(0, math.pi/5)
        pts = []
        for i in range(10):
            a = math.pi * i / 5 - math.pi/2 + rot
            r = r_out if i % 2 == 0 else r_in
            pts.append((ss2/2 + r * math.cos(a), ss2/2 + r * math.sin(a)))
        sd.polygon(pts, fill=(*sc, 255))
        sl = sl.resize((sx2, sx2), Image.LANCZOS)
        place_seamless(canvas, sl, x, y, CANVAS)

    return canvas


# =============================================================================
# 3. BOHO WILDFLOWER
# =============================================================================
def draw_boho_flower(d, cx, cy, ss, petal_color, center_color, num_petals=5):
    """Simple boho flower with round petals and a center."""
    petal_r = ss * 0.16
    dist = ss * 0.18
    for i in range(num_petals):
        angle = 2 * math.pi * i / num_petals - math.pi/2
        px = cx + dist * math.cos(angle)
        py = cy + dist * math.sin(angle)
        d.ellipse([px-petal_r, py-petal_r, px+petal_r, py+petal_r], fill=(*petal_color, 255))
    # Center
    cr = ss * 0.1
    d.ellipse([cx-cr, cy-cr, cx+cr, cy+cr], fill=(*center_color, 255))


def draw_boho_leaf(layer, cx, cy, ss, color, angle_deg):
    """Elongated leaf shape using rotated ellipse."""
    leaf = Image.new('RGBA', (ss, ss), (0, 0, 0, 0))
    ld = ImageDraw.Draw(leaf)
    lw = ss * 0.08
    lh = ss * 0.22
    ld.ellipse([ss/2-lw, ss/2-lh, ss/2+lw, ss/2+lh], fill=(*color, 255))
    # Vein line
    ld.line([(ss/2, ss/2-lh*0.8), (ss/2, ss/2+lh*0.8)],
            fill=(max(0,color[0]-30), max(0,color[1]-20), max(0,color[2]-20), 255),
            width=max(1, ss//250))
    leaf = leaf.rotate(angle_deg, resample=Image.BICUBIC, center=(ss/2, ss/2))
    layer.paste(Image.alpha_composite(
        Image.new('RGBA', (ss, ss), (0, 0, 0, 0)),
        leaf.crop((int(ss/2-ss/2), int(ss/2-ss/2), int(ss/2+ss/2), int(ss/2+ss/2)))
    ), (int(cx-ss/2), int(cy-ss/2)), leaf)


def create_boho_wildflower():
    print("  Boho Wildflower...")
    random.seed(103)
    canvas = Image.new('RGB', (CANVAS, CANVAS), (255, 248, 240))

    flower_palettes = [
        ((194, 125, 94), (180, 140, 90)),    # terracotta, gold center
        ((212, 160, 160), (200, 170, 100)),   # dusty pink, gold center
        ((217, 139, 123), (190, 150, 90)),    # coral, gold center
        ((195, 170, 130), (170, 140, 90)),    # tan, brown center
        ((200, 150, 170), (180, 140, 100)),   # mauve, gold center
    ]
    leaf_colors = [(139, 168, 136), (120, 150, 110), (150, 175, 140), (110, 140, 100)]

    cols, rows = 7, 7
    sx, sy = CANVAS / cols, CANVAS / rows

    for row in range(rows):
        for col in range(cols):
            x = col * sx + sx/2 + random.randint(-35, 35)
            y = row * sy + sy/2 + random.randint(-35, 35)
            if row % 2:
                x += sx / 2

            if random.random() < 0.6:
                # Flower
                size = random.randint(340, 440)
                ss = size * 3
                layer = Image.new('RGBA', (ss, ss), (0, 0, 0, 0))
                d = ImageDraw.Draw(layer)
                pc, cc = random.choice(flower_palettes)
                np = random.choice([5, 6])
                draw_boho_flower(d, ss/2, ss/2, ss, pc, cc, np)
                layer = layer.resize((size, size), Image.LANCZOS)
                place_seamless(canvas, layer, x, y, CANVAS)
            elif random.random() < 0.6:
                # Leaf cluster (2-3 leaves)
                size = random.randint(280, 380)
                ss = size * 3
                layer = Image.new('RGBA', (ss, ss), (0, 0, 0, 0))
                lc = random.choice(leaf_colors)
                for j in range(random.randint(2, 3)):
                    ang = random.uniform(-40, 40) + j * 35
                    ox = random.randint(-ss//8, ss//8)
                    oy = random.randint(-ss//8, ss//8)
                    draw_boho_leaf(layer, ss/2+ox, ss/2+oy, ss, lc, ang)
                layer = layer.resize((size, size), Image.LANCZOS)
                place_seamless(canvas, layer, x, y, CANVAS)
            else:
                # Berry cluster
                size = random.randint(200, 280)
                ss = size * 3
                layer = Image.new('RGBA', (ss, ss), (0, 0, 0, 0))
                d = ImageDraw.Draw(layer)
                bc = random.choice([(194, 125, 94), (180, 100, 100), (140, 100, 80)])
                for j in range(random.randint(3, 5)):
                    bx = ss/2 + random.randint(-ss//5, ss//5)
                    by = ss/2 + random.randint(-ss//5, ss//5)
                    br = ss * random.uniform(0.06, 0.09)
                    d.ellipse([bx-br, by-br, bx+br, by+br], fill=(*bc, 255))
                    # Highlight
                    hr = br * 0.3
                    d.ellipse([bx-br*0.3-hr, by-br*0.3-hr, bx-br*0.3+hr, by-br*0.3+hr],
                              fill=(255, 240, 230, 255))
                layer = layer.resize((size, size), Image.LANCZOS)
                place_seamless(canvas, layer, x, y, CANVAS)

    return canvas


# =============================================================================
# 4. AXOLOTL
# =============================================================================
def draw_axolotl(d, cx, cy, ss, body_color, gill_color):
    """Cute axolotl: oval body, round head, feathery gills, tiny legs, dot eyes."""
    lighter = tuple(min(255, c+20) for c in body_color)

    # Body (horizontal oval)
    bw = ss * 0.30
    bh = ss * 0.14
    d.ellipse([cx-bw, cy-bh, cx+bw, cy+bh], fill=(*body_color, 255))

    # Head (larger circle at front)
    hw = bh * 1.3
    hx = cx + bw * 0.65
    hy = cy - bh * 0.1
    d.ellipse([hx-hw, hy-hw, hx+hw, hy+hw], fill=(*body_color, 255))

    # Gills (3 feathery fronds on each side of head)
    for side in [-1, 1]:
        for i in range(3):
            ga = (side * 30 + side * i * 25) * math.pi / 180 - math.pi/2
            gx = hx + hw * 0.7 * math.cos(ga)
            gy = hy + hw * 0.7 * math.sin(ga) - hw * 0.2
            gw = hw * 0.25
            gh = hw * 0.55
            # Draw as rotated ellipse
            gill = Image.new('RGBA', (ss, ss), (0, 0, 0, 0))
            gd = ImageDraw.Draw(gill)
            gd.ellipse([ss/2-gw, ss/2-gh, ss/2+gw, ss/2+gh], fill=(*gill_color, 255))
            gill = gill.rotate(-math.degrees(ga)-90, resample=Image.BICUBIC, center=(ss/2, ss/2))
            # Shift to position
            ox = int(gx - ss/2)
            oy = int(gy - ss/2)
            shifted = Image.new('RGBA', (ss, ss), (0, 0, 0, 0))
            shifted.paste(gill, (ox, oy), gill)
            layer_parent = Image.new('RGBA', (ss, ss), (0, 0, 0, 0))
            d_parent = ImageDraw.Draw(layer_parent)
            # We need to composite onto the main drawing surface
            # Since d is tied to a specific image, we'll just draw simple ellipses
            d.ellipse([gx-gw, gy-gh*0.7, gx+gw, gy+gh*0.3], fill=(*gill_color, 255))

    # Eyes (cute dots)
    er = hw * 0.12
    for side_y in [-0.25]:
        for side_x in [-0.2, 0.35]:
            ex = hx + hw * side_x
            ey = hy + hw * side_y
            d.ellipse([ex-er, ey-er, ex+er, ey+er], fill=(30, 25, 35, 255))
            # Eye shine
            sr = er * 0.4
            d.ellipse([ex-er*0.2, ey-er*0.5, ex-er*0.2+sr, ey-er*0.5+sr],
                      fill=(255, 255, 255, 255))

    # Smile
    d.arc([hx-hw*0.3, hy+hw*0.05, hx+hw*0.3, hy+hw*0.5],
          start=0, end=180, fill=(*gill_color, 255), width=max(2, ss//180))

    # Cheek blush
    blush_r = hw * 0.15
    for side_x in [-0.5, 0.55]:
        bx = hx + hw * side_x
        by = hy + hw * 0.2
        d.ellipse([bx-blush_r, by-blush_r, bx+blush_r, by+blush_r],
                  fill=(*gill_color, 200))

    # Legs (4 tiny ovals)
    leg_w = bw * 0.08
    leg_h = bh * 0.5
    leg_positions = [(-0.5, 0.8), (-0.1, 0.8), (0.2, 0.8), (0.5, 0.8)]
    for lp_x, lp_y in leg_positions:
        lx = cx + bw * lp_x
        ly = cy + bh * lp_y
        d.ellipse([lx-leg_w, ly, lx+leg_w, ly+leg_h], fill=(*lighter, 255))

    # Tail (tapers off behind body)
    tx = cx - bw * 0.9
    ty = cy
    d.ellipse([tx-bw*0.35, ty-bh*0.4, tx+bw*0.15, ty+bh*0.3],
              fill=(*body_color, 255))
    # Tail tip
    d.ellipse([tx-bw*0.55, ty-bh*0.6, tx-bw*0.2, ty],
              fill=(*lighter, 255))


def create_axolotl():
    print("  Axolotl...")
    random.seed(104)
    canvas = Image.new('RGB', (CANVAS, CANVAS), (240, 248, 250))

    axolotl_colors = [
        ((245, 180, 190), (240, 130, 150)),  # pink body, deeper pink gills
        ((220, 190, 230), (200, 150, 210)),  # lavender body, purple gills
        ((180, 220, 210), (140, 200, 180)),  # mint body, teal gills
        ((245, 200, 170), (235, 160, 130)),  # peach body, coral gills
        ((190, 200, 235), (160, 170, 220)),  # soft blue body, blue gills
    ]

    cols, rows = 5, 5
    sx, sy = CANVAS / cols, CANVAS / rows

    for row in range(rows):
        for col in range(cols):
            x = col * sx + sx/2 + random.randint(-30, 30)
            y = row * sy + sy/2 + random.randint(-25, 25)
            if row % 2:
                x += sx / 2

            bc, gc = random.choice(axolotl_colors)
            size = random.randint(480, 580)
            flip = random.choice([-1, 1])

            ss = size * 3
            layer = Image.new('RGBA', (ss, ss), (0, 0, 0, 0))
            d = ImageDraw.Draw(layer)
            draw_axolotl(d, ss/2, ss/2, ss, bc, gc)

            if flip < 0:
                layer = layer.transpose(Image.FLIP_LEFT_RIGHT)

            layer = layer.resize((size, size), Image.LANCZOS)
            place_seamless(canvas, layer, x, y, CANVAS)

    # Small bubbles scattered
    for _ in range(30):
        bsize = random.randint(40, 80)
        bx = random.randint(0, CANVAS)
        by = random.randint(0, CANVAS)
        bl = Image.new('RGBA', (bsize*3, bsize*3), (0, 0, 0, 0))
        bd = ImageDraw.Draw(bl)
        br = bsize * 3 * 0.35
        bd.ellipse([bsize*3/2-br, bsize*3/2-br, bsize*3/2+br, bsize*3/2+br],
                   outline=(200, 220, 230, 255), width=max(2, bsize*3//40))
        # Shine
        sd_r = br * 0.25
        bd.ellipse([bsize*3/2-br*0.3-sd_r, bsize*3/2-br*0.3-sd_r,
                    bsize*3/2-br*0.3+sd_r, bsize*3/2-br*0.3+sd_r],
                   fill=(230, 240, 250, 255))
        bl = bl.resize((bsize, bsize), Image.LANCZOS)
        place_seamless(canvas, bl, bx, by, CANVAS)

    return canvas


# =============================================================================
# 5. DINOSAUR BONES
# =============================================================================
def draw_bone(d, cx, cy, ss, color):
    """Classic bone shape: elongated body with round knobs at each end."""
    bw = ss * 0.35
    bh = ss * 0.08
    knob_r = ss * 0.08
    # Shaft
    d.rounded_rectangle([cx-bw, cy-bh, cx+bw, cy+bh], radius=bh, fill=(*color, 255))
    # Knobs at each end (two circles per end)
    for side in [-1, 1]:
        for yoff in [-1, 1]:
            kx = cx + side * (bw - knob_r * 0.3)
            ky = cy + yoff * knob_r * 0.6
            d.ellipse([kx-knob_r, ky-knob_r, kx+knob_r, ky+knob_r], fill=(*color, 255))


def draw_skull(d, cx, cy, ss, color):
    """Cute dino skull: rounded head, two eye sockets, small jaw."""
    # Head
    hw = ss * 0.22
    hh = ss * 0.18
    d.ellipse([cx-hw, cy-hh, cx+hw, cy+hh], fill=(*color, 255))
    # Snout
    sw = hw * 0.6
    sh = hh * 0.5
    d.ellipse([cx+hw*0.3, cy+hh*0.1-sh, cx+hw*0.3+sw*2, cy+hh*0.1+sh], fill=(*color, 255))
    # Eye sockets (darker)
    darker = tuple(max(0, c-40) for c in color)
    er = hw * 0.22
    d.ellipse([cx-hw*0.35-er, cy-hh*0.2-er, cx-hw*0.35+er, cy-hh*0.2+er], fill=(*darker, 255))
    d.ellipse([cx+hw*0.15-er, cy-hh*0.2-er, cx+hw*0.15+er, cy-hh*0.2+er], fill=(*darker, 255))
    # Jaw teeth notches
    for i in range(3):
        tx = cx + hw * 0.2 + i * hw * 0.25
        ty = cy + hh * 0.15
        tw = hw * 0.06
        th = hh * 0.15
        d.polygon([(tx-tw, ty), (tx+tw, ty), (tx, ty+th)], fill=(*color, 255))


def draw_footprint(d, cx, cy, ss, color):
    """Dino footprint: large pad + 3 toe circles."""
    pad_r = ss * 0.12
    d.ellipse([cx-pad_r, cy-pad_r*0.8, cx+pad_r, cy+pad_r], fill=(*color, 255))
    # Toes
    toe_r = pad_r * 0.4
    toe_positions = [(-0.6, -1.3), (0, -1.5), (0.6, -1.3)]
    for tx, ty in toe_positions:
        d.ellipse([cx+pad_r*tx-toe_r, cy+pad_r*ty-toe_r,
                   cx+pad_r*tx+toe_r, cy+pad_r*ty+toe_r], fill=(*color, 255))


def create_dinosaur_bones():
    print("  Dinosaur Bones...")
    random.seed(105)
    canvas = Image.new('RGB', (CANVAS, CANVAS), (245, 237, 224))

    bone_colors = [
        (232, 221, 208),  # warm ivory
        (220, 210, 195),  # beige
        (210, 200, 185),  # tan
        (225, 215, 200),  # cream
    ]

    cols, rows = 7, 7
    sx, sy = CANVAS / cols, CANVAS / rows
    types = ['bone', 'bone', 'skull', 'footprint', 'bone']

    for row in range(rows):
        for col in range(cols):
            x = col * sx + sx/2 + random.randint(-30, 30)
            y = row * sy + sy/2 + random.randint(-30, 30)
            if row % 2:
                x += sx / 2

            etype = random.choice(types)
            size = random.randint(300, 420)
            rotation = random.uniform(-35, 35)
            color = random.choice(bone_colors)

            ss = size * 3
            layer = Image.new('RGBA', (ss, ss), (0, 0, 0, 0))
            d = ImageDraw.Draw(layer)

            if etype == 'bone':
                draw_bone(d, ss/2, ss/2, ss, color)
            elif etype == 'skull':
                draw_skull(d, ss/2, ss/2, ss, color)
            else:
                draw_footprint(d, ss/2, ss/2, ss, color)

            layer = layer.rotate(rotation, resample=Image.BICUBIC, expand=False)
            layer = layer.resize((size, size), Image.LANCZOS)
            place_seamless(canvas, layer, x, y, CANVAS)

    return canvas


# =============================================================================
# MAIN
# =============================================================================
def main():
    patterns = [
        ('8800000011', 'Dark Academia', create_dark_academia),
        ('8800000012', 'Watercolor Unicorn', create_unicorn),
        ('8800000013', 'Boho Wildflower', create_boho_wildflower),
        ('8800000014', 'Axolotl Watercolor', create_axolotl),
        ('8800000015', 'Dinosaur Bones', create_dinosaur_bones),
    ]
    for lid, name, builder in patterns:
        print(f"[{lid}] {name}")
        pat = builder()
        create_product_images(lid, pat)
    print("\nBatch 1 done! Check the results.")


if __name__ == '__main__':
    main()
