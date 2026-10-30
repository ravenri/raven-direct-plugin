# Section Specifications

The rules for each section of the Initial Deal Review, in render order. SKILL.md holds the workflow, the master
absence rule, the call batch, Pass 2, and delivery. Read this file once before drafting.

## Cover Block

Fill the cover table in the template (see Word Document Layout). Fields:

- **Project:** project name, company, and nickname if one exists. Use the deal list's name, never a dashboard's own Deal field.
- **Sponsor:** take it from the Deal Summary header. If that header carries no Sponsor, take it from the Credit
  Assessment header, then from the Deal & Party Identification answer, and cross-check them. List both if co-sponsored.
  If the sources disagree on whether a sponsor is identified, add an Analyst Note naming each.
- **Agent:** from #11, e.g. "Royal Bank of Canada". Omit the Agent row if no agent is found.
- **Facility under review:** the primary funded instrument, the figure resolved in Sources & Uses and Capitalization.
- **Earnings basis:** the LTM period label.

If `freshness.is_stale` is true, fill in the staleness note under the table with the `last_full_run_at` date.
Otherwise delete that note. The confidentiality line stays as it appears in the template.

---

## Initial Read

Placed first, directly under the cover table. Source it from the Credit Assessment dashboard's own short fields, as
stored. Render a two-column table with the Screening view (one row per tranche, from the Preliminary Screening View),
the Credit rating (the Rating word from the Call), and the Repayment read (the Call's Repayment Read sentence). Under
the table, render the Preliminary Screening View's Basis text as stored, then the Governing Conditions as a plain
numbered list. Do not use the Summary field and do not write your own synthesis. Leave out the Rating Value,
Composite, Composite Band, lens ratings, and scorecard. If the Credit Assessment is not generated, omit the section, tell the user in chat, and do not write a substitute read. If a figure in the Basis differs from the figure
resolved in Sources & Uses and Capitalization, keep the stored wording and add a shaded Analyst Note under the text
naming both figures and where each came from.

---

## Overview

Its own section, after the Initial Read. Pull from the transaction-overview content (call #13). Two to three
sentences: deal type, who is acquiring what and from whom, headline price, and the stated rationale. State the funding
structure in one clause without tranche amounts, since Sources & Uses shows them. Do not write sentences about what
the narrative leaves out. If the content isn't available, assemble the Overview from the deal context.

**Figure-discipline rule:** do not assert a figure that is still genuinely unresolved at the time this section runs,
i.e., anything Sources & Uses and Capitalization flags as in conflict for this run. This does not mean avoiding every
number the Credit Assessment mentions; once a figure is resolved, reference it naturally. Only genuinely open
conflicts get "see Sources & Uses and Capitalization for the flagged figure" treatment.

---

## Sources & Uses and Capitalization

Render these tables from the Deal Summary dashboard, Sources Uses section, exactly as stored. Do not rebuild,
regroup, re-rank, or recompute anything.

**Sources and Uses:** show the dashboard's amounts and balance result as stored. Show percent of total only where the
dashboard stores it; otherwise drop those columns. If the Sources Uses section lists uses only, take the sources lines
from the Cap Table's debt and equity rows, amounts as stored, and say so in the source line. If the Cap Table also
lacks them, take them from the sources-and-uses record (call #14).

**Capitalization:** show the Cap Table rows in the dashboard's own order and with its own columns: Instrument,
Amount, Tenor, Percent of capitalization, EBITDA multiple, EBITDA multiple on a cash basis, and Note. Keep subtotal
and total rows as stored. Seniority lives in the Note column, so tranches the dashboard describes as pari passu stay
grouped exactly as it shows them. Show the dashboard's EBITDA reference label directly under the table.

Write the balance check in words: the sources total, the uses total, and the gap, never the stored status code. If the
sources and uses do not balance, add an Analyst Note under the table naming the gap.

If the funded term loan, equity, or purchase price appears at two values across the pages read, show the Deal Summary
figure as stored and add an Analyst Note naming both values and where each came from. Do not choose between them.

If the dashboard's Fact Restatements table lists a figure that appears in these tables, show the stored figure and
add a shaded Analyst Note under the table naming the restated value.

---

## Pricing & Terms

Render the Debt Facilities section of the Deal Summary dashboard as one table, with facilities as columns and terms as
rows, in the order of the stored facility cards. Put each facility's ranking from its summary tag in its column heading,
for example "Term Loan B (first lien)". Do not add a ranking row. With six or more facilities, split into one table per
lien group and repeat the term rows in each.

Rows, in this order, using the dashboard's own term fields: Size (where two cards carry the same term under different
labels, such as Commitment and Facility size, use the first facility's label), Drawn at close, Maturity, Margin, Margin
step-down, Floor, Margin step-up, Amortization (merge Amortization and Repayment profile), Fee, Excess cash flow sweep,
MFN, Financial covenant, Security, OID / call protection. Omit a row where no facility shows a value. Add a row for any
other stored term that at least one facility shows and that bears on the credit read, such as a margin ratchet.

Reading across a row: where a facility's value equals the first facility's, write "Same as" and the first facility's
short name. Where every facility has the same value, merge the cells into one and add "(all facilities)". Write n/a
where a card does not show the term. Where a term is not disclosed and matters to the credit read, such as pricing,
write "Not disclosed" in that cell.

Keep cells to about 30 characters per line. Split long terms across rows (margin, step-down, floor, step-up), and move
conditions to numbered notes under the table, marked "(note n)" in the cell. If a covenant is listed against a facility
but the agreement applies it to another facility only, say so in a note. Do not add terms from outside the dashboard and
do not infer a market-standard term. If no financing structure has been proposed, say so once in a single line instead
of the table.

---

## Sponsor & Management

Take the management table and flag from the Management section of the Business Overview dashboard: roster with name,
title, tenure and background, plus its critical-gap callout where one exists. Do not carry its Contributions field.
Take the sponsor line from the Management / Sponsor lens of the Credit Assessment and the value creation thesis in
the Business Overview strategy section, labeled sponsor-sourced where the sponsor cites its own record. Do not
search the analysis for this section. Put the critical-gap callout in an Analyst Note under the table; delete the
note if there is none.

---

## Business Overview

Source this section from the Business Overview dashboard, reading Company Summary, Revenue Composition, Business
Model, Products Services, and Customers Markets. Use the earlier search only if the dashboard is not generated.

Write four parts in this order:

1. What the company does and its scale: one paragraph of three to four sentences covering what it makes and sells,
   who buys it, how it reaches customers, revenue and margin scale, and the transaction context, such as a
   carve-out. For EBITDA and leverage, use only the figures resolved in Sources & Uses and Capitalization, never the
   dashboard's own EBITDA figures.
2. A product line table with product line, revenue, percent of revenue, and market position.
3. A revenue cuts table with one line each for end market (life cycle view), vertical (line of business, or audited view only where the source states one), geography, and
   sales channel. Keep the cuts separate and never merge them into one hierarchy.
4. Revenue quality and credit read: one paragraph on how much revenue is aftermarket versus project-based, how much
   is contractually committed versus backlog or repeat ordering, customer concentration, and the two highest-ranked
   vulnerabilities, each with its figure.

Spell out every industry acronym on first use. Label company claims about its own market position as
sponsor-sourced. Never refer to the dashboard, the vault, or the record in the document text. Do not copy the
dashboard's summary sentences. If the dashboard disagrees with itself or another source on a figure, apply the flag
rule from Sources & Uses and Capitalization.

---

## Industry

Source this section from the Industry Analysis dashboard, reading Overview, Market Structure, End Markets, Growth
Drivers, and Threats. Use the earlier search only if the dashboard is not generated.

Write five parts in this order:

1. The market: one paragraph covering what the industry is, market size and year, historical and forecast growth,
   and the fastest and slowest growing segments with their rates.
2. A scorecard table with the dashboard's four verdicts exactly as stored: Growth trajectory, Stability through
   cycles, Pricing power, and Structural change risk, each with its stat line.
3. Structure and competition: two to three sentences on fragmentation, the larger incumbents, and the basis of
   competition.
4. Cyclicality: the stored verdict and cycle position, which demand is deferrable and which is not, and the backlog
   or secured revenue evidence. Where the dashboard says a figure is not determinable, say so once in this sentence and do not choose a position.
5. The top three risks as a numbered list, one line each, then one or two sentences on what the industry picture
   means for repayment.

Add one line under the section if the market sizing comes from sponsor materials rather than independent sources.
Keep sponsor claims about the company itself in Business Overview. Follow the same rules on acronyms, source
references, summary sentences, and conflicting figures as in Business Overview. Do not close with a verdict or a
general takeaway the facts above do not support.

---

## Sponsor Projections

Render from the Projections section of the Financial Analysis dashboard, as stored. One table with Entry (its first
period) followed by one column per forecast year, using its period labels. If the model runs longer than seven
forecast years, show the first seven and state in the source line how many years were omitted. Rows in this order
with the dashboard's own labels: Revenue, Revenue growth, Adj. EBITDA, EBITDA margin, Capex % of revenue, Levered FCF
available to repay debt, Net debt / PF Adj. EBITDA, Total debt / PF Adj. EBITDA, PF Adj. EBITDA / net interest, one
balance row per funded tranche, and Cumulative % of opening debt repaid. Never recompute, and leave a missing cell blank. If both sponsor and lender cases exist, do not blend them. Label which one is shown. State the
dashboard's paydown assumption in the line under the table. Take the two or three sentences on how leverage and
paydown move from the dashboard's own commentary. Do not add a conclusion of your own.

**Cumulative Debt Repaid caveat (required):** this row reflects whatever amortization or sweep mechanic is already
in the model. It is not confirmed to be a literal 100%-sweep case. It can be negative in early years if acquisitions
are debt-funded faster than amortization reduces the balance. State the caveat plainly and do not assume a
monotonic paydown shape.

If no structured projection record exists, omit the section and surface the absence once in Open Diligence Items. Do
not build the table from narrative prose.

---

## Merits & Risks

Pull directly from the Merits & Risks dashboard. Render a two-column table with the top 3 merits and top 3 risks,
each numbered 1 to 3 at the start of the cell in the dashboard's own order. Each column is ranked on its own. A merit
and a risk in the same row are not paired, and the line under the table says so. Render each item's Title as stored, with source-index brackets removed. Do not add the Stat Line, Body, or Mitigant
text. Full mitigant text stays in the source dashboard. A risk's mitigant can be disclosed as "none", which is a more severe finding than "limited" and
should be treated that way if it surfaces elsewhere.

---

## Key Focus Areas

Source from the Diligence Focus Areas synthesis (call #16), identified by its Focus Area Count header. Find the answer
by search, read the question id off the result, and fetch the whole answer with `analysis_get_question`. Never build
the list from search excerpts. Render the
first 5 to 7 items in its own rank order as a plain numbered list: the focus area, then its credit mechanism
sentence as stored. Do not write, reword, re-rank, or add items. If the synthesis is not available, omit the section, tell the user in chat, and do not build a substitute. A management flag stays in its own Analyst Note and does not
generate an extra item.

---

## Open Diligence Items

Source from the Open Data Gaps register (call #10), identified by its Gaps Identified header. Find the answer by
search, read the question id off the result, and fetch the whole answer with `analysis_get_question`. Never build the
list from search excerpts. Leave out any gap that
matches a Key Focus Areas item by topic. Render the first 10 remaining HIGH items in the register's own order, in full (topic, source, description,
diligence ask). Then state how many further HIGH items and how many MEDIUM items the full register holds, and that they
are not listed. Omit LOW items. Add any staleness note.

**Missing documents.** Judge absent documents (call #2) against the deal's stage. A Pre-Term deal, or one that cites only a
lender presentation or term sheet, is not expected to have an executed credit agreement, so its absence is not a gap.
List a missing document only when its absence limits a specific part of the credit read, and name what it limits. Do
not list a document the register already asks for. If the register is not available, omit the section and tell the user in chat.

---
