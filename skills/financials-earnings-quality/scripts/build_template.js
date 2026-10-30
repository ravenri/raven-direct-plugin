// Regenerates assets/Earnings_Quality_Template.docx: layout guidance with bracketed placeholders.
// Every bracket is replaced when a review is written. The template shows layout and style, not the form of the content.
const path = require('path');
const E = require('./eq_docx.js');
const { para, h1, title, caption, source, basis, bullets, numbered, label, gap, table, kv4, noteBox, finish } = E;
const c = [];
c.push(title('Earnings Quality'));
c.push(kv4([
  ['Project and company', '[Project name; company; project used if several matched]', 'Sponsor and sector', '[Sponsor; sector]'],
  ['Anchor period and basis', '[Anchor period; EBITDA basis label]', 'Projection source', '[Model; date; projection period]'],
  ['Peer set', '[Available or not available]', 'Lowest data confidence', '[Level, among the reads used]'],
  ['Reads missing or empty', '[List, or none]', 'Stored reads as of', '[Latest and earliest field dates]']
]));
c.push(gap(80));
c.push(noteBox('Analyst Note: ', '[One to three sentences, only when a trigger applies: history and projection on different EBITDA bases, a read empty or missing, two reads in conflict, or a stale read.]'));
c.push(para('[Terms line, 7.5 pt grey: define EBITDA and any basis labels; state the units; explain "appears" and "suggests" as inference; explain page references and D numbers.]', { size: 15, color: E.GREY, before: 60, after: 60 }));

c.push(h1('1. Executive Summary'));
c.push(para('[One sentence: the conclusion on revenue and EBITDA quality and forecast credibility.]'));
c.push(...bullets(['[One sentence with its key figure. **Bold** the key figures.]', '[One sentence with its key figure.]', '[One sentence with its key figure. About 120 words in all; no questions.]']));

c.push(h1('2. Revenue Quality'));
c.push(para('[One-line conclusion with its figure.]'));
c.push(label('[Subheading, for example Growth and mix]'));
c.push(...bullets(['[One to three bullets, at most two sentences each: growth and mix.]']));
c.push(label('[Subheading, for example Retention]'));
c.push(...bullets(['[Retention and churn by product.]']));
c.push(label('[Subheading, for example Concentration and visibility]'));
c.push(...bullets(['[Concentration; contract visibility.]']));
c.push(label('[Subheading, for example Durability]'));
c.push(...bullets(['[Competitive, barrier and industry evidence on durability. The section totals 4 to 7 bullets.]']));
c.push(basis('Basis: [source documents as the reads cite them; derived D numbers]'));
c.push(caption('Table 2.1', '[Revenue and retention by period]', 'USD in millions (MM)'));
c.push(table([3636, 2475, 2475, 2475, 2475], ['left', 'right', 'right', 'right', 'right'], [
  { k: 'head', c: ['Line', '[P1]', '[P2]', '[P3]', '[LTM]'] },
  { c: ['[Line]', '0.0', '0.0', '0.0', '0.0'] },
  { c: ['[Growth or retention line]', '0.0%', '0.0%', '0.0%', '0.0%'] }
]));
c.push(source('Source: [source documents as the reads cite them]; derived rows (D number). Credit assessment ratings: [lens name and rating only].'));

c.push(h1('3. EBITDA Quality'));
c.push(para('[One-line conclusion with its figure.]'));
c.push(label('[Subheading, for example Margin]'));
c.push(...bullets(['[One to three bullets, at most two sentences each: margin on one basis; gross margin.]']));
c.push(label('[Subheading, for example Cost structure]'));
c.push(...bullets(['[Cost lines and cost position; peer margins where a peer set exists.]']));
c.push(label('[Subheading, for example Cash conversion and reinvestment]'));
c.push(...bullets(['[Cash conversion and reinvestment; structural against temporary. The section totals 4 to 7 bullets.]']));
c.push(basis('Basis: [source documents; derived D numbers]'));
c.push(caption('Table 3.1', '[Margins, EBITDA and reinvestment by period]', 'USD in millions (MM)'));
c.push(table([3636, 2475, 2475, 2475, 2475], ['left', 'right', 'right', 'right', 'right'], [
  { k: 'head', c: ['Line', '[P1]', '[P2]', '[P3]', '[LTM]'] },
  { c: ['[Line]', '0.0', '0.0', '0.0', '0.0'] },
  { c: ['[Margin line]', '0.0%', '0.0%', '0.0%', '0.0%'] }
]));
c.push(source('Source: [source documents as the reads cite them]. Credit assessment ratings: [lens name and rating only].'));

c.push(h1('4. Forecast Credibility'));
c.push(para('[One-line conclusion: reasonable, aggressive or conservative, and the comparison behind the judgment.]'));
c.push(...bullets(['[4 to 7 bullets: the largest departures first, each with its figures, the comparison and what would have to be true; then any contradiction between reads and what would resolve it. If history and projection are on different bases, the first bullet says so.]']));
c.push(basis('Basis: [source documents; derived D numbers]'));
c.push(caption('Table 4.1', 'History, projection and benchmark', 'basis and period in each cell'));
c.push(table([1800, 2300, 2300, 2300, 1200, 3636], ['left', 'left', 'left', 'left', 'left', 'left'], [
  { k: 'head', c: ['Metric', 'Historical result', 'Projection', 'External benchmark', 'Departure', 'What would have to be true'] },
  { c: ['Revenue growth', '[Result, period, basis]', '[Result, period, basis]', '[Peer or industry, source]', '[Historical, Peer or industry, Unsupported, Not testable, None]', '[Condition]'] },
  { c: ['Gross margin', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]'] },
  { c: ['EBITDA margin', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]'] },
  { c: ['[Major cost category]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]'] },
  { c: ['[Each key assumption the projections list]', '[ ]', '[ ]', '[ ]', '[ ]', '[ ]'] }
], 17));
c.push(source('Source: [source documents as the reads cite them]. A cell the stored reads do not carry reads "not in the stored read".'));

c.push(h1('5. Priority Diligence Questions'));
c.push(...numbered(['[Question naming the figure or read it comes from. Up to six. Plain numbered list: no framing, no ranking.]', '[Next question.]'], 1));

c.push(h1('Appendix A: Inputs and Conflicts', true));
c.push(para('[One sentence: what the register covers and which reads were missing or empty.]', { keepNext: true }));
c.push(caption('Table A.1', 'Inputs register', ''));
c.push(table([3000, 2100, 3000, 2000, 3436], ['left', 'left', 'left', 'left', 'left'], [
  { k: 'head', c: ['Read (by topic)', 'Period covered', 'Basis', 'Data confidence', 'Date']},
  { c: ['[Historical financials]', '[ ]', '[ ]', '[ ]', '[Field date or "not dated in the freshness record"]'] }
], 17));
c.push(caption('Table A.2', 'Differences between reads', ''));
c.push(table([2200, 2900, 2900, 3436, 2100], ['left', 'left', 'left', 'left', 'left'], [
  { k: 'head', c: ['Item', 'First read', 'Second read', 'Difference or note', 'Type'] },
  { c: ['[Item]', '[Value, read]', '[Value, read]', '[Note; neither is chosen]', '[Numerical conflict, Definition or period difference, or Contradiction between reads]'] }
], 17));
c.push(source('Source: [reads by topic]. If there are no conflicts, say so in one sentence.'));
finish(c, { title: 'Earnings Quality (template)', outPath: path.join(__dirname, '..', 'assets', 'Earnings_Quality_Template.docx') }).then(p => console.log('written', p));
