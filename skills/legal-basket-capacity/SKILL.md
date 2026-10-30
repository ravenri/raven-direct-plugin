---
name: "legal-basket-capacity"
description: "Builds an interactive HTML artifact modeling how a deal's debt incurrence, liens, and distribution (restricted payments / investments / junior debt payments) baskets work together as one leverage-driven system. Every basket amount, section citation, ratio level, leverage basis, and structural feature (whether free-and-clear and ratio incurrence stack, whether reclassification across baskets is confirmed or absent, whether the liens basket mirrors the general debt basket) is read fresh from Raven's legal_review vault tile for the target deal — nothing is hardcoded from a prior run. Use for \"basket capacity,\" \"debt incurrence explainer,\" \"how do the baskets work together,\" or a request to visualize/interact with negative-covenant basket machinery. Companion to legal-credit-agreement-grid (full negotiation grid) and credit-agreement-snapshot (one-page summary) — this is the intuition layer behind those documents' densest rows, not a replacement for either."
when_to_use: "Use for \"basket capacity,\" \"debt incurrence explainer,\" \"how do the baskets work together,\" or a request to visualize or interact with the negative covenant baskets. Do not use for a term-by-term grid or a definitions read."
---

# Legal - Basket Capacity

Builds a single interactive HTML artifact that lets a reader move one or two leverage inputs and see
debt incurrence, liens, and distribution capacity respond together, the way they do in the actual
agreement. The point is to make the interaction visible — borrowing raises leverage, leverage gates
distributions, and distributions and junior debt payments compete for a shared reservoir — not just
to restate the terms as prose.

This is a **model of one deal's actual agreement**, built fresh each time from that deal's vault data.
It is never a reskin of a previous deal's artifact. Prior builds (Deal A — two-tranche
1L+2L, two separate reservoirs feeding the same three distribution covenants, and a springing covenant
tested only above a revolver-utilization trigger; Deal B — single-tranche, springing
revolver-only test; Deal C — dual-EBITDA-basis, confirmed automatic
reclassification) look structurally different from each other because the underlying agreements are
structurally different. That divergence is the proof the skill is reading each deal correctly, not a
bug to normalize away.

## Required source

