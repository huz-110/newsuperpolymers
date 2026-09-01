/* New Super Polymers — site behaviour */
(function () {
  'use strict';

  /* ---- Header: solid on scroll ---- */
  var hdr = document.querySelector('.hdr');
  function onScroll() {
    if (!hdr) return;
    hdr.classList.toggle('solid', window.scrollY > 24);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---- Mobile menu ---- */
  var burger = document.querySelector('.burger');
  var mnav = document.querySelector('.mobile-nav');
  if (burger && mnav) {
    burger.addEventListener('click', function () {
      var open = document.body.classList.toggle('menu-open');
      burger.setAttribute('aria-expanded', String(open));
      document.documentElement.style.overflow = open ? 'hidden' : '';
      Array.prototype.forEach.call(mnav.querySelectorAll('.mn-link'), function (a, i) {
        a.style.transitionDelay = open ? (0.09 + i * 0.055) + 's' : '0s';
      });
    });
    mnav.addEventListener('click', function (e) {
      if (e.target.closest('a')) {
        document.body.classList.remove('menu-open');
        burger.setAttribute('aria-expanded', 'false');
        document.documentElement.style.overflow = '';
      }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && document.body.classList.contains('menu-open')) burger.click();
    });
  }

  /* ---- Scroll reveal ---- */
  var rvs = document.querySelectorAll('.rv');
  if ('IntersectionObserver' in window && rvs.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    Array.prototype.forEach.call(rvs, function (el) { io.observe(el); });
  } else {
    Array.prototype.forEach.call(rvs, function (el) { el.classList.add('in'); });
  }

  /* ---- Count-up stats ---- */
  var nums = document.querySelectorAll('[data-count]');
  if ('IntersectionObserver' in window && nums.length && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    var nio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target, to = parseFloat(el.dataset.count), pre = el.dataset.pre || '', suf = el.dataset.suf || '';
        var dur = 1200, t0 = performance.now();
        (function step(t) {
          var p = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - p, 3);
          var n = Math.round(to * e);
          el.textContent = pre + (el.hasAttribute('data-plain') ? String(n) : n.toLocaleString('en-US')) + suf;
          if (p < 1) requestAnimationFrame(step);
        })(t0);
        nio.unobserve(el);
      });
    }, { threshold: 0.5 });
    Array.prototype.forEach.call(nums, function (el) { nio.observe(el); });
  }

  /* ---- Product filters ---- */
  var fbar = document.querySelector('[data-filters]');
  if (fbar) {
    var items = document.querySelectorAll('[data-tags]');
    var empty = document.querySelector('[data-empty]');
    fbar.addEventListener('click', function (e) {
      var btn = e.target.closest('.chip');
      if (!btn) return;
      Array.prototype.forEach.call(fbar.querySelectorAll('.chip'), function (c) {
        c.setAttribute('aria-pressed', String(c === btn));
      });
      var f = btn.dataset.filter, shown = 0;
      Array.prototype.forEach.call(items, function (it) {
        var ok = f === 'all' || (' ' + it.dataset.tags + ' ').indexOf(' ' + f + ' ') > -1;
        it.hidden = !ok;
        if (ok) shown++;
      });
      if (empty) empty.hidden = shown > 0;
    });
  }

  /* ---- Manufacturing: highlight active stage in the schematic ---- */
  var stages = document.querySelectorAll('[data-stage]');
  if (stages.length && 'IntersectionObserver' in window) {
    var sio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var id = en.target.dataset.stage;
        Array.prototype.forEach.call(document.querySelectorAll('[data-node]'), function (n) {
          n.classList.toggle('node-on', n.dataset.node === id);
        });
      });
    }, { rootMargin: '-42% 0px -42% 0px' });
    Array.prototype.forEach.call(stages, function (s) { sio.observe(s); });
  }

  /* ---- RFQ form -> WhatsApp ----------------------------------------------
     No backend required: the form composes a formatted enquiry from its own
     fields and hands it to WhatsApp pre-filled. Swap for a POST endpoint
     later without touching the markup. -------------------------------------*/
  var rfq = document.querySelector('[data-rfq]');
  if (rfq) {
    var label = function (el) {
      if (!el) return '';
      if (el.tagName === 'SELECT') return el.selectedIndex > 0 ? el.options[el.selectedIndex].text : '';
      return (el.value || '').trim();
    };
    rfq.addEventListener('submit', function (e) {
      e.preventDefault();
      if (rfq.reportValidity && !rfq.reportValidity()) return;

      var g = function (n) { return label(rfq.elements[n]); };
      var lines = [
        'New enquiry from newsuperpolymers.com', '',
        'Name: ' + g('name'),
        'Company: ' + g('company'),
        'Email: ' + g('email')
      ];
      var opt = [['Phone', 'phone'], ['Country', 'country'], ['Destination', 'destination'],
                 ['Product', 'product'], ['Colour', 'colour'], ['Gauge (micron)', 'gauge'],
                 ['Lay-flat width (mm)', 'width'], ['Quantity', 'quantity'], ['Terms', 'terms']];
      opt.forEach(function (p) { var v = g(p[1]); if (v) lines.push(p[0] + ': ' + v); });
      var req = g('requirements');
      if (req) { lines.push('', 'Requirement:', req); }

      var text = lines.join('\n');
      var num = rfq.getAttribute('data-rfq') || '919786050000';
      var url = 'https://wa.me/' + num + '?text=' + encodeURIComponent(text);

      var ok = rfq.querySelector('[data-rfq-ok]');
      if (ok) {
        var a = ok.querySelector('[data-rfq-link]');
        if (a) a.href = url;
        ok.hidden = false;
        ok.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
      var mail = rfq.querySelector('[data-rfq-mail]');
      if (mail) {
        mail.href = 'mailto:sales@newsuperpolymers.com?subject=' +
          encodeURIComponent('Enquiry — ' + (g('company') || g('name'))) +
          '&body=' + encodeURIComponent(text);
      }
      window.open(url, '_blank', 'noopener');
    });
  }

  /* ---- Glass: light follows the pointer across every pane ---- */
  var panes = document.querySelectorAll('.card, .notice, .stage-fig, .stats');
  if (panes.length && window.matchMedia('(hover: hover)').matches) {
    Array.prototype.forEach.call(panes, function (el) {
      el.addEventListener('pointermove', function (e) {
        var r = el.getBoundingClientRect();
        el.style.setProperty('--mx', ((e.clientX - r.left) / r.width * 100).toFixed(1) + '%');
        el.style.setProperty('--my', ((e.clientY - r.top) / r.height * 100).toFixed(1) + '%');
      });
    });
  }

  /* ---- Section seams brighten as they come into view ---- */
  var seams = document.querySelectorAll('.paper-2, .dark-2');
  if (seams.length && 'IntersectionObserver' in window) {
    var lio = new IntersectionObserver(function (en) {
      en.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('lit'); lio.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.05 });
    Array.prototype.forEach.call(seams, function (el) { lio.observe(el); });
  }

  /* ---- Year ---- */
  Array.prototype.forEach.call(document.querySelectorAll('[data-year]'), function (el) {
    el.textContent = new Date().getFullYear();
  });
})();
