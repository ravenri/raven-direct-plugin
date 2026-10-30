# Verification, Pass 2, and end-of-draft checks

## Verification discipline (mandatory — read before writing any field)

These protocols apply to every field in every section, not just the cases that first
surfaced them. Two principles run through them. First, a "not available" from one tool is
not a confirmed gap — it holds only after a targeted search of the deal's analysis
and, for anything material, a document-level check both come back empty, and where a tool
has a paired selection/analysis structure, both halves get checked first. Second, showing
arithmetic validates a sum given its inputs, not the inputs themselves, so anchor figures
get their inputs checked, not just their math. The routing table below carries the worked
examples; this section states the principles once.

**Protocol A — before writing "[Not disclosed]" or "not available" for ANY field:**
1. Check the obvious dashboard tile(s) for this section (per the routing table below).
2. If absent there, run at least one SPECIFIC, targeted search of the deal's analysis
   naming the exact fact (e.g. "sources and uses of funds transaction financing," not a
   broad query that merely touches the topic).
3. If that comes back empty or thin, search the underlying documents directly —
   a search of the deal's source documents with the same specific
   query, or read a specific document page's text if you have reason to
   believe you know where the fact sits (e.g. a terms summary is almost always a single
   page near the transaction overview). This step is not optional or a last resort — a
   confirmed audit against the reference deal's source documents found genuinely material content
   (a real estate collateral slide, segment-specific peer trading multiples, net debt
   figures) that no vault Q&A object surfaced at all, sitting in plain sight in the
   parsed document. Skipping this step means writing "[Not disclosed]" on facts that are
   actually disclosed, just not indexed into a vault Q&A object.
4. Only write "[Not disclosed]" if the document-level search ALSO comes back empty, or
   the source's own object explicitly says so (a field returning literal "null" or "-"
   across every period is a confirmed gap; an empty search result you haven't tried
   rephrasing is not yet a confirmed gap — try at least one rephrase before concluding).
5. Do not skip this protocol because a field "seems like" the kind of thing that's
   usually missing. Sources & Uses looked like an obvious dashboard gap and wasn't.
6. Watch for multi-stage pipelines specifically: a dashboard returning "not available" can
   mean the underlying selection/confirmation step is done but the rendering step never
   ran. The reference deal comp set is the example — the Comp Analysis dashboard said "not
   available," which reads as "no comp set exists," but the comp set view showed the comp
   SET was confirmed and ready (5 named peers) — the comp ANALYSIS dashboard (computed
   multiples) was simply never generated on top of it. For any tool with a paired
   selection/analysis structure (the comp set view vs. the Comp Analysis dashboard is the
   known example), check both before concluding the whole thing is unavailable.

**Protocol B — before using ANY figure that is central to the memo (total debt, total
leverage, total capitalization, anchor EBITDA, entry multiple) — not every minor figure,
but anything the reader would treat as an anchor fact:**
1. A value with shown arithmetic is not automatically more trustworthy than a repeated
   one — check the INPUTS to that arithmetic with the same skepticism you'd apply to a
   bare stated figure. Showing a calculation is not the same as showing the calculation
   is right.
2. Check the Deal Summary dashboard specifically for capital-structure
   anchor facts — it carries a KPI Snapshot, Deal At A Glance, and its own Cap Table, and
   tends to be human-reviewed (look for "User Edit Refresh"/"User Edit Reapply"
   timestamps). But do not treat it as infallible either: on the reference run, this exact
   dashboard's own Cap Table row disagreed with its own Debt Schedule and leverage ratios
   on Term Loan B's size — even a single well-reviewed dashboard can be internally
   self-contradictory. Cross-check within the tile, not just across tiles.
3. When sources conflict, count how many places each version of the figure is consistent
   with the SURROUNDING numbers, not just how many places cite the figure directly. The
   version that makes total debt, total leverage, total capitalization, and the equity
   percentage all foot together across multiple independently-generated surfaces beats
   the version with one impressive-looking derivation and no broader consistency.
4. If time allows, run one additional targeted search on the specific component most
   likely to vary (e.g. "Term Loan B amount size 1400 1600 1800 million" — naming the
   disputed number, not just the tranche) before treating the first figure found as
   settled.
5. Where a genuine conflict remains after this check, render it as an Analyst Note stating
   which figure this memo uses and why, rather than picking one silently or listing both
   with no resolution attempt. But don't over-produce these — if the check above settles
   it with reasonable confidence, use the settled figure cleanly without a note; reserve
   Analyst Notes for conflicts that are genuinely still open after checking.

