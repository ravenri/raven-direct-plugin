---
name: "deal-terms-loan-returns"
description: "Calculates levered and unlevered returns (IRR and MOIC) for a single loan tranche on a quarterly basis, using terms pulled from Raven Direct. Supports an optional PIK period, OID as the only upfront fee, no exit fees, and leverage by default, with the financing line paid down pro rata as the loan amortizes. Resolves the deal, asks which tranche if there is more than one, prompts for the assumptions (funding date, amount, spread, issue price, PIK quarters, amortization, hold, exit price, leverage multiple and spread), echoes them normalized, and runs a bundled quarterly engine against a SOFR forward curve aligned to the funding date (an uploaded curve is used first). Renders levered then unlevered headlines, cash flows by year, and a levered sensitivity table in chat. Use for \"run the returns,\" \"levered and unlevered returns,\" \"IRR and MOIC on this tranche,\" or \"returns with a PIK period.\" Single tranche only. Requires Raven Direct."
when_to_use: "Use for \"run the returns,\" \"levered and unlevered returns,\" \"IRR and MOIC on this tranche,\" or \"returns with a PIK period.\" Do not use for more than one tranche at a time, or for a coverage or covenant read."
---

# Deal Terms: Loan Returns

Calculates a single tranche's returns on a quarterly basis, levered and unlevered, and shows the work.
Leverage is part of the default flow, not an option. The returns math lives in a bundled spreadsheet
engine. Fill the inputs, recalculate, and read the results. Never calculate IRR or MOIC by hand.

## Language

Write all output in American English (color, behavior, favorable, organize, analyze).

## START HERE: this skill begins cold, every time

Assume nothing is loaded. Do not open by asking "what deal?" or "where is the file?" Resolve it in this order:

1. **Resolve the deal.** If a project_id is already known from earlier in the conversation, use it. Otherwise take the deal name from the request and search by deal name and by company name (`deal_list(name=...)` and `deal_list(company_name=...)`). If more than one deal matches across the two searches, show them as a table and ask which. If neither search returns a match, list all deals and match loosely on name, company name, and sponsor, because a deal can be listed under a project codename different from the name the person uses. Show any plausible match and confirm it before continuing.
2. **Confirm readiness.** `analysis_get_status(project_id)`. If not "Ready to view!", say so and stop.
3. **Pull the tranches and their terms.** `dashboard_get(tile="deal_summary_dashboard")` (Debt Facilities section: size, pricing and benchmark, OID, amortization), then `dashboard_get(tile="coverage_liquidity")` (Debt Structure table) if needed, then `research_search_analysis` for PIK terms, amortization, or the executed pricing grid when a credit agreement is loaded. A field shown as "Not disclosed in documents" is a real answer, not a gap to fill silently. Note the facility's actual base rate (for example 3M Term SOFR) and any floor.
4. **If there is more than one tranche, stop and ask which one to run.** List every tranche with its size and headline pricing. Never guess, never pick the largest, never blend tranches. Run the chosen one; a later run can do another.

## Sources and conflicts

If the dashboard says the deal's documents changed since the last full analysis, say so before presenting figures.

For each term taken from Raven, record its source document and page, for example "Spread: SOFR + 600 bps (Credit Agreement, p. XX)". If sources disagree on a modeled term, do not pick one. Show each value with its source and ask which applies, unless Raven has already designated an executed or current term.

## Ask: in plain text, in this order

After the scan, ask for the assumptions in one numbered message, with anything Raven discloses already filled in (with its source) and any default shown. Ask in plain text, not buttons:

1. Funding date (default today).
2. Position size: how much of the tranche are you modeling, for example "$25MM of the $330MM tranche"? Returns percentages don't change with position size; only the dollar figures do.
3. Spread over SOFR (confirm a disclosed figure with its source; if not disclosed, ask).
4. OID or issue price. Market convention is a price: "98" means a 2.0% discount, "100" means none.
5. PIK period in quarters (default 0).
6. Amortization, percent of original face per year. "1" means 1%. None is paid during a PIK period.
7. Hold, in quarters or years, up to 20 quarters. "3.5 years" is 14 quarters. If a hold is not a whole number of quarters, round to the nearest quarter and say so.
8. Exit price, percent of par. Default 100. "96" means 96% of remaining principal.
9. Leverage multiple (default 1.0x).
10. Leverage spread (default SOFR + 300 bps).

Never invent a tranche term. If a term is undisclosed, say so and ask. The financing line is always paid down pro rata with the loan's scheduled principal repayments; it is not a question.

