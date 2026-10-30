---
name: "company-dd-meeting-prep"
description: "Builds a bespoke diligence list for one deal and turns it into a meeting prep doc (spoken questions for management, an expert call, a customer or owner reference, or an advisor check-in) or a document request list for the sponsor or borrower. The list comes from the deal's own open gaps, failed checks, unsupported claims and status changes in the vault and dashboards, ranked by materiality to repayment, and never from a generic checklist. Use before any diligence meeting or call, or to prepare a diligence request list. Triggers on \"prep for management meeting,\" \"diligence call prep,\" \"expert call questions,\" \"customer reference questions,\" \"diligence request list,\" \"diligence questions for [deal],\" \"meeting prep for [company].\" Do not use for the questions a senior investor would press (Lightning Round Q&A) or an IC-ranked list of open items (Diligence Focus Areas)."
when_to_use: "Use before a diligence meeting or call, or to prepare a diligence request list: \"prep for management meeting,\" \"diligence call prep,\" \"expert call questions,\" \"customer reference questions,\" \"diligence request list,\" or \"meeting prep for [company].\" Do not use for the questions a senior investor would press (Lightning Round Q&A) or an IC-ranked list of open items (Diligence Focus Areas)."
---

# DD Meeting Prep

## Purpose

The deal's own evidence decides what goes on the list: what is not disclosed, what the company asserts without independent support, where sources disagree, and what has changed since a document was written. A fixed checklist never decides the list. It only checks that nothing was missed.

This skill is a script for a live conversation, or a request list sent to the other side. It is distinct from Lightning Round Q&A (what a senior investor would press you on) and Diligence Focus Areas (open items ranked for IC).

## Language

All output conforms to `references/language-standard.md`. Read and apply it before writing. Source lines cite documents and pages. Where attribution to the analysis is needed, say "the underlying analysis". Never name Raven, dashboards, the vault, the platform, records or question IDs in the meeting sheet or request list. Remove markdown bold markers, source-index brackets and number tags such as [[n3]] from stored text. In a Word document, never write markdown bold markers. The tile and narrative field rules in the language standard apply to dashboards, not to this document. Platform findings never go in the document.

## Output and Asset Guidance

The template and the layout in Step 8 are guidelines for typography, table design and ordering. They are not a required content schema and not the canonical form of the output. Absence of information is not itself an output.

1. Include a section, table, row or item only when there is substantive information to populate it. Do not create empty categories, placeholder rows or repeated "Not disclosed" lines.
2. When information is unavailable and its absence does not bear on the credit read, omit it.
3. When missing information is credit-relevant, state it once, as a question or request in the most appropriate place.
4. Before treating a material item as unavailable, apply Document Escalation.
5. A pipeline status, such as an analysis not generated, is not a deal fact. Keep it out of the document and tell the user in chat, once.
6. Never infer or manufacture content to complete the layout.
7. Judge missing documents against the deal's stage. An executed agreement is not expected before terms are proposed.

## Rules

1. The vault and dashboards are the only source of content. Adapt wording only. Do not invent questions or facts.
2. Pull before asking. Resolve the deal and read every source first. Ask the user only for what the data cannot tell you.
3. Record every source as read, empty, not generated or not read. Report only what limits the list, in the reply notes.
4. Every item is bespoke and carries four parts: why this deal, what we need to see, what it changes, and its source.
5. Where sources disagree, report both. The executed agreement governs terms, audited statements govern reported figures, and a draft is labeled draft.
6. Where a source is empty or a register under-reports, do not fill from memory. Say what is missing in the data notes, in analyst language.
7. Plain numbered lists and headings that name content.
8. Questions are neutral and open-ended first. Never "isn't it true that."

## Step 0: Resolve and check readiness

If the deal was identified earlier in this conversation, use it. Otherwise search the deal list by deal name and by company name in parallel, ignoring case, spaces and punctuation. If neither search finds a match, fall back to the full list with show_all true and follow next_cursor until the list ends or one match is found. One match: use it. More than one: show a table and ask. No deal named: ask which. Skip any fetch already made in this conversation. Use the deal list's name for the header, because a dashboard's own Deal field is sometimes wrong. If the Raven tools are not yet available, load them first.

