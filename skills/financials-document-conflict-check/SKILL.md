---
name: "financials-document-conflict-check"
description: "Compares the same financial figure (Revenue, Adjusted EBITDA, Capex, Free Cash Flow, Total Debt/Capitalization, or a named metric) across DIFFERENT source documents, CIM vs. QofE vs. audited financials vs. compliance certs vs. sponsor model, sorting by presentation basis (Historical Actual/Pro Forma/Projected) before comparing so a basis difference is never flagged as a discrepancy. Also checks whether Raven's own canonical anchor matches the most reliable source found. Judgment-driven and vault-search-based, not a stored-read: results can vary run to run. Runs a two-path check: cross-class AND intra-class (multiple documents of one class, since stale figures persist across revisions). Does not re-derive trends; that's financials-snapshot's job. Use for \"check for document conflicts,\" \"does the CIM match the QofE,\" \"cross-check the financials across documents,\" \"has this figure changed across decks,\" \"did Raven pick the right anchor,\" or a document-vs-document consistency check."
when_to_use: "Use for \"check for document conflicts,\" \"does the CIM match the QofE,\" \"cross-check the financials across documents,\" \"has this figure changed across decks,\" \"did Raven pick the right anchor,\" or any document-versus-document consistency check. Do not use for the quality of earnings read or the analysis of a single document."
---

# Financials — Document Conflict Check

Compares the same financial figure across different SOURCE DOCUMENTS in a deal and surfaces genuine
discrepancies. This is the one capability in the suite no dashboard tile can provide: every tile is one
synthesized view; this workflow deliberately looks document by document instead.

**This is a judgment-driven, non-deterministic workflow, unlike the rest of this suite.** Every other
skill here renders a stored tile faithfully; this one runs targeted vault searches and reasons over
whatever chunks surface. Results can vary run to run. Say so plainly when delivering a clean result: "no
discrepancy found across the metrics checked" is not the same claim as "this deal's financials fully
reconcile," and the render should never blur the two.

**Use only when the user specifically wants a cross-document consistency check.** This is not the default
financials pull, that is `financials-snapshot`. Do not re-derive Revenue/EBITDA/margin trend analysis
here; if the user wants that, point them to `financials-snapshot` instead of attempting it in this
workflow.

## Tone and rules

Apply `references/analyst-grade-discipline.md`: a cross-document disagreement is reported, never resolved
silently by picking the number that looks right. An unexplained internal inconsistency is evidence against
trusting a source, not a tiebreaker to average away.

Apply `references/conventions.md`: the platform's own EBITDA-role definitions and period-anchor selection
rules, shared verbatim from the system rule package. Use these definitions when mapping an idiosyncratic
label to one of the four EBITDA roles, when judging whether two figures are a genuine discrepancy versus a
named-basis difference, and when comparing Raven's canonical anchor (Step 2.5) against the documents.

All output conforms to `references/language-standard.md` (American spelling, credit-desk register, no
em-dashes, no hype adjectives). Read it and apply it. Do not expose platform plumbing in the body, no raw
tool or field names (`document_filename`, `research_search_analysis`, `report_type`, chunk indices, top_k)
and no search mechanics; name documents the way a person would ("the October 2024 CIP," "KPMG's QofE"),
not by internal identifiers.

**Self-check the AI-speak tells before delivering:**
- Em-dashes are banned. Scan for the character and replace it with a comma, semicolon, or period.
- No verdict-then-hedge. State the finding, then any qualifying detail as its own sentence.
- No hype or empty adjectives ("robust," "well-supported," "clean set of figures"). A finding is a
  statement carrying a figure and a source, not a characterization.
- Headings name content, never function ("The read," "Assessment," "Overview" are defects).

## Project Resolution

- If a project_id is known from earlier in this conversation, use it.
- Otherwise, `deal_list` to resolve by name. One match → use it. More than one → present as a table (Deal,
  Company, Sponsor, Status, Created; no internal IDs) and ask. Do not guess.
- If no deal is named, ask which deal first.

## STEP 0 — Analysis readiness

Call `analysis_get_status(project_id)` unless known. "Ready to view!" → proceed. Anything else → stop,
report the status, and suggest retrying once analysis completes or running `analysis_apply_start`.

## STEP 0.5 — Tool pre-load

`deal_list_documents` and `research_search_analysis` are deferred; if not loaded this conversation,
`tool_search` them first.

## STEP 1 — Document inventory: two parallel paths, not one gate

