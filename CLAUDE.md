# Handover: Sessions 6 & 7 iceberg page

Read this first. It is the context a fresh session needs to keep editing this repo.

## What this is

A single-page facilitation tool for the House of the People citizens' assembly on AI (Assemble, with the
Odyssean Institute and Involve). Sessions 6 and 7 are 4-hour online sessions where members of the public
work through the results of the Odyssean process. In this activity, each **table** (breakout group, with a
facilitator sharing their screen on Zoom) takes **one risk** from the Horizon Scan risk map down an
"iceberg", imagining 2030 gone wrong, then turns and comes back up imagining 2030 gone well:

Set up → Imagine → Surface → Underneath → Core belief → **Turn** → Core belief → Underneath → Surface → Whole iceberg

- Down (red, "dn") = 2030 gone wrong. Up (yellow, "up") = 2030 gone well.
- The facilitator types what the group says as notes on each layer.
- Expert sketches from the Horizon Summit can be revealed at each layer ("Take a peek at what the experts were thinking").

Owner: Yaz (Assemble). UK English, plain language for a general audience. Copy should stay warm and simple.

## Where it lives

- Repo: https://github.com/yazash123/session6-iceberg (branch `main`, served by GitHub Pages from the root)
- Live page: https://yazash123.github.io/session6-iceberg/
- Webflow: `webflow-embed.html` goes into one Code Embed in a full-width section on the HotP Webflow site. It
  iframes the live page and passes table links (`#g1`–`#g26`) through.
- Previous session for comparison: https://github.com/yazash123/session5 (Session 5 risk scoring; same
  GitHub Pages + Webflow iframe pattern, but that one uses Firebase for shared scores).
- The original prototype was a claude.ai artifact ("HotP Iceberg Futures",
  https://claude.ai/artifact/GaAYHmQbxCFyy38VbykXYq). **As of 18 Oct 2026, the repo is the source of truth.
  Edit `index.html` directly. Don't rebuild from the artifact** unless Yaz asks; `tools/build.py` would
  overwrite repo edits.
- Session design context (Claude Doc): "Sessions 6 & 7 — Workshop modules",
  https://claude.ai/artifact/59tVvHPGsekNpUpRJCEDC3. Reference scenarios: "Iceberg futures — Horizon Summit
  scenarios", https://claude.ai/artifact/JikXwfwb9XUtK5AoQ2yAw8 (only when asked).

## Tables and risks

26 tables, two per risk, numbered in risk-map (cluster) order. The table number sets the risk, and groups
can't switch it. Clusters only light up to show their risks; they can't be picked.

| tables | cluster id | risk |
|---|---|---|
| 1–2 / 3–4 | `data` Everyone with data | R06 / R08 |
| 5–6 / 7–8 | `voters` Voters and the public | R01 / R02 |
| 9–10 / 11–12 | `kids` Children and learners | R03 / R15 |
| 13–14 | `work` People at work | R14 |
| 15–16 / 17–18 / 19–20 | `war` Civilians in conflict | R09 / R10 / R11 |
| 21–22 / 23–24 / 25–26 | `check` The bodies meant to check | R05 / R07 / R12 |

The mapping is generated from `CLUSTERS` (`RISKOF` / `ROOMSOF`). Changing the order of `CLUSTERS` renumbers
every table, so don't, unless asked. Code says "room" internally; the page says "Table".

## How index.html is laid out

One ~540 KB file. The first ~200 lines hold base64-embedded fonts. **Don't Read the whole file.** Use
Grep/search for these anchors, then read around them:

| look for | what it is |
|---|---|
| `/* ================= ` | CSS blocks, in order of edits. Later blocks override earlier ones. The Turn tab is `Turn: one centred column`. |
| `var DEF={` | **every piece of visible text**, keyed (`'turn.q'`, `'setup.lead'`, `'risk.R06'`…). Edit copy here. `*asterisks*` = bold, `{n}` = filled in. |
| `<script type="application/json" id="copy">` | overrides of DEF saved from the artifact's "Edit text" mode. A key here wins over DEF. |
| `<script type="application/json" id="experts">` | Horizon Summit expert futures per risk (`down` / `up`, layer by layer). |
| `var CLUSTERS=` / `var STEPS=` / `var HUE=` | clusters & risks, step order, cluster colours. |
| `var FULLD=` | full risk descriptions (HTML), as on the Risk Wall. |
| `function viewImagine` / `viewLayer` / `viewTurn` / `viewWhole` | what each step draws. |
| `function render(` / `function go(` | redraw and step navigation. `render` sets `data-v`, `data-layer`, `data-turn`, `data-bg` on `#work`, which the CSS keys off. |
| `editing the page's own text` | the in-page "Edit text" tool. Only works inside claude.ai; harmless here. |

State is in `localStorage` under `hotp-iceberg-s6-v1`, per browser. Nothing is sent to a server. The
facilitator copies the table's record on the last step ("Copy the record").

## Working rules

1. Make the edit in `index.html`.
2. Run `python3 tools/check.py <screenshot dir>`. It walks every step at desktop and phone width, checks the
   table logic and the `#gN` links, and fails on any script error. Look at the screenshots for the steps you
   touched.
3. Commit with a plain message and push to `main`. Pages redeploys in a minute or two.
4. Keep the page working at phone width (16px side gutter, no sideways scroll) and in "Presenting" mode
   (no motion, bigger text, for Zoom screen-share).

## Gotchas already hit

- **Load order:** anything run at load that calls `render()` before `var HUE` (and the map setup below
  `the cluster map`) has run will crash the whole page. That's why the initial `#gN` handling only sets the
  table and step; `render()` runs once at the bottom of the script.
- `var X=` declarations are hoisted as `undefined`. Function declarations are hoisted whole, so a function
  can be called before the data it needs exists.
- Imagine text says "the year **2036**" while everything else says 2030. Flagged to Yaz on 18 Oct; leave it
  unless Yaz changes it.

## Open questions (as of 18 Oct 2026)

- Should notes be collected centrally (e.g. Firebase, as in Session 5) instead of only in each facilitator's browser?