**Protocol C — read each tile's reliability cues and carry material ones into the memo:**
Tiles expose reliability signals that are not decoration: a `data_confidence` rating
(HIGH / MEDIUM / LOW) and sourcing-incomplete notes (e.g. "computed without a
quality-of-earnings report ... treat as indicative," "thin evidence mode: relies
primarily on Tier 3 sponsor materials"). Where a figure the memo relies on carries a
low-confidence or indicative flag, say so in the prose ("indicative pending QoE,"
"sponsor-sourced, limited independent corroboration") rather than presenting it with the
same weight as a corroborated figure. Confirmed on a second reference deal: the Financial Analysis dashboard was
LOW confidence, the Deal Summary was computed without a QoE, and the Industry Analysis dashboard was in
thin-evidence mode — all three were surfaced in the memo rather than smoothed over. This
is a labeling discipline, not a reason to distrust the figure; it tells the committee how
much weight the number can bear.

**Pari passu structure — check this explicitly before building any cumulative
leverage/LTV walk (Section 2's pro forma cap table, Section 7's capital structure &
recovery table):** tranches that are pari passu with each other sit at the SAME rank and
should show the SAME cumulative multiple/LTV, not an ascending staircase as if each were
sequentially subordinated to the last. On the reference deal, the Deal Summary dashboard's
own Debt Facilities section states directly that the Senior Secured Notes and Senior
Secured Bridge are each "pari passu with Term Loan B" — meaning RCF, TLA, TLB, the Notes,
and the Bridge are all one first-lien layer, not five sequential layers. Check each
tranche's stated pari passu relationships (usually in its own Terms/Summary Tag) before
assuming seniority is purely a function of the order tranches happen to be listed in.

## Exploration mandate — this is a required SECOND PASS, not a mindset (read this before
the routing table below — it matters more)

A routing table can only tell you to look for things someone already thought of. The
material that gets missed is the material no instruction names — a real estate collateral
slide, segment-specific aftermarket peer multiples, net debt figures, 101 soft call terms,
cyclicality data — and it gets found only by reading the documents broadly, not by
following the table alone. The table is a floor of proven starting points, not a ceiling
on where to look.

This exploration has to be a separate, explicit pass, not a mindset carried through the
drafting pass. A principle that lives inside the main pass is optional in practice: once
attention is tight, "keep this in mind throughout" quietly collapses into building the
memo from the vault dashboards alone and calling it done, with the document-level
verification never actually run. Making it a distinct step after a full draft exists is
what keeps it from being dropped. So:

**Pass 1 (drafting):** pull vault dashboards, build the memo, per the routing table below.

**Pass 2 (mandatory, separate, done AFTER a full draft exists — not folded into Pass 1):**
Go back through the completed draft and do ALL of the following before calling the memo
finished. This is not optional, not a nice-to-have, and not satisfied by having "kept it
in mind" during Pass 1:
1. For every field in the draft marked "[Not disclosed]" or "not available," run ONE
   targeted document search (a search of the deal's source documents) to confirm it — per
   Protocol A above. A dashboard's own "Data Gaps" list saying something is missing is a
   claim to verify, not a fact to inherit; dashboards can be wrong about their own
   completeness the same way they can be wrong about a figure. But a gap confirmed once is
   confirmed: if one specific, well-formed search comes back empty, record it as a genuine
   gap and move on — do NOT re-query the same gap from three angles hoping to change the
   answer. The effort belongs in the open-ended searches in step 3, not in re-confirming
   gaps that are already confirmed.
2. For every anchor fact (entry multiple, total debt, EBITDA), confirm it was actually
   cross-checked per Protocol B, not just pulled from the first dashboard that answered.
3. Run at least 2-3 genuinely open-ended document searches with no specific field in
   mind — "what would a careful lender want to know about this deal that nothing in the
   draft addresses yet." This is where the real estate slide and the peer margin chart
   were found on the deal this protocol was built from; skipping this step is how a
   later run missed them entirely on a different deal.
4. Re-read the draft's own Diligence Items and gap list specifically looking for one
   that a two-minute document search could actually close, not just log. If every gap in
   the memo is something Pass 1 already knew about, Pass 2 didn't happen.
Report explicitly, alongside the memo, what Pass 2 found (even if the answer is
"nothing new") — a memo delivered without this report has not had Pass 2 run on it,
whatever the section content looks like.

The specific queries in the routing table below are worked examples of the METHOD, not
an exhaustive list of the only things worth searching for. Every deal will have its own
version of "the thing nobody thought to route to." Finding it is the job, not a bonus,
and it does not happen by accident inside Pass 1 — it happens because Pass 2 ran.

## After producing the memo

Report, alongside the delivered Word document:
- Whether each section's built format matches the template. Walk the 13 sections and confirm every table the template contains is still a table in the finished memo, sections 9 and 10 especially. This check exists because comprehension is not the failure mode: the table instruction is stated clearly, yet sections 9 and 10 have rendered as prose cards on multiple live builds and gone unnoticed through language screens and visual review. Format compliance survives on this end check, not on attention held across a long drafting pass.
- Whether the memo was scanned for first-person language ("I", "my", "our"), em-dashes, plumbing words ("the vault," "the dashboard," "the tile"), and the banned words in `language-standard.md` before delivery. A search of the drafted text for these is a cheap, mechanical way to confirm it rather than trusting attention held throughout a long drafting pass.
- Whether Pass 2 (the mandatory exploration and verification pass above) actually ran: what document searches were run, what was checked and confirmed vs. changed, and what the 2-3 open-ended searches turned up even if the answer was nothing new. A memo delivered without this line item has not had Pass 2 run on it.
- Which dashboards were available vs. thin or empty for this deal. This is itself a data point, not a flaw to smooth over.
- Whether the same figure (anchor EBITDA, leverage multiple) is used consistently across all 13 sections, or drifts. This is the internal-footing check.
- Any point where you had to guess or extrapolate because Raven's analysis did not state something plainly that the 13-section structure asks for (for example, precedent transactions, which Raven does not carry yet).
