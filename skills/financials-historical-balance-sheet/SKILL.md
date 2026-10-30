---
name: "financials-historical-balance-sheet"
description: "Analyzes a deal's historical balance sheet, sourced from vault search since no dashboard tile exists for it (current assets, PP&E, goodwill/intangibles, capital structure and equity, accounts payable, accrued liabilities, pension/OPEB, leases, non-current liabilities). Computes balance-sheet ratios (current ratio, quick ratio, asset turnover, tangible net worth, EV/net PP&E), pulling Revenue/EBITDA from financials-snapshot's anchor figures when available rather than re-deriving them. Carries carve-out handling (pre-transaction Net Parent investment is an intercompany balance, not loss-absorbing capital; parent cash under centralized cash management is flagged, not liquidity) and goodwill/tangible-net-worth discipline (book equity inflated by goodwill is not recovery value) as first-class. Historical periods only; excludes forward projections throughout. Use for \"balance sheet,\" \"historical balance sheet,\" \"working capital,\" \"tangible net worth,\" \"carve-out balance sheet,\" or a read on balance-sheet strength."
when_to_use: "Use for \"balance sheet,\" \"historical balance sheet,\" \"working capital,\" \"tangible net worth,\" \"carve-out balance sheet,\" or a read on balance-sheet strength. Do not use for the income statement and cash flow, or for the latest quarter alone (Current Period Results)."
---

# Financials — Historical Balance Sheet

Analyzes the historical Balance Sheet for a deal — vault-search-based since no dashboard tile exists for
it, unlike Income Statement/EBITDA which `financials-snapshot` already owns off the `financial_analysis`
tile. Historical periods only; forward projections are out of scope throughout, in every section and
every search.

## Scope and cross-skill sourcing

This skill owns Balance Sheet analysis: current assets, PP&E, goodwill and intangibles, capital structure
and equity, and liabilities (payables, accrued, pension/OPEB, leases, non-current). It does not own Income
Statement trend, margins, EBITDA derivation, or the Cash Flow Statement — those are `financials-snapshot`'s
job (Income Statement/EBITDA) or out of scope for this skill entirely (Cash Flow Statement).

**Before deriving any ratio that needs Revenue or EBITDA** (asset turnover, EV/net PP&E, any debt/EBITDA-
flavored metric), check whether `financials-snapshot` has already run earlier in this conversation. If it
has, use its anchor Revenue and EBITDA figures directly rather than re-deriving them through an independent
vault search — a second, possibly different search result for the same figure is exactly the kind of
cross-source drift `financials-document-conflict-check` exists to catch, and this skill should not create
that risk in the first place. Only run an independent search for Revenue or EBITDA if `financials-snapshot`
has not already established it this conversation, and say plainly that this figure was independently
sourced rather than pulled from an existing anchor.

## Tone and rules

Apply `references/analyst-grade-discipline.md`: no freestanding editorial adjective unless it traces to a
specific disclosed figure; where a figure disagrees with another surface, the disagreement is reported,
never silently resolved.

Apply `references/conventions.md` for any EBITDA or period-anchor figure this skill uses or cross-
references — the same role definitions and anchor-selection rules `financials-snapshot` and
`financials-document-conflict-check` already apply, so a ratio computed here never uses a different basis
than the same figure would carry elsewhere in the suite.

All output conforms to `references/language-standard.md` (American spelling, credit-desk register, no
em-dashes, no hype adjectives). Read it and apply it. Do not expose platform plumbing (no raw tool names,
`research_search_analysis`, `report_type`, similarity scores, or search mechanics) in the body.

**Carve-out handling — first-class, not a generic note.** Where the financials are a carve-out, treat
pre-transaction "equity" (e.g. Net Parent investment) as an intercompany balance, not loss-absorbing
third-party capital: it is replaced at close by sponsor equity, and the Equity section and header both say
so plainly. Parent cash excluded under centralized cash management is flagged as excluded, never read as a
liquidity figure the borrower can actually draw on.

**Goodwill and tangible-asset discipline.** For asset-light or goodwill-heavy balance sheets, state
tangible-asset coverage plainly: book equity inflated by goodwill and intangibles is not recovery value,
and a tangible net worth figure belongs beside any total-equity figure whenever goodwill is material. Where
pre-close equity is not loss-absorbing (a carve-out), prefer tangible asset coverage of total debt at close
over a tangible-net-worth-of-equity figure, since the latter would be measuring a balance that disappears
at close.

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

