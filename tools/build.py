"""Turn the claude.ai iceberg artifact into a standalone page for GitHub Pages.

Usage: python3 tools/build.py <artifact index.html> <repo dir>
Every edit is an exact-text replacement that must match exactly once, so a changed
artifact fails loudly instead of building something half-edited.
"""
import sys, pathlib

src, out = sys.argv[1], pathlib.Path(sys.argv[2])
s = open(src, encoding='utf-8').read()

def rep(old, new):
    global s
    n = s.count(old)
    assert n == 1, f'expected 1 match, got {n}: {old[:80]!r}'
    s = s.replace(old, new)

# 1. Tables, not rooms: 26 tables, two per risk, numbered in map order (#g1 to #g26 links keep working).
rep("'mast.room':'Room'", "'mast.room':'Table'")
rep("'setup.q':'Which *room* are you in?'", "'setup.q':'Which *table* are you at?'")
rep("'setup.lead':'Each room takes one risk down the iceberg, and every risk has two rooms.'",
    "'setup.lead':'Each table takes one risk down the iceberg, and every risk has two tables.'")
rep("'setup.how':'Hover over a cluster to see its risks. Click your room number to begin.','setup.howtap':'Tap your room number to begin.'",
    "'setup.how':'Hover over a cluster to see its risks. Click your table number to begin.','setup.howtap':'Tap your table number to begin.'")
rep("'imagine.change':'Choose a different room'", "'imagine.change':'Choose a different table'")
rep("'whole.copied':'Copied. Paste it into the room’s notes.'", "'whole.copied':'Copied. Paste it into the table’s notes.'")
rep("'room.first':'Which room are you in?'", "'room.first':'Which table are you at?'")
rep("'hub.rooms':'Rooms {a}–{b}','room.n':'Room {n}','room.aria':'Room {n}: {risk}','imagine.room':'Room {n} · your risk'",
    "'hub.rooms':'Tables {a}–{b}','room.n':'Table {n}','room.aria':'Table {n}: {risk}','imagine.room':'Table {n} · your risk'")
rep("'imagine.none':'Choose your group’s cluster in Set up first.'", "'imagine.none':'Choose your table number in Set up first.'")

# 2. The table number sets the risk. Clusters are no longer something to pick:
#    a cluster only lights up to show its risks, and the risk can't be switched in Imagine.
rep("b.addEventListener('click',function(){pick(c.id);});",
    "b.addEventListener('click',function(){if(M.mode==='map')hot(M.hot===c.id?null:c.id);});")
rep("  if(M.mode==='map'){pick(q.c.id);return;}\n",
    "  if(M.mode==='map'){hot(M.hot===q.c.id?null:q.c.id);return;}\n  if(S.room&&RISKOF[S.room])return; /* the table fixes the risk */\n")
rep("<div id=\"root\"></div>\n<script type=\"application/json\" id=\"copy\">",
    "<style>.cmap[data-mode=imagine] .sat,.cmap[data-mode=imagine] .slab{cursor:default}</style>\n<div id=\"root\"></div>\n<script type=\"application/json\" id=\"copy\">")

# 2b. Opening the page straight on a table link (#g7) used to call render() before the page had
#     finished setting up, which crashed it. On load, just set the table and go to Imagine;
#     later hash changes still re-render as before.
rep("fromHash(); window.addEventListener('hashchange',fromHash);",
    "(function(){var m=/^#g(\\d{1,2})$/.exec(location.hash||'');if(m&&+m[1]>=1&&+m[1]<=NROOMS){if(S.room!==m[1])setRoom(m[1]);if(S.step===0){S.step=1;save();}}})();\nwindow.addEventListener('hashchange',fromHash);")

# 3. Separate storage key from the claude.ai prototype, so old test notes don't carry over.
rep("var KEY='hotp-iceberg-v1';", "var KEY='hotp-iceberg-s6-v1';")

(out / 'index.html').write_text(s, encoding='utf-8')
print('wrote', out / 'index.html', len(s))
