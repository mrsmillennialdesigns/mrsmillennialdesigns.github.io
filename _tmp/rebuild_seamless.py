#!/usr/bin/env python3
"""
Rebuild seamless patterns for MrsMillennial Designs website.
- Generates _0, _1, _2 images for 15 new patterns
- Creates 15 product detail HTML pages
- Outputs products.html card snippets
"""

import os
import json
import shutil
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

SRC_DIR = '/Users/alexhosage/Downloads/seamless prints '
SITE_DIR = '/Users/alexhosage/Desktop/mmd-website'
IMG_DIR = os.path.join(SITE_DIR, 'img')
PRODUCTS_DIR = os.path.join(SITE_DIR, 'products')

# ─── Product definitions ───────────────────────────────────────
PRODUCTS = [
    {
        'id': '8800000030',
        'src': '084eaf58-8f91-436d-bd2a-1db8fbfd7033.jpg',
        'name': 'Watercolor Wildflower Garden',
        'title': 'Watercolor Wildflower Garden Seamless Pattern PNG | Pink Purple Floral Digital Paper',
        'search': 'watercolor wildflower garden seamless pattern png pink purple floral',
        'breadcrumb': 'Watercolor Wildflower Garden',
        'desc': 'Watercolor Wildflower Garden Seamless Pattern &ndash; Commercial Use Digital Paper<br><br>A stunning hand-painted watercolor garden of pink, purple, blue, and mauve wildflowers on a creamy white background. Delicate stems, leaves, and tiny berry accents create an elegant, flowing botanical design.<br><br>Perfect for nature lovers and anyone who adores romantic floral prints.',
        'use_cases': 'Wedding &amp; bridal stationery<br>Nursery &amp; bedroom wallpaper prints<br>Fabric &amp; textile design<br>Scrapbooking &amp; journaling<br>Gift wrap &amp; packaging<br>Print-on-demand products',
    },
    {
        'id': '8800000031',
        'src': '2613f0f7-f815-44fc-ad7f-50eaa479a09c.jpg',
        'name': 'Tiny Scattered Wildflower',
        'title': 'Tiny Scattered Wildflower Seamless Pattern PNG | Delicate Daisy Meadow Digital Paper',
        'search': 'tiny scattered wildflower seamless pattern png delicate daisy meadow',
        'breadcrumb': 'Tiny Scattered Wildflower',
        'desc': 'Tiny Scattered Wildflower Seamless Pattern &ndash; Commercial Use Digital Paper<br><br>A dainty meadow of tiny scattered wildflowers in pink, purple, blue, yellow, and peach tones. Each little bloom sits on a fine watercolor stem against a clean white background, creating a light and airy feel.<br><br>This gentle, ditsy floral is perfect for baby items, stationery, and light feminine designs.',
        'use_cases': 'Baby shower invitations &amp; decor<br>Stationery &amp; planner covers<br>Feminine branding &amp; packaging<br>Scrapbooking &amp; card making<br>Nursery fabric &amp; wallpaper<br>Print-on-demand products',
    },
    {
        'id': '8800000032',
        'src': '4207073b-cfb2-484f-8afa-f0d0dfb8a9b2.jpg',
        'name': 'Rainbow Watercolor Mermaid',
        'title': 'Rainbow Watercolor Mermaid Seamless Pattern PNG | Fantasy Kids Digital Paper',
        'search': 'rainbow watercolor mermaid seamless pattern png fantasy kids',
        'breadcrumb': 'Rainbow Watercolor Mermaid',
        'desc': 'Rainbow Watercolor Mermaid Seamless Pattern &ndash; Commercial Use Digital Paper<br><br>Vibrant rainbow-haired mermaids with stunning gradient tails in green, blue, purple, and pink watercolor splashes. Bold dripping paint effects and splatter details give this design an artistic, whimsical feel.<br><br>A magical design that kids and mermaid fans will absolutely love.',
        'use_cases': 'Mermaid birthday party supplies<br>Kids&rsquo; room &amp; bathroom decor<br>Pool party invitations<br>Children&rsquo;s fabric &amp; accessories<br>Scrapbooking &amp; sticker sheets<br>Print-on-demand products',
    },
    {
        'id': '8800000033',
        'src': '46c55267-cc01-4d2d-8e77-a920d74ce5a5.jpg',
        'name': 'Watercolor Oak Tree',
        'title': 'Watercolor Oak Tree Seamless Pattern PNG | Green Nature Forest Digital Paper',
        'search': 'watercolor oak tree seamless pattern png green nature forest',
        'breadcrumb': 'Watercolor Oak Tree',
        'desc': 'Watercolor Oak Tree Seamless Pattern &ndash; Commercial Use Digital Paper<br><br>Beautiful hand-painted watercolor oak trees with rich green foliage in varying shades from sage to deep forest green. Soft washes of light green create a dreamy, natural backdrop.<br><br>An elegant nature-inspired design perfect for nursery decor, eco-friendly branding, and woodland themes.',
        'use_cases': 'Woodland nursery decor<br>Eco-friendly branding &amp; packaging<br>Nature-themed stationery<br>Fabric &amp; home textiles<br>Scrapbooking &amp; journaling<br>Print-on-demand products',
    },
    {
        'id': '8800000034',
        'src': '51d7321e-0a97-4809-8267-1e64650b53eb.jpg',
        'name': 'Bee &amp; Spring Blossom',
        'title': 'Bee &amp; Spring Blossom Seamless Pattern PNG | Honey Bee Floral Digital Paper',
        'search': 'bee spring blossom seamless pattern png honey bee floral',
        'breadcrumb': 'Bee &amp; Spring Blossom',
        'desc': 'Bee &amp; Spring Blossom Seamless Pattern &ndash; Commercial Use Digital Paper<br><br>Cheerful honeybees buzzing among gorgeous pink, yellow, and white spring blossoms. Rich watercolor blooms in soft pink and butter yellow create a lively, garden-fresh feel.<br><br>A sweet, nature-inspired print perfect for spring projects, baby showers, and garden-themed crafts.',
        'use_cases': 'Spring baby shower supplies<br>Garden party invitations<br>Honey &amp; bee-themed branding<br>Kids&rsquo; room decor<br>Kitchen textiles &amp; accessories<br>Print-on-demand products',
    },
    {
        'id': '8800000035',
        'src': '5da048ee-ed93-49d5-b1bd-7dc3eb52306e.jpg',
        'name': 'Pink Princess Castle',
        'title': 'Pink Princess Castle Seamless Pattern PNG | Fairy Tale Nursery Digital Paper',
        'search': 'pink princess castle seamless pattern png fairy tale nursery',
        'breadcrumb': 'Pink Princess Castle',
        'desc': 'Pink Princess Castle Seamless Pattern &ndash; Commercial Use Digital Paper<br><br>Enchanting pink and purple fairytale castles with blue-purple pointed turrets, flags, and soft pink cloud backgrounds. A dreamy, storybook design with a warm, magical glow.<br><br>Perfect for princess-themed parties, nursery decor, and little girls who dream of fairy tales.',
        'use_cases': 'Princess birthday parties<br>Girls&rsquo; nursery wallpaper<br>Fairy tale stationery<br>Children&rsquo;s fabric &amp; clothing<br>Party favor packaging<br>Print-on-demand products',
    },
    {
        'id': '8800000036',
        'src': '673fc9a0-6983-4dc3-baf3-51c3e21979c7.jpg',
        'name': 'Watercolor Fairy Tale Castle',
        'title': 'Watercolor Fairy Tale Castle Seamless Pattern PNG | Dreamy Fantasy Digital Paper',
        'search': 'watercolor fairy tale castle seamless pattern png dreamy fantasy',
        'breadcrumb': 'Watercolor Fairy Tale Castle',
        'desc': 'Watercolor Fairy Tale Castle Seamless Pattern &ndash; Commercial Use Digital Paper<br><br>A dreamy watercolor castle in soft pink and blue tones with pointed blue turrets, pathway bridges, and fluffy clouds on a white background. Whimsical and enchanting.<br><br>Ideal for princess party supplies, fantasy story illustrations, and magical nursery themes.',
        'use_cases': 'Fantasy-themed nursery decor<br>Fairy tale party supplies<br>Storybook illustrations<br>Kids&rsquo; fabric &amp; accessories<br>Scrapbooking &amp; card making<br>Print-on-demand products',
    },
    {
        'id': '8800000037',
        'src': '9900a335-0056-4c82-b442-2a76412c0d85.jpg',
        'name': 'Honey Bee &amp; Wildflower',
        'title': 'Honey Bee &amp; Wildflower Seamless Pattern PNG | Summer Garden Digital Paper',
        'search': 'honey bee wildflower seamless pattern png summer garden',
        'breadcrumb': 'Honey Bee &amp; Wildflower',
        'desc': 'Honey Bee &amp; Wildflower Seamless Pattern &ndash; Commercial Use Digital Paper<br><br>Golden honeybees dancing among sunflowers, daisies, and colorful wildflowers in warm yellow, orange, pink, and teal watercolor splashes. A sunny, summer garden feel with artistic paint drip details.<br><br>Bring the warmth of summer to any project &ndash; perfect for garden themes, honey branding, and cheerful kids&rsquo; products.',
        'use_cases': 'Summer party &amp; picnic supplies<br>Honey &amp; farmhouse branding<br>Garden-themed stationery<br>Kitchen decor &amp; textiles<br>Kids&rsquo; craft projects<br>Print-on-demand products',
    },
    {
        'id': '8800000038',
        'src': '9e9156e3-dabb-419d-acbc-9a73a6caca3d.jpg',
        'name': 'Blue Sky Castle Kingdom',
        'title': 'Blue Sky Castle Kingdom Seamless Pattern PNG | Cloud Kingdom Kids Digital Paper',
        'search': 'blue sky castle kingdom seamless pattern png cloud kingdom kids',
        'breadcrumb': 'Blue Sky Castle Kingdom',
        'desc': 'Blue Sky Castle Kingdom Seamless Pattern &ndash; Commercial Use Digital Paper<br><br>Majestic blue castles with golden-tipped turrets floating among fluffy white clouds in a bright blue sky. A grand, regal design with beautiful detail and depth.<br><br>Perfect for boys&rsquo; room decor, adventure themes, and fantasy story projects.',
        'use_cases': 'Boys&rsquo; nursery &amp; bedroom decor<br>Adventure-themed party supplies<br>Fantasy storybook illustrations<br>Kids&rsquo; fabric &amp; clothing<br>Scrapbooking &amp; journaling<br>Print-on-demand products',
    },
    {
        'id': '8800000039',
        'src': '9f21ae46-9feb-4100-9c5a-7b42dd1c565e.jpg',
        'name': 'Watercolor Forest Grove',
        'title': 'Watercolor Forest Grove Seamless Pattern PNG | Green Trees Nature Digital Paper',
        'search': 'watercolor forest grove seamless pattern png green trees nature',
        'breadcrumb': 'Watercolor Forest Grove',
        'desc': 'Watercolor Forest Grove Seamless Pattern &ndash; Commercial Use Digital Paper<br><br>Elegant watercolor trees in rich deep greens, from dark forest to light sage, creating a layered woodland canopy. Each tree has beautiful organic shapes with varied foliage styles.<br><br>A sophisticated nature print perfect for rustic decor, woodland nurseries, and outdoor-themed designs.',
        'use_cases': 'Woodland nursery decor<br>Rustic wedding stationery<br>Nature-themed branding<br>Home textiles &amp; wallpaper<br>Outdoor adventure crafts<br>Print-on-demand products',
    },
    {
        'id': '8800000040',
        'src': 'abe964f8-f56b-40e5-92b3-907c6a587001.jpg',
        'name': 'Kids Affirmations',
        'title': 'Kids Affirmations Seamless Pattern PNG | I Am Brave Smart Kind Positive Words Digital Paper',
        'search': 'kids affirmations seamless pattern png i am brave smart kind positive words',
        'breadcrumb': 'Kids Affirmations',
        'desc': 'Kids Affirmations Seamless Pattern &ndash; Commercial Use Digital Paper<br><br>Uplifting positive affirmations in soft pastel rainbow colors &ndash; &ldquo;I Am Smart,&rdquo; &ldquo;I Am Wonderful,&rdquo; &ldquo;I Am Kind,&rdquo; &ldquo;I Am Brave,&rdquo; &ldquo;I Am Loved,&rdquo; &ldquo;I Am Strong,&rdquo; &ldquo;I Am Unique,&rdquo; and &ldquo;I Am Enough&rdquo; on a warm cream background.<br><br>A meaningful, empowering design for kids&rsquo; rooms, school supplies, and inspirational products that help children build confidence.',
        'use_cases': 'Kids&rsquo; room wall art &amp; decor<br>School supplies &amp; folders<br>Inspirational gift wrap<br>Children&rsquo;s clothing &amp; accessories<br>Therapy &amp; counseling materials<br>Print-on-demand products',
    },
    {
        'id': '8800000041',
        'src': 'b8bbee3a-f6a9-434a-9f38-35b1db028d6d.jpg',
        'name': 'Mauve Botanical Wildflower',
        'title': 'Mauve Botanical Wildflower Seamless Pattern PNG | Dusty Rose Floral Digital Paper',
        'search': 'mauve botanical wildflower seamless pattern png dusty rose floral',
        'breadcrumb': 'Mauve Botanical Wildflower',
        'desc': 'Mauve Botanical Wildflower Seamless Pattern &ndash; Commercial Use Digital Paper<br><br>Stunning dusty rose and mauve wildflowers with delicate line art details on a creamy white background. Beautiful botanical illustrations with soft pink, plum, and olive green tones create an elegant, vintage feel.<br><br>Perfect for wedding stationery, feminine branding, and sophisticated home decor projects.',
        'use_cases': 'Wedding &amp; bridal stationery<br>Feminine brand packaging<br>Vintage-style home decor<br>Journaling &amp; planner design<br>Fabric &amp; textile prints<br>Print-on-demand products',
    },
    {
        'id': '8800000042',
        'src': 'befa0169-2e2a-4c1a-bd4e-1776edb98e6b.jpg',
        'name': 'Pink Castle &amp; Clouds',
        'title': 'Pink Castle &amp; Clouds Seamless Pattern PNG | Princess Nursery Digital Paper',
        'search': 'pink castle clouds seamless pattern png princess nursery',
        'breadcrumb': 'Pink Castle &amp; Clouds',
        'desc': 'Pink Castle &amp; Clouds Seamless Pattern &ndash; Commercial Use Digital Paper<br><br>Beautiful pink and lavender fairy tale castles with blue-purple turrets and tiny floral accents, set against soft pink clouds. A sweet, enchanted design with a storybook feel.<br><br>Ideal for princess nursery decor, birthday party supplies, and girly craft projects.',
        'use_cases': 'Princess nursery wallpaper<br>Birthday party supplies<br>Girls&rsquo; clothing &amp; accessories<br>Fairy tale stationery<br>Scrapbooking &amp; card making<br>Print-on-demand products',
    },
    {
        'id': '8800000043',
        'src': 'ea275f3a-c896-4d3a-a162-b1b660ec2efc.jpg',
        'name': 'Rainbow Mermaid Splash',
        'title': 'Rainbow Mermaid Splash Seamless Pattern PNG | Vibrant Watercolor Kids Digital Paper',
        'search': 'rainbow mermaid splash seamless pattern png vibrant watercolor kids',
        'breadcrumb': 'Rainbow Mermaid Splash',
        'desc': 'Rainbow Mermaid Splash Seamless Pattern &ndash; Commercial Use Digital Paper<br><br>Bold, vibrant rainbow mermaids swimming through explosive watercolor splashes of red, orange, yellow, green, blue, and purple. An abstract, artistic style with incredible color saturation and energy.<br><br>A show-stopping design for mermaid lovers, kids&rsquo; products, and anyone who loves bold, colorful art.',
        'use_cases': 'Mermaid-themed birthday parties<br>Kids&rsquo; swimwear &amp; beach accessories<br>Vibrant room decor<br>Pool party invitations<br>Art-inspired stationery<br>Print-on-demand products',
    },
    {
        'id': '8800000044',
        'src': 'f6e477a0-fb5f-4fcc-b077-4ff3fce6a630.jpg',
        'name': 'Cottage Garden Wildflower',
        'title': 'Cottage Garden Wildflower Seamless Pattern PNG | Daisy &amp; Poppy Digital Paper',
        'search': 'cottage garden wildflower seamless pattern png daisy poppy',
        'breadcrumb': 'Cottage Garden Wildflower',
        'desc': 'Cottage Garden Wildflower Seamless Pattern &ndash; Commercial Use Digital Paper<br><br>A charming cottage garden with white daisies, blue cornflowers, golden poppies, and soft pink blooms nestled among sage green and blue-gray leaves. Rich, detailed illustration with a vintage botanical feel.<br><br>Perfect for farmhouse decor, wedding invitations, and classic floral craft projects.',
        'use_cases': 'Farmhouse &amp; cottage decor<br>Wedding invitations &amp; stationery<br>Kitchen textiles &amp; accessories<br>Vintage-style gift wrap<br>Scrapbooking &amp; journaling<br>Print-on-demand products',
    },
]

