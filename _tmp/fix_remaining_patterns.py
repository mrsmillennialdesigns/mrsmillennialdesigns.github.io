#!/usr/bin/env python3
"""Fix remaining 4 patterns — full opacity, solid fills, crisp edges."""

from PIL import Image, ImageDraw, ImageFont
import math
import random
import os

CANVAS = 3600
IMG_DIR = '/Users/alexhosage/Desktop/mmd-website/img'
PATTERNS_DIR = os.path.join(IMG_DIR, 'patterns')

random.seed(42)


def place_seamless(canvas, element, x, y, cs):
    ew, eh = element.size
    px, py = int(x - ew/2), int(y - eh/2)
    for ox in [-cs, 0, cs]:
        for oy in [-cs, 0, cs]:
            nx, ny = px + ox, py + oy
            if nx + ew > 0 and nx < cs and ny + eh > 0 and ny < cs:
                canvas.paste(element, (nx, ny), element)


def create_wildflower():
    """Crisp flowers — solid fills, no transparency."""
    print("  Wildflower...")
    canvas = Image.new('RGB', (CANVAS, CANVAS), (255, 253, 250))

    colors = [
        (240, 150, 170),  # pink
        (250, 200, 100),  # yellow
        (170, 180, 240),  # blue
        (230, 140, 120),  # coral
        (200, 170, 230),  # lavender
    ]

    cols, rows = 8, 8
    sx, sy = CANVAS / cols, CANVAS / rows

    for row in range(rows):
        for col in range(cols):
            x = col * sx + sx/2 + random.randint(-40, 40)
            y = row * sy + sy/2 + random.randint(-40, 40)
            if row % 2:
                x += sx / 2

            color = random.choice(colors)
            size = random.randint(300, 420)
            num_petals = random.choice([5, 6, 7])
            rotation = random.uniform(0, 2 * math.pi / num_petals)

            # Draw at 2x for anti-aliasing then downscale
            ss = size * 3
            layer = Image.new('RGBA', (ss, ss), (0, 0, 0, 0))
            d = ImageDraw.Draw(layer)
            cx, cy = ss/2, ss/2
            petal_r = ss * 0.38

            # Draw petals as ellipses (PIL built-in = crisp)
            for i in range(num_petals):
                angle = rotation + 2 * math.pi * i / num_petals
                # Petal center point
                pc_x = cx + petal_r * 0.5 * math.cos(angle)
                pc_y = cy + petal_r * 0.5 * math.sin(angle)
                pw = petal_r * 0.38
                ph = petal_r * 0.7

                # Create rotated petal using a separate layer
                petal_layer = Image.new('RGBA', (ss, ss), (0, 0, 0, 0))
                pd = ImageDraw.Draw(petal_layer)
                # Draw ellipse centered
                pd.ellipse([ss/2 - pw, ss/2 - ph, ss/2 + pw, ss/2 + ph],
                           fill=(*color, 255))
                # Rotate to correct angle
                petal_layer = petal_layer.rotate(-math.degrees(angle) - 90,
                                                 resample=Image.BICUBIC, center=(ss/2, ss/2))
                # Shift to petal position
                offset_x = int(pc_x - ss/2)
                offset_y = int(pc_y - ss/2)
                shifted = Image.new('RGBA', (ss, ss), (0, 0, 0, 0))
                shifted.paste(petal_layer, (offset_x, offset_y), petal_layer)
                layer = Image.alpha_composite(layer, shifted)

            # Golden center — solid, using ellipse
            d2 = ImageDraw.Draw(layer)
            cr = petal_r * 0.18
            d2.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=(230, 190, 80, 255))
            # Center highlight
            hr = cr * 0.45
            d2.ellipse([cx - hr - cr*0.12, cy - hr - cr*0.12,
                        cx + hr - cr*0.12, cy + hr - cr*0.12], fill=(250, 220, 130, 255))

            layer = layer.resize((size, size), Image.LANCZOS)
            place_seamless(canvas, layer, x, y, CANVAS)

    return canvas


