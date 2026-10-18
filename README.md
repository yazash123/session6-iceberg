# Sessions 6 & 7: Iceberg futures

The House of the People "iceberg, 2030" activity, running on its own on GitHub Pages and embedded in Webflow.

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
| `index.html` | the page. Built from the claude.ai artifact, so don't hand-edit it; rebuild instead. |
| `tools/build.py` | `python3 tools/build.py <artifact index.html> .` rebuilds `index.html` with the changes below. |
| `webflow-embed.html` | the one Webflow embed. |

## What changed from the artifact

- "Room" reads "Table" throughout.
- Clicking a cluster no longer picks it; only a table number does.
- Notes are kept in the facilitator's browser (localStorage key `hotp-iceberg-s6-v1`), as in the artifact. Nothing is sent anywhere. Use **Copy the record** on the last step to keep a table's notes.
- "Edit text" only works inside claude.ai. Make wording changes in the artifact, then rebuild.
