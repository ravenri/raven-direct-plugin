---
name: "financials-historical-income-statement-cash-flow"
description: "Analyzes a deal's full historical Income Statement (Revenue through Net Income: COGS, gross profit, SG&A, R&D, operating income, other income/expense, interest, taxes) and Cash Flow Statement (operating, investing, financing, line-item detail), sourced from vault search since no dashboard tile carries this level of GAAP line-item detail. Distinct from financials-snapshot, which owns EBITDA derivation, margin trend, and the LTM/current-period signal off the financial_analysis tile — this skill owns the full reported P&L walk to net income and the true cash flow statement, reusing financials-snapshot's anchor EBITDA/Revenue rather than re-deriving them. Carries carve-out handling (Net transfers to/from Parent in financing activities is a carve-out artifact, not real debt service, and disappears post-close) as first-class. Historical periods only. Use for \"income statement,\" \"P&L,\" \"cash flow statement,\" \"operating cash flow,\" \"net income,\" or a full line-item read on historical earnings and cash generation."
when_to_use: "Use for \"income statement,\" \"P&L,\" \"cash flow statement,\" \"operating cash flow,\" \"net income,\" or a full line-item read on historical earnings and cash generation. Do not use for the balance sheet or a summary trend (Financials Snapshot)."
---

# Financials — Historical Income Statement & Cash Flow

Analyzes the full historical Income Statement (Revenue down to Net Income) and Cash Flow Statement
(operating, investing, financing activities) for a deal — vault-search-based since no dashboard tile
carries this level of GAAP line-item detail. Historical periods only; forward projections are out of
scope throughout, in every section and every search.

## Scope and cross-skill sourcing

This skill owns the **full reported P&L walk** (Revenue, COGS, gross profit, SG&A, R&D, operating income,
other income/expense, interest expense, income tax, net income) and the **full Cash Flow Statement**
(operating, investing, and financing activities, line-item detail). It does not own EBITDA derivation,
margin trend narrative, or the LTM/current-period signal — those are `financials-snapshot`'s job, sourced
from the `financial_analysis` tile. It does not own the Balance Sheet — that is
`financials-historical-balance-sheet`'s job.

**Before deriving any ratio or note that needs an EBITDA figure** (e.g. an operating-cash-flow-to-EBITDA
conversion, or reconciling net income to EBITDA), check whether `financials-snapshot` has already run
earlier in this conversation and use its anchor EBITDA figure directly rather than re-deriving it through
an independent vault search. Only run an independent search for EBITDA if `financials-snapshot` has not
already established it this conversation, and say plainly that the figure was independently sourced rather
than pulled from an existing anchor. Revenue similarly reuses `financials-snapshot`'s anchor when
available.

**This skill's own reported P&L and cash flow figures are not themselves EBITDA-adjacent** — Net Income,
Operating Income, and the cash flow statement's line items are GAAP-reported facts in their own right, not
approximations of an EBITDA-basis figure. Do not silently convert between this skill's GAAP net income and
`financials-snapshot`'s adjusted EBITDA; where the two are compared (e.g. an EBITDA-to-net-income bridge),
name both figures and their bases explicitly.

## Tone and rules

Apply `references/analyst-grade-discipline.md`: no freestanding editorial adjective unless it traces to a
specific disclosed figure; where a figure disagrees with another surface, the disagreement is reported,
never silently resolved.

Apply `references/conventions.md` for any EBITDA or period-anchor figure this skill uses or cross-
references — the same role definitions and anchor-selection rules `financials-snapshot` and
`financials-historical-balance-sheet` already apply, so a figure computed here never uses a different basis
than the same figure would carry elsewhere in the suite.

All output conforms to `references/language-standard.md` (American spelling, credit-desk register, no
em-dashes, no hype adjectives). Read it and apply it. Do not expose platform plumbing (no raw tool names,
`research_search_analysis`, `report_type`, similarity scores, or search mechanics) in the body.

