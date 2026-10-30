---
name: "legal-credit-agreement-grid"
description: "Produces a populated credit agreement grid for a deal — the standard-form, term-by-term, tranche-by-tranche grid lenders and sponsors negotiate against (borrower proposed vs. lender response), delivered as an Excel workbook. Follows a fixed 30-section taxonomy spanning the facilities and pricing buildup, financial covenants and security, key definitions, the negative-covenant baskets (debt, liens, available amount, restricted payments, RDP, investments, asset sales), and structural sections (governance, intercreditor, conditions, affirmative covenants, creditor protections, events of default). Populates the Borrower Proposed column from Raven deal_summary and legal_review extraction, each value cited to section/page, leaving Lender Response open for negotiation. Works for a term sheet or a full executed credit agreement. Use for \"credit agreement grid,\" \"term sheet grid,\" \"build the grid,\" or \"extract the terms.\" Negative-covenant sections are headline-level; the covenant deep-dive is a separate skill."
when_to_use: "Use for \"credit agreement grid,\" \"term sheet grid,\" \"build the grid,\" or \"extract the terms.\" Do not use for a few key definitions (Key Definitions), a quick term sheet (Quick Screen), or a comparison across deals."
---

# Legal - Credit Agreement Grid

Produces the standard-form credit agreement grid the leveraged-finance industry negotiates against — every
material term, tranche by tranche, in Borrower Proposed / Lender Response columns — delivered as an
Excel workbook. The industry runs on dueling grids: the bank (or its counsel) produces a grid from
the proposed terms, or the sponsor delivers one upfront, and the deal is negotiated term by term,
round by round. This skill produces that grid, populated from Raven's extraction.

The same grid serves a short-form term sheet, a long-form term sheet, or a full executed credit
agreement — the structure is constant; only how much is filled in and how deep the rows go changes.

## Core assets

- `references/credit-agreement-grid-template.docx` — the **canonical taxonomy**: 30 sections, the exact row
  set and order, with bracketed placeholders (`[__]`, `[●]`) marking deal-specific values. This is
  the authority on structure. The Excel output reproduces this taxonomy as a workbook.
- `references/population-map.md` — maps each section to its Raven source (deal_summary vs.
  legal_review) and records the population discipline. Read it before populating.
- `references/language.py` — the canonical system language, tone and banned-words block. Apply it.

## What this skill produces

An **Excel workbook** (.xlsx), not a Word doc — a terms grid is a living negotiation document
(add lender-response columns, track status, add rounds, filter, compare), which is spreadsheet work.
Structure:

- One worksheet, the 30 sections as banded section headers down the rows, in template order.
- Columns: **Term · Borrower Proposed · Lender Response · Status · Source**.
  - **Term** — the row label from the template.
  - **Borrower Proposed** — populated from Raven extraction (the deal's actual terms), or "Not
    disclosed" where the agreement is silent.
  - **Lender Response** — left blank; the negotiation column the user fills.
  - **Status** — left blank or "Open" (the negotiation-tracking column: Open / Agreed / Issue).
  - **Source** — the section/page citation for the Borrower Proposed value, from the source's own
    citation fields. A source is a document, never a dashboard section.
- Section header rows visually banded; tranche rows (RCF/TLA/TLB/DDTL) grouped under their section.
- Professional font (Arial), frozen header row, sensible column widths, wrapped text.

Read the `xlsx` skill (`/mnt/skills/public/xlsx/SKILL.md`) before building — it governs openpyxl
usage, fonts, and output verification in this environment. Read the `docx` skill only if you need to
re-read the template's structure (`pandoc -t markdown` is enough for that).

## Project resolution

If a project_id is known from earlier in this conversation, use it. Otherwise, if the user named a
deal, `deal_list` to resolve: one match → use it; more than one → present as a table (Deal, Company,
Sponsor, Status, Created — no internal IDs) and ask. Do not guess. If no deal is named, ask first.

## Build steps

1. **Read the template taxonomy.** `pandoc -t markdown references/credit-agreement-grid-template.docx` to
   get the exact 30-section row set and order. This is the row skeleton — do not add, drop, or
   reorder sections; only omit rows per the absence rule below.

2. **Pull the sources.** Per `population-map.md`:
   - `dashboard_get(project_id, tile="deal_summary", ...)` for the buildup (sections 1-6).
   - `dashboard_get(project_id, tile="legal_review", section=<section>)` for the meat (sections
     7-30), section-scoped where the tile supports it, full-tile otherwise.
   - Both deferred — `tool_search` first. Surface any freshness/stale flag the tile returns; if a
     tile isn't generated, say so plainly and populate what's available rather than fabricating.

3. **Populate the grid.** Fill Borrower Proposed from the extraction, each cell cited in Source.
   Apply the absence rule:
   - **Omit** rows that don't apply to the deal's *structure* (no DDTL row without a DDTL, no
     Preferred Equity section without preferred, no second-lien intercreditor rows on a single-tranche
     deal).
   - **Keep and mark** rows where the *absence is a negotiated term* ("Call protection: None," "MFN:
     none," "None (cov-lite)," "Serta protection: not present").
   - Where the agreement is genuinely silent (not structurally N/A, just undisclosed in what was
     retrieved), render "Not disclosed" with the section searched — never leave the raw placeholder,
     never guess.
   - Never populate Lender Response.
   - Faithful extraction only — never infer or fabricate a term or a citation.

4. **Build the workbook** with openpyxl per the xlsx skill, run `recalc.py`, verify it opens clean,
   save to `/mnt/user-data/outputs/`, and `present_files` it. Offer, as next steps: the covenant
   deep-dive (separate skill) on the negative-covenant sections, or the source page behind any term.

## Rules

- The template is the taxonomy — 30 sections, fixed order. Don't invent sections or rows.
- Faithful, cited extraction. Borrower Proposed = what the docs say; Source = the doc/page; never
  infer, never fabricate, never fill Lender Response.
- Absence rule: omit structural non-applicability, preserve negotiated absences (see above).
- Deliverable is .xlsx — a working negotiation grid, not a static doc.
- Negative-covenant sections (17-22) are headline-level; the deep-dive is a separate skill.
- Surface stale/freshness flags; never silently render stale terms.
- Language standard applies to any prose in cells; keep values terse and term-sheet-like.
- ID fields internal — never display unless asked.

## Delivery

Build the .xlsx, verify, save to outputs, present_files. Keep any chat preamble short — the workbook
is the deliverable.
