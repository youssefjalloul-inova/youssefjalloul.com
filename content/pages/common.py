"""Helpers shared by page modules: load extracted sections and patch copy safely."""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))


def sec(name):
    return open(os.path.join(HERE, f'_sec_{name}.html')).read()


def sub(html, pairs):
    """Replace each (old, new); fail loudly if old is missing so copy never silently drifts."""
    for old, new in pairs:
        if old not in html:
            raise ValueError('copy anchor not found: ' + old[:80])
        html = html.replace(old, new)
    return html


def relink(html):
    """Old single-page anchors -> new pages."""
    m = {
        'href="#book"': 'href="{{PRE}}book.html"',
        'href="#cases"': 'href="{{PRE}}case-studies.html"',
        'href="#services"': 'href="{{PRE}}services.html"',
        'href="#options"': 'href="{{PRE}}services.html#options"',
        'href="#problem"': 'href="{{PRE}}services.html#problem"',
        'href="#signals"': 'href="{{PRE}}self-check.html"',
        'href="#check"': 'href="{{PRE}}self-check.html"',
        'href="#governance"': 'href="{{PRE}}services.html#governance"',
        'href="ai-readiness-assessment.html"': 'href="{{PRE}}ai-readiness-assessment.html"',
        'href="ai-governance-advisory.html"': 'href="{{PRE}}ai-governance-advisory.html"',
        'href="fractional-chief-ai-officer.html"': 'href="{{PRE}}fractional-chief-ai-officer.html"',
        'src="assets/': 'src="{{PRE}}assets/',
        'href="index.html#book"': 'href="{{PRE}}book.html"',
        'href="index.html#faq"': 'href="{{PRE}}faq.html"',
        'href="index.html#services"': 'href="{{PRE}}services.html"',
        'href="index.html#cases"': 'href="{{PRE}}case-studies.html"',
        'href="index.html#options"': 'href="{{PRE}}services.html#options"',
        'href="index.html#check"': 'href="{{PRE}}self-check.html"',
        'href="index.html#about"': 'href="{{PRE}}about.html"',
        'href="index.html"': 'href="{{PRE}}index.html"',
    }
    for a, b in m.items():
        html = html.replace(a, b)
    return html


def hero_art(key):
    if not key:
        return ''
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    if root not in sys.path:
        sys.path.insert(0, root)
    import covers
    return f'<div class="ph-art ph-{key}" aria-hidden="true"><svg class="cover" viewBox="0 0 1200 630" xmlns="http://www.w3.org/2000/svg">{covers.ART[key]()}</svg></div>'


def phero(eyebrow, h1, lead, crumbs, ctas='', art=''):
    return f'''<section class="phero{' has-art' if art else ''}">
  {hero_art(art)}
  <div class="wrap">
    <p class="crumbs"><a href="{{{{PRE}}}}index.html">Home</a> / {crumbs}</p>
    <span class="eyebrow">{eyebrow}</span>
    <h1>{h1}</h1>
    <p class="answer">{lead}</p>
    {('<div class="cta-row">' + ctas + '</div>') if ctas else ''}
  </div>
</section>'''


SLOGANS = ['No more slop!', 'Does your AI live in someone else’s house?', 'Generic in, generic out.', 'Rent the tools. Own the brand.', 'Content is cheap. Conviction isn’t.', 'Made with AI. Understood by humans.', 'Be the answer, not the ad.', 'Your competitors are using the same prompt.', 'Stop sounding like the default setting.', 'If AI can copy it, it was never your brand.', 'Bring your AI home.']
OWN = ['Does your AI live in someone else’s house?', 'Rent the tools. Own the brand.', 'Who owns your voice: you, or the model?', 'Is your brand renting its personality?', 'If AI can copy it, it was never your brand.', 'Bring your AI home.']
FIND = ['If the AI doesn’t know you, nobody will.', 'Be the answer, not the ad.', 'Google used to find you. Now AI has to recommend you.', 'No more slop!']


def ticker(items=None):
    items = items or SLOGANS
    inner = ''.join(f'<span>{t}</span><i>&#9679;</i>' for t in items)
    return f'<div class="ticker" aria-label="Slogans"><div class="tk-track">{inner}{inner}</div></div>'

def bldr_lockup(white=False, cls=''):
    v = '-white' if white else ''
    return (f'<span class="bl{(" "+cls) if cls else ""}" role="img" aria-label="BLDR">'
            f'<span class="blm{" w" if white else ""}"><img src="{{{{PRE}}}}assets/logos/bldr{v}-markpart.png" alt="" width="112" height="90"><i class="blp" aria-hidden="true"></i></span>'
            f'<img class="blw" src="{{{{PRE}}}}assets/logos/bldr{v}-word.png" alt="" width="189" height="44"></span>')


