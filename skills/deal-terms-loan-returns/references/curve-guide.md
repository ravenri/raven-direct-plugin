# SOFR Forward Curve Guide: quarterly

## What the model uses
One rate per quarter for quarters 1 to 20 (`Curve!C6:C25`). The loan accrues at that rate plus its spread, divided by 4. The engine aligns the curve to the quarter start nearest the funding date.

## Bundled curve (as of Oct 16, 2026)
- This is a proxy for forward SOFR derived from overnight SOFR swaps. It is not CME Term SOFR; Term SOFR carries a small basis. Always say so and name the facility's actual base rate.
- Quarter 1: 4.08%, the USD SOFR 3-month swap rate of Oct 15, 2026 (bluegamma.io/usd-swap-rates). Spot overnight SOFR was 3.88% (Oct 16, 2026).
- Quarters starting Dec 31, 2026 / 2027 / 2028 / 2029: forwards of 4.28% / 4.62% / 4.70% / 4.53% (bluegamma.io/sofr-forward-curve, updated Oct 16, 2026).
- Quarters between anchors: straight-line interpolation.
- After Dec 2029: held flat at 4.53%. The free source does not publish beyond 2029, so long holds, and holds funded later than the curve date, lean on this assumption. Say so when it applies.
- A public-source synthesis, not a live dealer quote. Replace it before a live decision.

## Uploading a curve
A two-column CSV, header `Quarter,Rate`, rows for quarters 1 to 20, rates as decimals (0.0407 = 4.07%). See `assets/sofr_curve_quarterly.csv`. Quarter 1 is the first quarter starting on the curve's as-of date; write that date into `Curve!D6` (ask if the file does not say).

Validate before writing it in, and tell the person about any fix:
1. The headers are exactly `Quarter` and `Rate`.
2. Quarters are unique and sequential from 1, with no blank interior points.
3. Rates are decimals. If any value is above 1, treat the column as percents (divide by 100) and confirm with the person.
4. Flag any rate outside 0 to 15% and ask before using it.
5. No more than 20 quarters are used. If there are fewer than 20, hold the last rate flat and say so.
