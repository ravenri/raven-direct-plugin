// Regenerates assets/Q_of_E_Review_Template.docx. The template is a guideline for layout and style:
// bracketed text says what belongs in each place; it is not content to keep.
const path = require('path');
const E = require('./eq_docx.js');
const { para, h1, title, caption, source, basis, bullets, numbered, label, gap, table, kv4, noteBox, finish } = E;
const c = [];
c.push(title('Financial Due Diligence Summary'));
c.push(kv4([
  ['Project', '[Project name; company]', 'Report', '[Provider; report title; draft or final; date]'],
  ['Provider and client', '[Provider (side: buy or sell); client]', 'Periods', '[Fiscal periods and any TTM; year end]'],
  ['Audit status', '[Audit status by period]', 'Reliance', '[Who may rely; scope limits]'],
  ['Direction of provider adjustments', '[Raised, lowered or unchanged the earnings figure; amount]', 'Other documents compared', '[CIM, lender model, others]']
]));
c.push(gap(80));
c.push(noteBox('Analyst Note: ', '[One to three sentences, only when a trigger applies: draft status, later documents that change the report, items shown outside the earnings figure, or the provider\'s own direction of adjustment.]'));
c.push(para('[Terms line, 7.5 pt grey: define EBITDA and any provider labels; state that tables are in USD thousands (K); explain "appears" and "suggests" as inference; explain page references and D numbers.]', { size: 15, color: E.GREY, before: 60, after: 60 }));

c.push(h1('1. Executive Assessment'));
c.push(para('[One-line conclusion on overall earnings quality.]'));
c.push(...bullets(['[Key Finding 1 (favorable or unfavorable): what the diligence established, with its figure and page, then why it matters to a lender.]','[Key Findings 2 to 5, mixing favorable and unfavorable.]']));
c.push(label('Priority Diligence Questions'));
c.push(...numbered(['[Question likely to affect earnings sustainability, liquidity or the transaction; also listed in Open Items.]','[Up to 5 questions. Plain numbered list.]'], 2));
c.push(basis('Basis: [report pages; derived D numbers]'));

c.push(h1('2. Quality of Earnings'));
c.push(para('[One-line conclusion with its figure.]'));
c.push(...bullets(['[4 to 7 bullets, one finding each, at most two sentences: who stands behind each layer of the bridge and what was tested; which adjustments recur, add income, overlap or are not quantified; items shown outside the figure with amount, basis and whether procedures were performed.]']));
c.push(basis('Basis: [report pages; derived D numbers]'));
c.push(caption('Figure 1', '[Composition or bridge chart]', 'USD in thousands (K)'));
c.push(para('[Chart image, 860 px wide. Use only when it shows something the table does not.]', { size: 16, color: E.GREY }));
c.push(source('Source: [report, pages]; [derived grouping (D number)].'));
c.push(caption('Table 2.1', '[Reconciliation by layer]', 'USD in thousands (K)'));
c.push(table([4400, 2000, 1600, 1845, 1845, 1846], ['left', 'left', 'left', 'right', 'right', 'right'], [
  { k: 'head', c: ['Line', 'Identified by', 'Role', '[Period 1]', '[Period 2]', '[Period 3]'] },
  { c: ['[Reported figure]', '[Ledger]', '', '[0,000]', '[0,000]', '[0,000]'] },
  { c: ['[Adjustments by layer]', '[Management]', '', '[0,000]', '[0,000]', '[0,000]'] },
  { k: 'sub', c: ['[Subtotal]', '[Provider]', '[Role]', '[0,000]', '[0,000]', '[0,000]'] }
]));
c.push(source('Source: [report, pages]. Role mapping: [provider label to Reported, Subtotal, Adjusted or Pro Forma Adjusted].'));
c.push(caption('Table 2.2', 'Adjustments by category', 'USD in thousands (K)'));
c.push(table([3200, 900, 900, 900, 1900, 1900, 1900, 1936], ['left', 'right', 'right', 'right', 'left', 'left', 'left', 'left'], [
  { k: 'head', c: ['Adjustment', '[P1]', '[P2]', '[P3]', 'Recurrence', 'Support', 'Economic substance', 'Conditionality'] },
  { k: 'group', c: ['[Layer, for example Management adjustments]', '0,000', '0,000', '0,000', '[Who identified it]', '', '', ''] },
  { c: ['[1. Adjustment name]', '0,000', '(0,000)', '-', '[Recurs or not]', '[Evidence]', '[Cost disappears or is replaced]', '[Depends on future events or not]'] }
], 17));
c.push(source('Source: [report, pages]. [Notes on items with no EBITDA effect or netting to nil.]'));

