# Deal Type, Analysis Subject and Entity Scope: convention

Canonical taxonomy and scope rules the customer-diligence skill classifies against. The skill reads this
deal's classification live from Transaction Overview (the Deal Type, Analysis Subject and Constituent
Entities fields); the credit subject comes from the same analysis. This file gives the labels and the scope
rules so the skill reasons correctly. If the Transaction Overview definitions change, refresh this copy.

---

## Deal types: classify into exactly ONE

- **REFINANCING**: existing debt repaid or replaced; no change of control, no new sponsor equity.
- **LBO**: a financial sponsor is purchasing the company with a purchase price and new equity; a new
  capital structure is put in place.
- **ACQUISITION**: a strategic or financial acquirer purchases a single target; a change of control,
  but not the classic sponsor-LBO build.
- **ADD-ON**: an existing platform is acquiring a target, funded through the platform's facilities or
  an incremental raise; the platform remains the borrower.
- **MERGER-COMBINATION**: two operating businesses of comparable substance combine into one credit
  group (platform-plus-target of real weight, or a merger of equals); the pro forma is a genuine
  combination, not a small tuck-in.
- **RECAPITALIZATION**: new debt raised or capital structure adjusted without a change in ownership,
  often returning cash to shareholders.
- **GROWTH FINANCING**: new capital primarily to fund organic growth, capex or expansion.
- **OTHER**: state a one-line reason if none fit.

Do not default to an LBO framing. Classify on the primary purpose the documents evidence. Where more
than one characteristic shows, classify on the PRIMARY purpose and note the secondary.

## Analysis subject: single entity or combined group

- **SINGLE ENTITY:** LBO, Acquisition, Refinancing, Recapitalization, Growth Financing, and Add-ons
  where a platform absorbs a small target (the platform is the borrower).
- **COMBINED GROUP:** Merger-Combination, and material Add-ons where the pro forma genuinely combines
  two operating businesses. Name each constituent and its role (platform/acquirer, target/acquired).

Where the subject is a COMBINED GROUP, all downstream financial assembly is struck on the COMBINED
group, never a single constituent. **Do not sum constituents to construct a combined figure the
documents do not present; use the combined presentation the documents give.**

## Multiple perimeters on one entity

A single-entity deal can carry more than one candidate set of financials: a carve-out perimeter and
its parent, an OpCo and a HoldCo, a restricted group and the consolidated group. This is NOT a
combination. Identify each, state which one the credit is extended to, and name the others so they are
not pulled by mistake.

## The entity scope test

- Refinancing, LBO, Recapitalization, Growth Financing → one operating business; no scope test.
- Acquisition, Add-on, Merger-Combination → figures for more than one entity; select the source
  matching the entity the credit is against.

**A single-entity source is the WRONG SCOPE where the credit is against the combined group, EVEN WHERE
IT FOOTS TO 100% ON ITS OWN.** An internally consistent figure for the wrong entity is the most common
form of this error, and no percentage or footing check will catch it. Where only single-entity sources
exist, say so and label which entity each covers. Do not blend them; do not present one entity's figure
as the whole.

**Agreement is not evidence of scope.** Two analyses that quietly read the same wrong entity agree
while both being wrong. Confirm the perimeter against the documents.

**Label is not entity.** A set labeled "Combined," "Consolidated," "Pro Forma" or "Total" may be one
entity's own internal roll-up rather than the deal's credit group. Confirm which entities a set
actually covers before treating it as combined.

**Perimeter discontinuity.** Where the disclosed historical series and the first projected period
differ by a factor organic growth cannot explain, that step change is itself evidence of a perimeter
change. Name both figures, their periods, and the implied change; never report the two as one
continuous history.

## Expected absence versus genuine gap

- Asset purchase: entity-level statements may not exist; asset-level information is the deal's shape,
  not an omission.
- Add-on: a combined HISTORICAL set is usually not disclosed; combined figures typically appear only
  in a model, forward of close.
- Merger-Combination: all three sets: each constituent standalone and the combined group: are
  expected, and a missing one IS a genuine gap.

## Describe, do not assume

Describe only what the documents state. Where something is absent, say "Not disclosed" rather than
inferring it from the deal type. The deal type tells you what to EXPECT; it never tells you what is
true.
