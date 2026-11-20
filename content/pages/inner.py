"""Inner pages: services, case studies, ventures, speaking, about, self-check, FAQ, book, insights index, guides."""
import re, os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
from common import sec, sub, relink, phero, ticker, FIND, bldr_section, bldr_compact, bldr_ld, glittch_banner

HERE = os.path.dirname(os.path.abspath(__file__))


def strip_section_head(html):
    """Drop a section's own eyebrow/h2/lead block (the page hero replaces it)."""
    return re.sub(r'<div class="sec-head">.*?</div>\s*</div>', '', html, count=1, flags=re.S) if False else html


def services(ctx):
    problem = sub(sec('problem'), [
        ('<h2>Four failure modes explain <mark class="hl">most stalled</mark> AI programmes.</h2>', '<h2>Four ways AI programmes die. <mark class="hl">None of them is the model.</mark></h2>'),
        ('It is rarely the model. Industry research keeps landing on the same causes, and each one has a fix that is organisational before it is technical.',
         'Your AI didn’t fail because the model was dumb. It failed because nobody owned it, the data wasn’t ready, legal turned up late and nobody changed how the work gets done. All four are fixable. None of them by buying another licence.'),
    ])
    who = sub(sec('who'), [
        ('<h2>Leaders with <mark class="hl">a mandate, a budget</mark> and a problem to solve.</h2>', '<h2>Built for leaders with <mark class="hl">a mandate, a budget</mark> and a toaster problem.</h2>'),
        ('Typically 200 to 20,000 employees, a leadership team that owns the P&amp;L, and an AI agenda that is moving faster than its governance. Corporates, regulated industries and government.',
         '200 to 20,000 people. A leadership team that owns the P&amp;L. An AI agenda moving faster than its governance. Corporates, regulated industries and government. If that’s you, keep reading.'),
    ])
    options = sub(sec('options'), [
        ("<h2>Four ways to get AI leadership. Here's how they compare.</h2>", '<h2>Four ways to get AI leadership. <mark class="hl">One of them is me.</mark></h2>'),
        ('An honest comparison, including where each option is the wrong choice. Short definitions first, then the table.', 'An honest comparison, including the rows where I lose. Short definitions first, then the table.'),
    ])
    svc = sub(sec('services'), [
        ('<h2>Strategy you can <mark class="hl">defend.</mark> Systems you can <mark class="hl">run.</mark></h2>', '<h2>Strategy you can defend. Systems you can run. <mark class="hl">Appliances that stay in their lane.</mark></h2>'),
        ('Independent advice at the top, delivery capacity through Inova underneath. You can buy one engagement or the whole chain.', 'Six services, three moves. Independent advice at the top, delivery through Inova underneath. Buy one, or the whole chain.'),
        ('<article class="svc-i rv"><span class="num">01</span>', '<article class="svc-i rv" id="break"><span class="num">01 &middot; Break</span>'),
        ('<article class="svc-i rv d1"><span class="num">02</span>', '<article class="svc-i rv d1"><span class="num">02 &middot; Break</span>'),
        ('<article class="svc-i rv"><span class="num">03</span>', '<article class="svc-i rv"><span class="num">03 &middot; Break</span>'),
        ('<article class="svc-i rv d1"><span class="num">04</span>', '<article class="svc-i rv d1" id="build"><span class="num">04 &middot; Build</span>'),
        ('<article class="svc-i rv"><span class="num">05</span>', '<article class="svc-i rv"><span class="num">05 &middot; Build</span>'),
        ('<article class="svc-i rv d1"><span class="num">06</span>', '<article class="svc-i rv d1" id="outside"><span class="num">06 &middot; Think outside</span>'),
        ('<h3>How an engagement runs</h3>\n      <p>The same four moves whether it\'s a 4-week diagnostic or a two-year transformation.</p>',
         '<h3>How an engagement runs</h3>\n      <p>Same four steps whether it’s a 4-week diagnostic or a two-year transformation. No 80-slide decks were harmed.</p>'),
    ])
    svc = svc.replace('<h3>Local &amp; Sovereign AI Architecture</h3>', '<h3><a href="{{PRE}}private-ai.html">Local &amp; Sovereign AI Architecture</a></h3>')
    gov = sub(sec('governance'), [
        ("<h2>Governance isn't the brake. It's what lets you <mark class=\"hl\">go faster.</mark></h2>", '<h2>Governance isn’t a policy PDF. <mark class="hl">It’s the lock on the fridge.</mark></h2>'),
        ('Enterprise buyers, regulators and insurers increasingly ask one question: how do you govern your AI? Organisations that can answer with evidence close deals, pass reviews and scale pilots without a legal stop.',
         'Enterprise buyers, regulators and insurers keep asking one question: how do you govern your AI? “We have a policy somewhere” is not an answer. Evidence is. Organisations that can show it close deals, pass reviews and scale pilots without a legal handbrake.'),
    ])
    body = phero('Out of the box is old news. Build a new one.', 'Break the box. Build a new one. <span class="grad">Then think outside that one.</span>',
                 'I help boards, executives and governments get AI out of someone else’s house and into production: readiness and governance to break the old box, private agents and sovereign AI to build the new one, and venture building to think outside it.',
                 'Services', '<a class="btn btn-primary" href="{{PRE}}book.html">Book a strategy call <svg><use href="#arr"/></svg></a><a class="btn btn-ghost" href="#options">Compare your options</a>', art='trio')
    body += '\n'.join([svc, problem, who, options, gov])
    meta = dict(path='services.html', title='AI Services: Readiness, Governance & Private AI | Youssef Jalloul',
                description='AI readiness, AI governance (ISO 42001, EU AI Act, NIST), fractional Chief AI Officer, agentic AI, sovereign AI and corporate venture building.',
                jsonld={"@context": "https://schema.org", "@graph": [ctx['breadcrumb']([('Home', ''), ('Services', 'services.html')])]},
                sources='Compensation and retainer ranges: Christian &amp; Timbers 2026 Corporate AI Compensation Study. Other comparison cells are qualitative. Governance guidance is advisory and not legal advice.')
    return ctx['render'](meta, relink(body))


