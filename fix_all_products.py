#!/usr/bin/env python3
"""Fix all 144 product detail pages in the MrsMillennial Designs website."""

import json
import os
import re
import html

PRODUCTS_DIR = '/Users/alexhosage/Desktop/mmd-website/products'
LISTINGS_JSON = '/Users/alexhosage/Desktop/drea/scraper/output/listings-real.json'

# Boilerplate markers - strip description at these points
BOILERPLATE_MARKERS = [
    'HOW IT WORKS',
    'WHAT YOU RECEIVE',
    'PRINTING',
    'PLEASE NOTE',
    'LOOKING FOR SOMETHING ELSE',
    'Thank you for visiting',
]

# Back link HTML to insert before detail-grid
BACK_LINK_HTML = '''  <div class="back-link"><a href="/products.html"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5"/><path d="M12 19l-7-7 7-7"/></svg> Back to Shop</a></div>

'''


def load_listings():
    """Load listings from JSON, indexed by listing ID."""
    with open(LISTINGS_JSON, 'r') as f:
        data = json.load(f)
    return {str(d['listingId']): d for d in data}


def clean_description(desc):
    """Strip Etsy boilerplate from description text."""
    if not desc:
        return ''
    for marker in BOILERPLATE_MARKERS:
        idx = desc.find(marker)
        if idx != -1:
            desc = desc[:idx]
    # Clean up trailing whitespace/newlines
    desc = desc.rstrip()
    # Remove trailing lone characters (truncation artifacts)
    desc = re.sub(r'\n\s*\S?\s*$', '', desc)
    return desc


def make_meta_description(desc):
    """Create ~155 char meta description, trimmed to last full sentence."""
    # Strip newlines for meta
    text = desc.replace('\n', ' ').replace('\r', ' ')
    text = re.sub(r'\s+', ' ', text).strip()
    if len(text) <= 155:
        return html.escape(text, quote=True)
    # Trim to 155 chars
    trimmed = text[:155]
    # Find last sentence boundary
    for end in ['. ', '! ', '? ']:
        last = trimmed.rfind(end)
        if last > 60:  # Don't trim too short
            trimmed = trimmed[:last + 1]
            break
    else:
        # No sentence boundary found, trim to last space
        last_space = trimmed.rfind(' ')
        if last_space > 60:
            trimmed = trimmed[:last_space]
    return html.escape(trimmed.strip(), quote=True)


def desc_to_html(desc):
    """Convert plain text description to HTML with line breaks."""
    # Escape HTML entities
    text = html.escape(desc)
    # Convert newlines to <br>
    text = text.replace('\n', '<br>')
    # Clean up multiple <br> tags
    text = re.sub(r'(<br>){3,}', '<br><br>', text)
    return text


def fix_product_file(filepath, listings):
    """Apply all fixes to a single product HTML file."""
    listing_id = os.path.basename(filepath).replace('.html', '')

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # 1a. Fix <a>...</button> tag mismatch for buy-btn
    # Target: <a href="..." class="buy-btn" ...>...</button> -> </a>
    content = re.sub(
        r'(<a\s[^>]*class="buy-btn"[^>]*>.*?)</button>',
        r'\1</a>',
        content,
        flags=re.DOTALL
    )

    # 1b. Remove detail-tags section
    content = re.sub(
        r'\s*<div class="detail-tags">.*?</div>',
        '',
        content,
        flags=re.DOTALL
    )

    # 1c. Replace truncated descriptions with full text
    listing = listings.get(listing_id)
    if listing and listing.get('description'):
        clean_desc = clean_description(listing['description'])
        if clean_desc:
            # Replace detail-desc content
            desc_html = desc_to_html(clean_desc)
            content = re.sub(
                r'<div class="detail-desc">.*?</div>',
                f'<div class="detail-desc">{desc_html}</div>',
                content,
                flags=re.DOTALL
            )
            # Fix meta description
            meta_desc = make_meta_description(clean_desc)
            content = re.sub(
                r'<meta name="description" content="[^"]*">',
                f'<meta name="description" content="{meta_desc}">',
                content
            )

    # 1d. Add "Back to Shop" link before detail-grid (if not already present)
    if 'class="back-link"' not in content:
        content = content.replace(
            '  <div class="detail-grid">',
            BACK_LINK_HTML + '  <div class="detail-grid">'
        )

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def main():
    listings = load_listings()
    print(f"Loaded {len(listings)} listings from JSON")

    files = sorted(f for f in os.listdir(PRODUCTS_DIR) if f.endswith('.html'))
    print(f"Found {len(files)} product pages to fix")

    fixed = 0
    no_listing = 0
    for filename in files:
        filepath = os.path.join(PRODUCTS_DIR, filename)
        listing_id = filename.replace('.html', '')
        if listing_id not in listings:
            no_listing += 1
        if fix_product_file(filepath, listings):
            fixed += 1

    print(f"\nResults:")
    print(f"  Fixed: {fixed} files")
    print(f"  No listing data: {no_listing} files")
    print(f"  Total: {len(files)} files")


if __name__ == '__main__':
    main()