# Old seamless product IDs to delete
OLD_IDS = [
    '8800000002', '8800000004', '8800000005', '8800000008',
    '8800000010', '8800000011', '8800000012', '8800000013',
    '8800000014', '8800000015', '8800000016', '8800000017',
    '8800000018', '8800000019', '8800000020', '8800000021',
    '8800000022', '8800000023', '8800000024', '8800000025',
]


def create_square_crop(img, size=800):
    """Center-crop to square, then resize."""
    w, h = img.size
    s = min(w, h)
    left = (w - s) // 2
    top = (h - s) // 2
    cropped = img.crop((left, top, left + s, top + s))
    return cropped.resize((size, size), Image.LANCZOS)


def create_tiled_preview(img, size=800):
    """Create a 3x3 tiled preview to show seamless repeat."""
    # Use a square tile from the image
    w, h = img.size
    s = min(w, h)
    left = (w - s) // 2
    top = (h - s) // 2
    tile = img.crop((left, top, left + s, top + s))

    # Resize tile for 3x3 grid
    tile_size = size // 3
    tile = tile.resize((tile_size, tile_size), Image.LANCZOS)

    # Create 3x3 tiled image
    tiled = Image.new('RGB', (size, size), (255, 255, 255))
    for row in range(3):
        for col in range(3):
            tiled.paste(tile, (col * tile_size, row * tile_size))

    return tiled


