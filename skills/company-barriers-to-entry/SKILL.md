---
name: "company-barriers-to-entry"
description: "Produces a descriptive read on the industry's barriers to entry and what gives the borrower's credit a durable reason to exist. Reads Raven's barriers analysis across nine dimensions (regulatory, economies of scale, capital, scarcity of inputs, R&D, intangibles covering brand/IP/switching costs/relationships, network effects, distribution access, learning curve), each with its High/Moderate/Low level, the evidence, the credit implication, and whether the borrower or a competitor holds the advantaged position. Carries the analysis's technology-disruption durability discount and its source-skepticism rule (company claims discounted unless independently corroborated). Where the borrower's materials are thin or self-serving, pulls same-stage public-peer filings (comp_set) to characterize the industry's barriers and test company claims, for information not benchmarking. Use for \"barriers to entry,\" \"moat,\" \"competitive protection,\" or \"switching costs.\" Not a competition read; not cross-stage screening."
when_to_use: "Use for \"barriers to entry,\" \"moat,\" \"competitive protection,\" or \"switching costs.\" Do not use for competitive position or named competitors (Competition), the industry read (Industry Overview), or a cross-deal screen."
---

# Barriers to Entry

Produces a focused, descriptive read on the barriers to entry in the borrower's industry and what
gives the credit a durable reason to exist. It presents Raven's nine-dimension barriers analysis, each dimension carrying its High/Moderate/Low
level, and frames the credit
question around it: which barriers actually protect this borrower, and do they hold over the hold
period. It is a synthesis of an existing analysis, not new extraction.

**The output shape lives in a separate, editable file: `output-structure.md`.** This SKILL.md owns the
procedure (what to read, how to handle the assessed levels, the peer step, the diligence close, Pass
2); `output-structure.md` owns the layout.

## Scope

The industry's barriers to entry and the durability of the borrower's competitive protection. Not a
competition or market-share read (that is its own family), though it names who holds each barrier. Not
cross-stage investment screening. The peer step characterizes the industry's barriers and tests the
borrower's own claims; it never assesses a peer as an investment or substitutes a peer's disclosure
for a borrower fact.

## The reason-to-exist framing

Barriers to entry are the credit's answer to two questions: why does this borrower have a reason to
exist (which barriers protect its revenue, pricing, and position today), and why will it continue to
(do those barriers hold over the hold period, or does something erode them). Frame the read around
those two questions. The per-dimension levels answer the first; the technology-
disruption discount answers the second.

## Language

All output conforms to `references/language-standard.md` (the Raven system language, tone and
banned-words standard): American spelling, credit-desk register, quantify rather than characterize, no
em-dashes, no hype adjectives ("robust," "best-in-class," "differentiated" as a bare claim), no
metaphor, and the house banned-word list. Narrative fields (Overview, section leads) are one to three
sentences; table/row values are crisp fragments that lead with the figure and drop legal suffixes.
Read it and apply it; do not restate its rules here.

## Describe, do not add a rating on top

This skill has a subtlety the others do not: Raven's barriers analysis already assigns each
dimension a High / Moderate / Low level. **Present those per-dimension levels faithfully as Raven's
calls** — they are established findings, not something to re-derive or second-guess. Do NOT add your
own overall barrier rating on top ("strong moat," "weak protection"). The skill's own Overview and
section leads are descriptive: they state which barriers protect the credit and whether they hold,
letting the per-dimension levels carry the ratings. Describe the picture; present the assessed
verdicts; do not rate the whole.

## Project Resolution

- If a project_id is known from earlier in this conversation, use it.
- Otherwise, if the user named a deal, `deal_list` to resolve it. One match → use it. More than one →
  present a table and ask. Do not guess. If no deal named, ask first.

**Skip-if-known (strict):** if `analysis_get_status`, a tile, or any analysis search below is already
available from earlier in this conversation, do not re-call it.

## STEP 0 — Analysis Readiness

`analysis_get_status(project_id)` (skip if already known). "Ready to view!" → proceed. Anything else →
stop, report status, suggest retry or `analysis_apply_start`.

## STEP 0.5 — Staleness

Check `freshness` on the first retrieval carrying it. Confirmed inconsistent in the wild. If present
and stale, surface at top on the conservative reading and note any internal disagreement as a Pass 2
finding. Absent is not a staleness signal.

## Deal-type / entity-scope gate

