/**
 * MrsMillennial Designs — Image Protection
 * Adds a transparent watermark overlay on ALL images site-wide.
 * Prevents casual right-click theft of product images and customer photos.
 */
(function() {
  // Create SVG watermark tile as data URI
  var text = 'MrsMillennial Designs';
  var svg = '<svg xmlns="http://www.w3.org/2000/svg" width="300" height="120">' +
    '<text x="150" y="60" text-anchor="middle" dominant-baseline="middle" ' +
    'font-family="-apple-system,Helvetica,Arial,sans-serif" font-size="14" ' +
    'font-weight="600" letter-spacing="2" fill="rgba(255,255,255,0.18)" ' +
    'transform="rotate(-30,150,60)">' + text + '</text></svg>';
  var tile = 'data:image/svg+xml,' + encodeURIComponent(svg);

  function protect(img) {
    if (img.dataset.wmProtected) return;
    if (img.closest('.nav') || img.closest('.footer') || img.width < 40 || img.height < 40) return;
    // Skip thumbnails — already protected by parent detail-main overlay
    if (img.classList.contains('thumb')) return;
    // Skip gallery images — protected via CSS ::before on .gal-item
    if (img.closest('.gal-item')) return;
    img.dataset.wmProtected = '1';

    var wrap = document.createElement('span');
    wrap.style.cssText = 'position:relative;display:inline-block;line-height:0;max-width:100%;';
    img.parentNode.insertBefore(wrap, img);
    wrap.appendChild(img);

    var ov = document.createElement('span');
    ov.style.cssText = 'position:absolute;inset:0;background:url("' + tile + '") repeat;pointer-events:none;z-index:1;border-radius:inherit;';
    wrap.appendChild(ov);

    // Disable right-click save on images
    img.addEventListener('contextmenu', function(e) { e.preventDefault(); });
    img.addEventListener('dragstart', function(e) { e.preventDefault(); });
  }

  function protectAll() {
    document.querySelectorAll('img').forEach(function(img) {
      if (img.complete && img.naturalWidth > 0) {
        protect(img);
      } else {
        img.addEventListener('load', function() { protect(img); });
      }
    });
  }

  // Run on DOM ready and watch for new images
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', protectAll);
  } else {
    protectAll();
  }

  // Watch for dynamically added images
  var observer = new MutationObserver(function(mutations) {
    mutations.forEach(function(m) {
      m.addedNodes.forEach(function(node) {
        if (node.nodeType === 1) {
          if (node.tagName === 'IMG') protect(node);
          else if (node.querySelectorAll) {
            node.querySelectorAll('img').forEach(protect);
          }
        }
      });
    });
  });
  observer.observe(document.body, { childList: true, subtree: true });
})();
