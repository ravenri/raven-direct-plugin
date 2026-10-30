---
name: "portfolio-analysis-closed-deal-metrics"
description: "Builds the Closed Deals by Year workbook for the book of closed deals: each deal with date, sponsor, GICS sector, business and amount, grouped by year with totals, plus summary tables by GICS sector and sponsor. Live formulas and a Notes tab."
when_to_use: "Use when asked for closed deals by year, how many deals closed and how much was committed, a closed deal list, or closed deal metrics by year, sector or sponsor. Do not use for concentration or exposure of the book (use the concentration view), for averages of deal metrics by year and sector (a separate report), for a leverage screen, or for a single deal."
---

# Portfolio Analysis - Closed deal metrics

Produces one Excel workbook, Closed Deals by Year, for every deal with status Closed in Raven. Deals are grouped by year with a count and commitments total for each year, followed by summary tables by GICS sector and by sponsor. Every total is a live formula.

All facts come from the deal list and the deal summary. Do not read IC memos or other documents to fill a gap. A gap stays blank and is listed in Notes.

## Language

All output conforms to `references/language-standard.md`. Use American spelling. Do not use em dashes. Do not refer to the vault, the dashboard, tiles, prompts or tools in the workbook or in the reply.

## Assets and scripts

Render from these fixed pieces. Do not redesign the layout per run.

- `assets/Closed_Deal_Metrics_Template.xlsx`: the approved workbook with all deal content cleared. It carries the title, header row, column widths, freeze panes and the Notes tab. It is a guideline for layout and style.
- `assets/GICS_Sectors.xlsx`: the 11 GICS sectors with their codes and a short description of each. It is the only list of sectors. Use it to classify every deal.
- `scripts/build_closed_deals.py`: fills the template from a build input file, writes the year blocks, totals, summary tables and Notes, all as formulas, and stops if a sector is not one of the 11. The input file is a working file, not a deliverable; keep it in scratch space. Its shape is documented at the top of the script.
- `scripts/check_closed_deals.py`: the pre-delivery check. Run it after recalculation with the same input file. It confirms the year totals, the all years total, the memo deal count and that the GICS sector table totals to the deal count and commitments, that every deal has a date, business, sponsor and a valid sector, that there are no formula errors, and that no banned wording or em dashes appear.

## Workbook layout

Sheet "Closed Deals". Columns: Deal, Date, Sponsor, GICS Sector, Business, Amount ($mm), Sponsor 1 to Sponsor 4.

- Year blocks in ascending order, each with a shaded year label, its deals in date order, and a total row showing the deal count and the sum of amounts. An All years row follows.
- By GICS sector: all 11 sectors in code order, with deals and commitments, and a total. A sector with no deals shows 0.
- By sponsor: every named sponsor, ordered by deal count, with deals and commitments. Every sponsor on a deal is credited in full, so the total row is labeled "Total (sponsors overlap)" and a Memo row beneath it shows the true deal count and commitments, with a one-line note explaining the overlap.
- Amounts are entered values in blue, formulas are black. Arial throughout, navy header rows, no other colors. Dates display as month and year.

Sheet "Notes": scope, the definition of each column, and anything specific to this run.

## Steps

1. Call `deal_list` with the filter for status Closed and the full list. This gives the company name, the deal name, the sponsor label and the loan amount.
2. Deal: the company name as the deal list shows it.
3. Date: the year and month at the start of the deal name (for example 2025-07 is July 2025). Store the first of that month. If a name has no year and month, leave the date blank and list the deal in Notes.
4. Amount: the loan amount as stored in Raven, in $ millions. Where Raven shows 0, leave the amount blank and list the deal in Notes. Do not estimate.
5. Sponsor: the sponsor label as the deal list shows it. Split it into up to four names, one per column. Expand abbreviations to the firm's name (for example Bain to Bain Capital, GS or Goldman to Goldman Sachs, 6th St to Sixth Street, Berkshire to Berkshire Partners). If a name cannot be resolved to one firm, keep it as shown with "(as shown in Raven)" and explain in Notes. Never assume.
6. GICS sector and business: pull the deal summary overview for every deal with `portfolio_compare`, tile `deal_summary_dashboard`, section `overview`, in batches of 8, sending the calls together. Large results are saved to a file; read them with a short script that pulls the company description for each deal. From the description, write a short business description (a few words) and assign the one GICS sector in `assets/GICS_Sectors.xlsx` that matches the principal business. If a company spans two sectors, take the larger part of its revenue. If the description is too thin to decide, assign the closest sector and add the deal to Notes as assumed.
7. Write the build input file, run `scripts/build_closed_deals.py`, recalculate with the xlsx skill's recalculation script, then run `scripts/check_closed_deals.py` with the same input file. Fix anything it names before delivering.
8. Name the file "Closed Deals by Year.xlsx" and deliver it.

## Notes tab

The fixed notes are written by the script. Add a run note for each of these when it applies:

- A deal with a blank amount.
- A deal whose name has no year and month.
- A deal whose GICS sector is assumed because the description was thin.
- A sponsor name that could not be resolved to one firm.

## Reply

Two or three sentences: how many deals are in the workbook, the commitments total, and the busiest year. Then a short numbered list of anything the user needs to confirm, taken from the Notes tab. Do not paste the tables into the reply. Say in one line what the check found.

## Rules

- Scope is deals with status Closed. New or declined deals are not included.
- Take every figure from Raven as stored. Do not convert, round or restate amounts. The only calculations are the live totals in the workbook.
- A blank is a blank. Do not fill a missing amount or date with an estimate, and do not go to other documents to find one.
- Deal lead is not part of this report until it is shown on the deal summary.
- Sponsor totals overlap and exceed the deal count. Always show the memo row beneath them.
- Carry nothing over between runs. Every run pulls fresh.