Check that analysis has finished. "Ready to view!" means proceed. Anything else means stop: give the status, say to try again in 15 to 30 minutes, or to start the analysis from within Raven if it shows Not started, Failed or Aborted. This chat cannot start it. Note today's date.

Check freshness once, using the freshness tool if it is available. If `is_stale` is true, state the warning at the top of the sheet. If no indicator comes back, say once that freshness could not be confirmed.

## Step 1: Pull the registers

Read `references/source-checklist.md`. Read Open Data Gaps and Diligence Focus Areas, plus Investment Risks, which Diligence Focus Areas is built from, and the deal overview and document list. Fetch each whole by question ID. Search only to discover an ID. Question IDs can be renumbered, so confirm each by name. If a response says it was truncated, fetch that ID alone and use the complete text. Never build the list from search fragments. Issue the Step 1 reads in a single parallel turn.

If an item needs a figure its entry does not carry, open the prompt named in its SOURCE field, read only that one, and cite it. Do not read other prompts to build or extend the list. Where the register under-reports or looks wrong, do not correct it silently. Say what is missing in the data notes.

If a register's header counts do not match the entries beneath it, count the entries and use them. Mention the mismatch only if the user asks for platform findings. Render stored figures as stored and never recompute them. Carry a source's own confidence signal. Render figures in the deal's own currency and units, and carry period labels as stored. Where a source has disclosed its own data-quality issue (a callout, a restatement, a footing gap), report it and do not silently correct it.

## Document Escalation

Where the analysis leaves a figure unavailable or a topic thin, read the document text or search documents by type before treating it as unavailable. Confirmed once is confirmed. Do not re-query hoping for a different answer.

## Step 2: Ask only what is missing

In one short message, ask for what the data cannot give: meeting type (management presentation, expert call, customer or owner reference, advisor check-in), attendees, date, topic focus and any specific concerns. Default to the meeting sheet and produce the request list on request.

## Step 3: Profile the deal

Capture deal type, business model, structure features (acquisition contributions, deferred payments, delayed draw, springing covenant) and the earnings basis. This decides which topics are live. A topic that does not apply is dropped.

## Step 4: Run the checks

1. **Status and date.** Run `references/status-date-checklist.md`.
2. **Source conflicts.** Compare revenue, Adjusted EBITDA, capex, free cash flow and total debt across documents, sorted by basis (actual, pro forma, projected). Also compare the QoE against the audited statements, the executed agreement against the vault, management claims across documents, and the vault against the dashboards. Label a basis difference with its mechanism. Report an unexplained difference as a discrepancy. Use the document conflict skill where available.
3. **Claimed versus supported.** Read the Competition and Barriers to Entry checks. Keep each claim, its support and its diligence request.
4. **Peer read.** Use the peer set skill. If Raven's comp analysis is not generated, build the read from the comp-set filings, with each peer's own figures, period and currency. Say that Raven's version is missing, and flag any summary figure that does not match the filings. Carry only peer signals that apply to the borrower's business model. Say in one line which signals were left out and why.

## Step 5: Collect candidates and rank

Candidates are:

1. Every gap in Open Data Gaps and every Diligence Focus Area.
2. Every risk with no or limited mitigant in Investment Risks.
3. Every failed check from Step 4.
4. Questions already logged in the Credit Q&A, if any. Do not ask what is already answered.

Remove duplicates and tag each with its topic, its workstream and its gap category (Company, Industry, Financial, Collateral & Liquidity, Structural). Each Diligence Focus Area is one topic. A gap or a conflict finding with no focus area goes under the topic it most affects. Order topics by the rank in Diligence Focus Areas. Within a topic, keep the order in Open Data Gaps. Do not re-rank. Use `references/meeting-type-guide.md` only to drop or defer items.

Aim for 30 spoken questions, and never fewer than 20. At least half must be Company or Industry questions. Fill remaining slots from high gaps, then medium gaps, then conflict findings. A conflict-driven Financial question is added only after the business gaps in that topic are covered. For a request list, keep up to 25 items. A deferred gap goes to Follow-up Requests and stays in the appendix.

