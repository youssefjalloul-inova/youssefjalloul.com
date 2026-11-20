/* Cookie consent for youssefjalloul.com
 * Opt-in by default for everyone, everywhere (GDPR / UK GDPR / ePrivacy standard, which also satisfies
 * CCPA/CPRA, Australia's Privacy Act, UAE and Saudi PDPL, LGPD, PIPEDA and Quebec Law 25).
 * Nothing that tracks loads until the visitor says yes. "Reject all" is as easy as "Accept all".
 * Global Privacy Control (GPC) is honoured as an opt-out of advertising.
 *
 * To switch a tracker on, paste its ID below. Empty = never loaded.
 */
(function () {
  var IDS = {
    ga4: '', // Google Analytics 4, e.g. 'G-XXXXXXXXXX'
    googleAds: '',    // Google Ads / Google tag, e.g. 'AW-XXXXXXXXX'
    metaPixel: '',    // Meta (Facebook) Pixel ID, e.g. '123456789012345'
    clarity: ''       // Microsoft Clarity project ID, e.g. 'abcd1234ef'
  };
  var KEY = 'yj-consent', VERSION = 2, d = document, w = window;
  var gpc = navigator.globalPrivacyControl === true;

  function read() { try { var v = JSON.parse(localStorage.getItem(KEY)); return v && v.v === VERSION ? v : null; } catch (e) { return null; } }
  function save(c) { c.v = VERSION; c.ts = new Date().toISOString(); try { localStorage.setItem(KEY, JSON.stringify(c)); } catch (e) {} }

  w.dataLayer = w.dataLayer || [];
  function gtag() { w.dataLayer.push(arguments); }
  w.gtag = w.gtag || gtag;

  function inject(src, attrs) { var s = d.createElement('script'); s.async = true; s.src = src; if (attrs) for (var k in attrs) s.setAttribute(k, attrs[k]); d.head.appendChild(s); }
  var loaded = {};

  function apply(c) {
    w.gtag('consent', 'update', {
      analytics_storage: c.analytics ? 'granted' : 'denied',
      ad_storage: c.marketing ? 'granted' : 'denied',
      ad_user_data: c.marketing ? 'granted' : 'denied',
      ad_personalization: c.marketing ? 'granted' : 'denied'
    });
    var gid = (c.analytics && IDS.ga4) || (c.marketing && IDS.googleAds);
    if (gid && !loaded.gtag) {
      loaded.gtag = 1; inject('https://www.googletagmanager.com/gtag/js?id=' + gid);
      w.gtag('js', new Date());
    }
    if (c.analytics && IDS.ga4 && !loaded.ga4) { loaded.ga4 = 1; w.gtag('config', IDS.ga4, { anonymize_ip: true }); }
    if (c.marketing && IDS.googleAds && !loaded.ads) { loaded.ads = 1; w.gtag('config', IDS.googleAds); }
    if (c.analytics && IDS.clarity && !loaded.clarity) {
      loaded.clarity = 1;
      w.clarity = w.clarity || function () { (w.clarity.q = w.clarity.q || []).push(arguments); };
      inject('https://www.clarity.ms/tag/' + IDS.clarity);
      w.clarity('consent');
    }
    if (c.marketing && IDS.metaPixel && !loaded.meta) {
      loaded.meta = 1;
      var f = w.fbq = function () { f.callMethod ? f.callMethod.apply(f, arguments) : f.queue.push(arguments); };
      if (!w._fbq) w._fbq = f; f.push = f; f.loaded = true; f.version = '2.0'; f.queue = [];
      inject('https://connect.facebook.net/en_US/fbevents.js');
      w.fbq('consent', 'grant'); w.fbq('init', IDS.metaPixel); w.fbq('track', 'PageView');
    } else if (!c.marketing && w.fbq) { w.fbq('consent', 'revoke'); }
  }

  var el;
  function render(open) {
    if (el) el.remove();
    var cur = read() || { analytics: false, marketing: false };
    el = d.createElement('div');
    el.className = 'ck' + (open ? ' ck-open' : '');
    el.setAttribute('role', 'dialog'); el.setAttribute('aria-modal', 'false'); el.setAttribute('aria-labelledby', 'ck-h');
    /* Built with DOM methods rather than innerHTML (no HTML parsing, Trusted Types friendly) */
    function n(tag, attrs, kids) {
      var x = d.createElement(tag);
      for (var k in attrs || {}) { if (attrs[k] === true) x.setAttribute(k, ''); else if (attrs[k] !== false && attrs[k] != null) x.setAttribute(k, attrs[k]); }
      (kids || []).forEach(function (c) { if (c) x.append(c); });
      return x;
    }
    function opt(input, title, text) { return n('label', { 'class': 'ck-o' }, [n('input', input), n('span', null, [n('b', null, [title]), ' ' + text])]); }
    function btn(cls, act, label) { return n('button', { type: 'button', 'class': cls, 'data-ck': act }, [label]); }
    el.append(n('div', { 'class': 'ck-in' }, [
      n('p', { 'class': 'ck-h', id: 'ck-h' }, ['Cookies. The digital kind, not the toaster kind.']),
      n('p', { 'class': 'ck-p' }, ['Strictly necessary storage keeps the site working. With your OK, I also use analytics (Google Analytics, Microsoft Clarity) to see what helps, and advertising tags (Meta Pixel, Google Ads) to measure campaigns. Nothing that tracks loads until you choose. ',
        n('a', { href: (w.YJ_PRE || '') + 'privacy.html' }, ['Privacy & cookie policy']), '.']),
      gpc ? n('p', { 'class': 'ck-gpc' }, ['Your browser sends a Global Privacy Control signal, so advertising stays off.']) : null,
      n('div', { 'class': 'ck-opts' }, [
        opt({ type: 'checkbox', checked: true, disabled: true }, 'Strictly necessary', 'Remembers your choices and keeps the site secure. Always on.'),
        opt({ type: 'checkbox', id: 'ck-a', checked: !!cur.analytics }, 'Analytics', 'Google Analytics 4 and Microsoft Clarity: anonymous usage, heatmaps and session insights.'),
        opt({ type: 'checkbox', id: 'ck-m', checked: !!(cur.marketing && !gpc), disabled: gpc }, 'Advertising', 'Meta Pixel and Google Ads: measure and personalise ads, including on other sites.')
      ]),
      n('div', { 'class': 'ck-b' }, [btn('ck-btn', 'reject', 'Reject all'), btn('ck-btn ck-cust', 'custom', 'Customise'), btn('ck-btn', 'save', 'Save choices'), btn('ck-btn ck-yes', 'accept', 'Accept all')])
    ]));
    d.body.appendChild(el);
    el.addEventListener('click', function (e) {
      var b = e.target.closest('[data-ck]'); if (!b) return;
      var a = b.getAttribute('data-ck'), c;
      if (a === 'custom') { el.classList.add('ck-open'); return; }
      if (a === 'accept') c = { analytics: true, marketing: !gpc };
      if (a === 'reject') c = { analytics: false, marketing: false };
      if (a === 'save') c = { analytics: d.getElementById('ck-a').checked, marketing: !gpc && d.getElementById('ck-m').checked };
      var had = read(); save(c); apply(c); el.remove(); el = null;
      if (had && ((had.analytics && !c.analytics) || (had.marketing && !c.marketing))) location.reload();
    });
  }

  function start() {
    var c = read();
    var any = IDS.ga4 || IDS.googleAds || IDS.metaPixel || IDS.clarity;
    if (c) apply(c); else if (any) render(false);
    d.addEventListener('click', function (e) {
      var t = e.target.closest('[data-cookie-settings]');
      if (t) { e.preventDefault(); render(true); }
    });
  }
  if (d.readyState === 'loading') d.addEventListener('DOMContentLoaded', start); else start();
})();
