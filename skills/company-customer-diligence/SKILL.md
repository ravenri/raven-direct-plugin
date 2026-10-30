---
name: "company-customer-diligence"
description: "'Produces a focused read on a deal''s customer base: who the customers are, how concentrated, why they stay, and where the credit risk sits. Fetches the Customers answer and its child answers whole from Raven''s analysis, reads the Customers & Markets page for its Credit Reads, applies a deal-type entity-scope gate and a mandatory Pass 2 sweep of the primary documents, and renders only what the sources carry, with everything undisclosed collected under Diligence Gaps. Retention is rendered in the frame the business model calls for (NRR, same-store, same-customer, repeat-client). Use for \"customer diligence,\" \"customer concentration,\" \"who are the customers,\" \"customer risk,\" or \"customer base review.\" Not a full business overview.'"
when_to_use: "Use for \"customer diligence,\" \"customer concentration,\" \"who are the customers,\" \"customer risk,\" or \"customer base review.\" Do not use for a full business overview or for supplier questions."
---

# Customer Diligence

A focused, verdict-light read of the customer base: concentration, durability, retention, contracts,
satisfaction and the credit risks that follow. It is deliberately narrower than the Business Overview.

The procedure is here. The layout is in `output-structure.md` and the Word layout guide is
`assets/customer-diligence-template.docx`. Read both before rendering.

## Scope

Customer concentration, retention, contracts, satisfaction, churn and relationship durability. Segments,
products, suppliers, management and cyber belong to the Business Overview and the other deep dives; if
asked for the broader read, say so and point there. EBITDA by customer is out of scope: companies do not
disclose it and a blended margin applied to customer revenue is a fabrication.

## Language

