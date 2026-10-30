// Builds the software tearsheet Word file from a filled input file.
// Usage: node build_tearsheet.js <input.json> <output.docx>
// The layout, table styles, fixed barrier names and fixed key metric rows live here.
// The input supplies only company facts and prose; it never changes the layout.
const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, ShadingType,
  BorderStyle, AlignmentType, Footer, TabStopType, PageNumber,
} = require('docx');

const [,, inPath, outPath] = process.argv;
const D = JSON.parse(fs.readFileSync(inPath, 'utf8'));
const budgets = JSON.parse(fs.readFileSync(__dirname + '/length_budgets.json', 'utf8'));

const FONT = 'Open Sans';
const NAVY = '1F3A52', GRAY = '5A636A', HDR = 'D9E0E4', SUB = 'E6EAEC', RULE = 'BFC5CA';
const W = 9936;
const warnings = [];

function budget(key, text) {
  const b = budgets[key];
  if (b && text && text.length > b) warnings.push(`${key}: ${text.length} characters, budget ${b}`);
  return text;
}

const run = (t, o = {}) => new TextRun({ text: t, font: FONT, size: o.size || 18, bold: o.bold, italics: o.italics, color: o.color });
const para = (text, o = {}) => new Paragraph({
  children: Array.isArray(text) ? text : [run(text, o)], keepNext: o.keepNext,
  spacing: { before: o.before ?? 0, after: o.after ?? 70, line: 250 },
});
const heading = (text, pageBreak = false) => new Paragraph({
  children: [run(text, { size: 22, bold: true, color: NAVY })], keepNext: true, pageBreakBefore: pageBreak,
  border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: NAVY, space: 2 } },
  spacing: { before: pageBreak ? 0 : 90, after: 50 },
});
const credit = (text) => new Paragraph({
  children: [run('Credit implication. ', { size: 17, bold: true, color: NAVY }), run(text, { size: 17 })],
  spacing: { before: 40, after: 40, line: 250 },
});
const small = (text, o = {}) => new Paragraph({
  children: [run(text, { size: 15, italics: true, color: GRAY })],
  spacing: { before: o.before ?? 20, after: o.after ?? 30, line: 250 },
});

const bd = (c, s = 4) => ({ style: BorderStyle.SINGLE, size: s, color: c });
function cell(text, width, o = {}) {
  return new TableCell({
    width: { size: width, type: WidthType.DXA }, columnSpan: o.span,
    shading: o.fill ? { type: ShadingType.CLEAR, fill: o.fill, color: 'auto' } : undefined,
    margins: { top: 15, bottom: 15, left: 80, right: 80 },
    borders: { top: o.topRule ? bd(NAVY, 6) : bd(RULE), left: bd(RULE), right: bd(RULE), bottom: o.hdr ? bd(NAVY, 10) : bd(RULE) },
    children: [new Paragraph({
      alignment: o.right ? AlignmentType.RIGHT : AlignmentType.LEFT,
      spacing: { before: 0, after: 0, line: 226 },
      children: [run(String(text ?? ''), { size: 16, bold: o.bold || o.hdr, color: o.hdr ? NAVY : undefined })],
    })],
  });
}
function table(widths, header, rows, o = {}) {
  const trs = [new TableRow({ tableHeader: true, cantSplit: true,
    children: header.map((h, i) => cell(h, widths[i], { hdr: true, right: o.numCols && o.numCols.includes(i) })) })];
  rows.forEach(r => {
    if (r.kind === 'group') {
      trs.push(new TableRow({ cantSplit: true, children: [cell(r.cells[0], W, { span: widths.length, fill: SUB, bold: true, topRule: true })] }));
      return;
    }
    trs.push(new TableRow({ cantSplit: true, children: r.cells.map((c, i) => cell(c, widths[i], {
      right: o.numCols && o.numCols.includes(i),
      bold: r.kind === 'total' || r.kind === 'key' || (o.boldFirst && i === 0),
      fill: r.kind === 'total' ? SUB : undefined, topRule: r.kind === 'total',
    })) }));
  });
  return new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: widths, rows: trs });
}

// ---- Fixed content: the nine barrier dimensions, in order ----
const BARRIERS = ['Regulatory requirements', 'Economies of scale', 'Capital requirements', 'Scarcity of input resources',
  'R&D requirements', 'Intangible assets', 'Network effects', 'Distribution and channel access', 'Experience curve'];

