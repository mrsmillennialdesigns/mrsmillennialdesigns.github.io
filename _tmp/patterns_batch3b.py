#!/usr/bin/env python3
"""Seamless patterns batch 3b: Affirmations for Kids, Rainbow & Clouds.
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
# 14. AFFIRMATIONS FOR KIDS (modern simplistic style)
# =============================================================================
def draw_text_bubble(layer, cx, cy, text, font, text_color, bg_color, padding=30):
    """Draw text inside a rounded rectangle bubble."""
    d = ImageDraw.Draw(layer)
    ss = layer.size[0]

    # Measure text
    bbox = d.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]

    # Bubble dimensions
    bw = tw + padding * 2
    bh = th + padding * 2
    bx = cx - bw / 2
    by = cy - bh / 2

    # Draw bubble
    d.rounded_rectangle([bx, by, bx+bw, by+bh], radius=bh*0.35,
                        fill=(*bg_color, 255))

    # Draw text centered
    tx = cx - tw / 2
    ty = cy - th / 2
    d.text((tx, ty), text, font=font, fill=(*text_color, 255))


def draw_small_star(d, cx, cy, r, color):
    """Tiny 4-point sparkle."""
    pts = []
    for i in range(8):
        angle = math.pi * i / 4 - math.pi/2
        rr = r if i % 2 == 0 else r * 0.3
        pts.append((cx + rr * math.cos(angle), cy + rr * math.sin(angle)))
    d.polygon(pts, fill=(*color, 255))


def draw_tiny_heart(d, cx, cy, r, color):
    """Tiny heart shape."""
    d.ellipse([cx-r*1.3, cy-r*1.0, cx-r*0.05, cy+r*0.1], fill=(*color, 255))
    d.ellipse([cx+r*0.05, cy-r*1.0, cx+r*1.3, cy+r*0.1], fill=(*color, 255))
    d.polygon([(cx-r*1.25, cy-r*0.15), (cx+r*1.25, cy-r*0.15),
               (cx, cy+r*1.3)], fill=(*color, 255))


def create_affirmations():
    print("  Affirmations for Kids...")
    random.seed(114)
    canvas = Image.new('RGB', (CANVAS, CANVAS), (255, 252, 248))

    affirmations = [
        "I am kind",
        "I am brave",
        "I am loved",
        "I am smart",
        "I am strong",
        "I am enough",
        "I can do it",
        "I am special",
        "I am creative",
        "I am helpful",
        "I believe",
        "I am amazing",
    ]

    bg_colors = [
        (255, 220, 220),  # soft pink
        (220, 235, 255),  # soft blue
        (255, 240, 210),  # soft yellow
        (225, 245, 225),  # soft green
        (240, 225, 255),  # soft purple
        (255, 230, 225),  # soft coral
        (225, 240, 245),  # soft teal
        (245, 235, 220),  # soft tan
    ]

    text_colors = [
        (140, 90, 100),   # muted rose
        (80, 100, 140),   # muted blue
        (130, 110, 70),   # muted gold
        (80, 120, 85),    # muted green
        (110, 85, 130),   # muted purple
        (140, 100, 85),   # muted terracotta
    ]

    accent_colors = [
        (240, 180, 180),  # pink
        (180, 200, 240),  # blue
        (240, 210, 140),  # yellow
        (180, 220, 180),  # green
        (210, 190, 240),  # purple
    ]

    # Try to load a nice font
    font = None
    font_paths = [
        '/System/Library/Fonts/Avenir Next.ttc',
        '/System/Library/Fonts/Helvetica.ttc',
        '/System/Library/Fonts/SFCompact.ttf',
    ]
    for fp in font_paths:
        try:
            font = ImageFont.truetype(fp, 48)
            break
        except:
            continue
    if font is None:
        font = ImageFont.load_default()

    # Place affirmations in a grid
    cols, rows = 4, 5
    sx, sy = CANVAS / cols, CANVAS / rows
    aff_idx = 0

    for row in range(rows):
        for col in range(cols):
            x = col * sx + sx/2 + random.randint(-15, 15)
            y = row * sy + sy/2 + random.randint(-10, 10)
            if row % 2:
                x += sx / 2

            text = affirmations[aff_idx % len(affirmations)]
            aff_idx += 1
            bg = random.choice(bg_colors)
            tc = random.choice(text_colors)

            # Create text bubble on layer
            size = 700  # larger to fit text
            layer = Image.new('RGBA', (size, size), (0, 0, 0, 0))
            draw_text_bubble(layer, size/2, size/2, text, font, tc, bg, padding=40)

            place_seamless(canvas, layer, int(x), int(y), CANVAS)

    # Scatter stars and hearts between text
    for _ in range(35):
        asize = random.randint(40, 70)
        ax = random.randint(0, CANVAS)
        ay = random.randint(0, CANVAS)
        ss2 = asize * 3
        al = Image.new('RGBA', (ss2, ss2), (0, 0, 0, 0))
        ad = ImageDraw.Draw(al)
        ac = random.choice(accent_colors)
        if random.random() < 0.5:
            draw_small_star(ad, ss2/2, ss2/2, ss2*0.3, ac)
        else:
            draw_tiny_heart(ad, ss2/2, ss2/2, ss2*0.18, ac)
        al = al.resize((asize, asize), Image.LANCZOS)
        place_seamless(canvas, al, ax, ay, CANVAS)

    # Small dots
    for _ in range(30):
        ds = random.randint(15, 30)
        dx = random.randint(0, CANVAS)
        dy = random.randint(0, CANVAS)
        dl = Image.new('RGBA', (ds*3, ds*3), (0, 0, 0, 0))
        dd = ImageDraw.Draw(dl)
        dc = random.choice(accent_colors)
        dr = ds * 3 * 0.3
        dd.ellipse([ds*3/2-dr, ds*3/2-dr, ds*3/2+dr, ds*3/2+dr], fill=(*dc, 255))
        dl = dl.resize((ds, ds), Image.LANCZOS)
        place_seamless(canvas, dl, dx, dy, CANVAS)

    return canvas


# =============================================================================
# 15. WATERCOLOR RAINBOW AND CLOUD
# =============================================================================
def draw_cloud(d, cx, cy, ss, color):
    """Fluffy cloud from overlapping circles."""
    bumps = [
        (0, 0, 0.16),
        (-0.12, -0.04, 0.12),
        (0.12, -0.03, 0.13),
        (-0.06, -0.1, 0.10),
        (0.07, -0.09, 0.11),
        (-0.18, 0.02, 0.09),
        (0.19, 0.01, 0.10),
    ]
    for bx, by, br in bumps:
        r = ss * br
        x = cx + ss * bx
        y = cy + ss * by
        d.ellipse([x-r, y-r, x+r, y+r], fill=(*color, 255))


def draw_rainbow(d, cx, cy, ss, rainbow_colors):
    """Half-circle rainbow with multiple colored bands."""
    num_bands = len(rainbow_colors)
    outer_r = ss * 0.30
    band_width = outer_r / (num_bands + 1)

    for i, color in enumerate(rainbow_colors):
        r = outer_r - i * band_width
        r_inner = r - band_width

        # Draw as filled arc using mask approach
        # Since PIL arc with fill isn't great, use two ellipses
        # Outer circle
        d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(*color, 255))

    # Cut out center (background-colored circle) and bottom half
    # Inner circle (to make it a band, not solid)
    inner_r = outer_r - num_bands * band_width
    # We need to draw the bands from outside in, then cut the center
    # Actually let's redraw more carefully

    # Clear and redraw
    # First, draw concentric filled semicircles from outside in
    # We need a mask approach for clean semicircles

    return  # We'll use the mask approach below


def draw_rainbow_mask(layer, cx, cy, ss):
    """Draw a rainbow using mask-based semicircles for clean bands."""
    rainbow_colors = [
        (235, 100, 100),  # red (muted)
        (240, 170, 100),  # orange
        (245, 220, 110),  # yellow
        (130, 200, 130),  # green
        (120, 170, 220),  # blue
        (170, 140, 210),  # indigo
        (200, 160, 220),  # violet
    ]

    num_bands = len(rainbow_colors)
    outer_r = ss * 0.32
    band_width = outer_r * 0.09

    for i, color in enumerate(rainbow_colors):
        r_out = outer_r - i * band_width
        r_in = r_out - band_width

        # Create band using mask
        band_mask = Image.new('L', (ss, ss), 0)
        md = ImageDraw.Draw(band_mask)
        # Outer semicircle (top half)
        md.ellipse([cx-r_out, cy-r_out, cx+r_out, cy+r_out], fill=255)
        # Cut inner circle
        md.ellipse([cx-r_in, cy-r_in, cx+r_in, cy+r_in], fill=0)
        # Cut bottom half
        md.rectangle([0, cy, ss, ss], fill=0)

        color_layer = Image.new('RGBA', (ss, ss), (*color, 255))
        layer.paste(color_layer, mask=band_mask)


def create_rainbow_clouds():
    print("  Rainbow & Clouds...")
    random.seed(115)
    canvas = Image.new('RGB', (CANVAS, CANVAS), (245, 250, 255))

    cloud_colors = [
        (255, 255, 255),  # white
        (245, 248, 255),  # blue-white
        (255, 250, 245),  # warm white
        (250, 245, 255),  # purple-white
    ]

    cols, rows = 5, 5
    sx, sy = CANVAS / cols, CANVAS / rows
    elements = ['rainbow', 'cloud', 'cloud', 'rainbow', 'cloud']

    for row in range(rows):
        for col in range(cols):
            x = col * sx + sx/2 + random.randint(-25, 25)
            y = row * sy + sy/2 + random.randint(-20, 20)
            if row % 2:
                x += sx / 2

            etype = random.choice(elements)
            size = random.randint(420, 520)

            ss = size * 3
            layer = Image.new('RGBA', (ss, ss), (0, 0, 0, 0))
            d = ImageDraw.Draw(layer)

            if etype == 'rainbow':
                # Rainbow with cloud base
                draw_rainbow_mask(layer, ss/2, ss/2 + ss*0.05, ss)
                # Cloud at the base of rainbow
                d2 = ImageDraw.Draw(layer)
                cc = random.choice(cloud_colors)
                # Left cloud base
                cloud_y = ss/2 + ss*0.05
                for side in [-1, 1]:
                    cloud_cx = ss/2 + side * ss * 0.22
                    draw_cloud(d2, cloud_cx, cloud_y, ss*0.5, cc)
            else:
                # Just a fluffy cloud
                cc = random.choice(cloud_colors)
                draw_cloud(d, ss/2, ss/2, ss, cc)
                # Add subtle shadow
                shadow_color = (230, 235, 240)
                d.ellipse([ss/2-ss*0.15, ss/2+ss*0.04, ss/2+ss*0.15, ss/2+ss*0.14],
                          fill=(*shadow_color, 255))

            layer = layer.resize((size, size), Image.LANCZOS)
            place_seamless(canvas, layer, x, y, CANVAS)

    # Scatter tiny stars
    star_colors = [(245, 215, 100), (240, 190, 180), (190, 210, 240), (210, 195, 235)]
    for _ in range(30):
        ssize = random.randint(30, 60)
        sx2 = random.randint(0, CANVAS)
        sy2 = random.randint(0, CANVAS)
        ss2 = ssize * 3
        sl = Image.new('RGBA', (ss2, ss2), (0, 0, 0, 0))
        sd = ImageDraw.Draw(sl)
        sc = random.choice(star_colors)
        r_out = ss2 * 0.3
        r_in = r_out * 0.35
        pts = []
        rot = random.uniform(0, math.pi/4)
        for i in range(8):
            angle = math.pi * i / 4 - math.pi/2 + rot
            r = r_out if i % 2 == 0 else r_in
            pts.append((ss2/2 + r * math.cos(angle), ss2/2 + r * math.sin(angle)))
        sd.polygon(pts, fill=(*sc, 255))
        sl = sl.resize((ssize, ssize), Image.LANCZOS)
        place_seamless(canvas, sl, sx2, sy2, CANVAS)

    # Scatter small raindrops
    for _ in range(20):
        rsize = random.randint(20, 40)
        rx = random.randint(0, CANVAS)
        ry = random.randint(0, CANVAS)
        rl = Image.new('RGBA', (rsize*3, rsize*3), (0, 0, 0, 0))
        rd = ImageDraw.Draw(rl)
        rc = (180, 210, 235)
        r2 = rsize * 3
        # Teardrop: circle + triangle
        dr = r2 * 0.2
        rd.ellipse([r2/2-dr, r2/2, r2/2+dr, r2/2+dr*2], fill=(*rc, 255))
        rd.polygon([(r2/2-dr, r2/2+dr*0.5), (r2/2, r2/2-dr*1.5),
                    (r2/2+dr, r2/2+dr*0.5)], fill=(*rc, 255))
        rl = rl.resize((rsize, rsize), Image.LANCZOS)
        place_seamless(canvas, rl, rx, ry, CANVAS)

    return canvas


# =============================================================================
# MAIN
# =============================================================================
def main():
    patterns = [
        ('8800000024', 'Affirmations for Kids', create_affirmations),
        ('8800000025', 'Rainbow & Clouds', create_rainbow_clouds),
    ]
    for lid, name, builder in patterns:
        print(f"[{lid}] {name}")
        pat = builder()
        create_product_images(lid, pat)
    print("\nBatch 3b done! All 15 patterns complete!")


if __name__ == '__main__':
    main()
