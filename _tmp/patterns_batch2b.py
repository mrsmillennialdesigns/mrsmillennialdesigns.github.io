#!/usr/bin/env python3
"""Seamless patterns batch 2b: Mermaid Watercolor, Watercolor Sea Animals.
3600x3600, 3x supersample, full opacity, PIL built-in primitives."""

from PIL import Image, ImageDraw
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
    from PIL import ImageFont
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
# 9. MERMAID WATERCOLOR (rainbow color scheme)
# =============================================================================
def draw_mermaid(d, cx, cy, ss, tail_color, hair_color, skin_color):
    """Cute mermaid: round head, flowing hair, simple body, scaled tail."""
    # Tail (curved teardrop shape at bottom)
    tail_w = ss * 0.14
    tail_h = ss * 0.28
    tail_top = cy + ss * 0.02

    # Main tail body (oval)
    d.ellipse([cx-tail_w, tail_top, cx+tail_w, tail_top+tail_h],
              fill=(*tail_color, 255))

    # Tail fin (two overlapping ellipses at bottom)
    fin_w = tail_w * 1.3
    fin_h = tail_h * 0.25
    fin_y = tail_top + tail_h * 0.85
    for side in [-1, 1]:
        d.ellipse([cx+side*tail_w*0.3-fin_w*0.7, fin_y-fin_h*0.3,
                   cx+side*tail_w*0.3+fin_w*0.7, fin_y+fin_h],
                  fill=(*tail_color, 255))

    # Scale details on tail (small arcs)
    scale_r = tail_w * 0.25
    darker_tail = tuple(max(0, c-25) for c in tail_color)
    for row_i in range(4):
        sy = tail_top + tail_h * 0.15 + row_i * tail_h * 0.18
        for col_i in range(3):
            sx = cx - tail_w*0.5 + col_i * tail_w * 0.5
            if row_i % 2:
                sx += tail_w * 0.25
            d.arc([sx-scale_r, sy-scale_r, sx+scale_r, sy+scale_r],
                  start=0, end=180, fill=(*darker_tail, 255), width=max(2, ss//200))

    # Body / torso (small oval, skin colored)
    torso_w = ss * 0.1
    torso_h = ss * 0.08
    torso_y = cy - ss * 0.01
    d.ellipse([cx-torso_w, torso_y-torso_h, cx+torso_w, torso_y+torso_h],
              fill=(*skin_color, 255))

    # Shell top (bikini)
    shell_r = torso_w * 0.35
    for side in [-1, 1]:
        sx = cx + side * torso_w * 0.45
        sy = torso_y - torso_h * 0.2
        d.ellipse([sx-shell_r, sy-shell_r, sx+shell_r, sy+shell_r],
                  fill=(*tail_color, 255))

    # Head (circle)
    hr = ss * 0.1
    hx = cx
    hy = cy - ss * 0.13
    d.ellipse([hx-hr, hy-hr, hx+hr, hy+hr], fill=(*skin_color, 255))

    # Hair (overlapping ovals behind and around head)
    hair_positions = [
        (-0.7, -0.6, 0.5, 0.7),   # left side
        (0.7, -0.6, 0.5, 0.7),    # right side
        (0, -1.1, 0.65, 0.45),    # top
        (-0.9, 0.1, 0.4, 0.8),    # left flow down
        (0.9, 0.1, 0.4, 0.8),     # right flow down
    ]
    for hpx, hpy, hw, hh in hair_positions:
        d.ellipse([hx+hr*hpx-hr*hw, hy+hr*hpy-hr*hh,
                   hx+hr*hpx+hr*hw, hy+hr*hpy+hr*hh],
                  fill=(*hair_color, 255))

    # Face details
    # Eyes
    er = hr * 0.1
    for side in [-1, 1]:
        ex = hx + side * hr * 0.3
        ey = hy - hr * 0.05
        d.ellipse([ex-er, ey-er, ex+er, ey+er], fill=(40, 35, 50, 255))
        # Eye shine
        sr = er * 0.45
        d.ellipse([ex-er*0.3, ey-er*0.5, ex-er*0.3+sr, ey-er*0.5+sr],
                  fill=(255, 255, 255, 255))

    # Blush
    blush_r = hr * 0.1
    for side in [-1, 1]:
        bx = hx + side * hr * 0.55
        by = hy + hr * 0.15
        d.ellipse([bx-blush_r, by-blush_r, bx+blush_r, by+blush_r],
                  fill=(240, 170, 170, 200))

    # Smile
    d.arc([hx-hr*0.2, hy+hr*0.1, hx+hr*0.2, hy+hr*0.4],
          start=0, end=180, fill=(180, 100, 100, 255), width=max(2, ss//200))


def draw_starfish(d, cx, cy, ss, color):
    """Five-pointed starfish with rounded tips."""
    r_outer = ss * 0.18
    r_inner = r_outer * 0.42
    pts = []
    for i in range(10):
        angle = math.pi * i / 5 - math.pi/2
        r = r_outer if i % 2 == 0 else r_inner
        pts.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    d.polygon(pts, fill=(*color, 255))
    # Center dot
    cr = r_inner * 0.35
    d.ellipse([cx-cr, cy-cr, cx+cr, cy+cr],
              fill=(min(255, color[0]+25), min(255, color[1]+20), min(255, color[2]+15), 255))


def draw_seashell(d, cx, cy, ss, color):
    """Simple scallop shell."""
    sw = ss * 0.16
    sh = ss * 0.14
    # Main shell body
    d.ellipse([cx-sw, cy-sh*0.5, cx+sw, cy+sh], fill=(*color, 255))
    # Fan ridges
    lighter = tuple(min(255, c+30) for c in color)
    for i in range(5):
        angle = math.pi * 0.15 + i * math.pi * 0.7 / 4
        rx = cx + sw * 0.6 * math.cos(angle) - sw * 0.3
        ry = cy + sh * 0.5 * math.sin(angle) - sh * 0.3
        d.line([(cx, cy+sh*0.4), (cx + sw*0.7*math.cos(angle-math.pi/2),
                cy - sh*0.3 + sh*0.6*math.sin(angle))],
               fill=(*lighter, 255), width=max(2, ss//180))
    # Hinge point
    hr = sw * 0.12
    d.ellipse([cx-hr, cy+sh*0.3, cx+hr, cy+sh*0.3+hr*2], fill=(*lighter, 255))


def create_mermaid():
    print("  Mermaid Watercolor...")
    random.seed(109)
    canvas = Image.new('RGB', (CANVAS, CANVAS), (240, 248, 255))

    tail_colors = [
        (140, 210, 200),  # teal
        (180, 160, 230),  # purple
        (240, 170, 180),  # pink
        (160, 200, 235),  # blue
        (200, 220, 140),  # green
        (240, 190, 130),  # coral/orange
    ]
    hair_colors = [
        (240, 180, 100),  # golden
        (200, 100, 80),   # red
        (180, 140, 100),  # brown
        (100, 80, 70),    # dark brown
        (220, 180, 160),  # strawberry blonde
        (160, 120, 180),  # purple
    ]
    skin_colors = [
        (245, 220, 200),  # light
        (230, 200, 175),  # medium
        (210, 180, 155),  # tan
        (240, 215, 195),  # warm light
    ]

    cols, rows = 5, 5
    sx, sy = CANVAS / cols, CANVAS / rows

    for row in range(rows):
        for col in range(cols):
            x = col * sx + sx/2 + random.randint(-25, 25)
            y = row * sy + sy/2 + random.randint(-20, 20)
            if row % 2:
                x += sx / 2

            tc = random.choice(tail_colors)
            hc = random.choice(hair_colors)
            sc = random.choice(skin_colors)
            size = random.randint(480, 560)
            flip = random.choice([-1, 1])

            ss = size * 3
            layer = Image.new('RGBA', (ss, ss), (0, 0, 0, 0))
            d = ImageDraw.Draw(layer)
            draw_mermaid(d, ss/2, ss/2, ss, tc, hc, sc)

            if flip < 0:
                layer = layer.transpose(Image.FLIP_LEFT_RIGHT)

            layer = layer.resize((size, size), Image.LANCZOS)
            place_seamless(canvas, layer, x, y, CANVAS)

    # Scatter starfish and shells
    accent_colors = [(240, 180, 140), (180, 200, 230), (200, 170, 220),
                     (240, 200, 160), (170, 215, 200)]
    for _ in range(25):
        asize = random.randint(100, 160)
        ax = random.randint(0, CANVAS)
        ay = random.randint(0, CANVAS)
        ss2 = asize * 3
        al = Image.new('RGBA', (ss2, ss2), (0, 0, 0, 0))
        ad = ImageDraw.Draw(al)
        ac = random.choice(accent_colors)
        if random.random() < 0.5:
            draw_starfish(ad, ss2/2, ss2/2, ss2, ac)
        else:
            draw_seashell(ad, ss2/2, ss2/2, ss2, ac)
        al = al.rotate(random.uniform(-20, 20), resample=Image.BICUBIC, expand=False)
        al = al.resize((asize, asize), Image.LANCZOS)
        place_seamless(canvas, al, ax, ay, CANVAS)

    # Small bubbles
    for _ in range(20):
        bsize = random.randint(30, 60)
        bx = random.randint(0, CANVAS)
        by = random.randint(0, CANVAS)
        bl = Image.new('RGBA', (bsize*3, bsize*3), (0, 0, 0, 0))
        bd = ImageDraw.Draw(bl)
        br = bsize * 3 * 0.35
        bd.ellipse([bsize*3/2-br, bsize*3/2-br, bsize*3/2+br, bsize*3/2+br],
                   outline=(190, 215, 235, 255), width=max(2, bsize*3//40))
        sr = br * 0.25
        bd.ellipse([bsize*3/2-br*0.3-sr, bsize*3/2-br*0.3-sr,
                    bsize*3/2-br*0.3+sr, bsize*3/2-br*0.3+sr],
                   fill=(220, 235, 250, 255))
        bl = bl.resize((bsize, bsize), Image.LANCZOS)
        place_seamless(canvas, bl, bx, by, CANVAS)

    return canvas


# =============================================================================
# 10. WATERCOLOR SEA ANIMALS
# =============================================================================
def draw_whale(d, cx, cy, ss, color):
    """Cute baby whale: oval body, tail fluke, eye, spout."""
    lighter = tuple(min(255, c+20) for c in color)
    belly_color = tuple(min(255, c+40) for c in color)

    # Body (horizontal oval)
    bw = ss * 0.28
    bh = ss * 0.16
    d.ellipse([cx-bw, cy-bh, cx+bw, cy+bh], fill=(*color, 255))

    # Belly (lighter bottom half overlay)
    d.ellipse([cx-bw*0.85, cy-bh*0.1, cx+bw*0.75, cy+bh*0.9],
              fill=(*belly_color, 255))

    # Tail fluke
    tx = cx - bw * 0.85
    ty = cy
    fluke_w = bw * 0.35
    fluke_h = bh * 0.6
    for side in [-1, 1]:
        d.ellipse([tx-fluke_w*1.5, ty+side*fluke_h*0.3-fluke_h*0.5,
                   tx+fluke_w*0.3, ty+side*fluke_h*0.3+fluke_h*0.5],
                  fill=(*color, 255))

    # Fin on top
    fin_x = cx + bw * 0.1
    fin_y = cy - bh * 0.85
    d.polygon([(fin_x-bw*0.08, cy-bh*0.6), (fin_x, fin_y),
               (fin_x+bw*0.12, cy-bh*0.5)], fill=(*color, 255))

    # Eye
    er = bh * 0.13
    ex = cx + bw * 0.5
    ey = cy - bh * 0.2
    d.ellipse([ex-er, ey-er, ex+er, ey+er], fill=(30, 30, 45, 255))
    sr = er * 0.4
    d.ellipse([ex-er*0.2, ey-er*0.4, ex-er*0.2+sr, ey-er*0.4+sr],
              fill=(255, 255, 255, 255))

    # Smile
    d.arc([cx+bw*0.3, cy+bh*0.05, cx+bw*0.65, cy+bh*0.45],
          start=0, end=180, fill=(*lighter, 255), width=max(2, ss//180))

    # Water spout
    spout_x = cx + bw * 0.2
    spout_y = cy - bh * 1.1
    for i in range(3):
        drop_r = bh * 0.08
        dx = spout_x + random.uniform(-bh*0.15, bh*0.15)
        dy = spout_y - i * bh * 0.2
        d.ellipse([dx-drop_r*0.6, dy-drop_r, dx+drop_r*0.6, dy+drop_r],
                  fill=(180, 210, 235, 255))


def draw_octopus(d, cx, cy, ss, color):
    """Cute octopus: round head, 8 tentacles, big eyes."""
    lighter = tuple(min(255, c+25) for c in color)

    # Head (large circle)
    hr = ss * 0.16
    d.ellipse([cx-hr, cy-hr*1.1, cx+hr, cy+hr*0.5], fill=(*color, 255))

    # Tentacles (8 small elongated ovals radiating down)
    tent_r_w = hr * 0.18
    tent_r_h = hr * 0.7
    for i in range(8):
        angle = math.pi * 0.15 + i * math.pi * 0.7 / 7
        tx = cx + hr * 0.8 * math.cos(angle - math.pi/2)
        ty = cy + hr * 0.3 + abs(math.cos(angle)) * hr * 0.2
        # Each tentacle curves down
        d.ellipse([tx-tent_r_w, ty, tx+tent_r_w, ty+tent_r_h],
                  fill=(*color, 255))
        # Suction cup dots
        dot_r = tent_r_w * 0.3
        for j in range(2):
            dy = ty + tent_r_h * 0.3 + j * tent_r_h * 0.25
            d.ellipse([tx-dot_r, dy-dot_r, tx+dot_r, dy+dot_r],
                      fill=(*lighter, 255))

    # Eyes
    er = hr * 0.18
    for side in [-1, 1]:
        ex = cx + side * hr * 0.35
        ey = cy - hr * 0.35
        d.ellipse([ex-er, ey-er, ex+er, ey+er], fill=(255, 255, 255, 255))
        # Pupil
        pr = er * 0.55
        d.ellipse([ex-pr+side*pr*0.15, ey-pr*0.1, ex+pr+side*pr*0.15, ey+pr*0.9],
                  fill=(35, 30, 45, 255))
        # Shine
        sr = er * 0.25
        d.ellipse([ex-er*0.1, ey-er*0.4, ex-er*0.1+sr, ey-er*0.4+sr],
                  fill=(255, 255, 255, 255))

    # Smile
    d.arc([cx-hr*0.25, cy-hr*0.05, cx+hr*0.25, cy+hr*0.3],
          start=0, end=180, fill=(max(0,color[0]-40), max(0,color[1]-40), max(0,color[2]-40), 255),
          width=max(2, ss//200))

    # Cheek blush
    br = hr * 0.1
    for side in [-1, 1]:
        d.ellipse([cx+side*hr*0.55-br, cy-hr*0.1-br,
                   cx+side*hr*0.55+br, cy-hr*0.1+br],
                  fill=(*lighter, 200))


def draw_fish(d, cx, cy, ss, color):
    """Simple cute fish: oval body, triangle tail, eye."""
    bw = ss * 0.18
    bh = ss * 0.11
    # Body
    d.ellipse([cx-bw, cy-bh, cx+bw, cy+bh], fill=(*color, 255))

    # Tail fin (triangle)
    d.polygon([(cx-bw*0.7, cy-bh*0.8), (cx-bw*1.3, cy-bh*1.2),
               (cx-bw*1.3, cy+bh*1.2), (cx-bw*0.7, cy+bh*0.8)],
              fill=(*color, 255))

    # Dorsal fin
    d.polygon([(cx-bw*0.1, cy-bh*0.8), (cx+bw*0.1, cy-bh*1.4),
               (cx+bw*0.4, cy-bh*0.7)], fill=(*color, 255))

    # Eye
    er = bh * 0.25
    ex = cx + bw * 0.45
    ey = cy - bh * 0.15
    d.ellipse([ex-er, ey-er, ex+er, ey+er], fill=(255, 255, 255, 255))
    pr = er * 0.5
    d.ellipse([ex-pr+pr*0.2, ey-pr, ex+pr+pr*0.2, ey+pr], fill=(30, 30, 40, 255))

    # Stripe
    lighter = tuple(min(255, c+30) for c in color)
    stripe_w = bw * 0.12
    d.ellipse([cx-stripe_w, cy-bh*0.7, cx+stripe_w, cy+bh*0.7],
              fill=(*lighter, 255))


def draw_jellyfish(d, cx, cy, ss, color):
    """Cute jellyfish: dome top + wavy tentacles."""
    lighter = tuple(min(255, c+30) for c in color)

    # Dome (half ellipse)
    dw = ss * 0.15
    dh = ss * 0.12
    d.ellipse([cx-dw, cy-dh, cx+dw, cy+dh*0.3], fill=(*color, 255))

    # Highlight
    hr = dw * 0.3
    d.ellipse([cx-hr+dw*0.1, cy-dh*0.5, cx+hr+dw*0.1, cy-dh*0.5+hr*1.5],
              fill=(*lighter, 255))

    # Tentacles (thin elongated ovals hanging down)
    tent_count = 5
    for i in range(tent_count):
        tx = cx - dw*0.6 + i * dw * 0.3
        ty = cy + dh * 0.2
        tw = dw * 0.06
        th = dh * random.uniform(1.0, 1.8)
        d.ellipse([tx-tw, ty, tx+tw, ty+th], fill=(*color, 230))

    # Eyes
    er = dw * 0.08
    for side in [-1, 1]:
        ex = cx + side * dw * 0.3
        ey = cy - dh * 0.2
        d.ellipse([ex-er, ey-er, ex+er, ey+er], fill=(40, 35, 50, 255))


def draw_seahorse(d, cx, cy, ss, color):
    """Simple seahorse: curved body with snout and curled tail."""
    lighter = tuple(min(255, c+25) for c in color)

    # Head (circle)
    hr = ss * 0.07
    hx = cx + ss * 0.02
    hy = cy - ss * 0.15
    d.ellipse([hx-hr, hy-hr, hx+hr, hy+hr], fill=(*color, 255))

    # Snout
    snout_w = hr * 0.4
    snout_h = hr * 0.25
    d.ellipse([hx+hr*0.6, hy-snout_h, hx+hr*0.6+snout_w*2, hy+snout_h],
              fill=(*color, 255))

    # Eye
    er = hr * 0.18
    d.ellipse([hx+hr*0.15-er, hy-hr*0.15-er, hx+hr*0.15+er, hy-hr*0.15+er],
              fill=(30, 30, 40, 255))

    # Crown/frill on head
    for i in range(3):
        fx = hx - hr * 0.3 + i * hr * 0.35
        fy = hy - hr * 0.9
        fr = hr * 0.2
        d.ellipse([fx-fr, fy-fr, fx+fr, fy+fr], fill=(*lighter, 255))

    # Body (series of overlapping ovals going down and curving)
    body_segments = [
        (0, -0.06, 0.065, 0.05),
        (0, 0, 0.06, 0.05),
        (-0.01, 0.06, 0.055, 0.045),
        (-0.02, 0.12, 0.05, 0.04),
        (-0.035, 0.17, 0.04, 0.035),
        (-0.055, 0.21, 0.035, 0.03),
        (-0.08, 0.24, 0.03, 0.025),
        (-0.1, 0.26, 0.025, 0.022),
    ]
    for bx, by, bw, bh in body_segments:
        d.ellipse([cx+ss*bx-ss*bw, cy+ss*by-ss*bh,
                   cx+ss*bx+ss*bw, cy+ss*by+ss*bh], fill=(*color, 255))

    # Curled tail tip
    d.ellipse([cx-ss*0.12-ss*0.02, cy+ss*0.26-ss*0.02,
               cx-ss*0.12+ss*0.02, cy+ss*0.26+ss*0.02], fill=(*color, 255))

    # Belly lighter stripe
    for bx, by, bw, bh in body_segments[:5]:
        d.ellipse([cx+ss*bx-ss*bw*0.4, cy+ss*by-ss*bh*0.5,
                   cx+ss*bx+ss*bw*0.4, cy+ss*by+ss*bh*0.5], fill=(*lighter, 255))


def create_sea_animals():
    print("  Watercolor Sea Animals...")
    random.seed(110)
    canvas = Image.new('RGB', (CANVAS, CANVAS), (235, 245, 252))

    whale_colors = [(140, 185, 220), (160, 195, 225), (120, 170, 210)]
    octopus_colors = [(210, 160, 200), (180, 140, 200), (200, 150, 180)]
    fish_colors = [(240, 180, 120), (180, 210, 170), (240, 160, 160),
                   (160, 200, 220), (220, 190, 140)]
    jelly_colors = [(200, 180, 230), (180, 210, 230), (230, 190, 210)]
    seahorse_colors = [(240, 190, 140), (200, 170, 210), (170, 210, 190)]

    cols, rows = 5, 5
    sx, sy = CANVAS / cols, CANVAS / rows
    animal_types = ['whale', 'octopus', 'fish', 'jellyfish', 'seahorse']

    for row in range(rows):
        for col in range(cols):
            x = col * sx + sx/2 + random.randint(-25, 25)
            y = row * sy + sy/2 + random.randint(-20, 20)
            if row % 2:
                x += sx / 2

            atype = random.choice(animal_types)
            size = random.randint(440, 540)
            flip = random.choice([-1, 1])

            ss = size * 3
            layer = Image.new('RGBA', (ss, ss), (0, 0, 0, 0))
            d = ImageDraw.Draw(layer)

            if atype == 'whale':
                draw_whale(d, ss/2, ss/2, ss, random.choice(whale_colors))
            elif atype == 'octopus':
                draw_octopus(d, ss/2, ss/2, ss, random.choice(octopus_colors))
            elif atype == 'fish':
                draw_fish(d, ss/2, ss/2, ss, random.choice(fish_colors))
            elif atype == 'jellyfish':
                draw_jellyfish(d, ss/2, ss/2, ss, random.choice(jelly_colors))
            else:
                draw_seahorse(d, ss/2, ss/2, ss, random.choice(seahorse_colors))

            if flip < 0:
                layer = layer.transpose(Image.FLIP_LEFT_RIGHT)

            layer = layer.resize((size, size), Image.LANCZOS)
            place_seamless(canvas, layer, x, y, CANVAS)

    # Small bubbles
    for _ in range(30):
        bsize = random.randint(25, 55)
        bx = random.randint(0, CANVAS)
        by = random.randint(0, CANVAS)
        bl = Image.new('RGBA', (bsize*3, bsize*3), (0, 0, 0, 0))
        bd = ImageDraw.Draw(bl)
        br = bsize * 3 * 0.35
        bd.ellipse([bsize*3/2-br, bsize*3/2-br, bsize*3/2+br, bsize*3/2+br],
                   outline=(185, 210, 230, 255), width=max(2, bsize*3//40))
        sr = br * 0.25
        bd.ellipse([bsize*3/2-br*0.3-sr, bsize*3/2-br*0.3-sr,
                    bsize*3/2-br*0.3+sr, bsize*3/2-br*0.3+sr],
                   fill=(215, 230, 245, 255))
        bl = bl.resize((bsize, bsize), Image.LANCZOS)
        place_seamless(canvas, bl, bx, by, CANVAS)

    return canvas


# =============================================================================
# MAIN
# =============================================================================
def main():
    patterns = [
        ('8800000019', 'Mermaid Watercolor', create_mermaid),
        ('8800000020', 'Watercolor Sea Animals', create_sea_animals),
    ]
    for lid, name, builder in patterns:
        print(f"[{lid}] {name}")
        pat = builder()
        create_product_images(lid, pat)
    print("\nBatch 2b done!")


if __name__ == '__main__':
    main()
