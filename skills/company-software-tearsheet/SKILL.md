---
name: "company-software-tearsheet"
description: "Produces a four-page Word tearsheet for a software borrower: business and revenue model, market position and barriers to entry, AI exposure, customers and contracts, financial summary, key metrics with formulas and reference ranges, and key issues, with a credit implication closing each major section. Built from the Software analysis and the core company answers as they stand, plus a silent analyst scan that selects and orders the key issues. Not for deals without the Software analysis. Use this instead of answering ad hoc when asked for a software tearsheet, software credit review, software company profile, or a read on a software borrower's ARR, retention, customers and AI exposure."
when_to_use: "Use for \"software tearsheet,\" \"software credit review,\" \"software company profile,\" or a read on a software borrower's ARR, retention, customers or AI exposure, including a loose \"tearsheet for [deal]\" on a software deal. Do not use for a deal without a Software analysis, a deep read of one topic, cyber or IT risk, or a non-software borrower."
---

# Company - Software Tearsheet

Produces a four-page credit tearsheet for a software borrower, delivered as a Word document built from
`assets/software_tearsheet_template.docx`. It reads what the analysis already stores, adds nothing the
documents do not support, and closes with the key issues an analyst would press on.

**What makes this more than a summary: a silent analyst scan.** After reading, the skill scans across the
answers the way an analyst would and selects the few issues that change how the credit should be read:
concentration against renewal timing, revenue that is transactional rather than committed, retention evidence,
competitive position, AI exposure, and margin and cash conversion. The scan is never shown or labeled; only the
Key issues section appears. Where borrower figures disagree, the document shows both figures.

## Scope

A tearsheet, not a full review. It does not re-run analysis, recompute a metric, rank the borrower against peers,
select an underwriting case or recommend a structure. For a deep read of one topic, say so and point to the
dedicated skill (customer diligence, earnings quality, competition, business overview).

## Language

