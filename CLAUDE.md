# Handover: Session 6 iceberg page (now the record)

Read this first. It is the context a fresh session needs to keep editing this repo.

## Record mode (since 1 Nov 2026)

`main` is a **read-only, anonymised record** of what members wrote on Saturday 24 October 2026. The version
used live on the day (Firebase, name prompts, hearts, `fakefirestore.js`, `check_shared.py`) is on the branch
**`activity-version`**; use it if the activity is run again. Most of the description below is of that live
version; what record mode changes:

- **No Firebase.** The Firebase script tags and `firebase-config.js` are gone. `var RECORD=true` sits in the
  `sharing: each table's notes` block, which now builds `DB` as a small read-only stand-in for Firestore:
  `collection().where('room','==',n).onSnapshot()` serves that table's notes from `SNAP`, the parsed
  `<script type="application/json" id="snapshot">`; `doc().set/update` always refuse. So `listen`,
  `liveList`, `notesOf`, `shared()` and the rest work as they did live.
- **The snapshot**: 1,494 notes `{id, room, dir, layer, t, k?, pid, at, st?}` from the sheet "Iceberg notes"
  in `session6-activity-data-anonymised.xlsx`, written by `python3 tools/snapshot.py <xlsx>`. No names: `pid`
  and the keys of `st` are opaque codes (`m1`…, shuffled each run), `st` values are empty; the stand-in fills in
  `name:''`, `gone:false`. Names typed inside notes already read `[member]`.
- **No names, no writing.** `noteEl` hands over to `recNoteEl` (the note, its kind label and a heart count,
  no author, nothing to press). `viewLayer` leaves out `composer`, `mindLine` and `othSwitch`; `othOn` is always
  true, so everyone's notes show. `gated` is false (no "I've finished reading" wait). `pickRoom` goes straight
  to Imagine through `joinGo` with no name; `paintJoin` stays hidden; no `nameBox` on Imagine. `addNote`,
  `editNote`, `del`, `toggleStar`, `renameMine`, `askName` return at once. `liveEl` is blank. `record()`
  leaves names out. The worksheet link (`wbk-js`) was removed; its CSS is still there, unused.
- **Copy**: the banner (`#recbar` in `SHELL`, key `rec.banner`, CSS in `<style id="record-css">`), and
  `rec.empty`, `rec.none` (a table with no notes), `rec.hearts` / `rec.heart1` in `var DEF`. `setup.q`,
  `setup.how(tap)`, `orb.table`, `imagine.room`, `imagine.begin` and `room.first` (in `#copy`) were reworded
  for visitors.
- Timers, "What to do", "Show me an example" (local, invented people, shown without names) and the members'
  futures peek are unchanged.
- The claude.ai artifact sync described below no longer applies to `main`.

## What we said tab (since 1 Nov 2026)

