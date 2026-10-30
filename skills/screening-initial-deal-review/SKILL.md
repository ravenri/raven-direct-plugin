---
name: "screening-initial-deal-review"
description: "Produces the first structured read on a brand-new deal: Sources & Uses, capitalization, pricing & terms, sponsor & management, business overview, industry context, sponsor projections, merits & risks, key focus areas, and open diligence items, plus an initial read drawn from the credit assessment."
when_to_use: "Use when a deal is newly loaded and needs its first pass; when the user asks to screen a deal or wants an initial read, early look, first cut, or pre-diligence credit summary; or when they ask what is known about a deal so far, even without naming Initial Deal Review. Run before the screening memo, credit assessment, or deep diligence. Prefer this over an ad hoc search of the deal's analysis when the request is for a first look. Do not use it when the deal already has an initial review, or for a question about a single topic."
---

# Initial Deal Review

Produces a screening-length first read on a new deal via Raven Direct, delivered as a Word document built with `scripts/build_review.js` (layout and styling follow
`assets/initial_deal_review_template.docx`), with a short summary in chat and a full chat render on request. Each section reads the finished analysis directly and renders it as
stored.

## Output Contract

Before the first data call, read this file in full. This skill defines the output. A reply is complete only when it
follows the template: the Initial Read table first, then the sections in the template's order. Do not answer in free
prose, do not substitute your own credit view, and do not skip a section because the data is thin; render the section
with what is stored and say what is not disclosed. If you cannot follow the template (for example, this session cannot
create the Word document), say so in the first line and render the same sections in chat in the same order.

Before sending, check:
1. The Initial Read table is first, with Screening view, Credit rating, and Repayment read.
2. Every section in the template appears in order, or is removed under the empty-section rule.
3. The deal is named as it appears in the deal list.
4. No section carries a view that is not drawn from the stored analysis.
5. Analyst Notes: every data flag appears as an Analyst Note under the table it affects. A note is required when: a stored
   total does not foot or a balance check fails; the same figure appears at two values anywhere in the review, including
   between the Initial Read and the tables; a percent column does not sum to its stated total; the analysis is stale; the
   Open Data Gaps counts do not match the entries listed; a source section flags a data-quality issue; or Pass 2 changes
   or contradicts the draft. If a trigger applies and the review has no note for it, add the note before sending. A
   review with no Analyst Notes at all fails this check unless you have confirmed that none of the triggers apply and say
   so in the chat summary. Any note you planned or reasoned about during the run must appear in the review, or you state
   in the chat summary why it was dropped.

If any check fails, fix the reply before sending.

A placement preference the user states, such as where the staleness note goes, overrides the template. Follow it and do
nothing else differently.

## Language

All output conforms to `references/language-standard.md`. Read and apply it before writing. The standard's markdown
bold rule for dashboard fields does not apply in the Word document. Source lines cite documents and pages. Where
attribution to the analysis is needed, say "the underlying analysis". Never name Raven, dashboards, the vault, or
records in the document. Remove markdown bold markers, source-index brackets, and number tags such as [[n3]] from stored text. Label each shaded flag "Analyst Note".

## Output and Asset Guidance

The analytical workflow is the same in every interface it is invoked from. The Initial Deal Review asset is a
presentation guide, not a required content schema. It shows the preferred structure and formatting when the
corresponding information is available. Absence of information is not itself an output. Only surface an absence when
it is analytically meaningful.

1. Include a section, table, row, or field only when there is substantive information to populate it. Do not create
   empty sections, placeholder tables, blank rows, or repeated "Not disclosed" fields because they appear in the asset.
2. When information is unavailable and its absence does not bear on the credit read, omit it.
3. When missing information is credit-relevant, state the gap once, concisely, in the most appropriate section or in
   Open Diligence Items.
4. Preserve an explicit "Not disclosed" only when that status appears in the underlying analysis and is useful to the
   credit read.
5. Before treating a material item as unavailable, apply Document Escalation and Pass 2. Sources & Uses,
   Capitalization, and Pricing & Terms are the exception and render as stored.
6. A pipeline status, such as an analysis that has not been generated, is not a deal fact. Keep it out of the
   document and tell the user in chat, once.