def create_celestial():
    """Crisp stars & moons — solid fills."""
    print("  Celestial...")
    canvas = Image.new('RGB', (CANVAS, CANVAS), (248, 248, 255))

    star_colors = [
        (225, 185, 75),   # warm gold
        (170, 195, 235),  # baby blue
        (235, 185, 165),  # peach
        (195, 175, 225),  # lavender
    ]
    moon_colors = [
        (225, 190, 85),   # gold
        (185, 175, 225),  # lavender
        (175, 205, 235),  # blue
    ]

    cols, rows = 11, 11
    sx, sy = CANVAS / cols, CANVAS / rows

    for row in range(rows):
        for col in range(cols):
            x = col * sx + sx/2 + random.randint(-25, 25)
            y = row * sy + sy/2 + random.randint(-25, 25)
            if row % 2:
                x += sx / 2

            if random.random() < 0.75:
                # Star — draw at 3x, solid fill
                color = random.choice(star_colors)
                size = random.randint(200, 300)
                n_pts = random.choice([4, 5, 6])
                rotation = random.uniform(0, math.pi / 5)

                ss = size * 3
                layer = Image.new('RGBA', (ss, ss), (0, 0, 0, 0))
                d = ImageDraw.Draw(layer)
                cx, cy = ss/2, ss/2
                outer = ss * 0.4
                inner = outer * (0.38 if n_pts == 5 else 0.45)

                pts = []
                for i in range(n_pts * 2):
                    angle = math.pi * i / n_pts - math.pi/2 + rotation
                    r = outer if i % 2 == 0 else inner
                    pts.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
                d.polygon(pts, fill=(*color, 255))

                layer = layer.resize((size, size), Image.LANCZOS)
                place_seamless(canvas, layer, x, y, CANVAS)
            else:
                # Moon — use two overlapping ellipses for crisp crescent
                color = random.choice(moon_colors)
                size = random.randint(220, 320)
                rotation = random.uniform(-25, 25)

                ss = size * 3
                layer = Image.new('RGBA', (ss, ss), (0, 0, 0, 0))
                d = ImageDraw.Draw(layer)
                cx, cy = ss/2, ss/2
                r = ss * 0.38

                # Outer circle (the moon)
                d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*color, 255))
                # Inner circle (cut out) — slightly offset
                cut_r = r * 0.85
                cut_offset = r * 0.35
                d.ellipse([cx + cut_offset - cut_r, cy - cut_r,
                           cx + cut_offset + cut_r, cy + cut_r], fill=(0, 0, 0, 0))

                # The cut-out leaves transparent pixels, but alpha_composite
                # doesn't work that way with solid. Use a mask approach instead.
                # Redraw properly:
                layer = Image.new('RGBA', (ss, ss), (0, 0, 0, 0))
                # Draw moon as difference of two circles
                moon_mask = Image.new('L', (ss, ss), 0)
                md = ImageDraw.Draw(moon_mask)
                md.ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
                md.ellipse([cx + cut_offset - cut_r, cy - cut_r,
                            cx + cut_offset + cut_r, cy + cut_r], fill=0)
                # Apply color through mask
                color_layer = Image.new('RGBA', (ss, ss), (*color, 255))
                layer.paste(color_layer, mask=moon_mask)

                layer = layer.rotate(rotation, resample=Image.BICUBIC, expand=False)
                layer = layer.resize((size, size), Image.LANCZOS)
                place_seamless(canvas, layer, x, y, CANVAS)

    return canvas


