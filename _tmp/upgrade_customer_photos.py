#!/usr/bin/env python3
"""Replace low-res customer photos with high-res versions and add new gallery images."""

from PIL import Image
import os
import shutil

HIRES_DIR = '/Users/alexhosage/Desktop/mmd-website/_tmp/hires'
CUSTOMER_DIR = '/Users/alexhosage/Desktop/mmd-website/img/customer-photos'

# Mapping: old filename (without extension) -> new high-res source filename
REPLACEMENTS = {
    'IMG_6316_0': 'IMG_6437.png',
    'IMG_6318_0': 'IMG_6438.png',
    'IMG_6334_0': 'IMG_6439.png',
    'IMG_6346_0': 'IMG_6440.png',
    'IMG_6351_0': 'IMG_6441.png',
    'IMG_6352_0': 'IMG_6441.png',  # same source (different crop of same photo)
    'IMG_6354_0': 'IMG_6442.png',
    'IMG_6361_0': 'IMG_6443.png',
    'IMG_6364_0': 'IMG_6444.png',
    'IMG_6374_0': 'IMG_6445.png',
    'IMG_6375_0': 'IMG_6447.png',
    'IMG_6375_1': 'IMG_6446.png',
    'IMG_6387_0': 'IMG_6448.png',
    'IMG_6393_0': 'IMG_6450.png',
    'IMG_6395_0': 'IMG_6451.png',
    'IMG_6402_0': 'IMG_6452.png',
}

# New photos that don't match existing reviews (for gallery only)
NEW_GALLERY_PHOTOS = [
    'IMG_6413.png',  # Mother's Day poem handprint flower art
    'IMG_6414.png',  # Yellow handprint wildflower bouquet
    'IMG_6415.png',  # Blue handprint with lavender bouquet
    'IMG_6416.png',  # Multiple framed prints on kitchen counter
    'IMG_6417.png',  # Two footprint flower arts in album
    'IMG_6418.png',  # Brown/yellow sibling handprints, rustic frame
    'IMG_6419.png',  # Blue handprint with wildflower/lavender
    'IMG_6420.png',  # Teal handprint, "Jackson" for Grammy
    'IMG_6421.png',  # Grandma/Grandpa Mother's Day 2022, white frame
    'IMG_6422.png',  # Two gold-framed yellow handprints
    'IMG_6423.png',  # Santino 2022 handprint
    'IMG_6424.png',  # Yellow+orange handprints
    'IMG_6425.png',  # Purple handprint wildflower
    'IMG_6426.png',  # Purple/pink handprint, blue iris
    'IMG_6427.png',  # Dark navy handprint in frame
    'IMG_6428.png',  # Yellow handprint, framed on counter
    'IMG_6429.png',  # Beautiful peach handprints, Mother's Day 2022
    'IMG_6430.png',  # Two framed handprints, green frames
    'IMG_6431.png',  # Brown handprints, neutral bouquet
    'IMG_6432.png',  # Yellow handprint, light wood frame
    'IMG_6433.png',  # Happy Nana's Day - Weston, Luna, Isaias
    'IMG_6434.png',  # Green handprints Remy & Reese
    'IMG_6435.png',  # Dinosaur bookmarks (classroom product)
    'IMG_6436.png',  # Blue+pink handprints, grandmother's heart
    'IMG_6449.png',  # Purple footprint, oval paper
]


def convert_to_jpg(src_path, dst_path, max_size=800):
    """Convert PNG to JPG, resize to reasonable web size."""
    img = Image.open(src_path)
    # Resize if larger than max_size on any side
    w, h = img.size
    if max(w, h) > max_size:
        ratio = max_size / max(w, h)
        img = img.resize((int(w * ratio), int(h * ratio)), Image.LANCZOS)
    img.convert('RGB').save(dst_path, 'JPEG', quality=90)
    return img.size


def main():
    os.makedirs(CUSTOMER_DIR, exist_ok=True)

    print("=== REPLACING LOW-RES WITH HIGH-RES ===\n")
    for old_name, new_src in REPLACEMENTS.items():
        src = os.path.join(HIRES_DIR, new_src)
        dst = os.path.join(CUSTOMER_DIR, f"{old_name}.jpg")
        if not os.path.exists(src):
            print(f"  SKIP {old_name} — source {new_src} not found")
            continue
        size = convert_to_jpg(src, dst)
        print(f"  REPLACED {old_name}.jpg with {new_src} ({size[0]}x{size[1]})")

    print(f"\n=== ADDING {len(NEW_GALLERY_PHOTOS)} NEW GALLERY PHOTOS ===\n")
    for src_name in NEW_GALLERY_PHOTOS:
        src = os.path.join(HIRES_DIR, src_name)
        # Use the original IMG number as the filename
        base = src_name.replace('.png', '').replace('.jpg', '')
        dst = os.path.join(CUSTOMER_DIR, f"{base}_0.jpg")
        if not os.path.exists(src):
            print(f"  SKIP {src_name} — not found")
            continue
        size = convert_to_jpg(src, dst)
        print(f"  ADDED {base}_0.jpg ({size[0]}x{size[1]})")

    # List final count
    all_photos = [f for f in os.listdir(CUSTOMER_DIR) if f.endswith('.jpg')]
    print(f"\nTotal customer photos: {len(all_photos)}")


if __name__ == '__main__':
    main()
