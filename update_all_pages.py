#!/usr/bin/env python3
"""Mass-update nav, footer, and remove sale banners across all MMD site pages."""
import re
import os
import glob

SITE_DIR = '/Users/alexhosage/Desktop/mmd-website'

SKIP_FILES = {
    'MMD_Marketing_Plan.html', 'MMD_Site_Report_Mar9.html',
    'file-matcher.html', 'ig-mothers-day.html'
}
SKIP_DIRS = {'_tmp', 'node_modules', 'docs', 'delivery', 'downloads'}

NEW_FOOTER = '''<footer class="footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <div class="footer-brand">Mrs<span>Millennial</span> Designs</div>
        <p class="footer-desc">Premium printable designs & event photo packages for life's biggest moments.</p>
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
        <h4>Services</h4>
        <ul class="footer-links">
          <li><a href="/photo-packages.html">Photo Packages</a></li>
          <li><a href="/wedding-photos.html">Wedding Photos</a></li>
          <li><a href="/event-photos.html">Event Photos</a></li>
        </ul>
      </div>
      <div>
        <h4>About</h4>
        <ul class="footer-links">
          <li><a href="/about.html">Our Story</a></li>
          <li><a href="/reviews.html">Reviews</a></li>
          <li><a href="/privacy.html">Privacy Policy</a></li>
          <li><a href="/contact.html">Contact</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">&copy; 2026 MrsMillennial Designs. All rights reserved.</div>
  </div>
</footer>'''

def get_active_page(filepath):
    """Determine which nav link should be active based on file path."""
    rel = os.path.relpath(filepath, SITE_DIR)
    basename = os.path.basename(rel)

    if basename == 'index.html':
        return '/'
    elif rel.startswith('products/') or basename == 'products.html':
        return '/products.html'
    elif rel.startswith('bundles/') or basename == 'bundles.html':
        return '/bundles.html'
    elif basename in ('photo-packages.html', 'wedding-photos.html', 'event-photos.html'):
        return '/photo-packages.html'
    elif basename in ('reviews.html', 'gallery.html'):
        return '/reviews.html'
    elif basename == 'about.html':
        return '/about.html'
    elif basename in ('contact.html', 'custom-orders.html'):
        return '/contact.html'
    return None

def build_nav(active_href):
    """Build new nav links with proper active class."""
    links = [
        ('/', 'Home'),
        ('/products.html', 'Shop'),
        ('/bundles.html', 'Bundles'),
        ('/photo-packages.html', 'Photo Packages'),
        ('/reviews.html', 'Reviews'),
        ('/about.html', 'About'),
        ('/contact.html', 'Contact'),
    ]
    items = []
    for href, label in links:
        cls = ' class="active"' if href == active_href else ''
        items.append(f'      <li><a href="{href}"{cls}>{label}</a></li>')
    return '<ul class="nav-links" id="navLinks">\n' + '\n'.join(items) + '\n    </ul>'

def process_file(filepath):
    """Process a single HTML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # 1. Replace nav links
    active = get_active_page(filepath)
    new_nav = build_nav(active)
    content = re.sub(
        r'<ul class="nav-links" id="navLinks">.*?</ul>',
        new_nav,
        content,
        flags=re.DOTALL
    )

    # 2. Replace footer
    content = re.sub(
        r'<footer class="footer">.*?</footer>',
        NEW_FOOTER,
        content,
        flags=re.DOTALL
    )

    # 3. Remove sale banners (md-banner divs)
    content = re.sub(
        r'\n*<div class="md-banner">.*?</div>\n*',
        '\n',
        content,
        flags=re.DOTALL
    )

    # 4. Remove inline md-banner styles from <head>
    content = re.sub(
        r'\s*<style>\s*\.md-banner\{.*?\}\s*</style>',
        '',
        content,
        flags=re.DOTALL
    )

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    # Collect all HTML files
    files = []

    # Root level
    for f in glob.glob(os.path.join(SITE_DIR, '*.html')):
        if os.path.basename(f) not in SKIP_FILES:
            files.append(f)

    # products/
    for f in glob.glob(os.path.join(SITE_DIR, 'products', '*.html')):
        files.append(f)

    # bundles/
    for f in glob.glob(os.path.join(SITE_DIR, 'bundles', '*.html')):
        files.append(f)

    updated = 0
    skipped = 0
    errors = []

    for filepath in sorted(files):
        try:
            if process_file(filepath):
                updated += 1
            else:
                skipped += 1
        except Exception as e:
            errors.append(f"{filepath}: {e}")

    print(f"Updated: {updated}")
    print(f"Skipped (no changes): {skipped}")
    print(f"Errors: {len(errors)}")
    for err in errors:
        print(f"  ERROR: {err}")

if __name__ == '__main__':
    main()
