"""Two (and three) people at the iceberg, without touching the real Firebase.

Usage: python3 tools/check_shared.py [output dir for screenshots]
Serves the repo over http, swaps the Firebase SDK for tools/fakefirestore.js (a shared collection in
localStorage that refuses what firestore.rules refuses), and opens several tabs as different people.
Exits non-zero if anything fails.
"""
import asyncio, functools, http.server, pathlib, socketserver, sys, threading
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else None
FAKE = (ROOT / 'tools' / 'fakefirestore.js').read_text()
fails = []

def ok(cond, msg):
    print(('ok   ' if cond else 'FAIL ') + msg)
    if not cond: fails.append(msg)

def serve():
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT))
    h.log_message = lambda *a: None
    srv = socketserver.TCPServer(('127.0.0.1', 0), h)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv

async def person(ctx, url, errs, pid, name=''):
    pg = await ctx.new_page()
    # tabs in one browser share storage, so give each tab its own person before the page loads
    await pg.add_init_script("localStorage.setItem('hotp-ice-me', JSON.stringify({name:'%s', pid:'%s'}))" % (name, pid))
    pg.on('pageerror', lambda e: errs.append(str(e)))
    await pg.route('**/firebase-app-compat.js', lambda r: r.fulfill(body=FAKE, content_type='text/javascript'))
    await pg.route('**/firebase-firestore-compat.js', lambda r: r.fulfill(body='', content_type='text/javascript'))
    await pg.goto(url); await pg.wait_for_timeout(1200)
    return pg

