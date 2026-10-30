# Vault access: primary retrieval, not just verification

The dashboard is a rendering of the underlying analysis. It does not carry everything the analysis has, so
reading the underlying answers directly is a primary retrieval step for this skill, run for every
applicable factor alongside the dashboard pull, not only afterward to check a figure.

Tools (deferred; `tool_search` to load if not already available this conversation):

- **`research_search_analysis`**: search the deal's analyzed answers. Use it to DISCOVER which answer holds
  a factor (read the question name and its `question_id` off a result).
- **`analysis_get_question`**: fetch a named answer whole, unranked, in one call. Use it once the answer is
  found. Search ranks and returns excerpts; this returns the complete answer, so use it for any factor you
  will render.
- **`research_search_documents_by_type`**: search the deal's documents by type. Use it when the analysis does
  not surface a needed fact, or to confirm a figure against the source documents.
- **`get_source_page`**: open the exact source page behind a citation.

## The answers to read, by name

Identify each by name. The numbers below are for lookup only and differ on older runs.

| Name | Current number | Note |
| --- | --- | --- |
| Other Risk Factors Assessment | 2300 | Ranks the live factors; read first |
| Legal & Litigation Risk | 2302 | Includes product liability, compliance and sanctions, employment claims |
| Pension & Legacy Liabilities | 2303 | Includes multiemployer plans |
| Environmental & Remediation | 2304 | Includes climate and physical risk |
| Transaction Situation | 2305 | Older runs carry five separate answers: Carve-out / Separation, Emergence from Bankruptcy, Active Restructuring, Regulatory Approval Conditions, Acquisition Integration (Acquisition Integration may sit in the Other Risk Factors Assessment) |
| Tax Risk | 2310 | Absent on older runs |
| Off-Balance-Sheet and Debt-Like Items | 2311 | Earnouts, deferred consideration, factoring, guarantees, leases; absent on older runs |
| Trade Policy & Tariff Exposure | 2312 | Includes country risk; absent on older runs |
| Business Continuity & Insurance | 288 | Operations; absent on older runs |

Commodity Risk (2301) is read by the Commodity Exposure skill, not here.

## How to use them across the workflow

1. **Retrieval (primary).** Search to find each answer, then fetch it whole with `analysis_get_question`.
   Merge with the dashboard. A fact the answer carries and the dashboard omits is still rendered under its factor.
2. **Second read (verification).** For a figure central to the read, or a gap the closing summary leans on,
   verify with `research_search_documents_by_type` or `get_source_page` against the source documents.
3. **No answer found.** If an answer for a factor does not exist on this run, say "Not assessed on this run."

Scale the number of calls to what each factor needs: a thin dashboard entry on a factor that plausibly
matters warrants a real query; a factor that is already rich and internally consistent needs less.
