# Spreadsheet Guide: quarterly_returns_template.xlsx

## Inputs (Returns tab; blue cells are editable)
| Cell | Input |
|---|---|
| C6 | Face amount, the position size being modeled ($MM) |
| C7 | Loan spread over SOFR (bps) |
| C8 | Issue price / OID as a price (98 = 2% discount, 100 = none). D8 shows the discount |
| C9 | Hold period, quarters, 1 to 20 |
| C10 | PIK period, quarters (0 = none) |
| C11 | Amortization, % of original face per year (decimal, 0.01 = 1%) |
| C12 | Exit price, % of par (100 = par) |
| C13 | Funding date |
| C14 | Curve shift in quarters, aligned to the nearest quarter start (formula) |
| C15 | Curve status message (formula): read this and relay it |
| I6 | Leverage multiple (1.0x = 50% advance rate) |
| I7 | Implied advance rate (formula) |
| I8 | Leverage spread over SOFR (bps) |
| I9 | Financing line at close (formula) |
| Curve!C6:C25 | Quarterly SOFR forward assumption, quarters 1 to 20 |
| Curve!D6 | Date quarter 1 of the curve starts (curve as-of date) |

## Mechanics
- Quarterly periods, quarter 0 = close. Interest = beginning balance x (SOFR + spread) / 4.
- The curve is shifted forward to the quarter start nearest the funding date (months between the curve date and the funding date, divided by 3, rounded to the nearest whole quarter). Beyond the last curve point the last rate is held flat. A funding date before the curve date applies the curve from quarter 1 (flagged in C15).
- PIK quarters: interest is added to the loan balance; no cash interest, no amortization.
- After PIK: cash interest on the (possibly grown) balance; amortization = face x amortization % / 4 per quarter.
- Exit at the end of the hold quarter: remaining balance x exit price. No exit fee.
- OID: lender funds face x issue price; the full face is owed back.
- Financing line at close = advance rate x funded amount (face x issue price). Each quarter it is paid down by the same share of its original balance that the loan's scheduled amortization represents of the original face. The remainder is repaid at exit. PIK interest does not change it. It pays interest at SOFR + leverage spread on its beginning balance.
- IRR: quarterly IRR on the cash flow row, annualized by compounding ((1 + quarterly)^4 - 1). Nominal (quarterly x 4) is in row 50.
- MOIC: all positive flows divided by all negative flows.

## Result cells
| Cells | Content |
|---|---|
| C48 / D48 | Quarterly IRR, unlevered / levered |
| C49 / D49 | Annualized (effective) IRR, unlevered / levered |
| C50 / D50 | Nominal IRR (quarterly x 4) |
| C51 / D51 | MOIC, unlevered / levered |
| Rows 36 to 45, columns C to W | Quarterly cash flows, quarter 0 to 20 |
| Rows 56 to 65, columns C to H | Annual roll-up, Year 0 to 5 (Initial Funding, Sub line draw, Cash Interest, Mandatory Prepayments, Interest on Sub line, Sub line paydown, Final Payoffs, Sub line Payoff, Total Levered, Total Unlevered) |
| Rows 70 to 74 | Levered sensitivity: column B coupon, C spread, D/E/F = 0.75x/1.0x/1.25x |
| B77 | Reconciliation check for the sensitivity table |

The `Sens` tab is hidden: 15 independent cash flow blocks feeding the sensitivity table.

## Verification history
Checked against an independent calculation on eight scenarios: base, PIK with a 14-quarter hold at issue price 96 and exit price 96, unlevered 20 quarters, 10% amortization at 1.5x leverage, PIK longer than the hold, funding two quarters after the curve date with PIK and 2x leverage, funding after the curve runs out, and funding before the curve date. Every IRR and MOIC matched to 1e-12 or better, and the sensitivity grid matched cell for cell on two scenarios.

Against the annual `loan-returns` template on a flat curve with no OID or amortization, MOIC and the nominal IRR match exactly. Two intended differences: this engine's headline IRR is compounded, so it runs higher than the annual template's, and the financing line here is paid down pro rata while the annual template holds it flat.
