# StyleMate — version log

Internal change log. The filename is the version.
Newest first. Each entry: what prompted it, what changed, why.

> ## ⚑ END OF THE OLLAMA LINE
> **`StyleMate_frontend_v15_ollama_v8.html` is the LAST version built on Ollama.**
> From here the project migrates to the Gemini API. Everything below this line
> that carries an `ollama_vN` name is the local-model era and is kept for
> reference, not for further work.
>
> What that migration has to deal with, recorded while it is fresh:
> - The page calls Ollama **directly from the browser**. Gemini cannot work that
>   way: an API key in a page is readable by anyone who opens it. The calls must
>   move behind `backend/app/llm/` — which already has a Gemini path and a
>   provider router, so the destination exists.
> - `backend/.env` already holds `GEMINI_API_KEY` and `SM_PROVIDER`. Setting the
>   key and `SM_PROVIDER=gemini` is the switch, once the page talks to the backend.
> - Model shortlist and costed comparison: `Gemini_model_shortlist.xlsx`.
> - Worth keeping from the Ollama era, because none of it is model-specific:
>   the two-stage pipeline (understand → search in code → rank only when it
>   helps), hard-vs-soft constraint separation, prices parsed in code rather
>   than trusted to the model, the balanced-brace JSON parser, the off-brief
>   guard, and the audit log.

---

## StyleMate_frontend_v15_gemini_v17.html — 30 Oct 2026

**Prompted by:** (1) turning AI on in the top search bar typed "I need
something to wear this winter" into the box, so the shopper had to delete it
first; it should be light placeholder text only, gone with the first letter,
back when the box is empty, never sent as the prompt. (2) The "STYLEMATE · AI
STYLING — Find your thing. Skip the endless scroll." banner should leave the
top so everything moves up, and a version of it should fill the empty space
under the Style tools in the left column, so the shopper scrolls less.

**Changed:**
- `setSearchAI`: with AI on, the example is the input's placeholder; nothing
  is written into the box or selected. An empty box with AI on still answers
  "Tell StyleMate what you need" rather than running the example.
- The banner above the results is removed; the results heading now starts
  level with the sidebar (`.lead-section`).
- New `.side-hero` card at the foot of the sidebar: the same kicker and
  "Find your thing. Skip the *endless scroll.*", one line on turning on AI in
  the search bar, and "Try AI search →", which scrolls to the top and turns
  AI search on.
- The sidebar still never scrolls (v14). Measured heights decide what shows:
  from 838 px tall both the card and the "Shopping, with intent" note show;
  from 776 to 837 px the card takes the note's place; below 776 px the card is
  left out (and below 692 px the note too, as before). The card is hidden on
  phones, where the sidebar is a horizontal strip.

**Checked in the browser:** placeholder on/off, typing and deleting, empty
submit, the card's button; 1440 × 1000 / 800 / 720 and 375 × 812 (sidebar
fits, no sideways scroll); no console errors.

---

## Clothes fitted to the GLB avatars — 30 Oct 2026 (no page change; serves v16)

**Prompted by:** a screenshot of the male model in a kurta: the clothes did not
sit on the person. Asked for: any garment on top of the 3D person, male or
female; T-shirts on the upper half, jeans and trousers on the lower half;
garment necks matching the person's neck; lengths from the size chart at the
size chosen (M/L/XL) against the scaled person, e.g. a sleeve 5 cm longer than
the arm runs 5 cm past it.

