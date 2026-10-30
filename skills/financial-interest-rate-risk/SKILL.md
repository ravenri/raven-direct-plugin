---
name: "financial-interest-rate-risk"
description: "Renders a deal's interest rate exposure from Raven's dedicated interest_rate_risk tile - fixed/floating split, benchmark rates, margin ratchets, hedging coverage, and rate sensitivity. Faithful stored-read: verdict and rationale, fixed/floating split (overall and per-tranche), a rate sensitivity table (base case, +100/+200/+300bps, additional interest $ and % of EBITDA - usually the single most useful piece, never truncated), benchmark rates, PIK/stepup/ratchet mechanics, base case assumptions, covenant IR impact, refinancing rate risk, hedging mitigation, margin ratchets table, and an IR scorecard. Distinguishes \"redacted in source\" from \"not disclosed at all.\" Use for \"interest rate risk,\" \"rate sensitivity,\" \"floating rate exposure,\" \"margin ratchets,\" \"hedging coverage,\" or how exposed a deal is to rising rates."
when_to_use: "Use for \"interest rate risk,\" \"rate sensitivity,\" \"floating rate exposure,\" \"margin ratchets,\" \"hedging coverage,\" or how exposed a deal is to rising rates. Do not use for FX exposure or lender returns."
---

# Financial - Interest Rate Risk

Renders the deal's interest rate exposure, sourced from Raven's dedicated `interest_rate_risk` tile. A
faithful stored-read: exposure verdict, fixed/floating split, rate sensitivity, benchmark rates, ratchet
mechanics, hedging, and a scorecard.

**This is a stored-read, not an analysis pass.** The tile already holds the sensitivity scenarios, the
ratchet mechanics, and the narrative for each. This skill renders that faithfully, in house voice, and
never computes, re-scores, or invents a sensitivity figure, benchmark rate, or verdict.

## Scope

Interest rate exposure only. This tile's own `Gaps` block is out of scope here — `interest_rate_risk` is
already a confirmed extension source in the Diligence Gaps skill, and rendering its gap list again under
this workflow's name would double-count the same content. Covenant testing itself belongs to
`test-covenants`; this skill renders the tile's own statement of covenant IR impact as a point-in-time
fact, cross-referencing `loan-coverage` / `test-covenants` figures if those have already run this
conversation — the headroom figures (e.g. a leverage multiple against its covenant max) should match
exactly if both pulled from consistent underlying data; a mismatch is worth flagging, not smoothing over.

**EBITDA sensitivity basis.** Apply `references/conventions.md` so the rate-sensitivity table's %-of-EBITDA
column is named on the correct basis (Reported / Adjusted / PF Adjusted / PF Adjusted Cash, per role, not
by label). If `financials-snapshot` has already run this conversation and established an anchor EBITDA
figure, note whether this tile's sensitivity is struck on the same basis; flag a mismatch if one exists,
but this is not a hard dependency — proceed without it if `financials-snapshot` hasn't run.

## Tone and rules

Apply `references/analyst-grade-discipline.md`: no freestanding editorial adjective unless it traces to a
specific tile field; an internal inconsistency in the tile is evidence against that tile, not a tiebreaker.

All output conforms to `references/language-standard.md` (American spelling, credit-desk register, no
em-dashes, no hype adjectives). Read it and apply it. Do not expose platform plumbing — no internal IDs
(project_id, tile identifiers), no raw section names (`exposure`, `hedging`, `Rate Detail`, `Gaps`), no tool
or parameter names — in the body.

**"Redacted" and "not disclosed" are different findings — never collapse them.** Where the tile's own
language distinguishes a pricing grid that exists but has specific values blacked out from a mechanism
that simply isn't described anywhere, preserve that distinction in the render. A redacted grid says
something different about the document set than a genuinely undisclosed one, and flattening both into
"not disclosed" loses that signal.

**The Rate Sensitivity table is usually the single most useful content in this whole skill.** Never omit
or truncate it. Lead with the %-of-EBITDA column in any summary framing, since it's the fastest way to
communicate materiality — a reader can judge $18MM in isolation only by knowing what it is relative to.

**Procyclical mechanics are worth naming plainly, not just listing.** Where a margin ratchet raises pricing
as leverage rises (the wrong direction for a borrower entering stress) or a stepdown only rewards
deleveraging without a symmetric protection on the way up, state that asymmetry as a sentence, not just a
mechanics table entry.

