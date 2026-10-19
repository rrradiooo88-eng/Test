// Build a Korean treatment .docx from the markdown master.
// Usage: node build_docx.js <input.md> <output.docx>
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, AlignmentType, HeadingLevel,
  BorderStyle, PageBreak, TabStopType,
} = require("docx");

const [, , inPath, outPath] = process.argv;
if (!inPath || !outPath) { console.error("usage: node build_docx.js in.md out.docx"); process.exit(1); }
const src = fs.readFileSync(inPath, "utf8").replace(/\r\n/g, "\n");

const FONT = "NanumGothic";
const BODY = 21; // 10.5pt in half-points

function runs(text, base = {}) {
  // inline **bold** parsing
  const out = [];
  const re = /\*\*(.+?)\*\*/g;
  let last = 0, m;
  while ((m = re.exec(text)) !== null) {
    if (m.index > last) out.push(new TextRun({ text: text.slice(last, m.index), ...base }));
    out.push(new TextRun({ text: m[1], bold: true, ...base }));
    last = m.index + m[0].length;
  }
  if (last < text.length) out.push(new TextRun({ text: text.slice(last), ...base }));
  return out;
}

const children = [];
const lines = src.split("\n");
let metaDone = false;
for (let i = 0; i < lines.length; i++) {
  const raw = lines[i];
  const line = raw.trim();
  if (!line) continue;
  if (line === "---") {
    children.push(new Paragraph({
      spacing: { before: 120, after: 240 },
      border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "999999", space: 1 } },
      children: [new TextRun({ text: "" })],
    }));
    continue;
  }
  if (line.startsWith("# ")) {
    children.push(new Paragraph({
      alignment: AlignmentType.LEFT,
      spacing: { before: 0, after: 120 },
      children: [new TextRun({ text: line.slice(2), bold: true, size: 44 })],
    }));
    continue;
  }
  if (line.startsWith("## ")) {
    children.push(new Paragraph({
      spacing: { before: 0, after: 120 },
      children: [new TextRun({ text: line.slice(3), bold: true, size: 28 })],
    }));
    continue;
  }
  if (line.startsWith("### ")) {
    children.push(new Paragraph({
      heading: HeadingLevel.HEADING_2,
      spacing: { before: 420, after: 160 },
      keepNext: true,
      children: [new TextRun({ text: line.slice(4), bold: true, size: 26, color: "000000" })],
    }));
    continue;
  }
  // note line: starts with ※ -> small grey
  if (line.startsWith("※")) {
    children.push(new Paragraph({
      spacing: { before: 0, after: 200 },
      children: [new TextRun({ text: line, size: 18, color: "555555" })],
    }));
    continue;
  }
  // dialogue line: raw line starts with full-width spaces (U+3000); "name<U+3000>text"
  if (raw.startsWith("\u3000")) {
    const body = raw.replace(/^\u3000+/, "");
    const idx = body.indexOf("\u3000");
    const name = idx >= 0 ? body.slice(0, idx) : body;
    const text = idx >= 0 ? body.slice(idx + 1).trim() : "";
    children.push(new Paragraph({
      spacing: { after: 160, line: 336 },
      indent: { left: 2700, hanging: 1500 },
      tabStops: [{ type: TabStopType.LEFT, position: 2700 }],
      children: [new TextRun({ text: name }), new TextRun({ text: "\t" }), ...runs(text)],
    }));
    continue;
  }
  // first plain line after the title block = meta line (smaller, grey)
  if (!metaDone) {
    metaDone = true;
    children.push(new Paragraph({
      spacing: { before: 0, after: 120 },
      children: [new TextRun({ text: line, size: 19, color: "555555" })],
    }));
    continue;
  }
  children.push(new Paragraph({
    spacing: { after: 160, line: 336 },
    alignment: AlignmentType.LEFT,
    children: runs(line),
  }));
}

const doc = new Document({
  creator: "IF Studio",
  title: "THE NEW MISSION",
  styles: {
    default: {
      document: { run: { font: { ascii: FONT, hAnsi: FONT, eastAsia: FONT, cs: FONT }, size: BODY } },
      heading2: { run: { font: { ascii: FONT, hAnsi: FONT, eastAsia: FONT, cs: FONT }, size: 26, bold: true, color: "000000" } },
    },
  },
  sections: [{
    properties: {
      page: {
        size: { width: 11906, height: 16838 }, // A4
        margin: { top: 1134, right: 1134, bottom: 1134, left: 1134 }, // 2.5cm
      },
    },
    children,
  }],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(outPath, buf);
  console.log("wrote", outPath, buf.length, "bytes,", children.length, "paragraphs");
});