def create_mockup(img, size=800):
    """Create a fabric swatch mockup with the pattern."""
    w, h = img.size

    # Create background (soft cream/gray)
    bg = Image.new('RGB', (size, size), (245, 242, 237))

    # Create pattern swatch (slightly smaller, centered)
    swatch_size = int(size * 0.72)
    margin = (size - swatch_size) // 2

    # Tile the pattern for the swatch
    s = min(w, h)
    left = (w - s) // 2
    top = (h - s) // 2
    tile = img.crop((left, top, left + s, top + s))
    tile_unit = swatch_size // 2
    tile = tile.resize((tile_unit, tile_unit), Image.LANCZOS)

    swatch = Image.new('RGB', (swatch_size, swatch_size), (255, 255, 255))
    for row in range(2):
        for col in range(2):
            swatch.paste(tile, (col * tile_unit, row * tile_unit))

    # Add subtle shadow behind swatch
    shadow = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_offset = 6
    shadow_draw.rectangle(
        [margin + shadow_offset, margin + shadow_offset,
         margin + swatch_size + shadow_offset, margin + swatch_size + shadow_offset],
        fill=(0, 0, 0, 40)
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=12))

    # Composite shadow onto bg
    bg_rgba = bg.convert('RGBA')
    bg_rgba = Image.alpha_composite(bg_rgba, shadow)
    bg = bg_rgba.convert('RGB')

    # Add thin border around swatch
    draw = ImageDraw.Draw(swatch)
    draw.rectangle([0, 0, swatch_size-1, swatch_size-1], outline=(220, 215, 210), width=2)

    # Paste swatch onto background
    bg.paste(swatch, (margin, margin))

    # Add subtle "fabric texture" label area at bottom
    draw_bg = ImageDraw.Draw(bg)
    label_y = margin + swatch_size + 12
    # Small decorative line
    line_w = 60
    line_x = (size - line_w) // 2
    draw_bg.line([(line_x, label_y), (line_x + line_w, label_y)], fill=(200, 195, 190), width=1)

    return bg