def case_studies(ctx):
    cases = sub(sec('cases'), [
        ('<h2>AI in production, with <mark class="hl">numbers attached.</mark></h2>', '<h2>Receipts, <mark class="hl">not renders.</mark></h2>'),
        ('Delivered through Inova AI Solutions across fintech, education, government, adtech and financial services in Australia, the Gulf and Asia-Pacific.',
         'Six systems in production across fintech, education, government, adtech and financial services, delivered through Inova AI Solutions in Australia, the Gulf and Asia-Pacific.'),
    ])
    body = phero('Case studies', 'AI in production. <span class="grad">Numbers attached.</span>',
                 'From live translation in 120+ languages for a Saudi government directorate to drone-based detection on a 6,751 km border: real systems, real clients, measured outcomes. No demos dressed up as deployments.', 'Case studies', art='agents')
    body += cases + sec('government')
    meta = dict(path='case-studies.html', title='AI Case Studies With Real Numbers | Youssef Jalloul',
                description='Enterprise and government AI in production: 94% lower translation cost, 96% identification accuracy, ad production cut from a week to 15 minutes.',
                jsonld={"@context": "https://schema.org", "@graph": [ctx['breadcrumb']([('Home', ''), ('Case studies', 'case-studies.html')])]},
                sources='Case-study metrics are as reported by Inova AI Solutions for its client engagements.')
    return ctx['render'](meta, relink(body))


STEALTH_V = '''<article class="v rv v-stealth"><div class="v-logo"><span class="stealth-tile" aria-hidden="true"><svg viewBox="0 0 24 24"><rect x="5" y="11" width="14" height="10" rx="2.5" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M8 11V8a4 4 0 0 1 8 0v3" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg></span></div><span class="status st-built">In stealth</span><h3>Healthcare AI</h3><p>An AI product for clinics. In build. More when it is ready.</p></article>'''


