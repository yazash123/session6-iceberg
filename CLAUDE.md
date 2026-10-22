# Handover: Sessions 6 & 7 iceberg page

Read this first. It is the context a fresh session needs to keep editing this repo.

## What this is

A single-page facilitation tool for the House of the People citizens' assembly on AI (Assemble, with the
Odyssean Institute and Involve). Sessions 6 and 7 are 4-hour online sessions where members of the public
work through the results of the Odyssean process. In this activity, each **table** (breakout group, with a
facilitator sharing their screen on Zoom) takes **one risk** from the Horizon Scan risk map down an
"iceberg", imagining 2036 gone wrong, then turns and comes back up imagining 2036 gone right:

Set up → Imagine → Surface → Underneath → Core belief → **Turn** → Core belief → Underneath → Surface → Whole iceberg

- Down (red, "dn") = 2036 gone wrong. Up (yellow, "up") = 2036 gone right.
- **Since 21 Oct 2026 every member writes their own notes.** They pick their table, then confirm their name
  ("And your name?", pre-filled, Go →). Each note is tagged with the author's name and shows in that person's
  post-it colour. Caps (22 Oct): 50 words on Surface, 75 on Underneath and Core beliefs, clipped to 600
  characters (`MAXL`, `MAXC`), matching `t.size() <= 600` in the rules. People can edit or remove only their own
  notes, and like (heart) other people's. You see only your own notes on a layer until you switch on "See what
  others at your table put" (`othOn`). Everyone's notes are always on the Whole iceberg. Everyone sees only
  their own table's notes, live.
- Surface on the way down opens with the full risk and an "I've finished reading" button; the rest of the
  layer waits until it's pressed (`finishReading`). A "What to do" pill on the right of each layer gives timings
  and steps.
- Timings (Yaz, 21 Oct): way down 70 min = Surface 25 (15 reading the risk and writing quietly, then 10 talking;
  Imagine counts as part of this), Underneath 20 (10 + 10), Core belief 25 (10 + 15). Way up 40 min as one block
  across all three layers (20 quiet + 20 talking). They're a guide, not a rule.
- Expert sketches from the Horizon Summit can be revealed at each layer ("Take a peek at what the experts were thinking").

Owner: Yaz (Assemble). UK English, plain language for a general audience. Copy should stay warm and simple.

## Where it lives

- Repo: https://github.com/yazash123/session6-iceberg (branch `main`, served by GitHub Pages from the root)
- Live page: https://yazash123.github.io/session6-iceberg/
- Webflow: `webflow-embed.html` goes into one Code Embed in a full-width section on the HotP Webflow site. It
  iframes the live page and passes table links (`#g1`–`#g26`) through.
- Previous session for comparison: https://github.com/yazash123/session5 (Session 5 risk scoring; same
  GitHub Pages + Webflow iframe pattern, but that one uses Firebase for shared scores).
