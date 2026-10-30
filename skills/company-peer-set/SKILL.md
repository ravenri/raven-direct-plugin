---
name: "company-peer-set"
description: "Produces a Word document benchmarking the target against its confirmed public peers, from Raven's stored Comp Analysis. Opens with an Executive Summary bundling the main takeaways from Industry Developments, Peer Insights and Filing Signals, then the benchmarking table with its basis caveats, summarized developments and insights with a Deal note on each, Filing Signals in full, and a Capital Structure table per company. Built from a fixed template and scripts, with length budgets and a pre-delivery check. Never recomputes. Use for peer set, peer benchmarking, peer analysis, how the target compares to public peers, or what peer filings reveal. Not for competitive position, the industry read, or private comps."
when_to_use: "Use for \"peer set,\" \"peer benchmarking,\" \"peer analysis,\" \"how does the target compare to public peers,\" \"what do peer filings reveal,\" or \"public comps.\" Do not use for competitive position or named competitors (Competition), for the industry read (Industry Overview), or for private-company comps."
---

# Peer Set

**When to use.** Use for "peer set," "peer benchmarking," "peer analysis," "how does the target compare to public peers," "what do peer filings reveal," or "public comps." Do not use for competitive position or named competitors (Competition), for the industry read (Industry Overview), or for private-company comps.

Produces the public-peer read as a Word document: how the target screens against its confirmed public peers
on the metrics that are comparable, and what those peers' own filings reveal that the deal documents do not.
The output is always Word, because of its complexity. Chat gets a short summary only (see Delivery).

**This is a stored-read, not an analysis pass.** Raven's Comp Analysis has already assembled the peer table,
the caveats, the median, the filing signals, the insights, the developments and the capital structure. This
skill renders them in the house voice. It never recomputes a figure, re-scores a severity or rating, or
invents a signal. Company facts come only from the dashboards and the analysis answers.

## Assets and scripts

- `assets/peer_set_template.docx`: the layout and style guideline (landscape Letter, Arial, named styles).
- `scripts/extract_comp_export.py`: reads the Word export of the Comp Analysis and writes `stored.json`: the
  benchmarking rows, every facility, the filing signals with their severity and classification, the item
  titles, and the source list. Claude does not retype these.
- `scripts/assemble_input.py`: merges `stored.json` with `authored.json` (the judgment fields Claude writes)
  and proposes a Source line for each item from the filings it cites.
- `scripts/build_peer_set.py`: builds the document. It enforces the length budgets, requires a source on
  every item, a Deal says line on every Filing Signal, a Deal note on every Peer Insight, and the Executive
  Summary.
- `scripts/check_peer_set.py`: the pre-delivery check. Fix every hard failure before delivering.
- `scripts/render_check.py`: converts the document to page images for a visual check.
- `scripts/authored_blank.json`: the authored file with placeholder text only.
- `references/writing-rules.md`: the language and sentence rules. Read it before writing.

All working files stay in the working folder. Only the Word document is delivered.

## Document order

Title block, Executive Summary, Peer Benchmarking, Industry Developments, Peer Insights, Filing Signals,
Capital Structure.

## What is summarized and what is kept in full

- **Kept in full:** the benchmarking table and its caveats, the takeaways, the data notes, and every Filing
  Signal with its Deal says line.
- **Summarized to the length budgets:** Industry Developments, Peer Insights and the Capital Structure
  narrative. Keep every item and every figure that carries the point. Cut the scaffolding.
- Keep the stored order. Render every item.

## Read the table correctly

Lead Peer Benchmarking with the caveats that apply, in plain terms and never as boilerplate:

1. **Basis.** The target's EBITDA is the deal Adjusted figure, which excludes synergies and pro forma items.
   Peer EBITDA is reported or derived. The comparison is directional, never like-for-like.
2. **Currency.** Peer rows are in their own currency where they differ. Margins and ratios compare across
   rows; absolute figures do not. Never convert.
3. **Leverage.** Public-peer leverage is not a benchmark for a leveraged target. The median is shown as n.m.
4. **Periods.** Say when the target and the peers are on different periods.

Handle defects explicitly in Data notes: a duplicate peer, a half-empty peer row, a derived against reported
EBITDA mix, a median resting on one peer, a units label that does not match the values, and a figure that
differs between two sections. Flag them. Do not silently correct them.

## Peer Insights and Industry Developments

Each item has a body, a Credit implication and a Source line. Peer Insights also carry a **Deal:** note.

- **Credit implication.** Lead with the borrower's own figure from the deal documents, set it against the
  peer evidence, and land the consequence for repayment. A statement, never a question. Where the borrower's
  position is genuinely undisclosed, name the gap.
- **Deal note.** One or two sentences stating where the deal stands on that theme, checked against the deal
  documents. Do not call a theme silent until the documents have been checked. A deal that presents a theme
  favorably is not silent on it; the gap is then the missing peer benchmark.

## Filing Signals

For each signal: the label, severity and classification as stored, then **Deal says**, then **Filings
reveal**. Keep every deal-silent item and keep "The deal documents do not address this" where that is true,
because the silence is the signal. Where the stored Deal says line contradicts the deal documents, correct
it to what the documents report and say so to the user in the chat summary.

## Capital Structure

A short narrative (covenants, comparability, target reference, leverage basis), then one table per company,
target first. One row per facility. Columns: Facility, Outstanding, Rate, Maturity, Security, Key terms.
The date each block is as of goes in its heading. Where the deal team has set a figure that differs from a
stale document figure, use the deal team figure and name it as such in Key terms or the Source line. No
chart, no bars, no timeline.

## Executive Summary