## Step 6: Write each item

Four parts: why this deal (the specific fact with figure and source), what we need to see, what it changes, and source (document and page). Question IDs and dashboard names stay out of the document and the reply, unless the user asks for platform findings.

- **Meeting view:** one neutral spoken question with one data point, starred if a must-ask, with a follow-up probe. Each question is followed by a probe line, then a source line in small gray type. The source line gives the focus area, gap or risk, what we need to see, what it changes, and the document and page. A question that comes from a conflict finding names the finding in its source line. Compare figures on the same period. If the periods differ, say so in the question.
- **Request view:** a request naming the document, dataset and period.

Drop or reword any item that a later document already answers. Before output, open the source page for the two highest-ranked items and confirm the cited figure appears on it.

## Step 7: Completeness check and Pass 2

Use `references/workstream-map.md`. Every high-priority gap must map to an item or a follow-up request. Note any workstream the list did not touch and any source not pulled, in the third reply note.

Run one parallel wave of up to four document searches: two on top-ranked items that depend on a fact a document may already answer, and two open-ended searches with no field in mind ("what would a careful lender want to know that nothing on this list addresses yet"). Run the open-ended searches against deal analysis only, unless the deal holds executed or draft legal documents. If a result contradicts an anchor fact or surfaces a material gap, one follow-up wave of up to three searches is allowed. Drop or reword any item the documents already answer. Report what Pass 2 found in chat, even if nothing new.

## Step 8: Output

The meeting sheet is a Word document named "[Deal name] Meeting Prep". Do not render the sheet in chat and do not publish a separate page. Build it with `scripts/build_meeting_prep.py`, which fills `assets/dd_meeting_prep_template.docx` from a structured input file. The script numbers questions and requests itself and resolves cross-references, so write each question once and refer to it by id. `scripts/input_placeholder.json` shows the input shape and holds placeholders only. The template and the layout below are guidelines for typography, table design and ordering, and are not a required content schema. Adapt the structure when the meeting type calls for a different shape, for example the request list view. Leave out any section or row with nothing to populate, and check that the file opens before presenting it. If the script or template cannot be used, follow `references/layout-spec.md`. A layout or placement preference stated by the user overrides the template. If this session cannot create files, say so and render the same content in chat.

The front section, in this order:

1. Logistics.
2. Objectives: the top three ranked topics that fit this meeting type.
3. Questions, grouped by topic. Each topic is one ranked focus area, shown with its number, name, category in brackets and its credit mechanism in one or two sentences, followed by its questions. Topics follow the rank in Diligence Focus Areas. Numbering runs continuously across topics. Must-asks are starred. Within a topic, order questions by gap priority, then the gap list's own order. Each question has a probe line and a source line as set out in Step 6.
4. Follow-up requests.

Appendices in the same document, in this order, each shown only when it has content:

- A. Full gap list: one table per category, in the gap list's own order, with the category's high, medium and low counts above it, and the columns priority, topic, description, diligence ask as written, and status for this meeting (asked in question N, or deferred to a request). Order each table high, medium, then low.
- B. Sources used: each document read, with the pages cited.
- C. Status and conflict findings: each finding, with the figures from both sources, the basis, and the question or request it feeds.
- D. Peer set and filing signals: each peer's own figures, period and currency, and what its filings show that the deal documents do not. When no peer set exists, say so in one line.
- E. Claims check: each claim, its support, and the diligence request.

When a step was not run, say so in one line in that appendix instead of leaving it blank. Source status, platform findings and what was not read stay in the chat reply.

After the output, the chat reply carries three short notes in analyst language, with no prompt IDs and no mention of the vault, dashboards or registers:

1. Data notes: conflicts between documents, figures that look stale or inconsistent, missing documents, and anything the list could not confirm, each stated once. The data notes give the headline conflicts and point to Appendix C for the figures.
2. What Pass 2 found, even if nothing new.
3. What was not read or not run, and why.

Issues in how the analysis itself was generated, such as a gap list whose counts do not match its entries, stay out of the reply. If the user asks for platform or data-quality findings, give all of them in full.