// ---- Fixed content: key metric rows (formulas and ranges from software-metrics-reference.md) ----
const METRICS = [
  { group: 'Revenue quality and growth' },
  { id: 'revenue_lines', name: 'Revenue line analysis', how: 'Split of revenue between subscription, term and perpetual license, maintenance, services and consumption', range: 'More subscription and maintenance than perpetual license' },
  { id: 'arr', name: 'Annual recurring revenue (ARR)', how: 'ARR as stated by the company', range: 'ARR growth 20 to 40% (ARR above $200MM); 40 to 60% ($50MM to $200MM)', rangeApplies: 'arr_band' },
  { id: 'billings', name: 'Billings and bookings', how: 'Billings: revenue plus change in deferred revenue. Bookings: revenue plus change in remaining performance obligation', range: 'Bookings are a leading indicator (qualitative)' },
  { id: 'services_mix', name: 'Professional services mix', how: 'Professional services as a share of total revenue', range: 'No greater than 20 to 25%' },
  { group: 'Customers and retention' },
  { id: 'gross_retention', name: 'Gross retention and churn', how: '(Beginning customers less customers lost) / beginning customers', range: 'Gross retention 90%+; churn no more than 10%' },
  { id: 'ndr', name: 'Net dollar retention', how: '(Beginning revenue + up-sells less down-sells less churn) / beginning revenue', range: 'Above 100%; ARR $50MM to $200MM: 110%+; ARR $200MM+: 115%+' , rangeApplies: 'arr_band' },
  { id: 'concentration', name: 'Client concentration', how: 'Revenue from the top clients as a share of total revenue', range: 'Top 10 under 30% preferred' },
  { id: 'smb', name: 'Small and medium-sized business (SMB) exposure', how: 'SMB revenue as a share of total revenue', range: 'SMB clients carry higher risk' },
  { group: 'Profitability, efficiency and cash flow' },
  { id: 'gross_margin', name: 'Gross margin', how: '(Revenue less cost of revenue) / revenue', range: '80%+ for subscription; about 75% blended' },
  { id: 'ebitda_margin', name: 'Adjusted EBITDA margin', how: 'Adjusted EBITDA / revenue', range: 'None' },
  { id: 'rule40', name: 'Rule of 40', how: 'Revenue growth plus free cash flow margin', range: 'Above 40' },
  { id: 'sales_eff', name: 'Sales efficiency', how: 'Lifetime value to customer acquisition cost (LTV to CAC), CAC payback and magic number', range: 'LTV to CAC 3x minimum, 5x healthy; CAC payback 24 months or less ($50MM to $200MM ARR), 18 months or less ($200MM+); magic number above 0.75', rangeApplies: 'arr_band' },
  { id: 'cash_conv', name: 'Cash conversion', how: '(Adjusted EBITDA less capex) / adjusted EBITDA', range: 'None' },
];

const c = [];

// ---- Header ----
c.push(new Paragraph({ children: [run(D.company, { size: 36, bold: true, color: NAVY })], spacing: { before: 0, after: 0, line: 250 } }));
c.push(new Paragraph({ children: [run('Software tearsheet', { size: 22, color: NAVY })], spacing: { before: 0, after: 30, line: 250 } }));
c.push(new Paragraph({ children: [run(D.meta_line, { size: 15, color: GRAY })], spacing: { before: 0, after: 20, line: 250 } }));
if (D.stale_note) c.push(new Paragraph({ children: [run(D.stale_note, { size: 15, italics: true, color: GRAY })], spacing: { before: 0, after: 30, line: 250 } }));
c.push(new Paragraph({ children: [run(budget('italic_line', D.italic_line), { size: 16, italics: true })], spacing: { before: 0, after: 40, line: 250 } }));
if (D.transaction) {
  const t = D.transaction;
  c.push(table([3100, 1600, 2200, 3036], ['Facilities', 'Sponsor equity', 'Total capitalization', 'Leverage (as stated)'],
    [{ cells: [t.facilities, t.sponsor_equity, t.total_capitalization, t.leverage] }]));
} else {
  c.push(small('No financing is described in the materials.'));
}

// ---- Business ----
c.push(heading('Business'));
c.push(para(budget('business_1', D.business[0]), { after: 40 }));
c.push(para(budget('business_2', D.business[1]), { after: 10 }));

// ---- Revenue model ----
const R = D.revenue;
c.push(heading('Revenue model'));
c.push(table([3936, 1900, 1900, 2200], ['Revenue stream', R.col_a, R.col_b, R.col_share],
  [...R.rows.map(r => ({ cells: [r.name, r.a, r.b, r.share] })),
   ...R.totals.map(r => ({ kind: 'total', cells: [r.name, r.a, r.b, r.share] }))], { numCols: [1, 2, 3] }));
c.push(para(budget('revenue_note', R.note), { before: 40, after: 10 }));
c.push(credit(budget('revenue_credit', R.credit)));

// ---- Market position and barriers ----
const M = D.market;
c.push(heading('Market position and barriers to entry'));
c.push(para(budget('market_position', M.position), { after: 40 }));
c.push(table([2750, 1200, 5986], ['Barrier', 'Assessment', 'Evidence'],
  BARRIERS.map(name => {
    const b = M.barriers[name];
    if (!b) throw new Error('Missing barrier dimension: ' + name);
    budget('barrier_evidence', b.evidence);
    return { cells: [name, b.level, b.evidence] };
  }), { boldFirst: true }));