All output follows `references/language-standard.md`: American spelling, credit-desk register, no
em dashes, no hype adjectives, the house banned-word list. Do not expose platform plumbing (no "the
vault," "the tile," prompt IDs, citation IDs). Name sources as the underlying documents or as "Raven's
analysis." Present a finding as a finding, with the figure first.

## Project resolution

Use a project_id already known in the conversation. Otherwise resolve a named deal with `deal_list`: one
match, use it; several, show a table (Deal, Company, Sponsor, Status, Created) and ask; none named, ask.
Skip any call whose result is already in the conversation.

## Step 0: readiness and freshness

Call `analysis_get_status`. If it is not "Ready to view!", stop and report the status. On the first
retrieval that carries a `freshness` block, if `is_stale` is true put one plain line at the top of the
output. If `is_stale` is true while `deal_doc_changed_since_full` is false, surface the staleness and note
the disagreement in Pass 2. If the block is absent, assume nothing.

## Retrieval: one batch, then only what is thin

Confirm these are loaded with `tool_search`: `dashboard_get`, `analysis_get_question`,
`research_search_analysis`, `research_search_documents_by_type`, `get_source_page`.

**Turn 1, all in parallel:**

1. `analysis_get_question` with Transaction Overview (Q100) and the customer answers, fetched whole (nine
   ids, one call): Customers (Q228, the master; it already rolls up concentration, durability, tenure,
   retention and the risk assessment), Customer Losses and Attrition (Q263), Customer Wins and New Business
   (Q264), Net Revenue Retention and Same-Store Growth (Q265), Customer Contract and Commitment Structure
   (Q266), Customer Satisfaction and NPS (Q267), Customer Churn Rate (Q277), Distribution Model (Q270).
   Transaction Overview carries Deal Type, Analysis Subject and Constituent Entities and is small; fetch it
   by id, because a ranked search for it missed on one deal. Customer Profile / End Markets (Q224) and Top
   Customers by Revenue (Q226) are folded into Customers; fetch them only if Customers is thin. IDs are for
   fetching. If an id returns not found, find it by registry name with one search and read the
   `question_id`.
2. `dashboard_get(business_overview_v2, section="customers-markets")` for the page's Credit Reads and what
   the page carries. Use that section id. The id `customers` returns the whole Company Analysis
   dashboard, about five times the size.
3. `dashboard_get(competition_analysis, section="basis-of-competition")` for pricing power, switching
   costs and customer response, including any price and volume bridge.

**Turn 2, only where triggered:**

- **Concentration pivot.** When customer concentration is undisclosed, low or dispersed, fetch Suppliers
  (Q235) and Business Composition (Q203) in one `analysis_get_question` call.
- **Software dashboard.** Call `dashboard_get(software)` only when Net Revenue Retention and Same-Store
  Growth classifies the business as software or subscription; it carries the quarterly ARR and retention
  series. Do not call it on other deals: it returns a full dashboard of mostly undisclosed rows.
- **Thin answers.** `research_search_analysis` by topic, `top_k` 2, three queries at most. Never run a
  fixed sweep: whole answers already hold what ranked searches returned in overlapping, truncated
  fragments.

**Call budget:** about five calls before drafting (status, one answer fetch, the page, the competition
dashboard, and the project lookup if needed), plus the Turn 2 calls that trigger, then Pass 2.

## Sourcing

- Company facts come from the fetched answers and the dashboards. Pass 2 adds primary documents, each
  labeled as a deal document.
- **Credit Read.** Quote Credit Reads verbatim and never write one. A current-format Customers page
  carries one Credit Read for customers. An earlier-format page carries a Status badge, a Credit Read and a
  Diligence Recommendation for each block (Wins, Losses, Retention, Contracts, Satisfaction); quote each at
  the head of its block and use the page's Diligence Recommendations as the ask where they are specific.
  Where the page carries none, say so once.
- **Conflicts.** Where an answer and a dashboard disagree, the answer governs and the conflict is
  reported, never silently resolved. Where two sources state different figures for the same measure,
  show both, flag them, and carry one verify item under Diligence Gaps naming both.
- **Own calculations** are labeled as such, with the arithmetic shown.
- Peer data is labeled as peer data and never stands in for a missing company fact.

## Deal-type gate

Read the Deal Type and Analysis Subject from Transaction Overview; `references/deal-type-conventions.md`
holds the taxonomy. Do not default to LBO.

- Single entity: say so in the Concentration basis row. If the credit sits on one perimeter of several
  (carve-out and parent, OpCo and HoldCo), name the perimeter the figures are on.
- Combined group (a Merger-Combination, or a material add-on that combines two operating businesses):
  every customer figure must be on the combined group. A single-entity table is the wrong scope even
  where it foots to 100%. A label such as "combined" does not make a table combined, and two sources
  agreeing does not confirm scope. Use the combined presentation the documents give; never sum
  constituents. If none exists, show the standalone figure labeled by entity, state the combined
  denominator, check for a shared top customer, and raise the restatement as a HIGH diligence gap on a
  Merger-Combination. Direction is not automatic: a shared top customer keeps combined concentration above
  the naive dilution floor, but whether it lands above or below the standalone figure depends on its share
  of the other entity.

## Retention frame

Net Revenue Retention and Same-Store Growth classifies the business model itself. Render the frame that
classification gives, with its own metrics, and name the frames that did not apply in one line:

- Software or subscription: ARR bridge, gross and net retention, expansion, downsell, churn. Show net
  retention with and without price and one-time migration uplift where the bridge allows.
- Industrial or manufacturer: same-store or organic growth in existing accounts, share of wallet,
  aftermarket attach, repeat orders.
- Services: revenue per account, renewal rate by revenue, cross-sell.
- Consumer or retail: same-store sales, order value, purchase frequency.
- Project or contract-based with repeat clients: repeat-client revenue, backlog rebooking, win-back.

Frames can co-occur across levels (one-time buyers with a same-store footprint metric); render the
footprint frame and add one line that customer-level repeat is not applicable. If the classification and
the Software dashboard disagree, the classification governs and the disagreement is a Pass 2 finding.

## Concentration pivot

A single-customer share above 10% is flagged and above 20% is a high-severity concentration. When
customer concentration is not disclosed, low or dispersed, it is not an all-clear: the credit-relevant
concentration may sit one layer back. Render the axes the fetched answers support, with a figure and a
credit note each: product or revenue type, channel or financing partner, supplier, geography, and payor
for healthcare or government-reimbursed businesses. Show only axes that have data; the rest go to
Diligence Gaps.

## Render

Read `output-structure.md` and render to it.

- **Render only what the sources carry.** A table, row or block with no data behind it is not rendered.
  Anything not disclosed is listed once, under Diligence Gaps.
- **Lead with the position.** The Overview opens with the finding (strength, weakness or mixed) and the
  reason, and connects the blocks to each other. There is no separate Verdict section.
- **No false all-clears.** Never write "no concentration to worry about," "no concern," "clean." State
  presence, absence or non-applicability factually, and where a risk is low on one axis say where the
  analogous risk sits. "Not disclosed" and "not applicable" are findings, not reassurances. Do not call a
  base diversified or sticky without figures, contracts, switching costs, tenure or retention data.
- Keep a customer's own framing: the retention block, contracts and risks follow the business model.
- Concentration is prose plus a clean table, not a bare statistic. Render the page's channel and mix data
  as tables under their true labels (a revenue-type mix is not an end-market mix).
- Never write a Credit Read, and never invent a customer name, share or figure.

## Diligence Gaps

One table, in the Open Data Gaps format: topic, what is not disclosed, why it matters, the ask naming the
document, dataset or call that would close it, and priority. Rate each HIGH, MEDIUM or LOW on this test and
no other: HIGH prevents a credit judgment on a material dimension (leverage, coverage, recovery or
durability of the earnings base); MEDIUM constrains confidence but a judgment can be formed with the caveat
stated; LOW is a completeness item. Carry a rating the source states unless the test clearly gives a
different tier.

- Do not carry a gap that another fetched answer's disclosed figure answers.
- Where the data plausibly does not exist for a business of this profile, say so once as Evidence Base
  Limitations and do not list it as an ask.
- Check the Company page's Open data gaps register. If a customer gap stated as not disclosed on the
  Customers page is missing from it, report that to the user as a data-quality note; do not add it to the
  register's rating.

## Pass 2 (mandatory, separate, reported)

Run after the draft exists. Open the primary documents; do not restate the analysis's summary of them.
Label each finding by where it came from (deal document, peer signal, open search).

1. **One batched document search** for the anchor "not disclosed" items (top-customer share, customer
   count, tenure, renewal mechanics, named lost or at-risk accounts). Customer scorecards, interview
   tables and consultant material can name accounts that the analysis says are not named; check them. If a
   figure is recovered, fold it in and drop the gap. Confirmed once is confirmed.
2. **Cross-check the anchors.** Does the retention bridge foot, and does it tie to reported ARR or revenue?
   Where sources disagree, show the figure flagged with both. On a combined group, confirm the gate fired.
   Pin a load-bearing figure with `get_source_page`. Where a dashboard cites a figure the answers omit or
   contradict, pin it before calling it unsupported, and report it with its stated basis and the conflict.
3. **Test the headline.** Is a retention or uplift figure flattered by price, a one-time migration effect,
   a definition choice (gross versus net, logo versus dollar), or by measuring the most favorable cohort
   first? State the figure without the flattering component and label the arithmetic as your own.
4. **Two open-ended searches at most**, no specific field in mind: what would a careful lender want to
   know about this customer base that the draft does not address. Angles: a customer large enough to be a
   covenant-level event, renewal cliffs, a customer that is also a supplier, competitor or related party,
   concentration by margin, a planned change to the renewal or contract motion during the hold.
5. Report what the sweep found, even if nothing new.

## Rules

- Take a position in the Overview. State the credit consequence of each customer risk.
- Render only what has data; collect the rest under Diligence Gaps.
- Quote the Credit Read; never write one.
- Distinguish "not disclosed" from "not applicable given this business."
- Peer data is labeled and never a substitute.
- Do not attempt EBITDA by customer.
- Pass 2 is mandatory and reported.

## Delivery

Render in chat by default and offer a Word document at the end. When the user wants Word, build it with
the docx skill and follow `assets/customer-diligence-template.docx` for layout and style (a guideline, not
the canonical form), save to `/mnt/user-data/outputs/` and call `present_files`. Offer a Raven sheet only
if `sheet_apply_create` is loaded in the session.
