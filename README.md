# Session 6: Iceberg futures, the record

The House of the People "iceberg, 2036" activity, as members left it on **Saturday 24 October 2026**. Since
1 November 2026 this page is a read-only, anonymised record: pick a table and look through what it wrote, step
by step, or all at once on the Whole iceberg. Nothing can be added, changed or hearted, and no names are shown.

- **Live page:** https://yazash123.github.io/session6-iceberg/ (table links: add `#g1` to `#g26`)
- **In Webflow:** paste `webflow-embed.html` into one Code Embed in a full-width section (not a Container). Table links work on the Webflow address too, for example `…/iceberg#g12`.
- **The version used on the day** (Firebase, rules, name prompts, the shared-notes test) is on the
  [`activity-version`](https://github.com/yazash123/session6-iceberg/tree/activity-version) branch. Use that
  branch if the activity is ever run again.

## Tables

26 tables, two per risk, numbered in risk-map order. Notes were saved at 16 of them; the others say so.

| tables | cluster | risk |
|---|---|---|
| 1–2 | Everyone with data | R06 AI with no safety guardrails |
| 3–4 | Everyone with data | R08 Using AI to predict and steer people's lives |
| 5–6 | Voters and the public | R01 AI used to manipulate people for profit |
| 7–8 | Voters and the public | R02 AI content flooding democratic processes |
| 9–10 | Children and learners | R03 AI companions shaping how young people grow up |
| 11–12 | Children and learners | R15 AI doing our thinking for us |
| 13–14 | People at work | R14 AI companies too big to regulate |
| 15–16 | Civilians in conflict | R09 AI choosing who gets targeted in war |
| 17–18 | Civilians in conflict | R10 AI making wars faster and harder to control |
| 19–20 | Civilians in conflict | R11 AI lowering barriers to weapons of mass destruction |
| 21–22 | The bodies meant to check | R05 AI companies controlling who can check their AI models |
| 23–24 | The bodies meant to check | R07 AI building AI faster than we can oversee |
| 25–26 | The bodies meant to check | R12 AI incidents crossing borders without international cooperation |

## The snapshot

The notes are embedded in `index.html`, in `<script type="application/json" id="snapshot">`: 1,494 notes, from
the sheet "Iceberg notes" in `session6-activity-data-anonymised.xlsx` (exported from Firestore `ice-s6`, without
the 50 notes their writers removed and 3 test notes). Each note keeps its table, way, layer, text, kind label,
time and hearts. Names are gone: each person is an opaque code (`m1`, `m2`…), used only so hearts still count.
Names that members typed inside notes already read `[member]`.

To rebuild it from the spreadsheet: `python3 tools/snapshot.py <path to the .xlsx>` (needs openpyxl).

## Files

| file | what it is |
|---|---|
| `index.html` | the page, with the snapshot inside. Edit it directly. |
| `CLAUDE.md` | handover notes for anyone (or any Claude session) picking up the work. |
| `tools/check.py` | run after every edit: walks every step on desktop and phone, checks it is read-only with no names and no Firebase, and compares a few tables with the sheet. |
| `tools/snapshot.py` | writes the snapshot into `index.html` from the spreadsheet. |
| `tools/build.py` | the one-off import from the claude.ai artifact. Don't rerun it; it would overwrite repo edits. |
| `firestore.rules` | kept for reference: the Firestore rules for the Session 5–7 pages. This page no longer uses Firebase. |
| `webflow-embed.html` | the one Webflow embed. |