Write it last, after the second read and the final review, from the finished Industry Developments, Peer
Insights and Filing Signals. It bundles the most important takeaways from those three sections into one
page opening.

**Form.** A lead of two or three sentences, then three to five numbered points. The whole summary stays
within 260 words, and each point within 55 words. No bullets, no sub-headings, no tables.

**Lead.** One sentence on what the peer filings show about the sector. One sentence counting the filing
signals the deal documents do not address, using the finished Filing Signals section. End by introducing the
points.

**Points.**

1. Choose the points that bear most on repayment. Rank them by the weight of the evidence across the three
   sections, and favor a theme that appears in more than one section.
2. Each point opens with a short plain statement of the theme, then pairs the peer evidence with the
   borrower's own figure from the same item's Credit implication or Deal note. A point with no borrower
   figure is not ready; either ground it or drop it.
3. Every figure in the summary already appears in the body of the document, with the same value and unit.
   The summary adds no new fact and makes no new calculation.
4. Include one point where the evidence favors the borrower, if the finished sections support one. Do not
   manufacture one.
5. Do not repeat a point's wording from the section it came from. Compress it.
6. Bold the key figures. State ratings only as the stored ratings, never in prose as an extra verdict.
7. Cover each theme once. If two items make the same point, merge them.

**Heading.** The heading is Executive Summary. It is the one section heading that names a function rather
than a noun phrase, and the check allows it.

## Language and rules

Apply `references/writing-rules.md`. In short: American spelling, no em dashes, credit-desk register, no
hype words, acronyms spelled out on first use, key figures in bold, no editorial adjective without a source,
the same fact not stated twice in the same place.

- Headings are plain nouns. No questions, no colons, no "overview" or "assessment" headings.
- No KPI tiles, colored borders, boxes or badges. Tables and prose only.
- Never refer to the system behind the output. Do not write "the vault," "the tile," "the AI summary," "the
  reads," "the run," prompt numbers or source index numbers. Name sources as the issuer and filing, for
  example "Lear 10-K FY2025; Lear 10-Q Q2 FY2026," or as "Deal documents."
- Every item carries a Source line naming the issuer, filing and fiscal period.
- Currency stays in its own stated currency, unit intact.
- No raw source brackets or internal identifiers in the body.

## Project resolution

Use the project in this conversation if known. Otherwise resolve the deal name with `deal_list`. One match,
use it. More than one, list them in a table (Deal, Company, Sponsor, Status, Created) and ask. No deal named,
ask which deal.

## Readiness

Check `analysis_get_status` unless already known. If the analysis is not ready, report the status and stop.

If the Comp Analysis dashboard returns "not available," call `comp_set_get`. A confirmed set that is ready
means the benchmarking has not generated yet; say so. A set that is fetching means the peer filings are
still downloading. No confirmed set means a peer set has to be suggested and confirmed first; offer to start
it. Never invent a peer set.

## Retrieve

1. Export the Comp Analysis dashboard as Word with `dashboard_export(project_id, tile="comp_analysis",
   format="word")`. Download the file from the link straight away, because the link expires in five minutes.
   Run `extract_comp_export.py` on it to write `stored.json`.
2. If the download fails, read the dashboard with `dashboard_get(project_id, tile="comp_analysis",
   detail="full")` and write the same content into the authored file by hand.
3. For the borrower figures used in the Credit implications, Deal notes and Deal says lines, search the
   deal's analysis answers and read the relevant dashboards. Use the deal documents' own figures. Where a
   deal team decision overrides a stale document figure, use the decision.
4. For Deal notes and the second read, search the peer filings with
   `research_search_documents_by_type(document_types=["comp_set"])`.

## Build

1. Read `stored.json` for the item order and the stored text.
2. Write `authored.json`, the judgment fields only, in stored order: the Executive Summary (last), the
   caveats, data notes, row notes and takeaways, a plain-noun label plus the summarized body and Credit
   implication for each Industry Development, the same plus a Deal note for each Peer Insight, a label for
   each Filing Signal (add Deal says or Filings reveal only where the stored text needs correcting), the four
   Capital Structure narratives, an as-of date for each company, and a rewrite of any Key terms the
   assembler marks for rewriting. Bold figures with double asterisks.
3. Run `assemble_input.py`. Review the Source lines it proposes and correct any that do not match what the
   text says. Fix anything it reports.
4. Run `build_peer_set.py`. Fix every length and completeness error.
5. Run `check_peer_set.py`. Fix every hard failure and proofread the headings it prints.
6. Run `render_check.py` and look at the contact sheet. Confirm the tables fit, no table splits badly, and
   the page count is sensible.

## Second read (mandatory, silent)

Before the final build:

1. Verify the peer figures that a takeaway or the Executive Summary leans on against the peer filings.
2. Test each Peer Insight and Industry Development against the deal documents to write the Deal note and the
   borrower figure.
3. Confirm no comparison treats the target's Adjusted EBITDA as like-for-like with peer EBITDA.
4. Confirm no Deal says line was dropped and no stored item was left out.

Findings change the document in place. Nothing is narrated as a process.

## Final review (mandatory, silent)

Read the finished document top to bottom. Check tone (statements, not directives), consistency (a figure that
appears in more than one place matches everywhere, including the Executive Summary), headings (parallel plain
nouns), and readability. Search for the em dash character and replace every one.

## Delivery

Always deliver the Word document. Do not offer a chat render in its place. In chat, give a short summary:
two or three sentences on what the peers show, plus every correction made to a stored line and every upstream
data problem found, so it can be fixed at the source. Do not paste the document into chat. Do not rerun the
deal's pipeline to test.
