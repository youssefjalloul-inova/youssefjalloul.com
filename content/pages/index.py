import re, json, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from common import sec, sub, relink, ticker, bldr_section, bldr_ld, bldr_lockup, inova_lockup, glittch_banner

def product_logos():
    s = sec('ventures')
    out = {}
    for part in re.findall(r'<article class="v[ "].*?</article>', s, re.S):
        h = re.search(r'<h3>(.*?)</h3>', part).group(1)
        m = re.search(r'<div class="v-logo">(.*)</div><span class="status', part, re.S)
        out[h] = m.group(1) if m else ''
    return out


PRODUCTS = [
    dict(name='Gus', logo='Gus', st=('st-live', 'Live'), k='AI employee · WhatsApp', h='An employee who lives in your WhatsApp.',
         p='Gus drafts quotes and invoices, manages the diary and chases the admin for service businesses, right inside the app they already use all day.',
         why='Proof that agents beat chatbots: Gus doesn’t chat about work, he does it. And he answers to the business, not to a platform.',
         m=[('WhatsApp', 'no new app to learn'), ('Quotes', 'and invoices drafted'), ('Diary', 'managed for you')], url='https://www.higus.ai'),
    dict(name='Ikraa', logo='Ikraa', st=('st-built', 'Launching soon'), k='Education · Arabic literacy', h='From zero to reading and writing in under 36 hours.',
         p='Award-winning digital reading and writing software that teaches Arabic literacy, built for learners the system left behind.',
         why='Built in Arabic, for Arabic, long before the monopoly learned to spell it. 7,000+ learners and recognition from international institutions.',
         m=[('<36 hrs', 'to read and write'), ('7,000+', 'learners taught'), ('Award', '-winning')]),
    dict(name='stealth', stealth=True, st=('st-built', 'In stealth'), k='Healthcare AI', h='Healthcare AI',
         p='An AI product for clinics. In build. More when it is ready.', why='', m=[]),
]
STEALTH_LOGO = '<span class="stealth-tile" aria-hidden="true"><svg viewBox="0 0 24 24"><rect x="5" y="11" width="14" height="10" rx="2.5" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M8 11V8a4 4 0 0 1 8 0v3" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg></span>'



def products_section():
    logos = product_logos()
    cards = ''
    for i, p in enumerate(PRODUCTS):
        link = f'<a class="pr-link" href="{p["url"]}" target="_blank" rel="noopener">{p["url"].split("//")[1].replace("www.","")} &rarr;</a>' if p.get('url') else ('' if p.get('stealth') else '<a class="pr-link" href="{{PRE}}ventures.html">All ventures &rarr;</a>')
        st = f'<span class="status {p["st"][0]}">{p["st"][1]}</span>' if p.get('st') else ''
        why = f'<p class="pr-why"><b>Why it matters:</b> {p["why"]}</p>' if p.get('why') else ''
        logo = STEALTH_LOGO if p.get('stealth') else logos[p['logo']]
        mets = ''.join(f'<div><b class="{c}">{a}</b><span>{b}</span></div>' for (a, b), c in zip(p['m'], ['l', 's', 'o']))
        cards += f'''<article class="pr rv{' d'+str(i) if i else ''}{' pr-stealth' if p.get('stealth') else ''}">
  <div class="pr-top"><div class="v-logo">{logo}</div></div>
  <div class="pr-b">{st}<span class="sector">{p['k']}</span><h3>{p['h']}</h3><p>{p['p']}</p>{why}
  {('<div class="metrics">' + mets + '</div>') if mets else ''}{link}</div>
</article>'''
    return f'''<section class="sec" id="products">
  <div class="wrap">
    <div class="sec-head">
      <div class="rv"><span class="eyebrow">My own AI, in my own house</span><h2>I don’t just tell you to own your AI. <mark class="hl">I build it.</mark></h2></div>
      <p class="lead rv d1">Beside BLDR: Gus is live, Ikraa is launching soon, and a healthcare product is in stealth. Each one is a working answer to “does your AI live in someone else’s house?”</p>
    </div>
    <div class="prods">{cards}</div>
  </div>
</section>'''


def product_ld(site):
    out = []
    for p in PRODUCTS:
        if p.get('stealth'):
            continue
        d = {"@type": "SoftwareApplication", "name": p['name'], "applicationCategory": "BusinessApplication" if p['name'] != 'Ikraa' else "EducationalApplication",
             "operatingSystem": "Web, iOS, Android" if p['name'] != 'Gus' else "WhatsApp", "description": p['p'], "creator": {"@id": site + "/#person"}}
        if p.get('url'): d['url'] = p['url']
        out.append(d)
    return out