def ventures(ctx):
    raw = sec('ventures')
    arts = {re.search(r'<h3>(.*?)</h3>', m).group(1): m for m in re.findall(r'<article class="v[ "].*?</article>', raw, re.S)}
    def card(k):
        return arts[k].replace('class="v v-feature rv"', 'class="v rv"')
    tech = [k for k in arts if k.startswith('Digital transformation')][0]
    torch = card('Torch Academy').replace('<span class="status st-built">Board member · GM · 2015–2020</span>', '<span class="status st-past">Board member · GM · 2015–2020</span>')
    techc = card(tech)
    toko = card('Toko · Beat2Beat').replace('backed by La French Tech, INSEAD Launchpad and Station F.', 'backed by INSEAD Launchpad, Station F, 10x, the French Ministry of the Economy and La French Tech.')
    toko = toko.replace('<div class="sup"><img src="assets/logos/insead.png" alt="INSEAD Launchpad"><img src="assets/logos/stationf.png" alt="Station F"><img src="assets/logos/frenchtech.png" alt="La French Tech"></div>',
                        '<div class="sup"><img src="assets/logos/insead.png" alt="INSEAD Launchpad"><img src="assets/logos/stationf.png" alt="Station F"><span class="sup-t" title="10x accelerator">10x</span><img src="assets/logos/minefi.png" alt="French Ministry of the Economy and Finance"><img src="assets/logos/frenchtech.png" alt="La French Tech"></div>')
    assert 'sup-t' in toko and 'st-past' in torch and 'st-past' in techc
    faces = card('Gus') + card('Ikraa') + STEALTH_V
    earlier = torch + techc + toko + card('VIP Rescue')
    body = phero('Ventures', 'Built. Operated. <span class="grad">Exited.</span>',
                 'One flagship that helps governments and enterprises run their own AI, a new line of AI products, and the companies before them. Several sold.', 'Ventures', art='house')
    body += bldr_compact()
    body += f'''<section class="sec vt-tier" id="products">
  <div class="wrap">
    <div class="sec-head"><div class="rv"><span class="eyebrow">Products with faces</span><h2>Built in-house. <mark class="hl">One live, one launching, one in stealth.</mark></h2></div>
    <p class="lead rv d1">Each one is a working answer to &ldquo;does your AI live in someone else&rsquo;s house?&rdquo; in small business, education and healthcare.</p></div>
    <div class="vent vent-3">{faces}</div>
  </div>
</section>
<section class="sec alt vt-tier" id="earlier">
  <div class="wrap">
    <div class="sec-head"><div class="rv"><span class="eyebrow">Earlier ventures &amp; exits</span><h2>I&rsquo;ve carried <mark class="hl">the P&amp;L</mark> myself.</h2></div>
    <p class="lead rv d1">Advice lands differently from someone who has raised the money, shipped the product and sold the company. Several times. These are the scars behind the opinions.</p></div>
    <div class="vent vent-2">{earlier}</div>
  </div>
</section>'''
    ld = {"@context": "https://schema.org", "@graph": [ctx['breadcrumb']([('Home', ''), ('Ventures', 'ventures.html')]), bldr_ld(ctx['SITE'])]}
    meta = dict(path='ventures.html', title='Ventures: Inova, BLDR and Exits | Youssef Jalloul',
                description='Inova AI Solutions and BLDR, the sovereign AI operating system; Gus and Ikraa; plus Torch Academy, *.Technology and exits from Toko and VIP Rescue.',
                jsonld=ld)
    return ctx['render'](meta, relink(body))


def speaking(ctx):
    st = sub(sec('stage'), [
        ('<p>I write it, you read it on LinkedIn. Subscribe to get new issues as they land.</p>', '<p>Sarcasm, sources and the occasional rogue toaster. Every issue also lives here on <a href="{{PRE}}insights.html" style="text-decoration:underline">Insights</a>.</p>'),
    ])
    st = st.replace('<h2>On stage, in the room, and <mark class="hl">behind founders.</mark></h2>', '<h2>Topics, stages and <mark class="hl">the founders I back.</mark></h2>')
    st = st.replace('<li>Enterprise AI strategy: from pilots to production</li>', '<li>Does your AI live in someone else’s house? Private AI for boards</li><li>Enterprise AI strategy: from pilots to production</li>')
    st = st.replace('<li>Building ventures inside corporates and ecosystems</li>', '<li>Building ventures inside corporates and ecosystems</li><li>The Generative Brand: brand strategy in the age of AI slop</li>')
    body = phero('Speaking &amp; mentoring', 'On stage, in the room, <span class="grad">behind founders.</span>',
                 'Keynotes, panels and board briefings on private AI, governance, agents and building ventures. Expect sarcasm, sources and at least one appliance.', 'Speaking',
                 '<a class="btn btn-primary" href="{{PRE}}book.html">Invite me to speak <svg><use href="#arr"/></svg></a>', art='microwave')
    body += st
    meta = dict(path='speaking.html', title='Speaking on Private AI & Governance | Youssef Jalloul',
                description='Keynotes on private AI, AI governance and agents. Stages include STEP Dubai, UBT Jeddah, ASCAME, Canadian University Dubai and ESA Beirut.',
                jsonld={"@context": "https://schema.org", "@graph": [ctx['breadcrumb']([('Home', ''), ('Speaking', 'speaking.html')])]})
    return ctx['render'](meta, relink(body))