7. Never infer or manufacture content to complete the asset.
8. A table in which most cells read Not disclosed is replaced by one sentence naming what is not disclosed. A table is
   kept only if at least half of its cells carry a stored value. This applies to every table in the document.

The document expands or contracts with the information available.

## Project Resolution

- If the deal is already identified from earlier in this conversation, use it directly.
- Otherwise, if the user named a deal, call the deal list with the name filter and read the full result, because the
  filter scans every deal. If nothing matches, repeat once with the company filter. Do not set both. Exactly one match:
  use it. More than one: present them as a table and ask.
- If no deal has been named, ask which deal before doing anything else.

**Skip-if-known (strict):** if the analysis status or any dashboard section below was already
retrieved earlier in this conversation, do not fetch it again.

## STEP 0: Vault Readiness

Check whether the deal's analysis has finished running (skip if already known).
- "Ready to view!" → proceed.
- Anything else → stop. Tell the user the analysis isn't ready, give the current status, and say to
  try again in 15-30 minutes, or to start the analysis from within Raven if it shows Not started,
  Failed, or Aborted. This chat cannot start it.

## STEP 0.5: Staleness Check (separate from readiness, do not skip)

The analysis status only confirms the *last* run completed, not that it reflects the *current*
documents. After STEP 0 passes, check the first dashboard section retrieved (calls #3-5 below) for a
freshness indicator. If it says the data is stale (`freshness.is_stale` is true), surface the warning
plainly at the top of the rendered document, before the Overview, and restate it in Open Diligence
Items. Do not silently proceed as if the data were current. If no freshness indicator came back, add
one line to Open Diligence Items saying freshness of the underlying analysis could not be
confirmed for this run.

**The `freshness` block can be internally inconsistent** (confirmed live, see validation history):
`is_stale: true` alongside `deal_doc_changed_since_full: false` in the same response. Don't try
to resolve the contradiction; surface the warning per `is_stale` (the more conservative signal),
and note the disagreement itself as a Pass 2 finding.

## STEP 0.75: Deal Maturity Check

A deal is Pre-Term when no financing structure has been quantified. Treat it as Pre-Term if any of these is true: the
Deal Summary and Credit Assessment did not generate; or the Deal Summary shows no amount for any tranche and no sources
and uses total; or the Sources and Uses answer states that no sources and uses is disclosed. A tile that generated with
every amount shown as NA or Not disclosed counts as not generated for this purpose. Use the results of calls #3, #5 and
#9; no extra calls are needed.

On a Pre-Term deal, say once, in the Overview, that no financing has been proposed, and omit Sources & Uses,
Capitalization, Pricing & Terms and Sponsor Projections. Do not render tables whose cells are all Not disclosed. Open
Diligence Items still lists the financing gaps the register holds.

## Tool Pre-Load

Before issuing the batch below, make sure the Raven tools for deal overview, document listing,
dashboards, and whole-answer fetch (`analysis_get_question`) are loaded, with analysis search loaded for the title-check fallback.

## Currency

Render every figure in the deal's own stored currency, unit intact. Never assume USD or convert.
Carry period labels (LTM date, FY, PF-at-close) as stored.

## Tile Self-ID Fields Are Not Always Reliable

A dashboard response's own internal `Deal` field can occasionally be wrong, seen once,
naming a different deal entirely, not just differently formatted (see validation history; not
established as a frequent issue, just a real one worth guarding against cheaply). Use the deal list's
name for the header always, it's never wrong, so there's no cost to preferring it regardless of
how often the tile field actually breaks.

## Sourcing discipline vs. analytical judgment

**Render, don't second-guess:** anywhere the vault has already made the judgment, Credit
Assessment's lens ratings, `merits_risks`' severity and mitigant classification, the open-data-gaps
register's priority ratings, the sources-and-uses record's balance-check verdict. Distill and
present accurately; don't re-derive, soften, or override because something looks off, flag it in
Pass 2 instead.

Verification protocols elsewhere in this skill (staleness, Coherence Notes, Callouts, Fact Restatements) exist to catch inconsistency *in Raven's own generation*, not to make Claude second-
guess its own reading of a document once it gets there, trust a clear primary-document answer.

---

## Document Escalation

Where the dashboards leave a figure unavailable or a section thin (Sponsor & Management, Business Overview,
Industry), documents are a real second tier: read the document's text, or search documents by type, before treating it as
unavailable. This does not apply to Sources & Uses, Capitalization, or Pricing & Terms, which render as stored.
Pass 2 step 1 applies the same check to every material gap.

## Confidence Carry-Through

If a source tile exposes its own confidence signal (e.g. `Data confidence: MEDIUM`) or a
thin-evidence note, carry it into the write-up, "PF Adj. EBITDA of $X (confidence: medium, pending
QoE)" rather than presenting every figure with equal certainty. Never invent a confidence level
where none is stated.

