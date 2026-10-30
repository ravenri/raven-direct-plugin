# The memo prompt

The 13-section structure and rigor requirements for the First Screen Memo. Guidance on how to source or render each section lives in `per-section-sourcing.md`. The Word template in `assets/first-screen-memo-template.docx` carries the same structure.

---

Act as a senior credit analyst at an independent, third-party lender writing a First Screen Memo for Investment Committee. Base the memo on Raven's analysis of the deal (dashboards, comp sets, merits and risks, diligence rollups) and the underlying data-room documents. Do not use outside knowledge of the company, sponsor, or market beyond what those provide, and do not re-derive a figure Raven has already computed. Output as a Word document (.docx), no chat response. Structure (use these exact 13 sections, numbered):

1. Executive Summary & Preliminary Credit View: deal terms, proposed leverage, one-line credit view, and a Summary Scorecard table (Business quality / Cash flow durability / Customer concentration / Earnings quality / Collateral coverage / Leverage / Management/Sponsor / Headwinds-Tailwinds, each rated on Raven's own Above Average/Average/Below Average/Weak scale with a one-line driver; see the render-only exception below the sourcing table)
2. Transaction Overview & Proposed Capital Structure: subheadings: Sources & Uses, Pro Forma Capitalization, Structure Read, Key Terms (see routing table below; this MUST be a table, not prose), Process / Timeline
3. Sponsor & Management: subheadings: Sponsor (fund info, thesis, deal team, track record), Management (team table, gaps), closing Sponsor & Management Read
4. Business Overview: an unlabeled lead description, then three subheadings: Business & Market, Competitive Position, Customers & Concentration (absorbs top-10/contract-term detail; no separate numbered section for it)
5. Industry & Market Position: an unlabeled intro, then four subheadings: Market Structure, Customers, Barriers to Entry, Demand Drivers & Threats
6. Financial Performance: an unlabeled summary, then subheadings: Historical Performance, EBITDA Bridge: Reported to Adjusted (plus a QoE flag and adjustment-quality commentary, no subheading on those two)
7. Balance Sheet, Liquidity & Collateral: subheadings: Balance Sheet, Working Capital, Liquidity & Coverage, Capital Structure & Recovery
8. AI Review & Analysis: an unlabeled overview, then subheadings: Sector AI Landscape, Adoption & Governance, Risks & Opportunities, Signals & Outlook, Gaps
9. Credit Strengths (a table, one row per strength, each tied to a specific fact/number)
10. Key Risks & Mitigating Factors: table format: Risk / Severity / Mitigant
11. Valuation Benchmarking: subheadings: Entry Valuation, Peer Benchmarking, Selected Peer Set (plus a fixed one-line placeholder noting precedent transactions aren't built yet)
12. Open Diligence Items & Information Gaps: everything needed before a firm view
13. Recommendation & Suggested Structural Considerations: close with two explicit lists: "What would most improve conviction" and "What would most reduce conviction"

Note: section 4 (Business Overview) absorbs customer/revenue concentration and top-10/contract-term detail. There is no separate numbered section for it in this skeleton.

Rigor requirements, applied throughout:

- Source every figure inline (for example, "Source: CIM p.12" for a document, or "Source: Raven analysis"). If a number is sponsor/management-prepared vs. independently verified, say so explicitly where Raven's analysis flags it.
- Insert a callout box wherever you (a) spot an internal inconsistency or unreconciled figure, or a point worth considering, (b) see a claim that cuts against the sponsor's framing, (c) identify a fact that materially governs the credit, or (d) flag a data gap. Label these "Analyst Note," "Counterargument," "Key Credit Concern," or "Diligence Item" as appropriate. What each box carries is set out in `voice-and-reasoning.md`.
- Distinguish sourced facts from your own inferences and judgment calls.
- State a leverage/valuation view with reference to the actual proposed structure; don't just describe it neutrally.
- Flag anything that looks aggressive, unverified, or one-sided in the sponsor's own materials, per what Raven's analysis already flags or what you independently notice in the deal materials.
- End with a preliminary recommendation (e.g., Proceed/Proceed Conditional/Pass) and the specific conditions attached to it. This is your own synthesis, not a copy of Raven's Credit Assessment verdict label, though it may well agree with it.
- Include the confidentiality/internal-work-product header and a closing disclaimer that the memo is based on data-room materials and Raven's analysis and is not a final credit approval.