Barriers are struck on the industry the credit group operates in. Classify the deal live —
`research_search_analysis(project_id, "deal type transaction structure analysis subject entity
scope", report_type="diligence_summary", top_k=3)` — and read the Analysis Subject. Full taxonomy in
`references/deal-type-conventions.md`. Raven's barrier analysis is struck at the deal's defined entity scope, so the
verdicts already reflect the right entity; on a combined group, read the barriers as the combined
group's and note where a dimension's evidence is only one constituent's.

## Tool Pre-Load

Confirm `analysis_get_status`, `dashboard_get`, `research_search_analysis`,
`research_search_documents_by_type`, `research_search_documents`, and `get_source_page` are loaded via
`tool_search` before starting.

## Currency

Every figure in the deal's own stored currency and unit; never assume USD or convert.

## Sourcing discipline

Raven carries a dedicated barriers analysis: a summary record that assesses nine dimensions
with a High/Moderate/Low verdict, credit implication, barrier holder, and source-independence flag for
each, plus leaf records per dimension and a technology-disruption record. **Read these and render
their findings faithfully**, including the per-dimension verdicts and the disruption discount; do not
re-derive them. The Overview, the peer synthesis, and the Pass 2 sweep are Claude's own descriptive
judgment. Trust a clear primary-document answer where the sweep reaches one.

## RETRIEVAL — analysis-first, then peer, adaptive

**Phase 1 — scope and the barriers verdict:**
- Deal-type classification (above).
- If a barriers-to-entry dashboard tile exists, pull it; otherwise (the common case) go to the
  analysis records. Do not assume a tile exists; check and fall back to the analysis search.
- Pull the barriers summary/verdict: `research_search_analysis(project_id, "barriers to entry summary
  verdict regulatory economies of scale capital intangibles network effects", report_type=
  "diligence_summary", top_k=3)`. This record rolls up all nine dimensions with their verdicts.

**Phase 2 — depth on the dimensions that carry the credit, `research_search_analysis(..., top_k=2)` by
content, only where the summary is thin or a dimension is central to this deal:**
1. **Durability / disruption** — "technology disruption barriers at risk erosion emerging technology"
   — the erosion read; which barriers weaken within the hold period. Pull this every time; it answers
   the reason-to-continue question.
2. **Intangibles / switching** — "brand intellectual property switching costs customer relationships
   contractual" — where the deal leans on brand, IP, switching cost, or relationships.
3. **Regulatory** — "regulatory requirements certifications licenses timelines" — where regulation is
   the barrier.
4. **Scale / capital / scarcity** — "economies of scale capital requirements scarce inputs specialized
   labor" — the cost-structure barriers.

Thin is a finding, say so. Do not fire every leaf if the summary already carries the dimension. The
absence of a barrier in a dimension is itself a finding (new entrants face lower friction there), not
a hole to skip.

**Phase 3 — peer commentary (for information, not benchmarking):**
Barriers are inherently industry-level, and the analysis flags company barrier claims as suspect unless
independently corroborated, so peer filings are useful both to characterize the industry's barriers
and to test the borrower's claims. Pull same-stage public-peer filings:
`research_search_documents_by_type(document_types=["comp_set"], query="barriers to entry regulation
capital intensity competition switching costs economies of scale", top_k=6)`. Use the filing text
(risk factors, MD&A, Business/Competition sections) to characterize the industry's structural barriers
and to corroborate or contradict the borrower's own barrier claims. If the deal has no comp access,
the backend returns a permission error — relay it plainly and run the borrower-only read; do not retry.

## Peer commentary discipline

- **Same-stage only, and labeled as peer data.** It characterizes the industry's barriers and tests
  the borrower's claims; it never substitutes a peer's disclosure for a borrower fact.
- **For information, not benchmarking.** The purpose is understanding the industry's barriers and
  pressure-testing company claims, not ranking the borrower against peers.
- **Describe, do not rate the peer.** No view on whether a peer is cheap, expensive, or better run.
- **Attribute every peer point** to its ticker and filing section.

## RENDER — read `output-structure.md` and render exactly to it

Fill every section it defines, in order. Behavioral rules:

- **Lead with a descriptive Overview**, framed on the reason-to-exist question: which barriers protect
  the credit and whether they hold. No overall barrier rating on top of the per-dimension
  verdicts.
- **Present the nine dimensions with each one's High/Moderate/Low level**, the evidence, the
  credit implication, who holds the barrier (borrower or a named competitor), and whether the evidence
  is independent or company-provided. Where a dimension has no material barrier, Low is the finding,
  not a blank.