c.push(new Paragraph({ children: [run(`Overall assessment of barriers to entry: ${M.overall}.`, { size: 16, bold: true }), run(' ' + budget('barrier_overall', M.overall_note), { size: 16 })], spacing: { before: 30, after: 10, line: 250 } }));
c.push(credit(budget('market_credit', M.credit)));

// ---- Customers and contracts ----
const C = D.customers;
c.push(heading('Customers and contracts', true));
c.push(para(budget('customers_1', C.p1), { after: 50 }));
c.push(para(budget('customers_2', C.p2), { after: 50 }));
c.push(table([2200, 7736], ['Measure', 'Value'], C.facts.map(f => ({ cells: [f.measure, f.value] })), { boldFirst: true }));
c.push(para(budget('customers_contract', C.contract), { before: 50, after: 10 }));
if (C.named_clients) {
  c.push(table([3936, 2000, 2000, 2000], ['Client', ...C.named_clients.cols], C.named_clients.rows.map(r => ({ cells: r })), { numCols: [1, 2, 3] }));
  if (C.named_clients.gap) c.push(small(C.named_clients.gap));
}
c.push(credit(budget('customers_credit', C.credit)));

// ---- Financial summary ----
const F = D.financial;
c.push(heading('Financial summary'));
const nCols = F.cols.length;
const fw = Math.floor((W - 3036) / nCols);
c.push(table([3036, ...Array(nCols).fill(fw)], ['USD MM', ...F.cols],
  F.rows.map(r => ({ kind: r.key ? 'key' : undefined, cells: [r.label, ...r.vals] })), { numCols: F.cols.map((_, i) => i + 1) }));
c.push(small(F.footnote, { before: 20, after: 10 }));
c.push(para(budget('financial_paragraph', F.paragraph), { before: 40, after: 10 }));
c.push(credit(budget('financial_credit', F.credit)));
c.push(small(F.sources, { before: 10, after: 0 }));

// ---- AI exposure ----
const A = D.ai;
c.push(heading('AI exposure', true));
c.push(para(budget('ai_1', A.p1), { after: 50 }));
c.push(para(budget('ai_2', A.p2), { after: 40 }));
c.push(table([2300, 3500, 4136], ['Exposure', 'Most exposed revenue', 'Basis'], A.table.map(r => ({ cells: [r.exposure, r.revenue, r.basis] })), { boldFirst: true }));
c.push(credit(budget('ai_credit', A.credit)));

// ---- Key issues ----
c.push(heading('Key issues'));
c.push(table([1700, 900, 4636, 2700], ['Issue', 'Type', 'Evidence', 'Credit implication'],
  D.issues.map((x, i) => {
    budget('issue_evidence', x.evidence); budget('issue_implication', x.implication);
    return { cells: [`${i + 1}. ${x.issue}`, x.type, x.evidence, x.implication] };
  }), { boldFirst: true }));

// ---- Key metrics ----
c.push(heading('Key metrics', true));
const rows = METRICS.map(m => {
  if (m.group) return { kind: 'group', cells: [m.group] };
  const v = D.metrics[m.id];
  if (v === undefined) throw new Error('Missing metric value: ' + m.id);
  const how = (v.how_note ? m.how + '; ' + v.how_note : m.how);
  const range = (v.range_override !== undefined) ? v.range_override : m.range;
  budget('metric_value', v.value);
  return { cells: [m.name, v.value, how, range] };
});
c.push(table([1700, 3200, 2736, 2300], ['Metric', 'Company', 'How measured', 'Reference range'], rows, { boldFirst: true }));
c.push(para([run('Open diligence: ', { size: 16, bold: true, color: NAVY }), run(budget('open_diligence', D.open_diligence), { size: 16 })], { before: 80, after: 40 }));
if (D.reconcile_note) c.push(para([run('Figures that do not reconcile: ', { size: 16, bold: true, color: NAVY }), run(budget('reconcile_note', D.reconcile_note), { size: 16 })], { before: 0, after: 0 }));

const footer = new Footer({ children: [new Paragraph({
  tabStops: [{ type: TabStopType.RIGHT, position: 9936 }],
  children: [run('Reference ranges are context, not pass or fail.', { size: 14, color: GRAY }),
    new TextRun({ children: ['\tPage ', PageNumber.CURRENT, ' of ', PageNumber.TOTAL_PAGES], font: FONT, size: 14, color: GRAY })],
})] });

const doc = new Document({
  creator: 'Credit analysis', title: `${D.company} software tearsheet`,
  styles: { default: { document: { run: { font: FONT, size: 18 } } } },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 700, bottom: 700, left: 1152, right: 1152, header: 708, footer: 708 } } },
    footers: { default: footer }, children: c,
  }],
});
Packer.toBuffer(doc).then(b => {
  fs.writeFileSync(outPath, b);
  console.log('built ' + outPath);
  if (warnings.length) { console.log('LENGTH WARNINGS (shorten before delivering):'); warnings.forEach(w => console.log('  ' + w)); }
});