All output conforms to `references/language-standard.md` (American spelling, credit-desk register, quantify rather
than characterize, no em dashes, no hype adjectives, house banned-word list). Read it and apply it; do not restate
its rules here. Never name Raven or expose prompt IDs, and never write "stored", "as stored", "the analysis", "the answers",
"the tile" or "the vault" in the document. Attribute a figure to the materials ("stated", "reported", "the presentation
shows") or state it plainly. Never use tiles, badges, tinted boxes or colored borders. Source lines cite documents and pages.

## Project resolution

- If a project_id is already known from earlier in the conversation, use it.
- Otherwise, if the user named a deal, call `deal_list` and resolve by project name or company name. One match: use
  it. More than one: show a table and ask. Do not guess.
- If no deal is named, ask which deal before doing anything else.

**Skip-if-known (strict):** if a call below was already made in this conversation, do not repeat it.

## Step 0: readiness and staleness

The `deal_list` response carries `analysis_status`; anything other than "Ready to view!": stop, report the status,
suggest retrying when analysis completes. Do not call `analysis_get_status`, which lists every document. Check the
`freshness` field on the first dashboard response. If `is_stale` is
true, add one line under the header giving the dashboard's own stated reason. If the field is absent, say nothing.

## Step 1: read everything in one parallel wave

Issue all reads in one block.

1. `dashboard_get` for tile "software", sections "business-model" and "financials-metrics". Do not read the "overview"
   section: it repeats these and carries benchmark scorecards the tearsheet does not use. Build the classification line
   from the business model's detail grid. If the business-model section is missing or empty, stop and say the deal has
   no Software analysis; point to the Company Analysis skills. Do not build a tearsheet from core answers alone.
2. `analysis_get_question` for the registry names and IDs in `references/section-spec.md`, in batches of seven IDs
   or fewer, all batches in the same block. Match by registry name first; if an ID returns a different name, trust
   the name. Do not read Open Data Gaps.

An answer that is not found, such as on a deal run before the answer existed, is omitted from the document and
listed once under Open diligence. Never fill it from memory or from another answer's neighboring text.

**Number tags.** Answers carry tags such as [[n3]] beside figures. Strip every tag from anything written. Use the
answer's numbers record to attach the period, the entity and the claim type to a figure. A record whose entity is
not the subject (a competitor or an industry figure) is not the company's figure and stays labeled as what it is, and
a threshold is a limit, not an actual.

## Step 2: assemble from the section specification

Follow `references/section-spec.md` for what each section shows, which answers feed it, table formats and the page
plan. The rules that hold for every section:

1. **Read, do not calculate.** Report a figure only as the answer states it, with its period label (A actual, B
   budget, P projected) and basis. Do not add, subtract, combine, convert or annualize figures, including to explain why
   two figures differ: state each with its source and say they do not reconcile. A percentage or total appears only if
   the answer states it. A historical table never mixes in a B or P
   period; budget and projected figures appear in a sentence or a separately labeled column.
2. **Core answers lead.** Where a Software answer and a core answer state the same fact differently, use the core
   answer and list the conflict in the chat summary only.
3. **Borrower discrepancies stay visible.** Where the documents disagree (for example client revenue by name against
   the top-five total), show both figures and state that the basis of the difference is not given. Never choose one
   silently, and list each such pair in the input's "figures that do not reconcile" note.
4. **No invented content.** Switching costs, AI effects, competitor positions and unit economics appear only if the
   answers state them. A figure the documents do not support is left out, even if a Software answer offers one.
5. **Absence is stated once.** Credit-relevant gaps go in the Open diligence line, not in every row, except in the
   Key metrics table, which always lists the full metric set with "Not disclosed" where absent. Take the open
   diligence items, at most five, from the key issues and the metrics marked Not disclosed. Read Open Data Gaps only
   when the user asks for the full list.
6. **EBITDA and periods.** Name every EBITDA figure by its canonical layer title from the EBITDA Layer Catalog (for
   example PF Adjusted Cash EBITDA, never "Adjusted EBITDA" for a cash layer) and label periods from Canonical Period
   Anchors. Where the Software tile's period labels repeat or disagree with the anchors, or two margins
   disagree, use the anchors and the cataloged layer and list the disagreement in the chat summary only.
7. **The tile's own conflicts.** The Software tile may carry a Data Conflicts block recording conflicts the analysis
   built itself (for example a recomputed retention figure against the disclosed one). Use the disclosed figure and
   list those conflicts in the chat summary only.
8. **Credit implication.** Each major section ends with one or two sentences saying what the facts mean for
   repayment, written from the facts above it and starting with the words "Credit implication."

## Step 3: select the key issues

Choose up to six, ordered by materiality to repayment. Each issue is a plain-noun heading, a type (Business or
Financial), evidence made of stated figures with period and perimeter, and one sentence of credit implication.
Menu: concentration and renewal timing, revenue commitment, retention evidence, delivery transition, competitive
position, AI exposure, earnings basis, margin and cash conversion, plan against history. Concentration and renewal
timing are one issue when both are present. State a disclosure limit only when lender materials assert the opposite
in words without figures.

## Step 4: write, build, check, deliver

The layout is fixed in assets and scripts. Write only the facts and prose.

1. Write the input file for this run into a working folder (never into the skill), following `references/input-guide.md`
   and `references/phrasing.md`. Stay inside the character budgets in `scripts/length_budgets.json`.
2. Build: `node scripts/build_tearsheet.js <input file> <output .docx>`. The script lays out the header, tables, all nine
   barrier rows and the thirteen fixed key metric rows, and prints length warnings. Shorten any field it flags.
   `assets/software_tearsheet_template.docx` is the same layout with placeholders, for a person to read or edit; it is
   not an input to the build.
3. Check: `python scripts/check_tearsheet.py <output .docx>`. It tests page count and page starts (Customers and
   contracts, AI exposure and Key metrics must begin pages 2 to 4), em dashes, banned words, system jargon, leftover
   placeholders and number tags, and acronym spell-out. Fix every problem it lists and rerun until it passes. Do not open
   page images unless the check fails on layout.
4. Present the file, then give a chat summary of at most 120 words: the two-sentence credit read, the issue
   headings, the conflicts found between answers that are not in the document, and any section omitted for missing answers.

## References

- `references/language-standard.md`: language, tone and banned words.
- `references/section-spec.md`: sections, reading map, table formats, page plan, disclosure adaptations.
- `references/software-metrics-reference.md`: metric formulas and reference ranges, with sources and dates. The only
  permitted source of reference ranges.
- `references/phrasing.md`: standard wordings for absent figures, conflicts and projections.
- `references/input-guide.md`: what each input field holds, and length budgets.
- `scripts/`: `build_tearsheet.js` (layout and tables), `check_tearsheet.py` (pre-delivery check), `length_budgets.json`, `placeholder_input.json`.
