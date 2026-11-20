(function(){
  'use strict';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches || /[?&]static/.test(location.search);

  if (/[?&]static/.test(location.search)) document.documentElement.classList.add('static');

  /* every new page starts at the top (also scrolls the preview frame's parent into place) */
  function toTop(){
    if (location.hash) return;
    window.scrollTo({top:0, left:0, behavior:'instant'});
    try { document.documentElement.scrollIntoView({block:'start', inline:'nearest', behavior:'instant'}); } catch(e) {}
  }
  toTop();
  window.addEventListener('pageshow', function(e){ if (!e.persisted) toTop(); });
  window.addEventListener('load', toTop);

  /* nav state + mobile drawer */
  var nav = document.getElementById('nav');
  function onScroll(){ nav.classList.toggle('scrolled', window.scrollY > 24); }
  onScroll(); window.addEventListener('scroll', onScroll, {passive:true});
  var burger = document.getElementById('burger'), drawer = document.getElementById('drawer');
  /* The drawer is a native popover (popovertarget on the button): Escape, tap-outside and focus return come free.
     The class toggle below is only the fallback for browsers without the Popover API. */
  var hasPopover = Object.hasOwn ? Object.hasOwn(HTMLElement.prototype, 'popover') : 'popover' in HTMLElement.prototype;
  function setDrawer(open){
    burger.setAttribute('aria-expanded', open);
    if (hasPopover) { if (drawer.matches(':popover-open') !== open) drawer.togglePopover(open); }
    else drawer.classList.toggle('open', open);
  }
  if (hasPopover) drawer.addEventListener('toggle', function(e){ burger.setAttribute('aria-expanded', e.newState === 'open'); });
  else burger.addEventListener('click', function(){ setDrawer(burger.getAttribute('aria-expanded') !== 'true'); });
  drawer.querySelectorAll('a').forEach(function(a){ a.addEventListener('click', function(){ setDrawer(false); }); });

  /* logo fallbacks: if a logo file is missing, show a clean text chip instead */
  document.querySelectorAll('img[data-fb]').forEach(function(img){
    function swap(){
      var p = img.parentElement, parts = img.getAttribute('data-fb').split('|');
      p.classList.add('txt'); p.replaceChildren(parts[0]);
      if (parts[1]) { var sm = document.createElement('small'); sm.textContent = parts[1]; p.append(sm); }
    }
    if (img.complete && img.naturalWidth === 0) swap(); else img.addEventListener('error', swap);
  });

  /* marquee: duplicate children for a seamless loop (after fallbacks are in place) */
  document.querySelectorAll('.track[data-clone]').forEach(function(t){
    Array.prototype.slice.call(t.children).forEach(function(c){
      var k = c.cloneNode(true); k.setAttribute('aria-hidden','true');
      var im = k.querySelector('img'); if (im) { im.alt = ''; im.removeAttribute('data-fb'); }
      t.appendChild(k);
    });
  });

  /* reveal on scroll */
  var rv = document.querySelectorAll('.rv');
  if ('IntersectionObserver' in window && !reduce){
    var io = new IntersectionObserver(function(es){ es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); } }); }, {threshold:.12, rootMargin:'0px 0px -40px 0px'});
    rv.forEach(function(el){ io.observe(el); });
  } else { rv.forEach(function(el){ el.classList.add('in'); }); }

  /* count-up numbers */
  var counters = document.querySelectorAll('[data-count]');
  function run(el){
    var end = +el.getAttribute('data-count'), t0 = null, dur = 1400;
    function f(ts){ if(!t0) t0 = ts; var p = Math.min((ts - t0)/dur, 1), e = 1 - Math.pow(1 - p, 4); el.textContent = Math.round(end * e); if(p < 1) requestAnimationFrame(f); }
    el.textContent = '0'; requestAnimationFrame(f);
  }
  if ('IntersectionObserver' in window && !reduce){
    var co = new IntersectionObserver(function(es){ es.forEach(function(e){ if(e.isIntersecting){ run(e.target); co.unobserve(e.target); } }); }, {threshold:.6});
    counters.forEach(function(c){ co.observe(c); });
  }

  /* card spotlight */
  document.querySelectorAll('.card').forEach(function(c){
    c.addEventListener('pointermove', function(e){ var r = c.getBoundingClientRect(); c.style.setProperty('--mx', (e.clientX - r.left) + 'px'); c.style.setProperty('--my', (e.clientY - r.top) + 'px'); });
  });

  /* hero: drifting node network that reacts to the cursor */
  var cv = document.getElementById('net');
  if (cv && !reduce){
    var ctx = cv.getContext('2d'), W, H, pts = [], mouse = {x:-999, y:-999}, DPR = Math.min(window.devicePixelRatio || 1, 2), raf;
    function size(){
      var r = cv.getBoundingClientRect(); W = r.width; H = r.height;
      cv.width = W * DPR; cv.height = H * DPR; ctx.setTransform(DPR,0,0,DPR,0,0);
      var n = Math.round(Math.min(70, Math.max(26, W * H / 24000)));
      pts = []; for (var i = 0; i < n; i++) pts.push({x:Math.random()*W, y:Math.random()*H, vx:(Math.random()-.5)*.28, vy:(Math.random()-.5)*.28, r:Math.random()*1.4 + .6});
    }
    function draw(){
      ctx.clearRect(0,0,W,H);
      for (var i = 0; i < pts.length; i++){
        var a = pts[i]; a.x += a.vx; a.y += a.vy;
        if (a.x < 0 || a.x > W) a.vx *= -1; if (a.y < 0 || a.y > H) a.vy *= -1;
        var dm = Math.hypot(a.x - mouse.x, a.y - mouse.y);
        if (dm < 140){ a.x += (a.x - mouse.x) * .006; a.y += (a.y - mouse.y) * .006; }
        for (var j = i + 1; j < pts.length; j++){
          var b = pts[j], d = Math.hypot(a.x - b.x, a.y - b.y);
          if (d < 150){ ctx.strokeStyle = 'rgba(76,195,255,' + (.2 * (1 - d/150)) + ')'; ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke(); }
        }
        ctx.fillStyle = dm < 140 ? 'rgba(198,244,50,.95)' : 'rgba(160,166,179,.55)';
        ctx.beginPath(); ctx.arc(a.x, a.y, a.r, 0, 6.283); ctx.fill();
      }
      raf = requestAnimationFrame(draw);
    }
    size(); draw();
    window.addEventListener('resize', size);
    cv.parentElement.addEventListener('pointermove', function(e){ var r = cv.getBoundingClientRect(); mouse.x = e.clientX - r.left; mouse.y = e.clientY - r.top; });
    document.addEventListener('visibilitychange', function(){ if (document.hidden) cancelAnimationFrame(raf); else draw(); });
  }
})();

