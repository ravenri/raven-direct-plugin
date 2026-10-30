# Credit Agreement Grid — Population Map

This maps each section of the canonical template (`credit-agreement-grid-template.docx`, 30 sections)
to the Raven source that populates it, and records the sourcing discipline. The template is the
authority on structure and row order; this map is the authority on where each row's value comes
from. Read both.

## The two sources

- **deal_summary dashboard** — the facilities-and-pricing buildup (sections 1-6): facility sizes,
  tenors, margins, fees, OID, call protection, amortization. These are term-sheet economics, not
  legal-review provisions. Pull via `dashboard_get(project_id, tile="deal_summary", ...)` (the same
  source the Deal Terms Quick Screen uses).
- **legal_review dashboard** — everything from Financial Covenants through Events of Default
  (sections 7-30): covenants, security, definitions, prepayments, the negative-covenant baskets,
  governance, intercreditor, creditor protections, EoD. Pull via
  `dashboard_get(project_id, tile="legal_review", section=<section>)`, section-scoped where possible.

Both are deferred tools — `tool_search` before first use. Both can report a stale-data / freshness
flag; surface it, never silently render stale terms.

## Section-to-source map

| # | Template section | Source | legal_review section (if applicable) |
|---|---|---|---|
| 1 | General | deal_summary + agreement | — (governing law, commitment %) |
| 2 | Facilities | deal_summary | — (tranches, sizes, tenors) |
| 3 | Margins | deal_summary | — |
| 4 | Fees | deal_summary | — |
| 5 | Call protection | deal_summary + legal_review | voluntary prepayments |
| 6 | Amortization | deal_summary | — |
| 7 | Financial covenants | legal_review | covenants |
| 8 | Security & Guarantors | legal_review | security & guarantors |
| 9 | Definitions: EBITDA | legal_review | definitions |
| 10 | Definitions: Indebtedness | legal_review | definitions |
| 11 | Definitions: Liens | legal_review | definitions |
| 12 | Definitions: Excess Cash Flow | legal_review | definitions |
| 13 | Definitions: Events of Default | legal_review | definitions |
| 14 | Definitions: Restricted/Unrestricted Sub | legal_review | definitions |
| 15 | Unrestricted Subsidiary: Designation Mechanics | legal_review | definitions |
| 16 | Mandatory prepayments | legal_review | prepayments |
| 17 | Debt incurrence: permitted debt / liens | legal_review | baskets / incremental |
| 18 | Available amount | legal_review | baskets (available amount) |
| 19 | Restricted payments | legal_review | baskets (RP) |
| 20 | Restricted debt payments | legal_review | baskets (RDP) |
| 21 | Investments | legal_review | baskets (investments) |
| 22 | Asset sales | legal_review | asset sales |
| 23 | Governance & Amendments | legal_review | governance |
| 24 | Assignments & transfers | legal_review | governance / assignments |
| 25 | Intercreditor matters | legal_review | intercreditor |
| 26 | Conditions & Certain Funds | legal_review | conditions |
| 27 | Preferred equity (if applicable) | legal_review | preferred equity |
| 28 | Affirmative covenants | legal_review | affirmative covenants |
| 29 | Creditor protections | legal_review + MANDATORY vault verification | creditor protections (tile) + independent vault query (see below) |
| 30 | Events of default | legal_review | events of default |

Section names on the legal_review tile may vary; if a section-scoped call returns nothing, pull the
full tile and locate the family. The exact section keys aren't guaranteed — discover them from the
tile rather than assuming.

## Population discipline

- **Faithful extraction, cited.** Populate the Borrower Proposed column with what the agreement /
  term sheet actually says, each value carrying its section/page citation from the source's own
  citation fields. Never infer or fabricate a term. This mirrors the legal_review registry's own
  contract ("do not infer, fabricate, or interpret beyond what is explicitly stated").
- **Leave Lender Response blank.** It's the negotiation column — the user fills it. Never populate it.
- **Placeholders stay only where genuinely undisclosed.** If the agreement discloses a value,
  replace the `[__]`/`[●]` with it. If the agreement is silent, render "Not disclosed" (with the
  section searched), not the raw placeholder.
- **Omit vs. flag (the absence rule):**
  - **Omit** a row when it does not apply to the deal's *structure* — e.g. no DDTL row if there is
    no DDTL, no Preferred Equity section if there is none, no second-lien intercreditor rows on a
    single-tranche deal. A structurally-inapplicable row left blank is noise.
  - **Keep and mark** a row when the *absence is itself a negotiated term* — "Call protection: None,"
    "MFN: none," "Financial covenant: none (cov-lite)," "Serta protection: not present." On a terms
    grid these blanks ARE the deal; dropping them hides a real, negotiated outcome. This is the
    judgment the template's "omit, not blank" instruction needs on the credit-read side: omit
    structural non-applicability, preserve negotiated absences.
- **Tranche awareness.** Sections 2-7 break out per tranche (RCF/TLA/TLB/DDTL/other). Populate each
  tranche the deal actually has; omit tranche rows for tranches that don't exist.
- **The negative-covenant sections (17-22) are headline-level here.** The grid carries the basket
  rows at term-sheet depth (capacity, ratio, section ref). The deep-dive skill expands them to full
  sub-clause detail. Don't try to reproduce the full deep-dive in the grid.
- **Section 29 (Creditor protections) — NEVER trust the tile's present/absent flag on its own.**
  Confirmed in live testing (via a related workflow): the `legal_review` tile reports J.Crew and
  Chewy protections as "absent" on deals whose credit agreement plainly contains both, because these
  protections live unlabeled inside the Investments / Asset Sales / subsidiary-designation /
  Release-of-Liens machinery rather than as their own named clause. A tile-only read produces a false
  "not present" that would understate real creditor protection to a reader relying on this grid.
  Before finalizing this section, always run one combined vault query per deal and read the
  underlying sections directly:

  `research_search_analysis(project_id, "creditor protections IP separation transaction unrestricted subsidiary guarantee lien release wholly owned non-pro-rata subordination affected lender", report_type="legal_review", top_k=3)`

  One query is sufficient — these protections are indexed together under the vault's creditor-
  protections category, and a single well-formed query returns all three vectors (J.Crew, Chewy,
  Serta) plus related asset-sale/subordination material in one payload. Only if that combined query
  returns empty on a specific vector, run one targeted follow-up for that vector alone. Populate the
  Borrower Proposed cell from what this query actually finds, not from the tile's own flag — describe
  the mechanic (what the agreement does), cite section and page, and only then tag it with its market
  shorthand ("... aka J.Crew protection") as an annotation on a described, cited provision. Where the
  agreement is genuinely silent on a vector, state that as a gap ("no restriction found"), never a
  bare "absent," since "absent" is exactly the word that misled readers when it came from the tile
  alone.