def generate_images():
    """Generate _0, _1, _2 images for all products."""
    print("Generating images...")
    for p in PRODUCTS:
        src_path = os.path.join(SRC_DIR, p['src'])
        img = Image.open(src_path).convert('RGB')

        # _0: Square crop (main/card image)
        img0 = create_square_crop(img, 800)
        img0.save(os.path.join(IMG_DIR, f"{p['id']}_0.jpg"), 'JPEG', quality=90)

        # _1: Tiled preview
        img1 = create_tiled_preview(img, 800)
        img1.save(os.path.join(IMG_DIR, f"{p['id']}_1.jpg"), 'JPEG', quality=90)

        # _2: Mockup
        img2 = create_mockup(img, 800)
        img2.save(os.path.join(IMG_DIR, f"{p['id']}_2.jpg"), 'JPEG', quality=90)

        # Also save high-res PNG pattern file
        patterns_dir = os.path.join(IMG_DIR, 'patterns')
        os.makedirs(patterns_dir, exist_ok=True)
        # Resize source to 3600x3600 square for high-res download
        img_hires = create_square_crop(img, 3600)
        img_hires.save(os.path.join(patterns_dir, f"{p['id']}-clean.png"), 'PNG')

        print(f"  ✓ {p['id']} - {p['name']}")

    print(f"\nGenerated images for {len(PRODUCTS)} products.")