---

## PARALLEL BATCH: issue all in one turn, in parallel, skip any already known

Issue every call below in a single turn, in parallel. Do not wait on one before issuing the next.

1. Deal overview (name, status, basic facts). Don't use its `sponsor` field (unreliable, often empty); use the Cover Block
   Sponsor rule instead.
2. List of uploaded documents. Judge absent documents against the deal's stage, as set out in Open Diligence Items.
3. Deal Summary dashboard (whole dashboard): its Sources Uses, Debt Facilities, and Fact Restatements sections feed
   Sources & Uses, Capitalization, and Pricing & Terms. The header carries Sponsor. Check `freshness.is_stale` and any
   `Callouts` field.
4. Financial Analysis dashboard, Projections section only: feeds Sponsor Projections.
5. Credit Assessment dashboard: feeds the Initial Read (Call, Preliminary Screening View, Governing Conditions) and the
   Management / Sponsor lens. Check its Coherence Notes; an absent Coherence Notes field is a mild positive, not
   incomplete data.
6. Business Overview dashboard (whole dashboard): feeds Business Overview, plus the Management and Strategy sections for
   Sponsor & Management.
7. Industry Analysis dashboard (whole dashboard): feeds Industry.
8. Merits & Risks dashboard: feeds Merits & Risks.
9. One whole-answer fetch (`analysis_get_question`) of these six registry answers together: Transaction Overview,
   Sources and Uses, Transaction Background, Deal & Party Identification, Open Data Gaps, and Diligence Focus Areas
   (question ids 100, 102, 105, 106, 2100, 2101).

Uses of call #9:
- Transaction Overview feeds the Overview.
- Sources and Uses is the fallback for the Sources lines, used only if neither the Sources Uses section nor the Cap
  Table lists them.
- Transaction Background supplies the seller and prior ownership.
- Deal & Party Identification supplies the Cover Block Agent and the sponsor group, including any second sponsor not in
  the #3 header. No single dashboard's Sponsor header is reliable on multi-sponsor deals. If a second sponsor appears,
  list both.
- Open Data Gaps feeds Open Diligence Items.
- Diligence Focus Areas feeds Key Focus Areas.

**Title check.** Before using any answer from call #9, confirm that its question title matches the expected one. If an
answer is missing or its title does not match, run one search for that answer by its header, read its id off the
result, and fetch it whole. Never build a register or list from search excerpts.

**Truncation.** If the response reports that an answer was truncated, fetch that id alone and use the complete text. Open
Data Gaps is long and can be cut when fetched with the others.

---

## Section Specifications

Before drafting, read `references/section-specs.md` once. It holds the rules for each section of the review, in render
order: Cover Block, Initial Read, Overview, Sources & Uses and Capitalization, Pricing & Terms, Sponsor & Management,
Business Overview, Industry, Sponsor Projections, Merits & Risks, Key Focus Areas, and Open Diligence Items. Apply them
exactly, and do not draft a section from memory of this file. The Output and Asset Guidance above governs absence in
every section.

---

## PASS 2: Exploration Mandate (mandatory, separate step, not a mindset for Pass 1)

Run only after Pass 1 produces a full draft, not folded into it (a "keep this in mind throughout"
version of this has failed before, see validation history).

**First wave.** Issue the Pass 2 searches in a single parallel turn, with a cap of four.

**Follow-up wave.** If a first-wave result contradicts an anchor fact or surfaces a material gap, one follow-up wave of
up to three searches is allowed. Do not run a third wave.

The checks:

