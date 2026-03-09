#!/usr/bin/env python3
"""
Seamless Pattern Generator v2 for MrsMillennial Designs
Larger elements, denser grid, more saturated colors — matching Easter egg style.
"""

from PIL import Image, ImageDraw, ImageFilter, ImageFont
import numpy as np
import random
import math
import os

random.seed(42)
np.random.seed(42)

OUTPUT_DIR = '/Users/alexhosage/Desktop/mmd-website/img/patterns'
os.makedirs(OUTPUT_DIR, exist_ok=True)

TILE_SIZE = 1200
FONT_PATH = '/System/Library/Fonts/Avenir Next.ttc'


def watercolor_shape(draw_func, size, base_color):
    """Create a watercolor-textured shape at 2x then downscale."""
    big = size * 2

    # Shape mask
    mask_img = Image.new('L', (big, big), 0)
    mask_draw = ImageDraw.Draw(mask_img)
    draw_func(mask_draw, big)
    # Soft edges
    mask_img = mask_img.filter(ImageFilter.GaussianBlur(radius=max(2, big // 25)))

    r, g, b = base_color
    base = np.full((big, big, 3), [r, g, b], dtype=np.float64)

    # Large watercolor wash variation
    noise_lo = np.random.normal(0, 25, (big // 4, big // 4, 3))
    noise_lo_img = Image.fromarray(np.clip(noise_lo + 128, 0, 255).astype(np.uint8))
    noise_lo_img = noise_lo_img.resize((big, big), Image.BILINEAR)
    noise_lo = np.array(noise_lo_img).astype(np.float64) - 128

    # Fine grain
    noise_hi = np.random.normal(0, 10, (big, big, 3))
    noise_hi_img = Image.fromarray(np.clip(noise_hi + 128, 0, 255).astype(np.uint8))
    noise_hi_img = noise_hi_img.filter(ImageFilter.GaussianBlur(radius=2))
    noise_hi = np.array(noise_hi_img).astype(np.float64) - 128

    textured = np.clip(base + noise_lo * 0.5 + noise_hi * 0.3, 0, 255)

    # Edge darkening
    mask_arr = np.array(mask_img).astype(np.float64) / 255.0
    k = max(5, big // 10)
    if k % 2 == 0: k += 1
    eroded = np.array(mask_img.filter(ImageFilter.MinFilter(k))).astype(np.float64) / 255.0
    edge = np.clip(mask_arr - eroded, 0, 1)
    edge_blur = np.array(
        Image.fromarray((edge * 255).astype(np.uint8)).filter(
            ImageFilter.GaussianBlur(radius=max(3, big // 15)))
    ).astype(np.float64) / 255.0
    for c in range(3):
        textured[:, :, c] *= (1 - edge_blur * 0.25)

    rgb = Image.fromarray(textured.astype(np.uint8))
    result = Image.new('RGBA', (big, big), (0, 0, 0, 0))
    result.paste(rgb, mask=mask_img)
    return result.resize((size, size), Image.LANCZOS)


def add_details(img, size, dtype='hearts', count=5):
    """Add small white details."""
    overlay = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    for _ in range(count):
        cx = random.randint(size // 4, 3 * size // 4)
        cy = random.randint(size // 4, 3 * size // 4)
        s = max(5, size // 10)
        if dtype == 'hearts':
            hr = s // 2
            d.ellipse([cx - hr, cy - hr, cx, cy + hr // 4], fill=(255, 255, 255, 150))
            d.ellipse([cx - hr // 4, cy - hr, cx + hr - hr // 4, cy + hr // 4], fill=(255, 255, 255, 150))
            d.polygon([(cx - hr, cy), (cx + hr - hr // 4, cy), (cx - hr // 4, cy + hr)],
                      fill=(255, 255, 255, 150))
        elif dtype == 'dots':
            r = max(2, s // 3)
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255, 130))
    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=1))
    return Image.alpha_composite(img, overlay)


# ===== SHAPES (all draw white on black, centered) =====

def draw_heart(d, s):
    m = s // 10
    cx = s // 2
    w = s - 2 * m
    r = w // 4
    # Top bumps — overlapping circles
    d.ellipse([cx - w // 2, m, cx + m // 2, m + w // 2 + m // 2], fill=255)
    d.ellipse([cx - m // 2, m, cx + w // 2, m + w // 2 + m // 2], fill=255)
    # Bottom point
    d.polygon([
        (m + m, m + w // 4),
        (s - m - m, m + w // 4),
        (cx, s - m)
    ], fill=255)


def draw_egg(d, s):
    m = s // 8
    # Slightly narrow at top
    d.ellipse([m + s // 14, m, s - m - s // 14, s - m + s // 14], fill=255)


def draw_star5(d, s):
    cx, cy = s // 2, s // 2
    ro = s // 2 - s // 10
    ri = ro * 0.38
    pts = []
    for i in range(10):
        a = math.radians(i * 36 - 90)
        r = ro if i % 2 == 0 else ri
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=255)


def draw_moon(d, s):
    m = s // 7
    d.ellipse([m, m, s - m, s - m], fill=255)
    off = s // 3
    d.ellipse([m + off, m - s // 15, s - m + off, s - m - s // 15], fill=0)


def draw_leaf(d, s):
    cx = s // 2
    m = s // 8
    pts = []
    n = 40
    for i in range(n + 1):
        t = i / n
        y = m + t * (s - 2 * m)
        w = math.sin(t * math.pi) * (s // 2 - m) * 0.5
        w *= (1 - 0.25 * (t - 0.3) ** 2)
        pts.append((cx + w, y))
    for i in range(n, -1, -1):
        t = i / n
        y = m + t * (s - 2 * m)
        w = math.sin(t * math.pi) * (s // 2 - m) * 0.5
        w *= (1 - 0.25 * (t - 0.3) ** 2)
        pts.append((cx - w, y))
    d.polygon(pts, fill=255)
    # Vein
    d.line([(cx, m + s // 10), (cx, s - m - s // 10)], fill=200, width=max(1, s // 25))


def draw_circle(d, s):
    m = s // 7
    d.ellipse([m, m, s - m, s - m], fill=255)


def draw_flower5(d, s):
    cx, cy = s // 2, s // 2
    pr = s // 4  # petal radius
    pd = pr * 0.75  # petal distance from center
    for i in range(5):
        a = math.radians(i * 72 - 90)
        px = cx + pd * math.cos(a)
        py = cy + pd * math.sin(a)
        d.ellipse([px - pr, py - pr, px + pr, py + pr], fill=255)
    # Center
    cr = pr * 0.6
    d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=255)


def draw_daisy(d, s):
    """More petal flower — daisy style."""
    cx, cy = s // 2, s // 2
    pr_w = s // 8   # petal width
    pr_l = s // 3   # petal length
    for i in range(8):
        a = math.radians(i * 45)
        px = cx + (pr_l * 0.5) * math.cos(a)
        py = cy + (pr_l * 0.5) * math.sin(a)
        # Rotated ellipse approximation
        pts = []
        for j in range(20):
            t = j / 19 * 2 * math.pi
            ex = pr_w * 0.5 * math.cos(t)
            ey = pr_l * 0.5 * math.sin(t)
            # Rotate
            rx = ex * math.cos(a) - ey * math.sin(a)
            ry = ex * math.sin(a) + ey * math.cos(a)
            pts.append((px + rx, py + ry))
        d.polygon(pts, fill=255)
    # Center
    cr = s // 7
    d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=255)


def draw_clover(d, s):
    cx = s // 2
    cy = s // 2 - s // 10
    lr = s // 4
    for i in range(3):
        a = math.radians(i * 120 - 90)
        lx = cx + lr * 0.55 * math.cos(a)
        ly = cy + lr * 0.55 * math.sin(a)
        # Each leaf is a heart-ish shape
        d.ellipse([lx - lr, ly - lr, lx + lr, ly + lr], fill=255)
    # Overlap center to make it smoother
    d.ellipse([cx - lr // 2, cy - lr // 2, cx + lr // 2, cy + lr // 2], fill=255)
    # Stem
    sw = max(3, s // 15)
    stem_top = cy + lr // 2
    stem_bot = s - s // 8
    d.line([(cx, stem_top), (cx + s // 12, stem_bot)], fill=255, width=sw)


def draw_snowflake(d, s):
    cx, cy = s // 2, s // 2
    arm = s // 2 - s // 7
    w = max(3, s // 16)
    for i in range(6):
        a = math.radians(i * 60)
        ex = cx + arm * math.cos(a)
        ey = cy + arm * math.sin(a)
        d.line([(cx, cy), (int(ex), int(ey))], fill=255, width=w)
        # Double branches
        for pos in [0.35, 0.6]:
            mx = cx + arm * pos * math.cos(a)
            my = cy + arm * pos * math.sin(a)
            blen = arm * 0.3 * (1.2 - pos)
            for j in [-30, 30]:
                ba = math.radians(i * 60 + j)
                bx = mx + blen * math.cos(ba)
                by = my + blen * math.sin(ba)
                d.line([(int(mx), int(my)), (int(bx), int(by))], fill=255, width=max(2, w - 1))
    cr = w * 2
    d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=255)


def draw_butterfly(d, s):
    cx, cy = s // 2, s // 2
    # Upper wings — large, round
    uw = s * 2 // 5
    uh = s // 3
    d.ellipse([cx - uw - s // 25, cy - uh, cx - s // 25, cy + uh // 5], fill=255)
    d.ellipse([cx + s // 25, cy - uh, cx + uw + s // 25, cy + uh // 5], fill=255)
    # Lower wings
    lw = s * 3 // 10
    lh = s // 4
    d.ellipse([cx - lw - s // 30, cy - lh // 5, cx - s // 30, cy + lh], fill=255)
    d.ellipse([cx + s // 30, cy - lh // 5, cx + lw + s // 30, cy + lh], fill=255)
    # Body
    bw = max(3, s // 18)
    d.rounded_rectangle([cx - bw, cy - s // 5, cx + bw, cy + s // 5], radius=bw, fill=255)
    # Antennae
    aw = max(2, bw // 2)
    d.line([(cx - 2, cy - s // 5), (cx - s // 7, cy - s // 3)], fill=255, width=aw)
    d.line([(cx + 2, cy - s // 5), (cx + s // 7, cy - s // 3)], fill=255, width=aw)
    # Antenna tips
    tr = max(3, s // 25)
    d.ellipse([cx - s // 7 - tr, cy - s // 3 - tr, cx - s // 7 + tr, cy - s // 3 + tr], fill=255)
    d.ellipse([cx + s // 7 - tr, cy - s // 3 - tr, cx + s // 7 + tr, cy - s // 3 + tr], fill=255)


# ===== WATERMARK =====

def add_watermark(img, text="MrsMillennial Designs"):
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    try:
        font = ImageFont.truetype(FONT_PATH, 42)
        font_sm = ImageFont.truetype(FONT_PATH, 36)
    except:
        font = ImageFont.load_default()
        font_sm = font
    w, h = img.size
    # Diagonal watermarks like the original
    positions = [
        (w // 8, h * 2 // 9, font),
        (w * 3 // 8, h // 2 - 15, font),
        (w // 8, h * 7 // 9, font_sm),
    ]
    for px, py, f in positions:
        d.text((px + 1, py + 1), text, font=f, fill=(80, 60, 60, 18))
        d.text((px, py), text, font=f, fill=(100, 80, 80, 38))
    return Image.alpha_composite(img.convert('RGBA'), overlay)


# ===== PATTERN BUILDER =====

def place_element(canvas, elem, x, y, tile_size):
    """Place element with seamless edge wrapping."""
    px = int(x - elem.width // 2)
    py = int(y - elem.height // 2)
    for wx in [0, -tile_size, tile_size]:
        for wy in [0, -tile_size, tile_size]:
            nx, ny = px + wx, py + wy
            if (nx + elem.width > 0 and nx < tile_size and
                    ny + elem.height > 0 and ny < tile_size):
                canvas.alpha_composite(elem, (nx, ny))


def build_grid_pattern(tile_size, draw_func, colors, elem_size,
                       rows, cols, rot=0, scale_var=0,
                       details=None, det_count=0):
    canvas = Image.new('RGBA', (tile_size, tile_size), (255, 255, 255, 255))
    sx = tile_size / cols
    sy = tile_size / rows
    ci = 0
    for row in range(rows + 1):
        for col in range(cols + 1):
            x = col * sx + (sx / 2 if row % 2 else 0)
            y = row * sy
            x += random.uniform(-2, 2)
            y += random.uniform(-2, 2)
            color = colors[ci % len(colors)]
            ci += 1
            sc = 1.0 + random.uniform(-scale_var, scale_var)
            esz = max(20, int(elem_size * sc))
            elem = watercolor_shape(draw_func, esz, color)
            if details:
                elem = add_details(elem, esz, details, det_count)
            if rot > 0:
                elem = elem.rotate(random.uniform(-rot, rot), expand=True,
                                   resample=Image.BICUBIC)
            place_element(canvas, elem, x, y, tile_size)
    return canvas


# ===== MAIN =====

def main():
    results = {}

    # 1. PASTEL HEARTS — dense, larger, vibrant
    print("1/8: Pastel Hearts...")
    results['pastel-hearts-seamless-pattern'] = build_grid_pattern(
        TILE_SIZE, draw_heart,
        [(235, 140, 170), (180, 160, 245), (140, 215, 185),
         (250, 200, 150), (150, 200, 235), (245, 175, 190)],
        elem_size=155, rows=7, cols=7, rot=12, scale_var=0.08,
        details='hearts', det_count=4
    )

    # 2. SPRING WILDFLOWERS — use daisy + colored centers
    print("2/8: Spring Wildflowers...")
    canvas = Image.new('RGBA', (TILE_SIZE, TILE_SIZE), (255, 255, 255, 255))
    petal_c = [(248, 145, 175), (250, 215, 100), (135, 185, 250),
               (255, 155, 120), (185, 170, 250), (150, 220, 185)]
    center_c = [(255, 210, 80), (255, 195, 110), (245, 200, 75)]
    sx, sy = TILE_SIZE / 6, TILE_SIZE / 6
    ci = 0
    for row in range(7):
        for col in range(7):
            x = col * sx + (sx / 2 if row % 2 else 0)
            y = row * sy
            x += random.uniform(-3, 3)
            y += random.uniform(-3, 3)
            sc = 1.0 + random.uniform(-0.1, 0.1)
            esz = int(170 * sc)
            pc = petal_c[ci % len(petal_c)]
            cc = center_c[ci % len(center_c)]
            ci += 1
            elem = watercolor_shape(draw_flower5, esz, pc)
            # Colored center
            csz = esz // 3
            ctr = watercolor_shape(draw_circle, csz, cc)
            off = (esz - csz) // 2
            elem.alpha_composite(ctr, (off, off))
            elem = elem.rotate(random.uniform(-20, 20), expand=True,
                               resample=Image.BICUBIC)
            place_element(canvas, elem, x, y, TILE_SIZE)
    results['spring-wildflower-seamless-pattern'] = canvas

    # 3. AUTUMN LEAVES & BERRIES
    print("3/8: Autumn Leaves...")
    canvas = Image.new('RGBA', (TILE_SIZE, TILE_SIZE), (255, 255, 255, 255))
    leaf_c = [(215, 100, 25), (185, 85, 25), (225, 155, 45),
              (190, 55, 25), (205, 125, 40), (175, 70, 20)]
    berry_c = [(205, 75, 35), (225, 110, 45), (185, 55, 25)]
    sx, sy = TILE_SIZE / 7, TILE_SIZE / 7
    ci = 0
    for row in range(8):
        for col in range(8):
            x = col * sx + (sx / 2 if row % 2 else 0)
            y = row * sy
            x += random.uniform(-5, 5)
            y += random.uniform(-5, 5)
            ci += 1
            if random.random() < 0.25:
                # Berry cluster
                for _ in range(random.randint(3, 5)):
                    bsz = random.randint(28, 40)
                    bc = berry_c[random.randint(0, len(berry_c) - 1)]
                    berry = watercolor_shape(draw_circle, bsz, bc)
                    bx = x + random.uniform(-20, 20)
                    by = y + random.uniform(-20, 20)
                    place_element(canvas, berry, bx, by, TILE_SIZE)
            else:
                sc = 1.0 + random.uniform(-0.12, 0.12)
                esz = int(135 * sc)
                lc = leaf_c[ci % len(leaf_c)]
                elem = watercolor_shape(draw_leaf, esz, lc)
                elem = elem.rotate(random.uniform(-50, 50), expand=True,
                                   resample=Image.BICUBIC)
                place_element(canvas, elem, x, y, TILE_SIZE)
    results['autumn-leaves-seamless-pattern'] = canvas

    # 4. CELESTIAL STARS & MOONS
    print("4/8: Celestial Stars & Moons...")
    canvas = Image.new('RGBA', (TILE_SIZE, TILE_SIZE), (255, 255, 255, 255))
    cel_c = [(250, 210, 155), (155, 200, 240), (255, 215, 170),
             (185, 170, 245), (255, 230, 160)]
    sx, sy = TILE_SIZE / 8, TILE_SIZE / 8
    ci = 0
    for row in range(9):
        for col in range(9):
            x = col * sx + (sx / 2 if row % 2 else 0)
            y = row * sy
            x += random.uniform(-3, 3)
            y += random.uniform(-3, 3)
            color = cel_c[ci % len(cel_c)]
            ci += 1
            sc = 1.0 + random.uniform(-0.08, 0.08)
            if (row + col) % 3 == 0:
                esz = int(125 * sc)
                elem = watercolor_shape(draw_moon, esz, color)
            else:
                esz = int(115 * sc)
                elem = watercolor_shape(draw_star5, esz, color)
                elem = add_details(elem, esz, 'dots', 2)
            elem = elem.rotate(random.uniform(-15, 15), expand=True,
                               resample=Image.BICUBIC)
            place_element(canvas, elem, x, y, TILE_SIZE)
    results['celestial-stars-seamless-pattern'] = canvas

    # 5. WATERCOLOR BUTTERFLIES
    print("5/8: Butterflies...")
    results['watercolor-butterfly-seamless-pattern'] = build_grid_pattern(
        TILE_SIZE, draw_butterfly,
        [(155, 205, 240), (245, 155, 195), (195, 180, 250),
         (255, 210, 140), (165, 225, 195)],
        elem_size=165, rows=6, cols=6, rot=15, scale_var=0.1
    )

    # 6. LUCKY SHAMROCKS
    print("6/8: Shamrocks...")
    results['lucky-shamrock-seamless-pattern'] = build_grid_pattern(
        TILE_SIZE, draw_clover,
        [(65, 170, 75), (95, 195, 95), (45, 140, 55),
         (120, 200, 125), (75, 165, 80)],
        elem_size=145, rows=7, cols=7, rot=15, scale_var=0.08
    )

    # 7. WINTER SNOWFLAKES
    print("7/8: Snowflakes...")
    results['winter-snowflake-seamless-pattern'] = build_grid_pattern(
        TILE_SIZE, draw_snowflake,
        [(155, 205, 240), (185, 215, 245), (135, 190, 235),
         (175, 210, 242), (145, 195, 238)],
        elem_size=155, rows=6, cols=6, rot=30, scale_var=0.15
    )

    # 8. PASTEL POLKA DOTS (with hearts like Easter eggs)
    print("8/8: Polka Dots...")
    results['pastel-polka-dot-seamless-pattern'] = build_grid_pattern(
        TILE_SIZE, draw_circle,
        [(235, 145, 175), (155, 210, 235), (185, 170, 248),
         (150, 220, 190), (250, 205, 155), (255, 215, 175)],
        elem_size=120, rows=8, cols=8, rot=0, scale_var=0.05,
        details='hearts', det_count=5
    )

    # Save all
    for name, img in results.items():
        wm = add_watermark(img)
        path = os.path.join(OUTPUT_DIR, f"{name}.png")
        wm.convert('RGB').save(path, 'PNG', dpi=(300, 300))
        # Clean version
        clean = os.path.join(OUTPUT_DIR, f"{name}-clean.png")
        img.convert('RGB').save(clean, 'PNG', dpi=(300, 300))
        print(f"  -> {path}")

    print(f"\nDone! {len(results)} patterns saved.")


if __name__ == '__main__':
    main()
