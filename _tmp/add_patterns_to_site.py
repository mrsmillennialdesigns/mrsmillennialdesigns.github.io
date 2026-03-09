#!/usr/bin/env python3
"""Add all 15 new seamless patterns to the website:
1. Create product detail pages
2. Add product cards to products.html
3. Update seamless count on index.html
"""
import os

SITE = '/Users/alexhosage/Desktop/mmd-website'

patterns = [
    {
        'id': '8800000011',
        'name': 'Dark Academia Seamless Pattern PNG',
        'subtitle': 'Vintage Books & Potions Digital Paper',
        'search': 'dark academia seamless pattern png vintage books potions mushrooms',
        'desc': 'Dark Academia Seamless Pattern &ndash; Commercial Use Digital Paper<br><br>A moody, magical dark academia pattern featuring vintage books, potion bottles, whimsical frogs, spotted mushrooms, and golden stars on a warm parchment background.<br><br>Perfect for creating unique stationery, journal covers, fabric, and print-on-demand products with a cozy, scholarly aesthetic.',
        'tags': 'Dark academia stationery &amp; journal design<br>Book lover fabric &amp; textile projects<br>Cottagecore decor &amp; accessories<br>Scrapbooking &amp; printable paper<br>Gift wrap &amp; packaging<br>Print-on-demand products',
    },
    {
        'id': '8800000012',
        'name': 'Watercolor Unicorn Seamless Pattern PNG',
        'subtitle': 'Pastel Kids Digital Paper',
        'search': 'watercolor unicorn seamless pattern png pastel kids nursery',
        'desc': 'Watercolor Unicorn Seamless Pattern &ndash; Commercial Use Digital Paper<br><br>Dreamy pastel unicorns with flowing rainbow manes and golden horns, surrounded by sparkling stars. Each unicorn is unique with soft pink, lavender, mint, and cream tones.<br><br>A magical design perfect for little ones who love unicorns and fairy tales.',
        'tags': 'Unicorn birthday parties<br>Girls\' room &amp; nursery decor<br>Kids\' fabric &amp; textile design<br>Party supplies &amp; invitations<br>Scrapbooking &amp; printable paper<br>Print-on-demand products',
    },
    {
        'id': '8800000013',
        'name': 'Boho Wildflower Seamless Pattern PNG',
        'subtitle': 'Terracotta Floral Digital Paper',
        'search': 'boho wildflower seamless pattern png terracotta floral',
        'desc': 'Boho Wildflower Seamless Pattern &ndash; Commercial Use Digital Paper<br><br>A warm, earthy boho wildflower pattern with terracotta petals, dusty pink blooms, sage green leaves, and clusters of berries on a soft cream background.<br><br>This nature-inspired design brings a cozy, bohemian feel to any project.',
        'tags': 'Boho wedding stationery<br>Farmhouse &amp; cottagecore decor<br>Fabric &amp; textile design<br>Planner &amp; journal covers<br>Gift wrap &amp; packaging<br>Print-on-demand products',
    },
    {
        'id': '8800000014',
        'name': 'Axolotl Watercolor Seamless Pattern PNG',
        'subtitle': 'Cute Kawaii Kids Digital Paper',
        'search': 'axolotl watercolor seamless pattern png cute kawaii kids',
        'desc': 'Axolotl Watercolor Seamless Pattern &ndash; Commercial Use Digital Paper<br><br>Adorable pastel axolotls with feathery gills, blushing cheeks, and sweet smiles floating among tiny bubbles on a light aqua background. Each axolotl comes in soft pink, lavender, mint, peach, and blue tones.<br><br>A fun, kawaii-inspired design that kids and animal lovers will adore.',
        'tags': 'Axolotl birthday parties<br>Kids\' room &amp; nursery decor<br>Children\'s fabric &amp; accessories<br>School supplies &amp; stationery<br>Scrapbooking &amp; printable paper<br>Print-on-demand products',
    },
    {
        'id': '8800000015',
        'name': 'Dinosaur Bones Seamless Pattern PNG',
        'subtitle': 'Fossil Archaeology Kids Digital Paper',
        'search': 'dinosaur bones fossil seamless pattern png kids archaeology',
        'desc': 'Dinosaur Bones Seamless Pattern &ndash; Commercial Use Digital Paper<br><br>Classic dinosaur bones, cute dino skulls, and prehistoric footprints scattered across a warm parchment background. The muted ivory and tan tones give it a vintage, archaeological feel.<br><br>A unique fossil-themed design perfect for little paleontologists and dinosaur lovers.',
        'tags': 'Dinosaur birthday parties<br>Kids\' room &amp; nursery decor<br>Science &amp; educational projects<br>Children\'s fabric &amp; accessories<br>Scrapbooking &amp; printable paper<br>Print-on-demand products',
    },
    {
        'id': '8800000016',
        'name': 'Classic Race Car Seamless Pattern PNG',
        'subtitle': 'Vintage Toy Car Kids Digital Paper',
        'search': 'classic race car seamless pattern png vintage toy kids',
        'desc': 'Classic Race Car Seamless Pattern &ndash; Commercial Use Digital Paper<br><br>Muted red, blue, yellow, and green toy race cars with racing stripes, checkered flags, and sparkle stars on a warm cream background. Each car features cute details like exhaust puffs and number circles.<br><br>A retro-inspired design perfect for boys who love cars and racing.',
        'tags': 'Race car birthday parties<br>Boys\' room &amp; nursery decor<br>Children\'s fabric &amp; textile design<br>Party supplies &amp; invitations<br>Scrapbooking &amp; gift wrap<br>Print-on-demand products',
    },
    {
        'id': '8800000017',
        'name': 'Watercolor Trees Seamless Pattern PNG',
        'subtitle': 'Green Forest Kids Digital Paper',
        'search': 'watercolor trees forest seamless pattern png green nature',
        'desc': 'Watercolor Trees Seamless Pattern &ndash; Commercial Use Digital Paper<br><br>Charming round-top trees in beautiful shades of green with brown trunks, and tiny scattered leaves on a soft cream background. The layered foliage gives each tree a lush, watercolor look.<br><br>A nature-inspired design perfect for outdoor and woodland-themed projects.',
        'tags': 'Woodland &amp; nature-themed decor<br>Nursery &amp; kids\' room design<br>Fabric &amp; textile projects<br>Camping &amp; outdoor stationery<br>Scrapbooking &amp; printable paper<br>Print-on-demand products',
    },
    {
        'id': '8800000018',
        'name': 'Bee &amp; Summer Flowers Seamless Pattern PNG',
        'subtitle': 'Honey Bee Floral Kids Digital Paper',
        'search': 'bee summer flowers seamless pattern png honey floral',
        'desc': 'Bee &amp; Summer Flowers Seamless Pattern &ndash; Commercial Use Digital Paper<br><br>Cute buzzing bees with translucent wings alongside pink, orange, lavender, and yellow summer flowers and daisies, with tiny golden pollen dots scattered throughout. A bright, cheerful warm cream background ties it all together.<br><br>A sweet, sunny design that captures the joy of summer.',
        'tags': 'Bee &amp; garden birthday parties<br>Summer &amp; spring decor<br>Baby shower stationery<br>Kids\' fabric &amp; accessories<br>Honey &amp; farmhouse packaging<br>Print-on-demand products',
    },
    {
        'id': '8800000019',
        'name': 'Mermaid Watercolor Seamless Pattern PNG',
        'subtitle': 'Rainbow Mermaid Kids Digital Paper',
        'search': 'mermaid watercolor seamless pattern png rainbow kids',
        'desc': 'Mermaid Watercolor Seamless Pattern &ndash; Commercial Use Digital Paper<br><br>Enchanting little mermaids with rainbow-colored tails in teal, purple, pink, blue, green, and coral, paired with diverse hair and skin tones. Surrounded by tiny starfish, seashells, and bubbles on a soft ocean blue background.<br><br>A magical, inclusive design celebrating the wonder of the sea.',
        'tags': 'Mermaid birthday parties<br>Under the sea themed decor<br>Girls\' room &amp; nursery design<br>Kids\' fabric &amp; swimwear<br>Party supplies &amp; invitations<br>Print-on-demand products',
    },
    {
        'id': '8800000020',
        'name': 'Watercolor Sea Animals Seamless Pattern PNG',
        'subtitle': 'Ocean Creatures Kids Digital Paper',
        'search': 'watercolor sea animals ocean seamless pattern png kids whale octopus',
        'desc': 'Watercolor Sea Animals Seamless Pattern &ndash; Commercial Use Digital Paper<br><br>A delightful collection of baby ocean creatures including blue whales with water spouts, pink octopuses with big eyes, colorful fish, translucent jellyfish, and tiny seahorses, all floating among gentle bubbles on a soft ocean blue background.<br><br>A charming design that brings the wonders of the deep sea to life.',
        'tags': 'Ocean &amp; beach birthday parties<br>Nautical nursery decor<br>Kids\' room &amp; bathroom design<br>Children\'s fabric &amp; accessories<br>Marine-themed stationery<br>Print-on-demand products',
    },
    {
        'id': '8800000021',
        'name': 'Princess Castle Seamless Pattern PNG',
        'subtitle': 'Fairy Tale Kids Digital Paper',
        'search': 'princess castle fairy tale seamless pattern png kids',
        'desc': 'Princess Castle Seamless Pattern &ndash; Commercial Use Digital Paper<br><br>Dreamy pastel fairy tale castles in pink, lavender, blue, cream, and peach, complete with towers, flags, arched windows, and crenellated walls. Scattered with golden crowns, tiny hearts, and sparkle stars.<br><br>A magical design fit for a princess-themed celebration or nursery.',
        'tags': 'Princess birthday parties<br>Fairy tale nursery decor<br>Girls\' room &amp; playroom design<br>Party supplies &amp; invitations<br>Scrapbooking &amp; gift wrap<br>Print-on-demand products',
    },
    {
        'id': '8800000022',
        'name': 'Modern Line Art Cat Seamless Pattern PNG',
        'subtitle': 'Minimalist Cat Lover Digital Paper',
        'search': 'modern line art cat minimalist seamless pattern png',
        'desc': 'Modern Line Art Cat Seamless Pattern &ndash; Commercial Use Digital Paper<br><br>Minimalist one-line-style sitting cats with delicate whiskers and curving tails, drawn in muted charcoal, warm brown, and blue-gray tones on a warm cream background. Scattered with tiny paw prints for extra charm.<br><br>A modern, sophisticated design for cat lovers and minimalist aesthetics.',
        'tags': 'Cat lover gifts &amp; accessories<br>Modern &amp; minimalist home decor<br>Pet-themed stationery<br>Fabric &amp; textile design<br>Planner &amp; journal covers<br>Print-on-demand products',
    },
    {
        'id': '8800000023',
        'name': 'Modern Line Art Dog Seamless Pattern PNG',
        'subtitle': 'Minimalist Dog Lover Digital Paper',
        'search': 'modern line art dog minimalist seamless pattern png',
        'desc': 'Modern Line Art Dog Seamless Pattern &ndash; Commercial Use Digital Paper<br><br>Charming minimalist one-line-style dogs with floppy ears, wagging tails, and tiny tongues, drawn in warm tones of charcoal, brown, and blue-gray on a soft cream background. Accented with mini bone outlines and small hearts.<br><br>A modern, playful design perfect for dog lovers.',
        'tags': 'Dog lover gifts &amp; accessories<br>Modern &amp; minimalist home decor<br>Pet-themed stationery<br>Fabric &amp; textile design<br>Planner &amp; journal covers<br>Print-on-demand products',
    },
    {
        'id': '8800000024',
        'name': 'Affirmations for Kids Seamless Pattern PNG',
        'subtitle': 'Positive Words Kids Digital Paper',
        'search': 'affirmations kids positive words seamless pattern png inspirational',
        'desc': 'Affirmations for Kids Seamless Pattern &ndash; Commercial Use Digital Paper<br><br>Uplifting positive affirmations like "I am kind", "I am brave", "I am loved", "I am enough", and more, displayed in soft pastel rounded bubbles with delicate hearts, stars, and dots.<br><br>A beautiful, empowering design that encourages confidence and self-love in children.',
        'tags': 'Classroom &amp; school decor<br>Kids\' room &amp; playroom design<br>Therapy &amp; counseling materials<br>Children\'s fabric &amp; accessories<br>Inspirational stationery<br>Print-on-demand products',
    },
    {
        'id': '8800000025',
        'name': 'Watercolor Rainbow &amp; Clouds Seamless Pattern PNG',
        'subtitle': 'Happy Sky Kids Digital Paper',
        'search': 'watercolor rainbow clouds seamless pattern png kids sky',
        'desc': 'Watercolor Rainbow &amp; Clouds Seamless Pattern &ndash; Commercial Use Digital Paper<br><br>Cheerful rainbows with all seven colors arching over fluffy white clouds, accompanied by puffy clouds, sparkle stars, and tiny raindrops on a soft sky blue background.<br><br>A bright, happy design that brings sunshine and smiles to any project.',
        'tags': 'Rainbow birthday parties<br>Nursery &amp; kids\' room decor<br>Baby shower stationery<br>Children\'s fabric &amp; accessories<br>Weather-themed classroom projects<br>Print-on-demand products',
    },
]

