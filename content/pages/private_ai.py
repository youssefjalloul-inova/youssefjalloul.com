import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from common import phero, relink, ticker, OWN

FAQ = [
    ('What is private AI?', 'Private AI is AI where the models, the data you send them and the logs they keep run in an environment your organisation controls: your own servers, an in-country cloud region or a dedicated private tenant, instead of a shared public chatbot.'),
    ('Is private AI the same as sovereign AI?', 'They overlap. Private AI is about control: who can see and keep your data. Sovereign AI adds jurisdiction: the data, models and compute stay inside a specific country and under its laws. A government ministry usually needs both.'),
    ('Do we have to give up ChatGPT, Claude or Copilot?', 'No. Most organisations run a hybrid: governed cloud tools for low-risk work, private models for confidential and regulated work. The point is choosing where each job runs on purpose.'),
    ('Are open-source models good enough for enterprise work?', 'For most business tasks (summarising, drafting, extraction, searching your own documents and agents running defined workflows) current open-weight models are good enough once they are connected to your data and tested. Frontier cloud models still lead on the hardest open-ended reasoning.'),
    ('What does private AI cost?', 'More to set up than a subscription, often less to run at volume. The cost drivers are compute (owned or reserved), engineering, and governance. A focused first use case can be live in 8 to 16 weeks.'),
    ('Can private AI work in Arabic?', 'Yes. Arabic-first agents on BLDR and a 120+ language translation platform for a Saudi government directorate were built this way, with models and hosting chosen for Arabic and in-region data rules.'),
]


