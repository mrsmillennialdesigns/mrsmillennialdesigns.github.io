#!/usr/bin/env python3
"""
V3 Pattern Generator — High-Resolution, Crisp Seamless Patterns
3600x3600 (300 DPI at 12x12"), clean anti-aliased shapes, true seamless tiling.
"""

from PIL import Image, ImageDraw, ImageFilter, ImageChops
import math
import random
import os
import numpy as np

CANVAS = 3600  # 300 DPI × 12 inches
PATTERNS_DIR = '/Users/alexhosage/Desktop/mmd-website/img/patterns'
IMG_DIR = '/Users/alexhosage/Desktop/mmd-website/img'

random.seed(42)
np.random.seed(42)

# ─── Shape Drawing Helpers ────────────────────────────────────────────

def draw_shape_on_layer(size, draw_func, color, supersample=2):
    """Draw a shape on a transparent RGBA layer with supersampling for AA."""
    ss = size * supersample
    layer = Image.new('RGBA', (ss, ss), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    draw_func(draw, ss, color)
    # Downscale with LANCZOS for smooth anti-aliasing
    layer = layer.resize((size, size), Image.LANCZOS)
    return layer


def heart_points(cx, cy, r, num_pts=200):
    """Mathematical heart curve."""
    pts = []
    for i in range(num_pts):
        t = 2 * math.pi * i / num_pts
        x = r * 16 * math.sin(t)**3 / 16
        y = -r * (13*math.cos(t) - 5*math.cos(2*t) - 2*math.cos(3*t) - math.cos(4*t)) / 16
        pts.append((cx + x, cy + y))
    return pts


def star_points(cx, cy, outer_r, inner_r, n=5):
    """Generate star polygon points."""
    pts = []
    for i in range(n * 2):
        angle = math.pi * i / n - math.pi / 2
        r = outer_r if i % 2 == 0 else inner_r
        pts.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    return pts


def crescent_points(cx, cy, r, thickness=0.35, num_pts=100):
    """Generate crescent moon points."""
    pts = []
    # Outer arc
    for i in range(num_pts):
        a = -math.pi/2 + math.pi * i / (num_pts - 1)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    # Inner arc (offset circle)
    offset = r * thickness
    inner_r = r * 0.92
    for i in range(num_pts - 1, -1, -1):
        a = -math.pi/2 + math.pi * i / (num_pts - 1)
        pts.append((cx + offset + inner_r * math.cos(a), cy + inner_r * math.sin(a)))
    return pts


def leaf_points(cx, cy, length, width, angle=0, num_pts=60):
    """Generate leaf shape points."""
    pts = []
    for i in range(num_pts):
        t = i / (num_pts - 1)  # 0 to 1
        # Leaf profile: narrow at ends, wide in middle
        x = length * (t - 0.5)
        y = width * math.sin(math.pi * t) * (0.5 + 0.5 * math.sin(math.pi * t))
        pts.append((x, y))
    # Bottom half
    for i in range(num_pts - 1, -1, -1):
        t = i / (num_pts - 1)
        x = length * (t - 0.5)
        y = -width * math.sin(math.pi * t) * (0.5 + 0.5 * math.sin(math.pi * t))
        pts.append((x, y))
    # Rotate and translate
    cos_a, sin_a = math.cos(angle), math.sin(angle)
    rotated = [(cx + x * cos_a - y * sin_a, cy + x * sin_a + y * cos_a) for x, y in pts]
    return rotated


def flower_petal_points(cx, cy, petal_r, num_petals=5, petal_width=0.6):
    """Generate a multi-petal flower as a list of petal polygons."""
    petals = []
    for i in range(num_petals):
        angle = 2 * math.pi * i / num_petals - math.pi / 2
        tip_x = cx + petal_r * math.cos(angle)
        tip_y = cy + petal_r * math.sin(angle)
        perp = angle + math.pi / 2
        half_w = petal_r * petal_width * 0.4
        base_dist = petal_r * 0.2
        base_x = cx + base_dist * math.cos(angle)
        base_y = cy + base_dist * math.sin(angle)
        pts = [
            (base_x + half_w * math.cos(perp), base_y + half_w * math.sin(perp)),
            (tip_x, tip_y),
            (base_x - half_w * math.cos(perp), base_y - half_w * math.sin(perp)),
        ]
        petals.append(pts)
    return petals


def clover_heart(draw, cx, cy, r, angle, color):
    """Draw a single clover leaf (heart-shaped) at given angle."""
    # Heart shape rotated to point outward from center
    pts = heart_points(cx, cy, r, 120)
    cos_a, sin_a = math.cos(angle), math.sin(angle)
    rotated = []
    for px, py in pts:
        dx, dy = px - cx, py - cy
        rotated.append((cx + dx * cos_a - dy * sin_a, cy + dx * sin_a + dy * cos_a))
    draw.polygon(rotated, fill=color)


# ─── Seamless Placement Helper ────────────────────────────────────────

def place_seamless(canvas, element, x, y, canvas_size):
    """Place an element on canvas with seamless edge wrapping."""
    ew, eh = element.size
    # Center the element at (x, y)
    px, py = int(x - ew/2), int(y - eh/2)

    # Place at all wrapped positions
    for ox in [-canvas_size, 0, canvas_size]:
        for oy in [-canvas_size, 0, canvas_size]:
            nx, ny = px + ox, py + oy
            # Check if this placement overlaps the canvas
            if nx + ew > 0 and nx < canvas_size and ny + eh > 0 and ny < canvas_size:
                canvas.paste(element, (nx, ny), element)


# ─── Individual Pattern Builders ──────────────────────────────────────

def create_hearts_pattern():
    """Pastel Watercolor Hearts — crisp, seamless."""
    print("  Creating Hearts pattern...")
    canvas = Image.new('RGB', (CANVAS, CANVAS), (255, 255, 255))

    colors = [
        (242, 170, 190, 220),  # pink
        (190, 170, 230, 220),  # lavender
        (170, 220, 195, 220),  # mint
        (250, 200, 170, 220),  # peach
        (175, 210, 240, 220),  # baby blue
        (245, 190, 210, 220),  # rose
        (200, 185, 240, 220),  # lilac
    ]

    elem_size = 240  # size of each heart element
    cols, rows = 12, 12
    spacing_x = CANVAS / cols
    spacing_y = CANVAS / rows

    for row in range(rows):
        for col in range(cols):
            color = random.choice(colors)
            size = elem_size + random.randint(-30, 30)
            rotation = random.uniform(-0.25, 0.25)

            x = col * spacing_x + spacing_x / 2 + random.randint(-30, 30)
            y = row * spacing_y + spacing_y / 2 + random.randint(-30, 30)
            # Offset every other row
            if row % 2:
                x += spacing_x / 2

            # Create heart element
            ss = size * 2
            layer = Image.new('RGBA', (ss, ss), (0, 0, 0, 0))
            d = ImageDraw.Draw(layer)
            pts = heart_points(ss/2, ss/2 + ss*0.05, ss * 0.38, 200)
            d.polygon(pts, fill=color)

            # Add subtle inner highlight
            highlight = (*color[:3], 60)
            inner_pts = heart_points(ss/2 - ss*0.02, ss/2 + ss*0.02, ss * 0.25, 200)
            d.polygon(inner_pts, fill=highlight)

            # Rotate
            layer = layer.rotate(math.degrees(rotation), resample=Image.BICUBIC, expand=False)
            # Downscale for AA
            layer = layer.resize((size, size), Image.LANCZOS)

            place_seamless(canvas, layer, x, y, CANVAS)

    return canvas


def create_wildflower_pattern():
    """Spring Wildflower — crisp flowers with golden centers."""
    print("  Creating Wildflower pattern...")
    canvas = Image.new('RGB', (CANVAS, CANVAS), (255, 253, 250))

    petal_colors = [
        (240, 150, 170),   # pink
        (250, 200, 100),   # yellow
        (170, 180, 240),   # blue
        (230, 140, 120),   # coral
        (200, 170, 230),   # lavender
    ]

    cols, rows = 8, 8
    spacing_x = CANVAS / cols
    spacing_y = CANVAS / rows

    for row in range(rows):
        for col in range(cols):
            x = col * spacing_x + spacing_x / 2 + random.randint(-40, 40)
            y = row * spacing_y + spacing_y / 2 + random.randint(-40, 40)
            if row % 2:
                x += spacing_x / 2

            petal_color = random.choice(petal_colors)
            flower_size = random.randint(280, 400)
            num_petals = random.choice([5, 6, 7])
            rotation = random.uniform(0, 2 * math.pi / num_petals)

            ss = flower_size * 2
            layer = Image.new('RGBA', (ss, ss), (0, 0, 0, 0))
            d = ImageDraw.Draw(layer)

            cx, cy = ss/2, ss/2
            petal_r = ss * 0.38

            # Draw petals
            for i in range(num_petals):
                angle = rotation + 2 * math.pi * i / num_petals
                tip_x = cx + petal_r * math.cos(angle)
                tip_y = cy + petal_r * math.sin(angle)
                perp = angle + math.pi / 2
                half_w = petal_r * 0.3
                base_dist = petal_r * 0.15
                base_x = cx + base_dist * math.cos(angle)
                base_y = cy + base_dist * math.sin(angle)

                # Rounded petal using ellipse-ish polygon
                pts = []
                for t_i in range(30):
                    t = t_i / 29
                    # Bezier-like curve from base to tip and back
                    if t < 0.5:
                        t2 = t * 2
                        px = base_x + half_w * math.cos(perp) + (tip_x - base_x - half_w * math.cos(perp)) * t2
                        py = base_y + half_w * math.sin(perp) + (tip_y - base_y - half_w * math.sin(perp)) * t2
                        # Bulge outward
                        bulge = math.sin(math.pi * t2) * half_w * 0.5
                        px += bulge * math.cos(perp)
                        py += bulge * math.sin(perp)
                    else:
                        t2 = (t - 0.5) * 2
                        px = tip_x + (base_x - half_w * math.cos(perp) - tip_x) * t2
                        py = tip_y + (base_y - half_w * math.sin(perp) - tip_y) * t2
                        bulge = math.sin(math.pi * t2) * half_w * 0.5
                        px -= bulge * math.cos(perp)
                        py -= bulge * math.sin(perp)
                    pts.append((px, py))

                alpha = 210 + random.randint(-10, 10)
                d.polygon(pts, fill=(*petal_color, alpha))

            # Golden center
            center_r = petal_r * 0.2
            d.ellipse([cx - center_r, cy - center_r, cx + center_r, cy + center_r],
                      fill=(230, 190, 80, 240))
            # Center highlight
            hr = center_r * 0.5
            d.ellipse([cx - hr - center_r*0.15, cy - hr - center_r*0.15,
                       cx + hr - center_r*0.15, cy + hr - center_r*0.15],
                      fill=(250, 220, 130, 150))

            layer = layer.resize((flower_size, flower_size), Image.LANCZOS)
            place_seamless(canvas, layer, x, y, CANVAS)

    return canvas


def create_autumn_pattern():
    """Autumn Leaves & Berries — clean maple/oak leaves + berry clusters."""
    print("  Creating Autumn Leaves pattern...")
    canvas = Image.new('RGB', (CANVAS, CANVAS), (255, 252, 248))

    leaf_colors = [
        (200, 80, 50),    # burnt orange
        (180, 60, 40),    # rust
        (220, 160, 50),   # gold
        (190, 130, 50),   # amber
        (160, 50, 35),    # deep red
        (200, 140, 70),   # tan
    ]
    berry_color = (160, 40, 50, 230)

    cols, rows = 9, 9
    spacing_x = CANVAS / cols
    spacing_y = CANVAS / rows

    for row in range(rows):
        for col in range(cols):
            x = col * spacing_x + spacing_x / 2 + random.randint(-35, 35)
            y = row * spacing_y + spacing_y / 2 + random.randint(-35, 35)
            if row % 2:
                x += spacing_x / 2

            # Alternate between leaves and berry clusters
            if random.random() < 0.7:
                # Maple leaf
                color = random.choice(leaf_colors)
                size = random.randint(250, 380)
                angle = random.uniform(0, 2 * math.pi)

                ss = size * 2
                layer = Image.new('RGBA', (ss, ss), (0, 0, 0, 0))
                d = ImageDraw.Draw(layer)
                cx, cy = ss/2, ss/2
                r = ss * 0.35

                # 5-pointed maple leaf
                alpha = 210 + random.randint(-10, 10)
                for lobe in range(5):
                    lobe_angle = 2 * math.pi * lobe / 5 - math.pi / 2
                    lobe_r = r * (1.0 if lobe % 2 == 0 else 0.65)
                    tip_x = cx + lobe_r * math.cos(lobe_angle)
                    tip_y = cy + lobe_r * math.sin(lobe_angle)

                    spread = 0.22 if lobe % 2 == 0 else 0.3
                    left_a = lobe_angle - spread
                    right_a = lobe_angle + spread
                    base_r = r * 0.2

                    pts = [
                        (cx + base_r * math.cos(left_a), cy + base_r * math.sin(left_a)),
                        (cx + lobe_r * 0.55 * math.cos(left_a), cy + lobe_r * 0.55 * math.sin(left_a)),
                        (tip_x, tip_y),
                        (cx + lobe_r * 0.55 * math.cos(right_a), cy + lobe_r * 0.55 * math.sin(right_a)),
                        (cx + base_r * math.cos(right_a), cy + base_r * math.sin(right_a)),
                    ]
                    d.polygon(pts, fill=(*color, alpha))

                # Center fill
                d.ellipse([cx - r*0.22, cy - r*0.22, cx + r*0.22, cy + r*0.22],
                          fill=(*color, alpha))

                # Stem
                stem_end_x = cx + r * 0.5 * math.cos(math.pi/2)
                stem_end_y = cy + r * 0.5 * math.sin(math.pi/2)
                d.line([(cx, cy), (stem_end_x, stem_end_y)],
                       fill=(120, 80, 40, 200), width=max(3, ss//80))

                layer = layer.rotate(math.degrees(angle), resample=Image.BICUBIC, expand=False)
                layer = layer.resize((size, size), Image.LANCZOS)
                place_seamless(canvas, layer, x, y, CANVAS)
            else:
                # Berry cluster
                size = random.randint(120, 180)
                ss = size * 2
                layer = Image.new('RGBA', (ss, ss), (0, 0, 0, 0))
                d = ImageDraw.Draw(layer)
                cx, cy = ss/2, ss/2

                for _ in range(random.randint(4, 7)):
                    bx = cx + random.randint(-ss//5, ss//5)
                    by = cy + random.randint(-ss//5, ss//5)
                    br = random.randint(ss//10, ss//7)
                    d.ellipse([bx-br, by-br, bx+br, by+br], fill=berry_color)
                    # Highlight
                    hr = br * 0.3
                    d.ellipse([bx-hr-br*0.2, by-hr-br*0.2, bx+hr-br*0.2, by+hr-br*0.2],
                              fill=(220, 100, 100, 150))

                layer = layer.resize((size, size), Image.LANCZOS)
                place_seamless(canvas, layer, x, y, CANVAS)

    return canvas


def create_celestial_pattern():
    """Celestial Stars & Moons — BEST pattern, just needs crispness."""
    print("  Creating Celestial pattern...")
    canvas = Image.new('RGB', (CANVAS, CANVAS), (248, 248, 255))

    star_colors = [
        (230, 190, 80, 225),   # warm gold
        (180, 200, 240, 225),  # baby blue
        (240, 190, 170, 225),  # peach
        (200, 180, 230, 225),  # lavender
    ]
    moon_colors = [
        (230, 195, 90, 225),   # gold
        (190, 180, 230, 225),  # lavender
        (180, 210, 240, 225),  # blue
    ]

    cols, rows = 11, 11
    spacing_x = CANVAS / cols
    spacing_y = CANVAS / rows

    for row in range(rows):
        for col in range(cols):
            x = col * spacing_x + spacing_x / 2 + random.randint(-25, 25)
            y = row * spacing_y + spacing_y / 2 + random.randint(-25, 25)
            if row % 2:
                x += spacing_x / 2

            if random.random() < 0.75:
                # Star
                color = random.choice(star_colors)
                size = random.randint(180, 280)
                rotation = random.uniform(0, math.pi / 5)
                n_points = random.choice([4, 5, 6])

                ss = size * 2
                layer = Image.new('RGBA', (ss, ss), (0, 0, 0, 0))
                d = ImageDraw.Draw(layer)
                cx, cy = ss/2, ss/2
                outer = ss * 0.4
                inner = outer * (0.38 if n_points == 5 else 0.45)

                pts = star_points(cx, cy, outer, inner, n_points)
                # Rotate
                cos_r, sin_r = math.cos(rotation), math.sin(rotation)
                pts = [(cx + (px-cx)*cos_r - (py-cy)*sin_r,
                        cy + (px-cx)*sin_r + (py-cy)*cos_r) for px, py in pts]
                d.polygon(pts, fill=color)

                # Inner glow
                inner_pts = star_points(cx, cy, outer * 0.55, inner * 0.55, n_points)
                inner_pts = [(cx + (px-cx)*cos_r - (py-cy)*sin_r,
                              cy + (px-cx)*sin_r + (py-cy)*cos_r) for px, py in inner_pts]
                d.polygon(inner_pts, fill=(*color[:3], 80))

                layer = layer.resize((size, size), Image.LANCZOS)
                place_seamless(canvas, layer, x, y, CANVAS)
            else:
                # Crescent moon
                color = random.choice(moon_colors)
                size = random.randint(200, 300)
                rotation = random.uniform(-0.4, 0.4)

                ss = size * 2
                layer = Image.new('RGBA', (ss, ss), (0, 0, 0, 0))
                d = ImageDraw.Draw(layer)
                cx, cy = ss/2, ss/2
                r = ss * 0.38

                pts = crescent_points(cx, cy, r, 0.4)
                d.polygon(pts, fill=color)

                layer = layer.rotate(math.degrees(rotation), resample=Image.BICUBIC, expand=False)
                layer = layer.resize((size, size), Image.LANCZOS)
                place_seamless(canvas, layer, x, y, CANVAS)

    return canvas


def create_butterfly_pattern():
    """Watercolor Butterfly — clean, detailed butterflies."""
    print("  Creating Butterfly pattern...")
    canvas = Image.new('RGB', (CANVAS, CANVAS), (252, 252, 255))

    wing_colors = [
        (170, 210, 245),  # sky blue
        (240, 175, 195),  # pink
        (200, 180, 235),  # lilac
        (230, 200, 120),  # golden
        (175, 220, 195),  # mint
    ]

    cols, rows = 8, 8
    spacing_x = CANVAS / cols
    spacing_y = CANVAS / rows

    for row in range(rows):
        for col in range(cols):
            x = col * spacing_x + spacing_x / 2 + random.randint(-40, 40)
            y = row * spacing_y + spacing_y / 2 + random.randint(-40, 40)
            if row % 2:
                x += spacing_x / 2

            color = random.choice(wing_colors)
            size = random.randint(300, 420)
            rotation = random.uniform(-0.5, 0.5)

            ss = size * 2
            layer = Image.new('RGBA', (ss, ss), (0, 0, 0, 0))
            d = ImageDraw.Draw(layer)
            cx, cy = ss/2, ss/2

            alpha = 210

            # Upper wings (larger, teardrop shape)
            for side in [-1, 1]:
                pts = []
                wing_w = ss * 0.35
                wing_h = ss * 0.3
                for t_i in range(50):
                    t = 2 * math.pi * t_i / 50
                    # Teardrop shape
                    wx = side * wing_w * (1 - math.cos(t)) * math.sin(t) * 0.8
                    wy = -wing_h * math.cos(t) * 0.7 - wing_h * 0.1
                    pts.append((cx + wx, cy + wy))
                d.polygon(pts, fill=(*color, alpha))
                # Wing pattern (inner circle)
                ic_x = cx + side * wing_w * 0.35
                ic_y = cy - wing_h * 0.35
                ic_r = wing_w * 0.18
                d.ellipse([ic_x-ic_r, ic_y-ic_r, ic_x+ic_r, ic_y+ic_r],
                          fill=(*[min(255, c+40) for c in color], 120))

            # Lower wings (smaller, rounder)
            for side in [-1, 1]:
                pts = []
                wing_w = ss * 0.22
                wing_h = ss * 0.2
                for t_i in range(50):
                    t = 2 * math.pi * t_i / 50
                    wx = side * wing_w * (0.8 + 0.2 * math.cos(t)) * math.sin(t)
                    wy = wing_h * (0.5 - 0.5 * math.cos(t)) + ss * 0.02
                    pts.append((cx + wx, cy + wy))
                darker = tuple(max(0, c - 20) for c in color)
                d.polygon(pts, fill=(*darker, alpha - 10))

            # Body
            body_w = ss * 0.025
            body_h = ss * 0.25
            d.ellipse([cx - body_w, cy - body_h * 0.6, cx + body_w, cy + body_h * 0.6],
                      fill=(60, 50, 40, 230))

            # Antennae
            for side in [-1, 1]:
                ant_pts = []
                for t_i in range(20):
                    t = t_i / 19
                    ax = cx + side * ss * 0.08 * t
                    ay = cy - body_h * 0.6 - ss * 0.12 * t
                    ant_pts.append((ax, ay))
                if len(ant_pts) >= 2:
                    d.line(ant_pts, fill=(60, 50, 40, 200), width=max(2, ss//200))
                # Tip dot
                d.ellipse([ant_pts[-1][0]-ss*0.012, ant_pts[-1][1]-ss*0.012,
                           ant_pts[-1][0]+ss*0.012, ant_pts[-1][1]+ss*0.012],
                          fill=(60, 50, 40, 220))

            layer = layer.rotate(math.degrees(rotation), resample=Image.BICUBIC, expand=False)
            layer = layer.resize((size, size), Image.LANCZOS)
            place_seamless(canvas, layer, x, y, CANVAS)

    return canvas


def create_shamrock_pattern():
    """Lucky Shamrock — crisp three-leaf clovers."""
    print("  Creating Shamrock pattern...")
    canvas = Image.new('RGB', (CANVAS, CANVAS), (252, 255, 252))

    greens = [
        (80, 160, 90),    # medium green
        (60, 140, 75),    # forest green
        (100, 180, 110),  # light green
        (50, 130, 70),    # deep green
        (90, 170, 100),   # spring green
    ]

    cols, rows = 9, 9
    spacing_x = CANVAS / cols
    spacing_y = CANVAS / rows

    for row in range(rows):
        for col in range(cols):
            x = col * spacing_x + spacing_x / 2 + random.randint(-30, 30)
            y = row * spacing_y + spacing_y / 2 + random.randint(-30, 30)
            if row % 2:
                x += spacing_x / 2

            color = random.choice(greens)
            size = random.randint(260, 380)
            rotation = random.uniform(-0.3, 0.3)

            ss = size * 2
            layer = Image.new('RGBA', (ss, ss), (0, 0, 0, 0))
            d = ImageDraw.Draw(layer)
            cx, cy = ss/2, ss/2 - ss*0.05

            alpha = 215
            leaf_r = ss * 0.2

            # Three heart-shaped leaves at 120° intervals
            for i in range(3):
                angle = 2 * math.pi * i / 3 - math.pi / 2
                leaf_cx = cx + leaf_r * 0.8 * math.cos(angle)
                leaf_cy = cy + leaf_r * 0.8 * math.sin(angle)

                # Each leaf is a heart shape pointing outward
                heart_pts = heart_points(0, 0, leaf_r * 0.85, 120)
                # Rotate heart to point outward
                rot = angle + math.pi / 2
                cos_r, sin_r = math.cos(rot), math.sin(rot)
                translated = [(leaf_cx + px * cos_r - py * sin_r,
                               leaf_cy + px * sin_r + py * cos_r) for px, py in heart_pts]
                d.polygon(translated, fill=(*color, alpha))

                # Leaf vein (center line)
                vein_start = (cx, cy)
                vein_end = (leaf_cx + leaf_r * 0.6 * math.cos(angle),
                            leaf_cy + leaf_r * 0.6 * math.sin(angle))
                darker = tuple(max(0, c - 30) for c in color)
                d.line([vein_start, vein_end], fill=(*darker, 120), width=max(2, ss//150))

            # Stem
            stem_top = (cx, cy + ss * 0.05)
            stem_bot = (cx + ss * 0.03, cy + ss * 0.3)
            d.line([stem_top, stem_bot], fill=(70, 120, 60, 200), width=max(3, ss//80))

            layer = layer.rotate(math.degrees(rotation), resample=Image.BICUBIC, expand=False)
            layer = layer.resize((size, size), Image.LANCZOS)
            place_seamless(canvas, layer, x, y, CANVAS)

    return canvas


def create_snowflake_pattern():
    """Winter Snowflake — geometric 6-fold crystal snowflakes."""
    print("  Creating Snowflake pattern...")
    canvas = Image.new('RGB', (CANVAS, CANVAS), (240, 245, 255))

    blue_shades = [
        (160, 200, 240, 220),  # light blue
        (140, 180, 225, 220),  # medium blue
        (180, 210, 245, 220),  # pale blue
        (130, 175, 220, 220),  # steel blue
        (170, 195, 235, 220),  # soft blue
    ]

    cols, rows = 10, 10
    spacing_x = CANVAS / cols
    spacing_y = CANVAS / rows

    for row in range(rows):
        for col in range(cols):
            x = col * spacing_x + spacing_x / 2 + random.randint(-25, 25)
            y = row * spacing_y + spacing_y / 2 + random.randint(-25, 25)
            if row % 2:
                x += spacing_x / 2

            color = random.choice(blue_shades)
            size = random.randint(220, 340)
            rotation = random.uniform(0, math.pi / 6)

            ss = size * 2
            layer = Image.new('RGBA', (ss, ss), (0, 0, 0, 0))
            d = ImageDraw.Draw(layer)
            cx, cy = ss/2, ss/2
            arm_len = ss * 0.38
            arm_w = max(4, ss // 50)

            # 6-fold symmetry
            for i in range(6):
                angle = rotation + math.pi * i / 3
                end_x = cx + arm_len * math.cos(angle)
                end_y = cy + arm_len * math.sin(angle)

                # Main arm
                d.line([(cx, cy), (end_x, end_y)], fill=color, width=arm_w)

                # Side branches (3 pairs per arm)
                for j in range(1, 4):
                    branch_pos = j / 4
                    bx = cx + arm_len * branch_pos * math.cos(angle)
                    by = cy + arm_len * branch_pos * math.sin(angle)
                    branch_len = arm_len * 0.3 * (1 - branch_pos * 0.4)

                    for side in [-1, 1]:
                        branch_angle = angle + side * math.pi / 3
                        bex = bx + branch_len * math.cos(branch_angle)
                        bey = by + branch_len * math.sin(branch_angle)
                        d.line([(bx, by), (bex, bey)], fill=color, width=max(2, arm_w // 2))

                        # Tiny tip crystal
                        tip_r = max(3, arm_w)
                        d.ellipse([bex-tip_r, bey-tip_r, bex+tip_r, bey+tip_r], fill=color)

                # Arm tip crystal
                tip_r = max(4, arm_w * 1.5)
                d.ellipse([end_x-tip_r, end_y-tip_r, end_x+tip_r, end_y+tip_r], fill=color)

            # Center hexagon
            hex_r = arm_w * 3
            hex_pts = [(cx + hex_r * math.cos(rotation + math.pi * k / 3),
                        cy + hex_r * math.sin(rotation + math.pi * k / 3)) for k in range(6)]
            d.polygon(hex_pts, fill=color)

            layer = layer.resize((size, size), Image.LANCZOS)
            place_seamless(canvas, layer, x, y, CANVAS)

    return canvas


def create_polkadot_pattern():
    """Pastel Polka Dot — same design, just crisper. Hearts-as-dots layout."""
    print("  Creating Polka Dot pattern (hearts)...")
    canvas = Image.new('RGB', (CANVAS, CANVAS), (255, 255, 255))

    colors = [
        (240, 160, 180, 230),  # pink
        (180, 210, 240, 230),  # blue
        (200, 180, 230, 230),  # purple
        (230, 190, 130, 230),  # gold/peach
        (170, 215, 195, 230),  # mint/teal
    ]

    # Dense grid of small hearts
    elem_size = 160
    cols, rows = 14, 18
    spacing_x = CANVAS / cols
    spacing_y = CANVAS / rows

    color_idx = 0
    for row in range(rows):
        for col in range(cols):
            # Cycle through colors in a pattern
            color = colors[color_idx % len(colors)]
            color_idx += 1

            x = col * spacing_x + spacing_x / 2
            y = row * spacing_y + spacing_y / 2
            if row % 2:
                x += spacing_x / 2

            ss = elem_size * 2
            layer = Image.new('RGBA', (ss, ss), (0, 0, 0, 0))
            d = ImageDraw.Draw(layer)
            pts = heart_points(ss/2, ss/2 + ss*0.04, ss * 0.36, 200)
            d.polygon(pts, fill=color)

            # Sparkle dots (white highlights)
            sparkle_r = ss * 0.04
            d.ellipse([ss*0.35 - sparkle_r, ss*0.35 - sparkle_r,
                        ss*0.35 + sparkle_r, ss*0.35 + sparkle_r],
                       fill=(255, 255, 255, 180))

            layer = layer.resize((elem_size, elem_size), Image.LANCZOS)
            place_seamless(canvas, layer, x, y, CANVAS)

    return canvas


def create_duck_pattern():
    """Duck pattern — extract elements from source image, arrange seamlessly."""
    print("  Creating Duck pattern from source image...")
    src_path = '/Users/alexhosage/Downloads/Copy of Surface Pattern Design 1 (12 X 12 in) - 2.png'
    src = Image.open(src_path).convert('RGBA')

    # The source image has elements on a cream background (~#FAF3EB)
    # Extract individual elements by cropping and removing background

    def extract_element(img, box, bg_threshold=30):
        """Crop region and make cream background transparent."""
        cropped = img.crop(box)
        arr = np.array(cropped).astype(float)
        # Cream background color (approximate)
        bg = np.array([250, 243, 235, 255], dtype=float)
        # Distance from background
        dist = np.sqrt(np.sum((arr[:,:,:3] - bg[:3])**2, axis=2))
        # Create alpha mask
        alpha = np.clip(dist / bg_threshold * 255, 0, 255).astype(np.uint8)
        result = cropped.copy()
        result.putalpha(Image.fromarray(alpha))
        return result

    # Define crop regions for key elements (x1, y1, x2, y2) in 1200x1200 source
    elements = {
        'duck_pair': (370, 340, 750, 650),      # Kissing ducks center
        'chicks': (680, 780, 1050, 1050),         # Baby chicks bottom right
        'flower_1': (520, 100, 700, 340),         # Orange flower top center
        'flower_2': (80, 600, 280, 850),          # Small flowers left
        'greenery_1': (30, 30, 350, 250),         # Willow branch top left
        'butterfly_1': (280, 240, 380, 330),      # Butterfly
        'herbs_1': (850, 200, 1050, 500),         # Herb sprigs right
        'flower_3': (900, 600, 1120, 850),        # Flowers right side
        'butterfly_2': (700, 120, 790, 200),      # Small butterfly
    }

    extracted = {}
    for name, box in elements.items():
        try:
            elem = extract_element(src, box, bg_threshold=35)
            extracted[name] = elem
            print(f"    Extracted {name}: {elem.size}")
        except Exception as e:
            print(f"    Failed {name}: {e}")

    # Create seamless pattern at 3600x3600
    canvas = Image.new('RGBA', (CANVAS, CANVAS), (250, 243, 238, 255))

    # Scale factor from 1200 to 3600
    scale = 3.0

    # Define placement grid
    placements = [
        # (element_name, x, y, scale_mult)
        ('duck_pair', 600, 600, 1.2),
        ('chicks', 2400, 2400, 1.1),
        ('duck_pair', 2200, 800, 1.0),
        ('chicks', 800, 2800, 1.0),
        ('flower_1', 1500, 300, 1.0),
        ('flower_1', 3200, 1800, 0.9),
        ('flower_2', 400, 1600, 1.0),
        ('flower_2', 2800, 400, 0.85),
        ('flower_3', 1800, 2000, 0.9),
        ('flower_3', 100, 3200, 1.0),
        ('greenery_1', 1200, 1400, 0.8),
        ('greenery_1', 3000, 3000, 0.9),
        ('herbs_1', 2600, 1400, 0.85),
        ('herbs_1', 600, 3400, 0.8),
        ('butterfly_1', 1000, 200, 1.2),
        ('butterfly_1', 2000, 1500, 1.0),
        ('butterfly_2', 3200, 600, 1.3),
        ('butterfly_2', 1400, 2600, 1.1),
        ('butterfly_1', 3400, 2800, 1.0),
        ('flower_2', 1800, 3400, 0.9),
        ('herbs_1', 200, 200, 0.7),
    ]

    for name, px, py, s in placements:
        if name not in extracted:
            continue
        elem = extracted[name]
        w, h = elem.size
        new_w = int(w * scale * s)
        new_h = int(h * scale * s)
        if new_w < 10 or new_h < 10:
            continue
        resized = elem.resize((new_w, new_h), Image.LANCZOS)
        place_seamless(canvas, resized, px, py, CANVAS)

    return canvas.convert('RGB')


def create_trex_pattern():
    """Cute T-Rex seamless pattern — cartoon dinosaurs in pastel colors."""
    print("  Creating T-Rex pattern...")
    canvas = Image.new('RGB', (CANVAS, CANVAS), (255, 253, 248))

    dino_colors = [
        (140, 195, 140),  # sage green
        (180, 210, 160),  # light green
        (160, 190, 220),  # blue
        (220, 170, 140),  # peach/orange
        (200, 170, 200),  # lavender
        (230, 190, 130),  # golden
    ]

    cols, rows = 7, 7
    spacing_x = CANVAS / cols
    spacing_y = CANVAS / rows

    for row in range(rows):
        for col in range(cols):
            x = col * spacing_x + spacing_x / 2 + random.randint(-30, 30)
            y = row * spacing_y + spacing_y / 2 + random.randint(-30, 30)
            if row % 2:
                x += spacing_x / 2

            color = random.choice(dino_colors)
            size = random.randint(350, 460)
            flip = random.choice([-1, 1])

            ss = size * 2
            layer = Image.new('RGBA', (ss, ss), (0, 0, 0, 0))
            d = ImageDraw.Draw(layer)
            cx, cy = ss/2, ss/2

            alpha = 225
            s = ss / 100  # scale unit

            # --- Cute cartoon T-Rex ---
            # Body (rounded rectangle / ellipse)
            body_x1 = cx - 20*s
            body_y1 = cy - 8*s
            body_x2 = cx + 15*s
            body_y2 = cy + 15*s
            d.rounded_rectangle([body_x1, body_y1, body_x2, body_y2],
                                radius=int(10*s), fill=(*color, alpha))

            # Head (circle, front of body)
            head_cx = cx + 22*s
            head_cy = cy - 8*s
            head_r = 14*s
            d.ellipse([head_cx - head_r, head_cy - head_r,
                       head_cx + head_r, head_cy + head_r], fill=(*color, alpha))

            # Snout (small oval extending from head)
            snout_cx = head_cx + 12*s
            snout_cy = head_cy + 2*s
            d.ellipse([snout_cx - 8*s, snout_cy - 5*s,
                       snout_cx + 8*s, snout_cy + 5*s], fill=(*color, alpha))

            # Eye (white circle + black pupil)
            eye_cx = head_cx + 5*s
            eye_cy = head_cy - 3*s
            eye_r = 4*s
            d.ellipse([eye_cx-eye_r, eye_cy-eye_r, eye_cx+eye_r, eye_cy+eye_r],
                      fill=(255, 255, 255, 240))
            pupil_r = 2.2*s
            d.ellipse([eye_cx+s-pupil_r, eye_cy-pupil_r, eye_cx+s+pupil_r, eye_cy+pupil_r],
                      fill=(40, 40, 40, 240))
            # Eye shine
            shine_r = 1.2*s
            d.ellipse([eye_cx-shine_r, eye_cy-1.5*s-shine_r,
                       eye_cx+shine_r, eye_cy-1.5*s+shine_r],
                      fill=(255, 255, 255, 200))

            # Mouth (small smile line)
            d.arc([snout_cx - 4*s, snout_cy - 1*s, snout_cx + 6*s, snout_cy + 5*s],
                  10, 170, fill=(80, 60, 50, 180), width=max(2, int(1.2*s)))

            # Nostril
            d.ellipse([snout_cx + 4*s, snout_cy - 1*s, snout_cx + 6*s, snout_cy + 1*s],
                      fill=(*[max(0, c-40) for c in color], 150))

            # Tiny arms
            for arm_y_off in [0]:
                arm_x = cx + 10*s
                arm_y = cy + arm_y_off
                # Upper arm
                d.line([(arm_x, arm_y), (arm_x + 8*s, arm_y + 6*s)],
                       fill=(*color, alpha), width=max(3, int(3*s)))
                # Lower arm / hand
                d.line([(arm_x + 8*s, arm_y + 6*s), (arm_x + 6*s, arm_y + 10*s)],
                       fill=(*color, alpha), width=max(2, int(2.5*s)))

            # Legs (two stubby legs)
            for leg_off in [-10*s, 5*s]:
                leg_x = cx + leg_off
                leg_y1 = cy + 13*s
                leg_y2 = cy + 28*s
                leg_w = 6*s
                d.rounded_rectangle([leg_x - leg_w, leg_y1, leg_x + leg_w, leg_y2],
                                    radius=int(4*s), fill=(*color, alpha))
                # Foot
                d.ellipse([leg_x - leg_w*1.3, leg_y2 - 3*s,
                           leg_x + leg_w*1.3, leg_y2 + 3*s], fill=(*color, alpha))

            # Tail (curves backward from body)
            tail_pts = []
            for t_i in range(30):
                t = t_i / 29
                tx = cx - 20*s - 18*s * t
                ty = cy + 5*s + 8*s * math.sin(t * math.pi * 0.7)
                tail_pts.append((tx, ty))
            # Draw tail as thick line
            for i in range(len(tail_pts)-1):
                tw = int((5 - 3 * (i / len(tail_pts))) * s)
                d.line([tail_pts[i], tail_pts[i+1]], fill=(*color, alpha), width=max(2, tw))

            # Back spines (small triangles along back)
            spine_color = (*[min(255, c + 30) for c in color], 200)
            for sp in range(5):
                sp_t = sp / 5
                sp_x = cx - 15*s + 30*s * sp_t
                sp_y = cy - 8*s - 2*s
                sp_h = 5*s * (0.5 + 0.5 * math.sin(math.pi * sp_t))
                d.polygon([(sp_x - 2.5*s, sp_y), (sp_x, sp_y - sp_h), (sp_x + 2.5*s, sp_y)],
                          fill=spine_color)

            # Belly lighter shade
            belly_color = (*[min(255, c + 25) for c in color], 140)
            d.ellipse([cx - 15*s, cy + 2*s, cx + 10*s, cy + 14*s], fill=belly_color)

            # Flip horizontally if needed
            if flip < 0:
                layer = layer.transpose(Image.FLIP_LEFT_RIGHT)

            layer = layer.resize((size, size), Image.LANCZOS)
            place_seamless(canvas, layer, x, y, CANVAS)

    return canvas


# ─── Product Image Generator ─────────────────────────────────────────

def create_product_images(lid, pattern):
    """Create 3 listing images from a pattern tile."""
    # _0: Pattern tile (main image)
    img0 = pattern.copy()
    img0.convert('RGB').save(os.path.join(IMG_DIR, f'{lid}_0.jpg'), 'JPEG', quality=95)
    print(f"    {lid}_0.jpg — pattern tile")

    # Also save high-res PNG for download
    pattern.save(os.path.join(PATTERNS_DIR, f'{lid}-clean.png'), 'PNG')

    # _1: 2x2 tiled preview
    tile_size = 1800
    tile = pattern.resize((tile_size, tile_size), Image.LANCZOS)
    tiled = Image.new('RGB', (CANVAS, CANVAS), (255, 255, 255))
    tiled.paste(tile, (0, 0))
    tiled.paste(tile, (tile_size, 0))
    tiled.paste(tile, (0, tile_size))
    tiled.paste(tile, (tile_size, tile_size))

    # Grid lines
    draw = ImageDraw.Draw(tiled)
    draw.line([(tile_size, 0), (tile_size, CANVAS)], fill=(200, 200, 200), width=3)
    draw.line([(0, tile_size), (CANVAS, tile_size)], fill=(200, 200, 200), width=3)

    # "Seamless Tile Repeat" label
    label_w, label_h = 500, 60
    lx = (CANVAS - label_w) // 2
    ly = (CANVAS - label_h) // 2
    draw.rounded_rectangle([lx, ly, lx + label_w, ly + label_h], radius=12,
                            fill=(255, 255, 255, 230))
    # Simple text without font dependency
    try:
        from PIL import ImageFont
        font = ImageFont.truetype('/System/Library/Fonts/Avenir Next.ttc', 32)
        draw.text((lx + 50, ly + 12), "Seamless Tile Repeat", font=font, fill=(100, 85, 85))
    except:
        pass

    tiled.convert('RGB').save(os.path.join(IMG_DIR, f'{lid}_1.jpg'), 'JPEG', quality=95)
    print(f"    {lid}_1.jpg — tiled preview")

    # _2: Framed mockup
    mockup = Image.new('RGB', (CANVAS, CANVAS), (245, 240, 235))
    pad = 200
    pat_small = pattern.resize((CANVAS - 2*pad, CANVAS - 2*pad), Image.LANCZOS)
    md = ImageDraw.Draw(mockup)
    # Shadow
    md.rectangle([pad+8, pad+8, CANVAS-pad+8, CANVAS-pad+8], fill=(200, 195, 190))
    mockup.paste(pat_small.convert('RGB'), (pad, pad))
    md.rectangle([pad, pad, CANVAS-pad, CANVAS-pad], outline=(180, 175, 170), width=3)

    mockup.save(os.path.join(IMG_DIR, f'{lid}_2.jpg'), 'JPEG', quality=95)
    print(f"    {lid}_2.jpg — framed mockup")


# ─── Main ─────────────────────────────────────────────────────────────

PATTERNS = [
    ('8800000001', 'Pastel Watercolor Hearts', create_hearts_pattern),
    ('8800000002', 'Spring Wildflower', create_wildflower_pattern),
    ('8800000003', 'Autumn Leaves & Berries', create_autumn_pattern),
    ('8800000004', 'Celestial Stars & Moons', create_celestial_pattern),
    ('8800000005', 'Watercolor Butterfly', create_butterfly_pattern),
    ('8800000006', 'Lucky Shamrock', create_shamrock_pattern),
    ('8800000007', 'Winter Snowflake', create_snowflake_pattern),
    ('8800000008', 'Pastel Polka Dot', create_polkadot_pattern),
    ('8800000009', 'Watercolor Ducks', create_duck_pattern),
    ('8800000010', 'Cute T-Rex Dinosaur', create_trex_pattern),
]


def main():
    os.makedirs(PATTERNS_DIR, exist_ok=True)

    print(f"Generating {len(PATTERNS)} patterns at {CANVAS}x{CANVAS} (300 DPI)...\n")

    for lid, name, builder in PATTERNS:
        print(f"\n[{lid}] {name}")
        pattern = builder()

        # Save clean pattern PNG
        clean_path = os.path.join(PATTERNS_DIR, f'{lid}-clean.png')
        pattern.save(clean_path, 'PNG')
        print(f"  Saved {clean_path}")

        # Create product listing images
        create_product_images(lid, pattern)

    print(f"\nDone! All {len(PATTERNS)} patterns generated at {CANVAS}x{CANVAS}.")


if __name__ == '__main__':
    main()