def about(ctx):
    ab = sec('about')
    ab = sub(ab, [
        ('<span class="eyebrow rv">About</span>', '<span class="eyebrow rv">About Youssef &middot; synthetic at the edges, human at the core</span>'),
        ('<h2 class="rv">Two decades where', '<h1 class="rv ab-h">Two decades where'),
        ('commerce</mark> meet.</h2>', 'commerce</mark> meet.</h1>'),
        ('<p class="rv"><strong>I\'m a technology entrepreneur and venture builder.</strong>',
         '<p class="rv"><strong>Why:</strong> I believe the most powerful technology of our lifetime shouldn’t be rented from someone who can read it. Everything below is how I earned the right to say that.</p>\n      <p class="rv"><strong>I\'m a technology entrepreneur and venture builder.</strong>'),
        ('<dd>Inova AI Solutions (founder, CEO, chairman); Toko (CMO) and VIP Rescue (co-founder), both exited; Torch Academy; *.Technology</dd>', '<dd>Inova AI Solutions (founder and CEO); Toko (CMO) and VIP Rescue (co-founder) among several exits; Torch Academy; *.Technology</dd>'),
    ]) if 'both exited' in ab else sub(ab, [
        ('<span class="eyebrow rv">About</span>', '<span class="eyebrow rv">About Youssef &middot; synthetic at the edges, human at the core</span>'),
        ('<h2 class="rv">Two decades where', '<h1 class="rv ab-h">Two decades where'),
        ('commerce</mark> meet.</h2>', 'commerce</mark> meet.</h1>'),
        ('<p class="rv"><strong>I\'m a technology entrepreneur and venture builder.</strong>',
         '<p class="rv"><strong>Why:</strong> I believe the most powerful technology of our lifetime shouldn’t be rented from someone who can read it. Everything below is how I earned the right to say that.</p>\n      <p class="rv"><strong>I\'m a technology entrepreneur and venture builder.</strong>'),
    ])
    ab = ab.replace('<section class="sec alt" id="about">', '<section class="sec" id="about" style="padding-top:150px">')
    ab = sub(ab, [('<span class="cap">Sydney · Dubai</span></div>', '<span class="cap">Sydney · Dubai</span><a class="btn btn-ghost btn-li pt-li" href="https://www.linkedin.com/in/youssef-jalloul/" target="_blank" rel="noopener me"><svg><use href="#li"/></svg>Connect on LinkedIn</a></div>')])
    person = {"@type": "ProfilePage", "@id": ctx['SITE'] + '/about.html', "mainEntity": {"@type": "Person", "@id": ctx['SITE'] + "/#person", "name": "Youssef Jalloul", "image": ctx['SITE'] + '/assets/img/portrait.webp',
              "jobTitle": "Founder and CEO, Inova AI Solutions", "worksFor": {"@type": "Organization", "name": "Inova AI Solutions", "url": "https://www.inovasolutions.ai"},
              "alumniOf": [{"@type": "CollegeOrUniversity", "name": "Monash University", "sameAs": "https://www.monash.edu"}, {"@type": "CollegeOrUniversity", "name": "American University of Beirut", "sameAs": "https://www.aub.edu.lb"}],
              "sameAs": ["https://www.linkedin.com/in/youssef-jalloul/", "https://www.linkedin.com/newsletters/the-ai-glittch-7332984165379805188/"]}}
    meta = dict(path='about.html', title='About Youssef Jalloul | AI Entrepreneur & Tech Venture Builder',
                description='Youssef Jalloul, founder and CEO of Inova AI Solutions. AI entrepreneur and venture builder, 20+ years, MBA (Monash), BBA (AUB), Ethics4AI co-author.',
                jsonld={"@context": "https://schema.org", "@graph": [person, ctx['breadcrumb']([('Home', ''), ('About', 'about.html')])]})
    return ctx['render'](meta, relink(ab))