/* ---- AI pulse check, floating CTA, Calendly fallback ---- */
(function(){
  var Q = [
   ["Does a named executive own AI outcomes?","One accountable person, not a committee.","Name an executive owner and a monthly decision rhythm."],
   ["Do you have 3–5 funded, prioritised AI use cases?","Ranked by value, feasibility and risk.","Build a ranked, funded use-case portfolio."],
   ["Are pilots tied to a P&L or operational metric?","A number someone is accountable for.","Tie each pilot to a measurable business metric."],
   ["Is there an AI policy people actually follow, with approved tools?","Not just a document on an intranet.","Publish an AI policy and an approved-tools list."],
   ["Could you show AI governance evidence to a customer or auditor within a week?","Inventory, risk tiers, oversight, reporting.","Create the evidence layer: inventory, risk tiers, board reporting."],
   ["Is the data for your priority use cases accessible, clean and cleared for AI use?","Permission as well as quality.","Run a data-readiness check per priority use case."],
   ["Are staff trained and using approved AI tools?","Not shadow tools.","Train staff and provide approved tools."],
   ["Is at least one AI pilot in production and measured?","Live, used and reporting results.","Take one pilot to production with a measured outcome."]
  ];
  var box = document.getElementById('qbox'); if (box) {
  var i = 0, ans = [];
  var $ = function(id){ return document.getElementById(id); };
  function show(){
    $('qbar').style.width = (i / Q.length * 100) + '%';
    $('qn').textContent = 'Question ' + (i + 1) + ' of ' + Q.length;
    $('qt').textContent = Q[i][0]; $('qh').textContent = Q[i][1];
    $('qback').hidden = i === 0;
  }
  function done(){
    var s = ans.filter(Boolean).length, tier, msg, cta = 'Book a strategy call';
    if (s <= 2){ tier = 'High exposure'; msg = 'AI is likely happening without direction or control. A short readiness assessment would give you a fast, defensible baseline.'; }
    else if (s <= 5){ tier = 'Uneven foundations'; msg = 'You have pieces in place, but the gaps below are where pilots stall. Closing two or three of them usually unlocks scale.'; }
    else { tier = 'Strong base'; msg = 'You are ahead of most organisations. The value now is in prioritisation, governance evidence and scaling what works.'; }
    $('rscore').textContent = s; $('rtier').textContent = tier; $('rmsg').textContent = msg;
    var g = $('rgaps'); g.replaceChildren();
    ans.forEach(function(a, k){ if (!a){ var li = document.createElement('li'); li.textContent = Q[k][2]; g.appendChild(li); } });
    box.style.display = 'none'; $('res').classList.add('on');
    $('rcta2').setAttribute('href', ans[4] === false || ans[3] === false ? 'ai-governance-advisory.html' : 'ai-readiness-assessment.html');
    $('rcta2').textContent = ans[4] === false || ans[3] === false ? 'How AI governance works' : 'How a readiness assessment works';
  }
  function answer(v){ ans[i] = v; i++; if (i >= Q.length) done(); else show(); }
  $('qyes').addEventListener('click', function(){ answer(true); });
  $('qno').addEventListener('click', function(){ answer(false); });
  $('qback').addEventListener('click', function(){ if (i > 0){ i--; ans.length = i; show(); } });
  $('redo').addEventListener('click', function(){ i = 0; ans = []; $('res').classList.remove('on'); box.style.display = 'flex'; show(); });
  show();
  }

  var fc = document.getElementById('fixcta'), book = document.getElementById('bookband') || document.getElementById('book');
  if (fc && book && 'IntersectionObserver' in window){
    var bookVis = false;
    new IntersectionObserver(function(e){ bookVis = e[0].isIntersecting; upd(); }).observe(book);
    window.addEventListener('scroll', upd, {passive:true});
    function upd(){ fc.classList.toggle('show', window.scrollY > 900 && !bookVis); }
  }
  /* Calendly loads from here (not a page <script> tag) so the CSP's 'strict-dynamic' trusts it */
  if (document.querySelector('.calendly-inline-widget')){
    var cs = document.createElement('script'); cs.src = 'https://assets.calendly.com/assets/external/widget.js'; cs.async = true; document.head.appendChild(cs);
  }
  setTimeout(function(){
    var w = document.querySelector('.calendly-inline-widget');
    if (w && !w.querySelector('iframe')){ var f = document.getElementById('calfb'); if (f) f.classList.add('on'); }
  }, 4500);
})();