**Carve-out handling — first-class, not a generic note.** Where the financials are a carve-out, "Net
transfers to/from Parent" in the financing activities section of the cash flow statement is a carve-out
accounting artifact reflecting settlement of intercompany balances, not real third-party debt service — it
disappears entirely post-close and is replaced by actual interest and amortization on the new capital
structure. State this plainly in the Cash Flow section. Similarly, where SG&A includes disclosed parent
corporate-allocation costs, name the dollar amount and note these allocations may not represent a
standalone cost structure post-close (the sponsor's own standalone cost adjustment, if disclosed, is the
relevant forward-looking estimate — cross-reference it rather than re-deriving one).

**Self-check the AI-speak tells before delivering:**
- Em-dashes are banned. Scan for the character and replace it with a comma, semicolon, or period.
- No verdict-then-hedge. State the finding, then the qualifying detail as its own sentence.
- Headings name content, never function ("The read," "Overview," "Assessment" are defects).
- Section commentary stays at 2 sentences and never restates a figure already visible in the table above
  it — commentary is for causation, quality, and credit implications, not a second copy of the numbers.

## Project Resolution

- If a project_id is known from earlier in this conversation, use it.
- Otherwise, `deal_list` to resolve by name. One match → use it. More than one → present as a table (Deal,
  Company, Sponsor, Status, Created; no internal IDs) and ask. Do not guess.
- If no deal is named, ask which deal first.

Capture the deal's display name, sponsor, and reporting currency for the header.

## STEP 0 — Analysis readiness

Call `analysis_get_status(project_id)` unless known. "Ready to view!" → proceed. Anything else → stop,
report the status, and note that running this now would flag everything as missing when the vault simply
hasn't finished building; suggest retrying once analysis completes or running `analysis_apply_start`.

## STEP 0.5 — Tool pre-load

`research_search_analysis` is deferred; if not loaded this conversation, `tool_search` it first.

## STEP 1 — Retrieve (parallel batch, three searches in one turn)

`report_type="diligence_summary"` for all three:

1. `research_search_analysis(project_id, "revenue cost of goods sold gross profit SG&A R&D operating income net income statement of operations", top_k=7)` — the full reported P&L.
2. `research_search_analysis(project_id, "cash flow from operations investing financing activities net income depreciation amortization working capital changes capex", top_k=7)` — the full Cash Flow Statement.
3. `research_search_analysis(project_id, "related party corporate allocations standalone costs net transfers to parent intercompany carve-out", top_k=7)` — carve-out and related-party context relevant to both statements.

Discard results with similarity below 0.02. Historical periods only — exclude forward projections from
every search's results.

## STEP 2 — Render

**Header:** deal name, sponsor, currency, PF basis, carve-out context note if applicable.

**Summary Income Statement table** (all disclosed historical periods, Revenue through Net Income) and
**Summary Cash Flow Statement table** (all disclosed historical periods, Operating/Investing/Financing).

**Revenue growth line, directly under the Income Statement table.** Where three or more full fiscal years
are disclosed, render a Revenue CAGR across the full historical range (matching `financials-snapshot`'s
own CAGR convention). Where only one or two full fiscal years are disclosed, a CAGR is not meaningful,
render simple year-over-year growth for each available year instead, and say so plainly rather than
computing a CAGR across too short a span. Never present a two-point CAGR as if it carried the same
statistical weight as a multi-year one.

**One section each for Revenue & Gross Profit, Operating Expenses & Operating Income, Net Income & Other
Items, and Cash Flow (Operating, Investing, Financing combined):**
- One-line trend summary.
- Exactly 2 sentences of analytical commentary — causation, quality, and credit implications only, never
  restating a figure already visible in the table or trend line above it.
- At most one ⚠️ risk callout, one sentence.
- At most one ✅ strength callout, one sentence.

