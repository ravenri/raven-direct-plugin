---
name: "portfolio-analysis-deals-at-a-glance"
description: "Builds the Deals at a Glance workbook for the book of closed deals: each deal with date, GICS sector, enterprise value, EV/EBITDA, net and total leverage, first lien LTV and sponsor equity, grouped by year with averages, plus averages by GICS sector. Live formulas, a detail tab and a Notes tab."
when_to_use: "Use when asked for deals at a glance, key metrics or typical terms across closed deals, average leverage, EV/EBITDA or sponsor equity by year or sector, or the averages report. Do not use for a ranked leverage screen or a threshold question (use the leverage screen), for deal counts and commitments by year, sector or sponsor (use closed deal metrics), for concentration of the book, or for a single deal."
---

# Portfolio Analysis - Deals at a glance

Produces one Excel workbook, Deals at a Glance, for every deal with status Closed in Raven. Each deal shows its key terms as Raven shows them. Deals are grouped by year with a simple average for each year, followed by an all deals average and averages by GICS sector. Every average is a live formula.

All facts come from the deal list and the Deal At A Glance section of each deal summary. Do not read IC memos or other documents to fill a gap. A gap stays blank and is listed in Notes.

## Language

All output conforms to `references/language-standard.md`. Use American spelling. Do not use em dashes. Do not refer to the vault, the dashboard, tiles, prompts or tools in the workbook or in the reply.

## Assets and scripts

Render from these fixed pieces. Do not redesign the layout per run.

- `assets/Deals_at_a_Glance_Template.xlsx`: the approved workbook with all deal content cleared. It carries the titles, header rows, column widths, freeze panes and the Notes tab. It is a guideline for layout and style.
- `assets/GICS_Sectors.xlsx`: the 11 GICS sectors with their codes and a short description of each. It is the only list of sectors. Use it to classify every deal.
- `scripts/extract_glance.py`: reads the saved deal summary results and writes a working file with, for each deal, the company name, the currency, the Deal At A Glance rows exactly as shown, and the opening of the company description. It reports any deal whose table is missing and prints one compact line per deal (name, currency, row count, the first 180 characters of the description), which is all that needs to be read to choose the sectors.
- `scripts/build_deals_at_a_glance.py`: reads the working file once the date and sector are added to each deal, parses the figures from the text Raven shows, fills the template, writes the year blocks, averages, sector table, detail tab and Notes, and stops if a sector is not one of the 11. The working file is not a deliverable; keep it in scratch space.
- `scripts/check_deals_at_a_glance.py`: the pre-delivery check. Run it after recalculation with the same working file. It confirms the deal count, the dates, the sectors, that the year, all deals and sector averages tie to the parsed figures, that the sector table totals the deal count, that there are no formula errors, and that no banned wording or em dashes appear.

## Workbook layout

Sheet "Averages by Year". Columns: Deal, Date, GICS Sector, Enterprise value ($mm), EV / EBITDA, Net leverage, Total leverage, First lien LTV, Sponsor equity / cushion %.

- Year blocks in ascending order, each with a shaded year label, its deals in date order, and an average row showing the deal count and the simple average of each metric. An All deals average row follows.
- Averages by GICS sector: all 11 sectors in code order, with the deal count and the average of each metric, and a total. A sector with no deals shows 0 and blank averages.
- Metric values are entered in blue, formulas are black. Arial throughout, navy header rows, no other colors. Dates display as month and year.

Sheet "Deal at a Glance": the same deals with Raven's text for each metric, including the basis and period of each leverage figure, the transaction size, total net debt, pro forma cash and any other lines Raven shows.

Sheet "Notes": scope, the definition of each column, and anything specific to this run.

## Steps

1. Call `deal_list` with the filter for status Closed and the full list. This gives the company name and the deal name for each deal.
2. Pull the deal summary overview for every deal with `portfolio_compare`, tile `deal_summary_dashboard`, section `overview`, in batches of 8, sending the calls together. Large results are saved to files. Always use section `overview` exactly; any other section name returns the whole deal summary for each deal, which is much larger. Do not open, print or read the saved files; the extract script in the next step is the only thing that reads them.
3. Run `scripts/extract_glance.py` on the saved files. If a deal comes back without a table, pull that deal again on its own. If it is still missing, leave its metrics blank and list it in Notes.
4. Date: the year and month at the start of the deal name (for example 2025-07 is July 2025). Store the first of that month. If a name has no year and month, leave the deal out of the year blocks only if there is no other choice, and say so in Notes.
5. GICS sector: from the company description, assign the one sector in `assets/GICS_Sectors.xlsx` that matches the principal business. If a company spans two sectors, take the larger part of its revenue. If the description is too thin to decide, assign the closest sector and add the deal to Notes as assumed.
6. Add the date and sector to each deal in the working file, run `scripts/build_deals_at_a_glance.py`, recalculate with the xlsx skill's recalculation script, then run `scripts/check_deals_at_a_glance.py` with the same working file. Fix anything it names before delivering.
7. Name the file "Deals at a Glance.xlsx" and deliver it.

## Notes tab

The fixed notes and the notes for leverage on a secured, first lien or net basis, equity cushion in place of sponsor equity, enterprise values in another currency, two values shown, and metrics Raven does not show are written by the script. Add a run note for each of these when it applies:

- A deal whose name has no year and month.
- A deal whose GICS sector is assumed because the description was thin.
- A deal whose Deal At A Glance table could not be found.

## Reply

Two or three sentences: how many deals are in the workbook, the all deals averages for net leverage and EV / EBITDA, and the count of deals behind each. Then a short numbered list of anything the user needs to confirm, taken from the Notes tab. Do not paste the tables into the reply. Say in one line what the check found.

## Rules

- Scope is deals with status Closed. New or declined deals are not included.
- Take every figure from Raven as shown. Do not correct, convert, round or restate a figure, and do not replace one value with a figure from another page or document. If a figure looks wrong, say so in the reply and leave it as shown.
- Where Raven shows two values for one metric, use the first and note it. Where a value is in a currency other than US dollars, leave it blank and note it.
- A blank is a blank. Averages skip blanks. Do not estimate a missing figure.
- Leverage is on each deal's own basis. Never relabel a basis, and keep secured net and first lien net visible in Notes.
- Deal lead is not part of this report until it is shown on the deal summary.
- Carry nothing over between runs. Every run pulls fresh.
