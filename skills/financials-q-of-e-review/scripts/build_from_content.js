// Builds the review Word document from a content file, keeping content apart from layout.
// usage: node build_from_content.js <content.json> <out.docx>
// The content file lists blocks in document order: { "fn": "para" | "h1" | "bullets" | "numbered" | "table" | "kv4" |
// "noteBox" | "caption" | "basis" | "source" | "label" | "gap" | "title", "args": [...] }. Arguments follow the helpers in eq_docx.js.
const fs = require('fs');
const E = require('./eq_docx.js');
const [, , contentPath, outPath] = process.argv;
if (!contentPath || !outPath) { console.error('usage: node build_from_content.js <content.json> <out.docx>'); process.exit(1); }
const content = JSON.parse(fs.readFileSync(contentPath, 'utf8'));
const children = [];
for (const b of content.blocks) {
  if (typeof E[b.fn] !== 'function') throw new Error('unknown block: ' + b.fn);
  const r = E[b.fn](...b.args);
  if (Array.isArray(r)) children.push(...r); else children.push(r);
}
E.finish(children, { title: content.title, outPath }).then(() => console.log('built', outPath));