- The claude.ai artifact "HotP Iceberg Futures" (https://claude.ai/artifact/GaAYHmQbxCFyy38VbykXYq) is where
  design changes are made at the moment (21–22 Oct 2026); the repo takes them when Yaz says push. **Last synced
  22 Oct 2026** from artifact version id 1792672972-b3eb. Always compare the two before either direction:
  - **Artifact → repo:** copy the artifact's `index.html` over this one, then add the three Firebase script
    tags just above `<script id="app">` (the artifact leaves them out, because claude.ai's viewer blocks them;
    without them the GitHub page can't share notes). Keep `firebase-config.js`. Run both tests.
  - **Repo → artifact:** read the artifact first; if it has changed since the last sync, carry those edits into
    the repo before publishing. Publishing the page with the script tags is harmless (the viewer blocks them).
  - Don't use `tools/build.py`: it was a one-off import and would overwrite everything.
- Firebase plan for all the activity pages (Rosie and Yaz): "Firebase for the Session 5–7 activity pages",
  https://claude.ai/artifact/XomTKKPxKYNgjWDMVq16G6. `firestore.rules` here is the full file from its section
  4.6 (Session 5, the Iceberg, Drivers, What's Missing and the poll).
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
| `/* ================= ` | CSS blocks, in order of edits. Later blocks override earlier ones. The Turn tab is `Turn: one centred column`; the Whole iceberg tab is `Whole iceberg: the iceberg centred` (keyed off `#work[data-whole]`). |
| `var DEF={` | **every piece of visible text**, keyed (`'turn.q'`, `'setup.lead'`, `'risk.R06'`…). Edit copy here. `*asterisks*` = bold, `{n}` = filled in. |
| `<script type="application/json" id="copy">` | overrides of DEF saved from the artifact's "Edit text" mode. A key here wins over DEF. |
| `<script type="application/json" id="experts">` | Horizon Summit expert futures per risk (`down` / `up`, layer by layer). |
| `var CLUSTERS=` / `var STEPS=` / `var HUE=` | clusters & risks, step order, cluster colours. |
| `var FULLD=` | full risk descriptions (HTML), as on the Risk Wall. |
| `function viewImagine` / `viewLayer` / `viewTurn` / `viewWhole` | what each step draws. |
| `function render(` / `function go(` | redraw and step navigation. `render` sets `data-v`, `data-layer`, `data-turn`, `data-whole`, `data-bg` on `#work`, which the CSS keys off. |
| `editing the page's own text` | the in-page "Edit text" tool. Only works inside claude.ai; harmless here. |

## Sharing (Firebase)

Notes live in Firestore, in the same Firebase project as Session 5 (`session-5-activity`, config in
`firebase-config.js`). One document per note in the collection named by `var BOARD` in `index.html`:
`ice-s6` for Session 6. **Before Session 7, change `BOARD` to `ice-s7`** so tables start empty.

- Note: `{room, dir, layer, t, k, name, pid, at, st: {pid: name}, gone}`. `pid` is a random id kept in the
  browser (`localStorage` `hotp-ice-me`, with the name). Removing a note sets `gone: true`; nothing is deleted
  from the page. To clear a board, delete the collection in the Firebase console.
- `firestore.rules` holds the rules for Sessions 5, 6 and 7 together. **They must be published in the Firebase
  console** (Firestore → Rules) or every write is refused and the page falls back to keeping notes on that
  computer, with a message saying so.
- There's no sign-in, so "only your own notes" is enforced by the page, not the rules.
- Each browser listens only to its own table (`where('room','==',n)`), which keeps reads small.
- The example table (Set up → Show me an example) is local only and never touches Firebase.
- `S` (step, table, timers, local notes) is still in `localStorage` under `hotp-iceberg-s6-v1`.
- Search for `sharing: each table's notes` (Firestore code), `function noteEl` (a post-it), `function composer`
  (the note box, 25-word limit, name check), `function askName` (the signal when someone has no name yet).

## Header, step bar, risk

- Header (22 Oct): one blue bar with the title, a timer pill on the right and a small Presenting switch. There
  is no name field in the header any more; names are given at Set up or in the yellow box above a note box.
- Step bar (`var GROUPS`, `function renderSteps`): Set up · Way down (Imagine, Surface, Underneath, Core
  beliefs) · Way up (Turn, Core beliefs, Underneath, Surface) · Whole iceberg. The area you're in opens in a
  lighter block; the step you're on is underlined in white.
- The risk is a card above each layer (`function riskCard`), its circle in the cluster's colour, opening to the
  full Risk Wall text. The corner circle (`renderOrb`) and the white band (`renderBand`) are switched off.
- Hovering a table number on Set up lights its cluster and its risk on the map (`M.hotRisk`).

## Tests

- `python3 tools/check.py <dir>`: every step, desktop and phone.
- `python3 tools/check_shared.py <dir>`: several people at one table, using `tools/fakefirestore.js` in place of
  Firebase (it refuses what the rules refuse; its checks are copied by hand, so change it when the rules
  change). It presses "I've finished reading" and switches on "See what others…" where it needs to. Firebase
  itself can't be reached from Claude's sandbox.

## Working rules

1. Make the edit in `index.html`.
2. Run `python3 tools/check.py <screenshot dir>` and `python3 tools/check_shared.py <screenshot dir>`. It walks every step at desktop and phone width, checks the
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
- The page is set in **2036** (changed from 2030 on 18 Oct at Yaz's request). The only 2030s left are
  `xp.card` and `xp.foot`, which describe the Horizon Summit experts' sketches: those really were set in 2030.

## Open questions (as of 22 Oct 2026)

- Timers run separately in each browser. A shared, facilitator-led timer would need its own Firestore document.
- Notes typed while the page says "only saved on this computer" are never uploaded once sharing returns (see
  the Firebase plan, 5.2). Claude can make the page upload them on reconnect.