**Self-check the AI-speak tells before delivering:**
- Em-dashes are banned. Scan for the character and replace it with a comma, semicolon, or period.
- No verdict-then-hedge. State the finding, then the qualifying detail as its own sentence.
- Headings name content, never function ("The read," "Overview," "Assessment" are defects).
- No hype ("well-hedged," "manageable exposure"). Lead with the fact and the figure.
- Where the tile itself states minimal or no rate exposure, render that plainly; do not manufacture
  exposure detail that isn't there.

## Project Resolution

- If a project_id is known from earlier in this conversation, use it.
- Otherwise, `deal_list` to resolve by name. One match → use it. More than one → present as a table (Deal,
  Company, Sponsor, Status, Created; no internal IDs) and ask. Do not guess.
- If no deal is named, ask which deal first.

**Skip-if-known (strict):** if `analysis_get_status` or any of the `dashboard_get(interest_rate_risk, ...)`
calls below is already available from earlier in this conversation, do not re-call.

## STEP 0 — Analysis readiness

Call `analysis_get_status(project_id)` unless known. "Ready to view!" → proceed. Anything else → stop,
report the status, and suggest retrying once analysis completes or running `analysis_apply_start`.

## STEP 0.5 — Tool pre-load

`dashboard_get` is deferred; if not loaded this conversation, `tool_search` it first.

## STEP 1 — Retrieve (parallel batch, two calls in one turn)

1. `dashboard_get(project_id, tile="interest_rate_risk", section="exposure")` — fixed/floating split,
   verdict, rate sensitivity table. Confirmed working live.
2. `dashboard_get(project_id, tile="interest_rate_risk", section="hedging")` — hedging mitigation/coverage,
   margin ratchets table, IR scorecard. Confirmed working live.

