#!/usr/bin/env python3
"""Static site builder for youssefjalloul.com.

Usage:  python3 build.py            -> writes ./dist
Pages live in content/pages/*.py (each defines PAGE dict), articles in content/insights/*.md.
Shared header, booking band and footer are defined once here.
"""
import sys, json, os, re, shutil, html, datetime, importlib.util, glob
import markdown

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, 'dist')
SITE = 'https://youssefjalloul.com'
TODAY = datetime.date(2026, 11, 20).isoformat()
# Search engine ownership tags. Paste the content="..." value from Google Search Console
# (Settings > Ownership verification > HTML tag) and Bing Webmaster Tools, then rebuild.
# Leave empty if you verify by DNS instead.
GOOGLE_SITE_VERIFICATION = ''
BING_SITE_VERIFICATION = ''
OG_DEFAULT = SITE + '/assets/img/og-v2.png'
OG_ALT_DEFAULT = 'Youssef Jalloul, sovereign enterprise AI'

NAV = [
    ('services.html', 'Services'),
    ('private-ai.html', 'Private AI'),
    ('case-studies.html', 'Case studies'),
    ('ventures.html', 'Ventures'),
    ('courses.html', 'Courses'),
    ('insights.html', 'Insights'),
    ('about.html', 'About'),
]
DRAWER_EXTRA = [('speaking.html', 'Speaking'), ('self-check.html', 'Self-check'), ('faq.html', 'FAQ')]

SPRITE = '''<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#4CC3FF"/><stop offset=".55" stop-color="#7BE0C9"/><stop offset="1" stop-color="#C6F432"/></linearGradient>
    <symbol id="yj" viewBox="0 0 40 40">
      <path d="M3 13V3h10M27 3h10v10M37 27v10H27M13 37H3V27" fill="none" stroke="url(#g)" stroke-width="3" stroke-linecap="square"/>
      <text x="20" y="27" text-anchor="middle" font-family="Inter Tight,Inter,sans-serif" font-weight="800" font-size="17" letter-spacing="-1.5" fill="#F3F4F6">YJ</text>
    </symbol>
    <symbol id="li" viewBox="0 0 24 24"><path fill="currentColor" d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5ZM3 9.75h4v11H3v-11Zm6.5 0h3.84v1.5h.05c.54-1 1.84-2.06 3.79-2.06 4.05 0 4.8 2.62 4.8 6.03v5.53h-4v-4.9c0-1.17-.02-2.68-1.63-2.68-1.64 0-1.89 1.28-1.89 2.6v4.98h-4v-11Z"/></symbol>
    <symbol id="arr" viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></symbol>
  </defs>
</svg>'''