**Before computing, echo the normalized assumptions**, for example: "Modeling 98 OID as a 2.0% discount, 1% annual amortization, and a 12-quarter hold." Ask for confirmation only where an input is ambiguous, was converted in a non-obvious way, or conflicts with a Raven-derived term, for example: "You entered '2 OID.' I'm reading that as a 98 issue price. Correct?"

## SOFR curve: check before every run

The engine prices off a quarterly SOFR forward assumption on the `Curve` tab (`C6:C25`, quarters 1 to 20, quarter 1 starting on the date in `D6`). The engine aligns the curve to the quarter start nearest the funding date.

1. Before computing, check whether the person uploaded a curve. If so, validate it (see `references/curve-guide.md`), write it into `Curve!C6:C25`, set `Curve!D6` to the date quarter 1 starts (ask if the file does not say), and say plainly that an uploaded curve is being used.
2. If none was uploaded, ask once whether they have one. If not, use the bundled curve and say so.
3. Before every run, check the as-of date of the bundled curve. If it is more than two weeks before today, refresh it from the sources named in `references/curve-guide.md`, write the new rates into `Curve!C6:C25`, and tell the person the curve was refreshed and its date.
4. After writing the inputs, read `Returns!C15` (curve status). If the funding date is before the curve date, or the curve runs out before the hold ends, say so in plain words. Beyond the last point the rate is held flat.

## Compute: use the bundled engine

1. Copy `assets/quarterly_returns_template.xlsx` to a working file.
2. Write the inputs (cell map in `references/spreadsheet-guide.md`): `C6` face, `C7` spread (bps), `C8` issue price, `C9` hold quarters, `C10` PIK quarters, `C11` amortization (decimal), `C12` exit price, `C13` funding date, `I6` leverage multiple, `I8` leverage spread (bps).
3. Recalculate the workbook.
4. Read results directly from cells: unlevered and levered annualized IRR (`C49`, `D49`), MOIC (`C51`, `D51`), the annual roll-up (rows 56 to 65), and the levered sensitivity table (rows 70 to 74). Never compute, combine, or split a figure by hand.

## Show

Render in chat, in this order:

1. **Assumptions first**, in two labeled groups: real from Raven (each term with its source document and page, and which terms were not disclosed), and assumed (funding date, hold, PIK, leverage, leverage spread, exit price, curve with its date). Always include these four disclosures:
   - "Facility benchmark: [base rate from Raven]. The bundled curve is derived from overnight SOFR swaps and is a proxy for forward SOFR. It is not CME Term SOFR. Use a Term SOFR curve for decision-grade work."
   - "Financing: paid down pro rata with the loan's scheduled principal repayments, with the remainder repaid at exit. PIK interest does not change it."
   - "Interest accrues at rate/4 each quarter. The model does not use an actual/360 day count, so calculated interest may differ modestly from contractual cash interest."
   - "Leverage: [X]x debt/equity, equivalent to a [Y]% advance rate." (The advance rate is in cell `I7`.)
2. **Levered headline**, then its cash flows, then the sensitivity table. Headline: "Levered return on a [N]-quarter hold at [X]x leverage is [Y]% IRR and [Z]x MOIC for [tranche]."
3. **Unlevered headline** and its cash flows. Headline: "Unlevered return on a [N]-quarter hold is [Y]% IRR and [Z]x MOIC."
4. **Cash flows by year by default**, from the annual roll-up rows. Offer the full quarterly schedule on request.
5. **Sensitivity table** (levered only): spread against leverage multiple (0.75x, 1.0x, 1.25x), labeled as a sensitivity table, with a spanning header "Leverage (x)". Confirm the 1.0x column at the real spread matches the main levered IRR when the leverage input is 1.0x (check cell `B77`).
6. **During a PIK period, levered cash flows can be negative** because the financing line still pays interest while the loan pays none in cash. Say so explicitly whenever it occurs.

## Not modeled

State once, in the response: SOFR floors, exit fees, excess cash flow sweeps, warrants, the Term SOFR basis, actual/360 day count, intra-quarter reset and payment timing, financing-line borrowing-base mechanics, default timing, delayed draws, unused fees, call protection or soft-call premiums, and portfolio-level returns. Upfront fees are represented by OID only.

## Iterate

Offer to change any assumption and rerun, showing the new results the same way. Offer the spreadsheet only if asked; then call `present_files`.

## Reference

- `assets/quarterly_returns_template.xlsx`: the quarterly engine.
- `assets/sofr_curve_quarterly.csv`: the bundled curve in upload format.
- `references/spreadsheet-guide.md`: cell map and mechanics.
- `references/curve-guide.md`: curve sources, validation rules, and the upload format.
