# Output structure

Read this in full before drafting. `assets/Earnings_Quality_Template.docx` shows the layout, `layout-spec.md` has
the exact values, `language-standard.md` governs every sentence and `source-map.md` governs what is read.

## What the output is

A credit analyst's dig into the quality of revenue and EBITDA, built from Raven's stored reads. It extends the
earnings quality lens of the credit assessment and does not restate each underlying read. The analytical unit is a
comparison: what history shows, what the projection assumes, what the benchmark says, and what would have to be
true. Do not select an underwriting case, modify assumptions, re-derive adjustments, rebuild the model or
recommend a structure.

## Length

Body (everything before Appendix A): up to 12 pages, no minimum. Appendix A: up to 3 pages. If the draft runs
over, cut in this order: tables beyond two per section, table rows that repeat the bullets, then bullets. Never cut
the Executive Summary, Forecast Credibility or Priority Diligence Questions.

## Profile (top of page 1)

A four-column table: project and company; sponsor and sector; anchor period and EBITDA basis; projection source
and period; peer set status; lowest data confidence among the reads; reads missing or empty; stored reads as of.
Then the Analyst Note and the terms line.

**Analyst Note** (one to three sentences, only when a trigger applies): history and projection are on different
EBITDA bases; a read is empty or missing; two reads conflict; a stored read is stale.

**Terms line** (small grey type): define EBITDA and any basis labels used; state the units; explain that
"appears" and "suggests" mark Raven's inference; explain page references and D numbers.

## Sections, in this order

Number the sections 1 to 5 in the order below. Number each table by its section (Table 2.1, 3.1) and the appendix
tables Table A.1 and A.2. Except for the Executive Summary, each section opens with a one-line conclusion and
figure, then runs 4 to 7 bullets, ends with a grey Basis line (source documents as the stored reads cite them;
derived D numbers), and then shows at most two supporting tables. Each material bullet states what the stored read
shows with its figure and period, then why it matters to a lender (earnings sustainability, liquidity or downside
exposure), in at most two sentences, with no sub-bullets and no bold run-in labels. Revenue Quality and EBITDA
Quality group their bullets under plain-noun subheadings (for example Margin, Cost structure, Cash conversion and
reinvestment); each subheading carries one to three bullets, and the section keeps its total of 4 to 7 bullets.
Discuss a credit assessment lens in a bullet only where this review's comparison differs from it, and say why.

1. **Executive Summary.** Half a page at most, about 120 words. A one-sentence conclusion on revenue and EBITDA
   quality and forecast credibility, then three bullets of one sentence each, each with its key figure. No
   questions: Priority Diligence Questions appear only at the end.
2. **Revenue Quality.** What drives revenue and how durable it is: growth and mix, price against volume where the
   reads show it, retention and churn by product, customer concentration, contract visibility, and the competitive,
   barrier and industry evidence that bears on durability. Cite the credit assessment ratings for Business quality,
   Customer concentration and Headwinds and tailwinds in the table note, by lens name and rating only. Table:
   revenue and retention by period.
3. **EBITDA Quality.** What the EBITDA is made of and how sustainable it is: margin on one basis, gross margin,
   cost lines and cost position against competitors, peer margins where a peer set exists, cash conversion
   (each measure labeled by its formula, with what it includes and excludes) and reinvestment, and what is structural against temporary. Cite the credit assessment ratings for Earnings quality
   and Cash flow durability in the table note, by lens name and rating only, and report the add-back load the
   stored reads give without re-deriving it. Table: margins, EBITDA and reinvestment by period.
4. **Forecast Credibility.** The signature section. See the rules below.
5. **Priority Diligence Questions.** A plain numbered list of up to six questions most likely to affect revenue or
   EBITDA quality, liquidity or the transaction. Each names the figure or read it comes from. A missing or empty
   read becomes a question. No framing, no ranking, no editorializing.

- **Appendix A: Inputs and Conflicts.** Starts on a new page; see below.

## Forecast Credibility

Open with the one-line conclusion, which states whether the forecast looks reasonable, aggressive or conservative
and the comparison behind that judgment. Then the comparison table (Table 4.1) with these columns: Metric,
Historical result (with period and basis), Projection (with period and basis), External benchmark (peer, industry
or competitor, with source read), Departure, and What would have to be true. The rows are fixed: revenue growth,
gross margin, EBITDA margin, the major cost categories, and each assumption the projections list under key
assumptions. Where the projections assume acquisitions, add rows for base-business growth, total growth and
acquisition cadence and cost, and for any run-rate or pro forma add-on carried into projected earnings. A cell
the stored reads do not carry reads "not in the stored read".

Departure takes one of five values: **Historical** (departs from the historical result), **Peer or industry**
(departs from the benchmark), **Unsupported** (the stored reads give no support for the assumption), **Not
testable** (the stored reads do not carry the figure needed), or **None**. A projection that departs from any one
of history, peers or industry is flagged. Not every departure is a problem; say where a departure is explained by
the stored reads.

A peer figure goes in the benchmark column with the peer's name and how it was derived; with fewer than two peers,
say no median exists.

Where a projection includes acquisitions, do not set an ending acquired-earnings figure against purchase
consideration or acquisition cash as if they covered the same thing, because the ending figure may include growth
after closing. State each figure as stored and say what it covers, and ask whether modeled consideration,
financing and acquired earnings reconcile deal by deal or year by year. Do not describe a difference as a funding
shortfall.

Then 4 to 7 bullets: the largest departures first, each with its figures, the comparison and what would have to be
true; then any contradiction between reads (a stored verdict or lens reading that sits against a projected
assumption) and what would resolve it. If the historical and projected series are on different bases, the first
bullet says so.

## Appendix A: Inputs and Conflicts

Table A.1, the inputs register: read (by topic, never by tile or section name), period covered, basis, data
confidence and date, one row per read, including reads that were empty or missing. Table A.2, differences between
reads, with a Type column and then: item, the first read's value, the second read's value, difference or note.
Show both values and do not choose. Type takes one of three values:

- **Numerical conflict:** two reads give different values for the same measure, period and basis.
- **Definition or period difference:** the figures differ because the basis, denominator or span differs.
- **Contradiction between reads:** one read's verdict or assumption sits against another's.

If there are no differences, say so in one sentence.

## Derived figures

Every derived figure has a D number cited in the text and a live formula in the workbook. The Derived sheet marks
each row with a Type: **Calculation** (arithmetic on stored inputs only) or **Assumption-dependent** (the result
depends on what an input covers or on the basis it uses). Every Assumption-dependent row carries a Caveat saying
what it depends on; an acquisition value calculation states the possible inclusion of post-closing growth. Group related figures
under one number (D4a, D4b). Cite the group in the text (D4). Recalculate the workbook, confirm no errors, and
confirm each figure in the document matches its row before delivery.

## Delivery

1. Build the Word document from the content file and the builder (`layout-spec.md`).
2. Build the derived-figures workbook from its template.
3. Reply in chat with a short summary: what the reads show in at most six lines, the forecast departures, the
   reads that were missing or empty, the page count, and any conflicts between reads. Name the files.
4. The document never names the platform, tiles, sections, prompts or tools. Where attribution to the analysis is
   needed, say "Raven's analysis".