def delete_old_products():
    """Remove old seamless pattern files."""
    print("\nDeleting old seamless products...")
    deleted = 0

    for old_id in OLD_IDS:
        # Delete product HTML
        html_path = os.path.join(PRODUCTS_DIR, f"{old_id}.html")
        if os.path.exists(html_path):
            os.remove(html_path)
            deleted += 1

        # Delete images
        for suffix in ['_0.jpg', '_1.jpg', '_2.jpg']:
            img_path = os.path.join(IMG_DIR, f"{old_id}{suffix}")
            if os.path.exists(img_path):
                os.remove(img_path)

        # Delete high-res pattern
        pattern_path = os.path.join(IMG_DIR, 'patterns', f"{old_id}-clean.png")
        if os.path.exists(pattern_path):
            os.remove(pattern_path)

    print(f"  Deleted {deleted} old product pages and their images.")


def generate_product_html(p, all_products):
    """Generate a product detail HTML page."""
    # Pick 4 related products (not self)
    related = [r for r in all_products if r['id'] != p['id']]
    # Rotate related based on position
    idx = all_products.index(p)
    related = related[idx % len(related):] + related[:idx % len(related)]
    related = related[:4]

    related_html = ''
    for r in related:
        r_name_safe = r['name'].replace('&amp;', '&amp;')
        related_html += f'''      <a href="/products/{r['id']}.html" class="product-card">
            <div class="card-img"><img src="/img/{r['id']}_0.jpg" alt="{r['name']} Seamless Pattern" loading="lazy"></div>
            <div class="card-body">
              <h3>{r['name']} Seamless Pattern</h3>
              <div class="card-price">$2.00</div>
            </div>
          </a>
'''

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{p['title']} | Commercial Use Background | MrsMillennial Designs</title>
  <meta name="description" content="{p['name']} Seamless Pattern PNG - High-resolution seamless pattern for fabric, stationery &amp; POD. Commercial use included.">
  <meta property="og:title" content="{p['title']} | Commercial Use Background">
  <meta property="og:image" content="https://mrsmillennialdesigns.com/img/{p['id']}_0.jpg">
  <meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' https://i.etsystatic.com data:; font-src 'self'; connect-src 'self' https://mmd-review-counter.mrsmillennial.workers.dev;">
  <meta http-equiv="X-Content-Type-Options" content="nosniff">
  <meta name="referrer" content="strict-origin-when-cross-origin">
  <link rel="stylesheet" href="/css/style.css">
  <script src="/js/review-count.js" defer></script>
