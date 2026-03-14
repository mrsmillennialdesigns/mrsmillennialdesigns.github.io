/* MrsMillennial Designs — Shopping Cart Engine
   localStorage-based cart for static GitHub Pages site.
   Checkout via Cloudflare Worker -> Stripe Checkout Sessions.
   No dependencies. */

(function () {
  'use strict';

  var STORAGE_KEY = 'mmd_cart';
  var WORKER_URL = 'https://mmd-checkout.mrsmillennial.workers.dev/create-session';

  // ---------------------------------------------------------------------------
  // Helpers
  // ---------------------------------------------------------------------------

  function load() {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];
    } catch (_) {
      return [];
    }
  }

  function save(cart) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(cart));
    notify();
  }

  function notify() {
    updateBadge();
    document.dispatchEvent(new CustomEvent('cart-updated', { detail: { cart: load() } }));
  }

  function updateBadge() {
    var badges = document.querySelectorAll('.cart-count');
    var c = count();
    badges.forEach(function (el) {
      el.textContent = c;
      el.style.display = c > 0 ? 'flex' : 'none';
    });
  }

  // ---------------------------------------------------------------------------
  // Toast
  // ---------------------------------------------------------------------------

  function injectToastStyles() {
    if (document.getElementById('mmd-cart-toast-style')) return;
    var style = document.createElement('style');
    style.id = 'mmd-cart-toast-style';
    style.textContent = [
      '.mmd-toast{',
      '  position:fixed;bottom:calc(24px + env(safe-area-inset-bottom, 0px));right:24px;z-index:10000;',
      '  max-width:calc(100vw - 48px);',
      '  background:#2d2926;color:#faf8f5;',
      '  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;',
      '  font-size:14px;font-weight:600;',
      '  padding:12px 24px;border-radius:50px;',
      '  box-shadow:0 4px 16px rgba(45,41,38,0.18);',
      '  border:1.5px solid rgba(212,168,83,0.3);',
      '  opacity:0;transform:translateY(12px);',
      '  transition:opacity 0.3s ease,transform 0.3s ease;',
      '  pointer-events:none;',
      '}',
      '.mmd-toast.show{opacity:1;transform:translateY(0)}'
    ].join('\n');
    document.head.appendChild(style);
  }

  var toastTimer = null;

  function showToast(message) {
    injectToastStyles();

    var existing = document.querySelector('.mmd-toast');
    if (existing) existing.remove();
    clearTimeout(toastTimer);

    var el = document.createElement('div');
    el.className = 'mmd-toast';
    el.textContent = message || 'Added to cart!';
    document.body.appendChild(el);

    // Force reflow then show
    el.offsetHeight; // eslint-disable-line no-unused-expressions
    el.classList.add('show');

    toastTimer = setTimeout(function () {
      el.classList.remove('show');
      setTimeout(function () { el.remove(); }, 300);
    }, 2000);
  }

  // ---------------------------------------------------------------------------
  // Public API
  // ---------------------------------------------------------------------------

  function add(item) {
    if (!item || !item.id || !item.priceId) return;
    var cart = load();
    var idx = cart.findIndex(function (c) { return c.id === item.id; });
    if (idx > -1) {
      cart[idx].qty = Math.min((cart[idx].qty || 1) + (item.qty || 1), 100);
    } else {
      cart.push({
        id: item.id,
        priceId: item.priceId,
        title: item.title || '',
        price: parseFloat(item.price) || 0,
        image: item.image || '',
        qty: parseInt(item.qty, 10) || 1,
        type: item.type || 'digital',
        designId: item.designId || undefined
      });
    }
    save(cart);
    showToast('Added to cart!');
  }

  function remove(id) {
    var cart = load().filter(function (c) { return c.id !== id; });
    save(cart);
  }

  function update(id, qty) {
    var cart = load();
    var idx = cart.findIndex(function (c) { return c.id === id; });
    if (idx === -1) return;
    qty = parseInt(qty, 10);
    if (qty <= 0) {
      cart.splice(idx, 1);
    } else {
      cart[idx].qty = qty;
    }
    save(cart);
  }

  function get() {
    return load();
  }

  function count() {
    return load().reduce(function (sum, c) { return sum + (c.qty || 1); }, 0);
  }

  function total() {
    return load().reduce(function (sum, c) {
      return sum + (parseFloat(c.price) || 0) * (c.qty || 1);
    }, 0);
  }

  function clear() {
    localStorage.removeItem(STORAGE_KEY);
    notify();
  }

  var _checkingOut = false;

  async function checkout() {
    if (_checkingOut) return;
    var cart = load();
    if (!cart.length) return;
    _checkingOut = true;

    var items = cart.map(function (item) {
      return { price: item.priceId, quantity: item.qty || 1 };
    });

    try {
      var res = await fetch(WORKER_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          items: items,
          success_url: 'https://mrsmillennialdesigns.com/thank-you.html',
          cancel_url: 'https://mrsmillennialdesigns.com/cart.html'
        })
      });

      if (!res.ok) {
        throw new Error('Checkout request failed (' + res.status + ')');
      }

      var data = await res.json();
      if (data.url) {
        window.location.href = data.url;
      } else {
        throw new Error('No checkout URL returned');
      }
    } catch (err) {
      _checkingOut = false;
      console.error('[MMDCart] Checkout error:', err);
      alert('Something went wrong starting checkout. Please try again.');
      throw err;
    }
  }

  // ---------------------------------------------------------------------------
  // Button binding
  // ---------------------------------------------------------------------------

  function bindButtons(root) {
    var scope = root || document;
    var buttons = scope.querySelectorAll('[data-cart-add]');
    buttons.forEach(function (btn) {
      // Avoid double-binding
      if (btn._mmdBound) return;
      btn._mmdBound = true;

      btn.addEventListener('click', function (e) {
        e.preventDefault();
        add({
          id: btn.getAttribute('data-id'),
          priceId: btn.getAttribute('data-price-id'),
          title: btn.getAttribute('data-title'),
          price: btn.getAttribute('data-price'),
          image: btn.getAttribute('data-image'),
          type: btn.getAttribute('data-type') || 'digital',
          designId: btn.getAttribute('data-design-id') || undefined,
          qty: 1
        });
      });
    });
  }

  // ---------------------------------------------------------------------------
  // Init on DOM ready
  // ---------------------------------------------------------------------------

  function init() {
    updateBadge();
    bindButtons();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // ---------------------------------------------------------------------------
  // Expose
  // ---------------------------------------------------------------------------

  window.MMDCart = {
    add: add,
    remove: remove,
    update: update,
    get: get,
    count: count,
    total: total,
    clear: clear,
    checkout: checkout,
    bindButtons: bindButtons
  };

})();