def create_butterfly():
    """Crisp butterflies — solid fills, clean wing shapes."""
    print("  Butterfly...")
    canvas = Image.new('RGB', (CANVAS, CANVAS), (252, 252, 255))

    wing_colors = [
        (160, 205, 240),  # sky blue
        (235, 170, 190),  # pink
        (195, 175, 230),  # lilac
        (225, 195, 115),  # golden
        (165, 215, 190),  # mint
    ]

    cols, rows = 8, 8
    sx, sy = CANVAS / cols, CANVAS / rows

    for row in range(rows):
        for col in range(cols):
            x = col * sx + sx/2 + random.randint(-40, 40)
            y = row * sy + sy/2 + random.randint(-40, 40)
            if row % 2:
                x += sx / 2

            color = random.choice(wing_colors)
            size = random.randint(320, 440)
            rotation = random.uniform(-25, 25)

            ss = size * 3
            layer = Image.new('RGBA', (ss, ss), (0, 0, 0, 0))
            d = ImageDraw.Draw(layer)
            cx, cy = ss/2, ss/2

            # Upper wings — ellipses rotated to form wing shapes
            uw = ss * 0.28
            uh = ss * 0.22
            for side in [-1, 1]:
                wing = Image.new('RGBA', (ss, ss), (0, 0, 0, 0))
                wd = ImageDraw.Draw(wing)
                wd.ellipse([cx - uw, cy - uh, cx + uw, cy + uh], fill=(*color, 255))
                # Rotate wing outward and up
                wing = wing.rotate(side * 35, resample=Image.BICUBIC, center=(cx, cy))
                # Shift up and to side
                shifted = Image.new('RGBA', (ss, ss), (0, 0, 0, 0))
                off_x = int(side * uw * 0.35)
                off_y = int(-uh * 0.45)
                shifted.paste(wing, (off_x, off_y), wing)
                layer = Image.alpha_composite(layer, shifted)

            # Lower wings — smaller ellipses
            lw = ss * 0.18
            lh = ss * 0.14
            for side in [-1, 1]:
                wing = Image.new('RGBA', (ss, ss), (0, 0, 0, 0))
                wd = ImageDraw.Draw(wing)
                darker = tuple(max(0, c - 25) for c in color)
                wd.ellipse([cx - lw, cy - lh, cx + lw, cy + lh], fill=(*darker, 255))
                wing = wing.rotate(side * 25, resample=Image.BICUBIC, center=(cx, cy))
                shifted = Image.new('RGBA', (ss, ss), (0, 0, 0, 0))
                off_x = int(side * lw * 0.5)
                off_y = int(lh * 0.6)
                shifted.paste(wing, (off_x, off_y), wing)
                layer = Image.alpha_composite(layer, shifted)

            # Wing spots (lighter circles on upper wings)
            d2 = ImageDraw.Draw(layer)
            lighter = tuple(min(255, c + 45) for c in color)
            spot_r = uw * 0.22
            for side in [-1, 1]:
                spot_x = cx + side * uw * 0.55
                spot_y = cy - uh * 0.35
                d2.ellipse([spot_x - spot_r, spot_y - spot_r,
                            spot_x + spot_r, spot_y + spot_r], fill=(*lighter, 255))

            # Body — solid ellipse
            body_w = ss * 0.022
            body_h = ss * 0.18
            d2.ellipse([cx - body_w, cy - body_h, cx + body_w, cy + body_h],
                       fill=(55, 45, 35, 255))

            # Antennae
            for side in [-1, 1]:
                tip_x = cx + side * ss * 0.06
                tip_y = cy - body_h - ss * 0.08
                d2.line([(cx, cy - body_h), (tip_x, tip_y)],
                        fill=(55, 45, 35, 255), width=max(3, ss // 180))
                dot_r = ss * 0.012
                d2.ellipse([tip_x - dot_r, tip_y - dot_r, tip_x + dot_r, tip_y + dot_r],
                           fill=(55, 45, 35, 255))

            layer = layer.rotate(rotation, resample=Image.BICUBIC, expand=False)
            layer = layer.resize((size, size), Image.LANCZOS)
            place_seamless(canvas, layer, x, y, CANVAS)

    return canvas


def create_polkadot():
    """Crisp hearts polka dot — full opacity, clean edges."""
    print("  Polka Dot (hearts)...")
    canvas = Image.new('RGB', (CANVAS, CANVAS), (255, 255, 255))

    colors = [
        (235, 150, 175),  # pink
        (170, 200, 235),  # blue
        (195, 170, 225),  # purple
        (225, 185, 125),  # gold
        (160, 210, 190),  # mint
    ]

    elem_size = 170
    cols, rows = 14, 18
    sx, sy = CANVAS / cols, CANVAS / rows

    color_idx = 0
    for row in range(rows):
        for col in range(cols):
            color = colors[color_idx % len(colors)]
            color_idx += 1

            x = col * sx + sx/2
            y = row * sy + sy/2
            if row % 2:
                x += sx / 2

            # Heart from two circles + triangle — PIL built-ins only
            ss = elem_size * 3
            layer = Image.new('RGBA', (ss, ss), (0, 0, 0, 0))
            d = ImageDraw.Draw(layer)
            cx, cy = ss/2, ss/2

            hr = ss * 0.2  # circle radius for heart lobes
            # Two circles for top of heart
            d.ellipse([cx - hr*1.7, cy - hr*1.5, cx - hr*0.05, cy + hr*0.2],
                      fill=(*color, 255))
            d.ellipse([cx + hr*0.05, cy - hr*1.5, cx + hr*1.7, cy + hr*0.2],
                      fill=(*color, 255))
            # Triangle for bottom point
            d.polygon([(cx - hr*1.65, cy - hr*0.3),
                       (cx + hr*1.65, cy - hr*0.3),
                       (cx, cy + hr*1.8)],
                      fill=(*color, 255))

            # White sparkle dot
            sparkle_r = hr * 0.22
            d.ellipse([cx - hr*0.6 - sparkle_r, cy - hr*0.8 - sparkle_r,
                        cx - hr*0.6 + sparkle_r, cy - hr*0.8 + sparkle_r],
                       fill=(255, 255, 255, 255))

            layer = layer.resize((elem_size, elem_size), Image.LANCZOS)
            place_seamless(canvas, layer, x, y, CANVAS)

    return canvas


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
    print(f"    {lid} — all 3 images done")


def main():
    os.makedirs(PATTERNS_DIR, exist_ok=True)
    patterns = [
        ('8800000002', 'Spring Wildflower', create_wildflower),
        ('8800000004', 'Celestial Stars & Moons', create_celestial),
        ('8800000005', 'Watercolor Butterfly', create_butterfly),
        ('8800000008', 'Pastel Polka Dot', create_polkadot),
    ]
    for lid, name, builder in patterns:
        print(f"[{lid}] {name}")
        pat = builder()
        create_product_images(lid, pat)
    print("\nDone!")


if __name__ == '__main__':
    main()
