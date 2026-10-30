# Raven Direct

Raven Direct connects Claude to the Raven platform, the AI platform for corporate credit, built for credit, not adapted for it. Ask in plain language and Claude works directly with the deals, analysis, financial models, dashboards, source documents and portfolio information in your Raven account, without you navigating the Raven application.

It supports the credit lifecycle from first screen through underwriting, financial and legal analysis, and ongoing monitoring. Create deals, upload documents, start analysis, search and read source documents, review results, build reports and models, and work across your portfolio. Through Claude and Cowork, you can also combine Raven's intelligence with your own analysis, research and information from other connected tools.

On top of the connector, the plugin adds more than 45 specialized credit skills, organized around the workflows Raven's analysts use to screen and underwrite a deal and analyze a portfolio. Skills give consistent, repeatable output on common tasks. You are not limited to them: ask Claude anything Raven's data supports.

## What you need

- A Raven account. Raven Direct works with the deals your company has in Raven. To get an account, contact info@ravenri.ai.
- A Claude plan that supports plugins. The plugin works in Claude chat, Cowork and Claude Code.

## Get started

1. Add the Raven Direct plugin from the Claude directory.
2. Open the plugin's **Connectors** tab, connect **Raven Direct**, and sign in with your Raven account. In Claude Code, the connector is added with the plugin; run `/mcp` to sign in.
3. Ask Claude about one of your deals, for example "Run an initial deal review on Project Z". Claude picks the matching skill. In Claude Code you can also run a skill by name, such as `/raven-direct:screening-initial-deal-review`.

## What it can do

**Screening**

- **Initial Deal Review**: the first structured read on a new deal, from capital structure through to open diligence items.
- **Top 5 Merits and Risks**: the five strongest reasons to do the deal and the five biggest reasons not to, with mitigants.
- **Diligence Gaps**: what is still missing from the deal's materials, by category, with the request that would close each gap.
- **Diligence Focus Areas**: the questions worth running down before investment committee, ranked, each with a next step.
- **Diligence Meeting Prep**: questions for a management meeting, expert call or reference call, or a document request list, built from the deal's own open gaps.
- **Credit Assessment**: the deal's credit rating and scorecard, with the preliminary recommendation.
- **Credit Assessment Memo**: the full Credit Assessment as a Word document, factor by factor, with the metrics to watch.
- **Lightning Round Q&A**: the questions a senior credit investor would press on, ranked by what matters to repayment.
- **Management Team**: who runs the business, their track record, and any gap at the top.
- **First Screen Memo**: a full first screen memo drawn from the analysis and the underlying documents.

**Deal terms**

- **Quick Screen**: the term sheet and at-close capital structure, flagged for anything that needs a closer look.
- **Loan Returns**: unlevered and levered IRR and MOIC for a single position, with the full cash flow.
- **Loan Coverage**: loan-to-value, leverage, interest coverage and cash flow after debt service, year by projected year, as a Word document.
- **Test Covenants**: the covenant package tested against a model scenario, with an EBITDA breakeven and stress grid.
- **Maturity Schedule**: debt maturities by tranche, with the balance outstanding at each and any refinancing need.

**Company**

- **Business Overview**, **Industry Overview**, **Barriers to Entry**, **Customer Diligence**, **Suppliers and Supply Chain**, **Competition**, **Peer Set**, **Commodity Exposure**, **Cyclicality**, **Other Risks**, **AI Review** and **Software Tearsheet**: the company, its market and its risks, each as its own read.

**Financial analysis**

- **EBITDA and Cap Table**, **Financials Snapshot**, **Current Period Results**, **Document Conflict Check**, **Historical Balance Sheet**, **Income Statement and Cash Flow**, **FX Exposure**, **Projections (Base Case)**, **Interest Rate Risk**, **Capex Analysis**, **Earnings Quality Review** and **Q of E Review**: the deal's numbers, period by period, with the source of each figure.

**Legal and documentation**

- **Credit Agreement Grid**: every material term, tranche by tranche.
- **Key Definitions**: the agreement's key defined terms and structural protections, in plain language.
- **Compare Loan Agreements**: terms and creditor protections compared across two to four deals.
- **Basket Capacity**: an interactive view of how the debt, lien and distribution baskets work together.

**Portfolio analysis**

- **Leverage Screen**: ranks your whole book by net leverage against a threshold you set, as an Excel workbook, with a drill-down into any one deal.
- **Closed Deal Metrics**: every closed deal by year with date, sponsor, sector, business and amount, with totals by year, sector and sponsor, as an Excel workbook.
- **Deals at a Glance**: key terms for every closed deal by year, with averages by year and sector, as an Excel workbook.
- **Deal Compare**: two deals side by side as a PDF, with headline terms, capital structure and paydown charts, a rated scorecard, and the repayment and screening view.

Results come back in the conversation. Many skills also offer a Word document or an Excel workbook.

## Example prompts

- "Show me my deals in Raven."
- "Run an initial deal review on Project Z."
- "What are the top five merits and risks on Project Z?"
- "Show me the loan coverage for Project Z."
- "Test the covenants on Project Z against the base case."
- "Compare the credit agreements for Project Z and Project Y."

## Data and privacy

- **What the plugin contains.** Instructions for Claude (skills), document templates, a few helper scripts, and the address of the Raven Direct connector: `https://mcp.ravenrisk.ai/mcp`. The plugin itself stores no data.
- **Where data goes.** The skills call only the Raven Direct connector, signed in as you, and see only the deals your Raven account can access. If you combine Raven with other tools you have connected in Claude, that is your choice, and those tools are governed by their own terms. Deal data stays in your company's Raven account under your agreement with Raven.
- **What it changes.** Most skills only read. Through the Raven Direct connector, Claude can also create a deal, add a portfolio company to Raven Monitoring, upload documents, start Raven's analysis, set up a peer set, create, edit, rename or delete reports and financial models, and apply your firm's underwriting thresholds to a checklist. It does these only when you ask, and most of them wait for you to confirm in Raven before anything is saved.
- **What the connector records.** Raven Direct logs each tool call for support and usage reporting: which tool, the signed-in user, their company, the deal name, timing and whether it succeeded. It does not log your questions, search terms, document content or results. Server logs also hold technical data such as IP addresses, kept for 30 days. See the [privacy policy](https://ravenrisk.ai/privacypolicy) for details, sub-processors and retention.
- **Generated files.** Word and Excel files are built inside your Claude session with Claude's own file tools.

## Important

Raven Platform and Raven Direct support the work of credit professionals and do not provide investment, legal, or credit advice. Outputs may contain errors. Users should verify material figures, assumptions, and conclusions against source documents before relying on them.

## Support

Setup, troubleshooting and more: [Raven Direct documentation](https://ravenrisk.ai/ravendirectdoc).

Questions or problems: info@ravenri.ai.

## License

Proprietary. This plugin may be used only with a Raven account and the Raven service. See [LICENSE](LICENSE).
