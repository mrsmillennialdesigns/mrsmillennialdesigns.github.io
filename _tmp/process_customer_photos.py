#!/usr/bin/env python3
"""Process customer photos from organized folders into web-ready JPGs for product pages."""

import os
from PIL import Image

BASE = "/Users/alexhosage/Downloads/high res customer images "
OUT = "/Users/alexhosage/Desktop/mmd-website/img/customer-photos"

# Map folders to product IDs and exclude screenshot files
FOLDERS = {
    "wild flower": {
        "product_id": "4005425060",
        "exclude": ["IMG_6455.PNG", "IMG_6456.jpg"],  # listing screenshots
    },
    "other flower": {
        "product_id": "4760045018",
        "exclude": ["IMG_6453.PNG"],  # listing screenshot
    },
    "dad day": {
        "product_id": "7648273962",
        "exclude": ["IMG_6457.jpg"],  # listing screenshot
    },
}

MAX_SIZE = 800

def process_image(src_path, dst_path):
    """Convert to JPG, resize to max 800px, optimize."""
    img = Image.open(src_path)
    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')

    # Resize maintaining aspect ratio
    w, h = img.size
    if max(w, h) > MAX_SIZE:
        ratio = MAX_SIZE / max(w, h)
        img = img.resize((int(w * ratio), int(h * ratio)), Image.LANCZOS)

    img.save(dst_path, 'JPEG', quality=85, optimize=True)
    return img.size

os.makedirs(OUT, exist_ok=True)

results = {}
for folder_name, config in FOLDERS.items():
    pid = config["product_id"]
    exclude = set(config["exclude"])
    folder_path = os.path.join(BASE, folder_name)

    files = sorted([f for f in os.listdir(folder_path)
                     if f not in exclude and not f.startswith('.')])

    processed = []
    for i, fname in enumerate(files):
        src = os.path.join(folder_path, fname)
        # Name: {product_id}_customer_{index}.jpg
        dst_name = f"{pid}_customer_{i}.jpg"
        dst = os.path.join(OUT, dst_name)

        size = process_image(src, dst)
        processed.append(dst_name)
        print(f"  {fname} -> {dst_name} ({size[0]}x{size[1]})")

    results[pid] = processed
    print(f"\n{folder_name} ({pid}): {len(processed)} photos processed")

print("\n=== SUMMARY ===")
for pid, files in results.items():
    print(f"Product {pid}: {len(files)} customer photos")
    for f in files:
        print(f"  /img/customer-photos/{f}")