</head>
<body>

<nav class="nav" id="mainNav">
  <div class="nav-inner">
    <a href="/" class="nav-logo">Mrs<span>Millennial</span> Designs</a>
    <ul class="nav-links" id="navLinks">
      <li><a href="/">Home</a></li>
      <li><a href="/products.html" class="active">Shop</a></li>
      <li><a href="/bundles.html">Bundles</a></li>
      <li><a href="/reviews.html">Reviews</a></li>
      <li><a href="/about.html">About</a></li>
      <li><a href="/contact.html">Contact</a></li>
    </ul>
    <button class="nav-toggle" id="navToggle" aria-label="Menu">
      <span></span><span></span><span></span>
    </button>
  </div>
</nav>

<div class="container">
  <div class="breadcrumb">
    <a href="/">Home</a> <span class="sep">/</span>
    <a href="/products.html">Shop</a> <span class="sep">/</span>
    <a href="/products.html?cat=seamless">Seamless Patterns</a> <span class="sep">/</span>
    <span>{p['breadcrumb']}</span>
  </div>

  <div class="back-link"><a href="/products.html"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5"/><path d="M12 19l-7-7 7-7"/></svg> Back to Shop</a></div>

  <div class="detail-grid">
    <div class="detail-images">
      <div class="detail-main"><img src="/img/{p['id']}_0.jpg" alt="{p['title']} | Commercial Use Background" id="mainImg" class="detail-main-img"></div>
      <div class="detail-thumbs"><img src="/img/{p['id']}_0.jpg" alt="Pattern" class="thumb active" onclick="document.getElementById('mainImg').src='/img/{p['id']}_0.jpg';document.querySelectorAll('.thumb').forEach(t=>t.classList.remove('active'));this.classList.add('active')"><img src="/img/{p['id']}_1.jpg" alt="Tiled Preview" class="thumb" onclick="document.getElementById('mainImg').src='/img/{p['id']}_1.jpg';document.querySelectorAll('.thumb').forEach(t=>t.classList.remove('active'));this.classList.add('active')"><img src="/img/{p['id']}_2.jpg" alt="Mockup" class="thumb" onclick="document.getElementById('mainImg').src='/img/{p['id']}_2.jpg';document.querySelectorAll('.thumb').forEach(t=>t.classList.remove('active'));this.classList.add('active')"></div>
    </div>
    <div class="detail-info">
      <span class="badge badge-seamless">Seamless Patterns</span>
      <h1>{p['title']} | Commercial Use Background</h1>
      <div class="detail-price">$2.00</div>
      <div class="detail-meta">
        <div class="meta-item">Instant digital download</div>
        <div class="meta-item">PNG &amp; JPEG formats</div>
        <div class="meta-item">Commercial use included</div>
      </div>
      <div class="buy-section">
        <a href="#" class="buy-btn" onclick="alert('Stripe payment link coming soon! Email mrsmillennialdesigns@outlook.com to purchase.');return false;">
          <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg>
          Buy Now &mdash; $2.00
        </a>
        <div class="buy-secure">
          <svg viewBox="0 0 24 24"><path d="M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zm-6 9c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zm3.1-9H8.9V6c0-1.71 1.39-3.1 3.1-3.1 1.71 0 3.1 1.39 3.1 3.1v2z"/></svg>
          Secure checkout powered by Stripe
        </div>
      </div>
      <div class="detail-desc">{p['desc']}<br><br>&#127775; Perfect For:<br>{p['use_cases']}<br><br>&#128229; What You&#8217;ll Receive:<br>1 High-Resolution PNG File<br>1 High-Resolution JPEG File<br>Seamless / Repeat Pattern<br>Commercial Use Included<br>Instant Digital Download<br><br>&#128196; License Summary:<br>&#10004; Personal use<br>&#10004; Small business commercial use<br>&#10008; No reselling or sharing the digital file<br>&#10008; No redistribution as a standalone design<br><br>This artwork was created with the assistance of AI tools and thoughtfully refined by the designer, Mrs. Millennial Designs.<br>All designs remain original and copyright protected.</div>
    </div>
  </div>

  <div class="etsy-notice">
    <div class="etsy-notice-inner">
      <div class="etsy-notice-heart">&#10084;</div>
      <h3>You're supporting a real family</h3>
      <p>When you buy here, <strong>100% of your purchase</strong> goes directly to our small business &mdash; no marketplace fees, no middleman. Thank you for shopping with us!</p>
    </div>
  </div>

  <div class="related-section">
    <h2>You Might Also Like</h2>
    <div class="product-grid">
{related_html}    </div>
  </div>