async def main():
    srv = serve(); base = f'http://127.0.0.1:{srv.server_address[1]}/index.html'
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for w, h, tag in [(1300, 900, 'wide'), (390, 844, 'phone')]:
            ctx = await b.new_context(viewport={'width': w, 'height': h}); errs = []
            A = await person(ctx, base, errs, 'pA')
            ok(await A.evaluate('!!DB'), f'{tag}: the fake Firestore is in use')
            # A picks table 7: the page asks for a name before moving on
            await A.locator('.strmb', has_text='7').first.click(); await A.wait_for_timeout(900)
            ok(await A.evaluate('S.step') == 0 and await A.locator('#joinname').is_visible(), f'{tag}: table 7 -> asks for a name first')
            if OUT: await A.screenshot(path=str(OUT / f'{tag}-join.png'))
            await A.locator('#stjoin button').click(); await A.wait_for_timeout(300)
            ok(await A.evaluate('S.step') == 0, f'{tag}: can’t join without a name')
            await A.fill('#joinname', 'Amira'); await A.press('#joinname', 'Enter'); await A.wait_for_timeout(900)
            ok(await A.evaluate('S.step') == 1 and await A.evaluate('S.risks') == ['R02'] and await A.input_value('#me') == 'Amira',
               f'{tag}: joined table 7 as Amira, Imagine with R02')
            await A.evaluate('go(2)'); await A.wait_for_timeout(400)
            ok(await A.evaluate('shared()'), f'{tag}: table 7 is shared')

            # B arrives by link, with no name, and tries to add a note
            B = await person(ctx, base + '#g7', errs, 'pB')
            await B.evaluate('go(2)'); await B.wait_for_timeout(400)
            ok(await B.locator('#pbody .namebox').count() == 1, f'{tag}: B sees a name box above the note box')
            await B.fill('#ta-dn-surface', 'Flooded inboxes'); await B.press('#ta-dn-surface', 'Enter'); await B.wait_for_timeout(400)
            ok(await B.evaluate("document.getElementById('mewrap').classList.contains('need')") and await B.evaluate('Object.keys(LIVE).length') == 0,
               f'{tag}: no name -> no note, and the name field is signalled')
            ok(await B.evaluate("document.activeElement.id") == 'nm-dn-surface', f'{tag}: focus jumps to the name box')
            if OUT: await B.screenshot(path=str(OUT / f'{tag}-needname.png'))
            await B.fill('#nm-dn-surface', 'Ben'); await B.wait_for_timeout(100)
            await B.locator('#pbody .compose button').click(); await B.wait_for_timeout(700)
            ok(await B.locator('#pbody .note').count() == 1, f'{tag}: Ben’s note appears for Ben')
            await A.wait_for_timeout(500)
            ok(await A.locator('#pbody .note .who', has_text='Ben').count() == 1, f'{tag}: …and for Amira, live, with his name')

            # 25 words at most
            long = ' '.join(f'w{i}' for i in range(1, 31))
            await A.fill('#ta-dn-surface', long); await A.wait_for_timeout(100)
            ok(await A.evaluate("document.getElementById('ta-dn-surface').value.trim().split(/\\s+/).length") == 25, f'{tag}: the note box stops at 25 words')
            await A.press('#ta-dn-surface', 'Enter'); await A.wait_for_timeout(700)
            ok(await A.locator('#pbody .note').count() == 2, f'{tag}: Amira’s 25-word note is added')

            # stars: on someone else’s note only
            ok(await A.locator('#pbody .note.mine .star').count() == 0, f'{tag}: no star button on your own note')
            await A.locator('#pbody .note:not(.mine) .star').click(); await A.wait_for_timeout(700)
            ok(await B.locator('#pbody .note.mine.hot .stars', has_text='1').count() == 1, f'{tag}: Ben sees Amira’s star on his note')
            # colours differ between people
            cols = await A.evaluate("Array.from(document.querySelectorAll('#pbody .note')).map(function(n){return getComputedStyle(n).backgroundColor;})")
            ok(len(set(cols)) == 2, f'{tag}: two people, two post-it colours {cols}')
            # only your own notes can be edited or removed
            ok(await A.locator('#pbody .note:not(.mine) [contenteditable]').count() == 0 and await A.locator('#pbody .note:not(.mine) .x').count() == 0,
               f'{tag}: Amira can’t edit or remove Ben’s note')
            # Ben renames himself: the name follows his note
            await B.fill('#me', 'Benjamin'); await B.wait_for_timeout(1500)
            ok(await A.locator('#pbody .note .who', has_text='Benjamin').count() == 1, f'{tag}: renaming updates Ben’s note for everyone')
            # Ben removes his note, then undoes it
            await B.locator('#pbody .note.mine .x').click(); await B.wait_for_timeout(700)
            ok(await A.locator('#pbody .note').count() == 1, f'{tag}: removed note disappears for Amira')
            await B.locator('#undo button').click(); await B.wait_for_timeout(700)
            ok(await A.locator('#pbody .note').count() == 2, f'{tag}: undo brings it back, star and all')
            # someone at table 8 sees none of it
            C = await person(ctx, base + '#g8', errs, 'pC')
            await C.evaluate('go(2)'); await C.wait_for_timeout(500)
            ok(await C.locator('#pbody .note').count() == 0, f'{tag}: table 8 doesn’t see table 7’s notes')
            # the rest of the iceberg shows the shared notes
            await A.evaluate('go(9)'); await A.wait_for_timeout(500)
            ok(await A.locator('#pbody .note').count() == 2, f'{tag}: the whole iceberg shows the table’s notes')
            ok('Benjamin' in await A.evaluate('record()') and '★ 1' in await A.evaluate('record()'), f'{tag}: the record names who said what, with stars')
            ok(await A.locator('#pbody', has_text='Start a new iceberg').count() == 0, f'{tag}: no “start again” on a shared table')
            if OUT: await A.screenshot(path=str(OUT / f'{tag}-whole-live.png'), full_page=True)
            await A.evaluate('go(6)'); await A.wait_for_timeout(400)
            ok(await A.locator('#pbody .echo li').count() == 0 and await A.evaluate('count("dn","surface")') == 2, f'{tag}: way up shows the right echo')
            await A.evaluate('go(8)'); await A.wait_for_timeout(400)
            ok(await A.locator('#pbody .echo li').count() == 2, f'{tag}: Surface on the way up echoes the 2 notes from the way down')

            # the example table
            D = await person(ctx, base, errs, 'pD', 'Dana')
            await D.evaluate('go(0)'); await D.wait_for_timeout(900)
            await D.locator('.exbtn').dispatch_event('click'); await D.wait_for_timeout(1200)
            for i, sid in [(2, 'd-surface'), (3, 'd-under'), (6, 'u-core'), (9, 'whole')]:
                await D.evaluate(f'go({i})'); await D.wait_for_timeout(600)
                if OUT: await D.screenshot(path=str(OUT / f'{tag}-example-{sid}.png'), full_page=True)
            await D.evaluate('go(2)'); await D.wait_for_timeout(400)
            ok(await D.locator('#pbody .note').count() == 5 and await D.locator('#pbody .note.hot').count() == 3, f'{tag}: example surface has 5 notes, 3 starred')
            ok(not await D.evaluate('shared()'), f'{tag}: the example never reaches the shared table')
            ok(not errs, f'{tag}: no script errors {errs[:3]}')
            await ctx.close()
        await b.close()
    srv.shutdown()

asyncio.run(main())
sys.exit(1 if fails else 0)
