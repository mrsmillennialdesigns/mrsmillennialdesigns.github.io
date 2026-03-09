#!/usr/bin/env python3
"""Create product listing images for the 8 new seamless patterns."""

from PIL import Image, ImageDraw, ImageFont
import os

IMG_DIR = '/Users/alexhosage/Desktop/mmd-website/img'
PATTERNS_DIR = os.path.join(IMG_DIR, 'patterns')

# Assign synthetic listing IDs for the 8 patterns
PATTERNS = [
    ('8800000001', 'pastel-hearts-seamless-pattern', 'Pastel Watercolor Hearts Seamless Pattern PNG'),
    ('8800000002', 'spring-wildflower-seamless-pattern', 'Spring Wildflower Seamless Pattern PNG'),
    ('8800000003', 'autumn-leaves-seamless-pattern', 'Autumn Leaves & Berries Seamless Pattern PNG'),
    ('8800000004', 'celestial-stars-seamless-pattern', 'Celestial Stars & Moons Seamless Pattern PNG'),
    ('8800000005', 'watercolor-butterfly-seamless-pattern', 'Watercolor Butterfly Seamless Pattern PNG'),
    ('8800000006', 'lucky-shamrock-seamless-pattern', 'Lucky Shamrock Seamless Pattern PNG'),
    ('8800000007', 'winter-snowflake-seamless-pattern', 'Winter Snowflake Seamless Pattern PNG'),
    ('8800000008', 'pastel-polka-dot-seamless-pattern', 'Pastel Polka Dot Seamless Pattern PNG'),
]


def create_listing_images():
    for lid, slug, title in PATTERNS:
        src = os.path.join(PATTERNS_DIR, f"{slug}.png")
        if not os.path.exists(src):
            print(f"  SKIP {slug} — not found")
            continue

        pattern = Image.open(src)

        # _0 image: The pattern itself (convert to JPG, same as other products)
        img0 = pattern.copy()
        img0_path = os.path.join(IMG_DIR, f"{lid}_0.jpg")
        img0.convert('RGB').save(img0_path, 'JPEG', quality=92)
        print(f"  {lid}_0.jpg — pattern tile")

        # _1 image: 2x2 tiled preview (shows seamless repeat)
        clean_src = os.path.join(PATTERNS_DIR, f"{slug}-clean.png")
        if os.path.exists(clean_src):
            clean = Image.open(clean_src).resize((600, 600), Image.LANCZOS)
        else:
            clean = pattern.resize((600, 600), Image.LANCZOS)

        tiled = Image.new('RGB', (1200, 1200), (255, 255, 255))
        tiled.paste(clean, (0, 0))
        tiled.paste(clean, (600, 0))
        tiled.paste(clean, (0, 600))
        tiled.paste(clean, (600, 600))

        # Add thin border and "Seamless Repeat" label
        draw = ImageDraw.Draw(tiled)
        # Grid lines to show tile boundaries
        draw.line([(600, 0), (600, 1200)], fill=(200, 200, 200), width=2)
        draw.line([(0, 600), (1200, 600)], fill=(200, 200, 200), width=2)

        try:
            font = ImageFont.truetype('/System/Library/Fonts/Avenir Next.ttc', 28)
        except:
            font = ImageFont.load_default()
        draw.rounded_rectangle([420, 555, 780, 595], radius=8, fill=(255, 255, 255, 220))
        draw.text((435, 560), "Seamless Tile Repeat", font=font, fill=(120, 100, 100))

        img1_path = os.path.join(IMG_DIR, f"{lid}_1.jpg")
        tiled.save(img1_path, 'JPEG', quality=92)
        print(f"  {lid}_1.jpg — tiled preview")

        # _2 image: Simple mockup frame
        mockup = Image.new('RGB', (1200, 1200), (245, 240, 235))
        # Centered pattern with shadow effect
        shadow_pad = 80
        pattern_small = pattern.resize((1200 - 2 * shadow_pad, 1200 - 2 * shadow_pad), Image.LANCZOS)
        # Simple shadow
        md = ImageDraw.Draw(mockup)
        md.rectangle([shadow_pad + 4, shadow_pad + 4,
                       1200 - shadow_pad + 4, 1200 - shadow_pad + 4],
                      fill=(200, 195, 190))
        mockup.paste(pattern_small.convert('RGB'), (shadow_pad, shadow_pad))
        # Border
        md.rectangle([shadow_pad, shadow_pad,
                       1200 - shadow_pad, 1200 - shadow_pad],
                      outline=(180, 175, 170), width=2)

        img2_path = os.path.join(IMG_DIR, f"{lid}_2.jpg")
        mockup.save(img2_path, 'JPEG', quality=92)
        print(f"  {lid}_2.jpg — framed mockup")

    print("\nDone! All product images created.")


if __name__ == '__main__':
    create_listing_images()