# Related products for each (pick 4 from the set)
def get_related(current_id):
    all_ids = [p['id'] for p in patterns]
    related = [pid for pid in all_ids if pid != current_id]
    import random
    random.seed(int(current_id) % 1000)
    random.shuffle(related)
    return related[:4]

# 1. Create product detail pages
print("Creating product detail pages...")
for p in patterns:
    pid = p['id']
    name = p['name']
    subtitle = p['subtitle']
    desc_html = p['desc']
    tags_html = p['tags']

    related = get_related(pid)
    related_html = ""
    for rid in related:
        rp = next(x for x in patterns if x['id'] == rid)
        rname_short = rp['name'].replace(' Seamless Pattern PNG', '')
        related_html += f'''      <a href="/products/{rid}.html" class="product-card">
            <div class="card-img"><img src="/img/{rid}_0.jpg" alt="{rname_short} Seamless Pattern" loading="lazy"></div>
            <div class="card-body">
              <h3>{rname_short} Seamless Pattern</h3>
              <div class="card-price">$2.00</div>
            </div>
          </a>
'''

    # For name_safe (no HTML entities in title tag)
    name_safe = name.replace('&amp;', '&').replace('&ndash;', '-')
    subtitle_safe = subtitle.replace('&amp;', '&')
    breadcrumb_name = name.replace(' Seamless Pattern PNG', '')

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{name_safe} | {subtitle_safe} | Commercial Use Background | MrsMillennial Designs</title>
  <meta name="description" content="{name_safe} - {subtitle_safe}. High-resolution seamless pattern for fabric, stationery &amp; POD. Commercial use included.">
  <meta property="og:title" content="{name} | {subtitle} | Commercial Use Background">
  <meta property="og:image" content="https://mrsmillennialdesigns.com/img/{pid}_0.jpg">
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
    <span>{breadcrumb_name}</span>
  </div>

  <div class="back-link"><a href="/products.html"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5"/><path d="M12 19l-7-7 7-7"/></svg> Back to Shop</a></div>

  <div class="detail-grid">
    <div class="detail-images">
      <div class="detail-main"><img src="/img/{pid}_0.jpg" alt="{name} | {subtitle} | Commercial Use Background" id="mainImg" class="detail-main-img"></div>
      <div class="detail-thumbs"><img src="/img/{pid}_0.jpg" alt="Pattern" class="thumb active" onclick="document.getElementById('mainImg').src='/img/{pid}_0.jpg';document.querySelectorAll('.thumb').forEach(t=>t.classList.remove('active'));this.classList.add('active')"><img src="/img/{pid}_1.jpg" alt="Tiled Preview" class="thumb" onclick="document.getElementById('mainImg').src='/img/{pid}_1.jpg';document.querySelectorAll('.thumb').forEach(t=>t.classList.remove('active'));this.classList.add('active')"><img src="/img/{pid}_2.jpg" alt="Mockup" class="thumb" onclick="document.getElementById('mainImg').src='/img/{pid}_2.jpg';document.querySelectorAll('.thumb').forEach(t=>t.classList.remove('active'));this.classList.add('active')"></div>
    </div>
    <div class="detail-info">
      <span class="badge badge-seamless">Seamless Patterns</span>
      <h1>{name} | {subtitle} | Commercial Use Background</h1>
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
      <div class="detail-desc">{desc_html}<br><br>🌟 Perfect For:<br>{tags_html}<br><br>📥 What You'll Receive:<br>1 High-Resolution PNG File<br>1 High-Resolution JPEG File<br>Seamless / Repeat Pattern<br>Commercial Use Included<br>Instant Digital Download<br><br>📄 License Summary:<br>✔ Personal use<br>✔ Small business commercial use<br>✘ No reselling or sharing the digital file<br>✘ No redistribution as a standalone design<br><br>This artwork was created with the assistance of AI tools and thoughtfully refined by the designer, Mrs. Millennial Designs.<br>All designs remain original and copyright protected.</div>
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

    filepath = os.path.join(SITE, 'products', f'{pid}.html')
    with open(filepath, 'w') as f:
        f.write(html)
    print(f"  Created {pid}.html")

# 2. Generate product card HTML for products.html
print("\nGenerating product cards HTML...")
cards_html = ""
for p in patterns:
    pid = p['id']
    name = p['name']
    subtitle = p['subtitle']
    search = p['search']
    cards_html += f'''      <a href="/products/{pid}.html" class="product-card" data-cat="seamless" data-title="{search}">
        <div class="card-img"><img src="/img/{pid}_0.jpg" alt="{name}" loading="lazy"></div>
        <div class="card-body">
          <span class="badge badge-seamless">Seamless Patterns</span>
          <h3>{name} | {subtitle}</h3>
          <div class="card-price">$2.00</div>
        </div>
      </a>
'''

print("Cards HTML to insert (saved to _tmp/new_cards.html):")
with open(os.path.join(SITE, '_tmp', 'new_cards.html'), 'w') as f:
    f.write(cards_html)

print(f"\nDone! Created {len(patterns)} product detail pages.")
print(f"New cards HTML saved to _tmp/new_cards.html")
print(f"Still need to: insert cards into products.html, update index.html count")