Call `deal_list_documents(project_id)` and identify which document classes are present: CIM/management
presentation, QofE report, audited financial statements, compliance certificates, lender/sponsor model.

**Cross-class check.** If two or more DIFFERENT classes exist, compare across classes as the primary
check; independent sources make this the strongest form of the test.

**Intra-class check — run this even when only one class exists.** Check whether there is more than one
document within that single class (successive sponsor decks dated at different points in the process: a
CIP, a later management presentation, a merger CIM, an overview deck). Sponsor materials get revised over
a deal's timeline, and a stale figure can persist in an earlier deck even though every document nominally
belongs to the same class. Confirmed live: a deal with only sponsor decks present, no
QofE or audited financials at all, still carried a real ~4% Adjusted EBITDA discrepancy between two earlier
and two later decks. Treating "one class" as "nothing to check" would have missed it entirely.

Only report "nothing to cross-check" when there is truly a single document in the entire deal with no
other document, of any class, to compare it against. More than one document of the same class is exactly
the case the intra-class path exists for; never skip it on the reasoning that it's "all sponsor material
anyway."

## STEP 2 — Search for the same metrics across documents

**Default metric set:** Revenue, Adjusted EBITDA (and EBITDA margin), Capex, Free Cash Flow, and Total
Debt / Capitalization, plus any other metric the user specifically names. This set was widened
deliberately from an earlier narrower default (Revenue and EBITDA only): Capex and Free Cash Flow feed
coverage calculations directly, and Total Debt / Capitalization is exactly the kind of figure that
disagrees between a term sheet and the actual executed credit agreement.

For each metric, run a targeted search and note which document each returned figure comes from. Attribute
every figure to its source document using each result's own `doc_sources[]` entries, not the top-level
chunk, since that is where `document_filename`, `document_category`, and `page_number` actually live in
the response shape. Pull enough results to see the same metric surfaced by more than one document (a
single top result is not enough to see a cross-document pattern). If a chunk's document source is
ambiguous, say so rather than guessing which document it came from — never invent an attribution.

**Presentation-basis discipline — sort before comparing, not after.** The same metric is routinely
disclosed on more than one presentation basis: Historical Actual, Pro Forma (transaction-adjusted, e.g.
synergies or standalone-cost layered in), and Projected/Forecast. Before treating any two figures as
comparable, confirm they sit on the same basis. A historical actual figure and a pro forma or projected
figure for the same metric are not a discrepancy when they differ, they are two different bases doing
their job correctly, and must be labeled as such rather than compared head-to-head. This applies within a
single document too, not just across documents: a lender model routinely shows one figure on a historical
column and a different, larger or smaller figure on a pro forma or 2024E column for the identical line
item, and that difference is never itself a finding.

Apply this per metric:
- **Revenue and EBITDA:** already governed by `references/conventions.md`'s period and EBITDA-role rules
  — use the period type (actual vs. estimate) and the EBITDA role (Reported/Adjusted/PF Adjusted) to sort
  before comparing.
- **Capex:** distinguish disclosed actual Capex (historical or LTM) from a model-projected Capex figure;
  a projected year's Capex is a planning assumption, not evidence about what a historical year actually
  spent, and the two are never compared as if one confirms or contradicts the other.
- **Free Cash Flow:** distinguish Levered FCF (after debt service) from Unlevered FCF (before it), and
  historical/LTM actual from projected; state which definition a source is using before comparing it to
  another source's FCF figure, since "Free Cash Flow" without a stated definition is not a comparable fact.
- **Total Debt / Capitalization:** distinguish at-close pro forma capitalization (the transaction's opening
  debt stack) from a current/actual outstanding balance at a later date; a term sheet's opening structure
  and an executed credit agreement's actual funded amount can legitimately differ by draws or amortization
  since close, and that is not automatically a conflict, though an unexplained difference in the stated
  opening structure itself (two documents disagreeing on Day 1 total debt) is.

## STEP 2.5 — Retrieve Raven's own canonical anchor for each metric

