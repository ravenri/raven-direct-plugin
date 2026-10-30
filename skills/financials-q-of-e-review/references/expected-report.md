# The expected report

The contents a quality of earnings (QoE) or financial due diligence report is expected to carry. It was drawn
from four reports and tested on a fifth. The skill reads each report
against this list. Every element ends in one of five coverage states, and the state decides what the output says.
The same list is the basis for the vault prompts, so keep the element IDs stable.

## Coverage states

| State | Meaning | What the output does |
|---|---|---|
| Reviewed | The report presents it and the provider did work on it. | Use it. |
| Not presented | The report is silent and gives no reason. | Say so once, in one sentence, in the section where it belongs. |
| Outside scope | The engagement or scope excludes it. | Say so once and cite the scope statement. |
| In scope, no results shown | The procedures list covers it and no findings appear. | Say so once and add it to Open Items. |
| Not quantified | The report names the item and gives no amount (often marked NQ or n.q.). | State it in the Quality of Earnings text and add it to Open Items. |

Do not render the states as a table. Use them to decide what to write. An absence is not an output by itself:
state a credit-relevant gap once, and leave out an element that does not matter for this deal.

## Elements

**Front matter (F)**
- F1 Provider, client and side (buy or sell)
- F2 Report date and draft or final status
- F3 Scope and procedures performed
- F4 Periods covered and basis of preparation
- F5 Reliance and exclusions

**Quality of Earnings (Q)**
- Q1 Reconciliation from net income or reported EBITDA to adjusted EBITDA, by layer
- Q2 Each adjustment by period, with description
- Q3 Support and testing for each adjustment
- Q4 Whether each adjustment recurs
- Q5 Provider commentary on the earnings trend and drivers
- Q6 Pro forma and run-rate items
- Q7 Items shown outside the figure (illustrative normalizations, forecast ramp-up)

**Growth mechanism, conditional (G)**
- G1 Acquisitions: pre-acquisition earnings, price paid, cost removal, synergies, integration
- G2 New markets or units: ramp-up, start-up losses, break-even

**Revenue Model and Retention (R)**
- R1 Revenue by type, product, channel and geography
- R2 Price and volume drivers
- R3 Customer and supplier concentration
- R4 Retention, churn, contracts, backlog
- R5 Seasonality
- R6 Recognition policy

**Cost Structure (C)**
- C1 Cost of sales by nature
- C2 Operating expenses by nature
- C3 Headcount and compensation
- C4 Pass-through costs
- C5 One-time against run-rate cost
- C6 Capital expenditure

**Financial Statement Review (S)**
- S1 Reconciliation to audited statements or trial balances
- S2 Income statement
- S3 Balance sheet
- S4 Debt and debt-like items
- S5 Cash, restricted and unrestricted
- S6 Taxes
- S7 Contingent consideration and earnouts
- S8 Related parties

**Net Working Capital (N)**
- N1 Definition
- N2 Reported to adjusted
- N3 Monthly trend and seasonality
- N4 Average or peg
- N5 Drivers
- N6 Adjustments

**Accounting Structure and Systems (A)**
- A1 Audit status
- A2 Policies and recognition
- A3 Finance organization
- A4 Systems
- A5 Close process and controls
- A6 Pending standards

## Names to search for

Providers label the same element differently. Search on the provider's own labels as well as these: Reported,
Management, Management adjusted, Sell-side adjusted, Buy-side adjusted, Diligence adjusted, Potentially adjusted,
Pro forma adjusted, Run-rate, Add-back, Normalization, Adjusted NWC, Peg, Net debt, Debt-like items, Recast,
Trial balance, Databook. Map the provider's label to one of Reported, Subtotal, Adjusted, Pro Forma Adjusted or Alternative Basis in
the bridge table (the Role column) and say which provider label maps to which.
