import datetime


def fmt_date(d):
    if not d:
        return None
    return datetime.datetime.strptime(d, '%Y-%m-%d').strftime('%-d %B %Y')


def card(a, covers, pre=''):
    date = fmt_date(a.get('date')) or 'The AI Glittch'
    return f'''<a class="ins-card rv" href="{pre}insights/{a['slug']}.html">
  <div class="ins-art">{covers.cover(a['art'])}</div>
  <div class="ins-b"><span class="ins-k">{a['kicker']}</span><h3>{a['title']}</h3><p>{a['description']}</p><span class="ins-m">{date} &middot; {a['minutes']} min read</span></div>
</a>'''


def build(a, ctx):
    covers, SITE, esc = ctx['covers'], ctx['SITE'], ctx['esc']
    path = f"insights/{a['slug']}.html"
    url = f"{SITE}/{path}"
    date = fmt_date(a.get('date'))
    origin = a.get('origin') == 'linkedin'
    posting = {
        "@type": "BlogPosting", "@id": url + "#article", "headline": a['title'], "description": a['description'],
        "url": url, "mainEntityOfPage": url, "inLanguage": "en",
        "author": {"@type": "Person", "@id": SITE + "/#person", "name": "Youssef Jalloul", "url": SITE + "/about.html"},
        "publisher": {"@type": "Person", "@id": SITE + "/#person", "name": "Youssef Jalloul"},
        "image": f"{SITE}/assets/og/{a['slug']}.jpg",
        "isPartOf": {"@type": "Blog", "name": "The AI Glittch", "url": SITE + "/insights.html"},
    }
    if a.get('date'):
        posting["datePublished"] = a['date']
        posting["dateModified"] = a.get('updated', a['date'])
    graph = [posting, ctx['breadcrumb']([('Home', ''), ('Insights', 'insights.html'), (a['title'], path)])]
    faq_html = ''
    if a.get('faq'):
        graph.append(ctx['faq_ld'](a['faq']))
        faq_html = '<section class="post-faq"><h2>Quick answers</h2>' + ''.join(f'<details><summary>{q}<i></i></summary><div class="a">{ans}</div></details>' for q, ans in a['faq']) + '</section>'
    meta = dict(path=path, title=(a['title'] if len(a['title']) > 52 else f"{a['title']} | Youssef Jalloul"), description=a.get('meta_description', a['description']), active='insights.html', og_alt=a['title'],
                published=a.get('date'), modified=a.get('updated', a.get('date')),
                og_type='article', og_title=a['title'], og_image=f"{SITE}/assets/og/{a['slug']}.jpg", jsonld={"@context": "https://schema.org", "@graph": graph})
    others = [o for o in ctx['articles'] if o['slug'] != a['slug']][:3]
    note = ('<p class="post-origin">First published in <a href="https://www.linkedin.com/newsletters/the-ai-glittch-7332984165379805188/" target="_blank" rel="noopener">The AI Glittch</a> on LinkedIn' + (f' on {date}' if date else '') + '. Republished here with light edits. Comments and hot takes live over there.</p>') if origin else ''
    body = f'''<article class="post">
  <header class="post-hero">
    <div class="wrap post-wrap">
      <p class="crumbs"><a href="../">Home</a> / <a href="../insights.html">Insights</a></p>
      <span class="eyebrow">{a['kicker']}</span>
      <h1>{a['title']}</h1>
      <p class="post-dek">{a['description']}</p>
      <div class="post-by"><img src="../assets/img/portrait.webp" alt="Youssef Jalloul" width="48" height="48"><span><b>Youssef Jalloul</b><small>{(f'<time datetime="{a["date"]}">{date}</time> · ') if date else ''}{a['minutes']} min read</small></span></div>
    </div>
    <div class="wrap post-cover">{covers.cover(a['art'])}</div>
  </header>
  <div class="wrap post-wrap post-body">
    {a['html']}
    {faq_html}
    <div class="next-step">
      <span class="eyebrow">Where are you right now?</span>
      <div class="ns-grid">
        <a href="../self-check.html"><b>Not sure it’s your problem yet?</b><span>Take the 2-minute self-check &rarr;</span></a>
        <a href="../private-ai.html"><b>Know the problem, comparing fixes?</b><span>Read the private AI guide &rarr;</span></a>
        <a href="../case-studies.html"><b>Want proof it works?</b><span>See the receipts &rarr;</span></a>
        <a class="ns-go" href="../book.html"><b>Ready to bring your AI home?</b><span>Book a strategy call &rarr;</span></a>
      </div>
    </div>
    <div class="post-follow">
      <a class="pf-logo" href="https://www.linkedin.com/newsletters/the-ai-glittch-7332984165379805188/" target="_blank" rel="noopener" aria-label="The AI Glittch on LinkedIn"><span class="gx" role="img" aria-label="The AI Glittch"><img src="../assets/logos/ai-glitch.jpg" alt="" width="1000" height="200" loading="lazy"><i class="gx-a" style="background-image:url(../assets/logos/ai-glitch.jpg)"></i><i class="gx-b" style="background-image:url(../assets/logos/ai-glitch.jpg)"></i><i class="gx-s"></i></span></a>
      <div><span class="eyebrow">Liked this one?</span><h3>Get the next one before your toaster does.</h3><p>New issues of The AI Glittch land on LinkedIn first. Subscribe there, and follow me for the bits too short for a newsletter.</p>
      <div class="cta-row"><a class="btn btn-primary" href="https://www.linkedin.com/newsletters/the-ai-glittch-7332984165379805188/" target="_blank" rel="noopener">Subscribe to The AI Glittch <svg><use href="#arr"/></svg></a><a class="btn btn-ghost btn-li" href="https://www.linkedin.com/in/youssef-jalloul/" target="_blank" rel="noopener me"><svg><use href="#li"/></svg>Follow on LinkedIn</a></div></div>
    </div>
    {note}
    <div class="post-sign"><img src="../assets/img/portrait.webp" alt="" width="64" height="64"><div><b>Youssef Jalloul</b><p>AI entrepreneur and venture builder. Builds private, governed AI for boards, executives and governments. Writes The AI Glittch. Has never trusted a toaster.</p></div></div>
  </div>
</article>
<section class="sec more-ins">
  <div class="wrap">
    <div class="rv"><span class="eyebrow">Keep reading</span><h2 style="margin-top:14px">More from <mark class="hl">the AI Glittch.</mark></h2></div>
    <div class="ins-grid">{''.join(card(o, covers, '../') for o in others)}</div>
  </div>
</section>'''
    return ctx['render'](meta, body)
