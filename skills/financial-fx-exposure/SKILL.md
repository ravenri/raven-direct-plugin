---
name: "financial-fx-exposure"
description: "Renders a deal's foreign currency exposure from Raven's dedicated fx_risk tile - revenue/cost geography, debt denomination, natural vs. financial hedging, and EBITDA sensitivity to FX moves. Faithful stored-read: verdict and rationale, revenue mix by geography, segment concentration, debt denomination, EBITDA sensitivity scenarios, mismatch analysis, hedging program, EM-specific considerations, covenant FX impact, and an FX scorecard. Always states plainly when a sensitivity estimate is a geographic proxy rather than an actual-currency-flow calculation - usually the tile's single most important caveat. Where a company has minimal or no FX exposure, says so directly rather than manufacturing detail. Use for \"FX exposure,\" \"foreign currency risk,\" \"currency hedging,\" \"EBITDA sensitivity to FX,\" or how exposed a deal is to exchange-rate moves."
when_to_use: "Use for \"FX exposure,\" \"foreign currency risk,\" \"currency hedging,\" \"EBITDA sensitivity to FX,\" or how exposed a deal is to exchange-rate moves. Do not use for commodity or interest rate exposure."
---

# Financial - FX Exposure

Renders the deal's foreign currency exposure, sourced from Raven's dedicated `fx_risk` tile. A faithful
stored-read: exposure verdict, revenue/cost geography, debt denomination, EBITDA sensitivity, mismatch
analysis, hedging program, and a scorecard.

**This is a stored-read, not an analysis pass.** The tile already holds the exposure summary, the
sensitivity scenarios, and the narrative for each. This skill renders that faithfully, in house voice, and
never computes, re-scores, or invents an exposure estimate, sensitivity figure, or verdict.

## Scope

FX exposure only. This tile's own `Gaps` block is out of scope here — `fx_risk` is already a confirmed
extension source in the Diligence Gaps skill, and rendering its gap list again under this workflow's name
would double-count the same content. Covenant testing itself belongs to `test-covenants`; this skill
renders the tile's own statement of how an adverse FX move would affect covenant headroom as a point-in-
time fact, cross-referencing `loan-coverage` / `test-covenants` figures if those have already run this
conversation, never re-deriving them.

**EBITDA sensitivity basis.** Apply `references/conventions.md` so the sensitivity figure's EBITDA basis
is named correctly (Reported / Adjusted / PF Adjusted / PF Adjusted Cash, per role, not by label). If
`financials-snapshot` has already run this conversation and established an anchor EBITDA figure, note
whether the fx_risk tile's sensitivity is struck on the same basis; flag a mismatch if one exists, but this
is not a hard dependency — proceed without it if `financials-snapshot` hasn't run.

## Tone and rules

Apply `references/analyst-grade-discipline.md`: no freestanding editorial adjective unless it traces to a
specific tile field; an internal inconsistency in the tile is evidence against that tile, not a tiebreaker.

All output conforms to `references/language-standard.md` (American spelling, credit-desk register, no
em-dashes, no hype adjectives). Read it and apply it. Do not expose platform plumbing — no internal IDs
(project_id, tile identifiers), no raw section names (`exposure`, `Detail`, `Gaps`), no tool or parameter
names — in the body.

**The single most important caveat on this skill: geographic proxy vs. actual currency flow.** State
plainly whenever an EBITDA sensitivity or exposure estimate is a geographic-revenue-mix proxy rather than
an actual invoice-currency-based calculation. The absence of real invoice-currency disclosure is itself a
credit-quality signal, not a footnote to bury — it means the sensitivity figure is an approximation, and
the reader should know that before treating it as precise.

**Self-check the AI-speak tells before delivering:**
- Em-dashes are banned. Scan for the character and replace it with a comma, semicolon, or period.
- No verdict-then-hedge. State the finding, then the qualifying detail as its own sentence.
- Headings name content, never function ("The read," "Overview," "Assessment" are defects).
- No hype ("well-hedged," "robust natural offset"). Lead with the fact and the figure.
- Where the tile itself states no exposure or minimal exposure, render that plainly; do not manufacture
  exposure detail that isn't there to make the section feel substantive.