def self_check(ctx):
    sg = sub(sec('signals'), [
        ('<h2>Eight quiet signs AI is <mark class="hl">already your problem.</mark></h2>', '<h2>Eight signs your toaster is <mark class="hl">already reading your board papers.</mark></h2>'),
        ('<h3>How ready is your organisation, really?</h3>', '<h1 class="ck-h">Is your AI ready, or just rented? <span class="grad">Find out in 2 minutes.</span></h1>'),
        ('Eight yes/no questions. You get a score, your biggest gaps and a suggested next step. Nothing you answer is stored or sent anywhere.',
         'Eight yes/no questions. A score, your biggest gaps and the next move. Nothing you answer is stored or sent anywhere. Unlike, you know, some chatbots.'),
        ('<section class="sec" id="signals">', '<section class="sec" id="signals" style="padding-top:150px">'),
    ])
    # put the check first: move <div class="check rv" id="check"> block to top of wrap
    m = re.search(r'\n\s*<div class="check rv" id="check">.*?\n    </div>\n  </div>\n</section>', sg, re.S)
    chk = re.search(r'<div class="check rv" id="check">.*?\n    </div>(?=\n  </div>\n</section>)', sg, re.S).group(0)
    sg = sg.replace(chk, '')
    sg = sg.replace('<div class="wrap">', '<div class="wrap">\n    ' + chk + '\n    <div style="height:90px"></div>', 1)
    meta = dict(path='self-check.html', title='Free 2-Minute AI Readiness Self-Check | Youssef Jalloul',
                description='A free 2-minute AI readiness self-check: eight yes/no questions on ownership, data, governance and adoption. Get a score, your gaps and a next step.',
                jsonld={"@context": "https://schema.org", "@graph": [ctx['breadcrumb']([('Home', ''), ('Self-check', 'self-check.html')])]},
                sources='Statistics: MIT Project NANDA (2025); Roland Berger Middle East (Feb 2026); IBM 2026 CEO Study as reported.')
    return ctx['render'](meta, relink(sg))


NEW_FAQ = [
    ('Is ChatGPT safe for company data?', 'It depends on the plan and what people paste. Business tiers such as ChatGPT Enterprise have stronger controls than free personal accounts, but the bigger risk is staff using personal accounts the company can’t see. Australia’s privacy regulator recommends keeping personal and sensitive information out of publicly available generative AI tools. <a href="insights/is-chatgpt-safe-for-company-data.html">Full answer</a>.'),
    ('What is private AI?', 'AI where the models, the data you send them and the logs they keep run somewhere your organisation controls: your own servers, an in-country cloud region or a dedicated private tenant. <a href="private-ai.html">The private AI guide</a>.'),
    ('How do we stop employees pasting confidential data into AI tools?', 'Not with a ban. Give people an approved tool that’s better than the one they’d sneak in, enforce company sign-in, keep the most sensitive work on private models, and keep governance evidence. <a href="insights/how-to-stop-employees-pasting-data-into-ai.html">The seven moves</a>.'),
]


def faq(ctx):
    f = sec('faq')
    f = sub(f, [('<h2 style="margin-top:18px"><mark class="hl">Straight answers.</mark></h2>', '<h1 style="margin-top:18px;font-size:clamp(2.4rem,5vw,4.2rem)">Straight answers. <mark class="hl">No toaster involved.</mark></h1>'),
                ('<section class="sec" id="faq">', '<section class="sec" id="faq" style="padding-top:150px">')])
    extra = ''.join(f'<details><summary>{q}<i></i></summary><div class="a">{a}</div></details>' for q, a in NEW_FAQ)
    f = f.replace('<div class="faq rv">', '<div class="faq rv">' + extra, 1)
    qas = re.findall(r'<summary>(.*?)<i></i></summary><div class="a">(.*?)</div>', f)
    meta = dict(path='faq.html', title='AI FAQ: Private AI, Governance, ChatGPT Safety',
                description='Straight answers on private AI, ChatGPT and company data, AI readiness, ISO 42001, the EU AI Act and what a fractional Chief AI Officer costs.',
                jsonld={"@context": "https://schema.org", "@graph": [dict(ctx['faq_ld'](qas), **{"@id": ctx['SITE'] + '/faq.html#faq'}), ctx['breadcrumb']([('Home', ''), ('FAQ', 'faq.html')])]})
    return ctx['render'](meta, relink(f))


def book(ctx):
    b = sub(sec('book'), [
        ('<section class="sec alt" id="book">', '<section class="sec alt bk-page" id="book">'),
        ('<span class="eyebrow">Book a strategy call</span>\n      <h2>', '<span class="eyebrow">Book a strategy call</span>\n      <h1 class="bk-h">'),
        ('<mark class="hl">a direction.</mark></h2>', '<mark class="hl">a direction.</mark></h1>'),
        ("Pick a time that suits you. We'll talk through where AI sits in your organisation today, what's blocking it, and whether I'm the right person to help.",
         'Pick a time. We’ll talk about where your AI lives today, what’s blocking it, and whether I’m the right person to help. No pitch deck. No toaster.'),
    ])
    meta = dict(path='book.html', title='Book a Strategy Call | Youssef Jalloul', no_bookband=True,
                description='Book a 45-minute strategy call with Youssef Jalloul on private AI, AI governance, readiness or a board brief. Leave with the right first move.',
                jsonld={"@context": "https://schema.org", "@graph": [ctx['breadcrumb']([('Home', ''), ('Book a call', 'book.html')])]})
    return ctx['render'](meta, relink(b))


