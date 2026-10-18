# Sessions 6 & 7: Iceberg futures

The House of the People "iceberg, 2036" activity, running on its own on GitHub Pages and embedded in Webflow.

- **Live page:** https://yazash123.github.io/session6-iceberg/ (table links: add `#g1` to `#g26`)
- **In Webflow:** paste `webflow-embed.html` into one Code Embed in a full-width section (not a Container). Table links work on the Webflow address too, for example `…/iceberg#g12`.

## Tables

26 tables, two per risk, numbered in risk-map order:

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

The table number sets the risk. Clusters light up to show their risks but can't be picked, and the risk can't be switched once a table is chosen.

## Files

| file | what it is |
|---|---|
| `index.html` | the page. Edit it directly: since 18 Oct 2026 the repo, not the artifact, is the source of truth. |
| `CLAUDE.md` | handover notes for anyone (or any Claude session) picking up the work. |
| `tools/check.py` | run after every edit: walks every step on desktop and phone and fails on errors. |
| `tools/build.py` | the one-off import from the claude.ai artifact. Don't rerun it; it would overwrite repo edits. |
| `webflow-embed.html` | the one Webflow embed. |

## What changed from the artifact

- "Room" reads "Table" throughout.
- Clicking a cluster no longer picks it; only a table number does.
- Notes are kept in the facilitator's browser (localStorage key `hotp-iceberg-s6-v1`), as in the artifact. Nothing is sent anywhere. Use **Copy the record** on the last step to keep a table's notes.
- Opening the page straight on a table link (`#g7`) no longer crashes it.
- "Edit text" only works inside claude.ai. Change wording in `var DEF` in `index.html`.