## Project Resolution

- If a project_id is known from earlier in this conversation, use it.
- Otherwise, `deal_list` to resolve by name. One match → use it. More than one → present as a table (Deal,
  Company, Sponsor, Status, Created; no internal IDs) and ask. Do not guess.
- If no deal is named, ask which deal first.

**Skip-if-known (strict):** if `analysis_get_status` or either `dashboard_get(fx_risk, ...)` call below is
already available from earlier in this conversation, do not re-call.

## STEP 0 — Analysis readiness

Call `analysis_get_status(project_id)` unless known. "Ready to view!" → proceed. Anything else → stop,
report the status, and suggest retrying once analysis completes or running `analysis_apply_start`.

## STEP 0.5 — Tool pre-load

`dashboard_get` is deferred; if not loaded this conversation, `tool_search` it first.

## STEP 1 — Retrieve (parallel batch, two calls in one turn)

1. `dashboard_get(project_id, tile="fx_risk", section="exposure")` — exposure summary, verdict, segment
   geographic concentration, debt denomination.
2. `dashboard_get(project_id, tile="fx_risk", section="detail")` — confirmed working (tested live):
   EBITDA sensitivity, mismatch analysis, hedging program, EM exposure, covenant FX impact, jurisdiction-
   specific repatriation gaps, projection FX assumptions, and the FX scorecard. Both calls are fully
   scoped; no full-tile fallback is needed.

If either call returns thin or unavailable content, say so plainly.

## STEP 2 — Render

**Header:** "FX Exposure — [Deal Name]"

**FX Exposure Summary:**
- **Verdict** (e.g. "Moderate FX exposure") and its rationale, rewritten to the language standard from the
  tile's own wording, not passed through verbatim if the tile's prose runs loose.
- **Revenue mix by geography** — render as a compact table (region → % revenue), not a description of a
  chart the reader can't see.
- **Segment geographic concentration** — each segment's revenue share and regional split, if the tile
  discloses a segment breakdown; skip this block entirely if it doesn't, rather than rendering an empty
  section.
- **Debt denomination** — which tranches, what currency, and the narrative on liability-side currency
  mismatch.

**FX Detail:**
- **EBITDA sensitivity** — the scenario table (e.g. a 10% or 5% adverse move in a named currency pair)
  with the stated $ and % impact, plus the methodology narrative. State the geographic-proxy-vs-actual
  caveat here explicitly, every time it applies — this is not optional detail. **Not every deal has this
  caveat as its limiting factor: some deals disclose no modeled sensitivity scenario at all, only observed
  historical FX impacts on past-period revenue/EBITDA (confirmed live). Where that's the case,
  state plainly that no modeled sensitivity exists and that the observed figures are historical
  calibration points, not a linear estimate of a hypothetical future move — don't force the
  geographic-proxy phrasing onto a gap that's actually a different, and often more severe, disclosure
  limitation.**
- **Mismatch analysis** — revenue vs. debt currency mismatch, transactional vs. translational exposure
  mechanism, cost currency.
- **Hedging program** — state plainly whether any hedging is disclosed; if none, say so directly, don't
  soften it into "limited hedging activity" or similar.
- **EM exposure** — emerging-market currency considerations (capital controls, managed floats), if flagged.
- **Covenant FX impact** — how an adverse FX move would affect covenant headroom, if quantified. Cross-
  reference `loan-coverage` / `test-covenants` figures if either has already run this conversation; note
  agreement or disagreement, never re-derive.
- **Jurisdiction-specific repatriation gaps** (e.g. China repatriation) — render if the tile flags material
  exposure to a jurisdiction with repatriation constraints.
