"""Render 1200x630 share cards (default + one per article) into static/assets/og/ and static/assets/img/og.png."""
import asyncio, os, sys, json, glob, html, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import covers
from playwright.async_api import async_playwright
ROOT = os.path.dirname(os.path.abspath(__file__))
FONT = 'file://' + ROOT + '/static/assets/fonts/'
CSS = f'''@font-face{{font-family:"Inter Tight";src:url("{FONT}inter-tight-latin-wght-normal.woff2")}}@font-face{{font-family:"JetBrains Mono";src:url("{FONT}jetbrains-mono-latin-wght-normal.woff2")}}
body{{margin:0;width:1200px;height:630px;overflow:hidden;background:#0A0B0E;font-family:"Inter Tight",sans-serif}}
.wrap{{position:relative;width:1200px;height:630px}} .art{{position:absolute;inset:0;opacity:.95}} .art svg{{width:1200px;height:630px;display:block}}
.shade{{position:absolute;inset:0;background:linear-gradient(90deg,rgba(10,11,14,.96) 0%,rgba(10,11,14,.88) 48%,rgba(10,11,14,.15) 75%)}}
.t{{position:absolute;left:80px;top:96px;width:640px;color:#F3F4F6}}
.k{{font-family:"JetBrains Mono",monospace;font-size:20px;letter-spacing:4px;color:#C6F432;text-transform:uppercase}}
h1{{font-weight:800;font-size:58px;line-height:1.02;letter-spacing:-2px;margin:22px 0 0}}
.by{{position:absolute;left:80px;bottom:62px;font-family:"JetBrains Mono",monospace;font-size:20px;letter-spacing:2px;color:#A0A6B3}} .by b{{color:#C6F432;font-weight:400}}'''

def page(art, kicker, title):
    return f'<html><head><style>{CSS}</style></head><body><div class="wrap"><div class="art">{re.sub(r'<g transform="translate\([^)]*\)"><rect x="0" y="0" width="[^"]+" height="74" rx="37".*?</text></g>', '', covers.cover(art), flags=re.S)}</div><div class="shade"></div><div class="t"><div class="k">{html.escape(kicker)}</div><h1>{title}</h1></div><div class="by">YOUSSEF JALLOUL &middot; <b>youssefjalloul.com</b></div></div></body></html>'

async def main():
    jobs = [('static/assets/img/og.png', page('trio', 'Private · Governed · Enterprise AI', 'Enterprise AI that won’t let your toaster rise up against you.'))]
    for p in glob.glob(os.path.join(ROOT, 'content/insights/*.md')):
        fm = json.loads(open(p).read().split('\n---\n', 1)[0])
        jobs.append((f"static/assets/og/{fm['slug']}.jpg", page(fm['art'], fm['kicker'], html.escape(fm['title']))))
    jobs.append(('static/assets/og/private-ai.jpg', page('house', 'Private AI', 'Does your AI live in someone else’s house?')))
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox', '--allow-file-access-from-files'])
        pg = await b.new_page(viewport={'width': 1200, 'height': 630})
        for out, h in jobs:
            tmp = os.path.join(ROOT, '_og.html'); open(tmp, 'w').write(h)
            await pg.goto('file://' + tmp); await pg.wait_for_timeout(250)
            await pg.screenshot(path=os.path.join(ROOT, out), type=('jpeg' if out.endswith('.jpg') else 'png'), **({'quality': 84} if out.endswith('.jpg') else {}))
        os.remove(tmp)
        await b.close()
    print(len(jobs), 'cards')

asyncio.run(main())
