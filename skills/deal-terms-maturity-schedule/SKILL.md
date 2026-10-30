---
name: "deal-terms-maturity-schedule"
description: "A debt maturity schedule by tranche, cited to source, showing the balance still outstanding at each maturity and flagging refinancing need. Use for maturity schedule, debt maturities, what is due when, refinancing risk, maturity wall for one deal."
when_to_use: "Maturity schedule, debt maturities, what is due when, refinancing risk, maturity wall for one deal. Use this instead of answering ad hoc."
---

# Deal - Terms - Maturity Schedule

One table for one deal: each tranche, when it matures, and how much of it is still outstanding on that date under the base case. A tranche with a balance outstanding at maturity is flagged as needing refinancing. Nothing else is judged.

## Scope

One deal, one schedule. Not a coverage read, not a view on whether refinancing markets will be open, and not a comparison across deals. Where the request is for any of those, say so and point to the right read (coverage and liquidity for coverage; the portfolio screen for several deals). Flag and point; do not perform.

## Assets

- `references/language-standard.md`: the house language standard. Read it and apply it to all prose; do not restate its rules here.
- `assets/maturity_schedule_template.docx`: the Word template, used only when a document is requested.

## Step 1: Find the deal

Use the deal the person names. If a project is already known from earlier in the conversation, use it. If a name is given, resolve it with `deal_list`: one match, use it; several, show them as a table (Deal, Company, Sponsor, Status) and ask which. If no deal is named, ask which one before doing anything else.

## Step 2: Read the sources

`dashboard_get` is deferred. If it is not loaded, load it with `tool_search` first. Do not call anything already available from earlier in the conversation.

1. **Facilities:** `dashboard_get(deal_summary_dashboard, section "debt-facilities")`. Read amount, maturity date, scheduled amortization and any springing or conditional maturity terms for every facility, including the revolver commitment.
2. **Balances and leverage:** `dashboard_get(coverage_liquidity, section "forecast")`, once. Read the balance of each instrument by year, the leverage by period and the model's own notes on the revolver and the sweep.
3. **Section fallback:** if a section is rejected, the response lists the valid ones. Use the nearest, or read the whole dashboard. If the page does not carry balances by tranche, or the deal has no page, read the base case Levered FCF model with `model_list` and `model_view`, and say in the source line that the model, not the page, supplied the balances.
4. **Document conflicts and missing dates:** only if a maturity date or amount is absent or the two dashboards disagree, run `research_search_analysis` for that facility's terms, once per facility.

Note each source's freshness. If a dashboard flags its data as stale, say so in the notes once, using the dashboard's own stated reason. Never manufacture staleness.

If the deal is not ready (`analysis_get_status` not "Ready to view!"), stop, report the status, and do not render figures.

## Step 3: Build the schedule

One table, one row per tranche, in the capital structure's own order (senior first), with these columns:

1. Tranche
2. Amount at close
3. Maturity date
4. Scheduled amortization
5. Balance outstanding at maturity (base case)
6. Repaid by maturity (percent, derived)
7. Leverage at maturity (as stated, with its basis)
8. Refinancing flag
9. Source

How each column is filled:

- **Balance outstanding at maturity:** the stored balance for the instrument in the period that contains its maturity date. If the model ends before the maturity date, write "Beyond model horizon" and state the last modeled balance and period in the source line. Never extrapolate.
- **Repaid by maturity:** amount at close less the balance outstanding at maturity, divided by the amount at close, shown as a percent and labeled derived. This is the only figure the skill computes. Leave it blank where either input is missing or the maturity is beyond the model horizon. Where the model assumes the revolver is undrawn, show n/a for the revolver row and say so in the notes.
- **Leverage at maturity:** Net Debt / PF Adjusted EBITDA for that period on every row, as stored, with the basis exactly as the page labels it. Where the page also carries first lien net leverage, add it once under the table. Never build a ratio from two stored inputs and never switch basis between rows.
- **Refinancing flag:** "Refinance required" where a balance is still outstanding at maturity under the base case; blank where the balance is zero. No threshold, no severity, no rating of our own. Where the maturity is beyond the model horizon, write "Not testable" with the reason.
- **Source:** the document and page the dashboard lists for the facility terms, and the model or page that supplied the balance.

Add a final row for total debt only if the pages store it, and as stored.

## Step 4: Springing and conditional maturities

Under the table, list any springing or conditional maturity as the documents state it: the facility, the trigger (for example, 91 days before another facility's maturity if it is still outstanding), the resulting date, and the document. Label each "Conditional". If a springing maturity would pull a tranche's effective maturity earlier than the date in the table, say so in one sentence under that row. Omit this section if there are none.

## Step 5: Notes

State credit-relevant gaps once, in a short numbered list: a missing maturity date, no model available, documents that disagree (show both figures and name each document), a stale source, a maturity beyond the model horizon. Where the page does not state whether balances are year-end or at the maturity date, say so once. Do not state absences that do not matter. Do not repeat in prose what the table shows.

## Rules

- Every figure is quoted as the source states it. Only Repaid by maturity is computed, and it is labeled derived.
- The refinancing flag means one thing: a balance is outstanding at maturity under the base case. A tranche fully repaid is not flagged.
- Where documents disagree on a date or amount, show both and name each document. Never pick a side.
- Name sources as the underlying documents. Never refer to the vault, the dashboards, the tiles, the run, or prompt IDs in the output.
- Omit empty rows and columns.
- Outflows and amortization in parentheses, as the page carries them. Currency and units as the page states them, stated once above the table.
- Language standard applies to all prose: American spelling, no em dashes, no hype adjectives.
- Scope: one deal, maturities and base case balances only.

## Delivery

Render in chat by default: the table, the springing list if any, the notes, then a link to the deal page and one natural next step (the coverage read for debt service, or the legal terms for springing mechanics). Build a Word document once, only on request, from what was already produced, using the docx skill and a copy of `assets/maturity_schedule_template.docx`, landscape, replacing placeholders and adding or deleting rows only as the schedule requires. If this session cannot create files, say so and stay in chat.