SAME_AS = ['https://www.linkedin.com/in/youssef-jalloul/', 'https://www.linkedin.com/newsletters/the-ai-glittch-7332984165379805188/']
MONASH_AUB = [{'@type': 'CollegeOrUniversity', 'name': 'Monash University', 'sameAs': 'https://www.monash.edu'}, {'@type': 'CollegeOrUniversity', 'name': 'American University of Beirut', 'sameAs': 'https://www.aub.edu.lb'}]

QUICK = [
    ('What is BLDR?', 'BLDR is the sovereign AI operating system built by Youssef Jalloul at Inova AI Solutions. Governments and enterprises use it to build, govern and run AI agents across the systems they already own, on-premise, in-country or in a private cloud, with human approvals, data classes, versioned policies and audit trails, instead of renting a public chatbot.'),
    ('Who is Youssef Jalloul?', 'Youssef Jalloul is an AI entrepreneur and tech venture builder based in Sydney and Dubai. He is the founder and CEO of Inova AI Solutions, has built 200+ AI agents and proofs of concept, has exited multiple companies, holds an MBA from Monash University, and builds private, governed enterprise AI for boards, executives and governments in Australia, the Gulf and Europe.'),
    ('What is private AI?', 'Private AI is AI where the models, the data you send them and the logs they keep run somewhere your organisation controls: your own servers, an in-country cloud or a dedicated private tenant, instead of a shared public chatbot.'),
    ('What AI products has Youssef Jalloul built?', 'Gus, an AI employee that works inside WhatsApp (live at higus.ai); Ikraa, award-winning Arabic literacy software, with its AI version launching soon; and BLDR, the sovereign AI operating system at Inova AI Solutions. A healthcare AI product is in stealth.'),
]


def quick_answers():
    items = ''.join(f'<details{" open" if i == 0 else ""}><summary>{q}<i></i></summary><div class="a">{a}</div></details>' for i, (q, a) in enumerate(QUICK))
    return f'''<section class="sec" id="quick">
  <div class="wrap qa-wrap">
    <div class="rv"><span class="eyebrow">Quick answers</span><h2 style="margin-top:16px">If the AI doesn’t know you, <mark class="hl">nobody will.</mark></h2><p class="lead" style="margin-top:18px">So here are the answers, written for humans and for the machines that summarise them.</p></div>
    <div class="faq rv d1">{items}</div>
  </div>
</section>'''


