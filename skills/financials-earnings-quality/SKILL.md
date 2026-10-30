---
name: "financials-earnings-quality"
description: "Use when the user wants to dig into the quality of a company's revenue and EBITDA and how credible its projections are: revenue durability and growth, margin and cost sustainability, cash conversion, and where the forecast departs from history, peers or industry conditions. Extends the earnings quality lens of the credit assessment. Consolidates Raven's stored reads on historical financials, projections, customers, competition, industry, barriers to entry and peers, and delivers a Word document and a derived-figures workbook. Judges whether the forecast looks reasonable, aggressive or conservative; does not select an underwriting case, re-derive adjustments or rebuild the model. Not for a quality of earnings report review, a single-topic read, or the EBITDA anchor and cap table."
when_to_use: "Use for \"earnings quality,\" \"quality of revenue and EBITDA,\" \"how credible are the projections,\" \"cash conversion,\" or \"where does the forecast depart from history or peers.\" Do not use for a review of a quality of earnings report (Q of E Review), a single-topic read, or the EBITDA anchor and cap table."
---

# Financials - Earnings Quality

A consolidator that digs into the quality of revenue and EBITDA. It extends the earnings quality lens of the credit
assessment: it reads Raven's stored analysis only, sets history, projection and benchmarks side by side on the same
basis, and says where the forecast needs more than the record supports. It does not reopen source documents and it
does not review a quality of earnings report (the quality of earnings review skill does that).

## Output contract


Before the first read, read in full: `references/source-map.md`, `references/output-structure.md`,
`references/language-standard.md` and `references/layout-spec.md`. They define the reads, the output and the
page. A reply is complete only when it follows the section order in `output-structure.md`. If you cannot build
the Word document, say so in the first line and render the same sections in chat in the same order.

Before sending, check:
1. The profile table, Analyst Note (only if a trigger applies) and terms line come first, then Executive Summary.
2. Sections follow the fixed order, ending with Priority Diligence Questions and Appendix A.
3. The Executive Summary is a one-sentence conclusion and three one-sentence bullets, about 120 words at most, with no questions.
4. Every other section opens with a one-line conclusion and figure, then bullets. Each material bullet states what the
   stored read shows and why it matters to a lender, in at most two sentences. Revenue Quality and EBITDA Quality
   group their bullets under plain-noun subheadings, with 4 to 7 bullets in total.
5. Every series states its basis and period, and no two series on different bases are compared without saying so.
6. Every derived figure has a D number and a live formula; the workbook recalculates with no errors and matches.
7. Body is up to 12 pages. Appendix A starts on a new page.
8. No platform wording in the document: no tile, section id, prompt or tool name. Cite the source document and
   page that the stored read itself cites, or say "Raven's analysis".
9. Priority Diligence Questions appear once, at the end, as a plain numbered list of up to six.

## Step 0: Project and readiness

- Use the project named in the conversation, or resolve it by name and ask if several match. If several match and
  only one has completed analysis, use that one and say so in the profile table.
- Analysis status must read ready, or stop and report it.
- Load the deferred tools before first use.

## Step 1: Read the stored analysis

Read, as scoped dashboard sections and never source documents, exactly the reads in `references/source-map.md`, in
one parallel batch, and no others. Record the period and the as-of status of each input, and state any difference
in periods before comparing them. If a section is empty or missing, say so once where it belongs and add it to the
questions. Do not search further. Where two stored reads disagree, show both and do not choose. Skip a read already
available earlier in the conversation.

## Step 2: Compare

Before drafting, answer for every comparison: is it on the same basis, the same period and the same denominator?
If not, say so in the row and compare only what is alike.

For revenue growth, gross margin, EBITDA margin and the major cost categories, set the historical result, the
projection and the external benchmark in one row with the credit question each raises. Flag every projection that
departs from any one of history, peers or industry conditions. Classify each as a historical departure, a peer or
industry departure, or an unsupported assumption, and say which; where the stored reads do not carry the figure
needed, classify it as not testable. For each material assumption, state what would have to be true for it to hold.
Judge the forecast as reasonable, aggressive or conservative only by citing the comparison behind the judgment.
Where one stored read contradicts another, state the contradiction and what would resolve it. Report each credit
assessment lens rating as that read's rating, in the table note, and discuss a lens only where this review differs and say why.

Where a projection includes acquisitions, do not set an ending acquired-earnings figure against purchase
consideration or acquisition cash as if they covered the same thing, because the ending figure may include growth
after closing. State each figure as stored and say what it covers. Ask whether modeled consideration, financing and
acquired earnings reconcile deal by deal or year by year. Do not describe a difference between them as a funding
shortfall.

Label every cash conversion measure by its formula and say what it includes and excludes. EBITDA less capex over
EBITDA excludes interest, taxes, working capital, acquisitions and other cash obligations. Operating cash flow over
EBITDA appears to be after interest, taxes and working capital and is before investing flows, including capex and
acquisitions. Neither measures cash left after all obligations. Do not place acquisitions in operating cash flow
unless the stored read does.

A peer figure goes in the benchmark column with the peer's name and how it was derived; with fewer than two peers,
say no median exists.

## Step 3: Derived figures and workbook

Record every stated input with its source and every derived figure as a live formula, from
`assets/Derived_Figures_Template.xlsx`. Recalculate with the spreadsheet skill's script, confirm zero errors, and
confirm each figure in the document matches its row.

## Step 4: Write and build

Write to `references/output-structure.md` and `references/language-standard.md`: a one-line conclusion and then
bullets in every section, key figures in bold, no metaphor or hype words, no em dashes, American spelling, acronyms
spelled out on first use, and "appears" or "suggests" on every inference. Write the content to a content file that
follows `scripts/Content_Template.json` (blocks in document order), then build with
`node scripts/build_from_content.js <content.json> <out.docx>`, which applies the layout in
`references/layout-spec.md`. Read the docx skill first, embed fonts through the helper, validate, render to PDF,
look at page 1 and one table page, and trim to the cap if needed. Before delivery run
`python3 scripts/check_deliverable.py <review.docx> <workbook.xlsx>` and fix every failure. It does not check that
each figure in the text equals its workbook row, so compare those by eye.

## Delivery

Word document and workbook, plus a short chat summary. Open with the findings. No progress narration. At most six
lines for what the reads show, then the forecast departures, the reads that were missing or empty, the page count,
and any conflicts between reads. Do not offer to save to a Raven sheet.

## Boundaries

Interpret only. Do not select an underwriting case, modify assumptions, re-derive adjustments, rebuild the model or
recommend a structure. A judgment on the forecast is a credit judgment, not a case decision.