/* ---- comparison cards (mobile), nav scrollspy ---- */
(function(){
  var t = document.querySelector('table.cmp'), box = document.getElementById('cmpcards');
  if (t && box){
    var heads = [].slice.call(t.querySelectorAll('thead th')).slice(1), rows = [].slice.call(t.querySelectorAll('tbody tr'));
    var cards = heads.map(function(h, c){
      var el = document.createElement('article'); el.className = 'cmp-card' + (h.classList.contains('me') ? ' me' : '');
      var h3 = document.createElement('h3'); h3.textContent = h.textContent;
      var dl = document.createElement('dl');
      rows.forEach(function(r){
        var row = document.createElement('div'), dt = document.createElement('dt'), dd = document.createElement('dd');
        dt.textContent = r.querySelector('th').textContent; dd.textContent = r.querySelectorAll('td')[c].textContent;
        row.append(dt, dd); dl.append(row);
      });
      el.append(h3, dl); return el;
    });
    cards.sort(function(a, b){ return b.classList.contains('me') - a.classList.contains('me'); });
    cards.forEach(function(el){ box.appendChild(el); });
    var mq = window.matchMedia('(max-width:720px)');
    function sync(){ box.setAttribute('aria-hidden', mq.matches ? 'false' : 'true'); }
    sync(); if (mq.addEventListener) mq.addEventListener('change', sync);
  }
  var links = [].slice.call(document.querySelectorAll('.nav-links a[href^="#"]'));
  if (!links.length || !('IntersectionObserver' in window)) return;
  var map = {}; links.forEach(function(a){ var s = document.querySelector(a.getAttribute('href')); if (s) map[a.getAttribute('href').slice(1)] = a; });
  var spy = new IntersectionObserver(function(es){
    es.forEach(function(e){
      if (!e.isIntersecting) return;
      links.forEach(function(a){ a.classList.remove('on'); a.removeAttribute('aria-current'); });
      var a = map[e.target.id] || (e.target.id === 'signals' ? map.check : null); if (a){ a.classList.add('on'); a.setAttribute('aria-current', 'true'); }
    });
  }, {rootMargin:'-45% 0px -50% 0px'});
  document.querySelectorAll('main > section[id]').forEach(function(sec){ spy.observe(sec); });
})();