def asset_v(name):
    """Short content hash so browsers fetch new CSS/JS as soon as it changes."""
    import hashlib
    return hashlib.sha1(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', name), 'rb').read()).hexdigest()[:8]


def asset_sri(name):
    """Subresource Integrity hash; also listed in the CSP so 'strict-dynamic' trusts this file."""
    import hashlib, base64
    data = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', name), 'rb').read()
    return 'sha384-' + base64.b64encode(hashlib.sha384(data).digest()).decode()


def esc(s):
    return html.escape(s, quote=True)


def head(meta, pre):
    title = meta['title']
    desc = meta['description']
    if len(desc) > 160:
        raise ValueError(f"meta description over 160 characters ({len(desc)}) on {meta['path']}: write a shorter one")
    path = meta['path']
    canon = SITE + '/' + ('' if path == 'index.html' else path)
    og = meta.get('og_image', OG_DEFAULT)
    og_alt = meta.get('og_alt', OG_ALT_DEFAULT)
    og_type_mime = 'image/png' if og.endswith('.png') else 'image/jpeg'
    verify = ''
    if GOOGLE_SITE_VERIFICATION:
        verify += f'<meta name="google-site-verification" content="{GOOGLE_SITE_VERIFICATION}">\n'
    if BING_SITE_VERIFICATION:
        verify += f'<meta name="msvalidate.01" content="{BING_SITE_VERIFICATION}">\n'
    art = ''
    if meta.get('published'):
        art = f'<meta property="article:published_time" content="{meta["published"]}">\n<meta property="article:modified_time" content="{meta.get("modified", meta["published"])}">\n<meta property="article:author" content="{SITE}/about.html">\n'
    jsonld = meta.get('jsonld')
    blocks = []
    if jsonld:
        blocks.append('<script type="application/ld+json">\n' + (jsonld if isinstance(jsonld, str) else json.dumps(jsonld, ensure_ascii=False, indent=1)) + '\n</script>')
    robots = meta.get('robots', 'index,follow,max-image-preview:large,max-snippet:-1')
    return f'''<!DOCTYPE html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<script>document.documentElement.classList.remove('no-js');if('scrollRestoration' in history)history.scrollRestoration='manual';</script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('consent','default',{{ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',analytics_storage:'denied',functionality_storage:'granted',security_storage:'granted',wait_for_update:500}});gtag('set','ads_data_redaction',true);gtag('set','url_passthrough',true);window.YJ_PRE='{pre}';</script>
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="author" content="Youssef Jalloul">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canon}">
<meta name="theme-color" content="#0A0B0E">
{verify}<link rel="icon" href="{pre}favicon.ico" sizes="32x32">
<link rel="icon" href="{pre}assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{pre}apple-touch-icon.png">
<link rel="manifest" href="{pre}site.webmanifest">
<link rel="alternate" type="application/rss+xml" title="The AI Glittch by Youssef Jalloul" href="{pre}feed.xml">
<link rel="preload" href="{pre}assets/fonts/inter-tight-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{pre}assets/fonts/inter-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<meta property="og:type" content="{meta.get('og_type','website')}">
<meta property="og:site_name" content="Youssef Jalloul">
<meta property="og:locale" content="en_AU">
<meta property="og:title" content="{esc(meta.get('og_title', title))}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{og}">
<meta property="og:image:secure_url" content="{og}">
<meta property="og:image:type" content="{og_type_mime}">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{esc(og_alt)}">
{art}
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(meta.get('og_title', title))}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{og}">
<meta name="twitter:image:alt" content="{esc(og_alt)}">
<link rel="stylesheet" href="{pre}styles.css?v={asset_v('styles.css')}">
{chr(10).join(blocks)}
</head>'''


def header(active, pre):
    on = ' class="on" aria-current="page"'
    links = ''.join(f'<a href="{pre}{h}"{on if h == active else ""}>{t}</a>' for h, t in NAV)
    drawer = ''.join(f'<a href="{pre}{h}">{t}</a>' for h, t in NAV + DRAWER_EXTRA)
    return f'''<body>
<a class="skip" href="#main">Skip to content</a>
{SPRITE}
<header class="nav" id="nav">
  <div class="wrap nav-in">
    <a class="brand" href="{pre}index.html" aria-label="Youssef Jalloul, home"><svg class="mark"><use href="#yj"/></svg><span>Youssef Jalloul</span></a>
    <nav class="nav-links" aria-label="Primary">{links}</nav>
    <div class="nav-end"><a class="nav-li" href="https://www.linkedin.com/in/youssef-jalloul/" target="_blank" rel="noopener me" aria-label="Follow Youssef Jalloul on LinkedIn" title="Follow me on LinkedIn"><svg><use href="#li"/></svg></a><a class="btn btn-primary" href="{pre}book.html">Book a call <svg><use href="#arr"/></svg></a></div>
    <button type="button" class="burger" id="burger" aria-label="Menu" aria-expanded="false" aria-controls="drawer" popovertarget="drawer"><i></i><i></i><i></i></button>
  </div>
  <nav class="drawer" id="drawer" aria-label="Mobile" popover="auto">{drawer}<a href="https://www.linkedin.com/in/youssef-jalloul/" target="_blank" rel="noopener me">LinkedIn</a><a href="https://www.linkedin.com/newsletters/the-ai-glittch-7332984165379805188/" target="_blank" rel="noopener">The AI Glittch</a><a class="btn btn-primary" href="{pre}book.html">Book a strategy call</a></nav>
</header>
<main id="main" tabindex="-1">'''


def bookband(pre):
    return f'''<section class="bookband" id="bookband">
  <div class="wrap bb-in">
    <div>
      <span class="eyebrow">Unplug the toaster</span>
      <h2>Your AI should live in your house. <mark class="hl">Let&rsquo;s move it in.</mark></h2>
      <p class="lead">45 minutes. Bring one problem: stalled pilots, a governance question, a board brief, data that can&rsquo;t leave the country. Leave with the first move. If the answer is that you don&rsquo;t need me, you&rsquo;ll hear that too.</p>
    </div>
    <div class="bb-cta">
      <a class="btn btn-primary" href="{pre}book.html">Book a strategy call <svg><use href="#arr"/></svg></a>
      <a class="btn btn-ghost" href="{pre}self-check.html">Take the 2-minute check</a>
      <p class="bb-follow">Not ready to talk? <a href="https://www.linkedin.com/in/youssef-jalloul/" target="_blank" rel="noopener me"><svg><use href="#li"/></svg>Follow along on LinkedIn</a> or get <a href="https://www.linkedin.com/newsletters/the-ai-glittch-7332984165379805188/" target="_blank" rel="noopener">The AI Glittch</a> in your feed.</p>
    </div>
  </div>
</section>'''


def footer(pre, sources=None):
    src = f'<p class="src">{sources}</p>' if sources else ''
    return f'''</main>
<footer>
  <div class="wrap">
    <div class="f-grid">
      <div class="f-brand"><a class="brand" href="{pre}index.html"><svg class="mark"><use href="#yj"/></svg><span>Youssef Jalloul</span></a><p>AI entrepreneur and tech venture builder. Private, local, governed enterprise AI that answers to you.</p><p class="disclose">Made with AI. Understood by humans. Illustrations drawn in code; every word signed off by a human.</p></div>
      <div><h4>Work with me</h4><ul><li><a href="{pre}services.html">Services</a></li><li><a href="{pre}private-ai.html">Private AI</a></li><li><a href="{pre}case-studies.html">Case studies</a></li><li><a href="{pre}self-check.html">Self-check</a></li><li><a href="{pre}book.html">Book a call</a></li></ul></div>
      <div><h4>Read</h4><ul><li><a href="{pre}insights.html">Insights</a></li><li><a href="{pre}faq.html">FAQ</a></li><li><a href="{pre}ai-readiness-assessment.html">AI readiness guide</a></li><li><a href="{pre}ai-governance-advisory.html">AI governance guide</a></li><li><a href="{pre}fractional-chief-ai-officer.html">Fractional CAIO guide</a></li></ul></div>
      <div><h4>About</h4><ul><li><a href="{pre}about.html">About Youssef</a></li><li><a href="{pre}ventures.html">Ventures</a></li><li><a href="{pre}courses.html">Courses</a></li><li><a href="{pre}speaking.html">Speaking &amp; mentoring</a></li><li><a href="https://www.linkedin.com/newsletters/the-ai-glittch-7332984165379805188/" target="_blank" rel="noopener">The AI Glittch</a></li><li><a href="https://www.inovasolutions.ai" target="_blank" rel="noopener">Inova AI Solutions</a></li></ul></div>
    </div>
    <div class="f-follow"><a class="fl-li" href="https://www.linkedin.com/in/youssef-jalloul/" target="_blank" rel="noopener me"><svg><use href="#li"/></svg><span><b>Connect on LinkedIn</b><small>Youssef Jalloul</small></span></a><a class="fl-gl" href="https://www.linkedin.com/newsletters/the-ai-glittch-7332984165379805188/" target="_blank" rel="noopener"><img src="{pre}assets/logos/ai-glitch.jpg" alt="" width="1000" height="200" loading="lazy"><span><b>Subscribe to The AI Glittch</b><small>LinkedIn newsletter</small></span></a></div>
    {src}
    <div class="f-bottom"><span>&copy; 2026 Youssef Jalloul. All rights reserved. <a href="{pre}privacy.html">Privacy &amp; cookies</a> &middot; <a href="#" data-cookie-settings>Cookie settings</a></span><span class="f-machine">For machines: <a href="{pre}sitemap.xml">sitemap.xml</a> &middot; <a href="{pre}llms.txt">llms.txt</a> &middot; <a href="{pre}llms-full.txt">llms-full.txt</a> &middot; <a href="{pre}genome.json">genome.json</a> &middot; <a href="{pre}feed.xml">RSS</a></span><span>Sydney &middot; Dubai</span></div>
    <div class="f-anchor"><a class="brand" href="{pre}index.html"><svg class="mark"><use href="#yj"/></svg><span>Youssef Jalloul</span></a></div>
  </div>
</footer>
<div class="fixcta" id="fixcta"><a class="btn btn-primary" href="{pre}book.html">Book a strategy call <svg><use href="#arr"/></svg></a></div>
<script src="{pre}main.js?v={asset_v('main.js')}" integrity="{asset_sri('main.js')}" defer></script>
<script src="{pre}consent.js?v={asset_v('consent.js')}" integrity="{asset_sri('consent.js')}" defer></script>
'''


def render(meta, body, extra_scripts=''):
    path = meta['path']
    depth = path.count('/')
    pre = '../' * depth
    body = body.replace('{{PRE}}', pre)
    out = head(meta, pre) + '\n' + header(meta.get('active', path), pre) + '\n' + body
    if not meta.get('no_bookband'):
        out += '\n' + bookband(pre)
    out += '\n' + footer(pre, meta.get('sources')) + extra_scripts + '\n</body>\n</html>\n'
    out = out.replace(f'href="{pre}index.html"', f'href="{pre or "./"}"')
    out = POST(out)
    dest = os.path.join(DIST, path)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    open(dest, 'w').write(out)
    return path


LOGOMAP = json.load(open(os.path.join(ROOT, 'logomap.json')))


def POST(out):
    """Serve right-sized WebP logos and give every logo explicit dimensions (no layout shift)."""
    for src, v in LOGOMAP.items():
        if len(v) < 5 or src.endswith('.webp'):
            continue
        new, w, h = v[0], v[1], v[2]
        out = out.replace('assets/logos/' + src, 'assets/logos/' + new)
        def dims(m, w=w, h=h):
            tag = m.group(0)
            tag = re.sub(r'\s(width|height)="\d+"', '', tag)
            return tag[:-1].rstrip('/').rstrip() + f' width="{w}" height="{h}">'
        out = re.sub(r'<img\b[^>]*assets/logos/' + re.escape(new) + r'"[^>]*>', dims, out)
    return out


def person_ref():
    return {"@id": SITE + "/#person"}


def breadcrumb(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + '/' + u} for i, (n, u) in enumerate(items)]}


