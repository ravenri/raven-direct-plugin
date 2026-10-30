---
name: "financial-projections-base-case"
description: "Gets an analyst up the curve fast on a sponsor's base case model - leads with a plain-language Model Orientation (model type, what drives deleveraging, anchor EBITDA basis, biggest gap) before any table, then builds starting at Revenue down through Gross Margin (as much detail as disclosed, never starting at EBITDA), key assumptions (growth, margins, capex %, NWC %, tax rate, interest rate, labeled derived if not stated), the EBITDA ladder, credit statistics per period, the levered FCF walk, and the debt paydown schedule. States the cash sweep mechanic explicitly - a stated contractual percentage is never conflated with a rate merely implied by the paydown numbers. Reuses the anchor from financial-proforma-cap-table-ebitda, faithfully reproducing the sponsor's own model, not a house sensitivity lens. Use for \"base case projections,\" \"key assumptions,\" \"credit statistics,\" \"cash sweep,\" \"debt paydown schedule,\" \"levered FCF,\" or how the deal delevers."
when_to_use: "Use for \"base case projections,\" \"key assumptions,\" \"credit statistics,\" \"cash sweep,\" \"debt paydown schedule,\" \"levered FCF,\" or how the deal delevers. Do not use for downside or sensitivity cases, or for historical results."
---

# Financial - Projections Base Case

**Think of this as getting an analyst up the curve on the sponsor's (or borrower's) own model, fast.**
Someone opening this model for the first time needs to understand how it *works* before the individual
numbers mean anything: what kind of model this is, what mechanic actually drives deleveraging, which
EBITDA basis everything strikes on, and where the real gaps are, before they start relying on any single
figure in it. This skill renders the numbers faithfully, but it's built around that orientation goal, not
around the tables alone.

This is the forward extension of `financial-proforma-cap-table-ebitda`, which stays deliberately
point-in-time; this skill picks up exactly where that one stops.

**This must faithfully reproduce the sponsor's own model, never a house sensitivity lens standing in for
it.** The sponsor's model encodes real choices, its own cash sweep percentage and step-downs, its own
M&A/cash-deployment assumptions, its own coverage definitions, that a generic house convention can deviate
from. Presenting a house-generated projection as if it were the deal's own forward view would misstate the
sponsor's thesis. If what's available is a house-generated model rather than the sponsor's own, say so
plainly before rendering anything from it.

## Scope and cross-skill sourcing

Owns: model assumptions, the EBITDA build across projection years, credit statistics per period, the
levered FCF walk, and the debt paydown schedule. Does not own the point-in-time anchor, opening cap table,
or debt terms outline — that's `financial-proforma-cap-table-ebitda`. Does not own historical capex
analysis — that's `financial-capex-analysis`. Does not own covenant-by-covenant compliance testing against
the actual credit agreement — that's `test-covenants`; this skill renders the model's own credit statistics
as the model presents them, not a covenant compliance verdict.

**Reuse the anchor, don't re-derive it.** If `financial-proforma-cap-table-ebitda` has already run this
conversation, use its resolved anchor EBITDA role, period, and opening capital structure directly rather
than re-selecting them. If it hasn't run, resolve the anchor using the same `references/conventions.md`
role definitions (Reported → Adjusted → PF Adjusted → PF Adjusted Cash, in that priority) before rendering
anything projection-related, since every projected multiple and coverage ratio needs to strike on the same
basis the opening structure does.

## Tone and rules

Apply `references/analyst-grade-discipline.md`: no freestanding editorial adjective unless it traces to a
specific disclosed figure; an internal inconsistency in the model is evidence against trusting it blindly,
not a tiebreaker.

All output conforms to `references/language-standard.md` (American spelling, credit-desk register, no
em-dashes, no hype adjectives). Read it and apply it. Do not expose platform plumbing (no raw tool names,
`research_search_analysis`, similarity scores, or search mechanics) in the body.

