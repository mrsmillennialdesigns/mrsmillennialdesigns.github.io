#!/usr/bin/env python3
"""Fix the 4 weaker patterns: shamrocks, butterflies, snowflakes, autumn leaves."""

from PIL import Image, ImageDraw, ImageFilter, ImageFont
import numpy as np
import random
import math
import os

random.seed(42)
np.random.seed(42)

OUTPUT_DIR = '/Users/alexhosage/Desktop/mmd-website/img/patterns'
TILE_SIZE = 1200
FONT_PATH = '/System/Library/Fonts/Avenir Next.ttc'


def watercolor_shape(draw_func, size, base_color):
    big = size * 2
    mask_img = Image.new('L', (big, big), 0)
    mask_draw = ImageDraw.Draw(mask_img)
    draw_func(mask_draw, big)
    mask_img = mask_img.filter(ImageFilter.GaussianBlur(radius=max(2, big // 25)))

    r, g, b = base_color
    base = np.full((big, big, 3), [r, g, b], dtype=np.float64)
    noise_lo = np.random.normal(0, 25, (big // 4, big // 4, 3))
    noise_lo_img = Image.fromarray(np.clip(noise_lo + 128, 0, 255).astype(np.uint8))
    noise_lo_img = noise_lo_img.resize((big, big), Image.BILINEAR)
    noise_lo = np.array(noise_lo_img).astype(np.float64) - 128
    noise_hi = np.random.normal(0, 10, (big, big, 3))
    noise_hi_img = Image.fromarray(np.clip(noise_hi + 128, 0, 255).astype(np.uint8))
    noise_hi_img = noise_hi_img.filter(ImageFilter.GaussianBlur(radius=2))
    noise_hi = np.array(noise_hi_img).astype(np.float64) - 128
    textured = np.clip(base + noise_lo * 0.5 + noise_hi * 0.3, 0, 255)

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
    for px, py, f in [(w // 8, h * 2 // 9, font), (w * 3 // 8, h // 2 - 15, font),
                       (w // 8, h * 7 // 9, font_sm)]:
        d.text((px + 1, py + 1), text, font=f, fill=(80, 60, 60, 18))
        d.text((px, py), text, font=f, fill=(100, 80, 80, 38))
    return Image.alpha_composite(img.convert('RGBA'), overlay)


def place_element(canvas, elem, x, y, ts):
    px, py = int(x - elem.width // 2), int(y - elem.height // 2)
    for wx in [0, -ts, ts]:
        for wy in [0, -ts, ts]:
            nx, ny = px + wx, py + wy
            if nx + elem.width > 0 and nx < ts and ny + elem.height > 0 and ny < ts:
                canvas.alpha_composite(elem, (nx, ny))


def draw_circle(d, s):
    m = s // 7
    d.ellipse([m, m, s - m, s - m], fill=255)


def draw_leaf(d, s):
    cx, m = s // 2, s // 8
    pts = []
    n = 40
    for i in range(n + 1):
        t = i / n
        y = m + t * (s - 2 * m)
        w = math.sin(t * math.pi) * (s // 2 - m) * 0.5 * (1 - 0.25 * (t - 0.3) ** 2)
        pts.append((cx + w, y))
    for i in range(n, -1, -1):
        t = i / n
        y = m + t * (s - 2 * m)
        w = math.sin(t * math.pi) * (s // 2 - m) * 0.5 * (1 - 0.25 * (t - 0.3) ** 2)
        pts.append((cx - w, y))
    d.polygon(pts, fill=255)
    d.line([(cx, m + s // 10), (cx, s - m - s // 10)], fill=200, width=max(1, s // 25))


# ===== IMPROVED SHAMROCK =====
def draw_shamrock(d, s):
    """Better shamrock: 3 distinct heart-shaped leaves."""
    cx, cy = s // 2, s * 4 // 10
    lr = s // 5  # leaf radius

    for i in range(3):
        angle = math.radians(i * 120 - 90)
        # Position leaf center
        lx = cx + lr * 0.75 * math.cos(angle)
        ly = cy + lr * 0.75 * math.sin(angle)

        # Each leaf is a heart shape pointing outward
        leaf_angle = math.radians(i * 120 - 90)
        # Two overlapping circles + triangle pointing outward
        spread = lr * 0.35
        c1x = lx + spread * math.cos(leaf_angle + math.radians(30))
        c1y = ly + spread * math.sin(leaf_angle + math.radians(30))
        c2x = lx + spread * math.cos(leaf_angle - math.radians(30))
        c2y = ly + spread * math.sin(leaf_angle - math.radians(30))

        d.ellipse([c1x - lr * 0.55, c1y - lr * 0.55, c1x + lr * 0.55, c1y + lr * 0.55], fill=255)
        d.ellipse([c2x - lr * 0.55, c2y - lr * 0.55, c2x + lr * 0.55, c2y + lr * 0.55], fill=255)

        # Inner fill triangle
        tip_x = lx - lr * 0.4 * math.cos(leaf_angle)
        tip_y = ly - lr * 0.4 * math.sin(leaf_angle)
        d.polygon([(c1x, c1y), (c2x, c2y), (tip_x, tip_y)], fill=255)

    # Center overlap
    d.ellipse([cx - lr * 0.3, cy - lr * 0.3, cx + lr * 0.3, cy + lr * 0.3], fill=255)

    # Stem
    sw = max(3, s // 16)
    d.line([(cx, cy + lr * 0.3), (cx + s // 14, s - s // 7)], fill=255, width=sw)


# ===== IMPROVED BUTTERFLY =====
def draw_butterfly_v2(d, s):
    """Better butterfly with pointed wing tips."""
    cx, cy = s // 2, s // 2

    # Upper wings — teardrop shapes (wider at body, pointed at tips)
    for side in [-1, 1]:
        pts = []
        # Wing outline as bezier-like polygon
        wing_w = s * 0.42
        wing_h = s * 0.35
        steps = 30
        for i in range(steps + 1):
            t = i / steps
            # Parametric wing shape
            angle = t * math.pi
            # Width varies: narrow at body, wide in middle, pointed at tip
            x_factor = math.sin(angle) ** 0.7
            # Height follows smooth curve
            y_val = -wing_h * (1 - t)  # top to bottom
            x_val = side * wing_w * x_factor

            # Slight scallop on outer edge
            if 0.3 < t < 0.8:
                x_val *= 1.05

            pts.append((cx + x_val, cy + y_val + wing_h * 0.3))

        # Close back to body
        pts.append((cx, cy + wing_h * 0.3))
        d.polygon(pts, fill=255)

    # Lower wings — smaller, rounder
    for side in [-1, 1]:
        lw = s * 0.3
        lh = s * 0.25
        lwx = cx + side * lw * 0.4
        lwy = cy + lh * 0.3
        d.ellipse([lwx - lw * 0.55, lwy - lh * 0.4,
                   lwx + lw * 0.55, lwy + lh * 0.7], fill=255)

    # Body
    bw = max(3, s // 18)
    d.rounded_rectangle([cx - bw, cy - s * 0.22, cx + bw, cy + s * 0.22],
                         radius=bw, fill=255)
    # Antennae — curved
    aw = max(2, bw // 2)
    for side in [-1, 1]:
        # Draw antenna as series of small segments for curve
        steps = 10
        prev = (cx + side * 2, cy - s * 0.22)
        for i in range(1, steps + 1):
            t = i / steps
            ax = cx + side * (s * 0.12 * t + s * 0.02 * math.sin(t * math.pi))
            ay = cy - s * 0.22 - s * 0.12 * t
            d.line([prev, (int(ax), int(ay))], fill=255, width=aw)
            prev = (int(ax), int(ay))
        # Tip dot
        tr = max(3, s // 28)
        d.ellipse([prev[0] - tr, prev[1] - tr, prev[0] + tr, prev[1] + tr], fill=255)


# ===== IMPROVED SNOWFLAKE =====
def draw_snowflake_v2(d, s):
    """More detailed, crystalline snowflake."""
    cx, cy = s // 2, s // 2
    arm = s // 2 - s // 8
    w = max(3, s // 18)

    for i in range(6):
        a = math.radians(i * 60)
        # Main arm
        ex = cx + arm * math.cos(a)
        ey = cy + arm * math.sin(a)
        d.line([(cx, cy), (int(ex), int(ey))], fill=255, width=w)

        # Tip diamond
        tip_r = max(4, s // 22)
        d.regular_polygon((int(ex), int(ey), tip_r), 4, rotation=i * 60, fill=255)

        # Triple branches at 3 positions
        for pos in [0.3, 0.5, 0.7]:
            mx = cx + arm * pos * math.cos(a)
            my = cy + arm * pos * math.sin(a)
            blen = arm * 0.28 * (1.3 - pos)
            bw = max(2, w - 1)
            for j in [-45, 45]:
                ba = math.radians(i * 60 + j)
                bx = mx + blen * math.cos(ba)
                by = my + blen * math.sin(ba)
                d.line([(int(mx), int(my)), (int(bx), int(by))], fill=255, width=bw)

    # Center crystal
    cr = max(5, w * 3)
    d.regular_polygon((cx, cy, cr), 6, fill=255)


# ===== MAPLE LEAF for autumn =====
def draw_maple_leaf(d, s):
    """More recognizable autumn leaf shape."""
    cx, cy = s // 2, s * 45 // 100
    r = s * 35 // 100
    pts = []
    # Create a maple-like leaf with pointed lobes
    angles_and_radii = [
        (0, 1.0), (20, 0.55), (35, 0.8), (55, 0.4),
        (72, 0.85), (90, 0.45), (110, 0.5),
        (130, 0.3), (155, 0.45), (180, 0.35),
        (205, 0.45), (230, 0.3), (250, 0.5),
        (270, 0.45), (288, 0.85), (305, 0.4),
        (325, 0.8), (340, 0.55), (360, 1.0)
    ]
    for ang, rad in angles_and_radii:
        a = math.radians(ang - 90)  # Start pointing up
        px = cx + r * rad * math.cos(a)
        py = cy + r * rad * math.sin(a)
        pts.append((px, py))
    d.polygon(pts, fill=255)
    # Stem
    sw = max(2, s // 20)
    d.line([(cx, cy + r * 0.3), (cx + s // 15, s - s // 8)], fill=255, width=sw)


def save_pattern(name, canvas):
    wm = add_watermark(canvas)
    path = os.path.join(OUTPUT_DIR, f"{name}.png")
    wm.convert('RGB').save(path, 'PNG', dpi=(300, 300))
    clean = os.path.join(OUTPUT_DIR, f"{name}-clean.png")
    canvas.convert('RGB').save(clean, 'PNG', dpi=(300, 300))
    print(f"  -> {path}")


def main():
    # FIX 1: SHAMROCKS
    print("Fixing shamrocks...")
    random.seed(100)
    np.random.seed(100)
    canvas = Image.new('RGBA', (TILE_SIZE, TILE_SIZE), (255, 255, 255, 255))
    colors = [(60, 168, 70), (90, 195, 90), (40, 138, 50),
              (115, 200, 120), (70, 160, 75), (50, 150, 60)]
    sx, sy = TILE_SIZE / 7, TILE_SIZE / 7
    ci = 0
    for row in range(8):
        for col in range(8):
            x = col * sx + (sx / 2 if row % 2 else 0)
            y = row * sy
            x += random.uniform(-3, 3)
            y += random.uniform(-3, 3)
            color = colors[ci % len(colors)]
            ci += 1
            sc = 1.0 + random.uniform(-0.08, 0.08)
            esz = int(150 * sc)
            elem = watercolor_shape(draw_shamrock, esz, color)
            elem = elem.rotate(random.uniform(-12, 12), expand=True, resample=Image.BICUBIC)
            place_element(canvas, elem, x, y, TILE_SIZE)
    save_pattern('lucky-shamrock-seamless-pattern', canvas)

    # FIX 2: BUTTERFLIES
    print("Fixing butterflies...")
    random.seed(200)
    np.random.seed(200)
    canvas = Image.new('RGBA', (TILE_SIZE, TILE_SIZE), (255, 255, 255, 255))
    colors = [(150, 200, 240), (245, 150, 195), (190, 175, 250),
              (255, 205, 135), (160, 225, 190), (230, 175, 220)]
    sx, sy = TILE_SIZE / 6, TILE_SIZE / 6
    ci = 0
    for row in range(7):
        for col in range(7):
            x = col * sx + (sx / 2 if row % 2 else 0)
            y = row * sy
            x += random.uniform(-3, 3)
            y += random.uniform(-3, 3)
            color = colors[ci % len(colors)]
            ci += 1
            sc = 1.0 + random.uniform(-0.1, 0.1)
            esz = int(170 * sc)
            elem = watercolor_shape(draw_butterfly_v2, esz, color)
            elem = elem.rotate(random.uniform(-15, 15), expand=True, resample=Image.BICUBIC)
            place_element(canvas, elem, x, y, TILE_SIZE)
    save_pattern('watercolor-butterfly-seamless-pattern', canvas)

    # FIX 3: SNOWFLAKES
    print("Fixing snowflakes...")
    random.seed(300)
    np.random.seed(300)
    canvas = Image.new('RGBA', (TILE_SIZE, TILE_SIZE), (255, 255, 255, 255))
    colors = [(140, 195, 240), (170, 210, 248), (120, 180, 230),
              (160, 205, 242), (130, 190, 235)]
    sx, sy = TILE_SIZE / 6, TILE_SIZE / 6
    ci = 0
    for row in range(7):
        for col in range(7):
            x = col * sx + (sx / 2 if row % 2 else 0)
            y = row * sy
            x += random.uniform(-3, 3)
            y += random.uniform(-3, 3)
            color = colors[ci % len(colors)]
            ci += 1
            sc = 1.0 + random.uniform(-0.12, 0.12)
            esz = int(165 * sc)
            elem = watercolor_shape(draw_snowflake_v2, esz, color)
            elem = elem.rotate(random.uniform(-30, 30), expand=True, resample=Image.BICUBIC)
            place_element(canvas, elem, x, y, TILE_SIZE)
    save_pattern('winter-snowflake-seamless-pattern', canvas)

    # FIX 4: AUTUMN LEAVES (denser, with maple leaves mixed in)
    print("Fixing autumn leaves...")
    random.seed(400)
    np.random.seed(400)
    canvas = Image.new('RGBA', (TILE_SIZE, TILE_SIZE), (255, 255, 255, 255))
    leaf_c = [(218, 100, 22), (188, 82, 22), (228, 158, 42),
              (195, 52, 22), (208, 128, 38), (178, 68, 18)]
    berry_c = [(208, 72, 32), (228, 108, 42), (188, 52, 22)]
    sx, sy = TILE_SIZE / 7, TILE_SIZE / 7
    ci = 0
    for row in range(8):
        for col in range(8):
            x = col * sx + (sx / 2 if row % 2 else 0)
            y = row * sy
            x += random.uniform(-5, 5)
            y += random.uniform(-5, 5)
            ci += 1
            if random.random() < 0.2:
                # Berry cluster
                for _ in range(random.randint(3, 6)):
                    bsz = random.randint(30, 45)
                    bc = berry_c[random.randint(0, len(berry_c) - 1)]
                    berry = watercolor_shape(draw_circle, bsz, bc)
                    bx = x + random.uniform(-22, 22)
                    by = y + random.uniform(-22, 22)
                    place_element(canvas, berry, bx, by, TILE_SIZE)
            else:
                sc = 1.0 + random.uniform(-0.1, 0.1)
                lc = leaf_c[ci % len(leaf_c)]
                # Mix regular leaves and maple leaves
                if random.random() < 0.4:
                    esz = int(145 * sc)
                    elem = watercolor_shape(draw_maple_leaf, esz, lc)
                else:
                    esz = int(140 * sc)
                    elem = watercolor_shape(draw_leaf, esz, lc)
                elem = elem.rotate(random.uniform(-45, 45), expand=True,
                                   resample=Image.BICUBIC)
                place_element(canvas, elem, x, y, TILE_SIZE)
    save_pattern('autumn-leaves-seamless-pattern', canvas)

    print("\nAll 4 patterns fixed!")


if __name__ == '__main__':
    main()
