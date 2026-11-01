"""Freeze the Session 6 notes into index.html, for the record page (1 Nov 2026).

Usage: python3 tools/snapshot.py <session6-activity-data-anonymised.xlsx>
Reads the sheet "Iceberg notes" (already without removed notes and tests) and writes the notes into
<script type="application/json" id="snapshot"> in index.html, in the page's own note shape, with no names:
each person is an opaque code (pid), and hearts keep their count with the hearter's name left empty.
The codes are shuffled afresh on every run. Needs openpyxl.
"""
import datetime, json, pathlib, random, re, sys, zoneinfo
import openpyxl

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = ROOT / 'index.html'
DIR = {'2036 gone wrong': 'dn', '2036 gone right': 'up'}
LAYER = {'1 Surface': 'surface', '2 Underneath': 'under', '3 Core beliefs': 'core'}
KINDS = {'Words of wisdom', 'Everyday saying', 'Figure of speech'}
UK = zoneinfo.ZoneInfo('Europe/London')  # the sheet's times are UK time

wb = openpyxl.load_workbook(sys.argv[1], read_only=True)
rows = list(wb['Iceberg notes'].iter_rows(values_only=True))
head, rows = rows[0], rows[1:]
c = {h: i for i, h in enumerate(head)}

people = sorted({r[c['Name']] for r in rows} | {p.strip() for r in rows if r[c['Hearted by']] for p in r[c['Hearted by']].split(',')})
codes = ['m%d' % (i + 1) for i in range(len(people))]
random.SystemRandom().shuffle(codes)
code = dict(zip(people, codes))

notes = []
for r in rows:
    k = r[c['Kind']] or ''
    assert k == '' or k in KINDS, k
    at = r[c['Saved at']]
    if isinstance(at, datetime.datetime): at = int(at.replace(tzinfo=UK).timestamp() * 1000)
    st = {code[p.strip()]: '' for p in (r[c['Hearted by']] or '').split(',') if p.strip()}
    assert len(st) == (r[c['Hearts']] or 0), r
    n = {'id': r[c['Note id']], 'room': int(r[c['Table']]), 'dir': DIR[r[c['Way']]], 'layer': LAYER[r[c['Layer']]],
         't': str(r[c['Note']]), 'pid': code[r[c['Name']]], 'at': at}
    if k: n['k'] = k
    if st: n['st'] = st
    notes.append(n)

blob = json.dumps(notes, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')
s = PAGE.read_text()
pat = re.compile(r'(<script type="application/json" id="snapshot">)(.*?)(</script>)', re.S)
assert pat.search(s), 'no snapshot script in index.html'
s = pat.sub(lambda m: m.group(1) + blob + m.group(3), s, count=1)
PAGE.write_text(s)
print(f'{len(notes)} notes from {len(people)} people written into {PAGE.name}')