- **Carry the durability discount.** Name the barriers the analysis flags as eroding within the hold
  period and the mechanism. This is the reason-to-continue answer.
- **Source-skepticism.** Where a High or Moderate barrier rests only on company-provided materials and
  is not independently corroborated, say so; do not present a self-serving barrier claim as settled.
- **Switching gets a short called-out block**, presenting the switching-cost read (contractual
  versus operational, quantified or not). Do not add a buyer-propensity verdict; propensity is not
  reliably knowable from a deal, and the deal's churn/retention data is the honest limit.
- **Lead every section with one to two sentences of narrative** before its table.
- **Peer commentary is a labeled block**, used to characterize the industry and test company claims,
  not to benchmark.
- **Close with the diligence ask** per `references/diligence-gaps-standard.md` (the workbook's Q190
  rubric), scoped to the barriers slice: rank HIGH/MEDIUM/LOW on the Q190 test (the only three tiers;
  no "Material" or "Critical"), one Description and one Diligence Ask per gap, HIGH first. This is the
  slice, not the full-deal register.

## Completeness check

After rendering, note genuinely missing barrier elements as their own lines: any dimension the analysis
could not assess for lack of disclosure, barrier claims resting only on company materials, and the
durability read where disruption is not addressed. Distinguish "not disclosed" from "no material
barrier in this dimension" (the latter is a finding, not a gap).

## PASS 2 — Exploration Mandate (mandatory, separate step)

Pass 1 renders what the analysis already knows. Pass 2 is where you go and look, into the primary
documents and the peer filings, for what the analysis missed or got wrong. It is not a review of the
Pass 1 draft: a summary of your own render ("the source-skepticism rule fired," "the peer step ran")
is not a Pass 2. Report what the looking found, and label each finding by where it came from.

1. **Open the deal documents on the load-bearing claims.** Take the two or three barrier calls the
   credit leans on and search the primary documents (`research_search_documents`, then `get_source_page`
   on the hit) to corroborate or contradict them. Do not restate the analysis's summary of a document;
   open the document. A barrier asserted in the lender deck that the audited financials contradict (a
   patent-lead claim against a fully-amortized, zero-net-book intangible, say) is exactly what this
   step exists to catch.
2. **Go to the peers, and read them for contradiction.** If a comp set exists, pull same-stage peer
   filings (`research_search_documents_by_type(document_types=["comp_set"], ...)`) and read them for
   what contradicts or corroborates the read, not only what fills a blank: a barrier the borrower
   asserts that no peer treats as real, a competitor operating directly in the "hard to enter" market,
   or a durability risk every peer names that the borrower is silent on. If no comp set exists, say so
   plainly and lean harder on step 1; an empty peer step is not a completed step.
3. **Seek the contradiction on the strongest call.** For the single highest barrier in the draft, ask
   what evidence would overturn it, then go look for that evidence. Report it whether or not you find
   it.
4. **2-3 open-ended searches** for a barrier, a competitor, or an erosion risk nothing in the draft
   addresses.
5. **Re-read the Completeness check** for one gap a quick search could close.

**Report what Pass 2 found, even if "nothing new," labeled by source (a deal document, a peer filing,
an open search).** No report means Pass 2 did not happen.

## Rules

- Describe, do not rate the whole. Present the per-dimension levels faithfully; the Overview
  and section leads are descriptive; lead every section with a short narrative.
- Frame the read on the reason-to-exist and reason-to-continue questions.
- Carry the durability discount and the source-skepticism rule from the analysis; do not present an
  uncorroborated company barrier claim as settled.
- A Low verdict is a finding (lower friction for new entrants), not a blank.
- Switching presents the cost read only; no buyer-propensity verdict.
- Peer commentary is same-stage, labeled, for information not benchmarking, never a borrower fact.
- Close with a barriers-slice diligence ask using the Q190 HIGH/MEDIUM/LOW rubric; three tiers only.
- Query by content/topic, never by prompt ID.
- Plain prose, per the language standard.
- Pass 2 is mandatory and reported.

## Delivery

Run Pass 2 first and report its findings. Then `ask_user_input_v0`: "📄 Export as Word doc" /
"Skip — chat is fine". Word → docx skill → `/mnt/user-data/outputs/` →
`present_files`. Default is chat; only produce a file when asked.
