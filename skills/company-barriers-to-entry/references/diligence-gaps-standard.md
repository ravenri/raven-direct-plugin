# Diligence Gaps standard — Q190 rubric and format

Source: Credit Vault Prompt Workbook, Diligence Gaps (190s) sheet, Q190 "Open Data Gaps" and Q191
"Diligence Focus Areas." Source of truth is the workbook; refresh this copy if it changes. The
suppliers-supply-chain skill's "Diligence Required" wrap-up renders the **supplier/supply-chain slice**
of this format so it is consistent with the platform's own diligence output. It does not reproduce the
full-deal register (that is Q190 / the diligence-gaps skill).

## Priority rubric (the only three tiers used anywhere in the workbook)

Assign each gap HIGH / MEDIUM / LOW on this test and no other:

- **HIGH** — the gap prevents a credit judgment on a material dimension: leverage, coverage, recovery,
  or the durability of the earnings base cannot be assessed without it. (For this skill's slice: input-
  cost pass-through, supply continuity, or the durability of the cost base.)
- **MEDIUM** — the gap constrains confidence but a judgment can be formed with the caveat stated.
- **LOW** — a completeness item; it does not change the credit conclusion.

Do not introduce "Material," "Critical," or any other label. Do not leave a gap unrated. (Note: the
dev-team has flagged that severity labels drift across rendering prompts; this rubric is the canonical
one — use it, do not add a tier.)

## Categories (full Q190 set, for reference)

Company · Industry · Financial · Collateral & Liquidity · Structural. Supplier and supply-chain gaps
fall under **Company** (supply base, concentration, single-source, switching) and **Structural /
Other Risk** (tariffs, country-of-origin, logistics, disruption). This skill's slice does not need to
group by all five; it lists the supplier/supply-chain gaps ranked by materiality.

## Per-gap entry shape (Q190)

- CATEGORY: one of the five above (optional in this skill's slice, since all items are supplier/supply
  chain)
- PRIORITY: HIGH / MEDIUM / LOW
- TOPIC: short label (e.g. "Supplier Concentration," "Country-of-Origin," "Pass-Through Mechanism")
- SOURCE: where it surfaced (Raven's analysis record or the peer/Pass-2 finding)
- DESCRIPTION: one sentence — what specific data point is missing and why it matters to the credit
- DILIGENCE ASK: one sentence — exactly what document, data point, management-call question, or model
  run would close it; be specific (name the document type or the question)

## Output rules (Q190)

- Order by credit materiality, HIGH first.
- Deduplicate: if the same absence surfaces from more than one place, one item, most credit-material
  framing.
- Do not fabricate gaps the read did not surface. Do not include gaps standard and expected for the
  deal type.
- If no gaps remain, state that explicitly.
- American spelling.
- Structured tally: Gaps identified: [n] · By priority: [HIGH n | MEDIUM n | LOW n].

## Focus-area synthesis (Q191, for reference)

Q191 ranks the HIGH-priority gaps plus risk-card focus areas into up to 10 investigative focus areas,
each with a RANK, FOCUS AREA label, CATEGORY, CREDIT MECHANISM (one verdict-first sentence on how it
impairs debt service, recovery, or the earnings base), and 2-3 specific INVESTIGATIVE ACTIONS. This
skill's wrap-up stays at the Q190 gap-register level for its slice; a full focus-area synthesis across
the deal is Q191 / the diligence-focus-areas skill.
