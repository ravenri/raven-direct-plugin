---
name: "screening-management-team"
description: "Pulls a deal's management team read, covering the roster (names, roles, tenure, and prior experience), plus the team's disclosed strengths, risks, and any critical leadership gap, from the Management section of Raven's Business Overview dashboard, each line cited to source. A screening-stage read that answers who runs this business, how long they have been there, where they came from, and what is missing at the top. Renders the dashboard's roster table and its ranked strengths and risks faithfully (never re-ranks or re-characterizes), surfacing its own critical-gap flag (for example, no CEO named or an interim CFO) as the headline where one exists. Does not carry compensation data (not disclosed) and does not draw an org chart."
when_to_use: "Use when the user asks about the management team, who runs this company, the management roster, the bench, sponsor and management, or leadership depth and continuity for a deal."
---

# Management Team

Pulls a deal's management team read from the Management section of Raven's Business Overview dashboard: the roster,
the team's disclosed strengths and risks, and any critical leadership gap. A screening-stage read
answering who runs the business, how long they have been there, where they came from, and what is
missing at the top.

This is a faithful render of a well-structured tile section, not a re-analysis. The tile already
carries a roster table, ranked strengths and risks, and its own critical-gap flag; the skill surfaces
those cleanly and honestly, and does not re-rank, re-characterize, or invent.

The dashboard already renders the exact structure this skill produces — a Management team roster, a
Critical gap callout where one exists, and ranked Disclosed capabilities and Management risks blocks.
Mirror those sections one-to-one; do not add scaffolding on top. This is a summary of what the
dashboard shows, not a re-analysis.

## Language

All output conforms to `references/language-standard.md`, the canonical language, tone, and
banned-words standard. Read and apply it. Do not expose platform plumbing (no "the tile," "the vault,"
prompt IDs). ID fields are internal; never display unless asked.

## What this skill does and does not carry

- **Carries:** the roster (name, role, tenure, prior experience), the tile's ranked strengths
  (Disclosed capabilities) and risks (Management risks), and the critical-gap flag where one exists,
  each cited to source.
- **Drops the Contributions column.** The tile carries a Contributions field, but it is thin and
  mostly filler ("Leads marketing," "Leads the products business") and falls flat. Do not render it as
  a column. Where a single contribution is genuinely meaningful (e.g. "continuity through the
  carve-out," a specific platform rollout), fold it into that person's Experience cell; otherwise drop
  it.
- **Does not carry:** compensation or comp bands (not disclosed in the tile), and a drawn org chart
  (the source references a pro forma org structure document but the tile does not render a chart). Do
  not promise or fabricate either. If asked for comp, say it is not disclosed in the available
  analysis.

## Project resolution

- If the deal is already identified from earlier in this conversation, use it. Otherwise, if the user
  named a deal, look it up by name in the user's list of deals: one match → use it; more than one →
  present as a table (Deal, Company, Sponsor, Status, Created, no internal IDs) and ask. Do not guess.
  If no deal is named, ask first.

## Retrieve

Retrieve the Management section of the deal's Business Overview dashboard. Make sure the Raven
dashboard tool is loaded first. If the dashboard isn't generated yet, stop and tell the user plainly
using the status returned, and say to start the analysis from within Raven if it hasn't run. Do not
fall back to a search of the deal's analysis.

## Render — mirror the dashboard's own sections

**[Company] · Management Team**

**Critical gap** (only if the tile flags one) — lead with it. The dashboard shows a "Critical gap"
callout when leadership is incomplete (no CEO identified, an interim finance leader, an undisclosed
succession plan). Where the tile carries it, state it first and plainly — leadership completeness is
the first thing a credit reader checks on a sponsor-owned or carve-out deal. If the tile flags no gap,
omit this block — do not manufacture one.

**Roster** — the Management team table, as the tile carries it, without the Contributions column:

| Name | Role | Tenure | Experience |
|---|---|---|---|

One row per named executive, in the tile's order. Keep the figures and facts exactly (tenure, years
of experience, prior employers). Where a person's contribution is genuinely meaningful, fold it into
the Experience cell; otherwise leave it out. Do not add an executive the tile doesn't name, and do not
infer a role or tenure the tile doesn't state. Where a field is blank, render it plainly (e.g. "n/d"),
never invented.

**Disclosed capabilities** — the tile's ranked strengths on the team, in its order, each in a
sentence (functional coverage, incumbent continuity, disclosed operating backgrounds). Render them
faithfully; do not re-rank or add.

**Management risks** — the tile's ranked risks, same discipline (incomplete top-of-house, carve-out
standalone build, finance-transition risk, recent bench, integration risk). Faithful to the tile's
ranking and wording, cleaned to the language standard.

**Sources** — cite the tile's own source references (document and page), from the tile's
`Source`/citation fields. A source is a document, not a dashboard section. Omit where the tile gives
none; never invent.

Close with a single "🔗 Open in Raven" link if the dashboard carries one. Omit it if it isn't present;
never construct it.

## Rules

- Faithful render — mirror the dashboard's own sections (roster, critical gap, disclosed capabilities,
  management risks) one-to-one. Keep the roster facts, the strengths/risks ranking, and the gap flag
  exactly as the tile states them. Never re-rank, re-characterize, or invent an executive, tenure, or
  finding.
- Drop the Contributions column — it is thin filler. Fold a genuinely meaningful contribution into the
  Experience cell where one exists; otherwise leave it out.
- Lead with the critical-gap flag where one exists; omit the block where none does (don't manufacture).
- Do not carry comp/comp bands or a drawn org chart — not in the tile. Say "not disclosed" if asked.
- Rewrite the tile's prose to the language standard, but do not change its facts or its ranking.
- Cite sources from the tile's own fields; a source is a document, never a dashboard section.
- ID fields are internal — never display unless asked.

## Delivery

Render in chat. Offer, as a next step, the source page behind a specific person or finding, a related
dashboard (sponsor, business overview), or a Word export. A Word export is only possible if this
session can create files; if it can't, say so and keep it in chat.