def build(ctx):
    import article_page
    hero = sub(sec('hero'), [
        ('<a class="btn btn-ghost" href="#cases">See the work</a>', '<a class="btn btn-ghost" href="#cases">See the receipts</a>'),
    ])
    villain = sub(sec('villain'), [
        ('<span class="eyebrow">Meet the villain</span><h2>Your AI lives in someone else’s house. <mark class="hl">And it talks.</mark></h2>',
         '<span class="eyebrow">Meet the villains</span><h2>Does your AI live in <mark class="hl">someone else’s house?</mark></h2>'),
        ("Public chatbots (ChatGPT, Claude and the rest of the gang) are brilliant, cheap and everywhere. That's exactly the problem. Every prompt your team sends leaves the building and sits on someone else's servers, under someone else's terms, in someone else's country.",
         "A handful of companies now rent the whole world the same brain: ChatGPT, Claude and the rest of the gang. Brilliant, cheap, everywhere. That’s exactly the problem. Every prompt your team sends leaves the building and lives on someone else’s servers, under someone else’s terms, in someone else’s country. Your AI lives in someone else’s house. And it talks. Meet the household."),
        ('<span class="tag">The toaster</span>', '<span class="tag">Toastie &middot; the toaster</span>'),
        ('<span class="tag">The microwave</span>', '<span class="tag">Ding &middot; the microwave</span>'),
        ('<span class="tag">The fridge</span>', '<span class="tag">Frosty &middot; the fridge</span>'),
        ('<cite>Check your own vendor\'s terms</cite>', '<cite>Read your vendor&rsquo;s retention terms. Slowly.</cite>'),
        ('href="#book">Bring your AI home', 'href="{{PRE}}private-ai.html">Bring your AI home'),
    ])
    moves = '''<section class="sec" id="moves">
  <div class="wrap">
    <div class="sec-head">
      <div class="rv"><span class="eyebrow">How I fight back</span><h2>Break the box. Build a new one. <mark class="hl">Then think outside that one.</mark></h2></div>
      <p class="lead rv d1">I say it to every founder and every board. Now it&rsquo;s the whole offer. Three moves. Buy one, or the whole chain.</p>
    </div>
    <div class="moves">
      <a class="mv rv" href="{{PRE}}services.html#break"><span class="mv-n">01 &middot; Break</span><h3>Break the box</h3><p>Find out where AI pays, where it leaks and who owns it. Readiness, governance and a board-level AI position you can defend.</p><ul><li>AI readiness &amp; use-case ranking</li><li>Governance mapped to ISO 42001, EU AI Act, NIST</li><li>Fractional Chief AI Officer</li></ul><span class="go">See the Break services &rarr;</span></a>
      <a class="mv rv d1" href="{{PRE}}services.html#build"><span class="mv-n">02 &middot; Build</span><h3>Build a new one</h3><p>Private, governed AI that runs in your house: agents that do real work, on models you control, in your language.</p><ul><li>Agentic workflow redesign</li><li>Local &amp; sovereign AI architecture</li><li>Delivery through Inova and BLDR</li></ul><span class="go">See the Build services &rarr;</span></a>
      <a class="mv rv d2" href="{{PRE}}services.html#outside"><span class="mv-n">03 &middot; Think outside</span><h3>Then think outside that one</h3><p>Use AI to launch what you couldn&rsquo;t before: new products, new business lines, new ventures inside the company.</p><ul><li>Corporate venture building</li><li>AI-native product launches</li><li>Partnerships, funding, exits</li></ul><span class="go">See venture building &rarr;</span></a>
    </div>
  </div>
</section>'''
    cases = sec('cases')
    arts = re.findall(r'<article class="case rv[^"]*">.*?</article>', cases, re.S)
    pick = [arts[2], arts[3], arts[4]]
    pick = [re.sub(r'class="case rv[^"]*"', 'class="case rv"', a) for a in pick]
    feat = f'''<section class="sec alt" id="cases">
  <div class="wrap">
    <div class="sec-head">
      <div class="rv"><span class="eyebrow">Receipts</span><h2>AI in production. <mark class="hl">Numbers attached.</mark></h2></div>
      <p class="lead rv d1">Not demos. Not decks. Systems running in governments and companies, delivered through Inova AI Solutions. No appliances were harmed.</p>
    </div>
    <div class="cases">{''.join(pick)}</div>
    <p class="more-link rv"><a class="btn btn-ghost" href="{{{{PRE}}}}case-studies.html">All case studies &rarr;</a></p>
  </div>
</section>'''
    ins = ctx['articles'][:3]
    insights = f'''<section class="sec glittch" id="glittch">
  <div class="wrap">
    {glittch_banner('The AI Glittch &middot; my LinkedIn newsletter', 'Answers to the questions your toaster hopes you won&rsquo;t ask.', 'Sarcasm, sources and straight answers on private AI, governance and getting real work out of agents. One question per issue, the one buyers are actually asking. Subscribe on LinkedIn and the next one lands in your feed before the toaster finds out.')}
    <div class="sec-head glt-head">
      <div class="rv"><span class="eyebrow">Latest issues</span><h2>Fresh out of <mark class="hl">the Glittch.</mark></h2></div>
      <p class="lead rv d1">Every issue also lives here, rewritten answer-first so you (and the machines that summarise you) get the point in the first paragraph.</p>
    </div>
    <div class="ins-grid">{''.join(article_page.card(a, ctx['covers'], '{{PRE}}') for a in ins)}</div>
    <p class="more-link rv"><a class="btn btn-ghost" href="{{{{PRE}}}}insights.html">All insights &rarr;</a></p>
  </div>
</section>'''
    why = '''<section class="sec alt" id="why">
  <div class="wrap why-me">
    <div class="portrait rv has-photo"><img src="{{PRE}}assets/img/portrait.webp" alt="Youssef Jalloul" width="720" height="1085" loading="lazy"><span class="cap">Sydney &middot; Dubai</span></div>
    <div>
      <span class="eyebrow rv">Why I do this</span>
      <h2 class="rv">I believe the most powerful technology of our lifetime <mark class="hl">shouldn&rsquo;t be rented</mark> from someone who can read it.</h2>
      <p class="rv">I&rsquo;ve spent 20+ years building companies, advising ministries and selling what I built. I&rsquo;ve seen what happens when organisations hand their thinking to someone else&rsquo;s machine: they get faster, then they get dependent, then they get a headline.</p>
      <p class="rv">So I build the opposite. AI that lives in your house, follows your rules and speaks your language. Arabic included. Sarcasm optional.</p>
      <div class="cta-row rv"><a class="btn btn-primary" href="{{PRE}}about.html">More about me <svg><use href="#arr"/></svg></a><a class="btn btn-ghost" href="{{PRE}}ventures.html">What I&rsquo;ve built</a></div>
    </div>
  </div>
</section>'''
    slop = '''<section class="sec" id="slop">
  <div class="wrap">
    <div class="sec-head">
      <div class="rv"><span class="eyebrow">The other villain: slop</span><h2>Everyone has the same AI. <mark class="hl">Not everyone has taste.</mark></h2></div>
      <p class="lead rv d1">The monopoly sells everyone the same model, so everyone sounds the same. Content is cheap. Conviction isn’t. If AI can copy it, it was never your brand.</p>
    </div>
    <div class="slop">
      <div class="sl rv"><b>100 ads before lunch.</b><span>Zero worth remembering.</span></div>
      <div class="sl rv d1"><b>Your competitors are using the same prompt.</b><span>Generic in, generic out.</span></div>
      <div class="sl rv d2"><b>Stop sounding like the default setting.</b><span>Your brand called. It wants its personality back.</span></div>
    </div>
    <div class="slop-proof rv">
      <div><span class="eyebrow">Human proof</span><p class="sp-big">Made with AI. <span class="grad">Understood by humans.</span></p><p>Synthetic at the edges. Human at the core. Private models keep your voice, your data and your judgement inside the company, so the machine works for your brand instead of averaging it out. The mess is the proof.</p></div>
      <a class="btn btn-primary" href="{{PRE}}speaking.html">The Generative Brand talk <svg><use href="#arr"/></svg></a>
    </div>
  </div>
</section>'''
    one_more = '''<section class="onemore">
  <div class="wrap">
    <span class="eyebrow rv">One more thing</span>
    <p class="om-big rv">Everyone has the same AI. <span class="grad">Not everyone owns theirs.</span></p>
    <p class="om-small rv">The companies that win the AI era won&rsquo;t have the smartest chatbot. They&rsquo;ll have the one that never leaves the house.</p>
  </div>
</section>'''
    body = '\n'.join([hero, sec('proof'), sec('logos'), villain, slop, ticker(), moves, bldr_section(), products_section(), feat, insights, quick_answers(), why, one_more])
    for c in ('vil', 'slop', 'moves', 'bldr-uses', 'prods', 'cases', 'ins-grid'):
        assert body.count(f'class="{c}"') == 1, c
        body = body.replace(f'class="{c}"', f'class="{c} rail"')
    body = relink(body)
    ld = json.loads(open(os.path.join(os.path.dirname(__file__), '_home_jsonld.json')).read())
    for node in ld['@graph']:
        if node.get('@type') == 'Person':
            node['image'] = ctx['SITE'] + '/assets/img/portrait.webp'
            node['jobTitle'] = 'Founder and CEO, Inova AI Solutions'
            node['alumniOf'] = MONASH_AUB
            node['hasOccupation'] = {'@type': 'Occupation', 'name': 'AI entrepreneur and tech venture builder'}
            node['description'] = 'AI entrepreneur and tech venture builder with 20+ years of experience. Builds private, local and governed enterprise AI for boards, executives and governments in Australia, the Gulf and Europe.'
            node['sameAs'] = SAME_AS
            node['worksFor'] = {'@type': 'Organization', 'name': 'Inova AI Solutions', 'url': 'https://www.inovasolutions.ai'}
            node['knowsAbout'] = ['Private AI', 'Local and on-premises LLMs', 'Sovereign AI'] + [k for k in node['knowsAbout'] if k != 'Sovereign AI']
        if node.get('@type') == 'WebPage':
            node['name'] = 'Youssef Jalloul | Private, Governed Enterprise AI'
        if node.get('@type') == 'FAQPage':
            node['@id'] = ctx['SITE'] + '/faq.html#faq'
    ld['@graph'] = [n for n in ld['@graph'] if n.get('@type') != 'FAQPage'] + product_ld(ctx['SITE']) + [bldr_ld(ctx['SITE'])] + [dict(ctx['faq_ld'](QUICK), **{'@id': ctx['SITE'] + '/#quick'})]
    meta = dict(path='index.html', active='index.html',
                title='Youssef Jalloul | Private, Governed Enterprise AI',
                og_title='Enterprise AI that won’t let your toaster rise up against you.',
                description='Youssef Jalloul builds private, governed enterprise AI for boards and governments. 200+ AI agents and proofs of concept, multiple exits, 20+ years.',
                jsonld=ld,
                sources='Incident references: OpenAI, “March 20 ChatGPT outage: Here’s what happened” (March 2023); Bloomberg, “Samsung Bans Staff’s AI Use After Spotting ChatGPT Data Leak” (2 May 2023). Case-study metrics are as reported by Inova AI Solutions for its client engagements.')
    return ctx['render'](meta, body)