def build(ctx):
    cov = ctx['covers']
    hero = phero('Private AI', 'Does your AI live in <span class="grad">someone else&rsquo;s house?</span>',
                 '<strong>Private AI</strong> means the model, the data you send it and the logs it keeps all run somewhere you control: your servers, an in-country cloud, or a locked-down private tenant. You need it when the data is sensitive, regulated or legally required to stay in the country. Everything else can make toast in the cloud.',
                 'Private AI', '<a class="btn btn-primary" href="{{PRE}}book.html">Bring your AI home <svg><use href="#arr"/></svg></a><a class="btn btn-ghost" href="#options">See the four options</a>')
    body = hero + f'''
<section class="psec">
  <div class="wrap pa-split">
    <div class="rv">
      <h2>The fridge test</h2>
      <p class="lead">Before anyone pastes anything into an AI tool, ask one question: <strong>would I be comfortable if this sat in a stranger&rsquo;s fridge for a year?</strong></p>
      <p class="lead">If yes, use whatever tool is fastest. If no, that job belongs on private AI. That&rsquo;s it. That&rsquo;s the strategy. The rest is engineering.</p>
    </div>
    <div class="pa-art rv d1">{cov.cover('fridge')}</div>
  </div>
</section>

<section class="psec" id="options">
  <div class="wrap">
    <h2 class="rv">Four ways to run AI, from rent it to own it</h2>
    <div class="cmp-wrap rv">
      <table class="cmp">
        <caption>Where your AI can live, and what each option is good for</caption>
        <thead><tr><th></th><th>Public chatbot</th><th>Enterprise cloud tenant</th><th class="me">In-country private cloud</th><th class="me">On-premises</th></tr></thead>
        <tbody>
          <tr><th>Where it runs</th><td>Vendor&rsquo;s shared cloud, often overseas</td><td>Vendor&rsquo;s cloud under a business contract</td><td class="me">Open or licensed models in a cloud region inside your country</td><td class="me">Your servers, your building</td></tr>
          <tr><th>Good for</th><td>Drafting, research, brainstorming</td><td>Most office work, with governance</td><td class="me">Regulated industries, government, data-residency rules</td><td class="me">Crown-jewel and classified data</td></tr>
          <tr><th>Who controls the data</th><td>Mostly the vendor</td><td>Shared, set by contract</td><td class="me">You, in your jurisdiction</td><td class="me">You, end to end</td></tr>
          <tr><th>Watch out for</th><td>Personal accounts, retention, jurisdiction</td><td>Data still leaves your environment</td><td class="me">Engineering effort, capacity planning</td><td class="me">Hardware, operations, upgrades</td></tr>
        </tbody>
      </table>
    </div>
    <p class="cmp-note">Most organisations run a hybrid: the cloud for the toast, the house for the family recipes.</p>
  </div>
</section>

<section class="psec">
  <div class="wrap">
    <h2 class="rv">When you need it (and when you don&rsquo;t)</h2>
    <div class="two">
      <div class="box rv"><h3>You probably need private AI if&hellip;</h3><ul class="ticks">
        <li><b>The law says where data lives.</b> Saudi Arabia&rsquo;s PDPL became fully enforceable on 14 September 2024, with a dedicated regulation for transfers outside the Kingdom.</li>
        <li><b>Your regulator is watching.</b> Australia&rsquo;s privacy regulator recommends keeping personal and sensitive information out of publicly available generative AI tools, and overseas AI providers bring cross-border disclosure rules into play.</li>
        <li><b>Your customers ask</b> where their data goes in procurement questionnaires.</li>
        <li><b>The data would hurt if it leaked:</b> patients, citizens, legal files, M&amp;A, source code.</li>
        <li><b>You need real Arabic,</b> not Arabic-ish.</li>
        <li><b>You run at volume,</b> where owning the engine beats renting it by the token.</li>
      </ul></div>
      <div class="box rv d1"><h3>You probably don&rsquo;t if&hellip;</h3><ul class="ticks">
        <li>It&rsquo;s public information or low-risk drafting.</li>
        <li>A governed cloud tool with company sign-in already meets your rules.</li>
        <li>You haven&rsquo;t picked a use case yet. Start with the <a href="{{{{PRE}}}}ai-readiness-assessment.html" style="text-decoration:underline">readiness assessment</a>.</li>
      </ul><p class="pa-note">Private AI is for the crown jewels, not the cutlery.</p></div>
    </div>
  </div>
</section>

<section class="psec">
  <div class="wrap">
    <h2 class="rv">What it looks like in production</h2>
    <div class="three">
      <div class="box rv"><span class="pa-k">Government &middot; Riyadh</span><h3>120+ languages, live</h3><p>Real-time audio and text translation on screens inside facilities for a Saudi government directorate. Reported 94% lower translation cost.</p></div>
      <div class="box rv d1"><span class="pa-k">Public safety &middot; Riyadh</span><h3>Drone detection, on a 6,751 km border</h3><p>Real-time video analysis and facial recognition for a Saudi government directorate, with a reported 96% identification accuracy.</p></div>
      <div class="box rv d2"><span class="pa-k">Enterprise &middot; Sydney &amp; Dubai</span><h3>BLDR agents</h3><p>Agents built on Inova&rsquo;s BLDR platform, deployed in the cloud, hybrid or locally depending on what the data allows.</p></div>
    </div>
    <p class="cmp-note">Delivered through Inova AI Solutions. Metrics as reported for the client engagement.</p>
  </div>
</section>

<section class="psec">
  <div class="wrap">
    <h2 class="rv">How to get there without a two-year programme</h2>
    <ol class="pa-steps rv">
      <li><b>Map the data.</b> Crown jewels, confidential, internal, public. One page.</li>
      <li><b>Pick the use case that pays.</b> One workflow, a named owner, a number that should move.</li>
      <li><b>Choose the house.</b> In-country cloud or on-premises, sized for that use case.</li>
      <li><b>Choose the model.</b> Open-weight for most work; a frontier cloud model for hard, low-risk reasoning.</li>
      <li><b>Govern from day one.</b> Access, logging, human sign-off and evidence, mapped to ISO/IEC 42001, the EU AI Act or NIST AI RMF.</li>
      <li><b>Ship in 8 to 16 weeks, measure, expand.</b></li>
    </ol>
  </div>
</section>

<section class="psec">
  <div class="wrap">
    <h2 class="rv">Questions people ask</h2>
    <div class="faq rv">{''.join(f'<details><summary>{q}<i></i></summary><div class="a">{a}</div></details>' for q, a in FAQ)}</div>
    <p class="cmp-note" style="margin-top:28px">Go deeper: <a href="{{{{PRE}}}}insights/is-chatgpt-safe-for-company-data.html">Is ChatGPT safe for company data?</a> &middot; <a href="{{{{PRE}}}}insights/what-is-private-ai-does-my-company-need-it.html">What is private AI?</a> &middot; <a href="{{{{PRE}}}}insights/how-to-stop-employees-pasting-data-into-ai.html">How to stop shadow AI</a></p>
  </div>
</section>
''' + ticker(OWN)
    service = {"@type": "Service", "@id": ctx['SITE'] + '/private-ai.html#service', "name": "Private and sovereign AI architecture", "serviceType": "Private AI, local LLM and sovereign AI deployment",
               "provider": {"@id": ctx['SITE'] + '/#person'}, "areaServed": ["Australia", "Saudi Arabia", "United Arab Emirates", "Europe"],
               "description": "Design and delivery of private, in-country and on-premises AI: model selection, hosting, governance and agentic workflows."}
    meta = dict(path='private-ai.html', title='Private & Sovereign AI for Enterprise | Youssef Jalloul',
                og_title='Does your AI live in someone else’s house?', og_image=ctx['SITE'] + '/assets/og/private-ai.jpg',
                description='Private AI keeps models, data and logs where you control them: on-premises, in-country cloud or a private tenant. When you need it and how to deploy it.',
                jsonld={"@context": "https://schema.org", "@graph": [service, ctx['faq_ld'](FAQ), ctx['breadcrumb']([('Home', ''), ('Private AI', 'private-ai.html')])]},
                sources='Sources: Clyde &amp; Co, “Saudi Arabia’s Personal Data Protection Law becomes enforceable” (Sept 2024); OAIC, “Guidance on privacy and the use of commercially available AI products” (Oct 2024). Advisory, not legal advice.')
    return ctx['render'](meta, relink(body))