def insights(ctx):
    import article_page
    arts = ctx['articles']
    new = [a for a in arts if a.get('origin') == 'site']
    old = [a for a in arts if a.get('origin') != 'site']
    lead = arts[0]
    body = phero('The AI Glittch', 'Dispatches from <span class="grad">the appliance uprising.</span>',
                 'Google used to find you. Now AI has to recommend you. So every article here answers one real question, every number has a source, and every toaster is under surveillance. Be the answer, not the ad.', 'Insights',
                 '<a class="btn btn-primary" href="https://www.linkedin.com/newsletters/the-ai-glittch-7332984165379805188/" target="_blank" rel="noopener">Subscribe on LinkedIn <svg><use href="#arr"/></svg></a><a class="btn btn-ghost" href="{{PRE}}feed.xml">RSS</a>', art='magnifier')
    body += f'''<section class="sec ins-sec">
  <div class="wrap">
    <div class="rv"><span class="eyebrow">Questions buyers ask</span><h2 style="margin:14px 0 34px">Straight answers, <mark class="hl">no slop.</mark></h2></div>
    <div class="ins-grid">{''.join(article_page.card(a, ctx['covers'], '') for a in new)}</div>
    <div style="margin-top:90px">{glittch_banner('Never miss an issue', 'Get the next answer before your toaster does.', 'New issues of The AI Glittch land on LinkedIn first: one real question, straight answers, sources attached and a little sarcasm. Subscribe to the newsletter and follow me for the bits too short for an issue.')}</div>
    <div class="rv"><span class="eyebrow">From the newsletter</span><h2 style="margin:14px 0 34px">The AI Glittch <mark class="hl">archive.</mark></h2></div>
    <div class="ins-grid">{''.join(article_page.card(a, ctx['covers'], '') for a in old)}</div>
  </div>
</section>''' + ticker(FIND)
    blog = {"@type": "Blog", "@id": ctx['SITE'] + '/insights.html', "name": "The AI Glittch", "author": {"@id": ctx['SITE'] + '/#person'},
            "blogPost": [{"@type": "BlogPosting", "headline": a['title'], "url": f"{ctx['SITE']}/insights/{a['slug']}.html"} for a in arts]}
    meta = dict(path='insights.html', title='Insights: The AI Glittch | Youssef Jalloul',
                description='Answer-first articles on private AI, ChatGPT and company data, shadow AI and governance, plus the full archive of The AI Glittch newsletter.',
                jsonld={"@context": "https://schema.org", "@graph": [blog, ctx['breadcrumb']([('Home', ''), ('Insights', 'insights.html')])]})
    return ctx['render'](meta, body)


def guides(ctx):
    out = []
    for g in ['ai-governance-advisory', 'ai-readiness-assessment', 'fractional-chief-ai-officer']:
        main = open(os.path.join(HERE, f'_guide_{g}.html')).read()
        title, desc = open(os.path.join(HERE, f'_guide_{g}.meta')).read().split('\n', 1)
        import html as _h
        title, desc = _h.unescape(title).replace(' | Youssef Jalloul', ''), _h.unescape(desc)
        jl = open(os.path.join(HERE, f'_guide_{g}.json')).read()
        main = main.replace('href="index.html#book"', 'href="book.html"').replace('Book a strategy call', 'Book a strategy call')
        main = re.sub(r'<section class="psec[^"]*">\s*<div class="wrap">\s*<div class="pcta.*?</section>', '', main, flags=re.S)
        out.append(ctx['render'](dict(path=f'{g}.html', title=title, description=desc.strip(), jsonld=jl.strip(), active='services.html'), relink(main)))
    return out


def notfound(ctx):
    body = phero('404', 'The toaster ate <span class="grad">this page.</span>', 'It was here a minute ago. Then Toastie said “sure, stranger!” and now it’s gone. Try one of these instead.', '404',
                 '<a class="btn btn-primary" href="{{PRE}}index.html">Home <svg><use href="#arr"/></svg></a><a class="btn btn-ghost" href="{{PRE}}insights.html">Insights</a><a class="btn btn-ghost" href="{{PRE}}book.html">Book a call</a>', art='toaster')
    return ctx['render'](dict(path='404.html', title='Page not found | Youssef Jalloul', description='This page was eaten by a toaster.', robots='noindex'), body)



