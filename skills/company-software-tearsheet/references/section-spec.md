# Section specification

Read once before assembling. Registry names are the reference; IDs are for retrieval only and must never appear in
the document.

## Reading map

| Section | Software tile | Answers (registry name, ID) |
|---|---|---|
| Header and business | business-model | Company Summary (Q200); Customer Profile / End Markets (Q224) |
| Revenue model | business-model | Revenue Model & Software Revenue Streams (Q2009); Revenue Stability (Q607) |
| Market position and barriers | business-model | Competition Summary (Q500); Market Position (Q502); Barriers to Entry Summary (Q300); Switching Costs (Q327) |
| AI exposure | business-model (product and delivery) | AI Adoption & Deployment (Q274); AI Strategy and Risk (Q262); AI Operational Threats (Q276); AI Sector Exposure & Use-Case Map (Q431, optional) |
| Customers and contracts | business-model | Customers (Q228); Top Customers by Revenue (Q226); Customer Losses and Attrition (Q263); Net Revenue Retention and Same-Store Growth (Q265); Customer Contract and Commitment Structure (Q266) |
| Financial summary | financials-metrics | Cost Structure (Q618); Gross Margin Trends (Q614); Unlevered FCF Conversion (Historical) (Q635); Capex (Q632) |
| Key metrics | business-model, financials-metrics | The answers above; Canonical Period Anchors (Q2401) and EBITDA Layer Catalog (Q2403) for period and EBITDA labels |
| Transaction table (only when the deal has facilities) | none | Sources and Uses (Q102); Capitalization Table (Q1160) |
| Open diligence | none | Drawn from the key issues and the metrics marked Not disclosed; Open Data Gaps (Q2100) only when the user asks for the full list |

## Header

Company name, "Software tearsheet", and one line giving the project, units, the period convention (actuals
unless marked B or P) and the EBITDA basis, given as the layer title from the EBITDA Layer Catalog only; the build-up
belongs in the Financial summary. Under it, one italic line:
application, delivery, customers, revenue. Where the deal has facilities, add a compact table: facilities,
sponsor equity, total capitalization and leverage as stated. Say total capitalization, never enterprise value. Where
there is no financing in the materials, omit the table and say so once.

## Sections

1. **Business.** Two short paragraphs. First: what it does, who buys it, how it is delivered and where it operates.
   Second: scale (clients or users, revenue, adjusted EBITDA and margin, each with its period) and what supports
   revenue visibility.
2. **Revenue model.** A table of revenue by stream using the company's own stream names, with the periods the
   documents give and each stream's share of the budget year or anchor period. Carry recurring and non-recurring
   totals when stated; up to eight rows, compact. Where the revenue model answer already tabulates streams with
   shares, use its rows as stated. One paragraph on what is committed and what is
   transactional, pricing structure, and the credit implication. Never force streams into standard buckets.
3. **Market position and barriers to entry.** One paragraph on position (share if disclosed, prime or
   subcontractor standing, where the company is absent or nascent, IP and supplier dependence, peer-filing
   findings). Then a barriers table using the stated dimension verdicts, naming the stated overall verdict.
   Switching costs appear only as the stated answer states them; if unquantified, say so.
4. **AI exposure.** Status (what is released, in prototyping or planned, with stated dates and amounts), threat and
   opportunity as the stated answers state them, a table of exposure against most exposed revenue, and a sentence on
   evidence limits. Never infer an effect on bookings, pricing or margin that is not stated.
5. **Customers and contracts.** Two narrative paragraphs (composition and concentration; tenure, wins and
   losses), a facts table (clients, top five, largest client, backlog and pipeline, renewals, retention,
   satisfaction), a contract structure paragraph, a table of revenue by named client when stated, and the
   credit implication. Show any reconciliation gap.
6. **Financial summary.** A table of actuals only (revenue, growth, gross margin, adjusted EBITDA, margin), a
   paragraph that places any budget or projection in a sentence, and the credit implication.
7. **Key issues.** Step 4 of the skill, up to six rows: issue, type, evidence, credit implication.
8. **Key metrics.** The fixed set below, in three groups, with company value, how measured and reference range.
9. **Open diligence.** One line of the asks the gaps imply.

## Key metrics set

Revenue quality and growth: revenue line analysis; ARR; billings and bookings; professional services mix.
Customers and retention: gross retention and churn; net dollar retention; ARR up for renewal; client
concentration; SMB exposure. Profitability, efficiency and cash flow: gross margin; adjusted EBITDA margin; Rule of
40; sales efficiency (LTV to CAC, CAC payback, magic number in one row); cash conversion.

Formulas and ranges come only from `software-metrics-reference.md`. Company values are stated values with period
labels. Show "Not disclosed" where absent, and name any substitute the company does disclose (backlog for bookings,
training for professional services). Show a reference range only when it applies; ranges tied to an ARR band apply
only when ARR falls in the band. Where the range's basis differs from the stated figure (top 10 against top 5), say
so in the How measured cell.

## Adapting to what the deal discloses

- **ARR disclosed:** ARR and retention rows as stated; annual and quarterly series when stated.
- **No ARR (public or seller materials):** use subscription revenue and remaining performance obligation, with the
  next-twelve-month portion, as the recurring measure; state that ARR is not disclosed.
- **Older deals:** omit any block whose answer is missing; list it once under Open diligence.

## Table formatting

Header rows are filled a light blue-gray with bold navy text and a navy rule beneath. Total and subtotal rows (for
example recurring total, non-recurring total, ending retention) are shaded one step lighter, bold, with a darker rule
above. Group rows in the key metrics table use the same lighter shade. Key lines in the financial summary (revenue,
adjusted EBITDA, anchor EBITDA layer) are bold without shading. Numbers are right-aligned, and USD MM tables show one decimal throughout. No colored borders, no
badges, no zebra striping.

## Large deals and long answers

Where a deal has facilities, many revenue streams or nine barrier dimensions, the page plan flexes: start Market position
and barriers on page 2 when its table would split, keep Customers and contracts and the Financial summary together,
and keep Key issues and AI exposure together. State the basis of any concentration figure (ARR or revenue, with or
without the largest customer) and keep both views when both are stated. Show a sources-and-uses gap that follows a deal
team edit as one sentence under the transaction table. Drop a key issue that repeats a section on the same page rather
than shorten the evidence.

## Page plan

Set a page break before Customers and contracts, AI exposure and Key metrics, and keep each table with the paragraph that
introduces it.

Page 1: header, business, revenue model, market position and barriers. Page 2: customers and contracts, financial
summary. Page 3: AI exposure, key issues. Page 4: key metrics and the open diligence line. Four pages is the cap.