This tile also has a "Rate Detail" content block (benchmark rates, PIK/stepup/ratchet mechanics, base case
assumptions, covenant IR impact, refinancing rate risk) with no confirmed dedicated section id.
**Confirmed live: `section="detail"` does NOT scope to Rate Detail — it silently returns the
entire tile** (Exposure, Rate Detail, Hedging, and the Gaps block), matching `dashboard_get`'s own
documented behavior that an unrecognized section returns the whole dashboard rather than an error. Do not
re-test this; go straight to the full-tile fallback for Rate Detail: call
`dashboard_get(project_id, tile="interest_rate_risk")` with no section, and extract only the Rate Detail
content. Discard the Exposure and Hedging content already captured in calls 1 and 2 (don't render it
twice), discard the Gaps block entirely (out of scope), and discard any trailing pipeline-diagnostic
blocks that may appear in a full-tile response (e.g. sections named "Run," "Numeric Validation," "Prose
Scale," or "Prose") — these are internal QA metadata, never reader-facing content.

## STEP 2 — Render

**Header:** "Interest Rate Risk — [Deal Name]"

**Interest Rate Exposure Summary:**
- **Verdict** (e.g. "High rate exposure") and its rationale, rewritten to the language standard, not passed
  through verbatim if the tile's own prose runs loose.
- **Fixed/Floating split** — render as a compact table (Fixed / Floating / Unspecified, % of debt), not a
  description of a chart the reader can't see.
- **Per-tranche detail** — breakdown by tranche (e.g. Term Loan B, Revolver), and Hedged Floating / Net
  Unhedged Floating figures if disclosed.
- **Rate sensitivity table** — every scenario row (base case, +100bps, +200bps, +300bps, or whatever the
  tile discloses) with additional interest $ and % of EBITDA. Render in full; this is the section's most
  load-bearing content.

**Rate Detail** (from the confirmed `detail` section or the full-tile fallback):
- **Benchmark rates** — reference rate(s) (SOFR, EURIBOR, SONIA, CORRA), floor level, margin over
  benchmark. State plainly if specific pricing-grid values are redacted rather than genuinely undisclosed.
- **PIK / stepups / ratchets** — render all four sub-items where present (PIK applicability, margin
  stepdowns, margin ratchet mechanics, MFN stepup). Name any procyclical asymmetry as a sentence, not just
  a table row.
- **Base case assumptions** — what the model assumes for rates, and any gap note on redacted or unspecified
  values.
- **Covenant IR impact** — how a rate increase affects covenant headroom, if quantified. Cross-reference
  `loan-coverage` / `test-covenants` figures if either has already run this conversation; the same headroom
  figures should match if both pulled from consistent data — report agreement or flag a mismatch, never
  re-derive.
- **Refinancing rate risk** — maturity dates and any stated or unstated refinancing rate assumptions.

**Hedging:**
- **Hedging mitigation** — state plainly whether hedges are disclosed; if none, say so directly (e.g. "no
  interest rate hedges disclosed; the entire floating-rate debt profile is unhedged"), never softened.
- **Margin ratchets table** — every mechanism, trigger, direction, and magnitude row.
- **IR scorecard** — all dimensions the tile discloses (typically floating rate exposure, rate sensitivity,
  hedging coverage, margin ratchet risk) as a compact summary.

**Close with:** the `web_url` from the `dashboard_get` response, formatted as "🔗 [Open in Raven]({web_url})".

## Second read (mandatory, INTERNAL — a separate pass run AFTER the full render, never shown as a section)

Silent, every time.
1. **Verify every figure traces to the tile.** The verdict, the sensitivity scenarios, the benchmark rate
   and margin figures — confirm each is a rendered fact from Step 1's results, not reconstructed or
   assumed between calls.
2. **Confirm the Rate Sensitivity table rendered in full**, every scenario row, with no truncation.
3. **Confirm "redacted" and "not disclosed" stayed distinct** wherever the tile's own language distinguishes
   them; a render that collapsed the two into one phrasing is a defect to fix now.
4. **Confirm the Gaps block didn't leak into the render.** Exposure, Hedging, and Rate Detail only.
5. **Confirm the EBITDA basis is named correctly**, and any cross-check against `financials-snapshot`'s
   anchor (if that skill ran this conversation) is reported, not silently skipped.
6. **Confirm covenant IR impact figures were checked against `loan-coverage` / `test-covenants`** if either
   ran this conversation, and that any mismatch was reported rather than smoothed over.
7. **Confirm no exposure was manufactured.** Where the tile states minimal or no rate exposure, the render
   should say so plainly and stop.
8. **Scan every figure and word for citation-bracket garbling.** A word or number split by an inline
   source citation (e.g. "an[3,5]d") must be reconstructed before delivery, never rendered as the source
   text presented it. If the full-tile fallback was used, confirm no pipeline-diagnostic block (Run,
   Numeric Validation, Prose Scale, Prose) leaked into the render.

Findings weave into the render in place; nothing labeled "second read" reaches the output.

## Final review (mandatory, INTERNAL — the last step, over the whole assembled artifact)

Read the finished piece top to bottom once more and fix: **tone** (credit-desk register, no hedge-then-
verdict, no hype); **platform plumbing** (no internal IDs, no raw tile/section names anywhere in the
body); **headings** (clean, parallel, name content); and a **literal proofread** of every heading and
figure. Scan literally for the em-dash character and replace each with a comma, semicolon, or period.
Silent; its only evidence is a cleaner artifact.

## Rules

- Faithful stored-read. Never compute, re-score, or invent a sensitivity figure, benchmark rate, or
  verdict; render exactly what the tile returns.
- Distinguish "redacted in the source document" from "not disclosed at all" wherever the tile's own
  language makes that distinction; never collapse the two.
- Never omit or truncate the Rate Sensitivity table; lead with the %-of-EBITDA column, not the raw dollar
  figures alone.
- Name any procyclical margin-ratchet or asymmetric stepdown/ratchet mechanic as a plain sentence, not just
  a mechanics table row.
- Do not render the tile's own Gaps block; it duplicates Diligence Gaps under a different workflow name.
- When the full-tile fallback is used for Rate Detail, also discard any pipeline-diagnostic blocks that
  may appear (e.g. "Run," "Numeric Validation," "Prose Scale," "Prose") — these are internal QA metadata
  from the tile's own generation process, never reader-facing content.
- No platform plumbing in the body: no internal IDs, no raw tile or section names, no tool or parameter
  names.
- Where a company has minimal or no rate exposure, render that finding plainly rather than manufacturing
  exposure detail that isn't there.
- Name the EBITDA sensitivity's basis correctly per `references/conventions.md`; cross-check against
  `financials-snapshot`'s anchor if that skill has already run this conversation, but don't treat it as a
  hard dependency. Cross-check covenant IR impact figures against `loan-coverage` / `test-covenants` on the
  same terms.
- **Watch for citation brackets embedded mid-word in the tile's raw text** (confirmed live,
  repeatedly: "an[3,5]d," "wh[3,5]ile," "exe[7,14]cuted"). Reconstruct the actual word or figure from
  context rather than reproducing the garbled text verbatim; this is a tile-generation artifact affecting
  more than one dashboard tile, not a real data point to render as-is.
- Second read and final review are mandatory, separate, and silent; the evidence they ran is a changed
  artifact, never a narrated process block.

## Delivery

Render in chat by default. Only produce a Word document if asked; when generating one, use the docx skill
with a title block (deal name) and the same section structure as the chat render. Save to
`/mnt/user-data/outputs/` and `present_files`. After delivering, offer one natural next step: the exact
source page behind a specific figure, `loan-coverage` or `test-covenants` for the covenant-side detail, or
the Word export if the read was in chat.