BLDR_USES = [
    ('Sales teams', 'Agents that log, qualify, forecast and coach while the rep is still on the call.', [('−82%', 'admin work'), ('−34%', 'sales cycle')]),
    ('Education', 'Tutoring and support agents that adapt to each student, in Arabic and English.', [('+312%', 'engagement'), ('↓', 'dropout rates')]),
    ('Procurement', 'Reads supplier licences, checks the ERP, flags at-risk orders and drafts the follow-up for a human to approve.', [('Human', 'signs off'), ('Policy', 'versioned')]),
    ('Government &amp; regulated', 'Policy answerers that cite the source clause, run in-country and log every decision for audit.', [('Local', 'or in-country'), ('Audit', 'every action')]),
]


INOVA_BAND = """<div class="inova-band rv">
      <div class="ib-who"><span class="status st-live">Founder &amp; CEO &middot; 2024&ndash;now</span><h2 class="ib-h">Inova AI Solutions</h2><p>Enterprise AI consultancy, Sydney and Dubai. Inova exists to help enterprises and governments build their own AI, locally, sovereign and governed, instead of renting it. BLDR is how we do it.</p></div>
      <div class="ib-k"><div><b>200+</b><span>AI agents &amp; proofs of concept</span></div><div><b>20x</b><span>internal engineering productivity</span></div><div><b>2</b><span>offices: Sydney and Dubai</span></div></div>
    </div>"""


def bldr_section(ventures=False):
    uses = ''
    for i, (k, d, m) in enumerate(BLDR_USES):
        mets = ''.join(f'<div><b>{a}</b><span>{b}</span></div>' for a, b in m)
        dl = ' d' + str(i) if i else ''
        uses += f'<article class="bu rv{dl}"><span class="bu-k">{k}</span><p>{d}</p><div class="bu-m">{mets}</div></article>'
    return f'''<section class="bldr" id="bldr" aria-labelledby="bldr-h">
  <div class="bldr-glow" aria-hidden="true"></div>
  <div class="wrap">
    <div class="bldr-top rv">
      {bldr_lockup(True, 'big')}
      <span class="bldr-by">The AI Factory &middot; built by {inova_lockup(True)}</span>
    </div>
    {INOVA_BAND if ventures else ''}
    <div class="bldr-grid">
      <div class="bldr-copy">
        <span class="eyebrow rv">The flagship &middot; why Inova exists</span>
        <h2 id="bldr-h" class="rv d1">Everyone has the same AI. <mark class="hl">BLDR lets you build your own.</mark></h2>
        <p class="lead rv d2">BLDR is the sovereign AI operating system I built at Inova AI Solutions. Governments and enterprises use it to build, govern and run AI agents across the systems they already own: on-premise, in-country or in a private cloud. Not in someone else&rsquo;s house.</p>
        <ul class="bldr-pillars rv d3">
          <li><b>Local</b><span>Cloud, hybrid or fully on-premise. The model moves in with you.</span></li>
          <li><b>Sovereign</b><span>Data, prompts and logs stay in your jurisdiction. Arabic and English from day one.</span></li>
          <li><b>Governed</b><span>Human approvals, data classes and versioned policies on every action that matters.</span></li>
        </ul>
        <div class="cta-row rv d4"><a class="btn btn-primary" href="{{{{PRE}}}}book.html">Build your first agent <span aria-hidden="true">&rarr;</span></a><a class="btn btn-ghost" href="https://www.inovasolutions.ai" target="_blank" rel="noopener">inovasolutions.ai &rarr;</a></div>
      </div>
      <div class="bldr-shots rv d2">
        <figure class="shot s1"><div class="shot-bar"><i></i><i></i><i></i><span>BLDR &middot; Approvals</span></div><img src="{{{{PRE}}}}assets/img/bldr-approvals.webp" alt="BLDR console Approvals screen: agent outputs waiting for a human, each with its sources, policy version and data class" width="1800" height="1125" loading="lazy"></figure>
        <figure class="shot s2"><div class="shot-bar"><i></i><i></i><i></i><span>Threads</span></div><img src="{{{{PRE}}}}assets/img/bldr-threads.webp" alt="BLDR console Threads screen: a supplier document agent checking a licence against open purchase orders" width="1800" height="1125" loading="lazy"></figure>
        <span class="shot-tag"><i></i>Human in the loop</span>
      </div>
    </div>
    <h3 class="bldr-uh rv">What it does on a Tuesday</h3>
    <div class="bldr-uses">{uses}</div>
    <p class="bldr-note rv">The toaster gets a job description, a manager and an audit trail. It does not get your data.</p>
  </div>
</section>'''


