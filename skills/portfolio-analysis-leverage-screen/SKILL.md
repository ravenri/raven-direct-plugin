---
name: "portfolio-analysis-leverage-screen"
description: "Screens the whole book for deals whose net leverage clears a threshold and delivers a ranked Excel workbook with sponsor, debt, EBITDA, basis, as-of period and maturity range. A drill-down on one deal follows on request."
when_to_use: "Use for \"leverage screen,\" \"which deals are over a leverage threshold,\" \"rank the book by leverage,\" \"net leverage above X,\" or any screen of the whole book. Do not use for one deal's leverage (Loan Coverage, Quick Screen) or a comparison of two deals."
---

# Portfolio Analysis - Leverage Screen

Screens the book for deals whose leverage clears a threshold. The unit of analysis is the whole book, even though the answer is a list of deals. Two stages:

- **Stage 1 (default):** a ranked Excel workbook across all deals with sponsor, total debt, EBITDA, net leverage, basis, as-of period and maturity range, plus a short summary in chat.
- **Stage 2 (follow-up):** when the PM names a deal, the full debt build for that deal: tranches, the net debt calculation, sources and flags.

This is Portfolio Analysis, not Monitoring. It asks a cross-deal question (which deals are over X), not how one deal is tracking against its own plan.

## Language

All output conforms to `references/language-standard.md`. Use American spelling. Do not use em dashes. Do not expose platform plumbing (no tile names, tool names, prompt IDs, or references to the vault). Present a leverage figure as a leverage figure and name sources as the underlying deal documents.

## The leverage basis convention

Leverage is inconsistent across deals: some disclose net, some total, some both, some neither. A screen that mixes net and total on one axis is misleading, because the same deal can be over the threshold on net and under on total. The screen enforces one basis:

- **Net is the baseline.** Use net leverage wherever it is disclosed.
- **When the deal holds no cash, net equals total.** Use total; it is the net figure.
- **When net is not disclosed but cash likely exists, show total and label it "total; net n/d".** This is a disclosure gap, not a clean net read. Never rank a total figure as if it were net.
- **Where both are disclosed, screen on net.** Note total in the basis column, but net is what the row is ranked and thresholded on. A deal under on net is under, even if total is over.
- **Partial net measures are not total net.** If the stated net figure is first lien or secured only, label it "1L net" or "secured net" and show the total figure beside it. Do not present it as clean net.

## STEP 1: Resolve the book

Call `deal_list` with the full list of processed deals (skip if the set is already known from this conversation). If the PM named a subset ("my software deals", "the names in my second fund"), screen only those. Otherwise screen the whole book.

If the PM gave no threshold, use 5.0x net and say so at the top of the answer.

## STEP 2: Pull the book in batches of 8, two passes in parallel

`portfolio_compare` takes at most 8 project_ids per call. Use `tile="deal_summary_dashboard"` and run two passes over the same batches, sending the calls together:

- `section="overview"` for leverage, EBITDA, debt, cash, sponsor and the EBITDA basis label.
- `section="debt-facilities"` for tranche maturities.

A book of 37 deals is five batches per pass. Large results are saved to a file instead of returned inline, and a few deal entries are shortened. Read the saved files with a short script that pulls the leverage, EBITDA, debt, cash and maturity lines per deal rather than reading the raw text. If a deal entry is shortened and a needed field is missing, say it is not disclosed on the screen rather than guessing, or pull that deal alone.

From each deal's overview read: net leverage and total leverage, the EBITDA figure and its label, total debt or net debt and cash, the sponsor, and whether the deal states any cash conflict. Take the sponsor from the deal summary, not the deal list. If the two disagree, show the summary's sponsor and note the conflict. Where total debt is not stated, derive it as net debt plus cash and say so in the notes. When the Financial Analysis or monitoring feed is available for a deal, prefer it for the quarterly series (up to four quarters); until then entry leverage is the single point.

From each deal's debt facilities read each tranche's maturity and reduce to a range, handling the real states honestly:

- Dated tranches: the range of actual dates (for example "Oct 2031 to Oct 2032").
- Tenor only, no absolute date: say so ("~2032, tenor only").
- Sources conflict on a maturity: flag it ("Dec 2030, source conflict"). Do not silently pick one.
- Instruments with undisclosed maturity (HoldCo notes, seller notes): name them ("HoldCo PIK n/d").
- Nothing disclosed: "n/d".

Refinancing risk is not leverage risk. The least levered deal can have the nearest maturity, so the maturity range earns its place on the screen.

## Stage 1: Build the workbook

Build the workbook from the fixed layout below. Do not redesign it per run.

**Sheet "Leverage Screen".** Title, one-line subtitle, then the threshold input cell (C3, blue text, outlined, no fill), a count of deals over threshold (a COUNTIF formula on the threshold cell), and the count of deals screened. The table header is on row 7, with columns:

