---
name: "deal-terms-quick-screen"
description: "Produces a fast, skimmable deal-terms summary for the initial screen, delivered as a Word document: a transaction overview, a quick term sheet by facility, Sources & Uses and Capitalization as stored, at-close key metrics, and numbered Analyst Notes. Sourced from the Deal Summary dashboard. Adds a silent analyst scan that flags what an analyst would catch: a stale dashboard, the same field disclosed at conflicting or restated figures, undisclosed card fields, and callouts that bear on how the deal is levered (such as a cash-vs-accrual EBITDA gap driving the leverage figure). Uses the house note vocabulary shared with the Raven-powered memo (Analyst Note, Key Credit Concern, Counterargument, Diligence Item). Deliberately a screening-depth read, not a covenant-by-covenant agreement analysis. Use for \"deal terms,\" \"quick term sheet,\" \"what are the terms,\" or a fast read of a deal's debt facilities at close."
when_to_use: "Use for \"deal terms,\" \"quick term sheet,\" \"what are the terms,\" or a fast read of a deal's debt facilities at close. Do not use for a covenant-by-covenant analysis (Credit Agreement Grid, Key Definitions) or for returns."
---

# Deal Terms Quick Screen

Produces a fast, skimmable term-sheet read for the initial screen: a short transaction overview, a quick term sheet
by facility, Sources & Uses and Capitalization as stored, and a handful of at-close metrics. Sourced from the Deal
Summary dashboard and delivered as a Word document built from `assets/deal_terms_quick_screen_template.docx`.

**What makes this more than a condensation: a silent analyst scan surfaced as Analyst Notes.** The prior connector
only compressed what the dashboard showed and stopped. This skill does that condensation and then silently reads
across it the way an analyst would on a first pass, surfacing the few things that change how the terms should be
read: a stale dashboard, a figure disclosed at conflicting or restated values, and any callout that bears on the
leverage. The scan itself is never shown or labeled; only its output appears, as Analyst Notes in the house
vocabulary shared with the Raven-powered memo. The term sheet is the what; the Analyst Notes are what an analyst
would notice about it.

## Scope

Screening depth, not terms-stage depth. This is the fast read an analyst wants during the initial screen: facility
sizes, pricing, tenor, security, the headline mechanics, and a short flag list. It is NOT a covenant-by-covenant,
prepayment-waterfall, incremental-capacity agreement analysis; that is the separate Terms-stage skill. When the
request is for that depth, say so and point there rather than expanding this one. The line: this skill flags that
something needs a closer look; the Terms-stage skill is the closer look.

## Language

All output conforms to `references/language-standard.md` (American spelling, credit-desk register, quantify rather
than characterize, no em dashes, no hype adjectives, house banned-word list). Read it and apply it; do not restate
its rules here. The standard's markdown bold rule for dashboard fields does not apply in the Word document. Source
lines cite documents and pages. Never name Raven, dashboards, the vault, or records in the document, and never
expose prompt IDs. Present a term as a term and a flag as a flag.

## Project Resolution

- If a project_id is already known from earlier in this conversation, use it directly.
- Otherwise, if the user named a deal, call `deal_list` to resolve it by name. Exactly one match: use it. More than
  one: present as a table and ask the user to confirm. Do not guess.
- If no deal has been named, ask which deal before doing anything else.

**Skip-if-known (strict):** if `analysis_get_status` or the `dashboard_get` call below is already available from
earlier in this conversation, do not re-call it.

## STEP 0: Analysis Readiness

If the deal list entry already shows analysis status "Ready to view!", proceed without calling `analysis_get_status`. Otherwise call `analysis_get_status(project_id)` (skip if already known). "Ready to view!" means proceed. Anything else: stop,
report the status, and suggest retrying once analysis completes or running `analysis_apply_start`. Do not produce a
term sheet from an unready deal.

## STEP 0.5: Staleness (do not skip)

Check the `freshness` field on the dashboard response. It is inconsistently present, and on at least one real deal it
came back `is_stale: true` on a fully-termed deal. Staleness matters more for a terms summary than almost anywhere
else, because a stale term is worse than a missing one: someone acts on it. If `is_stale` is true, fill in the
shaded Analyst Note under the cover table: the terms shown reflect the last full analysis date. In the shaded note, give the dashboard's own stated
reason, for example "Some figures were edited after that analysis." Say the deal documents changed only if the
freshness field says so. Confirm any figure that drives a decision. If the field is absent, do not assume
either way and do not manufacture a staleness claim; delete the note.

## Retrieve