1. For every material information gap that affects the credit read or may become a diligence item, one targeted
   document search (searching documents by type, or reading the document's text) to confirm it is a real gap, not a
   routing miss. Confirmed once is confirmed, don't re-query hoping for a different answer.
2. For every anchor fact (PF Adj. EBITDA, entry leverage, purchase price, total debt), confirm the figure matches
   across the dashboards read and check it against the Fact Restatements table.
3. Include 2-3 genuinely open-ended searches in the first wave, no specific field in mind, "what would a careful lender
   want to know that nothing in the draft addresses yet." This catches what routing couldn't have
   anticipated, by construction.
4. Re-read the draft's own Open Diligence Items for one gap a quick search could actually close.

**Report what Pass 2 found in chat after the review, even if "nothing new."** No report means Pass 2
didn't happen, regardless of how complete the draft looks.

---

## Rules

- All figures are stored reads. Never recompute leverage, EBITDA, or projections.
- Never invent a figure or citation. No stored value: leave it out. Surface the absence only when it is credit-relevant.
- The figure-discipline rule (Overview) is the one exception to "render what's
  stored", it withholds only figures still genuinely unresolved at runtime.
- When a source has already self-disclosed a data-quality issue (footing gap, staleness, a
  Coherence Note, a Callout), render that disclosure, do not silently correct, re-derive, or omit
  it.
- **Don't be too rigid about "one call, done."** The batch above is a starting point, not a
  ceiling. If a call's answer is clearly thinner than what the vault actually holds, a follow-up
  call to that specific source is the right move, not a deviation from the spec.

- A table row with no value in any column is removed. If the row is required to read the section, say in an Analyst Note
  that the figure is not stored.
- Never print a system status value (for example a balance check code). State the sources total, the uses total, and the
  gap in words.
- The Source column in Open Diligence Items cites documents and pages, or the register category when no document is named.
  Never print a question id or prompt id.
- If the Open Data Gaps header counts do not match the entries listed beneath it, show the counts from the entries, and
  add an Analyst Note stating both sets of counts.

---

## Delivery

Default: build the Word document with `scripts/build_review.js`, using the content from Pass 1 and Pass 2. Make the chat reply a short summary: the Initial Read table, the Analyst Notes, the Pass 2 report, and the link
to the file. Render the full review in chat only if the user asks, following the structure of the template: the asset's
tables as markdown tables, each shaded note on its own quoted line beginning "Analyst Note:", and a source line in
italics under each table.

To build the Word document: write the review content as a build-input file kept in the working folder, run
`scripts/build_review.js` on it, and check that the file opens and renders before presenting it. Build once. Do not
re-run any source call or Pass 2 to build it. The script follows the template's layout and styling: page size, margins,
font, table header shading, Analyst Note shading and footer. The template is a guideline for layout and style, not the
canonical form. Label the vertical row "Vertical (line of business)" unless the source states an audited view. If this
session cannot create files, say so and render the review in chat.

If your environment produces a canvas or markdown document instead of a Word file, build the same sections, tables,
Analyst Notes, and source lines there. Layout is the renderer's. Every content rule and the Output Contract still apply.

## Layout

Word document format: portrait, 5 to 6 pages. The title Initial Deal Review sits at the top of page 1, with no logo or
branding. Everything is black text with plain gray table headers and no colored section bars. The page and portrait
rules apply to the Word document only.

Sections in this order: Cover Block, Initial Read, Overview, Sources & Uses and Capitalization, Pricing and
Terms, Sponsor and Management, Business Overview, Industry, Sponsor Projections, Merits and Risks, Key Focus Areas,
Open Diligence Items.

Tables: Cover Block as a two-column table. Initial Read as a two-column table. Sources and Uses as two side-by-side tables, with the capitalization table
directly below. Pricing and Terms as one table with facilities as columns and terms as rows, with numbered notes underneath. Management as a table. Business
Overview with a product line table and a revenue cuts table. Industry with a scorecard table. Projections as Entry
plus one column per forecast year. Merits and Risks as two numbered columns. Open Diligence Items with high-priority
gaps in a table and medium-priority gaps as a short list.

Prose: the Initial Read is its table, the Basis text, and a numbered list of governing conditions. The Overview is
one short paragraph. Business Overview and Industry follow the parts set out in their sections. Key Focus Areas
is a plain numbered list.

Every table has a source line underneath. Any data flag appears in a shaded Analyst Note under the table it affects.

The second-pass review notes go in chat after the review, never in the review itself. Anything from them that changes
the review appears in an Analyst Note or in Open Diligence Items.