**The cash sweep mechanic is never implicit.** State the sweep percentage explicitly and prominently, in
its own line, every time a debt schedule or credit statistics table is rendered, whether it's 100%, 50%,
some other stated rate, or a stepped-down rate tied to a leverage threshold (e.g. "50% sweep at leverage
above 3.0x, stepping to 25% below 3.0x, 0% below 2.0x"). Never let a reader infer the sweep rate from the
shape of the debt paydown numbers; say what it is.

**Every multi-period table renders periods along the top as columns, metrics as rows.** No exceptions,
matching the standing convention across the other financials skills.

**Self-check the AI-speak tells before delivering:**
- Em-dashes are banned. Scan for the character and replace it with a comma, semicolon, or period.
- No verdict-then-hedge. State the finding, then the qualifying detail as its own sentence.
- Headings name content, never function ("The read," "Overview," "Assessment" are defects).
- No hype ("robust deleveraging," "healthy coverage cushion"). Lead with the fact and the figure.
- Where the model doesn't disclose a figure or mechanic, say so plainly rather than filling the gap with
  a market-convention assumption.

## Project Resolution

- If a project_id is known from earlier in this conversation, use it.
- Otherwise, `deal_list` to resolve by name. One match → use it. More than one → present as a table (Deal,
  Company, Sponsor, Status, Created; no internal IDs) and ask. Do not guess.
- If no deal is named, ask which deal first.

## STEP 0 — Analysis readiness

Call `analysis_get_status(project_id)` unless known. "Ready to view!" → proceed. Anything else → stop,
report the status, and suggest retrying once analysis completes or running `analysis_apply_start`.

## STEP 0.5 — Tool pre-load

`research_search_analysis` is deferred; if not loaded this conversation, `tool_search` it first.

## STEP 1 — Retrieve (parallel batch, six searches in one turn)

`report_type="diligence_summary"` for all six; content-based queries only, never a hardcoded question ID:

1. `research_search_analysis(project_id, "model assumptions revenue margin capex NWC tax rate interest rate", top_k=7)` — key assumptions driving the projection.
2. `research_search_analysis(project_id, "sponsor model EBITDA build projected reported adjusted pro forma", top_k=7)` — the EBITDA ladder across projection years.
3. `research_search_analysis(project_id, "levered free cash flow build capex working capital taxes interest one-time costs", top_k=7)` — the levered FCF walk.
4. `research_search_analysis(project_id, "credit statistics leverage coverage ratio per period projected", top_k=7)` — credit statistics by year.
5. `research_search_analysis(project_id, "excess cash flow sweep percentage step-down leverage threshold mandatory prepayment", top_k=7)` — the sweep mechanic specifically; never skip this search even if the credit statistics search already surfaced sweep-adjacent content.
6. `research_search_analysis(project_id, "cash bridge debt schedule balance by period term loan revolver paydown", top_k=7)` — the per-tranche debt schedule.

Discard results with similarity below 0.02. If `financial-proforma-cap-table-ebitda` already established the anchor this conversation, skip re-resolving it but still run all six searches above, since none of them duplicate that skill's own retrieval.

## STEP 2 — Render

**Header:** deal name, sponsor, reporting currency, model source (sponsor's own model vs. a house-generated
model, stated explicitly — this determines how much weight the whole render can bear).

**Model Orientation — lead with this, before any table.** In a few plain sentences, get the reader oriented
on how this specific model works, not just what it contains:
- **What kind of model is this?** Single base case, or multiple scenarios/cases (per the model's own
  inventory/archetype)? If multiple cases exist, state plainly that this render covers the base case only.
- **What actually drives the deleveraging path?** Name the real mechanic in one or two sentences — e.g.
  "debt declines because all available levered free cash flow is applied to paydown after a $10MM minimum
  cash retention; no other mechanic (asset sales, refinancing, additional equity) is modeled."
- **What EBITDA basis does everything strike on?** Name the anchor role plainly (reusing
  `financial-proforma-cap-table-ebitda`'s resolved anchor if it ran this conversation) so the reader isn't
  left to infer it from a table header three sections later.
- **What's the single biggest gap in this model that a reader should know before trusting any number in
  it?** Usually this is the sweep mechanic or the rate/pricing assumption; name whichever gap actually
  matters most for this specific deal, don't default to a generic "some things aren't disclosed" line.

This section is short, prose, and comes before every table below — the goal is that someone could stop
reading after this paragraph and still know how to think about the model, even without the numbers.

**Key Assumptions.** Revenue growth, gross margin, EBITDA margin, capex (% of sales), change in NWC (% of
sales), tax rate, interest rate. For any assumption not stated directly as a percentage, derive it from the
disclosed dollar figures and label it "(derived)" — never present a derived assumption as if the model
stated it outright. Render any accompanying narrative explanation the model or supporting materials give
for each assumption; where none exists, say so.

**Revenue Through EBITDA Build** (periods as columns, anchor period through the final projection year).
**Always start at Revenue, never at EBITDA** — build down in this order, with as much line-item detail as
the model actually discloses at the projected level:
1. **Revenue**, and its stated YoY growth rate.
2. **COGS** and **Gross Profit**, with **Gross Margin %**, if the model discloses them at the projected
   level. Many sponsor models project Revenue and EBITDA directly without a separate projected COGS/Gross
   Profit line — where that's the case here, say so explicitly ("COGS and Gross Profit are not projected
   as separate lines in this model; only Revenue and EBITDA are directly forecast") rather than silently
   skipping from Revenue straight to EBITDA with no explanation for the gap.
3. **The full EBITDA ladder**, from Reported EBITDA (or the earliest disclosed layer) through the anchor
   role, using the same role names and priority order as `references/conventions.md` and
   `financial-proforma-cap-table-ebitda`. Name every add-back line the model itself uses; don't collapse or
   relabel them.

Run the arithmetic check at each step (does the stated subtotal actually equal the sum of the lines above
it, within rounding) and flag, never force, a period that doesn't reconcile — a model's own internal build
not tying out in a given year is a real finding, not something to paper over. This applies to the Revenue-
to-Gross-Profit step too, not only the EBITDA ladder, wherever that detail is disclosed.

**Credit Statistics Per Period** (periods as columns): gross leverage (Total Debt / anchor EBITDA), net
leverage (Net Debt / anchor EBITDA), EBITDA-to-net-interest coverage, (EBITDA − Capex)-to-net-interest
coverage, levered FCF available to repay debt. State the basis of each ratio explicitly (which EBITDA
layer, gross vs. net) so a reader never has to infer it.

**The Sweep & Paydown Mechanic — its own clearly labeled block, never folded silently into the debt
schedule.** State the cash sweep percentage explicitly, and any step-down mechanism (the triggering metric,
the threshold, and the resulting rate at each level). State what happens to swept cash operationally (paid
against which tranche(s), in what order of priority) if the model discloses it. If the model's debt paydown
figures imply a sweep rate that isn't explicitly stated anywhere, say that the rate is implied by the
schedule rather than disclosed as a stated policy, and show the derivation.

**Levered Free Cash Flow Build** (periods as columns): the walk from the anchor EBITDA role down to
levered FCF — capex, change in NWC, cash taxes, cash interest, one-time or transaction costs, any other
model-specific deduction or addition (an excess-cash funding line, a value-creation-plan cost) — each line
named as the model labels it. Run the arithmetic check the same way as the EBITDA build.

**Cash Bridge & Debt Schedule** (periods as columns): cash balance, and the balance of every disclosed
tranche, by period, with total debt and net debt as subtotals. This should tie directly to the credit
statistics above; if it doesn't, flag the inconsistency rather than silently reconciling one against the
other.

**Data gaps table** — one line per missing item (an assumption not stated, a sweep mechanism not disclosed,
a tranche missing from the schedule in a given year), status only, no filled-in guesses.

**Source citations** at the bottom.

## Second read (mandatory, INTERNAL — a separate pass run AFTER the full render, never shown as a section)

Silent, every time.
1. **Confirm every figure traces to a retrieved chunk.** A number in a table or commentary not backed by
   Step 1's results is fabricated; remove it or re-search.
2. **Re-run the arithmetic checks** on both the EBITDA build and the levered FCF walk, every period. Flag,
   never force, a period that doesn't reconcile.
3. **Confirm the sweep mechanic is stated explicitly and prominently**, not buried in the debt schedule or
   left for the reader to infer from the paydown shape. If it's implied rather than disclosed, confirm the
   render says so and shows the derivation.
4. **Confirm the anchor basis is consistent with `financial-proforma-cap-table-ebitda`'s** if that skill
   ran this conversation; a projection struck on a different EBITDA role or period than the opening
   structure is a real inconsistency to flag, not smooth over.
5. **Confirm this is presented as the sponsor's own model, or explicitly flagged as a house-generated
   substitute**, never left ambiguous which one is being rendered.
6. **Confirm every multi-period table has periods as columns, metrics as rows.**
7. **Confirm data gaps are reported, not filled.**
8. **Confirm the Model Orientation section actually orients, rather than restating a table in prose.** It
   should be readable and useful on its own, before any numbers, and should name the single most important
   gap for this specific deal rather than a generic disclaimer.
9. **Confirm the build starts at Revenue, not at EBITDA.** If COGS or Gross Profit aren't projected as
   separate lines in this model, confirm the render says so explicitly rather than silently jumping from
   Revenue to EBITDA with no acknowledgment of the missing detail in between.

Findings weave into the render in place; nothing labeled "second read" reaches the output.

## Final review (mandatory, INTERNAL — the last step, over the whole assembled artifact)

Read the finished piece top to bottom once more and fix: **tone** (credit-desk register, no hedge-then-
verdict, no hype); **platform plumbing** (no raw tool or parameter names anywhere in the body);
**headings** (clean, parallel, name content); and a **literal proofread** of every heading and figure. Scan
literally for the em-dash character and replace each with a comma, semicolon, or period. Silent; its only
evidence is a cleaner artifact.

## Rules

- Faithfully reproduce the sponsor's own model; never substitute a house-generated projection without
  saying so explicitly.
- Lead every render with a Model Orientation paragraph — what kind of model, what actually drives
  deleveraging, the anchor EBITDA basis, and the single biggest gap — before any table. This is the
  get-up-the-curve purpose of the skill, not an optional preamble.
- The cash sweep mechanic always gets its own labeled block, stated explicitly (percentage, any step-down
  thresholds); never left implicit or inferable only from the debt schedule's shape.
- Every multi-period table renders periods as columns, metrics as rows, with no exceptions.
- The build always starts at Revenue and walks down through Gross Margin before the EBITDA ladder, with
  as much line-item detail as the model discloses; never start directly at EBITDA. If COGS/Gross Profit
  aren't projected as separate lines, say so explicitly rather than skipping silently.
- Arithmetic checks are mandatory on the EBITDA build and the levered FCF walk, every period; flag, never
  force, a period that doesn't reconcile.
- Reuse `financial-proforma-cap-table-ebitda`'s anchor role and period if that skill has already run this
  conversation; never strike a projected ratio on a different basis than the opening structure without
  flagging the inconsistency.
- Never hardcode a question ID for any search in this skill; search by content, since prompt IDs get
  renumbered.
- No platform plumbing in the body: no raw tool or parameter names, no similarity scores.
- Flag data gaps plainly rather than filling them.
- Second read and final review are mandatory, separate, and silent; the evidence they ran is a changed
  artifact, never a narrated process block.

## Delivery

Render in chat by default. Only produce a Word document if asked; when generating one, use the docx skill
with a title block (deal name, sponsor, currency) and the same section structure as the chat render. Save
to `/mnt/user-data/outputs/` and `present_files`. After delivering, offer one natural next step: the
`financial-proforma-cap-table-ebitda` read if the opening structure hasn't been pulled yet, `test-covenants`
for actual compliance testing against the credit agreement, or the Word export if the read was in chat.
