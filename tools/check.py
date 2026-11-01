"""Check for the record page (1 Nov 2026): run after every edit.

Usage: python3 tools/check.py [output dir for screenshots]
Needs Playwright with Chromium (pip install playwright && python3 -m playwright install chromium).
Walks every step at desktop and phone width and checks that the page is a read-only, anonymised record:
no Firebase requests, no script errors, no names, nothing to type into or press to change notes, and each
table shows the notes in the snapshot. The expected counts below come from the sheet "Iceberg notes" in
session6-activity-data-anonymised.xlsx. Exits non-zero if anything fails.
"""
import asyncio, pathlib, sys
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
URL = (ROOT / 'index.html').as_uri()
OUT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else None
LAYERS = [(2, 'dn', 'surface'), (3, 'dn', 'under'), (4, 'dn', 'core'), (6, 'up', 'core'), (7, 'up', 'under'), (8, 'up', 'surface')]
# from the sheet: notes per step, total, hearts, notes with a kind label
SHEET = {
    1: ({'dn-surface': 18, 'dn-under': 18, 'dn-core': 22, 'up-surface': 10, 'up-under': 13, 'up-core': 17}, 98, 50, 3),
    10: ({'dn-surface': 36, 'dn-under': 20, 'dn-core': 25, 'up-surface': 22, 'up-under': 15, 'up-core': 27}, 145, 152, 0),
    17: ({'dn-surface': 32, 'dn-under': 25, 'dn-core': 27, 'up-surface': 13, 'up-under': 23, 'up-core': 21}, 141, 100, 1),
    20: ({'dn-surface': 0, 'dn-under': 0, 'dn-core': 0, 'up-surface': 0, 'up-under': 1, 'up-core': 0}, 1, 0, 0),
    23: ({'dn-surface': 18, 'dn-under': 16, 'dn-core': 15, 'up-surface': 22, 'up-under': 14, 'up-core': 26}, 111, 23, 1),
}
# anything a visitor could type into or press to change a note (#edta is the hidden "Edit text" box, claude.ai only)
WRITE = 'textarea:not(#edta), input, [contenteditable="true"], [contenteditable="plaintext-only"], button.star, .note .x, .oth, .namebox input, #joinname, .compose, .kw'
fails = []

def ok(cond, msg):
    print(('ok   ' if cond else 'FAIL ') + msg)
    if not cond: fails.append(msg)

async def page(b, w, h, url, errs, reqs):
    ctx = await b.new_context(viewport={'width': w, 'height': h}); pg = await ctx.new_page()
    # someone who was there on the day still has their name in this browser: it must never show
    await pg.add_init_script("localStorage.setItem('hotp-ice-me', JSON.stringify({name:'Tester Zed', pid:'pT'}))")
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
    pg.on('request', lambda r: reqs.append(r.url))
    await pg.goto(url); await pg.wait_for_timeout(1200)
    return ctx, pg