def bldr_compact():
    """Ventures page: Inova + BLDR in one band. The full BLDR story lives on the home page."""
    return f'''<section class="bldr bldr-compact" id="bldr" aria-labelledby="bldr-h">
  <div class="bldr-glow" aria-hidden="true"></div>
  <div class="wrap">
    <div class="bldr-top rv">
      {bldr_lockup(True, 'big')}
      <span class="bldr-by">The AI Factory &middot; built by {inova_lockup(True)}</span>
    </div>
    {INOVA_BAND}
    <div class="bldr-copy bc-row">
      <div><span class="eyebrow rv">The flagship &middot; why Inova exists</span>
      <h2 id="bldr-h" class="rv d1">BLDR is the <mark class="hl">sovereign AI operating system.</mark></h2></div>
      <div><p class="lead rv d2">Governments and enterprises use it to build, govern and run AI agents across the systems they already own: on-premise, in-country or in a private cloud. Human approvals, data classes, versioned policies and audit trails come built in.</p>
      <div class="cta-row rv d3"><a class="btn btn-primary" href="{{{{PRE}}}}./#bldr">See BLDR at work <span aria-hidden="true">&rarr;</span></a><a class="btn btn-ghost" href="https://www.inovasolutions.ai" target="_blank" rel="noopener">inovasolutions.ai &rarr;</a></div></div>
    </div>
  </div>
</section>'''


def bldr_ld(site):
    return {"@type": "SoftwareApplication", "name": "BLDR", "alternateName": "BLDR by Inova AI Solutions",
            "applicationCategory": "BusinessApplication", "applicationSubCategory": "Sovereign AI operating system",
            "operatingSystem": "Web; cloud, hybrid or on-premise deployment",
            "description": "BLDR is the sovereign AI operating system by Inova AI Solutions. Governments and enterprises use it to build, govern and run AI agents across the systems they already own, on-premise, in-country or in a private cloud, with human approvals, data classes, versioned policies and audit trails.",
            "url": "https://www.inovasolutions.ai", "publisher": {"@type": "Organization", "name": "Inova AI Solutions", "url": "https://www.inovasolutions.ai"},
            "creator": {"@id": site + "/#person"}}



def inova_lockup(white=False, cls=''):
    v = '-white' if white else ''
    return (f'<span class="il{(" "+cls) if cls else ""}" role="img" aria-label="Inova AI Solutions">'
            f'<img class="ilw" src="{{{{PRE}}}}assets/logos/inova{v}-word.png" alt="" width="414" height="121">'
            f'<span class="ilm{" w" if white else ""}"><img src="{{{{PRE}}}}assets/logos/inova{v}-markpart.png" alt="" width="226" height="97"><i class="ilp" aria-hidden="true"></i></span></span>')


LI_URL = "https://www.linkedin.com/in/youssef-jalloul/"
GL_URL = "https://www.linkedin.com/newsletters/the-ai-glittch-7332984165379805188/"


def glitch_logo(cls=''):
    src = '{{PRE}}assets/logos/ai-glitch.jpg'
    return (f'<span class="gx{(" "+cls) if cls else ""}" role="img" aria-label="The AI Glittch">'
            f'<img src="{src}" alt="" width="1000" height="200" loading="lazy">'
            f'<i class="gx-a" style="background-image:url({src})"></i><i class="gx-b" style="background-image:url({src})"></i><i class="gx-s"></i></span>')


def follow_btns():
    return (f'<a class="btn btn-primary" href="{GL_URL}" target="_blank" rel="noopener">Subscribe to The AI Glittch <svg><use href="#arr"/></svg></a>'
            f'<a class="btn btn-ghost btn-li" href="{LI_URL}" target="_blank" rel="noopener me"><svg><use href="#li"/></svg>Follow me on LinkedIn</a>')


def glittch_banner(eyebrow='The newsletter', h='Sarcasm, sources and the occasional rogue toaster.', p='The AI Glittch is my LinkedIn newsletter for leaders who have to make AI decisions this quarter, not next decade. One question per issue. Straight answers. Receipts attached.'):
    return f'''<div class="glt rv">
      <div class="glt-logo">{glitch_logo('big')}</div>
      <div class="glt-copy"><span class="eyebrow">{eyebrow}</span><h3>{h}</h3><p>{p}</p><div class="cta-row">{follow_btns()}</div></div>
    </div>'''
