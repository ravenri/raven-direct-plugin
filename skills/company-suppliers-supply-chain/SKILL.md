---
name: "company-suppliers-supply-chain"
description: "Descriptive read on a deal's supply base and supply chain, the upstream mirror of customer diligence. Covers supplier concentration, single-source and country-of-origin exposure, switching and contract terms, input-cost pass-through, and supply-chain flow and resilience, with a chain-flow map and a ranked diligence ask. Fills borrower blanks with same-stage public-peer filings, labeled as peer data. Use for supplier diligence, supplier concentration, single-source risk, supply chain, or input cost and pass-through. Not a customer diligence; not cross-stage screening."
when_to_use: "Use for \"supplier diligence,\" \"supplier concentration,\" \"single-source risk,\" \"supply chain,\" or \"input cost and pass-through.\" Do not use for customer questions (Customer Diligence) or a standalone commodity read."
---

# Suppliers and Supply Chain

A descriptive read on where the borrower's inputs come from and where the supply chain can break. It describes where the risk sits and does not render a summary verdict. Every section opens with one to two sentences of narrative before its table.

The layout lives in `output-structure.md`; render exactly to it. Language follows `references/language-standard.md`. Read `references/deal-type-conventions.md` only when the deal is not a single entity.

## Scope

The borrower's own suppliers and the flow of inputs behind them. Customer concentration and retention belong to customer diligence. Peer filings characterize the stage and fill borrower blanks; they never stand in for a borrower fact and never rate a peer.

## Setup (one pass)

1. Resolve the deal: use a project already known in the conversation; otherwise `deal_list` by name. One match, use it; several, show a table and ask; none named, ask.
2. `analysis_get_status`; anything other than "Ready to view!" stops the read and reports the status.
3. `dashboard_freshness` once. If stale, state it at the top. An absent flag is not a staleness signal.
4. One `tool_search` to load `research_search_analysis`, `analysis_get_question`, `research_search_documents`, `research_search_documents_by_type`. Skip any call whose result is already in the conversation.

## Retrieval

One fetch covers the whole read: `analysis_get_question` with `100,2404,235,2301,510,426`, which are Transaction Overview, Statement Set Inventory, Suppliers, Commodity Risk, Input Costs and Industry Supply Chain & Input Disruption Risk. If any id comes back not found, run one `research_search_analysis` on that topic to find the id, then fetch it whole. Searches return fragments of long answers; fetch by id when a complete answer is needed.

Read the answers as findings. Render their disclosed and not-disclosed calls as stated and do not re-derive them. Quote any gap priority they already carry. The Overview, peer synthesis and Pass 2 are Claude's own judgment.

Handling the stored answers. The skill, not the stored prompts, shapes the output:

1. Skip any table whose rows are all "Not disclosed"; state the gap in one sentence instead.
2. State the 15% supplier and 25% country thresholds only where supplier-level or country spend is disclosed. Where it is not, say "not disclosed" once and do not mention the threshold.
3. Carry at most three supply-chain risks, most material first, and carry each figure once.
4. Size the residual input-cost exposure only in Input Cost & Pass-Through, and label its basis: disclosed actual, management target, or computed. A management savings target is not a measured exposure.
5. Where a stored cost position is "In Line" only because the documents give no evidence, show it as "Not evidenced".

Currency and units: every figure in the deal's own stored currency and scale, in one consistent form ($MM or $B, not both); never convert.

## Entity gate

From Transaction Overview and Statement Set Inventory, read deal type and analysis subject.

- **Single entity** (refinancing, LBO, acquisition, recapitalization, growth, small add-on): proceed.
- **Combined group**: strike supplier figures on the combined group. Label any single-constituent figure. Never sum constituent tables into a combined figure the documents do not present.
- **Carve-out**: the supply base is the carve-out's. Note any input or service still supplied by the former parent under a transition services agreement as an upstream dependency to unwind, separate from third-party supplier risk.

## Peer step (only when borrower data is silent)

When concentration, single-source or country-of-origin is not disclosed, run one `research_search_documents_by_type` on `comp_set` (supply chain, raw materials, pass-through, single source, tariff; top_k 5). If the deal has no comp access, relay the permission error plainly, run the borrower-only read, and do not retry.

- Same-stage only, labeled as peer data, attributed to ticker, filing and section.
- Note the filing period when it differs from the deal documents.
- For information, not benchmarking. A peer naming a shortage means the stage has that exposure, not that the borrower does.

## Render

Follow `output-structure.md`. Rules:

- Describe, do not rate. No strength, weakness or mixed verdict.
- No false all-clears. A dispersed or undisclosed supply base is not "no risk"; name where the offsetting exposure sits. "Not disclosed" and "not applicable" are findings, and every one is stated as such.
- Separate price exposure (pass-through) from availability exposure (single-source, disruption).
- Say each fact once, in the place it belongs. Do not restate in prose what a table shows.
- Name a supplier or customer only where the documents name it.

## Pass 2 (mandatory, reported)

After the draft, at most three `research_search_documents` calls at top_k 4, combined where possible:

1. Confirm the "not disclosed" calls with one targeted search; fold in anything recovered.
2. Stress the single point of failure: an input, sub-tier supplier, plant, country or route whose loss would stop production.
3. Check price against availability. Pass-through neutralizes inflation, not a shortage.
4. Look for one risk nothing in the draft addresses (tariff or export control, a single qualified source, a freight or energy shock, a labor dependency).

Report what Pass 2 found, including "nothing new". An unreported Pass 2 did not happen.

## Delivery

Run Pass 2, then render in chat. Ask once with `ask_user_input_v0`: "Export as Word doc" or "Chat is fine"; add "Save to Raven as a sheet" only if a sheet-saving tool is loaded in the session. Word: use the docx skill with `assets/suppliers-template.docx` as the layout guideline, write to `/mnt/user-data/outputs/`, then `present_files`. The template guides layout and style; it is not the fixed form of the output. Default is chat; produce a file only when asked.
