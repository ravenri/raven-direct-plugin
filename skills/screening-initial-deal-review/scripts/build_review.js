#!/usr/bin/env node
/*
 * build_review.js: builds the Initial Deal Review Word document.
 *
 * Usage:  node build_review.js <content.json> <output.docx>
 *
 * The content file is a build input written at run time and kept in the working folder. It is not a deliverable and
 * is never shipped with the skill. Shape:
 *   { "title": "Initial Deal Review", "blocks": [ ... ] }
 * Block types:
 *   {"type":"heading","text":"..."}
 *   {"type":"para","text":"...", "bold":false, "italic":false, "small":false}
 *   {"type":"runs","runs":[{"text":"...","bold":true}, ...]}            (a paragraph with mixed bold text)
 *   {"type":"table","widths":[...],"rows":[[cell,...],...],"header":true,"labelCol":false}
 *        cell is a string, or {"t":"...","span":2,"bold":true}
 *        widths must sum to 9936 (US Letter, 0.8 inch margins)
 *   {"type":"note","text":"..."}        shaded Analyst Note; the script adds the "Analyst Note: " prefix
 *   {"type":"source","text":"..."}      italic gray source line under a table
 *   {"type":"list","ref":"gov","items":[{"lead":"Optional bold lead. ","text":"..."}]}   numbered list; each ref restarts at 1
 *   {"type":"spacer"}
 * Layout follows assets/initial_deal_review_template.docx: Open Sans, 9 pt body, gray table headers, shaded notes with
 * a left rule, confidential footer with page number. The template is a guideline, not the canonical form.
 *
 * Guards: the script stops if the content contains an em dash or any of the words Raven, vault, dashboard, or if a
 * table's widths do not sum to the page width.
 */
const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, ShadingType,
  BorderStyle, AlignmentType, Footer, PageNumber, LevelFormat, TabStopType, VerticalAlign
} = require('docx');

const [,, inPath, outPath] = process.argv;
if (!inPath || !outPath) { console.error('Usage: node build_review.js <content.json> <output.docx>'); process.exit(1); }
const content = JSON.parse(fs.readFileSync(inPath, 'utf8'));

// Guards
const flat = JSON.stringify(content);
if (flat.includes('\u2014')) { console.error('Content contains an em dash. Replace it with a comma, period or semicolon.'); process.exit(2); }
const banned = flat.match(/\b(raven|vault|dashboard)s?\b/i);
if (banned) { console.error('Content names the system ("' + banned[0] + '"). Name the underlying documents instead.'); process.exit(2); }

const FONT = 'Open Sans', W = 9936, body = 18, small = 17;
const run = (t, o = {}) => new TextRun({ text: t, font: FONT, size: o.size || body, bold: o.bold, italics: o.italics, color: o.color || '000000' });
const para = (t, o = {}) => new Paragraph({
  spacing: { before: o.before ?? 0, after: o.after ?? 100, line: 264 }, keepNext: o.keepNext,
  children: Array.isArray(t) ? t : [run(t, o)]
});
const heading = (t) => new Paragraph({ spacing: { before: 220, after: 100 }, keepNext: true, children: [run(t, { bold: true, size: 22 })] });
const thin = { style: BorderStyle.SINGLE, size: 4, color: 'auto' };
const borders = { top: thin, bottom: thin, left: thin, right: thin };