c.push(h1('3. [Growth section, only when the report gives a mechanism separate attention: for example Acquisitions and Roll-Up or New Markets]'));
c.push(para('[One-line conclusion with its figure.]'));
c.push(...bullets(['[4 to 7 bullets, one finding each, at most two sentences: what grew and at what price or ramp; how the growth enters the bridge; what is forward and untested.]']));
c.push(basis('Basis: [report pages; derived D numbers]'));

c.push(h1('4. Revenue Analysis'));
c.push(para('[One-line conclusion with its figure.]'));
c.push(...bullets(['[4 to 7 bullets, one finding each, at most two sentences: how revenue is earned and what moved it; retention, or the statement that it is not measured with the nearest indicators; seasonality and concentration.]']));
c.push(basis('Basis: [report pages; derived D numbers]'));
c.push(caption('Table 4.1', '[Revenue by type or driver]', 'USD in thousands (K)'));
c.push(table([5336, 2050, 2050, 2050, 2050], ['left', 'right', 'right', 'right', 'right'], [
  { k: 'head', c: ['Line', '[P1]', '[P2]', '[P3]', '[Change or share]'] },
  { c: ['[Line]', '0,000', '0,000', '0,000', '0.0'] },
  { k: 'sub', c: ['[Total]', '0,000', '0,000', '0,000', '100.0'] }
]));
c.push(source('Source: [report, pages]; derived rows (D number).'));

c.push(h1('5. Cost Base'));
c.push(para('[One-line conclusion with its figure.]'));
c.push(...bullets(['[4 to 7 bullets, one finding each, at most two sentences: what drives cost of sales and overhead; what the margin depends on, including cost removals and run-rate items.]']));
c.push(basis('Basis: [report pages; derived D numbers]'));

c.push(h1('6. Working Capital'));
c.push(para('[One-line conclusion with its figure.]'));
c.push(...bullets(['[4 to 7 bullets, one finding each, at most two sentences: what the measure includes and how it moves through the year; what it hides, including restricted cash and timing.]']));
c.push(basis('Basis: [report pages; derived D numbers]'));

c.push(h1('7. Cash Flow and Conversion'));
c.push(para('[One-line conclusion with its figure.]'));
c.push(...bullets(['[4 to 7 bullets, one finding each, at most two sentences: EBITDA-to-cash conversion; capital expenditure; what the report shows about cash generation; where the report has no cash flow statement, say so once and use the nearest figures.]']));
c.push(basis('Basis: [report pages; derived D numbers]'));

c.push(h1('8. Financial and Accounting Matters'));
c.push(para('[One-line conclusion with its figure.]'));
c.push(...bullets(['[4 to 7 bullets, one finding each, at most two sentences: the audit and trial balance reconciliation; the balance sheet, debt, cash and debt-like items, and carried against contractual amounts; who prepared the numbers, the reliance chain, systems, controls and pending standards.]']));
c.push(basis('Basis: [report pages; derived D numbers]'));

c.push(h1('9. Open Items'));
c.push(...numbered(['[One item the report does not show, with the key figure in bold. Other documents: covered or not covered.]', '[Next item. Plain numbered list: no framing, no ranking.]'], 1));

c.push(h1('Appendix A: Differences', true));
c.push(para('[One sentence: what was compared, and every deal document that was not compared with the reason. State when no other deal documents were available.]', { keepNext: true }));
c.push(...bullets(['[Up to three differences that bear on earnings, with figures.]']));
c.push(caption('Table A.1', 'Differences within the report, against the audited statements, and against the deal documents', 'USD in thousands (K)'));
c.push(table([2300, 2600, 3300, 3936, 1400], ['left', 'left', 'left', 'left', 'left'], [
  { k: 'head', c: ['Item', '[Report]', 'Other value', 'Difference or note', 'Source'] },
  { k: 'group', c: ['Within the report', '', '', '', ''] },
  { c: ['[Item]', '[Value (page)]', '[Value]', '[Difference]', '[Source]'] },
  { k: 'group', c: ['Against the audited statements', '', '', '', ''] },
  { c: ['[Item]', '[Value (page)]', '[Value]', '[Difference]', '[Source]'] },
  { k: 'group', c: ['Against the other deal documents', '', '', '', ''] },
  { c: ['[Item]', '[Value (page)]', '[Value]', '[Difference]', '[Source]'] }
], 17, false));
c.push(source('Source: [report; other documents with short names]. [Audited figures are as presented in the report if the statements were not provided.]'));
finish(c, { title: 'Financial Due Diligence Summary (template)', outPath: path.join(__dirname, '..', 'assets', 'Q_of_E_Review_Template.docx') }).then(p => console.log('written', p));