`Raven Direct:dashboard_get(project_id, tile="legal_review")` is the only source. Do not reuse
figures, section numbers, or structural assumptions from a previous run of this skill on a different
deal, even ones that seem generic (a $132MM RP basket, a 5.00x gate, "Available Amount" as the
reservoir's name) — those are one deal's actual disclosed terms, not defaults. If a project_id isn't
already known, resolve it via `deal_list` first (one match → use it; multiple → present as a table and
ask; none named → ask).

## House rules (never violate these)

1. **Never approximate one leverage basis from another with an invented multiplier.** First lien,
   secured, and total leverage each get their own independent slider, even if that means three sliders
   instead of one. Don't derive "total leverage ≈ first lien + 1.2x" or similar.
2. **Never default slider starting values to the deal's actual reported position.** This is agreement
   analysis, not performance monitoring — starting values should sit at a neutral, illustrative point
   (e.g. mid-range or the covenant gate itself), not wherever the borrower currently sits.
3. **Never wire interest expense or a rate assumption into any output.** Nothing in the model should
   make debt service, cash interest, or an interest-rate curve a dependency of basket capacity.
4. **Never use "Available Amount" (or "Cumulative Amount" or any other generic capacity term) as a
   label unless the agreement actually uses that defined term.** Use the deal's own defined term. If
   the agreement's term is unclear from the excerpts, flag it rather than guessing.
5. **Every default value needs a traceable source** — a section citation, a stated derivation, or an
   explicit illustrative label. No unlabeled magic numbers.
6. **Write for experienced credit professionals.** Declarative sentences, no rhetorical questions, no
   hand-holding, no explaining what a covenant is.
7. **When a deal has more than one builder/reservoir basket feeding the same set of covenants**
   (e.g. a Cumulative Amount built from ECF/NI *and* a separate Cumulative Equity Amount built from
   equity proceeds, both usable across RP/Investments/JDP), render each reservoir once as its own
   shared pool — never duplicate a reservoir's balance into every consuming card. Each distribution
   card's headline figure is that covenant's own fixed basket only; state explicitly that the shared
   reservoirs are drawn down by whichever covenant uses them first and are not additive on top of each
   card's own number. This is the general form of refinement #2 below — it applies however many
   reservoirs a given deal actually has, not just one.
8. **When a financial covenant is tested only above or below a separate trigger** (revolver
   utilization crossing a threshold, an EBITDA floor, a leverage-independent condition), model that
   trigger as its own explicit control — a toggle or slider distinct from the leverage slider the
   covenant itself is measured against. Don't fold the trigger into the ratio slider or assume the
   covenant is always live; show plainly whether the covenant is even being tested before showing
   whether it's passed.

## Three standing refinements (apply on every build)

These came out of practitioner review of an early build and now apply to every deal, not just the one
that prompted them:

1. **Split the aggregate headline.** A single "Aggregate" figure at the top of the debt-incurrence
   section is useful for the simple question ("what's my ceiling if I max out everything") but
   misleads if left unqualified — it invites reading the whole number as equally "safe" room. Add a
   one-line sub-caption directly under it: "$X available today without clearing a ratio test" (sum of
   the free-and-clear / general / contribution-style baskets, excluding the ratio layer) vs. "$Y more
   requires headroom under the [x.xx]x [basis] covenant" (the ratio-incremental layer alone).
2. **Never model a computed refill rate for an Available Amount / Cumulative Amount / Builder Basket
   equivalent.** These build mechanisms (retained ECF, 50% Net Income, etc.) are heavily and
   deliberately adjusted deal-by-deal — often negative for years by design, so the sweep never
   triggers — and in practice the number comes off a compliance certificate or a borrower rep, not a
   bottom-up estimate. Model the reservoir's *floor* (the unconditional starter amount) precisely, but
   let the slider above the floor be a free input the reader sets themselves, with an explicit note
   that the build is certificate-sourced, not modeled.
3. **Default to reclassification being the market-typical case, not a hypothetical.** In sponsor-
   backed / private-credit agreements, reclassification of basket usage (e.g. general-basket debt
   reclassifying into the ratio basket after delevering) is closer to the market default than the
   exception. Frame an unconfirmed reclass mechanic as "likely present given the deal type, mechanics
   not yet confirmed against the executed agreement" — never as a speculative, low-probability add-on.
   Two exceptions where confidence should be stated plainly instead of hedged:
   - The agreement **affirmatively confirms** reclassification (cite the section) → state it as
     confirmed, no hedge.
   - The agreement **affirmatively bars** reclassification for a specific basket (an explicit
     carve-out) → state that plainly as the agreement's own exception to its general rule, don't soften
     it into uncertainty.

## Structure to build

Use `assets/template.html` as the starting structure (CSS variables, layout, JS patterns) — swap in
the target deal's own figures, labels, and section citations rather than writing the shell from
scratch. Sections, in order:

1. **Header** — deal name, structure one-liner (facility types, cov-lite vs. maintenance-tested), and
   a lede naming the EBITDA basis/bases used and the source document.
2. **Terms grid** (two columns) — Debt incurrence, Liens, Investments, Distributions & reservoir term,
   plus a full-width Documentation notes group for anything that doesn't fit cleanly (undisclosed
   definitions, no fixed dollar cap, first test date not disclosed, etc.). Use `<span class="flag">`
   for gaps/cautions and `<span class="conf">` for agreement-confirmed features.
3. **Interactive panel**:
   - Leverage/EBITDA sliders (one per basis actually used to gate something in this agreement — don't
     add a slider for a basis nothing gates).
   - Reservoir-floor slider (see refinement #2).
   - Hypothetical draw slider with a sequencing toggle (secured/unsecured) if the agreement's basis
     tests care about lien status.
   - Debt incurrence capacity bar (segmented: free-and-clear / ratio / general) with the aggregate +
     split sub-caption (refinement #1).
   - Liens capacity bar (separate scale from debt $ — a lien permission, not new borrowing).
   - Draw sequencing block (conditional on draw > 0): shows which layers absorb the draw in order, and
     post-draw leverage reads.
   - Distribution capacity reads (RP / Investments / JDP) as three cards with open/shut gate chips,
     each showing its own gate level, its own fixed basket only, and how much more leverage reduction
     is needed to clear the gate. Never fold a shared reservoir's balance into these cards' headline
     figures — see house rule #7.
   - Reservoir bar(s) (the Available-Amount-equivalent, or several if the deal has more than one — see
     house rule #7) with their consuming baskets tagged by citation, rendered once each as shared
     pools, not repeated per consuming covenant.
   - Gate strip summarizing every ratio gate in the agreement at a glance, including a distinct control
     for any covenant that only springs above/below a separate trigger (house rule #8) rather than
     folding that trigger into a leverage slider.
4. **Reading notes** — the two or three things a first-time reader would get wrong without them:
   which leverage basis gates which test, how reclassification actually works here (refinement #3),
   any basket sized identically to another for a stated reason, any basket explicitly walled off from
   reclassification.
5. **Footer** — one line naming the source document (with date) and flagging anything modeled as
   illustrative rather than disclosed.

## Output

Save as `<deal-name>-basket-capacity.html`, copy to `/mnt/user-data/outputs/`, and
`present_files`. Offer to rerun the same build on another deal rather than editing the just-built file
in place when the deal changes — this is a fresh build each time, not a template fill-in.