- **Projection FX assumptions** — whether the lender/sponsor model discloses operating FX assumptions
  (currency-pair rates, constant-currency vs. forward-curve vs. spot-hold basis) for a business with
  material non-domestic revenue; where absent, say so, since a projected dollar-EBITDA path with no stated
  FX translation basis is a real modeling gap worth surfacing, not a minor omission.
- **FX scorecard** — all dimensions the tile discloses (typically exposure magnitude, P&L sensitivity,
  natural hedging, financial hedging) as a compact summary.

**Close with:** the `web_url` from the `dashboard_get` response, formatted as "🔗 [Open in Raven]({web_url})".

## Second read (mandatory, INTERNAL — a separate pass run AFTER the full render, never shown as a section)

Silent, every time.
1. **Verify every figure traces to the tile.** The verdict, the sensitivity scenarios, the revenue mix
   percentages — confirm each one is a rendered fact from Step 1's results, not something reconstructed or
   assumed between calls.
2. **Confirm the geographic-proxy caveat is present wherever a sensitivity figure appears**, not stated once
   at the top and then dropped from later mentions of the same figure.
3. **Confirm the Gaps block didn't leak into the render.** Exposure and Detail only; nothing from the
   tile's own Gaps section should appear here.
4. **Confirm the EBITDA basis is named correctly**, and that any cross-check against `financials-snapshot`'s
   anchor (if that skill ran this conversation) is reported, not silently skipped.
5. **Confirm no exposure was manufactured.** Where the tile states minimal or no FX exposure, the render
   should say so plainly and stop, not pad the section with speculative detail.
6. **Scan every dollar figure for citation-bracket garbling.** A number split by an inline source citation
   (e.g. "$6 [15, 34]00.0MM") must be reconstructed to its real value before delivery, never rendered as
   the source text presented it.

Findings weave into the render in place; nothing labeled "second read" reaches the output.

## Final review (mandatory, INTERNAL — the last step, over the whole assembled artifact)

Read the finished piece top to bottom once more and fix: **tone** (credit-desk register, no hedge-then-
verdict, no hype); **platform plumbing** (no internal IDs, no raw tile/section names anywhere in the
body); **headings** (clean, parallel, name content); and a **literal proofread** of every heading and
figure. Scan literally for the em-dash character and replace each with a comma, semicolon, or period.
Silent; its only evidence is a cleaner artifact.

## Rules

- Faithful stored-read. Never compute, re-score, or invent an exposure estimate, sensitivity figure, or
  verdict; render exactly what the tile returns.
- Always state plainly when a sensitivity estimate is a geographic proxy rather than an actual-currency-
  flow-based calculation — this is usually the tile's own single most important flagged gap.
- Do not render the tile's own Gaps block; it duplicates Diligence Gaps under a different workflow name.
- No platform plumbing in the body: no internal IDs, no raw tile or section names, no tool or parameter
  names.
- Where a company has minimal or no FX exposure, render that finding plainly rather than manufacturing
  exposure detail that isn't there.
- Name the EBITDA sensitivity's basis correctly per `references/conventions.md`; cross-check against
  `financials-snapshot`'s anchor if that skill has already run this conversation, but don't treat it as a
  hard dependency.
- **Watch for citation brackets embedded mid-number in the tile's raw text** (confirmed live: a
  dollar figure split by an inline source citation, e.g. "$6 [15, 34]00.0MM" instead of "$600.0MM").
  Reconstruct the actual figure from context rather than reproducing the garbled text verbatim; this is a
  tile-generation artifact, not a real data point to render as-is.
- Second read and final review are mandatory, separate, and silent; the evidence they ran is a changed
  artifact, never a narrated process block.

## Delivery

Render in chat by default. Only produce a Word document if asked; when generating one, use the docx skill
with a title block (deal name) and the same section structure as the chat render. Save to
`/mnt/user-data/outputs/` and `present_files`. After delivering, offer one natural next step: the exact
source page behind a specific figure, `loan-coverage` or `test-covenants` for the covenant-side detail, or
the Word export if the read was in chat.