The first tab in the step bar, and where the page opens unless a table link (`#gN`) is given. It shows the
results of the activity: common themes across futures (Jacob's 19 themes of the 1,494 notes), the four that came
up at almost every table, and a risk map to filter the notes by risk.

- It lives in its own file, `said.html` (fonts, data and script all inside), shown in a frame (`#saidf`) that
  sits after the step bar. `said.html` tells the page its height with `postMessage({hotpSaid:h})` and the frame
  grows to fit.
- In `index.html`: `var SAID` and `setSaid()` beside `NAVOPEN`; `NAV.said` is the tab, built first in
  `buildSteps`; `renderSteps` marks it current; `go()` and table links leave it; `renderTimer` hides the timer
  on it. CSS at the end of the last `<style>`: `html[data-said]` hides the banner, the iceberg, the rail and
  "What to do".
- `said.html` is built outside this repo from the "Iceberg Futures: What We Said" claude.ai artifact
  (https://claude.ai/artifact/9ueHFBixM4D4cMqjhR4UT3), without its header and tab bar. Edit the artifact and
  rebuild, or edit `said.html` directly with care (it is one large file; grep, don't read it whole).

## What this is

A single-page facilitation tool for the House of the People citizens' assembly on AI (Assemble, with the
Odyssean Institute and Involve). Sessions 6 and 7 are 4-hour online sessions where members of the public
work through the results of the Odyssean process. In this activity, each **table** (breakout group, with a
facilitator sharing their screen on Zoom) takes **one risk** from the Horizon Scan risk map down an
"iceberg", imagining 2036 gone wrong, then turns and comes back up imagining 2036 gone right:

Set up → Imagine → Surface → Underneath → Core belief → **Turn** → Core belief → Underneath → Surface → Whole iceberg

- Down (red, "dn") = 2036 gone wrong. Up (yellow, "up") = 2036 gone right.
- **Since 21 Oct 2026 every member writes their own notes.** They pick their table, then confirm their name
  ("And your name?", pre-filled, Go →). Each note is tagged with the author's name. Post-its (22 Oct): your own notes are yellow, everyone
  else's mustard #E7C764 (`colourOf`; the hex values are written inside the function on purpose, because
  the first draw runs before `var`s at the bottom of the script are set, which left notes see-through). Caps (24 Oct): 35 words on every layer, clipped to 600
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
  24 Oct 2026 (early hours)**: artifact https://claude.ai/code/artifact/7e1a80d2-b2d4-462f-b20a-4b9bff267b66, version id 1792797336-69e9, and this repo match (35-word caps; no way-down echo on the way up; the peek now shows a future other members imagined). The artifact now carries the three Firebase script tags itself, so it copies over as is. Always compare the two before either direction:
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

One ~930 KB file (the snapshot is about 280 KB of it, on one line just above `<script id="app">`). The first ~200 lines hold base64-embedded fonts. **Don't Read the whole file.** Use
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

## Sharing (Firebase): the live version, on `activity-version` only

On `main` the notes come from the snapshot (see Record mode). On the day, notes lived in Firestore, in the same Firebase project as Session 5 (`session-5-activity`, config in
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

- `python3 tools/check.py <dir>` (record mode): every step at desktop and phone width; fails on any script or
  console error, any request to gstatic/Firebase, a name on the page (it plants a name in `hotp-ice-me` to make
  sure it never shows), anything to type into or press to change a note, or sideways scroll. It checks tables
  1, 10, 17, 20 and 23 layer by layer, and their Whole iceberg notes, hearts and kind labels, against counts
  from the sheet, plus `#g26` (no notes) and `#g17`.
- `check_shared.py` and `fakefirestore.js` (several people at one table, fake Firebase) are on `activity-version`.

## Working rules

1. Make the edit in `index.html`.
2. Run `python3 tools/check.py <screenshot dir>`. Look at the screenshots for the steps you touched.
3. Commit with a plain message and push to `main`. Pages redeploys in a minute or two.
4. Keep the page working at phone width (16px side gutter, no sideways scroll) and in "Presenting" mode
   (no motion, bigger text, for Zoom screen-share).

## Gotchas already hit

- **Load order:** anything run at load that calls `render()` before `var HUE` (and the map setup below
  `the cluster map`) has run will crash the whole page. That's why the initial `#gN` handling only sets the
  table and step; `render()` runs once at the bottom of the script.
- **Short screens (22 Oct):** on a wide but short window (a laptop at 650–770px tall) the Set up panel used to run past the bottom of `#work`, so the name box and "Show me an example" couldn't be reached. `layoutMap` now grows `#work` to fit the panel, and a ResizeObserver on `#stintro` re-lays the map when the name box appears.
- `var X=` declarations are hoisted as `undefined`. Function declarations are hoisted whole, so a function
  can be called before the data it needs exists.
- The page is set in **2036** (changed from 2030 on 18 Oct at Yaz's request). The only 2030s left are
  `xp.card` and `xp.foot`, which describe the Horizon Summit experts' sketches: those really were set in 2030.

## Open questions (as of 22 Oct 2026)

- Timers run separately in each browser. A shared, facilitator-led timer would need its own Firestore document.
- Notes typed while the page says "only saved on this computer" are never uploaded once sharing returns (see
  the Firebase plan, 5.2). Claude can make the page upload them on reconnect.
