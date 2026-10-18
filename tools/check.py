"""Smoke test for index.html: run after every edit.

Usage: python3 tools/check.py [output dir for screenshots]
Needs Playwright with Chromium (pip install playwright && python3 -m playwright install chromium).
Exits non-zero if anything fails.
"""
import asyncio, pathlib, sys
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
URL = (ROOT / 'index.html').as_uri()
OUT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else None
fails = []

def ok(cond, msg):
    print(('ok   ' if cond else 'FAIL ') + msg)
    if not cond: fails.append(msg)

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for w, h, tag in [(1300, 900, 'wide'), (390, 844, 'phone')]:
            pg = await b.new_page(viewport={'width': w, 'height': h})
            errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
            await pg.goto(URL); await pg.wait_for_timeout(1200)
            ok(await pg.locator('.strmb').count() == 26, f'{tag}: 26 table buttons')
            await pg.locator('.hub').first.click(); await pg.wait_for_timeout(500)
            ok(await pg.evaluate('S.step') == 0, f'{tag}: clicking a cluster does not pick it')
            await pg.locator('.strmb', has_text='7').first.click(); await pg.wait_for_timeout(1500)
            ok(await pg.evaluate('S.step') == 1 and await pg.evaluate('S.risks') == ['R02'], f'{tag}: table 7 -> Imagine with R02')
            for i, sid in enumerate(await pg.evaluate('STEPS.map(function(s){return s.id;})')):
                await pg.evaluate(f'go({i})'); await pg.wait_for_timeout(400)
                if OUT: await pg.screenshot(path=str(OUT / f'{tag}-{i:02d}-{sid}.png'))
            ok(not errs, f'{tag}: no script errors walking every step {errs[:2]}')
            # straight onto a table link, fresh browser state (this used to crash)
            ctx = await b.new_context(viewport={'width': w, 'height': h}); pg2 = await ctx.new_page()
            errs2 = []; pg2.on('pageerror', lambda e: errs2.append(str(e)))
            await pg2.goto(URL + '#g26'); await pg2.wait_for_timeout(1200)
            ok(not errs2 and await pg2.evaluate('S.room') == '26' and await pg2.evaluate('S.risks') == ['R12'],
               f'{tag}: opening #g26 directly -> table 26, R12 {errs2[:2]}')
            await ctx.close()
        await b.close()

asyncio.run(main())
sys.exit(1 if fails else 0)