function cell(t, w, o = {}) {
  return new TableCell({
    width: { size: w, type: WidthType.DXA }, borders,
    shading: o.fill ? { fill: o.fill, type: ShadingType.CLEAR, color: 'auto' } : undefined,
    margins: { top: 50, bottom: 50, left: 100, right: 100 }, verticalAlign: VerticalAlign.CENTER, columnSpan: o.span,
    children: [new Paragraph({ spacing: { before: 0, after: 0 }, children: [run(t, { bold: o.bold, size: small })] })]
  });
}
function table(b) {
  const widths = b.widths;
  const total = widths.reduce((a, c) => a + c, 0);
  if (total !== W) { console.error('Table widths sum to ' + total + ', expected ' + W); process.exit(3); }
  const rows = b.rows.map((r, ri) => {
    const head = b.header && ri === 0;
    let ci = 0;
    const cells = r.map((c) => {
      const o = typeof c === 'string' ? { t: c } : c;
      const span = o.span || 1;
      const w = widths.slice(ci, ci + span).reduce((a, x) => a + x, 0);
      const label = b.labelCol && ci === 0;
      const out = cell(o.t, w, { fill: head ? 'D9D9D9' : (label ? 'F2F2F2' : undefined), bold: head || label || o.bold, span: span > 1 ? span : undefined });
      ci += span;
      return out;
    });
    return new TableRow({ cantSplit: true, tableHeader: head, children: cells });
  });
  return new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: widths, rows });
}
function note(t) {
  const none = { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' };
  return new Table({
    width: { size: W, type: WidthType.DXA }, columnWidths: [W],
    rows: [new TableRow({ cantSplit: true, children: [new TableCell({
      width: { size: W, type: WidthType.DXA },
      shading: { fill: 'EDEDED', type: ShadingType.CLEAR, color: 'auto' },
      borders: { top: none, bottom: none, right: none, left: { style: BorderStyle.SINGLE, size: 18, color: '5A636A' } },
      margins: { top: 80, bottom: 80, left: 140, right: 140 },
      children: [new Paragraph({ spacing: { before: 0, after: 0 }, children: [run('Analyst Note: ' + t, { size: small })] })]
    })] })]
  });
}

const refs = new Set();
const children = [new Paragraph({ spacing: { before: 0, after: 160 }, children: [run(content.title || 'Initial Deal Review', { bold: true, size: 40 })] })];
let prevWasTable = false;
for (const b of content.blocks) {
  if (prevWasTable && (b.type === 'table' || b.type === 'note')) children.push(new Paragraph({ spacing: { before: 0, after: 60 }, children: [] }));
  prevWasTable = (b.type === 'table' || b.type === 'note');
  switch (b.type) {
    case 'heading': children.push(heading(b.text)); break;
    case 'para': children.push(para(b.text, { bold: b.bold, italics: b.italic, size: b.small ? 16 : undefined, color: b.small ? '5A636A' : undefined, before: b.before, after: b.after, keepNext: b.keepNext })); break;
    case 'runs': children.push(para(b.runs.map(r => run(r.text, { bold: r.bold })), { before: b.before })); break;
    case 'table': children.push(table(b)); break;
    case 'note': children.push(note(b.text)); break;
    case 'source': children.push(new Paragraph({ spacing: { before: 60, after: 120 }, children: [run(b.text, { italics: true, size: 16, color: '5A636A' })] })); break;
    case 'list':
      refs.add(b.ref);
      b.items.forEach(it => children.push(new Paragraph({ numbering: { reference: b.ref, level: 0 }, spacing: { before: 0, after: 80, line: 264 },
        children: it.lead ? [run(it.lead, { bold: true }), run(it.text)] : [run(it.text)] })));
      break;
    case 'spacer': children.push(new Paragraph({ spacing: { before: 0, after: 60 }, children: [] })); break;
    default: console.error('Unknown block type: ' + b.type); process.exit(4);
  }
}
const mkRef = (reference) => ({ reference, levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 400, hanging: 400 } } } }] });
const doc = new Document({
  creator: 'Initial Deal Review', title: content.title || 'Initial Deal Review',
  styles: { default: { document: { run: { font: FONT, size: body } } } },
  numbering: { config: [...refs].map(mkRef) },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1008, right: 1152, bottom: 1008, left: 1152, header: 708, footer: 708 } } },
    footers: { default: new Footer({ children: [new Paragraph({ tabStops: [{ type: TabStopType.RIGHT, position: W }],
      children: [run('Confidential: internal work product', { size: 15, color: '5A636A' }), new TextRun({ children: ['\tPage ', PageNumber.CURRENT], font: FONT, size: 15, color: '5A636A' })] })] }) },
    children
  }]
});
Packer.toBuffer(doc).then(buf => { fs.writeFileSync(outPath, buf); console.log('Built ' + outPath); });