COOKIES = [
    ('yj-consent', 'This site (local storage)', 'Strictly necessary', 'Remembers your cookie choices', 'Until you change them or clear your browser'),
    ('_ga, _ga_&lt;id&gt;', 'Google Analytics 4', 'Analytics', 'Counts visits and how pages are used, with IP anonymised', 'Up to 2 years'),
    ('_clck, _clsk, CLID, MUID', 'Microsoft Clarity', 'Analytics', 'Heatmaps and session insights, with text input masked', '1 day to 1 year'),
    ('_fbp, fr', 'Meta Pixel (Facebook, Instagram)', 'Advertising', 'Measures ad campaigns and builds audiences on Meta platforms', 'Up to 3 months'),
    ('_gcl_au, IDE, test_cookie', 'Google Ads / Google tag', 'Advertising', 'Measures conversions from Google ads and supports remarketing', 'Up to 13 months'),
    ('Calendly cookies', 'Calendly (booking page only)', 'Functional, third party', 'Runs the booking calendar when you open it', 'Set by Calendly; see its policy'),
]

REGIONS = [
    ('European Union, EEA and Switzerland', 'GDPR, the ePrivacy Directive and Switzerland’s revised FADP. Non-essential cookies need your prior, opt-in consent. You can ask for access, correction, erasure, restriction, portability, object to processing and withdraw consent at any time, and complain to your local data protection authority.'),
    ('United Kingdom', 'UK GDPR, the Data Protection Act 2018 and PECR. Same rights as the EU. You can complain to the Information Commissioner’s Office (ICO).'),
    ('United States', 'The California Consumer Privacy Act as amended by the CPRA, and comparable state laws (including Virginia, Colorado, Connecticut, Utah, Texas, Oregon and others). You can ask to know, delete and correct personal information and opt out of its “sale” or “sharing” for cross-context behavioural advertising. I do not sell personal information for money. Advertising tags may count as “sharing”, so they stay off unless you accept them, and a Global Privacy Control signal is treated as an opt-out. I will not discriminate against you for using these rights.'),
    ('Australia', 'The Privacy Act 1988 and the Australian Privacy Principles. You can access and correct your information and complain to the Office of the Australian Information Commissioner (OAIC).'),
    ('United Arab Emirates and Saudi Arabia', 'The UAE Personal Data Protection Law (Federal Decree-Law 45 of 2021), the DIFC and ADGM data protection regimes where they apply, and Saudi Arabia’s Personal Data Protection Law. You can be informed, access, correct and request deletion of your data, and withdraw consent.'),
    ('Canada', 'PIPEDA and Quebec’s Law 25: consent for non-essential tracking, access, correction and withdrawal of consent.'),
    ('Brazil, and everywhere else', 'Brazil’s LGPD, and similar laws such as Singapore’s PDPA, India’s DPDP Act, Japan’s APPI, South Africa’s POPIA and New Zealand’s Privacy Act 2020. Wherever you are, you get the strictest standard on this page: nothing that tracks you runs until you say yes.'),
]