Pull the Deal Summary dashboard once, the whole dashboard, via `dashboard_get(tile="deal_summary_dashboard")`, so the
Fact Restatements table is visible. Read its Overview, Sources Uses, Debt Facilities, and Fact Restatements,
including every callout. Callouts are material for the scan and are not to be skipped. Render only at-close content.
Do not render the Projections or Gaps sections. Do not cross-reference the credit agreement or the analysis Q&A to
re-derive or resolve terms; read what the dashboard shows, flag what needs a closer look, and leave the closer look
to the Terms-stage skill. Show "Not disclosed" and "Not specified" as the dashboard does. Write n/a for a blank cell.
Never use an em dash.

## The silent analyst scan: read across everything, surface only what matters

After assembling the term sheet, silently read across everything pulled the way an analyst would on a first pass.
**This is a scan, not a rendered step: never label it, never narrate it, never show a "second review" or "scan"
heading.** It produces a set of Analyst Notes (below), and nothing else about the scan itself appears in the output.
**Be systematic: walk every field on every facility card and every callout, not just the first few interesting
things.** Stopping at two or three notes when a card is still flagging something (a warning icon, a "Not disclosed")
is under-scanning, a confirmed failure mode. Include a note only when it is real; a clean, fresh,
internally-consistent deal legitimately produces zero notes. Look specifically for, at minimum:

1. **Staleness.** From STEP 0.5. It goes in the shaded note under the cover table, not in the numbered list.
2. **Same field, conflicting figures across sources.** The dashboard often shows a metric at different values from
   different documents. Confirmed live: an RCF at "$175MM executed" vs. "$200MM in presentation/model", a first lien
   shown as both "$2,225MM" (header) and "$2.2B funded" (Size field) on the same card. Do not silently pick one.
   Raise it as an Analyst Note, name which source carries which figure (executed agreement, lender model, lender
   presentation), and state the analyst's default plainly: the executed agreement governs current terms; the
   marketing case may differ. Do NOT go pull the agreement to resolve it (that is Terms-stage depth); naming the
   sources is usually enough for the analyst to resolve it.
3. **Restated figures.** If the Fact Restatements table lists a figure that appears in the Transaction Overview,
   Key Metrics, Sources & Uses, or Capitalization, show the stored figure and raise an Analyst Note naming the
   restated value. Never quote leverage from the Situation Overview text without checking it against the KPI
   snapshot and the restatements.
4. **Any card field flagged "Not disclosed."** Confirmed live: the 1L Term Loan card flagged "OID / Upfront Fees: Not
   disclosed in documents" with a warning marker. Undisclosed OID or fees is a real economic gap for a
   returns-sensitive reader. Raise these as Diligence Items, consolidated by theme (see Quick Term Sheet); do not let a
   "Not disclosed" pass silently just because the field rendered. Walk every field for this, not only OID. A field a
   card does not show at all is not flagged.
5. **A callout that bears on leverage or pricing.** Carry forward any Overview or Debt Facilities callout that
   changes how the terms read, as an Analyst Note or Key Credit Concern per its weight. The clearest example,
   confirmed live: a "cash EBITDA below accrual EBITDA" callout (a deferred-revenue haircut cutting the earnings base
   the leverage is struck on) is arguably the single most important fact about how a deal is levered. Do not carry
   boilerplate callouts that add nothing; carry the ones that move the read.
6. **Coverage gap.** If the Deal At A Glance debt-structure line or total-debt figure implies more tranches than the
   Debt Facilities section has cards for (a known gap on some deals: Notes or a bridge present in the structure but
   missing facility-level terms), raise a Diligence Item naming which tranches the term sheet covers and which it
   does not.

7. **Multiples across tables.** Compare each multiple that appears in more than one place, for example total leverage
   in the key metrics and in the capitalization table. If they differ, raise an Analyst Note stating both figures and
   the likely cause, such as truncation versus rounding.

This list is a floor, not a ceiling. Anything else the systematic walk turns up that an analyst would want flagged
(an unusual call-protection structure, an MFN with a short sunset, a springing covenant set at an unusually loose
level) is fair game for an Analyst Note. The point is to walk everything, then surface what matters, not to stop at
a fixed count.

## Word Document Layout

Build a Word document from `assets/deal_terms_quick_screen_template.docx`, using the Word
document skill. Work on a copy so fonts, table layout, and section order carry over exactly. Replace bracketed
placeholders, repeat the group heading and term table once per group, add or delete table rows and columns only where the data requires it, and delete any shaded note that
does not apply. If this session cannot create files, render the same sections in chat.

Build: write a content file as described in `references/content-format.md` and run `scripts/build_quick_screen.py content.json output.docx`. The script fills the template; do not edit the Word XML by hand.

Sections in this order: cover table with the staleness note, Transaction Overview, Quick Term Sheet, Sources & Uses
and Capitalization, Key Metrics at Close, Analyst Notes. Every table has a source line underneath.

**Cover table:** Project (project name and company), Sponsor (list both if co-sponsored), Transaction (type and
headline price), Earnings basis (the LTM period label).