1. `research_search_analysis(project_id, "current assets cash receivables inventory balance sheet working capital", top_k=7)` — current assets and working capital.
2. `research_search_analysis(project_id, "PP&E property plant equipment gross net depreciation goodwill intangibles non-current assets total assets capital structure equity", top_k=7)` — fixed assets, intangibles, and equity.
3. `research_search_analysis(project_id, "accounts payable accrued liabilities pension OPEB leases non-current liabilities intercompany carve-out parent", top_k=7)` — liabilities and carve-out context.

Discard results with similarity below 0.02. Historical periods only — exclude forward projections from
every search's results.

## STEP 2 — Render

**Header:** deal name, sponsor, currency, PF basis, carve-out context note if applicable.

**Summary Balance Sheet table** (all disclosed historical periods) plus a **post-transaction capital
structure table**.

**One section each for Current Assets, Fixed Assets & Intangibles, Liabilities, and Equity & Returns:**
- One-line trend summary.
- Exactly 2 sentences of analytical commentary — causation, quality, and credit implications only, never
  restating a figure already visible in the table or trend line above it.
- At most one ⚠️ risk callout, one sentence.
- At most one ✅ strength callout, one sentence.

**Derived ratios** (current ratio, quick ratio, asset turnover, tangible net worth or tangible asset
coverage per the carve-out rule above, EV/net PP&E), each labeled "(derived)" or "(calc.)" where the vault
does not disclose it directly. Every ratio using Revenue or EBITDA states which path supplied that figure —
reused from `financials-snapshot`'s anchor, or independently sourced this run — per the cross-skill
sourcing rule above. Never present a derived figure as disclosed, and never derive one the underlying
materials genuinely lack; say "not derivable" instead.

**Data gaps table** — one line per missing item, status only, no filled-in guesses.

**Source citations** at the bottom.

## Second read (mandatory, INTERNAL — a separate pass run AFTER the full render, never shown as a section)

Silent, every time.
1. **Confirm every figure traces to a retrieved chunk.** A number in a table or commentary that isn't
   backed by Step 1's results is fabricated; remove it or re-search.
2. **Confirm the cross-skill sourcing rule actually ran.** Any ratio using Revenue or EBITDA should show
   which path supplied it; a ratio that silently used a fresh, unattributed figure is a defect to fix
   before delivering, not after.
3. **Confirm the carve-out and goodwill disciplines fired where applicable.** If the balance sheet is a
   carve-out, the Equity section and header must both carry the intercompany-balance note; if goodwill is
   material, a tangible-asset-coverage or tangible-net-worth figure must sit beside total equity, using
   whichever the carve-out rule above calls for.
4. **Confirm every commentary block is exactly 2 sentences and doesn't restate a table figure.** This is
   the most common drift point on a strict-format skill; check it explicitly rather than assuming the
   draft already complied.
5. **Confirm data gaps are reported, not filled.** A blank or "not disclosed" item in Step 1's results
   should appear in the Data Gaps table, not be quietly estimated into a number.

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
- For asset-light or goodwill-heavy balance sheets, state tangible-asset coverage plainly; book equity
  inflated by goodwill is not recovery value.
- Carve-out equity is an intercompany balance, not loss-absorbing capital, replaced at close by sponsor
  equity; parent cash under centralized cash management is flagged, never read as liquidity. Where equity
  is not loss-absorbing, prefer tangible asset coverage of debt over tangible net worth of equity.
- Before deriving any Revenue- or EBITDA-based ratio, check for and reuse `financials-snapshot`'s anchor
  figures if that skill has already run this conversation; state which path supplied the figure either way.
- Flag data gaps plainly rather than filling them.
- No platform plumbing in the body: no raw tool, field, or parameter names, no similarity scores.
- Second read and final review are mandatory, separate, and silent; the evidence they ran is a changed
  artifact, never a narrated process block.

## Delivery

Render in chat by default. Only produce a Word document if asked; when generating one, use the docx skill
with a title block (deal name, sponsor, currency, PF basis) and the same section structure as the chat
render. Save to `/mnt/user-data/outputs/` and `present_files`. After delivering, offer one natural next
step: the `financials-snapshot` read if Income Statement/EBITDA hasn't been pulled yet, or a deeper look at
a specific flagged risk or gap.