async def counts(pg):
    out = {}
    for i, d, l in LAYERS:
        await pg.evaluate(f'go({i})'); await pg.wait_for_timeout(250)
        out[f'{d}-{l}'] = await pg.locator('#pbody .note').count()
    return out

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for w, h, tag in [(1300, 900, 'wide'), (390, 844, 'phone')]:
            errs, reqs = [], []
            ctx, pg = await page(b, w, h, URL, errs, reqs)
            ok(await pg.evaluate('RECORD===true && SNAP.length') == 1494, f'{tag}: record mode, 1494 notes in the snapshot')
            ok(await pg.locator('#recbar').is_visible() and 'record of what members wrote' in await pg.locator('#recbar').inner_text(), f'{tag}: the banner shows')
            ok(await pg.locator('.strmb').count() == 26, f'{tag}: 26 table buttons')
            if OUT: await pg.screenshot(path=str(OUT / f'{tag}-00-setup.png'))
            await pg.locator('.hub').first.click(); await pg.wait_for_timeout(500)
            ok(await pg.evaluate('S.step') == 0, f'{tag}: clicking a cluster does not pick it')
            await pg.locator('.strmb', has_text='7').first.click(); await pg.wait_for_timeout(1500)
            ok(await pg.evaluate('S.step') == 1 and await pg.evaluate('S.risks') == ['R02'], f'{tag}: table 7 -> straight to Imagine with R02, no name asked')
            ok(await pg.locator('#joinname').count() == 0, f'{tag}: no name box at set up')
            seen = set()
            for i, sid in enumerate(await pg.evaluate('STEPS.map(function(s){return s.id;})')):
                await pg.evaluate(f'go({i})'); await pg.wait_for_timeout(400)
                if OUT: await pg.screenshot(path=str(OUT / f'{tag}-t7-{i:02d}-{sid}.png'), full_page=(sid == 'whole'))
                n = await pg.locator(WRITE).count()
                if n: seen.add(f'{sid}:{n}')
                sw = await pg.evaluate('document.documentElement.scrollWidth>window.innerWidth+1')
                if sw: seen.add(f'{sid}:sideways scroll')
            ok(not seen, f'{tag}: nothing to write in, heart, edit or remove on any step {sorted(seen)}')
            # tables against the sheet
            for t, (per, total, hearts, kinds) in SHEET.items():
                await pg.evaluate(f"setRoom('{t}');go(1)"); await pg.wait_for_timeout(300)
                got = await counts(pg)
                ok(got == per, f'{tag}: table {t} step by step matches the sheet {got if got != per else ""}')
                await pg.evaluate('go(9)'); await pg.wait_for_timeout(400)
                wn = await pg.locator('#pbody .note').count()
                wh = await pg.evaluate("Array.from(document.querySelectorAll('#pbody .note .stars span')).reduce(function(a,s){return a+(+s.textContent);},0)")
                wk = await pg.locator('#pbody .note .k').count()
                ok((wn, wh, wk) == (total, hearts, kinds), f'{tag}: table {t} whole iceberg: {wn} notes, {wh} hearts, {wk} kind labels (sheet: {total}, {hearts}, {kinds})')
                if OUT and t == 10: await pg.screenshot(path=str(OUT / f'{tag}-t10-whole.png'), full_page=True)
            await pg.evaluate("setRoom('10');go(2)"); await pg.wait_for_timeout(500)
            if OUT: await pg.screenshot(path=str(OUT / f'{tag}-t10-d-surface.png'), full_page=True)
            await pg.evaluate("go(4)"); await pg.wait_for_timeout(400)
            if OUT: await pg.screenshot(path=str(OUT / f'{tag}-t10-d-core.png'))
            txt = await pg.evaluate('document.body.innerText')
            ok('Tester' not in txt and 'Person I' not in txt and 'You ·' not in txt, f'{tag}: no names on the page')
            ok(await pg.evaluate('typeof firebase') == 'undefined', f'{tag}: Firebase never loaded')
            # the example still works, and shows no names
            await pg.evaluate('go(0)'); await pg.wait_for_timeout(600)
            await pg.locator('.exbtn').dispatch_event('click'); await pg.wait_for_timeout(900)
            await pg.evaluate('go(2)'); await pg.wait_for_timeout(500)
            ok(await pg.locator('#pbody .note').count() == 5 and await pg.locator('#pbody .note .who').count() == 0, f'{tag}: the example shows its 5 notes, no names')
            if OUT: await pg.screenshot(path=str(OUT / f'{tag}-example-d-surface.png'))
            await ctx.close()
            # straight onto a table link, and onto a table with no notes
            ctx, pg2 = await page(b, w, h, URL + '#g26', errs, reqs)
            ok(await pg2.evaluate('S.room') == '26' and await pg2.evaluate('S.risks') == ['R12'], f'{tag}: opening #g26 directly -> table 26, R12')
            await pg2.evaluate('go(2)'); await pg2.wait_for_timeout(400)
            ok(await pg2.locator('#pbody .note').count() == 0 and 'No notes were saved for Table 26' in await pg2.locator('#pbody').inner_text(), f'{tag}: table 26 says no notes were saved')
            await ctx.close()
            ctx, pg3 = await page(b, w, h, URL + '#g17', errs, reqs)
            await pg3.evaluate('go(3)'); await pg3.wait_for_timeout(400)
            ok(await pg3.locator('#pbody .note').count() == 25, f'{tag}: opening #g17 -> Underneath shows its 25 notes')
            await ctx.close()
            ok(not errs, f'{tag}: no script or console errors {errs[:3]}')
            bad = [u for u in reqs if 'gstatic' in u or 'firebase' in u or 'googleapis' in u]
            ok(not bad, f'{tag}: no requests to Firebase or gstatic {bad[:2]}')
        await b.close()

asyncio.run(main())
sys.exit(1 if fails else 0)