**Transaction Overview:** two to three sentences: what is being acquired, by whom, for how much, and how it is
funded (equity contribution and total debt at a headline level, not tranche by tranche, since that is the term sheet
below). State the transaction type if the source gives it. Check any leverage figure against the KPI snapshot and
the Fact Restatements table before using it.

**Quick Term Sheet:** take each facility's fields from its own card, in the card's order. Do not add a field the card
does not show, such as OID, ranking, or mandatory prepayment, and do not write Not disclosed for a field the card
omits. Where two cards carry the same term under different labels (for example Commitment and Facility size, or
Amortization and Repayment profile), put them on one row and use the first facility's label. Write n/a where a card
does not show the term. Group facilities by pari passu group, using the capitalization table: facilities that share one cumulative x EBITDA figure form one group. Within a group, separate bank debt from bonds. Bank debt is revolvers and term loans. Bonds are notes and the bridge facilities that take them out. Each table holds one such group, with its facilities as columns in dashboard order, under a heading naming the ranking and the type (for example, First lien, bank debt). Groups follow the capitalization table order, from most senior to least. A facility the dashboard shows at its own cumulative multiple, or one whose form is not disclosed, is its own group. Column headings are the facility names; the ranking sits in the group heading, so do not add a ranking row. Card fields the dashboard marks Not disclosed become Diligence Items, consolidated by theme. Write one item per term (pricing, fees, call protection, financial covenants, guarantors and so on) naming every facility where it is not disclosed and the dollar amount of debt those facilities represent. A facility with no disclosed terms at all, such as rolled other debt, is its own item. Cell values follow the tile-field rules in the language standard: lead with the figure,
stay under 90 characters, and no sentences. If the source labels a pricing figure an estimate, add one footnote under
the table.

**Sources & Uses and Capitalization:** render these two tables exactly as stored from the Sources Uses section, as in
Initial Deal Review. Do not rebuild, regroup, or recompute. If the Sources Uses section lists uses only, take the sources lines from the
Cap Table's debt and equity rows, amounts as stored, and say so in the source line. Show percent of total only where
the dashboard stores it; otherwise drop those columns.

**Key Metrics at Close:** a four-column table from the Deal At A Glance block, at-close metrics only: total net debt, net and total leverage, first lien LTV, and any other at-close metric the Deal At A Glance block shows, such as transaction size or enterprise value with its basis. Leave out any metric the capitalization table already shows. Do not compute or add a metric the dashboard does not carry.

**Analyst Notes:** a plain numbered list, each item starting with its label: Analyst Note (an inconsistency,
unreconciled figure, or restated value), Key Credit Concern (a fact that materially changes how the terms or leverage
read, like the cash-vs-accrual EBITDA basis), Counterargument (a claim that cuts against the sponsor's framing), or
Diligence Item (a coverage gap or an open question to resolve). Label each per what it actually is. Staleness goes in
the shaded note under the cover table and is not repeated in the list. The scan stays silent: never render a scan or
second-review heading. If the scan produces nothing, omit the section rather than writing "no notes".

In chat, after delivering the file, close with a plain-text link to the dashboard and one natural next step: the
source page behind a specific term, or the deeper Terms-stage read if a flag warrants it.

## Rules

- Screening depth only. Raise an Analyst Note or Diligence Item that flags what needs a closer look; do not perform
  the closer look. Covenant, prepayment, and incremental depth is the Terms-stage skill's job.
- The analyst scan is silent. Never render a "second review," "scan," or "analysis pass" heading. Only its output
  appears, as Analyst Notes.
- Use the house note vocabulary shared with the Raven-powered memo: Analyst Note, Key Credit Concern,
  Counterargument, Diligence Item. Label each per what it actually is.
- Never silently pick between conflicting figures. Raise an Analyst Note and attribute each figure to its source.
- Take term sheet fields from each facility's own card. Do not add a field the card does not show and do not drop one
  it does show as "too deep"; the card is the screening view. Borrower, Guarantors, and Incremental mechanics are not
  on the cards and are omitted.
- Render the term sheet as tables, one per pari passu group as set out under Quick Term Sheet. Never a loose bulleted list.
- The scan is systematic: walk every field on every card and every callout. Stopping at a fixed count of notes while
  a card still flags a "Not disclosed" or warning icon is under-scanning, a confirmed failure mode.
- Card fields flagged "Not disclosed" become Diligence Items, consolidated by theme, not silent omissions.
- Surface staleness first when present, in the shaded note; never manufacture it when the field is absent.
- Show "Not disclosed" as the dashboard does, write n/a for a blank cell, and never fabricate a figure the dashboard
  does not show.
- Every facility appears. Condensation, not omission.
- Zero Analyst Notes on a clean deal is a valid, honest outcome. Omit the section rather than inventing concerns to
  fill it.