Rank, Deal, Sponsor, Currency, Total debt (MM), EBITDA (MM), Net leverage, Status, Basis, As-of, Maturity range.

- Rank is a RANK formula on net leverage.
- Status is an IF formula against the threshold cell ("Over" or "Under").
- Rows with leverage above the threshold are bold by conditional formatting driven by the threshold cell, so changing the threshold re-runs the screen.
- Sort rows by net leverage, highest first.
- Net leverage is formatted 0.00"x". Debt and EBITDA are in millions. Name the currency per row. Leverage is a ratio, so a non-USD deal is ranked normally and its currency is shown.
- Entered values are blue, formulas are black. No colored fills, tinted boxes, colored borders or badges, and no KPI tiles. Use Arial throughout and a dark header row.
- Below the table, a Not assessable block listing each deal that cannot be screened and why (no leverage disclosed, an EV multiple mistaken for leverage, or no debt amounts disclosed). A deal that cannot be assessed is not under the threshold, and the block says so.

**Sheet "Notes".** Plain text, no tables: the basis convention, the rows to read with care, and the data notes (how total debt was derived, where EBITDA is not shown, what maturity range means, and the source line).

Run a recalculation and confirm there are no formula errors before delivering. Check that the count over threshold matches a hand count of the table.

Column rules:

- **As-of** is the period the figure is struck on, carrying the deal's own EBITDA basis label verbatim (for example "LTM Jun-25 PF Adj Cash", "2026E PF Adj"). Do not normalize or shorten it. A "Cash" label appears on deals with a deferred revenue adjustment, and its absence means accrual PF Adjusted EBITDA. Cash and accrual leverage are not comparable, and the label is the only signal of it on the screen. As-of is the period the figure reflects, not the generated date.
- **Basis** reads "net", "net; total 8.25x gross" where the gap to total is worth seeing, "1L net; total 8.24x gross", "secured net; total 8.40x gross", or "total; net n/d".
- **Sponsor** drops legal suffixes (LLC, L.P., Inc.) per the language standard.
- Provision for four quarters of leverage history as added year-labeled columns (Q1'25, Q2'25, never bare Q1), oldest to newest, once monitoring data exists. Until then there is one figure per deal and no delta column.

## Flags to carry on the Notes sheet

Raise a flag whenever one applies:

- The leverage anchor is struck on a different perimeter from the deal being financed (for example a combined company against a standalone acquisition package).
- A first lien or secured net figure is ranked in place of total net.
- Net is far below total and cash does not explain the gap (for example HoldCo PIK notes sit in total but not net).
- Net depends on restricted, trust or operating cash.
- Two sources disagree on closing cash, a maturity, or a facility amount.
- EBITDA is a sponsor projection with no actuals disclosed, or embeds unrealized synergies.
- Debt and EBITDA are in a non-USD currency.

## Chat summary

After delivering the workbook, give a short summary in chat: the threshold used, how many deals were screened and how many are over, the not assessable deals by name, and the two or three flags that most change how the list reads. Do not paste the full table into chat. Close with one line offering the drill-down: name a deal for its full debt build, tranches, calculation and sources.

## Stage 2: Per-deal drill-down

When the PM names a deal, pull its debt facilities (`dashboard_get` with `tile="deal_summary_dashboard"` and `section="debt-facilities"`, or the cap table) and render, in chat unless Word is requested:

- The tranche breakdown: each facility, size, drawn or undrawn, maturity.
- The net debt build: total funded debt, less cash, equals net debt.
- The calculation: net debt over EBITDA is net leverage, total debt over EBITDA is total leverage, with the EBITDA figure and its period named.
- The source documents behind each figure.
- Any flag: an EBITDA basis that embeds unrealized synergies, a net figure that is not disclosed, a drawn revolver reducing day-one liquidity, a springing or near-term maturity, a covenant threshold the current figure sits near.

Stage 2 fires only when the PM names a deal. Do not drill into every deal.

## Rules

- Net is the baseline. Total only when there is no cash, and "total; net n/d" when net is undisclosed. Never mix net and total silently on the ranked axis.
- Screen and threshold on the basis that governs. A deal under on net is under, even if total is over.
- Take every figure from the deal summaries as stated. Quote leverage, EBITDA and maturities; do not recompute or re-rate them. The only derivation allowed is total debt as net debt plus cash, disclosed in the notes.
- Maturity is shown as a range with honest states. Refinancing risk is not leverage risk.
- Not assessable deals are listed below the table, never ranked as under the threshold.
- Coverage ratios are out of scope. They come from the Financial Analysis and monitoring feed.
- Batch both passes in 8s for a large book and say so if the screen is partial.
- Stage 1 is the whole book workbook. Stage 2 is the per-deal build, only on a follow-up naming a deal.