**Changed (`frontend/stylemate-room.js` only, in place):** on a GLB model,
each garment is now built from the model's own skin instead of the measurement
shells made for the Basic avatar. The skeleton's skin weights say which skin is
torso, arm, hand, leg, foot or neck; that skin is pushed out by the garment's
ease (chart girth at the chosen size minus the shopper's measurement) and cut:
- neckline at the base of the neck; top hem at the chart length down from it;
- sleeves the chart length from the top of the shoulder, continuing past the
  wrist over the hand by the difference when longer than the arm (the model's
  arm from the shoulder top is 56.5 cm at 1.72 m);
- sleeveless armholes at the chart shoulder width;
- trousers from a mid-rise waistband to the chart inseam (shorts 20 cm at most);
- kurtas, dresses, skirts and long tops hang as one piece below the hip joints.

Made to read as cloth, after the first render showed where it did not:
- holes where the file keeps nipples and nails separately are closed, and
  vertices the file splits along texture seams are merged (15,252 of them),
  so the clothes neither have holes nor crack open;
- smoothing over small bumps, spanning hollows across the trunk (between the
  breasts, along the spine), and falling 0.8 cm per cm at most below a fuller
  part, so there is no shelf under the bust;
- a top with no chart waist falls straight from the chest instead of bulging
  by its waist ease; the fitted part blends onto the lower part over 4 cm and
  overlaps it by 5 mm, so there is no band, step or hairline at the hips;
- hems and waistbands are straight cuts and every edge an even curve;
- layers are fitted inside-out (shoes, bottoms and skirts, tops and dresses,
  jackets) and each is kept 6 mm outside what is worn beneath it;
- shoes are a smooth closed shell over each foot below the ankle (the foot's
  convex outline every centimetre, heel to toe), not a sock over the toes.

Basic still shows the shells. A model without the MakeHuman/MPFB skeleton
falls back to the shells with a message. `frontend/models/README.md` updated.

**Checked in the browser:** male kurta (L) + jeans, front and side; men's
T-shirt + shorts; shirt (XL, 65 cm sleeve, 8.5 cm past the wrist) + jeans;
female sleeveless midi dress; top + trousers; top + skirt; kurta size L → XXL
refits (hem 5 cm lower, looser); blazer over shirt with jeans and shoes;
hide/show; Basic and back; no fitting-room errors in the console.

**Not done:** it is a shape, not a cloth simulation: no folds. The body is
not reshaped to the shopper (only height); looseness is the shopper's, added
to the model's body.

---

## GLB avatars in the fitting room — 29 Oct 2026 (no page change; serves v16)

**Prompted by:** a prompt to load male/female `.glb` models from a models folder
into the existing 3D fitting room, discovered automatically, without changing
anything else. Models supplied: `male-base-mesh-base_male.glb`,
`female-base-mesh-base_female.glb` (Blender exports, 4.5 MB each, ~73k
vertices, rigged, no morph targets or textures, one clay material, Y-up metres,
feet on the floor, facing +Z, arms-out pose; 1.786 m and 1.593 m tall).

**Tailored to this project:** one canonical folder `frontend/models/` (copies
named `male_base.glb`, `female_base.glb`; originals left where they were),
served by FastAPI at `/models` straight from that folder (no copy in
`app/static`), and listed by `GET /api/models`. No ZIP: the project is edited in place.

**Files:**
- New `backend/app/services/avatar_models.py`: scans the folder on every request
  and checks each GLB (header, length, JSON, meshes, size ≤80 MB, required
  extensions, external files). Category comes from optional `models.json`, else
  the file name ("female" before "male"). `.glb` is served as `model/gltf-binary`.
- `backend/app/main.py`: `GET /api/models`, plus the `/models` static mount
  (before "/", `check_dir=False`).
- New `frontend/GLTFLoader.js` and `frontend/BufferGeometryUtils.js`: three.js
  r169 (matches `three.module.min.js`), vendored; the one change is the import
  path. They go to `app/static` via `sync_static.py` and both
  `start_stylemate.command` copies (asset lists only).
- `frontend/stylemate-room.js` (in place), GLB AVATARS section:
  - **Loading:** the loader is imported only when needed. The chosen model
    replaces the basic body in the same viewer; the basic body stays, hidden, as
    the fallback.
  - **Placement:** in a holder group, scaled uniformly to the avatar's height,
    centred, feet on the floor. Authored materials are untouched (no tinting).
  - **Choosing:** "Model" chips (models for the current Body model, plus Basic)
    under Body model, remembered per Male/Female in the browser.
  - **Safety:** a newer choice or a closed room cancels an older load. Up to 4
    models stay cached; older ones are disposed. Errors (404, not a GLB, bad
    dimensions, loader missing) show in the panel and keep the basic avatar.
- New `frontend/models/README.md`: how to add models, naming, `models.json`,
  checks, limitations.

**Untouched:** the page HTML, measurements and fit maths, garment shells, fit
reports, catalogue, search, AI, Colour Studio, Shop a Look, the sidebar mini
mannequin, `render.yaml`.

**Tested (over localhost):**
- **Serving:** `/api/models` lists both; `/models/*.glb` 200 as
  `model/gltf-binary`; a missing file 404.
- **Male model:** loads into the fitting room (scale 0.961 to 1.72 m, centred,
  feet at 0); the basic body is hidden and there is one model in the scene.
  Screenshots show it upright, front-facing, on the floor.
- **Switching:** Female → the female model (1.60 m). Basic → the basic avatar;
  back to the model from cache in 0.25 s. Six switches: GPU geometries 11 → 11.
  Two clicks in one tick: the last one wins.
- **Failures:** an injected missing model gives "file was not found (404)"; a
  non-GLB gives "not a valid GLB"; both keep the basic avatar, and a working
  model loads afterwards.
- **Discovery:** missing folder, empty folder, fake/truncated `.glb`, `.fbx` and
  broken `models.json` are all reported correctly. A test `.glb` dropped into the
  folder appeared and loaded with no restart (then removed).
- **Rest of the app:** plain and AI search, Colour Studio rows, Shop a Look and
  the mini mannequin still work; the backend suite (`python -m tests.test_all`)
  gives 116 passed, 0 failed; no console errors.
- **Not tested:** a real Render deploy.

---

## StyleMate_frontend_v15_gemini_v16.html — SIZE PRE-PICKED, SHORT AI READING, LOGO HOME, LEANER PAGE — 29 Oct 2026

**Prompted by:** "Your size: M should be auto-picked"; "remove Catalogue size";
"the AI reading is too long - just undertone, depth (and boy/girl) with a 2-3 line
static explanation for each of the 3×3 combinations, and it must update when my
choices change"; "clicking the SM · STYLE MATE logo should go to a fresh home
page"; "remove the categories bar"; "remove the lower Ask StyleMate anything box -
the top bar's AI switch replaces it".

**Product cards:** the S/M/L/XL picker pre-selects the size from the shopper's
measurements (`sizeAdviceFor`) until they pick another. "Catalogue size: Not
provided in dataset" is gone.

**Colour Studio AI reading:** now just "AI READING · model · time", then
"<undertone> undertone · <depth> depth · shopping for <Women/Men>", then a fixed
explanation for that undertone × depth (9 texts in `TONE_EXPLAIN`). The model's
observation, caveat, the undertone/depth definitions and the footnote are gone;
the AI still decides Women/Men. `toneReadingRender()` draws it from the current
choices and runs on every change (clicks or a tapped patch), so it never
disagrees with the buttons; a change marks it "edited by you". The status line
under it follows too.

**Logo:** `goHome()` - closes panels and the drawer, clears search and AI mode,
AI results, price filter, sort, colour and fit ranking and the Women/Men chip
override, shows the banner, opens Ethnic and scrolls to the top. The cart,
fitting room, wardrobe, saved palette and Women/Men/All are kept, and the page
is not reloaded (a reload would empty the cart).

**Layout:** the categories bar is removed (categories stay in the header); the
columns now pin 91 px down, so the left column's cut-offs moved 49 px lower
(note ≤691 px, extras ≤631 px, descriptions ≤546 px). The lower "Ask StyleMate
anything" box is hidden - kept in the page because the agent code still reads
its input - and the agent no longer clears the prompt typed in the top bar.

**Tested (1440×790, over localhost):** no categories bar or lower box; left
column pinned at 91, ends at 670, everything shown; size XL pre-picked where the
measurements say XL, a click on M overrides; no Catalogue size; man's photo →
"warm · medium · shopping for Men" + the warm/medium text, clicking Cool + Deep
→ the panel and status switch to cool/deep, "edited by you"; logo after an AI
search + filter + fit ranking + open studio → Ethnic, banner, nothing filtered,
no panel open, cart and fitting room kept, still signed in; phone: header
categories, tool cards, no sideways scroll; no new console errors (the only 500
was the separate audit-log sink on :8765).

---

## StyleMate_frontend_v15_gemini_v15.html — AI SEARCH SWITCH, AI FIT RANKING, COLOUR FILTERS — 29 Oct 2026

**Prompted by:** an AI switch on the top search bar; "Rank my results by this
fit" should really rank (with basic body-shape research, using AI); drop "My
colour palette" from the right column; make the Colour Studio's colour chips
filter the products, with an All chip; tell the shopper when the fitting room
has nothing in it.

**1. Top search bar - AI switch.** A small "AI" switch at its left. On: the
placeholder becomes "Ask StyleMate anything", a starter prompt is filled in
("I need something to wear this winter", selected so typing replaces it), the
button reads "Find my match ↗", the Budget · Occasion · Fit · Colour · Brand ·
Delivery hint shows under the bar, and Enter/the button run the same agent as
the box below (`window.runAgent`). Off: the plain catalogue search, and an
untouched starter prompt is cleared. The lower "Ask StyleMate anything" box stays.

**2. Rank my results by this fit - AI.** `rankByFit()` sends the products on
screen (the current search or category, first 40: id, name, type, outfit part,
description) with the shopper's body shape, silhouette and rise to the text model
through `/api/llm/chat`, together with a short brief per shape (common styling
guidance: pear - balance the top, A-line/wide-leg/bootcut below; apple - V-necks,
wrap, empire, longline, no crop or tight waist; hourglass - follow the waist;
rectangle - create shape with peplum, belts, flare; inverted triangle - soften
the shoulders, volume below; oval - long vertical lines). The model scores each
0-100 with a reason of up to 9 words; the grid re-orders (stable - unscored
products keep their order after) and the reason shows on each card ("◈ Fit 90 ·
Tailored jacket adds structure to balance pear hips"), with a status line and a
"ranked by fit" chip; Stop using it / × undoes it, and a new search or category
clears it. Guards found in testing: the model at first called men's garments
"fit does not depend on body shape" - the prompt now says shapes apply to men
too, and any garment still marked neutral is scored by the keyword rules
instead. With no model, the same brief scores the words in each listing.
~4 s for 36 products.

**3. Right column:** "My colour palette" is no longer shown; Colour combination
(1) and Fit & silhouette (2). The palette lives in the Colour Studio.

**4. Colour Studio colour chips filter (`stylemate-room.js`, in place).** An "All"
chip (selected by default) plus one per season colour. A colour shows every
product in each outfit part, from the whole catalogue in the page, that is that
colour or a close shade, for the same Women/Men/All choice. Close shade, calibrated
on the catalogue's colours: two vivid colours within 15° of hue and similar
lightness, otherwise CIE Lab ΔE ≤ 10 (Peach → Peach, Coral, Rose Gold, Nude;
Turquoise → Turquoise, Teal; Mustard → Yellow, Gold, Mustard, Tan). Row headers
read "· N IN PEACH & CLOSE SHADES"; no match says so. Chip dots now use the
page's own colour table, plus shades for Aqua, Mint Green and Camel - which used
to show grey and would have matched grey products.

**5. Fitting room nudge (`stylemate-room.js`).** With nothing added, the panel
opens with "Nothing to try on yet - add a piece with ＋ Add to Fitting Room" and a
"Pick something to try on ↗" button that closes the room, and the 3D view shows
"No pieces yet · add one from the store to try it on". Both go once a piece is added.

**Tested (1440×850, over localhost):** switch on/off restores both states; the
hint sits above the categories bar; AI search from the top bar → 36 winter
pieces; fit ranking (Pear · Relaxed · Mid-rise) → AI-ranked 36, tailored and
structured blazers top, crop jacket bottom, no garment marked neutral, 4.4 s;
Stop using it clears chip and notes; chips: Peach 28, Coral 26, Turquoise 9, Mint
Green empty message, All back to 44; empty fitting room shows both nudges and the
button closes it; with one piece neither shows; plain search with AI off → 56 for
"jeans"; no console errors.

---

## StyleMate_frontend_v15_gemini_v14.html — SKIN-TONE ART, LEFT COLUMN THAT NEVER SCROLLS — 29 Oct 2026

**Prompted by:** "the colour splash doesn't say what the Colour studio does - make
it reflect skin tones (three bands, like the reference)"; "the left sidebar
shouldn't scroll - freeze it, reduce the size so it all fits".

**Colour studio art:** one face cut into three portrait strips - deep, medium and
light skin tones - with matching shade chips underneath. Original inline SVG,
drawn in code; the reference was a watermarked Shutterstock photo, used for the
idea only. Scales up slightly on hover. Replaces the paint splash.

**Compact cards, no sidebar scroll:** the column had `max-height` + `overflow-y:
auto`, so it scrolled whenever the cards were taller than the window. Now it has
no height limit or scrollbar, and the cards are compact: icon, title and status
on one row with the picture on the right; description and link below. Measured
column height (pinned 140 px down): 579 px with everything, 517 without the
note, 433 without the extras, 271 titles only - so shorter windows drop the note
(≤740 px), then the "Try it on" links and the line under STYLE TOOLS (≤680 px),
then the descriptions (≤595 px). Phones (≤760 px wide) keep everything in the
swipeable row. The column stays 270 px wide down to 761 px, so the row fits.
The Colour studio status reads "Palette: warm" (was "Your palette: warm") so it
fits beside the picture.

**Tested (column pinned, page scrolled):** 900 px tall - everything, ends at 719;
790 px (a MacBook browser) - everything, ends at 719; 660 px - ends at 573,
descriptions kept; 580 px - titles only, ends at 411; no titles or statuses
clipped; phone: 263×141 cards with descriptions, no sideways page scroll; the
3D mini mannequin still renders at its smaller size.

---

## StyleMate_frontend_v15_gemini_v13.html — CORNER ART ON THE STYLE TOOLS — 29 Oct 2026

**Prompted by:** "a miniature of the fitting-room 3D model in the Fitting room
card's top-right corner, ideally turning - check feasibility first; a splash of
colours for the Colour studio; a hanger with a cloth on it. Left sidebar only."

**Feasibility of the turning model:** cheap. `/api/avatar` already builds the
same parametric mesh (2,247 vertices, ~110 KB, ~15 ms, no AI call, not
rate-limited) and three.js is already loaded, so a live mini is ~70 lines -
simpler than pre-rendering a video, and it matches the shopper's measurements.

**Page (v13, from v12) - the three cards only:** each card's top row is now the
icon (left) and a small illustration (right); the title moves below them.
- Shop a look: two polaroids, an outfit in the front one, focus corners and a
  scan line that sweeps on hover.
- Fitting room: the live mini mannequin beside a shirt on a hanger, on a rail
  (the hanger sways on hover). A drawn mannequin shows until the 3D one renders,
  and stays if there is no WebGL or backend.
- Colour studio: a paint splash with drips, drops and a wet sheen. Original
  artwork, generated in code - the pngtree reference is watermarked stock, so it
  was used for style only. It tilts slightly on hover.
- prefers-reduced-motion turns all the motion off.

**`stylemate-room.js` (in place):** MINI MANNEQUIN section - its own tiny
renderer (no floor, shadows or controls), the mesh from `/api/avatar`, ~9 s per
turn (time-based, same speed at 60 Hz or 120 Hz), drawn only while the card is
on screen and the tab visible; it takes the fitting room's mesh whenever the
avatar is rebuilt, so it always matches. `window.MINI` exposes its state, like
`window.PAL`.

**Tested:** the 3D mini renders in the card (frames to the full figure);
rendering every 45° gives silhouette widths 23-35 px, a real 3D turn; speed
measured at one turn per 9.4 s even at an extreme frame rate; opening the fitting
room hands the mini the new mesh; descriptions still 3 lines at 1440 px; phone
layout swipes with no sideways page scroll; no console errors. Note: the
in-app test browser runs this tab as hidden (about one frame a second), so the
turn was verified by measurement, not watched.

---

## StyleMate_frontend_v15_gemini_v12.html — CATEGORIES BAR, STYLE TOOLS AS THE HIGHLIGHT — 29 Oct 2026

**Prompted by:** "hide 'What the agent understood' (comment it out); put the
'you own a similar product' check inside the StyleMate Agent message, smaller,
with See the one you own / Open my wardrobe; remove the Ask the agent … My
wardrobe bar and put the shop categories there; remove the categories from the
left; make Shop a look / Fitting room / Colour studio bigger, with a nicer icon
and a three-line description - the highlight of the app."

**Page (v12, from v11):**
- The bar under the header now holds the 5 shop categories (icon, name,
  product count; the open one highlighted). It replaces the feature bar, whose
  items all live elsewhere (My size and My wardrobe in the profile menu; the AI
  tools on the left). On phones it scrolls sideways and replaces the category
  chips.
- The left column is Style tools only: three cards with a gradient icon tile
  (line icons: camera, hanger, palette), a serif title, a status pill (AI · one
  photo / N pieces waiting / Your palette: …) and a three-line description. The
  column is 270 px wide (240 px under 1120 px) to fit them. On phones the cards
  are a swipeable row.
- The wardrobe check is now a short note at the end of the StyleMate Agent's
  answer, with its buttons (See the one you own, Open my wardrobe; or for an
  exact match: the agent's suggestion, Hide items I own, Open my wardrobe).
  Without an answer (the in-page agent) the same note goes where the banner was.
- The bar's wardrobe badge and the sidebar category list were written to
  without null checks; both are guarded (the v10 blank-page lesson).

**`stylemate-room.js` (in place):** the "What the agent understood" block (spec
chips, explanation, how it was read, why the top four matched) is commented out,
with a note on how to bring it back; "Nothing matched" still shows. The answer
is now written before the page shows the results, so the wardrobe note has a
place to go.

**Tested (1440×900 and 375×812, over localhost):** categories bar switches
category (header tab follows); the three cards open Shop a look, Colour studio
and the 3D fitting room; descriptions are exactly 3 lines; "I need a cargo
pants" → no "What the agent understood", the wardrobe note inside the answer,
both its buttons work, styling panel on the right; on a phone the bar scrolls
with no overlap and no sideways page scroll; no console errors.

---

## StyleMate_frontend_v15_gemini_v11.html — STYLING PANEL VIA THE BACKEND — 29 Oct 2026

**Prompted by:** "the Colour combination panel on the right shows when I open
the HTML file directly, but not when I launch with start_stylemate.command."
**Why:** two paths answer "Ask StyleMate anything". Opened as a file, the page
cannot reach the backend, so `stylemate-room.js` falls back to the page's own
agent, which ends by hiding the banner, running the wardrobe check and calling
`renderAssist()` - the panel. Through the launcher the backend answers, and the
backend path only re-drew the grid: no panel, no wardrobe check, banner still
up. It also wrote its answer over the whole `#agent-response`, deleting the
page's `#agent-trace` and `#wardrobe-flag`, so the wardrobe check had nowhere to
go and a later in-page search crashed (`renderTrace` on null).
**Change:** the page gets `showSearchResults(results, heading)`, the same
follow-up its own agent does (banner hidden, filters reset, wardrobe check,
similar-to-owned tags, styling panel). `stylemate-room.js` (in place) hands the
backend's ranked list to it, keeping the backend's order, and writes its answer
into its own `#agent-backend` box instead of replacing the panel. Older pages
keep the old behaviour.
**Tested over localhost (as the launcher serves it):** "I need a cargo pants" -
backend answered (no fallback), 36 results in the backend's order, banner hidden,
wardrobe check shown, Colour combination panel styling "Women Solid Y2K Cargo
Trousers · White"; a second search ("white sneakers") updates the same box and
the panel; no console errors.

---

## StyleMate_frontend_v15_gemini_v10.html — STYLE TOOLS, GEMINI STATUS LIGHT — 29 Oct 2026

**Prompted by:** "remove the Agent model box completely; move Shop categories
down and add, in the same style, Shop a look / Fitting room / Colour studio;
the header ◉ icon should be green when Gemini has a working API key, red if
not, and no longer open the Colour Studio. UI changes only."

**Page (v10, from v9):**
- The Agent model box in the left column is gone.
- New **STYLE TOOLS** section above SHOP CATEGORIES, same row style:
  📸 Shop a look (AI), 🪞 Fitting room (pieces waiting), 🎨 Colour studio (saved
  palette, or "new"). Each opens its feature; the feature bar is unchanged.
- The header icon is now a status light (`#model-light`): grey while checking,
  green when Gemini is the active provider and its key works, red otherwise
  (bad or missing key, or backend not running), with the reason on hover.
  Clicking it opens model settings (what "Change model" in the removed box did);
  it no longer opens the Colour Studio.
- The removed box's button had been wired without a null check, which stopped
  the page script and left the page blank in the first v10 build; now guarded.

**`stylemate-room.js` (in place):** the 20-second status poll now also paints
the header light, and keeps running when the page has no status card. Older
pages still get their card. No backend change.

**Tested (1280×800):** light green with the reason "Gemini connected ·
gemini-3.1-flash-lite · photos: gemini-3.5-flash-lite"; backend stopped → red,
"the StyleMate backend is not running"; restarted → green. Sidebar rows open
Shop a look, Colour studio and the 3D fitting room; the light opens model
settings, not the Colour Studio; no console errors after the fix.

---

## StyleMate_frontend_v15_gemini_v9.html — FITTING ROOM AS IN v3 — 29 Oct 2026

**Prompted by:** "in v8 the fitting room is messed up — look at v3".
**Found:** the fitting-room code (page and `stylemate-room.js`) is identical in
v3 and v8, and with the same state the two render identically. The one change
that reached it: since v4, `setShopFor()` also set the size profile's gender, so
saving Women in the Colour Studio switched the 3D body model to Female while the
measurements stayed the seeded male defaults (chest 108 cm, shoulder 46 cm). A
men's T-shirt then read "TOO TIGHT" instead of "REGULAR".
**Change:** `setShopFor()` no longer touches the body model. As in v3, it is set
only by the fitting room's Male/Female chips and in My size. Nothing else changed.
**Tested:** saved Women in the Colour Studio → body model stays Male; with the
same T-shirt and jeans the fitting room matches v3 (2 garment shapes, T-shirt
REGULAR); no console errors. An avatar already switched to Female by v4-v8 is
put back with one click on Male in the fitting room.

---

## StyleMate_frontend_v15_gemini_v8.html — PROFILE MENU, ORDERS, SLIM BANNER — 29 Oct 2026

**Prompted by:** "hovering on my profile icon should show a list: Orders, Returns,
My size, Wardrobe, each opening its feature; don't remove anything"; "make the
'Find your thing' banner smaller in height".

**Profile menu.** Hovering the avatar/name (or focusing it - keyboard, touch)
opens "Your account": Orders, Returns, My size, Wardrobe, with counts. Each opens
the existing feature (Returns drawer, size studio, wardrobe drawer) or the new
Orders view; after a click the menu closes until the pointer leaves. Nothing was
removed - the Returns button and feature bar stay. The chip used to clip its
overflow, which would have hidden the menu; the narrow-screen rule that hid the
name now hides only the name, not the menu.

**Orders (new).** One list, newest first: delivered orders (the wardrobe's),
returned ones (status, refund, reason) and orders placed at the demo checkout,
which are now kept per account in this browser (`sm_orders_<user>`), so the
checkout feeds Orders. SWAP POINT: GET /orders.

**Banner.** One-line heading, smaller type and orb, no minimum height: about
111 px tall at 1280 px wide, from about 175.

**Tested (1280×800):** hover shows the menu with Orders 11 / Returns 6 /
Wardrobe 5; real clicks open Orders (5 delivered + 6 returned), Returns, My size
and Wardrobe, and the menu closes; a placed demo order appears first in Orders
(12) - removed after the test; no console errors.

---

## StyleMate_frontend_v15_gemini_v7.html — SEARCH BAR, RETURNS, RETURN PENALTY — 29 Oct 2026

**Prompted by:** "the search bar at the top says no item matching for jeans";
"a Returns button next to Cart with past returns, backdated, for the test
user"; "warn at checkout that returning costs a ₹100 penalty once 6 are
returned"; "make the cart image 1/3 the size"; "remove the Dataset SKU line".

**Top search bar.** It only searched the open category tab, so "jeans" with
Ethnic open found nothing. Now `textSearch()` searches the whole catalogue: every
word must match the name, brand, type, colour, usage, category or the product's
own description; plurals fold ("jeans"/"jean"), "t-shirt"/"tee" are one word, a
word's start is enough, and one-letter typos are corrected ("jeens" → jeans,
"kurtha" → kurta, shown in the heading). "men"/"women" in the query pick the
section (otherwise the Shopping for choice applies); "under 1500" caps the
price, and an empty result says how many exist above the cap. When no product
has every word, the closest are shown and labelled. No AI. Placeholder now
"Search products, brands, colours…".

**Returns.** "↺ Returns N" button beside Cart, same style. The demo account
`test` has 6 backdated 2026 returns against real catalogue SKUs (men's, not
already in the wardrobe): order, bought/returned dates, reason, refund. The
drawer says they are seeded. SWAP POINT: GET /orders/returns.

**Return penalty.** `RETURN_TIERS=[{from:6,fine:100}]`: with 6+ past returns,
each further return costs ₹100 (static for now; add tiers such as
`{from:10,fine:1000}` later). The cart and checkout show a warning banner and
"↺ ₹100 penalty if returned" under every item; the order confirmation repeats it.

**Cart.** Thumbnails 120×160 (they rendered at full drawer width, the same id-rule
problem the wardrobe had). **Product cards** no longer show "Dataset SKU: … ·
Image and product attributes are from the same source record."

**Launchers (in place).** `start_stylemate.command` already serves the highest
page version, so it needed no change for v7. The copy inside `stylemate/` (the
one that goes to GitHub) was behind the root copy on the Python checks (prefer
3.10+, rebuild a 3.9 venv, install `eval_type_backport`); it is now identical
to the root copy. `Start_StyleMate.bat` (Windows) never refreshed the page at
all; it now runs `backend/sync_static.py` first (step 4/5), so Windows also
serves the newest version.

**`start_stylemate.command` (in place, later the same day).** Prints
"→ PAGE VERSION: v15 · gemini v7" in step 5 and a "Page" line in the Running
summary. After start-up it fetches `/` from the server and compares it with the
files, so it reports the version actually being served (and which one, if it is
not the newest). A StyleMate backend left over from an earlier run, or from
another folder, used to be reused as-is ("reusing it"), keeping old code; it is
now restarted (`--no-restart` keeps the old behaviour). The backend's pid is
recorded, so Ctrl-C now stops it as the help text always said. The browser is
opened at `/?page=v15geminiv7` so it cannot show a cached older page. Both
copies of the script are identical.

**Tested:** jeans from the Ethnic tab → 56; women jeans → 29 women's; kurta 65;
silver watch 5; jeens/kurtha corrected; "men sneakers under 2000" → nothing,
"2 found above that price" (the only men's sneakers cost ₹8,999); Returns 6 in
the header and drawer; cart and checkout warnings on both items; images 120×160;
no card shows the Dataset SKU line; no console errors.

---

## StyleMate_frontend_v15_gemini_v6.html — PHOTO ALWAYS SETS WOMEN/MEN — 29 Oct 2026

**Prompted by:** a man's photo in the Colour Studio left "All" selected.
**Cause:** Gemini did answer — the audit log for that call has
`"section": "men"` — but v5 ignored it when a choice had been clicked earlier
in the same sitting (the shopper had clicked All before uploading).
**Change:** every photo reading now sets Women or Men, over a saved choice and
over an earlier click, because the photo is the newest input; a click after the
reading still switches it. The AI reading line now shows it ("warm undertone ·
medium depth · shopping for Men", or "Women or Men not clear — pick one").
**Tested:** All clicked, then a man's photo → Men, products all men's; a woman's
photo → Women; clicking All afterwards stays All.

---

## StyleMate_frontend_v15_gemini_v5.html — PHOTO PICKS WOMEN/MEN, STRICT LISTS — 29 Oct 2026

**Prompted by:** "If it's a girl, Women should be chosen by default; if it's a
guy, Men … you're allowed to shift between choices … when we choose Women only
women-specific options must be shown, even if it's fewer."

**Page (v5, from v4):**
- The choices are **Women / Men / All** (was Women's / Men's / Both).
- **The photo picks the default.** In the Colour Studio a reading of a girl
  selects Women and of a man selects Men, now also over a saved choice (the
  saved one may be someone else's). A choice clicked in that sitting is never
  overwritten; one click switches it.
- **Strict lists.** Women = women's products only, no unisex, everywhere: the
  browse grid, the in-page agent (and the model's SKU list), Complete the look.
  The agent no longer relaxes the section when results are few. All = everything.
  Chip: "Showing women's products only · show all".

**`stylemate-room.js` (in place):** Shop a Look's buttons are Women / Men / All
(was As worn / Men / Women). It opens on the person in the photo, with
"chosen from the photo" beside it; a photo with no clear person uses the saved
choice, else All. An empty part of the outfit says "No women's product like
this in the catalogue. Try All."

**Backend (in place):** `look.py` - `look_audience()` (photo → saved → all)
replaces the per-item resolution; women/men filter strictly with no fallback,
All leans on the garment's cut only as a soft score; `/api/look` returns
`audience` and `audienceFrom`. `search.py` and `palette.py` filter strictly
(no unisex) too.

**Tested:** saved Men + a girl's selfie → Women, studio products 48 women's /
0 other; clicking Men → 32 men's only; Women saved → every category, AI search
women's only; "a watch for my husband" → men's only; Shop a Look with Women
saved: a man's photo opens on Men (all men's), Women → all women's, All →
mixed; a girl's photo with Men saved opens on Women.

---

## StyleMate_frontend_v15_gemini_v4.html — SHOPPING FOR (WOMEN'S / MEN'S) — 29 Oct 2026

**Prompted by:** "In the Colour Studio I want to tailor recommendations by
whether it is a boy or girl … girls were being recommended boys' clothes."

**Why it happened (three causes):**
1. Every new visitor was silently set to **male**: the size profile seeds
   `gender:'male'` on first visit, and AI search, the Colour Studio's product
   rows and Shop a Look all read that field. A girl who never opened the size
   panel shopped as a man.
2. Shop a Look judged men's/women's from the garment's cut only. A plain tee
   or jeans is "unisex", so the (male) default decided and men's jeans won.
3. 248 catalogue SKUs were "unisex" only because their URL slug had no gender
   word; 65 of them say Men/Women in the photo file name (e.g. a man's hoodie).

**Page (v4, from v3):**
- Colour Studio gets **03 / SHOPPING FOR**: Women's (girls & women), Men's
  (boys & men), Both. Saving the palette now requires a choice. Stored as
  `shopFor` in `sm_style`; it also sets the size chart / 3D body model gender.
- The photo reading suggests it (`section` in the vision JSON) **only when the
  shopper has not chosen**, labelled "Suggested from your photo". The prompt no
  longer forbids gender; it still forbids age, ethnicity, health and mood.
- One helper, `shopFor()`, drives: the browse grid (women's/men's + unisex,
  with a "show everyone's" chip), the in-page agent (default audience unless
  the request names someone — "for my husband" still gets men's), the model's
  SKU list, Complete the look, and the agent's profile.
- Cards show Women / Men next to the brand.
- No choice saved = both, never a hidden default. A girl who had already picked
  Female in the size panel keeps it.

**`frontend/stylemate-room.js` (in place):** search, the studio's product rows
(refill instantly when the choice changes) and Shop a Look use `shopFor()`;
older pages fall back to the size-profile gender as before. Shop a Look opens on
"Women (you)"/"Men (you)" when a choice is saved; "As worn" re-matches from
text and each view is kept, so switching back sends nothing.

**Backend `services/look.py`:** the vision schema adds `wearer`
(women/men/unclear). Audience order: the shopper's choice → the person in the
photo → the garment's cut. The search text swaps the model's gender words for
the audience being shopped ("men blue jeans" on a girl → "women's blue jeans").

**Catalogue:** `build_myntra_catalogue.py --refine-audience` (no CSV needed)
re-labelled 65 unisex SKUs from their photo file names (46 women's, 19 men's);
same 1,000 products. A full rebuild now applies the same fallback. The search
index was rebuilt for the new labels and the shipped copy in `backend/app/data/`
replaced (`emb-…-59e7a73cb800ba14.npz`).

**Tested:** new visitor sees everyone's products; choosing Women's leaves 0
men's items in the studio rows, every category, AI search and Complete the
look; "for my husband" → men's; a woman's outfit "as worn" → all women's; a
man's outfit with Women's saved → women's versions, "As worn" → men's; a
woman's selfie pre-selects Women's; a fresh disk loads the shipped index
without re-embedding.

---

## Hosting on GitHub + Render — 28 Oct 2026 (no page change; serves v3)

**Prompted by:** "host it on Render and GitHub so anyone can open it."
The `stylemate/` folder is the repository; Render builds it from GitHub.
Step-by-step instructions: `stylemate/DEPLOY.md`.

**New files:** `stylemate/render.yaml` (one free web service, Singapore,
`pip install` + `sync_static.py`, `uvicorn` on `$PORT`, health check
`/api/ping`, key prompted once via `sync: false`), `stylemate/.python-version`
(3.12; Render now defaults to 3.14), `stylemate/.gitignore` (key, `.venv`,
`backend/var`, logs), `backend/sync_static.py` (build step: highest page
version + 3D assets into `app/static`), `backend/app/guard.py`,
`backend/app/data/emb-gemini-embedding-001-*.npz` (shipped search index).

**Public mode (`SM_PUBLIC=1`, set by render.yaml; off locally):**
- 15 AI calls per visitor per minute, 600 per day site-wide (env-tunable);
  429 with a retry time past that.
- `POST /api/settings/llm` is 403: no visitor can swap key/provider/model.
- `/api/llm/chat` ignores a client-requested model and caps prompt size.
- Audit records go to `/api/audit/log` → one line in Render's Logs tab
  (localhost:8765 would have been each visitor's own machine).
- CORS off unless `SM_CORS` is set.
- Also everywhere: Gemini model list cached 5 min (each tab polls every 20 s),
  `/api/ping` for health checks, held fitting-room photos capped at 64.

**Verified** by exporting exactly the files git would push (56 files, 8.3 MB;
no `.env`, `.venv`, `var/`, logs; the real key in none of them) and running
them Render-style with no `.env`: build served v3; key from env only;
search index ready from the shipped file on an empty disk; settings 403;
no CORS header for another origin; `gemini-4-argon` request answered by
`gemini-3.1-flash-lite`; 4th call in a minute 429; Shop a Look worked in the
page with its audit line in the server log and zero calls to :8765.
Not verified: a real Render build (needs your GitHub + Render accounts) and
`pip install` on Python 3.12 (this Mac has only 3.9).

---

## `StyleMate_frontend_v15_gemini_v3.html` — 28 Oct 2026 — CAMERA + WARDROBE LAYOUT

**Prompted by:** "when I click camera the Capture option needs scrolling; the
wardrobe has oversized images with the text squeezed into the corner."

**Camera (Colour Studio, and Shop a Look which shares the controls).**
- Root cause: `#tone-ph{display:grid}` outranked the browser's `[hidden]` rule,
  so the big "Curious about your colour?" placeholder stayed on screen after
  the camera started and the live video stacked underneath it, pushing
  Capture below the fold. Added `#tone-ph[hidden]{display:none}`.
- While live, the preview is capped to `min(46vh, 380px)` with `contain` (the
  preview shows exactly the frame that will be captured), and the
  Capture / Cancel bar is sticky at the bottom of the panel as a backstop.
- Verified at 1280×720 with a stand-in camera stream: the placeholder hides,
  Capture is on screen with the panel unscrolled, capture still works, and the
  panel returns to normal afterwards. Same for the Shop a Look camera.

**Wardrobe drawer.**
- Root cause: `#drawer-content img.real` (an id rule) beat `.ward-row img.real`,
  so Myntra's 360×480 photos rendered at full size. HuggingFace thumbnails were
  small enough that this never showed before.
- Thumbnails are now 120×160 (a third of before), text gets the rest of the row.
- Intro said "Six backdated orders"; it now states the real count (5, since
  Beauty left the catalogue).

---

## `StyleMate_frontend_v15_gemini_v2.html` — 28 Oct 2026 — MYNTRA CATALOGUE + SHOP A LOOK

**Prompted by:** "upload a photo of a person, have the AI recognise the t-shirt,
jeans, watch, bands, lockets, give that to the Python backend, search the
catalogue for similar SKUs and recommend them. Use 1,000 Myntra SKUs across 5
categories instead of HuggingFace. Send the image once, turn it into text, and
use semantic search."

**Catalogue: 1,000 Myntra SKUs replace the HuggingFace fetch.**
- `stylemate/build_myntra_catalogue.py` (run once; `--force` to rebuild) streams
  the 1.4 GB `myntra dataset/myntra202305041052.csv` in ~14 s, standard library only.
- The CSV has no category or colour column, but each product URL does:
  `myntra.com/<type>/<brand>/<slug>/<id>` — type from the path; gender, colour
  and the search text from the slug.
- 5 categories: Western 340 · Accessories 260 · Footwear 170 · Ethnic 130 ·
  Sports 100. Beauty dropped (nothing in an outfit photo maps to it, and with it
  the wardrobe's consumable/refill demo line).
- Per type: most-rated first, rating ≥ 3.5 and ≥ 10 ratings, max 2 per brand,
  alternating men/women, no kids' items, re-listed duplicates removed.
- Real price, MRP, discount, rating and photo (Myntra CDN, 360×480). 169 SKUs
  have no colour anywhere in their URL or name and say "Not specified".
- Outputs `backend/app/data/myntra_catalogue.json` (the backend's source of
  truth) and `frontend/catalogue.js` (for a file:// page). The backend also
  serves `/catalogue.js` from the JSON, so the page and backend always agree.
- Backend pins it: replaces the SQLite table on startup when the file changes;
  `/api/catalogue/sync` from the browser is now a no-op.

**Shop a Look: image once → text → semantic match.**
1. Page shrinks the photo to 768 px JPEG; backend enforces the same bound.
2. ONE Gemini vision call (`gemini-3.5-flash-lite`) with a response schema:
   per item slot, catalogue article type, colour, pattern, listing-style
   details, worn_by and a one-line product-title description. Prompt walks
   wrists/hands/neck/ears/face/waist so small accessories are not missed.
   Measured: ~1,600–1,700 in / 270–500 out tokens, 0 thinking tokens, ~3.5 s.
3. Cached by image + prompt hash: the same photo is never sent twice.
4. Matching in Python, no chat model: hard filters (slot, audience from the
   garment's cut), then 45% embeddings (`gemini-embedding-001`, 768-d) +
   20% BM25 + 15% same article type + 15% same/related colour + 5% audience.
   Catalogue embedded once (10 batch calls, cached in `var/cache/`); each look
   is ONE embedding request for all its items.
5. "As worn / Men / Women" re-matches via `POST /api/look/match` from the text
   only — zero image tokens.
- Verified: jeans photo → the exact SKU ranked #1; t-shirt photo → exact SKU #1
  plus cap, track pants and sneakers found; kurta photo → earrings, bangles,
  clutch found (the kurta itself read as "ethnic dress").
- Each call writes an audit file to `logs/` (tokens, latency, cached, semantic
  model); the image is never logged.

**Page (v2):** real price / MRP / discount / ★ rating on cards; "Recommended"
now sorts by rating × review count; HuggingFace copy removed; Shop a Look panel
shows what the AI saw, the cost line and the matches. `stylemate-room.js`
rewritten for the new flow (falls back to the colour-only matcher if the
backend is down).

**Launcher:** frontend assets are now copied into `app/static` when they
*differ*, not only when missing, so edits to `stylemate-room.js` reach the server.
Two more launcher changes (both copies of `start_stylemate.command`):
- New step 2/5 **Catalogue**: if `backend/app/data/myntra_catalogue.json` is
  built, it says so and does nothing; if missing or unreadable, it builds it from
  the CSV (~15 s); if the CSV is gone too, it says exactly what to restore.
  Recreates `frontend/catalogue.js` from the JSON if only that is missing.
- The page served is the **highest version number** (`v15_gemini_v2` >
  `v15_gemini_v1`, `v16_*` > `v15_*`), not the newest file date.
- Tested: built → skipped; JSON missing → rebuilt with identical rows; JSON and
  CSV missing → clear message, no crash; catalogue.js missing → recreated.

**The Myntra CSV is not needed at runtime.** Only `build_myntra_catalogue.py`
reads it. `archive (1).zip` (118 MB) holds the identical CSV, so the 1.3 GB
`myntra dataset/` folder can go as long as the zip is kept for rebuilds.

---

## `StyleMate_frontend_v15_gemini_v1.html` — 28 Oct 2026 — FIRST GEMINI VERSION

**The key never touches the browser.** The page used to call Ollama directly
from JavaScript. A Gemini key cannot live there — anyone who opens the page can
read it. So:

- New backend endpoint **`POST /api/llm/chat`** relays one model call. The
  server holds the key and picks the provider; the page never learns which.
- The page's `llmChat()` now posts there. That one function underpins the whole
  pipeline — query parsing, reranking, the colour studio's photo reading — so
  all of it moved to Gemini in a single change.
- `transport: 'auto'` → backend when served over http(s), direct Ollama when
  opened as a `file://` page, so the standalone page still works.

**Models** (ids verified against the Gemini docs, 28 Oct 2026):
`SM_GEMINI_TEXT_MODEL=gemini-3.1-flash-lite` — cheapest current-gen model that
still reasons, and the only one defaulting to *minimal* thinking, so reasoning
is opt-in rather than billed by default. `SM_GEMINI_VISION_MODEL=gemini-3.5-flash-lite`
— one call per photo, so a better model costs almost nothing there. Both are
listed with image input on the pricing page.

**Fixed while testing:** `base64.b64decode` ignores characters outside the
base64 alphabet by default, so a corrupt image decoded to `b""` and reached the
model as an empty picture with a 200 response. Now `validate=True`, and empty
images are rejected.

**Not done, deliberately:** `/api/llm/chat` is an unauthenticated relay to a
paid API. Fine on localhost. Before this is exposed to the internet it needs
auth and a rate limit, or anyone who finds the URL spends the key's quota.

---

## `stylemate/` — StyleMate v15 + Ollama v8 — 28 Oct 2026  ⚑ FINAL OLLAMA VERSION

The project moves into the `stylemate/` folder: a FastAPI backend that serves
the page, the 3D fitting room (three.js, OrbitControls, stylemate-room.js), and
an `/api/*` layer with its own Gemini/Ollama router.

**Checked first:** v15 already contains our Ollama work **through v8** — the
two-stage pipeline, the vision colour studio, the balanced-brace JSON parser and
the palette badge are all in it. Nothing needed porting. The page still calls
Ollama directly from the browser; the backend's `/api/*` routes are available
but unused by the page today.

**Page:** `frontend/StyleMate_frontend_v15_ollama_v8.html` is now the source of
truth. The launcher copies it to `backend/app/static/index.html` when it differs,
so the version lives in the filename without breaking the server's static mount.

**`.env` — and a gap worth knowing about.** `backend/.env.example` says "copy to
.env", but nothing in the code read a .env file and `python-dotenv` is not a
dependency: a .env would have sat there being silently ignored. Added a
dependency-free loader to `config.py` (KEY=VALUE, `#` comments, optional
`export`, optional quotes). **A value already in the shell wins** — the launcher
and the shell are more specific than a file in the project.

**The page gets its settings from .env** through a new `GET /api/config`, which
publishes the non-secret half: Ollama host, text and vision model, num_ctx,
timeout, results, log sink. `GEMINI_API_KEY` is deliberately NOT in it — only
whether a key is present. The page adopts these at boot, and anything the
shopper changed by hand in Agent settings still wins over them.

**One launcher:** `start_stylemate.command`. Loads .env, restarts Ollama with
`OLLAMA_ORIGINS=*`, `OLLAMA_CONTEXT_LENGTH`, `OLLAMA_MAX_LOADED_MODELS=2`,
checks both models (`--pull` to fetch), starts the log sink, creates the venv
and installs requirements on first run, starts uvicorn, verifies the 3D assets
are in `app/static`, prints the live config and opens the browser. Ctrl-C stops
the backend and sink; Ollama is left up deliberately.

`.env` defaults set here: `SM_VISION_MODEL=qwen3-vl:8b` (the one pulled and
working; the project example names `qwen2.5vl:7b`), `SM_NUM_CTX=32768` and
`SM_LLM_TIMEOUT=300`.

---

## `stylemate_v10_featurebar_mysize_ollama_v8.html` — 28 Oct 2026

**Prompted by:** "send the saved palette and its recommended colours with the AI
query, and tag matching products with something visually distinct from the
existing tags."

**The palette now travels with the request.** When the Colour Studio has been
used, both model calls carry it:
- Stage A (understand) gets the palette name, depth and its colours.
- Stage C (rank) gets them again, where they actually change the order.

Sent as a **soft preference, stated twice**: "this is a PREFERENCE, not a
requirement… never make a colour a hard constraint because of this list". A
shopper who asks for a black shirt gets a black shirt whether or not black is in
their palette. The palette orders results; it never filters them. With no
palette saved, nothing is added to the prompt — no empty header.

**New badge: ✦ SUITS YOUR PALETTE**, deep berry `#6e3b5a` with white text.
- 8.6:1 contrast on white, above the 4.5:1 AA threshold.
- 156° from the wardrobe green, 112° from the "similar" blue-grey, 76° from the
  refill amber — distinct from all three at a glance.
- Orange was the suggestion, but the refill badge is already dark amber and the
  whole page sits on a warm rust-and-paper palette, so an orange badge would
  have read as a variant of an existing tag rather than a new kind of thing.

Ribbons now **stack** in a flex column, so an item can be both "in your
wardrobe" and "suits your palette" instead of one hiding the other. The card's
footnote line explains the match in words: "Maroon is in the warm palette you
saved in the Colour Studio."

The badge shows whenever a palette is saved, not only after an AI search — it
reflects the saved preference, which is true while browsing too. Switching
palette re-badges everything on the next render; the colour set is cached by
palette+depth and invalidates on change.

The agent trace says when the palette was sent and that it ordered rather than
filtered.

---

## `stylemate_v10_featurebar_mysize_ollama_v7.html` — 28 Oct 2026

**Prompted by:** "AI READING UNAVAILABLE — the model replied, but not with
usable JSON. Diagnose why."

**Cause: the JSON parser, not the model.** `extractJson` took everything between
the first `{` and the last `}`. Tested against nine replies a reasoning model
really produces, **five failed** — and qwen3-vl reasons before it answers:
- an unclosed `<think>` block when the token budget runs out mid-thought
- braces inside that reasoning, which the first-to-last span swallowed
- the reply arriving in `message.thinking` with `content` empty
- JSON truncated by `num_predict`
- two objects in one reply, the wrong one picked

**Fixes**
- Parser rewritten: scans for *balanced* objects with string-awareness, and
  callers pass the keys their answer should have, so the right object wins when
  there is more than one. 9 of 9 now behave correctly.
- `think:false` sent on the vision call so the model answers instead of
  reasoning into its budget; a 400 retries without the field for models that
  do not accept it.
- `message.thinking` is read when `content` comes back empty.
- Vision `num_predict` 400 → 900; one automatic retry at 1,400 with a blunt
  "raw JSON only" instruction.
- When it still fails, the panel **shows the raw reply**, the token count and
  how much of it was reasoning. "Not usable JSON" with the reply hidden is an
  error nobody can act on.
- Log records gained `thinking_chars` and `content_was_empty`.

---

## `stylemate_v10_featurebar_mysize_ollama_v6.html` — 28 Oct 2026

**Prompted by:** "run qwen3-vl:8b too — send the Colour Studio photo to the
vision model, ask for undertone and depth, explain what they mean, say it is an
AI response, and if there is no person in the image say so."

**A second model, for the Colour Studio.**
- `qwen3-vl:8b` is called on capture or upload. The photo is re-encoded to
  768px JPEG, sent as base64 in `messages[].images` on Ollama's native
  `/api/chat`, with `num_ctx 4096` — one photo and one question need nothing
  like 32k, and the two models share the same memory.
- Returns `person_detected`, `skin_visible`, `undertone`, `depth`, `confidence`,
  `observation`, `caveat`. Undertone and depth are applied to the selectors only
  when the value is one of the allowed ones; `"bronze"` is ignored.
- The panel shows the reading, the model's confidence, what it saw, and any
  caveat, labelled as a local AI estimate the shopper overrides with one tap.
- Definitions of undertone and depth are the **page's** fixed words, not the
  model's. A definition that changes per call is not a definition.

**No person in the photo.** The model is told to say so rather than read a skin
tone off a sofa. Critically, "no person" is treated as an **answer**, not a
failure: the pixel-average fallback does *not* then run. Getting this wrong
would have had the old estimator guess a skin tone from a dog photo — which is
precisely the nonsense the vision model was added to prevent. The pixel
estimate now runs only when the model is genuinely unavailable.

**Honesty fix.** The studio used to say "Nothing is uploaded, stored or sent
anywhere." The photo now goes to Ollama, so it does leave the page even though
it never leaves the machine. New wording: "read on this computer… goes to the
model running at localhost and nowhere else."

**Log hygiene.** The base64 photo is stripped from the audit record — ~100 KB
per call, and no reason to write a picture of someone's face to disk. The
prompt is logged, the pixels are not. Records now carry `has_image` and the
model that actually ran.

**Running two models.** `runall.sh` sets `OLLAMA_MAX_LOADED_MODELS=2` so Ollama
holds both instead of evicting one on each switch, checks whether the vision
model is pulled, offers `--pull-vision`, and reports total VRAM with a note that
a 7B plus an 8B on ~12 GB is tight — Ollama may swap one out and reload on
demand. Nothing breaks either way; the first call after a swap is just slower.

---

## `stylemate_v10_featurebar_mysize_ollama_v5.html` — 28 Oct 2026

**Prompted by:** "logs are getting downloaded every time I send a query — I just
want them in my folder", and the upload of `stylemate_v10.html`.

**Ported v5 onto the v10 base.** v10 is v8 plus ~40 lines, so the v8→v10 delta
was applied to the v5 file rather than re-applying 25 Ollama edits onto v10 —
far fewer ways to go wrong. 10 of 13 regions merged automatically; three were
touched by both sides and were merged by hand:
- `card()` — v10's apparel size picker plus v5's "similar to one you own" ribbon.
- Settings modal — v10's provider/API-key fields plus v5's pipeline switch.
- A duplicated "My size" feature-bar button, left behind by the move.

Gained from v10: per-item S/M/L/XL picker with a size-chart modal, a model
provider dropdown and API-key field (UI only, not wired), sidebar relabelled
"Agent model".

**Logs no longer download.** `logFallbackDownload` now defaults to **false**, so
nothing lands in Downloads. Files are written only by the sink, into `logs/`.

**Why the sink was never running:** macOS ships a `/usr/bin/python3` that is a
stub — it opens the Xcode command-line-tools dialog and exits. That is what
`sink.log` contained, so no log file was ever written, which is why the
browser-download fallback was firing on every search.
- Added `serve_with_logs.js`, a Node version of the sink, same endpoints and
  same path-traversal guard.
- `runall.sh` now probes for a runtime that actually *runs* (`python3 -c 'print(1)'`,
  then homebrew pythons, then `node`) and reports the exact fix if none works:
  `xcode-select --install` or `brew install node`.

---

## `stylemate_v8_featurebar_mysize_ollama_v5.html` — 28 Oct 2026

**Prompted by:** ChatGPT's two notes on architecture (use the model as a query
interpreter, not as catalogue memory; handle vague queries by relevance rather
than by inventing filters), plus "what do we do when the query is vague?"

**The change: a two-stage pipeline, now the default.**

| | v4 and earlier | v5 |
|---|---|---|
| Model's job | read ~430 product rows and pick | read one sentence, return conditions |
| First call | ~15,500 tokens | ~430 tokens (**97% smaller**) |
| Product rows in call 1 | ~430 | none |
| Calls for a precise query | 1 | 1 |
| Calls for a vague query | 1 | 2 (understand, then rank) |
| Price enforcement | model | code |

- **Stage A — understand.** One small call: the sentence plus the catalogue's
  *vocabulary* (category ids, article types, colours, usages, price range). No
  product rows. Returns hard constraints, soft preferences and a `query_type`.
- **Stage B — search.** Ordinary code over every SKU. Hard constraints are
  enforced here. A price cap is a number comparison, not something to reason about.
- **Stage C — rank.** A second call, only when it will change the answer: a
  vague request, or many candidates with soft preferences to order by. A precise
  request with a short shortlist returns after one call.

**Vague and empty queries.**
- `precise` → filter, usually no second call.
- `vague` → never invent a hard constraint; if the filters match nothing, take an
  even spread across all categories and let the ranking call choose. This is the
  one case where the second call is clearly worth the time.
- `insufficient` ("hi", "show me stuff") → ask one short question with category
  buttons. Nothing is searched, because guessing would fill the page at random.

**Other fixes in v5**
- A guessed category is no longer applied as a *hard* filter on a vague request.
  "Casual dinner" was quietly becoming `categories: ['ethnic','western']`.
- Prices are parsed from the sentence in code and override the model's number.
  Tested: model says `max_price: 12000` for "under ₹1,200", code wins.
- A failed ranking call keeps the filtered results instead of losing them.
- Settings has a **Search pipeline** switch; `full-catalogue` keeps the old
  single-call path so the two can be measured against each other.

---

## `stylemate_v8_featurebar_mysize_ollama_v4.html` — baseline

The state everything above builds on.

- Search bar is an ordinary keyword filter. AI runs only from "Ask StyleMate
  anything" → **Find my match**.
- Prompt fitted to the context ceiling: Ollama accepts at most half of `num_ctx`
  and silently keeps only the tail past that. Rows are selected by relevance to
  the request, ~430 of 1,200 at `num_ctx 32768`.
- Measured: these rows cost **2.07 characters per token**, not 3.6.
- The request is repeated before the rows and in the task tail, because
  truncation eats the head first.
- Off-brief guard: an answer made entirely of a different product kind than the
  request is rejected and retried.
- Failure ladder: full → repair → facets-only → keyword rules.
- Wardrobe check distinguishes owned / similar / refill, with card tags.
- Audit logging to `logs/*.json`, no UI. `keep_alive: 30m`, `num_predict: 1200`,
  max 24 SKUs returned.
- Text only to the model: no images, paths or base64, ever.

### Known open items
- `sink.log` shows the log sink failing to start on macOS (`xcode-select`
  prompt). Fix with `xcode-select --install`, else no `logs/` files are written.
- A reported "T-shirts under ₹1,200 → 300 s → no results" has not been
  reproduced: the keyword fallback returns 38 results for that query in testing.
  The 300 s is the timeout. Needs the log file from that search to close out.
- Not built yet: local embeddings for semantic retrieval (ChatGPT's Solution 2),
  and catalogue enrichment with occasion/style tags.