</div>

<footer class="footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <div class="footer-brand">Mrs<span>Millennial</span> Designs</div>
        <p class="footer-desc">Handmade digital art &amp; printable keepsakes crafted with love by Andrea.</p>
        <p class="footer-stats"><a href="/reviews.html" style="color:rgba(255,255,255,0.5)">777 reviews</a> &middot; 5.0 avg rating</p>
      </div>
      <div>
        <h4>Shop</h4>
        <ul class="footer-links">
          <li><a href="/products.html">All Products</a></li>
          <li><a href="/bundles.html">Bundles</a></li>
          <li><a href="/custom-orders.html">Custom Orders</a></li>
        </ul>
      </div>
      <div>
        <h4>Help</h4>
        <ul class="footer-links">
          <li><a href="/contact.html">Contact Us</a></li>
          <li><a href="/about.html">Our Story</a></li>
          <li><a href="/reviews.html">Reviews</a></li>
          <li><a href="/privacy.html">Privacy Policy</a></li>
          <li><a href="/terms.html">Terms of Service</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">&copy; 2026 MrsMillennial Designs. All rights reserved.</div>
  </div>
</footer>
<script>
const n=document.getElementById('mainNav');
window.addEventListener('scroll',()=>n.classList.toggle('scrolled',scrollY>20));
const t=document.getElementById('navToggle'),l=document.getElementById('navLinks');
t.addEventListener('click',()=>l.classList.toggle('open'));
l.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>l.classList.remove('open')));
</script>

