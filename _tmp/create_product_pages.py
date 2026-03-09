#!/usr/bin/env python3
"""Create product HTML pages for the 8 new seamless patterns."""

import os
import html

OUTPUT_DIR = '/Users/alexhosage/Desktop/mmd-website/products'

PATTERNS = [
    {
        'id': '8800000001',
        'slug': 'pastel-hearts-seamless-pattern',
        'title': 'Pastel Watercolor Hearts Seamless Pattern PNG | Valentine Digital Paper | Commercial Use Background',
        'short_title': 'Pastel Watercolor Hearts Seamless Pattern',
        'desc_emoji': '💕',
        'desc_intro': 'Add a sweet, romantic touch to your products with this pastel watercolor hearts seamless pattern featuring delicate heart shapes in soft pink, lavender, mint, peach, and baby blue tones.',
        'desc_perfect': 'Valentine\'s Day products &amp; cards\nWedding stationery &amp; invitations\nBaby shower &amp; nursery decor\nScrapbooking &amp; printable paper\nFabric &amp; textile design\nGift wrap &amp; packaging\nPrint-on-demand products',
        'meta_desc': 'Pastel watercolor hearts seamless pattern PNG. Sweet valentine digital paper for crafts, scrapbooking, fabric design & POD. Commercial use included.',
    },
    {
        'id': '8800000002',
        'slug': 'spring-wildflower-seamless-pattern',
        'title': 'Spring Wildflower Seamless Pattern PNG | Watercolor Floral Digital Paper | Commercial Use Background',
        'short_title': 'Spring Wildflower Seamless Pattern',
        'desc_emoji': '🌸',
        'desc_intro': 'Brighten your designs with this cheerful spring wildflower seamless pattern featuring colorful watercolor blooms in pink, yellow, blue, coral, and lavender with golden centers.',
        'desc_perfect': 'Spring &amp; Mother\'s Day products\nFloral fabric &amp; textile design\nStationery &amp; greeting cards\nScrapbooking &amp; journaling\nNursery &amp; kids room decor\nGift wrap &amp; packaging\nPrint-on-demand products',
        'meta_desc': 'Spring wildflower seamless pattern PNG. Colorful watercolor floral digital paper for crafts, fabric design & POD. Commercial use included.',
    },
    {
        'id': '8800000003',
        'slug': 'autumn-leaves-seamless-pattern',
        'title': 'Autumn Leaves & Berries Seamless Pattern PNG | Fall Watercolor Digital Paper | Commercial Use Background',
        'short_title': 'Autumn Leaves & Berries Seamless Pattern',
        'desc_emoji': '🍂',
        'desc_intro': 'Wrap your products in warm autumn vibes with this fall leaves seamless pattern featuring watercolor maple leaves, simple leaves, and berry clusters in rich burnt orange, rust, gold, and amber tones.',
        'desc_perfect': 'Fall &amp; Thanksgiving products\nAutumn fabric &amp; textile design\nSeasonal stationery &amp; cards\nScrapbooking &amp; printable paper\nHome decor &amp; table settings\nGift wrap &amp; packaging\nPrint-on-demand products',
        'meta_desc': 'Autumn leaves and berries seamless pattern PNG. Warm fall watercolor digital paper for crafts, scrapbooking & POD. Commercial use included.',
    },
    {
        'id': '8800000004',
        'slug': 'celestial-stars-seamless-pattern',
        'title': 'Celestial Stars & Moons Seamless Pattern PNG | Nursery Digital Paper | Commercial Use Background',
        'short_title': 'Celestial Stars & Moons Seamless Pattern',
        'desc_emoji': '✨',
        'desc_intro': 'Create dreamy designs with this celestial seamless pattern featuring soft watercolor stars and crescent moons in warm gold, baby blue, peach, and lavender tones.',
        'desc_perfect': 'Nursery &amp; baby shower decor\nKids room wallpaper &amp; fabric\nSpace-themed party supplies\nBedding &amp; apparel design\nScrapbooking &amp; stationery\nGift wrap &amp; packaging\nPrint-on-demand products',
        'meta_desc': 'Celestial stars and moons seamless pattern PNG. Dreamy nursery digital paper for crafts, fabric design & POD. Commercial use included.',
    },
    {
        'id': '8800000005',
        'slug': 'watercolor-butterfly-seamless-pattern',
        'title': 'Watercolor Butterfly Seamless Pattern PNG | Spring Digital Paper | Commercial Use Background',
        'short_title': 'Watercolor Butterfly Seamless Pattern',
        'desc_emoji': '🦋',
        'desc_intro': 'Flutter into beautiful designs with this delicate butterfly seamless pattern featuring soft watercolor butterflies in sky blue, pink, lilac, golden, and mint tones.',
        'desc_perfect': 'Spring &amp; summer products\nGarden party supplies\nFabric &amp; textile design\nStationery &amp; greeting cards\nNursery &amp; girls room decor\nGift wrap &amp; packaging\nPrint-on-demand products',
        'meta_desc': 'Watercolor butterfly seamless pattern PNG. Delicate spring digital paper for crafts, fabric design & POD. Commercial use included.',
    },
    {
        'id': '8800000006',
        'slug': 'lucky-shamrock-seamless-pattern',
        'title': 'Lucky Shamrock Seamless Pattern PNG | St. Patrick\'s Day Digital Paper | Commercial Use Background',
        'short_title': 'Lucky Shamrock Seamless Pattern',
        'desc_emoji': '☘️',
        'desc_intro': 'Get lucky with this charming shamrock seamless pattern featuring watercolor three-leaf clovers in rich green tones — perfect for St. Patrick\'s Day and Irish-themed designs.',
        'desc_perfect': 'St. Patrick\'s Day products\nIrish-themed party supplies\nFabric &amp; textile design\nStationery &amp; greeting cards\nScrapbooking &amp; printable paper\nGift wrap &amp; packaging\nPrint-on-demand products',
        'meta_desc': 'Lucky shamrock seamless pattern PNG. Green watercolor clover digital paper for St. Patrick\'s Day crafts & POD. Commercial use included.',
    },
    {
        'id': '8800000007',
        'slug': 'winter-snowflake-seamless-pattern',
        'title': 'Winter Snowflake Seamless Pattern PNG | Christmas Holiday Digital Paper | Commercial Use Background',
        'short_title': 'Winter Snowflake Seamless Pattern',
        'desc_emoji': '❄️',
        'desc_intro': 'Add a frosty touch to your holiday designs with this winter snowflake seamless pattern featuring intricate crystalline snowflakes in soft icy blue watercolor tones.',
        'desc_perfect': 'Christmas &amp; holiday products\nWinter party supplies &amp; decor\nFabric &amp; textile design\nStationery &amp; greeting cards\nGift wrap &amp; packaging\nSublimation &amp; apparel\nPrint-on-demand products',
        'meta_desc': 'Winter snowflake seamless pattern PNG. Icy blue Christmas digital paper for holiday crafts & POD. Commercial use included.',
    },
    {
        'id': '8800000008',
        'slug': 'pastel-polka-dot-seamless-pattern',
        'title': 'Pastel Polka Dot Seamless Pattern PNG | Watercolor Dot Digital Paper | Commercial Use Background',
        'short_title': 'Pastel Polka Dot Seamless Pattern',
        'desc_emoji': '🎨',
        'desc_intro': 'A timeless classic reimagined — this pastel polka dot seamless pattern features soft watercolor circles with tiny heart details in rose, blue, lavender, mint, peach, and cream.',
        'desc_perfect': 'Baby shower &amp; nursery decor\nBirthday party supplies\nFabric &amp; textile design\nStationery &amp; invitations\nScrapbooking &amp; printable paper\nGift wrap &amp; packaging\nPrint-on-demand products',
        'meta_desc': 'Pastel polka dot seamless pattern PNG. Watercolor dot digital paper with hearts for crafts, scrapbooking & POD. Commercial use included.',
    },
]


