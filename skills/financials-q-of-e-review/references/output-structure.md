# Output structure

Read this in full before drafting. It defines the document. `assets/Q_of_E_Review_Template.docx` shows the
layout; `layout-spec.md` has the exact values; `language-standard.md` governs every sentence.

## What the output is

A credit analyst's reading of the report. It is not a condensed copy of the report and not an underwriting
recommendation. The analytical unit is a finding: what the report shows, what it means for the earnings, and what
it leaves open. Do not recommend a structure, set an earnings basis for underwriting, or draw leverage or
covenant conclusions in the body.

## Length

Body (everything before Appendix A): up to 12 pages, no minimum. Appendix A: up to 3 pages. A thin report gives a shorter
document; do not pad. If the draft runs over, cut in this order: tables beyond two per section, table rows that
repeat the prose, charts, then sentences. Never cut the Executive Assessment or Open Items.

## Report profile (top of page 1)

A four-column table: project and company; provider, side and client; report title, date and draft status; periods
(including whether a TTM or year-to-date period exists); audit status by period; reliance and exclusions; the direction of the provider's own adjustments (raised, lowered or unchanged the earnings figure, with the amount).
Then the Analyst Note and the terms line.

**Analyst Note** (one to three sentences, only when a trigger applies): the report is a draft; later documents
change the report (an audit, a closing, a signed agreement); items sit outside the earnings figure; the provider's
own adjustments raised or lowered the figure; the report and another deal document disagree on a figure that
matters. Omit the note when none applies.

**Terms line** (small grey type): define EBITDA and the provider's bracketed or named labels; state that tables are
in USD thousands (K) and the text shows millions to one decimal and thousands as K; explain that "appears" and
"suggests" mark Raven's inference; explain page references and D numbers.

## Sections, in this order

The order is fixed. Number the sections 1 to 9 in the order of the section list. Number each table by its section (Table 2.1, 2.2, 3.1) and the appendix table Table A.1. Depth varies with the report. Each section opens with a one-line conclusion and figure, then
runs 4 to 7 bullets, ends with a grey Basis line (report pages; derived D numbers), and then shows at most two
supporting tables or one chart and one table. Each material bullet states what the diligence established with its
figure and page, then why it matters to a lender (earnings sustainability, liquidity or downside exposure), in at
most two sentences, with no sub-bullets and no bold run-in labels. The unresolved question goes to Open Items, and
the bullet cites its number.

1. **Executive Assessment.** One page at most. A one-line conclusion on overall earnings quality. Then 3 to 5 Key
   Findings as bullets, mixing favorable and unfavorable, each with its figure and why it matters to a lender
   (earnings sustainability, liquidity or downside exposure). Then Priority Diligence Questions as a plain numbered
   list of up to 5, each also appearing in Open Items.
2. **Quality of Earnings.** Who stands behind each layer of the bridge (ledger, acquired ledgers, management,
   sell-side, provider, forecast) and what was tested. The direction of the provider's own adjustments. Items
   outside the figure, per the rule below. Tables: the reconciliation by layer (with the Role column; a provider layer on a different basis, such as billings or cash, takes the role Alternative Basis, is shown beside Adjusted and is never added to it) and the
   adjustments by category with a column for each of the four tests (recurrence, support, economic substance,
   conditionality).
3. **Growth section (conditional).** Include only when the report gives a mechanism separate attention. Title it
   plainly for the mechanism (for example Acquisitions and Roll-Up, New Markets). Cover what grew and at what price
   or ramp, how it enters the bridge, and what is forward and untested. Omit the section otherwise.
4. **Revenue Analysis.** How revenue is earned, what moved it (price against volume), concentration, seasonality,
   backlog and conversion, recognition. Retention: if the business has no repeat customers or the report does not
   measure retention, say so and use the nearest indicators the report does contain.
5. **Cost Base.** What drives cost of sales and overhead, what is fixed or variable, what is passed through, and
   what the margin depends on (cost removals, run-rate items, incentive pay).
6. **Working Capital.** What the measure includes, the bridge from reported to adjusted, the monthly pattern, and
   what the measure hides (restricted cash, timing, extended terms).
7. **Cash Flow and Conversion.** EBITDA-to-cash conversion, capital expenditure, and what the report shows about
   cash generation. Where the report has no cash flow statement, say so once and use the nearest figures.
8. **Financial and Accounting Matters.** The audit or trial balance reconciliation, income statement to net income,
   the balance sheet, debt and debt-like items, restricted and unrestricted cash, contingent consideration, and
   where a carried amount differs from a contractual amount. Also who prepared the numbers, the reliance chain,
   systems, controls and pending standards.
9. **Open Items.** A plain numbered list. No framing, no ranking, no editorializing. Each item names what the
   report does not show, with the key figure in bold, and ends with "Other documents:" followed by "covered" or "not covered".
10. **Appendix A: Differences.** Starts on a new page; see below.

## Items outside the bridge

Classify every earnings item in one of three states.

- **In the bridge:** part of the figure the provider calls its earnings number.
- **Shown but excluded:** quantified by the provider and left outside the figure (illustrative normalizations,
  run-rate, forecast ramp-up, pro forma). Report each beside the headline with its amount and basis, say whether the
  provider performed procedures on it, and never add it to the headline. Do not total excluded items unless the
  provider does.
- **Not addressed:** relevant and not covered. Name it as a gap once, and cite another document if one covers it.

## Labels

Every claim is one of three kinds. **Stated:** the report says it; cite the page in the Basis line. **Derived:** a
calculation from stated figures; it has a D number and a live formula in the workbook. **Inferred:** Raven's
conclusion; mark it in the sentence with "appears" or "suggests". Do not use a bracket label or a table of labels.

## Appendix A: Differences

Compare in three groups: within the report; against the audited statements; against the other deal documents.
Show both values with sources and do not choose between them. Omit rounding differences. The introduction is one sentence naming what was compared and every deal document that was not compared, with the reason, then up to three bullets for the differences that bear on earnings, with figures. Do not leave a document unread without saying so. A table of five columns: item, report, other value,
difference or note, source. Multiples that combine report figures with another document (for example a loan amount
over the report's earnings figure) belong here and nowhere in the body. If no other documents were available, say
the comparison covers the report only.

## Derived figures

Every derived figure has a D number cited in the text and a live formula in the workbook. Group related figures
under one number (D4a, D4b). Cite the group in the text (D4). Recalculate the workbook, confirm no errors, and
confirm each figure in the document matches its row before delivery.

## Delivery

1. Build the Word document from the template and helper module (`layout-spec.md`).
2. Build the derived-figures workbook from its template.
3. Reply in chat with a short summary: what the report shows in four to six lines, the items outside the bridge,
   the number of open items, the page count, which other documents were compared, and any place where Raven's
   stored analysis and the report disagreed. Name the files. Do not offer to save to a Raven sheet.
4. The document never names the platform, the vault, tiles, prompts or prompt IDs. Where attribution to the
   analysis is needed, say "Raven's analysis". Cite documents and pages.
