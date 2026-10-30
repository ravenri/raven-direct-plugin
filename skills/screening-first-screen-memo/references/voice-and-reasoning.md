# Voice, callout boxes, reasoning and length

## Voice

Write as a senior credit professional preparing a memo for Investment Committee. Third person only; never "I," "my," or "our." All prose conforms to `language-standard.md`, Raven's language, tone and banned-words standard, including American spelling and no em-dashes. Name the EBITDA every leverage multiple is struck against, and the status of every synergy or add-back figure (identified, included in LTM-PF, or targeted run-rate). Argue rather than list: lead with the conclusion, support it with the number, name the constraint.

Rating words (Above Average, Average, Below Average, Weak) appear in the Summary Scorecard and the Key Risks severity column. Do not restate them in prose. Quoting a sponsor's own phrase inside a Counterargument box in order to test it is not using the phrase.

Write agentless statements of the analyst's position: "Preliminary credit view: ...," "Committing capital ahead of X is not supportable," "This recommendation is an independent synthesis, not a restatement of Raven's Credit Assessment label."

## Callout boxes

Keep each box to three sentences or fewer: the finding, why it matters to repayment, and where to look next. A box that repeats a numbered item in section 12 points to it by number instead. Boxes about Raven's own data, such as conflicts between Raven outputs, go in the run report and not the memo. Diligence Items appear only in section 12, except where a gap alone changes the recommendation.

No box comments on, reconciles, or interprets the scorecard ratings. Ratings stand on their drivers.

Use a box only where something real is flagged. A clean section needs none, and section 12 carries none. Keep each box short enough to fit the section's page budget. A box reads as the analyst's own reasoning on top of sourced facts: it connects facts already sourced and does not introduce new ones.

- **Analyst Note.** An observation a careful reader should weigh. It covers an unreconciled figure or a conflict between sources, stating which figure the memo uses and why. It also covers a point to consider: something in the facts that bears on the credit but that no source states directly, such as how facts in two different sections interact. Label any figure the analyst computed as "analyst calculation, not disclosed."
- **Key Credit Concern.** A fact that materially governs repayment, followed by where the analysis should look next. Name the metric or exposure the concern points to and why. For example, high leverage points to cash conversion and interest coverage, because debt service is paid from cash, not EBITDA. An EBITDA built on unrealized synergies points to leverage on unadjusted EBITDA and the timing of the savings. A concentrated customer base points to contract terms and renewal dates.
- **Diligence Item.** An open question, with a short note on why it matters to repayment and the specific ask that would close it. Refer to the numbered item in section 12 rather than restating it.
- **Counterargument.** A point that cuts against the sponsor's framing, with the evidence.

## Reasoning and elaboration — the other half of "don't just curate"

Most of the language elsewhere in this skill pushes toward compression: distill, trim,
keep tight, hit the one-page target. Left unchecked, that produces a memo that curates
the vault well but adds nothing of its own — which is a real risk given how much of this
skill is sourcing mechanics. Curating the vault's facts is necessary but not sufficient;
the analyst's own reasoning across those facts is what a senior credit analyst is
actually being paid for, and it's explicitly in scope here.

**Encouraged — reasoning ABOUT verified facts, clearly Claude's own:**
- Connect facts that live in different sections but were never connected by any single
  vault object. On the reference run, nothing in the vault explicitly linked the CFO-role
  ambiguity (Section 3) to the execution risk on the cost-savings program (Sections 1/6)
  — but both are already-sourced facts, and noting that leadership transition risk and
  the credit's single largest execution dependency land in the same window is a genuine
  analytical observation, not a new fact. Look for this kind of connection across every
  section once the facts are gathered, not just within one section in isolation.
- Draw out the implication of a number, not just state it. "Top-10 concentration of 47%
  sits below the peer median of ~71%" is a fact; "that gap is doing real work for the
  credit, because it means no single sourcing decision at a major OEM is likely to move
  the earnings base by itself" is the reasoning a reader actually wants and the vault
  didn't spell out. Both sentences use only verified figures.
- Where a gap itself is informative, say what it's informative OF, not just that it
  exists. "No balance sheet is disclosed" is a fact; "that means recovery analysis in
  this memo rests entirely on the EV/cash-flow view in Section 7, with no independent
  tangible-asset check on it" is the reasoning that makes the gap matter to the reader.
- When length allows (i.e., a section is under its target, not over it), prefer adding
  one more sentence of genuine analytical connection over stopping at the minimum that
  technically satisfies the field's word count. The one-page targets are a ceiling meant
  to prevent bloat, not a floor that excuses thin analysis once the word count is hit.
