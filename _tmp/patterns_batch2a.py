#!/usr/bin/env python3
"""Seamless patterns batch 2a: Race Car, Watercolor Trees, Bee & Flowers.
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
# 6. CLASSIC RACE CAR (red, blue, yellow muted tones)
# =============================================================================
def draw_race_car(d, cx, cy, ss, body_color, accent_color):
    """Classic toy race car: rounded body, cockpit, wheels, number circle."""
    # Car body (rounded rectangle)
    bw = ss * 0.38
    bh = ss * 0.13
    d.rounded_rectangle([cx-bw, cy-bh, cx+bw, cy+bh],
                        radius=ss*0.04, fill=(*body_color, 255))

    # Hood slope (front triangle area)
    d.polygon([(cx+bw*0.5, cy-bh), (cx+bw, cy-bh*0.3),
               (cx+bw, cy+bh), (cx+bw*0.5, cy+bh)], fill=(*body_color, 255))

    # Roof / cockpit bump
    rw = bw * 0.35
    rh = bh * 1.1
    d.rounded_rectangle([cx-rw, cy-bh-rh, cx+rw*0.3, cy-bh+rh*0.1],
                        radius=ss*0.03, fill=(*body_color, 255))

    # Windshield (lighter)
    ww = rw * 0.5
    wh = rh * 0.7
    lighter = tuple(min(255, c+40) for c in body_color)
    d.rounded_rectangle([cx+rw*0.1, cy-bh-wh, cx+rw*0.1+ww, cy-bh+wh*0.1],
                        radius=ss*0.015, fill=(*lighter, 255))

    # Number circle on side
    nr = bh * 0.5
    d.ellipse([cx-bw*0.15-nr, cy-nr, cx-bw*0.15+nr, cy+nr], fill=(255, 255, 255, 255))
    # Number dot inside
    d.ellipse([cx-bw*0.15-nr*0.3, cy-nr*0.3, cx-bw*0.15+nr*0.3, cy+nr*0.3],
              fill=(*accent_color, 255))

    # Racing stripe
    stripe_h = bh * 0.15
    d.rectangle([cx-bw*0.8, cy-stripe_h, cx+bw*0.8, cy+stripe_h],
                fill=(*accent_color, 255))

    # Wheels (two circles)
    wheel_r = bh * 0.55
    for wx in [-0.55, 0.55]:
        wxx = cx + bw * wx
        wyy = cy + bh * 0.8
        # Tire (dark)
        d.ellipse([wxx-wheel_r, wyy-wheel_r, wxx+wheel_r, wyy+wheel_r],
                  fill=(50, 45, 40, 255))
        # Hubcap (lighter)
        hub_r = wheel_r * 0.55
        d.ellipse([wxx-hub_r, wyy-hub_r, wxx+hub_r, wyy+hub_r],
                  fill=(200, 195, 190, 255))
        # Hub center dot
        hd_r = hub_r * 0.3
        d.ellipse([wxx-hd_r, wyy-hd_r, wxx+hd_r, wyy+hd_r],
                  fill=(120, 115, 110, 255))

    # Exhaust puff (small circles behind car)
    for i in range(3):
        pr = bh * 0.2 * (1 - i*0.25)
        px = cx - bw - bh*0.4 - i * bh * 0.35
        py = cy + bh * 0.3 + random.uniform(-bh*0.15, bh*0.15)
        d.ellipse([px-pr, py-pr, px+pr, py+pr], fill=(220, 215, 210, 255))


def draw_flag(d, cx, cy, ss, color):
    """Small checkered flag."""
    pole_h = ss * 0.25
    pole_w = ss * 0.012
    # Pole
    d.rectangle([cx-pole_w, cy-pole_h, cx+pole_w, cy+pole_h*0.3],
                fill=(100, 90, 80, 255))
    # Flag (rectangle with checkers)
    fw = ss * 0.15
    fh = ss * 0.12
    fx = cx + pole_w
    fy = cy - pole_h
    d.rectangle([fx, fy, fx+fw, fy+fh], fill=(255, 255, 255, 255))
    # Checker squares
    sq = fw / 3
    for r in range(3):
        for c in range(3):
            if (r + c) % 2 == 0:
                d.rectangle([fx+c*sq, fy+r*(fh/3), fx+(c+1)*sq, fy+(r+1)*(fh/3)],
                            fill=(40, 35, 30, 255))


def draw_star_simple(d, cx, cy, r, color):
    """Small 4-point star."""
    pts = []
    for i in range(8):
        angle = math.pi * i / 4 - math.pi/2
        rr = r if i % 2 == 0 else r * 0.4
        pts.append((cx + rr * math.cos(angle), cy + rr * math.sin(angle)))
    d.polygon(pts, fill=(*color, 255))


def create_race_car():
    print("  Classic Race Car...")
    random.seed(106)
    canvas = Image.new('RGB', (CANVAS, CANVAS), (248, 245, 240))

    car_palettes = [
        ((190, 65, 60), (245, 210, 90)),     # muted red, yellow stripe
        ((70, 100, 155), (230, 200, 80)),     # muted blue, yellow stripe
        ((195, 170, 65), (180, 70, 65)),      # muted yellow, red stripe
        ((65, 130, 100), (230, 200, 80)),     # muted green, yellow stripe
        ((180, 100, 55), (240, 215, 100)),    # muted orange, yellow stripe
    ]

    cols, rows = 5, 5
    sx, sy = CANVAS / cols, CANVAS / rows

    for row in range(rows):
        for col in range(cols):
            x = col * sx + sx/2 + random.randint(-25, 25)
            y = row * sy + sy/2 + random.randint(-20, 20)
            if row % 2:
                x += sx / 2

            bc, ac = random.choice(car_palettes)
            size = random.randint(520, 600)
            flip = random.choice([-1, 1])

            ss = size * 3
            layer = Image.new('RGBA', (ss, ss), (0, 0, 0, 0))
            d = ImageDraw.Draw(layer)
            draw_race_car(d, ss/2, ss/2, ss, bc, ac)

            if flip < 0:
                layer = layer.transpose(Image.FLIP_LEFT_RIGHT)

            layer = layer.resize((size, size), Image.LANCZOS)
            place_seamless(canvas, layer, x, y, CANVAS)

    # Scatter small flags and stars
    for _ in range(20):
        fsize = random.randint(120, 180)
        fx = random.randint(0, CANVAS)
        fy = random.randint(0, CANVAS)
        ss2 = fsize * 3
        fl = Image.new('RGBA', (ss2, ss2), (0, 0, 0, 0))
        fd = ImageDraw.Draw(fl)
        if random.random() < 0.5:
            draw_flag(fd, ss2/2, ss2/2, ss2, (50, 45, 40))
        else:
            sc = random.choice([(190, 65, 60), (70, 100, 155), (195, 170, 65)])
            draw_star_simple(fd, ss2/2, ss2/2, ss2*0.3, sc)
        fl = fl.resize((fsize, fsize), Image.LANCZOS)
        place_seamless(canvas, fl, fx, fy, CANVAS)

    return canvas


# =============================================================================
# 7. WATERCOLOR TREE PRINT (shades of green)
# =============================================================================
def draw_tree(d, cx, cy, ss, trunk_color, foliage_colors):
    """Cute watercolor-style tree: brown trunk + layered round foliage."""
    # Trunk
    tw = ss * 0.05
    th = ss * 0.22
    d.rounded_rectangle([cx-tw, cy+ss*0.02, cx+tw, cy+th],
                        radius=tw*0.5, fill=(*trunk_color, 255))

    # Foliage layers (3 overlapping circles, bottom to top)
    positions = [
        (0, -0.08, 0.22),     # bottom layer (wide)
        (-0.06, -0.18, 0.17), # mid-left
        (0.05, -0.16, 0.16),  # mid-right
        (0, -0.27, 0.14),     # top
    ]
    for i, (ox, oy, r_mult) in enumerate(positions):
        fc = foliage_colors[i % len(foliage_colors)]
        fr = ss * r_mult
        fx = cx + ss * ox
        fy = cy + ss * oy
        d.ellipse([fx-fr, fy-fr, fx+fr, fy+fr], fill=(*fc, 255))

    # Highlight dot on top circle
    hr = ss * 0.04
    d.ellipse([cx-hr+ss*0.03, cy-ss*0.32, cx+hr+ss*0.03, cy-ss*0.32+hr*2],
              fill=(min(255, foliage_colors[0][0]+30),
                    min(255, foliage_colors[0][1]+25),
                    min(255, foliage_colors[0][2]+20), 255))


def draw_small_leaf(d, cx, cy, ss, color):
    """Tiny fallen leaf."""
    lw = ss * 0.12
    lh = ss * 0.06
    d.ellipse([cx-lw, cy-lh, cx+lw, cy+lh], fill=(*color, 255))
    # Vein
    d.line([(cx-lw*0.7, cy), (cx+lw*0.7, cy)],
           fill=(max(0,color[0]-25), max(0,color[1]-20), max(0,color[2]-15), 255),
           width=max(1, ss//250))


def create_watercolor_trees():
    print("  Watercolor Trees...")
    random.seed(107)
    canvas = Image.new('RGB', (CANVAS, CANVAS), (252, 250, 245))

    trunk_colors = [(140, 100, 70), (120, 85, 55), (155, 110, 80)]
    foliage_palettes = [
        [(110, 170, 110), (90, 150, 95), (130, 185, 120), (80, 140, 85)],   # bright green
        [(95, 145, 100), (75, 130, 80), (115, 160, 110), (65, 120, 75)],    # forest green
        [(140, 185, 130), (120, 170, 115), (155, 195, 140), (100, 155, 100)], # sage green
        [(85, 155, 120), (70, 140, 105), (100, 165, 130), (60, 130, 95)],   # teal green
    ]

    cols, rows = 6, 6
    sx, sy = CANVAS / cols, CANVAS / rows

    for row in range(rows):
        for col in range(cols):
            x = col * sx + sx/2 + random.randint(-30, 30)
            y = row * sy + sy/2 + random.randint(-25, 25)
            if row % 2:
                x += sx / 2

            size = random.randint(400, 520)
            tc = random.choice(trunk_colors)
            fp = random.choice(foliage_palettes)

            ss = size * 3
            layer = Image.new('RGBA', (ss, ss), (0, 0, 0, 0))
            d = ImageDraw.Draw(layer)
            draw_tree(d, ss/2, ss/2, ss, tc, fp)

            layer = layer.resize((size, size), Image.LANCZOS)
            place_seamless(canvas, layer, x, y, CANVAS)

    # Scatter small leaves
    leaf_colors = [(130, 175, 115), (100, 155, 95), (145, 180, 125), (80, 140, 80)]
    for _ in range(35):
        lsize = random.randint(80, 140)
        lx = random.randint(0, CANVAS)
        ly = random.randint(0, CANVAS)
        ss2 = lsize * 3
        ll = Image.new('RGBA', (ss2, ss2), (0, 0, 0, 0))
        ld = ImageDraw.Draw(ll)
        lc = random.choice(leaf_colors)
        draw_small_leaf(ld, ss2/2, ss2/2, ss2, lc)
        ll = ll.rotate(random.uniform(-45, 45), resample=Image.BICUBIC, expand=False)
        ll = ll.resize((lsize, lsize), Image.LANCZOS)
        place_seamless(canvas, ll, lx, ly, CANVAS)

    return canvas


# =============================================================================
# 8. BEE WATERCOLOR WITH SUMMER FLOWERS
# =============================================================================
def draw_bee(d, cx, cy, ss):
    """Cute watercolor bee: striped oval body, wings, face."""
    # Wings (behind body)
    wing_r_w = ss * 0.16
    wing_r_h = ss * 0.11
    for side in [-1, 1]:
        wx = cx + side * ss * 0.08
        wy = cy - ss * 0.1
        d.ellipse([wx-wing_r_w, wy-wing_r_h, wx+wing_r_w, wy+wing_r_h],
                  fill=(220, 235, 245, 255))
        # Wing outline
        d.ellipse([wx-wing_r_w, wy-wing_r_h, wx+wing_r_w, wy+wing_r_h],
                  outline=(180, 200, 215, 255), width=max(2, ss//200))

    # Body (oval)
    bw = ss * 0.18
    bh = ss * 0.13
    d.ellipse([cx-bw, cy-bh, cx+bw, cy+bh], fill=(245, 210, 80, 255))

    # Black stripes
    stripe_w = bw * 0.25
    for i, sx_off in enumerate([-0.45, 0, 0.45]):
        sx2 = cx + bw * sx_off - stripe_w/2
        d.rectangle([sx2, cy-bh*0.95, sx2+stripe_w, cy+bh*0.95],
                    fill=(55, 45, 35, 255))

    # Head (circle at front)
    hr = bh * 0.7
    hx = cx + bw * 0.85
    d.ellipse([hx-hr, cy-hr, hx+hr, cy+hr], fill=(55, 45, 35, 255))

    # Eyes
    er = hr * 0.3
    d.ellipse([hx+hr*0.1-er, cy-hr*0.3-er, hx+hr*0.1+er, cy-hr*0.3+er],
              fill=(255, 255, 255, 255))
    # Pupil
    pr = er * 0.5
    d.ellipse([hx+hr*0.15-pr, cy-hr*0.3-pr, hx+hr*0.15+pr, cy-hr*0.3+pr],
              fill=(30, 25, 20, 255))

    # Smile
    d.arc([hx-hr*0.3, cy+hr*0.05, hx+hr*0.4, cy+hr*0.5],
          start=0, end=180, fill=(245, 210, 80, 255), width=max(2, ss//180))

    # Antennae
    for side in [-1, 1]:
        ax = hx + hr * 0.3
        ay = cy - hr * 0.7
        tip_x = ax + ss * 0.04
        tip_y = ay - ss * 0.06 + side * ss * 0.03
        d.line([(ax, ay), (tip_x, tip_y)], fill=(55, 45, 35, 255), width=max(2, ss//180))
        dot_r = ss * 0.015
        d.ellipse([tip_x-dot_r, tip_y-dot_r, tip_x+dot_r, tip_y+dot_r],
                  fill=(55, 45, 35, 255))

    # Stinger
    sx3 = cx - bw * 0.95
    d.polygon([(sx3, cy-bh*0.15), (sx3, cy+bh*0.15), (sx3-bh*0.4, cy)],
              fill=(55, 45, 35, 255))


def draw_summer_flower(d, cx, cy, ss, petal_color, center_color):
    """Simple 5-petal summer flower."""
    petal_r = ss * 0.14
    dist = ss * 0.15
    for i in range(5):
        angle = 2 * math.pi * i / 5 - math.pi/2
        px = cx + dist * math.cos(angle)
        py = cy + dist * math.sin(angle)
        d.ellipse([px-petal_r, py-petal_r*0.8, px+petal_r, py+petal_r*0.8],
                  fill=(*petal_color, 255))
    # Center
    cr = ss * 0.08
    d.ellipse([cx-cr, cy-cr, cx+cr, cy+cr], fill=(*center_color, 255))
    # Center detail
    dr = cr * 0.4
    d.ellipse([cx-dr, cy-dr, cx+dr, cy+dr],
              fill=(min(255, center_color[0]+30), min(255, center_color[1]+25),
                    min(255, center_color[2]+15), 255))


def draw_daisy(d, cx, cy, ss, petal_color):
    """Small daisy with elongated petals."""
    num_petals = 8
    for i in range(num_petals):
        angle = 2 * math.pi * i / num_petals
        px = cx + ss * 0.12 * math.cos(angle)
        py = cy + ss * 0.12 * math.sin(angle)
        pw = ss * 0.04
        ph = ss * 0.09
        # Simple ellipse at angle (approximate with circles)
        d.ellipse([px-pw, py-ph*0.5, px+pw, py+ph*0.5], fill=(*petal_color, 255))
    # Yellow center
    cr = ss * 0.06
    d.ellipse([cx-cr, cy-cr, cx+cr, cy+cr], fill=(245, 210, 80, 255))


def create_bee_flowers():
    print("  Bee & Summer Flowers...")
    random.seed(108)
    canvas = Image.new('RGB', (CANVAS, CANVAS), (255, 252, 245))

    flower_palettes = [
        ((240, 160, 170), (245, 210, 80)),   # pink petals, yellow center
        ((255, 200, 120), (210, 160, 80)),    # orange petals, brown center
        ((200, 170, 230), (245, 210, 80)),    # lavender petals, yellow center
        ((255, 220, 140), (200, 150, 80)),    # yellow petals, brown center
        ((240, 180, 180), (250, 220, 100)),   # coral petals, yellow center
    ]

    cols, rows = 6, 6
    sx, sy = CANVAS / cols, CANVAS / rows
    elements = ['bee', 'flower', 'flower', 'daisy', 'bee', 'flower']

    for row in range(rows):
        for col in range(cols):
            x = col * sx + sx/2 + random.randint(-30, 30)
            y = row * sy + sy/2 + random.randint(-25, 25)
            if row % 2:
                x += sx / 2

            etype = random.choice(elements)
            size = random.randint(360, 460)
            flip = random.choice([-1, 1])

            ss = size * 3
            layer = Image.new('RGBA', (ss, ss), (0, 0, 0, 0))
            d = ImageDraw.Draw(layer)

            if etype == 'bee':
                draw_bee(d, ss/2, ss/2, ss)
                rotation = random.uniform(-20, 20)
                layer = layer.rotate(rotation, resample=Image.BICUBIC, expand=False)
            elif etype == 'flower':
                pc, cc = random.choice(flower_palettes)
                draw_summer_flower(d, ss/2, ss/2, ss, pc, cc)
            else:
                pc = random.choice([(255, 255, 250), (255, 245, 240), (245, 245, 255)])
                draw_daisy(d, ss/2, ss/2, ss, pc)

            if flip < 0:
                layer = layer.transpose(Image.FLIP_LEFT_RIGHT)

            layer = layer.resize((size, size), Image.LANCZOS)
            place_seamless(canvas, layer, x, y, CANVAS)

    # Scatter tiny pollen dots
    for _ in range(40):
        ds = random.randint(20, 40)
        dx = random.randint(0, CANVAS)
        dy = random.randint(0, CANVAS)
        dl = Image.new('RGBA', (ds*3, ds*3), (0, 0, 0, 0))
        dd = ImageDraw.Draw(dl)
        dc = random.choice([(245, 215, 90), (240, 200, 80), (250, 225, 110)])
        dr = ds * 3 * 0.35
        dd.ellipse([ds*3/2-dr, ds*3/2-dr, ds*3/2+dr, ds*3/2+dr], fill=(*dc, 255))
        dl = dl.resize((ds, ds), Image.LANCZOS)
        place_seamless(canvas, dl, dx, dy, CANVAS)

    return canvas


# =============================================================================
# MAIN
# =============================================================================
def main():
    patterns = [
        ('8800000016', 'Classic Race Car', create_race_car),
        ('8800000017', 'Watercolor Trees', create_watercolor_trees),
        ('8800000018', 'Bee & Summer Flowers', create_bee_flowers),
    ]
    for lid, name, builder in patterns:
        print(f"[{lid}] {name}")
        pat = builder()
        create_product_images(lid, pat)
    print("\nBatch 2a done!")


if __name__ == '__main__':
    main()
