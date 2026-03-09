#!/usr/bin/env python3
"""
Seamless Pattern Generator for MrsMillennial Designs
Creates watercolor-style seamless patterns matching Andrea's aesthetic.
Output: 1200x1200 PNG tiles (same as existing Easter egg pattern)
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


def watercolor_shape(draw_func, size, base_color, edge_darken=True):
    """Create a watercolor-textured shape element as RGBA."""
    # Work at 2x for antialiasing
    big = size * 2

    # Create shape mask
    mask_img = Image.new('L', (big, big), 0)
    mask_draw = ImageDraw.Draw(mask_img)
    draw_func(mask_draw, big)

    # Soften edges for watercolor look
    mask_img = mask_img.filter(ImageFilter.GaussianBlur(radius=max(2, big // 30)))

    # Create base color layer with noise texture
    r, g, b = base_color
    base = np.full((big, big, 3), [r, g, b], dtype=np.float64)

    # Large-scale color variation (watercolor wash effect)
    noise_large = np.random.normal(0, 20, (big // 4, big // 4, 3))
    noise_large = np.array(Image.fromarray(
        np.clip(noise_large + 128, 0, 255).astype(np.uint8)
    ).resize((big, big), Image.BILINEAR)).astype(np.float64) - 128

    # Small-scale grain
    noise_small = np.random.normal(0, 8, (big, big, 3))
    noise_small_img = Image.fromarray(
        np.clip(noise_small + 128, 0, 255).astype(np.uint8)
    ).filter(ImageFilter.GaussianBlur(radius=2))
    noise_small = np.array(noise_small_img).astype(np.float64) - 128

    textured = np.clip(base + noise_large * 0.6 + noise_small * 0.4, 0, 255)

    # Edge darkening (pigment accumulation)
    if edge_darken:
        mask_arr = np.array(mask_img).astype(np.float64) / 255.0
        erode_size = max(3, big // 12)
        if erode_size % 2 == 0:
            erode_size += 1
        eroded = np.array(
            mask_img.filter(ImageFilter.MinFilter(erode_size))
        ).astype(np.float64) / 255.0
        edge = np.clip(mask_arr - eroded, 0, 1)
        # Blur the edge for smooth transition
        edge_img = Image.fromarray((edge * 255).astype(np.uint8))
        edge_img = edge_img.filter(ImageFilter.GaussianBlur(radius=max(2, big // 20)))
        edge = np.array(edge_img).astype(np.float64) / 255.0
        for c in range(3):
            textured[:, :, c] = textured[:, :, c] * (1 - edge * 0.2)

    # Create RGBA
    rgb = Image.fromarray(textured.astype(np.uint8))
    result = Image.new('RGBA', (big, big), (0, 0, 0, 0))
    result.paste(rgb, mask=mask_img)

    # Downscale for antialiasing
    result = result.resize((size, size), Image.LANCZOS)
    return result


def add_white_details(img, size, detail_type='hearts', count=6):
    """Add small white detail marks to an element."""
    overlay = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    for _ in range(count):
        cx = random.randint(size // 4, 3 * size // 4)
        cy = random.randint(size // 4, 3 * size // 4)
        ds = max(4, size // 14)

        if detail_type == 'hearts':
            hr = ds // 2
            draw.ellipse([cx - hr, cy - hr, cx + hr // 2, cy], fill=(255, 255, 255, 140))
            draw.ellipse([cx - hr // 2, cy - hr, cx + hr, cy], fill=(255, 255, 255, 140))
            draw.polygon([(cx - hr, cy - hr // 4), (cx + hr, cy - hr // 4),
                          (cx, cy + hr)], fill=(255, 255, 255, 140))
        elif detail_type == 'dots':
            dr = max(2, ds // 3)
            draw.ellipse([cx - dr, cy - dr, cx + dr, cy + dr], fill=(255, 255, 255, 120))
        elif detail_type == 'stars':
            sr = max(3, ds // 2)
            points = []
            for i in range(10):
                a = math.radians(i * 36 - 90)
                r = sr if i % 2 == 0 else sr * 0.4
                points.append((cx + r * math.cos(a), cy + r * math.sin(a)))
            draw.polygon(points, fill=(255, 255, 255, 130))

    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=1))
    return Image.alpha_composite(img, overlay)


# ===== SHAPE DRAWING FUNCTIONS =====

def draw_heart(draw, size):
    m = size // 8
    cx = size // 2
    r = (size - 2 * m) // 4
    # Two circles for bumps
    draw.ellipse([cx - 2 * r + m // 2, m, cx, m + 2 * r], fill=255)
    draw.ellipse([cx, m, cx + 2 * r - m // 2, m + 2 * r], fill=255)
    # Bottom point
    draw.polygon([
        (m + r // 3, m + r + r // 3),
        (size - m - r // 3, m + r + r // 3),
        (cx, size - m)
    ], fill=255)


def draw_egg(draw, size):
    m = size // 6
    # Slightly taller than wide, narrow at top
    draw.ellipse([m + size // 12, m, size - m - size // 12, size - m], fill=255)


def draw_star5(draw, size):
    cx, cy = size // 2, size // 2
    r_out = size // 2 - size // 8
    r_in = r_out * 0.4
    points = []
    for i in range(10):
        angle = math.radians(i * 36 - 90)
        r = r_out if i % 2 == 0 else r_in
        points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.polygon(points, fill=255)


def draw_moon(draw, size):
    m = size // 6
    draw.ellipse([m, m, size - m, size - m], fill=255)
    offset = size // 3
    draw.ellipse([m + offset, m - size // 12, size - m + offset, size - m - size // 12], fill=0)


def draw_leaf(draw, size):
    cx = size // 2
    m = size // 6
    points = []
    steps = 30
    for i in range(steps + 1):
        t = i / steps
        y = m + t * (size - 2 * m)
        w = math.sin(t * math.pi) * (size // 2 - m) * 0.45
        # Asymmetric leaf shape
        w *= (1 - 0.3 * abs(t - 0.35))
        points.append((cx + w, y))
    for i in range(steps, -1, -1):
        t = i / steps
        y = m + t * (size - 2 * m)
        w = math.sin(t * math.pi) * (size // 2 - m) * 0.45
        w *= (1 - 0.3 * abs(t - 0.35))
        points.append((cx - w, y))
    draw.polygon(points, fill=255)


def draw_circle(draw, size):
    m = size // 6
    draw.ellipse([m, m, size - m, size - m], fill=255)


def draw_flower5(draw, size):
    cx, cy = size // 2, size // 2
    petal_r = size // 5
    petal_dist = petal_r * 0.8
    for i in range(5):
        angle = math.radians(i * 72 - 90)
        px = cx + petal_dist * math.cos(angle)
        py = cy + petal_dist * math.sin(angle)
        draw.ellipse([px - petal_r, py - petal_r, px + petal_r, py + petal_r], fill=255)
    # Center dot (will be recolored)
    cr = petal_r // 2
    draw.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=255)


def draw_clover(draw, size):
    cx = size // 2
    cy = size // 2 - size // 12
    lr = size // 5
    for i in range(3):
        angle = math.radians(i * 120 - 90)
        lx = cx + lr * 0.6 * math.cos(angle)
        ly = cy + lr * 0.6 * math.sin(angle)
        draw.ellipse([lx - lr, ly - lr, lx + lr, ly + lr], fill=255)
    # Stem
    sw = max(2, size // 18)
    draw.line([(cx, cy + lr), (cx + size // 10, size - size // 6)], fill=255, width=sw)


def draw_snowflake(draw, size):
    cx, cy = size // 2, size // 2
    arm_len = size // 2 - size // 6
    w = max(3, size // 18)
    for i in range(6):
        angle = math.radians(i * 60)
        ex = cx + arm_len * math.cos(angle)
        ey = cy + arm_len * math.sin(angle)
        draw.line([(cx, cy), (int(ex), int(ey))], fill=255, width=w)
        # Branches
        blen = arm_len * 0.35
        for pos in [0.4, 0.65]:
            mx = cx + arm_len * pos * math.cos(angle)
            my = cy + arm_len * pos * math.sin(angle)
            for j in [-35, 35]:
                ba = math.radians(i * 60 + j)
                bx = mx + blen * math.cos(ba)
                by = my + blen * math.sin(ba)
                draw.line([(int(mx), int(my)), (int(bx), int(by))],
                          fill=255, width=max(1, w - 1))
    cr = w * 2
    draw.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=255)


def draw_butterfly(draw, size):
    cx, cy = size // 2, size // 2
    # Upper wings
    uw = size * 3 // 8
    uh = size * 3 // 10
    draw.ellipse([cx - uw, cy - uh, cx - size // 30, cy + uh // 6], fill=255)
    draw.ellipse([cx + size // 30, cy - uh, cx + uw, cy + uh // 6], fill=255)
    # Lower wings
    lw = size // 4
    lh = size // 4
    draw.ellipse([cx - lw - size // 30, cy - lh // 6, cx - size // 30, cy + lh], fill=255)
    draw.ellipse([cx + size // 30, cy - lh // 6, cx + lw + size // 30, cy + lh], fill=255)
    # Body
    bw = max(3, size // 20)
    draw.rounded_rectangle([cx - bw, cy - size // 5, cx + bw, cy + size // 5],
                            radius=bw, fill=255)
    # Antennae
    draw.line([(cx - bw, cy - size // 5), (cx - size // 6, cy - size // 3)],
              fill=255, width=max(1, bw // 2))
    draw.line([(cx + bw, cy - size // 5), (cx + size // 6, cy - size // 3)],
              fill=255, width=max(1, bw // 2))


# ===== WATERMARK =====

def add_watermark(img, text="MrsMillennial Designs"):
    """Add subtle diagonal watermark like the original Easter egg pattern."""
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    try:
        font = ImageFont.truetype(FONT_PATH, 38)
    except:
        font = ImageFont.load_default()

    # Place watermark text diagonally across the image
    w, h = img.size
    positions = [
        (w // 6, h // 4),
        (w // 2 - 80, h // 2 - 10),
        (w // 6, h * 3 // 4),
    ]
    for px, py in positions:
        # Draw text with slight shadow
        draw.text((px + 1, py + 1), text, font=font, fill=(0, 0, 0, 12))
        draw.text((px, py), text, font=font, fill=(120, 100, 100, 35))

    return Image.alpha_composite(img.convert('RGBA'), overlay)


# ===== MIXED PATTERN (stars + moons) =====

def create_mixed_celestial(tile_size, colors):
    """Create pattern with alternating stars and moons."""
    canvas = Image.new('RGBA', (tile_size, tile_size), (255, 255, 255, 255))

    elem_size = 100
    rows, cols = 9, 9
    sx = tile_size / cols
    sy = tile_size / rows
    ci = 0

    for row in range(rows + 1):
        for col in range(cols + 1):
            x = col * sx + (sx / 2 if row % 2 else 0)
            y = row * sy
            x += random.uniform(-3, 3)
            y += random.uniform(-3, 3)

            color = colors[ci % len(colors)]
            ci += 1
            scale = 1.0 + random.uniform(-0.1, 0.1)
            esz = int(elem_size * scale)

            # Alternate between stars and moons
            if (row + col) % 3 == 0:
                elem = watercolor_shape(draw_moon, esz, color)
            else:
                elem = watercolor_shape(draw_star5, esz, color)
                elem = add_white_details(elem, esz, 'dots', 3)

            angle = random.uniform(-15, 15)
            elem = elem.rotate(angle, expand=True, resample=Image.BICUBIC)

            px = int(x - elem.width // 2)
            py = int(y - elem.height // 2)
            for wx in [0, -tile_size, tile_size]:
                for wy in [0, -tile_size, tile_size]:
                    nx, ny = px + wx, py + wy
                    if (nx + elem.width > 0 and nx < tile_size and
                            ny + elem.height > 0 and ny < tile_size):
                        canvas.alpha_composite(elem, (nx, ny))
    return canvas


# ===== FLOWER PATTERN WITH CENTERS =====

def create_flower_pattern(tile_size, petal_colors, center_colors):
    """Flowers with different colored centers."""
    canvas = Image.new('RGBA', (tile_size, tile_size), (255, 255, 255, 255))

    elem_size = 140
    rows, cols = 7, 7
    sx = tile_size / cols
    sy = tile_size / rows
    ci = 0

    for row in range(rows + 1):
        for col in range(cols + 1):
            x = col * sx + (sx / 2 if row % 2 else 0)
            y = row * sy
            x += random.uniform(-5, 5)
            y += random.uniform(-5, 5)

            petal_color = petal_colors[ci % len(petal_colors)]
            center_color = center_colors[ci % len(center_colors)]
            ci += 1
            scale = 1.0 + random.uniform(-0.12, 0.12)
            esz = int(elem_size * scale)

            # Create flower petals
            elem = watercolor_shape(draw_flower5, esz, petal_color)
            # Add center dot in different color
            center_sz = esz // 4
            center = watercolor_shape(draw_circle, center_sz,
                                       center_color, edge_darken=False)
            offset = (esz - center_sz) // 2
            elem.alpha_composite(center, (offset, offset))

            angle = random.uniform(-25, 25)
            elem = elem.rotate(angle, expand=True, resample=Image.BICUBIC)

            px = int(x - elem.width // 2)
            py = int(y - elem.height // 2)
            for wx in [0, -tile_size, tile_size]:
                for wy in [0, -tile_size, tile_size]:
                    nx, ny = px + wx, py + wy
                    if (nx + elem.width > 0 and nx < tile_size and
                            ny + elem.height > 0 and ny < tile_size):
                        canvas.alpha_composite(elem, (nx, ny))
    return canvas


# ===== LEAF PATTERN WITH BERRIES =====

def create_autumn_pattern(tile_size, leaf_colors, berry_colors):
    """Autumn leaves with scattered berries."""
    canvas = Image.new('RGBA', (tile_size, tile_size), (255, 255, 255, 255))

    rows, cols = 8, 8
    sx = tile_size / cols
    sy = tile_size / rows
    ci = 0

    for row in range(rows + 1):
        for col in range(cols + 1):
            x = col * sx + (sx / 2 if row % 2 else 0)
            y = row * sy
            x += random.uniform(-5, 5)
            y += random.uniform(-5, 5)

            ci += 1
            scale = 1.0 + random.uniform(-0.15, 0.15)

            if random.random() < 0.3:
                # Berry cluster
                for _ in range(random.randint(2, 4)):
                    bsz = int(30 * scale)
                    bcolor = berry_colors[random.randint(0, len(berry_colors) - 1)]
                    berry = watercolor_shape(draw_circle, bsz, bcolor, edge_darken=False)
                    bx = int(x + random.uniform(-15, 15) - bsz // 2)
                    by = int(y + random.uniform(-15, 15) - bsz // 2)
                    for wx in [0, -tile_size, tile_size]:
                        for wy in [0, -tile_size, tile_size]:
                            nx, ny = bx + wx, by + wy
                            if (nx + bsz > 0 and nx < tile_size and
                                    ny + bsz > 0 and ny < tile_size):
                                canvas.alpha_composite(berry, (nx, ny))
            else:
                # Leaf
                esz = int(110 * scale)
                color = leaf_colors[ci % len(leaf_colors)]
                elem = watercolor_shape(draw_leaf, esz, color)
                angle = random.uniform(-60, 60)
                elem = elem.rotate(angle, expand=True, resample=Image.BICUBIC)
                px = int(x - elem.width // 2)
                py = int(y - elem.height // 2)
                for wx in [0, -tile_size, tile_size]:
                    for wy in [0, -tile_size, tile_size]:
                        nx, ny = px + wx, py + wy
                        if (nx + elem.width > 0 and nx < tile_size and
                                ny + elem.height > 0 and ny < tile_size):
                            canvas.alpha_composite(elem, (nx, ny))
    return canvas


# ===== GENERIC PATTERN =====

def create_generic_pattern(tile_size, draw_func, colors, elem_size,
                           rows, cols, offset=True, rot=0, scale_var=0,
                           details=None, detail_count=0):
    """Generic grid pattern creator."""
    canvas = Image.new('RGBA', (tile_size, tile_size), (255, 255, 255, 255))
    sx = tile_size / cols
    sy = tile_size / rows
    ci = 0

    for row in range(rows + 1):
        for col in range(cols + 1):
            x = col * sx + (sx / 2 if (offset and row % 2) else 0)
            y = row * sy
            x += random.uniform(-4, 4)
            y += random.uniform(-4, 4)

            color = colors[ci % len(colors)]
            ci += 1
            sc = 1.0 + random.uniform(-scale_var, scale_var)
            esz = int(elem_size * sc)

            elem = watercolor_shape(draw_func, esz, color)
            if details and detail_count > 0:
                elem = add_white_details(elem, esz, details, detail_count)

            if rot > 0:
                angle = random.uniform(-rot, rot)
                elem = elem.rotate(angle, expand=True, resample=Image.BICUBIC)

            px = int(x - elem.width // 2)
            py = int(y - elem.height // 2)
            for wx in [0, -tile_size, tile_size]:
                for wy in [0, -tile_size, tile_size]:
                    nx, ny = px + wx, py + wy
                    if (nx + elem.width > 0 and nx < tile_size and
                            ny + elem.height > 0 and ny < tile_size):
                        canvas.alpha_composite(elem, (nx, ny))
    return canvas


# ===== GENERATE ALL 8 PATTERNS =====

def main():
    patterns = {}

    # 1. Pastel Hearts
    print("1/8: Pastel Watercolor Hearts...")
    p = create_generic_pattern(
        TILE_SIZE, draw_heart,
        colors=[(232, 160, 180), (196, 181, 253), (167, 222, 199),
                (253, 218, 174), (173, 216, 230), (255, 200, 200)],
        elem_size=120, rows=8, cols=8, offset=True,
        rot=15, scale_var=0.1, details='hearts', detail_count=4
    )
    patterns['pastel-hearts-seamless-pattern'] = p

    # 2. Spring Wildflowers
    print("2/8: Spring Wildflowers...")
    p = create_flower_pattern(
        TILE_SIZE,
        petal_colors=[(244, 160, 181), (253, 224, 124), (147, 197, 253),
                      (255, 170, 130), (196, 181, 253), (167, 222, 199)],
        center_colors=[(255, 220, 100), (255, 200, 130), (240, 200, 80),
                       (255, 230, 150), (250, 210, 100), (255, 215, 90)]
    )
    patterns['spring-wildflower-seamless-pattern'] = p

    # 3. Autumn Leaves & Berries
    print("3/8: Autumn Leaves & Berries...")
    p = create_autumn_pattern(
        TILE_SIZE,
        leaf_colors=[(210, 105, 30), (178, 90, 30), (220, 160, 60),
                     (180, 60, 30), (200, 130, 50), (190, 80, 25)],
        berry_colors=[(200, 80, 40), (220, 120, 50), (180, 60, 30)]
    )
    patterns['autumn-leaves-seamless-pattern'] = p

    # 4. Celestial Stars & Moons
    print("4/8: Celestial Stars & Moons...")
    p = create_mixed_celestial(
        TILE_SIZE,
        colors=[(253, 218, 174), (173, 216, 240), (255, 223, 186),
                (196, 181, 253), (255, 236, 179)]
    )
    patterns['celestial-stars-seamless-pattern'] = p

    # 5. Watercolor Butterflies
    print("5/8: Watercolor Butterflies...")
    p = create_generic_pattern(
        TILE_SIZE, draw_butterfly,
        colors=[(173, 216, 240), (244, 170, 200), (200, 190, 255),
                (255, 220, 150), (180, 230, 200)],
        elem_size=130, rows=7, cols=7, offset=True,
        rot=20, scale_var=0.12
    )
    patterns['watercolor-butterfly-seamless-pattern'] = p

    # 6. Lucky Shamrocks
    print("6/8: Lucky Shamrocks...")
    p = create_generic_pattern(
        TILE_SIZE, draw_clover,
        colors=[(76, 175, 80), (104, 195, 100), (56, 142, 60),
                (129, 199, 132), (85, 170, 85)],
        elem_size=110, rows=8, cols=8, offset=True,
        rot=20, scale_var=0.1
    )
    patterns['lucky-shamrock-seamless-pattern'] = p

    # 7. Winter Snowflakes
    print("7/8: Winter Snowflakes...")
    p = create_generic_pattern(
        TILE_SIZE, draw_snowflake,
        colors=[(173, 216, 240), (200, 225, 248), (150, 200, 235),
                (190, 215, 242), (160, 200, 238)],
        elem_size=120, rows=7, cols=7, offset=True,
        rot=30, scale_var=0.15, details='dots', detail_count=3
    )
    patterns['winter-snowflake-seamless-pattern'] = p

    # 8. Pastel Polka Dots
    print("8/8: Pastel Polka Dots...")
    p = create_generic_pattern(
        TILE_SIZE, draw_circle,
        colors=[(232, 160, 180), (173, 216, 230), (196, 181, 253),
                (167, 222, 199), (253, 218, 174), (255, 223, 186)],
        elem_size=100, rows=9, cols=9, offset=True,
        rot=0, scale_var=0.05, details='hearts', detail_count=5
    )
    patterns['pastel-polka-dot-seamless-pattern'] = p

    # Save all
    for name, img in patterns.items():
        # Add watermark
        img_wm = add_watermark(img)
        path = os.path.join(OUTPUT_DIR, f"{name}.png")
        img_wm.convert('RGB').save(path, 'PNG', dpi=(300, 300))
        print(f"  -> {path}")

        # Also save a clean version (no watermark) for the actual product
        clean_path = os.path.join(OUTPUT_DIR, f"{name}-clean.png")
        img.convert('RGB').save(clean_path, 'PNG', dpi=(300, 300))

    print(f"\nDone! {len(patterns)} patterns saved to {OUTPUT_DIR}")


if __name__ == '__main__':
    main()