def privacy(ctx):
    rows = ''.join(f'<tr><td><code>{a}</code></td><td>{b}</td><td>{c}</td><td>{d}</td><td>{e}</td></tr>' for a, b, c, d, e in COOKIES)
    regs = ''.join(f'<details><summary>{h}<i></i></summary><div class="a">{t}</div></details>' for h, t in REGIONS)
    body = phero('Privacy &amp; cookies', 'Your data. <span class="grad">Your house. Your rules.</span>',
                 'I preach private AI, so this site practises it. Nothing that tracks you loads until you say yes, &ldquo;Reject all&rdquo; is one click, and you can change your mind any time.', 'Privacy &amp; cookies',
                 '<a class="btn btn-primary" href="#" data-cookie-settings>Change cookie settings <svg><use href="#arr"/></svg></a>')
    body += f'''<section class="sec legal">
  <div class="wrap legal-w">
    <p class="legal-meta">Last updated 12 November 2026</p>
    <h2>The short version</h2>
    <ul>
      <li>One global standard: opt-in consent for every visitor, everywhere, before any analytics or advertising cookie is set.</li>
      <li>Analytics (Google Analytics 4, Microsoft Clarity) and advertising (Meta Pixel, Google Ads) are separate choices. You can accept one and not the other.</li>
      <li>Google Consent Mode v2 starts every visit at &ldquo;denied&rdquo;. Global Privacy Control is honoured as an opt-out of advertising.</li>
      <li>I do not sell your personal information. I do not use cookies to make decisions about you.</li>
      <li>Right now no analytics or advertising tags are switched on, so the site sets no tracking cookies at all. If that changes, this page and the cookie banner will tell you first.</li>
    </ul>

    <h2>Who is responsible</h2>
    <p>This website, youssefjalloul.com, is run by Youssef Jalloul (&ldquo;I&rdquo;, &ldquo;me&rdquo;), who is the data controller for the information described here. Contact for anything privacy-related: <a href="mailto:privacy@example.com">privacy@example.com</a>. Work delivered through Inova AI Solutions is covered by Inova&rsquo;s own privacy terms.</p>

    <h2>What I collect</h2>
    <ul>
      <li><b>Technical data</b> your browser sends to any website (IP address, browser, device, pages requested), kept briefly in my host&rsquo;s security logs.</li>
      <li><b>Usage data</b>, only if you accept analytics: pages viewed, clicks, scrolls and approximate location (country or city). Clarity masks text you type.</li>
      <li><b>Advertising identifiers</b>, only if you accept advertising: cookie IDs that let Meta and Google measure and target ads.</li>
      <li><b>What you choose to share</b> when you book a call through Calendly (name, email, notes). Calendly processes this under its own privacy policy.</li>
    </ul>

    <h2>Why, and on what legal basis</h2>
    <ul>
      <li>Running and securing the site: legitimate interests (and strict necessity for the consent record).</li>
      <li>Analytics and advertising: your consent, which you can withdraw at any time.</li>
      <li>Replying to you and holding a call you booked: taking steps at your request, and legitimate interests.</li>
    </ul>

    <h2>Cookies and similar technologies</h2>
    <div class="legal-t"><table><thead><tr><th>Name</th><th>Provider</th><th>Category</th><th>Purpose</th><th>Duration</th></tr></thead><tbody>{rows}</tbody></table></div>
    <p>Tags only run once their IDs are configured and you have consented. Third parties (Google, Microsoft, Meta, Calendly) process data under their own policies and may transfer it outside your country.</p>

    <h2>Your choices</h2>
    <ul>
      <li>Use <a href="#" data-cookie-settings>Cookie settings</a> at any time; it also sits at the bottom of every page.</li>
      <li>Turn on Global Privacy Control in your browser and advertising stays off automatically.</li>
      <li>Opt out at source: <a href="https://tools.google.com/dlpage/gaoptout" target="_blank" rel="noopener">Google Analytics opt-out</a>, <a href="https://adssettings.google.com" target="_blank" rel="noopener">Google ad settings</a>, <a href="https://www.facebook.com/adpreferences" target="_blank" rel="noopener">Meta ad preferences</a>.</li>
    </ul>

    <h2>Your rights, wherever you are</h2>
    <div class="qa-wrap legal-r">{regs}</div>

    <h2>Transfers, retention and security</h2>
    <p>Data may be processed in Australia, the UAE, the EU, the US and other countries where my providers operate. Where the law requires it, transfers rely on adequacy decisions, standard contractual clauses or equivalent safeguards. Analytics data is kept for no more than 14 months, consent records for as long as your choice applies, and booking details for as long as we are in conversation plus any period the law requires.</p>

    <h2>Children</h2>
    <p>This site is for professionals and is not directed at children. I do not knowingly collect children&rsquo;s data.</p>

    <h2>Changes and complaints</h2>
    <p>If this policy changes in a way that affects your choices, the cookie banner will ask you again. To use any right above, email <a href="mailto:privacy@example.com">privacy@example.com</a>; I reply within 30 days. You can also complain to your local regulator.</p>
  </div>
</section>'''
    meta = dict(path='privacy.html', title='Privacy & Cookie Policy | Youssef Jalloul',
                description='How youssefjalloul.com handles cookies and personal data: opt-in consent worldwide, GDPR, CCPA/CPRA, Australian Privacy Act, UAE and Saudi PDPL, and more.',
                jsonld={"@context": "https://schema.org", "@graph": [ctx['breadcrumb']([('Home', ''), ('Privacy & cookies', 'privacy.html')])]})
    return ctx['render'](meta, relink(body))


def build(ctx):
    return [services(ctx), case_studies(ctx), ventures(ctx), speaking(ctx), about(ctx), self_check(ctx), faq(ctx), book(ctx), insights(ctx), notfound(ctx), privacy(ctx)] + guides(ctx)
