"""Courses page: the YJ Ventures course ladder (Not on the Syllabus, SideGig, MainGig Playbook)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from common import phero, relink, ticker

LI_URL = 'https://www.linkedin.com/in/youssef-jalloul/'

COURSES = [
    dict(
        key='nots', step='01', move='Start it', name='Not on the Syllabus', short='NOTS',
        status=('st-live', 'Launching first'),
        line='What you don’t learn at school.',
        promise='From idea to <mark class="hl">something real</mark> in one day.',
        who='Uni students, 18 to 24, with an idea and a laptop. You use AI for essays. Time to build with it.',
        gets=['Your brand universe: story, hero, villain, audience', 'Logo, colours, type and a simple design system',
              'Your first product: a digital product, service or course', 'A live website on your own domain',
              'On-brand images and short videos, made with free tools', 'A launch kit: offer, price and first posts'],
        time='A few focused hours. Spread them over a week if you like.',
        price='A$149', founding='A$99 for the first 50 students',
        extra='First Lessons Guarantee',
    ),
    dict(
        key='sidegig', step='02', move='Fit it around work', name='SideGig', short='SideGig',
        status=('st-built', 'Up next'),
        line='Keep the job. Build your thing.',
        promise='From idea to launch in <mark class="hl">five evenings.</mark>',
        who='People 25 to 35 with a day job, a skill from that job and an idea for something on the side.',
        gets=['Three side-gig options built from what you already do at work', 'A clean setup with your day job: contract, time, tools',
              'Brand, look and feel, and a first offer priced for your hours', 'A website, payments and a 7-day launch kit',
              'Your first 10 customers from people who already know you'],
        time='Five evenings of about 2 hours, or one weekend.',
        price='A$149', founding='A$99 for the first 50 students',
        extra='Launch Guarantee',
    ),
    dict(
        key='maingig', step='03', move='Grow it', name='MainGig Playbook', short='MainGig',
        status=('st-past', 'In the studio'),
        line='Turn the side thing into the main thing.',
        promise='A growth plan you can <mark class="hl">actually run.</mark>',
        who='People who already run a side gig and want to grow it. SideGig and NOTS graduates first.',
        gets=['A growth diagnosis: website score, numbers and riskiest assumptions', 'Your brand genome rebuilt from real customer evidence',
              'Your Flaming Corner: the small group you can own first', 'Competitor ad intelligence from the Meta Ad Library',
              'Your first ads, built with you and reviewed before they spend', 'A Growth Strategy and Action Plan, plus a weekly review routine'],
        time='8 modules, 32 core lessons, 3 bonus modules. At your pace.',
        price='A$499', founding='A$349 for the first 50 seats',
        extra='Monthly group growth clinic',
    ),
]


def card(c, i):
    gets = ''.join(f'<li>{g}</li>' for g in c['gets'])
    d = ' d1' if i == 1 else (' d2' if i == 2 else '')
    return f'''<article class="crs rv{d}" id="{c['key']}">
      <div class="crs-cover"><img src="{{{{PRE}}}}assets/img/courses/{c['key']}.webp" alt="{c['name']} course cover" width="800" height="450" loading="lazy"></div>
      <div class="crs-b">
        <div class="crs-top"><span class="crs-step"><b>{c['step']}</b>{c['move']}</span><span class="status {c['status'][0]}">{c['status'][1]}</span></div>
        <h3>{c['name']}</h3>
        <p class="crs-line">{c['line']}</p>
        <p class="crs-promise">{c['promise']}</p>
        <p class="crs-who"><span>For</span>{c['who']}</p>
        <ul class="crs-gets">{gets}</ul>
        <div class="crs-meta">
          <p><span>Time</span>{c['time']}</p>
          <p><span>Price</span><b>{c['price']}</b> &middot; founding price {c['founding']}</p>
          <p><span>Plus</span>1-hour review with me or my team &middot; {c['extra']}</p>
        </div>
      </div>
    </article>'''


def build(ctx):
    cards = ''.join(card(c, i) for i, c in enumerate(COURSES))
    body = phero('Courses by YJ Ventures', 'Three courses. <span class="grad">One ladder.</span>',
                 'The same AI setup I use to build brands for governments and companies, packed into self-paced courses for people building their own. Start it at uni. Fit it around a job. Grow it into the main thing. Claude or ChatGPT does the heavy lifting. You keep the brand.',
                 'Courses',
                 f'<a class="btn btn-primary" href="#ladder">Find your course <svg><use href="#arr"/></svg></a><a class="btn btn-ghost btn-li" href="{LI_URL}" target="_blank" rel="noopener me"><svg><use href="#li"/></svg>Get launch news on LinkedIn</a>')
    body += ticker(['No more slop!', 'Hours, not semesters.', 'Keep the job. Build your thing.', 'Turn the side thing into the main thing.', 'Made with AI. Understood by humans.', 'Someday is not a launch date.'])
    body += f'''
<section class="sec" id="ladder">
  <div class="wrap">
    <div class="sec-head"><div class="rv"><span class="eyebrow">The ladder</span><h2>Pick the rung <mark class="hl">you&rsquo;re standing on.</mark></h2></div>
    <p class="lead rv d1">Each course hands you real things with your name on them, not notes. Finish one, and the next one is already waiting. Skip ahead if you&rsquo;re already there.</p></div>
    <div class="crs-grid">{cards}</div>
  </div>
</section>
<section class="sec alt" id="how">
  <div class="wrap">
    <div class="sec-head"><div class="rv"><span class="eyebrow">How every course works</span><h2>Built like my client work. <mark class="hl">Sized for one person.</mark></h2></div>
    <p class="lead rv d1">The villain here is not a company or a competitor. It&rsquo;s Someday: the launch date that never arrives. Every course is designed to beat it.</p></div>
    <div class="steps steps-3">
      <div class="step rv"><div class="dot">01</div><h4>Install the skills once</h4><p>You get my skills as one package. Install it in Claude (recommended) or ChatGPT and the AI builds with you, in your voice and your brand.</p><p class="out">Out: <b>an AI that knows your brand</b></p></div>
      <div class="step rv d1"><div class="dot">02</div><h4>Short lessons, real outputs</h4><p>Every video is under 3 minutes and every lesson has a written guide with screenshots. Paste the prompt, check the result, save your progress.</p><p class="out">Out: <b>something you can show</b></p></div>
      <div class="step rv d2"><div class="dot">03</div><h4>A human checks your work</h4><p>Every buyer gets a 1-hour review with me or my team. Questions get answered by real people, not a chatbot with a smile.</p><p class="out">Out: <b>a second pair of eyes</b></p></div>
    </div>
  </div>
</section>
<section class="sec" id="course-faq">
  <div class="wrap">
    <div class="sec-head"><div class="rv"><span class="eyebrow">Questions</span><h2>Before you <mark class="hl">grab a seat.</mark></h2></div>
    <p class="lead rv d1">Straight answers. If yours isn&rsquo;t here, ask me on LinkedIn.</p></div>
    <div class="faq rv">
      <details><summary>When can I join?<i></i></summary><div class="a">Not on the Syllabus opens first, then SideGig, then the MainGig Playbook. Launch dates and founding seats are announced on <a href="{LI_URL}" target="_blank" rel="noopener me" style="text-decoration:underline">LinkedIn</a> first. Courses are sold and hosted on Whop under YJ Ventures.</div></details>
      <details><summary>Do I need to know how to code?<i></i></summary><div class="a">No. You need a laptop, a paid Claude or ChatGPT plan and a few focused hours. The AI writes the code; the lessons show you exactly what to paste and what to check.</div></details>
      <details><summary>Which course should I start with?<i></i></summary><div class="a">At uni, or just graduated, with an idea: Not on the Syllabus. Working a job and building on the side: SideGig. Already selling something and ready to grow it: the MainGig Playbook.</div></details>
      <details><summary>Will I make money?<i></i></summary><div class="a">I don&rsquo;t promise income, and you should be wary of anyone who does. What I promise is the setup: you leave with a brand, an offer and the tools to launch it. The rest is the fun part, and it&rsquo;s yours.</div></details>
      <details><summary>Is this for my company?<i></i></summary><div class="a">The courses are for individuals building their own thing. If your organisation needs private, governed AI, that&rsquo;s my day job: <a href="{{{{PRE}}}}book.html" style="text-decoration:underline">book a strategy call</a>.</div></details>
    </div>
  </div>
</section>'''
    ld = {"@context": "https://schema.org", "@graph": [
        ctx['breadcrumb']([('Home', ''), ('Courses', 'courses.html')]),
        {"@type": "ItemList", "name": "Courses by Youssef Jalloul (YJ Ventures)", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "item": {
                "@type": "Course", "name": c['name'], "description": c['line'] + ' ' + c['who'],
                "url": ctx['SITE'] + '/courses.html#' + c['key'],
                "provider": {"@type": "Organization", "name": "YJ Ventures", "sameAs": ctx['SITE']},
                "instructor": ctx['person_ref'](), "inLanguage": "en"}} for i, c in enumerate(COURSES)]},
        ctx['faq_ld']([
            ('Do I need to know how to code?', 'No. You need a laptop, a paid Claude or ChatGPT plan and a few focused hours.'),
            ('Which course should I start with?', 'At uni with an idea: Not on the Syllabus. Working a job and building on the side: SideGig. Already selling and ready to grow: the MainGig Playbook.'),
        ])]}
    meta = dict(path='courses.html', title='AI Courses: Not on the Syllabus, SideGig, MainGig | Youssef Jalloul',
                description='Self-paced AI courses by Youssef Jalloul: Not on the Syllabus for students, SideGig for side projects, MainGig Playbook to grow one.',
                og_image=ctx['SITE'] + '/assets/img/og-courses.jpg', og_alt='Not on the Syllabus, SideGig and MainGig Playbook course covers',
                jsonld=ld)
    return ctx['render'](meta, relink(body))