For each metric checked, also search for Raven's own canonical anchor selection (its "conventions" layer:
the platform's own pick of which figure and basis to treat as the anchor, distinct from the raw documents
themselves). A targeted query naming the metric plus "canonical" or "anchor" (e.g. "canonical anchor
EBITDA," "canonical revenue basis") reliably surfaces this; the category will read as `conventions` in the
result and typically states the picked layer, the picked value, and the reasoning in plain language.

Compare Raven's canonical pick against the range of figures found in Step 2:
- **If it matches the most reliable, most current source** (e.g. the latest-dated document, or the one an
  earlier document itself flags as superseding a preliminary figure), say so explicitly. This is a genuine
  confirmation worth stating, not just a non-finding: it means the platform's anchor selection holds up
  against the underlying documents, which the reader should not have to take on faith.
- **If it matches a stale, preliminary, or otherwise less-reliable source instead**, flag this plainly and
  with real weight: it means a downstream figure (a rendered dashboard, a memo, a covenant calculation)
  may be built on the wrong number even though the correct one is sitting in the document set.
- **If Raven's anchor doesn't match anything found in Step 2 at all**, say that too, rather than assuming
  the anchor is right by default because it came from the platform's own layer.

**Never hardcode a question ID for this search, ever.** Prompt IDs in this system get renumbered, and
different views of the same conventions answer have been observed under different ID schemes. Searching by
content and category (`conventions`) survives a renumbering; searching by a specific ID doesn't, and a
future edit that "helpfully" adds a literal Q-number here is a regression, not an improvement.

**Derived metrics get a tie-out check, not a document comparison.** Some metrics in the default set are
not disclosed anywhere as a single stated figure — Unlevered Free Cash Flow (EBITDA minus Capex) is the
clearest example. Where a metric is derived from other figures rather than stated directly, the right
check is confirming the derivation ties correctly to its already-verified inputs, not searching for a
second document that states the same derived number. Name this plainly when it applies: state which
inputs the figure is built from, confirm each traces to a source already checked, and confirm the
arithmetic. Where a disclosed derived figure's own inputs (e.g. a Levered FCF walk's cash interest and cash
taxes) are not separately disclosed at all, that is a coverage gap, not a discrepancy and not a tie-out
failure — report it as exactly that, since it limits how far the figure can be independently checked even
though nothing about it is contradicted.

## STEP 3 — Render

For each metric checked, one block per presentation basis actually disclosed (Historical Actual, Pro
Forma, Projected/Forecast — omit any basis with nothing to show):

**[Metric name] — [Basis] — [Period]**

| Source Document (dated where known) | Value | Basis Notes |
|---|---:|---|
| [Document, e.g. "CIP, Oct 2024"] | | |
| [Document, e.g. "Management Presentation, Dec 2024"] | | |
| [Document, e.g. "Merger CIM"] | | |
| [Document, e.g. "KPMG QofE"] | | |

Only compare figures within the same basis block against each other. A Historical Actual figure and a
Projected figure for the same metric are never compared head-to-head as a potential discrepancy; state the
relationship between them (e.g. "2024E builds off the 2023A base above") in prose if useful, but the
comparison table itself stays within one basis.

Date each source where available. For an intra-class discrepancy, the most common explanation is that a
figure was simply updated between an earlier and later version of the same deck; dating each source is
what distinguishes "the deck was revised" from "an unexplained inconsistency."

- **All sources agree (within immaterial rounding):** one line — "No material discrepancy: all sources
  report [value] within rounding."
- **Sources disagree:** flag it plainly with a **Discrepancy** marker, state the range, and note which
  source is more conservative. The typical independence ordering is audited financials, then QofE, then
  compliance certificate, then CIM/sponsor materials, but confirm that ordering actually fits the specific
  discrepancy rather than applying it by default.
- **Basis difference, not a discrepancy:** when sources diverge because one uses reported EBITDA and
  another pro forma or adjusted, because a diligence-adjusted figure was carried into only one projection
  year, or because one figure sits at an earlier stage of the same walk than another (e.g. before vs. after
  a standalone-cost deduction), label it as a basis difference explicitly and name the mechanism. A basis
  difference is not a red flag and
  should never be rendered as a Discrepancy.