<script>
(function(){{
  var endpoint='/a/track';
  function t(data){{
    data.referrer=document.referrer||'';
    data.page=location.pathname;
    navigator.sendBeacon?navigator.sendBeacon(endpoint,JSON.stringify(data)):
    fetch(endpoint,{{method:'POST',body:JSON.stringify(data),keepalive:true}});
  }}
  t({{event:'pageview'}});
  if(location.pathname.startsWith('/products/')&&location.pathname.endsWith('.html')){{
    var id=location.pathname.split('/').pop().replace('.html','');
    var h1=document.querySelector('h1');
    var price=document.querySelector('.detail-price');
    t({{event:'product_view',productId:id,productTitle:h1?h1.textContent.slice(0,60):'',productPrice:price?price.textContent:''}});
  }}
  document.addEventListener('click',function(e){{
    var btn=e.target.closest('.buy-btn');
    if(!btn)return;
    var id=location.pathname.split('/').pop().replace('.html','');
    var price=document.querySelector('.detail-price');
    t({{event:'buy_click',productId:id,productPrice:price?price.textContent:''}});
  }});
}})();
</script>
</body>
</html>'''


def generate_product_pages():
    """Generate all 15 product HTML pages."""
    print("\nGenerating product pages...")
    for p in PRODUCTS:
        html = generate_product_html(p, PRODUCTS)
        path = os.path.join(PRODUCTS_DIR, f"{p['id']}.html")
        with open(path, 'w') as f:
            f.write(html)
        print(f"  ✓ {p['id']}.html - {p['name']}")
    print(f"\nGenerated {len(PRODUCTS)} product pages.")


def generate_products_html_cards():
    """Output the product card HTML to paste into products.html."""
    print("\n\n═══ PRODUCTS.HTML CARD SNIPPETS ═══")
    print("(Replace old seamless cards with these)\n")

    cards = []
    for p in PRODUCTS:
        card = f'''      <a href="/products/{p['id']}.html" class="product-card" data-cat="seamless" data-title="{p['search']}">
        <div class="card-img"><img src="/img/{p['id']}_0.jpg" alt="{p['name']} Seamless Pattern PNG" loading="lazy"></div>
        <div class="card-body">
          <span class="badge badge-seamless">Seamless Patterns</span>
          <h3>{p['title']}</h3>
          <div class="card-price">$2.00</div>
        </div>
      </a>'''
        cards.append(card)

    print('\n'.join(cards))

    # Save to file for easy copy
    with open(os.path.join(SITE_DIR, '_tmp', 'seamless_cards.html'), 'w') as f:
        f.write('\n'.join(cards))
    print(f"\n\nSaved to _tmp/seamless_cards.html")


def update_stripe_links():
    """Update stripe-links.json with new product entries."""
    stripe_path = os.path.join(SITE_DIR, 'stripe-links.json')
    with open(stripe_path, 'r') as f:
        data = json.load(f)

    # Remove old seamless IDs
    for old_id in OLD_IDS:
        if old_id in data:
            del data[old_id]

    # Also remove IDs 8800000001, 8800000003, 8800000006, 8800000007 (old seamless not on site)
    for extra_id in ['8800000001', '8800000003', '8800000006', '8800000007', '8800000009']:
        if extra_id in data:
            del data[extra_id]

    # Add new seamless IDs
    for p in PRODUCTS:
        data[p['id']] = {
            "productId": "",
            "priceId": "",
            "paymentUrl": "",
            "title": f"{p['title']} | Commercial Use Background",
            "price": 2.0,
            "sku": ""
        }

    with open(stripe_path, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"\nUpdated stripe-links.json: removed {len(OLD_IDS)} old, added {len(PRODUCTS)} new.")


if __name__ == '__main__':
    print("=" * 60)
    print("REBUILDING SEAMLESS PATTERNS")
    print("=" * 60)

    # Step 1: Delete old products
    delete_old_products()

    # Step 2: Generate new images
    generate_images()

    # Step 3: Generate product pages
    generate_product_pages()

    # Step 4: Output card snippets for products.html
    generate_products_html_cards()

    # Step 5: Update stripe links
    update_stripe_links()

    print("\n" + "=" * 60)
    print("DONE! Next steps:")
    print("1. Update products.html - replace old seamless cards with _tmp/seamless_cards.html")
    print("2. Update index.html - change '24 designs' to '15 designs'")
    print("3. Update filter button count in products.html")
    print("=" * 60)