**Derived ratios** (gross margin, operating margin, net margin, effective tax rate, operating cash flow
conversion of net income, capex as % of revenue), each labeled "(derived)" or "(calc.)" where the vault does
not disclose it directly. Any ratio using an EBITDA figure states which path supplied it — reused from
`financials-snapshot`'s anchor, or independently sourced this run — per the cross-skill sourcing rule
above. Never present a derived figure as disclosed, and never derive one the underlying materials
genuinely lack; say "not derivable" instead.

**Data gaps table** — one line per missing item, status only, no filled-in guesses.

**Source citations** at the bottom.

## Second read (mandatory, INTERNAL — a separate pass run AFTER the full render, never shown as a section)

Silent, every time.
1. **Confirm every figure traces to a retrieved chunk.** A number in a table or commentary that isn't
   backed by Step 1's results is fabricated; remove it or re-search.
2. **Confirm the cross-skill sourcing rule actually ran.** Any figure using EBITDA should show which path
   supplied it; a figure that silently used a fresh, unattributed EBITDA number is a defect to fix before
   delivering, not after.
3. **Confirm the carve-out disciplines fired where applicable.** If the cash flow statement shows Net
   transfers to/from Parent, the Cash Flow section must state plainly that this is a carve-out artifact
   that disappears post-close; if SG&A carries a disclosed corporate allocation, it must be named with its
   dollar amount.
4. **Confirm every commentary block is exactly 2 sentences and doesn't restate a table figure.** This is
   the most common drift point on a strict-format skill; check it explicitly rather than assuming the
   draft already complied.
5. **Confirm data gaps are reported, not filled.** A blank or "not disclosed" item in Step 1's results
   should appear in the Data Gaps table, not be quietly estimated into a number.
6. **Confirm GAAP net income and any EBITDA figure are never silently conflated.** Every bridge or
   comparison between the two names both figures and their bases explicitly.

Findings weave into the render in place; nothing labeled "second read" reaches the output.

## Final review (mandatory, INTERNAL — the last step, over the whole assembled artifact)

Read the finished piece top to bottom once more and fix: **tone** (credit-desk register, no hedge-then-
verdict, no X-not-Y); **platform plumbing** (no raw tool, field, or parameter names anywhere in the body);
**headings** (clean, parallel, name content); and a **literal proofread** of every heading and figure. Scan
literally for the em-dash character and replace each with a comma, semicolon, or period. Silent; its only
evidence is a cleaner artifact.

## Rules

- Historical periods only; exclude forward projections throughout, in every section and every search.
- Read stored content faithfully; never invent a figure or a citation.
- Commentary is exactly 2 sentences per section and never restates a figure already visible in the table;
  focus on causation, quality, and credit implications.
- Derived ratios are always labeled "(derived)" or "(calc.)"; never present one as disclosed, and never
  derive one the materials genuinely lack — say so instead.
- Render Revenue CAGR only across three or more full fiscal years; with one or two years disclosed, render
  simple year-over-year growth instead and say so, never a two-point CAGR presented as equivalent.
- Net transfers to/from Parent in the cash flow statement is a carve-out artifact, not real debt service;
  state this plainly and note it disappears post-close. Disclosed corporate allocations inside SG&A are
  named with their dollar amount.
- Before using any EBITDA figure, check for and reuse `financials-snapshot`'s anchor if that skill has
  already run this conversation; state which path supplied the figure either way. Never silently conflate
  GAAP net income with an EBITDA figure.
- Flag data gaps plainly rather than filling them.
- No platform plumbing in the body: no raw tool, field, or parameter names, no similarity scores.
- Second read and final review are mandatory, separate, and silent; the evidence they ran is a changed
  artifact, never a narrated process block.

## Delivery

Render in chat by default. Only produce a Word document if asked; when generating one, use the docx skill
with a title block (deal name, sponsor, currency, PF basis) and the same section structure as the chat
render. Save to `/mnt/user-data/outputs/` and `present_files`. After delivering, offer one natural next
step: the `financials-snapshot` read if EBITDA/margin trend hasn't been pulled yet, the
`financials-historical-balance-sheet` read for balance-sheet strength, or a deeper look at a specific
flagged risk or gap.