def generate_related(current_id):
    """Pick 4 related patterns (other seamless patterns)."""
    others = [p for p in PATTERNS if p['id'] != current_id]
    import random
    random.seed(int(current_id))
    selected = random.sample(others, min(4, len(others)))
    cards = []
    for p in selected:
        t = html.escape(p['short_title'])[:60]
        cards.append(f'''      <a href="/products/{p['id']}.html" class="product-card">
            <div class="card-img"><img src="/img/{p['id']}_0.jpg" alt="{html.escape(p['short_title'])}" loading="lazy"></div>
            <div class="card-body">
              <h3>{t}</h3>
              <div class="card-price">$2.00</div>
            </div>
          </a>''')
    return '\n'.join(cards)


def create_page(p):
    title_esc = html.escape(p['title'])
    related = generate_related(p['id'])

    page = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title_esc} | MrsMillennial Designs</title>
  <meta name="description" content="{html.escape(p['meta_desc'])}">
  <meta property="og:title" content="{title_esc}">
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
    <span>{html.escape(p['short_title'])}</span>
  </div>

  <div class="back-link"><a href="/products.html"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5"/><path d="M12 19l-7-7 7-7"/></svg> Back to Shop</a></div>

  <div class="detail-grid">
    <div class="detail-images">
      <div class="detail-main"><img src="/img/{p['id']}_0.jpg" alt="{title_esc}" id="mainImg" class="detail-main-img"></div>
      <div class="detail-thumbs"><img src="/img/{p['id']}_0.jpg" alt="Pattern" class="thumb active" onclick="document.getElementById('mainImg').src='/img/{p['id']}_0.jpg';document.querySelectorAll('.thumb').forEach(t=>t.classList.remove('active'));this.classList.add('active')"><img src="/img/{p['id']}_1.jpg" alt="Tiled Preview" class="thumb" onclick="document.getElementById('mainImg').src='/img/{p['id']}_1.jpg';document.querySelectorAll('.thumb').forEach(t=>t.classList.remove('active'));this.classList.add('active')"><img src="/img/{p['id']}_2.jpg" alt="Mockup" class="thumb" onclick="document.getElementById('mainImg').src='/img/{p['id']}_2.jpg';document.querySelectorAll('.thumb').forEach(t=>t.classList.remove('active'));this.classList.add('active')"></div>
    </div>
    <div class="detail-info">
      <span class="badge badge-seamless">Seamless Patterns</span>
      <h1>{title_esc}</h1>
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
      <div class="detail-desc">{p['desc_emoji']} {html.escape(p['short_title'])} &ndash; Commercial Use Digital Paper<br><br>{html.escape(p['desc_intro'])}<br><br>Whether you're creating fabric, stationery, packaging, or sublimation products, this seamless pattern makes it easy to design beautiful collections.<br><br>🌟 Perfect For:<br>{p['desc_perfect'].replace(chr(10), '<br>')}<br><br>📥 What You'll Receive:<br>1 High-Resolution PNG File<br>1 High-Resolution JPEG File<br>Seamless / Repeat Pattern<br>Commercial Use Included<br>Instant Digital Download<br><br>📄 License Summary:<br>✔ Personal use<br>✔ Small business commercial use<br>✘ No reselling or sharing the digital file<br>✘ No redistribution as a standalone design<br><br>This artwork was created with the assistance of AI tools and thoughtfully refined by the designer, Mrs. Millennial Designs.<br>All designs remain original and copyright protected.</div>
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
{related}</div>
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
    return page


def main():
    for p in PATTERNS:
        page_html = create_page(p)
        path = os.path.join(OUTPUT_DIR, f"{p['id']}.html")
        with open(path, 'w') as f:
            f.write(page_html)
        print(f"  -> {path}")

    print(f"\nDone! {len(PATTERNS)} product pages created.")


if __name__ == '__main__':
    main()
