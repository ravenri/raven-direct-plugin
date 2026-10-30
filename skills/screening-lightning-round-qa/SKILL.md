---
name: "screening-lightning-round-qa"
description: "Ranked list of the questions a senior credit investor would press on for a deal, taken from Raven's own diligence priorities and gaps. Triggers: lightning round, what will they ask me, top questions on this deal, quiz me, question set before IC."
when_to_use: "Use when the user asks for a lightning round, what will they ask me, the top questions on this deal, to be quizzed, or a ranked question set before IC. Use this instead of answering ad hoc."
---

# Lightning Round Q&A

Produces the questions a senior credit investor would press on for a deal, as preparation for IC or a
skeptical senior. The questions come from Raven's own diligence priorities and open data gaps, in
Raven's own order. Claude does not re-rank them. It turns each into a specific question tied to a deal
fact, adds the answer where the analysis has one, and states plainly where the answer is a gap.

The selection basis for the few added questions is in `references/prioritization-prompt.md`. Read it
before Step 3.

## Language

All output conforms to `references/language-standard.md`. Read and apply it. The questions themselves
are genuine questions; the standard's ban on rhetorical questions applies to the answer sentences. Do
not expose platform plumbing (no "the tile," "the vault," prompt IDs). ID fields are internal; never
display them unless asked.

## Project resolution

If the deal is already identified from earlier in this conversation, use it. Otherwise, if the user
named a deal, look it up by name in the user's list of deals, and by company name if the name returns
nothing. One match, use it; more than one, present a table (Deal, Company, Sponsor, Status, Created, no
internal IDs) and ask. Do not guess. If no deal is named, ask first.

## Step 0: Analysis readiness

Check whether the deal's analysis has finished running. If it has not, stop. Tell the user the status
and to retry in 15 to 30 minutes, or to start the analysis from within Raven if it shows Not started,
Failed, or Aborted. This chat cannot start it.

## Step 1: Read the spine

Read the Diligence Focus Areas, the Open Data Gaps register and Investment Risks, each whole.

- Fetch each by question id, never by search. Search ranks and returns fragments of a long register,
  so a list or count read from it is incomplete. In the current workbook the Open Data Gaps register is
  id 2100 and Diligence Focus Areas is id 2101. Find the id for Investment Risks with one search, then
  fetch it whole. If a fetch returns something other than the expected content, confirm the id with one
  search before using it.
- The Open Data Gaps register starts with the header fields Gaps Identified, Gaps By Priority and Gaps
  By Category. Diligence Focus Areas starts with Focus Area Count. Do not confuse them.
- If none of the three has been generated for this deal, say so and stop. Do not assemble questions
  from a fresh search of the deal's analysis.

## Step 2: Fill in figures, only where missing

For each question, open a dashboard section only when a figure needed to state the question or its
answer is missing from the register entry, and open only the single section the focus area or gap
points to. Do not scan the dashboards deal-wide. If a section needed was not generated, say so in one
closing line.

## Step 3: Order and write the questions

Order follows Raven.

1. Diligence Focus Areas, in their own rank order.
2. Then HIGH gaps, in the register's category order (Company, Industry, Financial, Collateral &
   Liquidity, Structural), skipping any gap already covered by a focus area.
3. Then MEDIUM gaps, in the same category order.

Claude does not re-rank or re-prioritize. Priority labels are exactly as the register states them.

Each question names the specific deal fact that makes it matter. Where the analysis answers it, give
the answer in one short sentence, facts and figures unchanged. Where the item is a gap, state in one
short sentence that the information is undisclosed and why that matters to repayment. Never invent an
answer, a figure or a source.

Additions: after the register-ordered questions of the first batch, add at most three company-specific
questions, each naming the deal fact behind it. These exist to nominate a telling absence or an
exposure the registers did not flag. Select them with `references/prioritization-prompt.md`. Mark them
"Added for this deal" so they are not mistaken for Raven's own order. If nothing qualifies, add none.

## Render

Lead with: **[Deal Name], [Company]: Top Questions**

A plain numbered list, no cards, no per-item headings, no narrative around the list. Each item is:

[Number]. [Question, grounded in the deal fact.] [One sentence: the answer, or the statement that it is
undisclosed and why that matters.]

Then, on a new line under the item, only where the underlying analysis carries a source:
*Sources: [document p.X, document p.Y]*, copied from the source field. A source is a document, not a
dashboard section. Omit the line if there is none.

Example of an item (format only):

1. No reported-to-adjusted-to-pro-forma EBITDA bridge or Quality of Earnings report is disclosed for the
anchor period. Which adjustments sit in the earnings base that leverage and coverage are struck on? The
bridge and itemized add-backs are not disclosed, so the quality of the leverage anchor cannot be judged.

First batch: ten questions in Raven's order, followed by any additions, numbered continuing. Then end
with one plain line offering more.

## Continuing

If the user asks for more, give the next ten down the same order, numbered from the last number, with
no repeats of anything already asked in this conversation. When the register is exhausted, say so
plainly. Do not manufacture filler or generic follow-ups.

## Rules

- Spine first: Focus Areas, Open Data Gaps and Investment Risks, fetched whole by id.
- Order follows Raven. Claude does not re-rank.
- Dashboards are opened only to supply a missing figure, one section at a time.
- Every question names the specific deal fact driving it; never a generic checklist prompt.
- A gap is stated as a gap, with why it matters; never fabricate an answer or a citation.
- Stored-analysis read: never recompute a figure or verdict the analysis already states.
- Every question shows its number.
- ID fields are internal; never display them unless asked.

## Delivery

Render in chat.