def faq_ld(qas):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub('<[^>]+>', '', a)}} for q, a in qas]}


def load_py(path):
    spec = importlib.util.spec_from_file_location(os.path.basename(path)[:-3], path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---------------- articles ----------------
def parse_article(path):
    raw = open(path).read()
    fm, body = raw.split('\n---\n', 1)
    meta = json.loads(fm)
    md = markdown.Markdown(extensions=['tables', 'sane_lists', 'attr_list'])
    htmlbody = md.convert(body)
    # external links open in a new tab
    htmlbody = re.sub(r'<a href="(https?://[^"]+)">', r'<a href="\1" target="_blank" rel="noopener">', htmlbody)
    meta['html'] = htmlbody
    meta['md'] = body.strip()
    words = len(re.sub('<[^>]+>', ' ', htmlbody).split())
    meta['minutes'] = max(2, round(words / 230))
    return meta


def build():
    if os.path.exists(DIST):
        shutil.rmtree(DIST)
    shutil.copytree(os.path.join(ROOT, 'static'), DIST)
    import covers
    pages = []
    arts = [parse_article(p) for p in glob.glob(os.path.join(ROOT, 'content/insights/*.md'))]
    arts.sort(key=lambda a: (a.get('order', 0)), reverse=True)
    ctx = dict(articles=arts, covers=covers, render=render, SITE=SITE, faq_ld=faq_ld, breadcrumb=breadcrumb, person_ref=person_ref, esc=esc, ROOT=ROOT, TODAY=TODAY)
    for p in sorted(glob.glob(os.path.join(ROOT, 'content/pages/*.py'))):
        if os.path.basename(p) == 'common.py':
            continue
        mod = load_py(p)
        res = mod.build(ctx)
        pages += res if isinstance(res, list) else [res]
    # articles
    import article_page
    for a in arts:
        pages.append(article_page.build(a, ctx))
    write_sitemap(pages, arts)
    write_feed(arts)
    write_llms_full(arts)
    add_img_dims()
    write_csp()
    print('built', len(pages), 'pages')
    return pages


def add_img_dims():
    """Give every local <img> its intrinsic width/height so the browser reserves space before it loads (no layout shift).
    CSS still decides the displayed size; these only set the aspect ratio."""
    from PIL import Image
    cache = {}
    def dims(path):
        if path not in cache:
            try:
                if path.endswith('.svg'):
                    t = open(path).read(2000)
                    m = re.search(r'viewBox="[\d.\-]+ [\d.\-]+ ([\d.]+) ([\d.]+)"', t)
                    cache[path] = (round(float(m.group(1))), round(float(m.group(2)))) if m else None
                else:
                    with Image.open(path) as im:
                        cache[path] = im.size
            except Exception:
                cache[path] = None
        return cache[path]
    for f in glob.glob(os.path.join(DIST, '**', '*.html'), recursive=True):
        src_html = open(f, encoding='utf-8').read()
        def fix(m):
            tag = m.group(0)
            if re.search(r'\swidth=', tag) or re.search(r'\sheight=', tag):
                return tag
            sm = re.search(r'\ssrc="([^"]+)"', tag)
            if not sm or re.match(r'(https?:|data:|//)', sm.group(1)):
                return tag
            d = dims(os.path.normpath(os.path.join(os.path.dirname(f), sm.group(1).split('?')[0])))
            if not d:
                return tag
            return tag[:-1].rstrip('/').rstrip() + f' width="{d[0]}" height="{d[1]}">'
        out = re.sub(r'<img\b[^>]*>', fix, src_html)
        if out != src_html:
            open(f, 'w', encoding='utf-8').write(out)


def write_csp():
    """Hash every inline script on every page and put the list into .htaccess.
    Report-Only for now: violations show in the browser console without blocking anything.
    Swap the header name to Content-Security-Policy once the console is clean."""
    import hashlib, base64
    hashes = set()
    for f in glob.glob(os.path.join(DIST, '**', '*.html'), recursive=True):
        for attrs, body in re.findall(r'<script(\b[^>]*)>(.*?)</script>', open(f, encoding='utf-8').read(), flags=re.S):
            if 'src=' in attrs or 'application/ld+json' in attrs:
                continue
            hashes.add("'sha256-" + base64.b64encode(hashlib.sha256(body.encode('utf-8')).digest()).decode() + "'")
    hashes |= {"'" + asset_sri('main.js') + "'", "'" + asset_sri('consent.js') + "'"}
    policy = ("script-src " + ' '.join(sorted(hashes)) + " 'strict-dynamic' 'unsafe-inline' https: 'report-sample'; "
              "object-src 'none'; base-uri 'none'; frame-ancestors 'self'")
    ht = os.path.join(DIST, '.htaccess')
    t = open(ht).read()
    line = 'Header set Content-Security-Policy-Report-Only "' + policy + '"'
    if '# CSP (generated by build.py)' not in t:
        raise ValueError('static/.htaccess is missing the "# CSP (generated by build.py)" marker')
    open(ht, 'w').write(t.replace('# CSP (generated by build.py)', '# CSP (generated by build.py)\n' + line))


def write_sitemap(pages, arts):
    lm = {('insights/' + a['slug'] + '.html'): a.get('updated') or a.get('date') or TODAY for a in arts}
    urls = []
    for p in sorted(set(pages)):
        if p in ('404.html',):
            continue
        loc = SITE + '/' + ('' if p == 'index.html' else p)
        urls.append(f'  <url><loc>{loc}</loc><lastmod>{lm.get(p, TODAY)}</lastmod></url>')
    open(os.path.join(DIST, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + '\n'.join(urls) + '\n</urlset>\n')


def write_llms_full(arts):
    """One plain-Markdown file with the site summary, quick answers, FAQ and every article, for AI assistants."""
    sys.path.insert(0, os.path.join(ROOT, 'content', 'pages'))
    import index as _ix, inner as _in
    out = [open(os.path.join(ROOT, 'static', 'llms.txt')).read().strip(), '', '---', '', '# Quick answers', '']
    for q, a in _ix.QUICK:
        out += [f'## {q}', '', re.sub('<[^>]+>', '', a), '']
    faq = getattr(_in, 'NEW_FAQ', [])
    if faq:
        out += ['# FAQ', '']
        for item in faq:
            q, a = item[0], item[1]
            out += [f'## {re.sub("<[^>]+>", "", q)}', '', re.sub('<[^>]+>', '', a), '']
    out += ['# Articles', '']
    for a in arts:
        out += ['---', '', f"# {a['title']}", '', f"URL: {SITE}/insights/{a['slug']}.html  ", f"Published: {a.get('date', '')}  ", f"Summary: {a.get('description', '')}", '', a.get('md', ''), '']
    open(os.path.join(DIST, 'llms-full.txt'), 'w').write('\n'.join(out) + '\n')


def write_feed(arts):
    items = []
    for a in arts:
        url = f"{SITE}/insights/{a['slug']}.html"
        d = a.get('date')
        pub = datetime.datetime.strptime(d, '%Y-%m-%d').strftime('%a, %d %b %Y 09:00:00 +1000') if d else ''
        items.append(f"<item><title>{esc(a['title'])}</title><link>{url}</link><guid>{url}</guid>{'<pubDate>'+pub+'</pubDate>' if pub else ''}<description>{esc(a['description'])}</description></item>")
    open(os.path.join(DIST, 'feed.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>The AI Glittch by Youssef Jalloul</title><link>' + SITE + '/insights.html</link><description>Sarcasm, sources and the occasional rogue toaster. Enterprise AI, private AI and governance.</description>' + ''.join(items) + '</channel></rss>\n')


if __name__ == '__main__':
    import sys
    sys.path.insert(0, ROOT)
    build()