- Flag inconsistencies in how the SPONSOR presents its own numbers, not just conflicts
  across sources. A worked example: sponsor materials that use 4.9x (TEV/EBITDA) and 5.1x
  (Total Capitalization/EBITDA) for essentially the same transaction without ever bridging
  the two — a careful reader flags that rather than quoting both multiples in different
  sections as if they were interchangeable. This is the kind of catch a human analyst
  reading the deal makes as a matter of course, and this skill should make it too, using
  whichever source (vault or document) surfaces the figures. Look for this pattern whenever
  two figures describing "the same thing" (an entry multiple, a leverage ratio, an EBITDA
  figure) appear on different bases without an explicit reconciliation.
- COMPUTE useful derived figures from disclosed components — don't just report what's
  already computed for you. Two concrete examples worth doing on every deal: (1) if a
  source states a metric's definition (e.g. "FCF = Adj. EBITDA − CapEx") and separately
  discloses the two inputs historically, compute the third figure and check it against
  what's projected forward — this surfaces cases like projected capex (4.5-5.0% of revenue)
  sitting well above the historical range (2.5-5.2%, mostly at the low end), a gap that
  stopping at the disclosed figures would miss. (2) When entry leverage is struck on an
  adjusted EBITDA with a large synergy/addback layer, also compute leverage on the
  *unadjusted* figure sitting right next to it — the gap between multiples (3.9x stated
  vs. ~6.3x on Reported EBITDA here) is itself a data point, not just a qualitative
  "leverage depends on synergies." ALWAYS label the result as your own calculation
  ("analyst calculation, not disclosed"), never as if the source stated it — same
  fact-vs-inference distinction as the rest of this section, applied to arithmetic.
- Explicitly flag timing mismatches between disclosure dates, not just figure
  discrepancies. A customer-concentration table dated "as of FYE 2021A" sitting in a
  memo built mostly on LTM 9/30/2022 financials is not a wrong number — it's simply from
  a different date, often 9-21 months apart — but a reader who doesn't know that will
  treat the two as contemporaneous. State the date each figure is actually as-of whenever
  it differs from the memo's primary anchor period, not just when the underlying number
  itself looks suspicious.

**Still forbidden — this does not loosen anything about facts:**
- Never state a number, date, name, or figure that isn't sourced from the vault or the
  underlying documents (per the Verification discipline protocols above and the Scope
  discipline below). Reasoning connects verified facts; it does not manufacture new
  ones, however plausible-sounding.
- Never present Claude's own inference as if it were a rendered fact. If a connection is
  Claude's synthesis rather than something a source stated, the prose should read that
  way ("this suggests," "taken together, these two facts mean") rather than being folded
  in as if it carried the same evidentiary status as the figures around it. The reader
  should be able to tell, if pressed, which sentences are sourced facts and which are the
  analyst's own reasoning on top of them.
- Do not manufacture a connection or implication that doesn't actually follow from the
  facts, just to add length or seem more analytical. A forced insight is worse than no
  insight — the bar is "genuinely follows from what's already sourced," not "sounds smart."

## Length discipline (read before drafting)

This section is a ceiling, meant to stop the memo from sprawling — it is not license to
stop developing an analytical point once the word count is technically satisfied. Read
it alongside "Reasoning and elaboration" above: fill available room with genuine
analytical connection before you fill it with restated figures or descriptive padding.

HOUSE RULE, applied consistently: one page per section is the standard. Business
Overview (section 4) is the only real exception — it can extend up to 2 pages if
necessary, matching its own explicit house cap ("one and a half pages, two at the very
most"). Other house prompts contain looser language in places (e.g. s07 says "up to two
pages"), but that is not a second exception to honor — the governing policy is one page
everywhere except Business, and every section below is held to that. A "page" here means
prose + any table/chart on it together, not prose alone — a section with a dense table
has less room for prose, not more room overall. Section 7 needs the most deliberate
compression to hit one page despite its four topics/tables (helped on this deal by the
working-capital schedule being naturally sparse); sections 8, 12, and 13 are naturally
thin given confirmed gaps on this deal (no AI deployment); section 11 carries a real peer
table (5 confirmed comps) but stays short because the multiples analysis on that set
hasn't been run yet — none of this needs special handling beyond what's already in the
routing table. If a section is trending long, cut descriptive/scene-setting prose
before cutting the founded read, the risk/merit substance, or a cited figure — the same
trim-order the house prompts specify. Total memo target, based on the section-by-section
pass below: roughly 3,000-3,500 words of prose across all 13 sections (tables and callout
boxes separate).