**Raven's canonical anchor, every metric block:** one line stating what Step 2.5 found. If it matches the
most reliable source in the table above, say so as a plain confirmation ("Raven's canonical anchor uses
the [date] [document]'s $X figure, the most current source found here"). If it matches a stale or
less-reliable source instead, flag it as plainly as a Discrepancy, since it means a platform-level figure
may be built on the wrong number. If no canonical anchor was found for this metric, say that plainly too.

Close with one paragraph: how many metrics were checked, how many showed genuine discrepancies (not basis
differences), whether Raven's canonical anchor matched the most reliable source on each metric, and, if
more than one discrepancy exists, which is most credit-relevant and why. If every metric checked came back
clean and every anchor matched, say so, and add the coverage caveat: this reflects the metrics and
documents the search actually surfaced, not a guarantee that no other figure in the deal disagrees.

## Consistency check (mandatory, INTERNAL — a separate pass run AFTER the full render, never shown as a section)

Silent, every time.
1. **Confirm every table attribution traces to an actual retrieved chunk.** A source named in a table but
   not actually returned by Step 2's search is a fabricated attribution; remove it or re-search.
2. **Confirm the closing summary matches the tables above it.** The discrepancy count and the
   "most credit-relevant" call must be traceable to the Discrepancy-marked blocks actually rendered, not a
   separate impression formed while writing the summary.
3. **Confirm the intra-class path actually ran** when Step 1 found only one document class but more than
   one document within it. A skipped intra-class check on a single-class deal is the exact failure mode
   that deal surfaced; re-run Step 1's logic if there's any doubt it was applied.
4. **Re-examine every basis-difference label.** Confirm it names the actual mechanism (different EBITDA
   layer, different period, different adjustment tier), not just an assertion that a difference "must be"
   explainable.
5. **Confirm the Raven-canonical-anchor comparison actually happened for every metric**, not just the ones
   where a discrepancy was already found. A metric with no document-vs-document conflict can still have an
   anchor mismatch; the two checks are independent and both are mandatory.
6. **Confirm no comparison table mixes presentation bases.** A Historical Actual figure sitting in the same
   table as a Projected or Pro Forma figure for the same metric is a basis-sorting failure, not a genuine
   finding; check every table against the periods and bases Step 2 actually classified.

Findings weave into the render in place; nothing labeled "consistency check" reaches the output.

## Final review (mandatory, INTERNAL — the last step, over the whole assembled artifact)

Read the finished piece once more and fix: **tone** (credit-desk register, no hedge-then-verdict, no
X-not-Y); **platform plumbing** (no raw tool, field, or parameter names anywhere in the body); **headings**
(clean, parallel, name content); and a **literal proofread** of every heading, source name, and figure.
Scan literally for the em-dash character and replace each with a comma, semicolon, or period. Confirm the
non-determinism caveat is present if the overall result is clean. Silent; its only evidence is a cleaner
artifact.

## Rules

- Judgment-driven and non-deterministic by design; say so, and never present a clean result as a guarantee
  of full reconciliation.
- Default metric set is Revenue, Adjusted EBITDA (and margin), Capex, Free Cash Flow, and Total Debt /
  Capitalization, plus anything the user specifically names.
- Sort every figure by presentation basis (Historical Actual, Pro Forma, Projected/Forecast) before
  comparing; a difference across bases is never itself a discrepancy, and figures on different bases are
  never placed in the same comparison table.
- Where a metric is derived rather than directly disclosed (e.g. Unlevered FCF from EBITDA minus Capex),
  check it by tying the derivation to its already-verified inputs, not by searching for a second document
  stating the same derived number. Where a disclosed derived figure's own inputs aren't broken out at all,
  report that as a coverage gap, distinct from both a discrepancy and a failed tie-out.
- Run both the cross-class and intra-class paths every time; a single document class is never itself a
  reason to skip the check.
- Never present a basis difference (reported vs. adjusted, pre- vs. post-synergy, different adjustment
  tier or period) as a data-quality discrepancy; label it as a basis difference explicitly.
- Never invent a source attribution; an ambiguous chunk source is stated as ambiguous.
- For every metric checked, also retrieve and report Raven's own canonical anchor selection, and state
  plainly whether it matches the most reliable source found or a stale/less-reliable one; never assume the
  platform's own anchor pick is correct by default. Search by content and category, never by a hardcoded
  question ID, since those get renumbered.
- Do not re-derive Revenue/EBITDA/margin trend analysis here; that is `financials-snapshot`'s job, and this
  skill should point there rather than attempt it.
- No platform plumbing in the body: no raw tool, field, or parameter names.
- Consistency check and final review are mandatory, separate, and silent; the evidence they ran is a
  changed artifact, never a narrated process block.

## Delivery

Render in chat by default. Only produce a Word document if asked; when generating one, use the docx skill
with a title block (deal name, metrics checked, date) and the same per-metric structure as the chat
render. Save to `/mnt/user-data/outputs/` and `present_files`. After delivering, offer one natural next
step: a deeper look at the most credit-relevant discrepancy, checking an additional metric, or the
`financials-snapshot` read if the underlying trend hasn't been pulled yet.
