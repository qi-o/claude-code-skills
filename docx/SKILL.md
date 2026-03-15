---
name: docx
description: "Use this skill whenever the user wants to create, read, edit, or manipulate Word documents (.docx files). Triggers include: any mention of 'Word doc', 'word document', '.docx', or requests to produce professional documents with formatting like tables of contents, headings, page numbers, or letterheads. Also use when extracting or reorganizing content from .docx files, inserting or replacing images in documents, performing find-and-replace in Word files, working with tracked changes or comments, or converting content into a polished Word document. If the user asks for a 'report', 'memo', 'letter', 'template', or similar deliverable as a Word or .docx file, use this skill. Do NOT use for PDFs, spreadsheets, Google Docs, or general coding tasks unrelated to document generation. 触发词：创建Word文档、编辑docx、Word文件、生成Word、修改Word。Do NOT use for PDF files (use pdf skill instead) or spreadsheets (use xlsx instead)."
license: Proprietary. LICENSE.txt has complete terms
github_url: https://github.com/anthropics/skills
github_hash: b0cbd3df1533b396d281a6886d5132f623393a9c
version: 0.1.0
---

# DOCX creation, editing, and analysis

## Overview

A .docx file is a ZIP archive containing XML files.

## Quick Reference

| Task | Approach |
|------|----------|
| Read/analyze content | `pandoc` or unpack for raw XML |
| Create new document | Use `docx-js` — see `references/docx_reference.md` |
| Edit existing document | Unpack → edit XML → repack — see `references/docx_reference.md` |

### Converting .doc to .docx

Legacy `.doc` files must be converted before editing:

```bash
python scripts/office/soffice.py --headless --convert-to docx document.doc
```

### Reading Content

```bash
# Text extraction with tracked changes
pandoc --track-changes=all document.docx -o output.md

# Raw XML access
python scripts/office/unpack.py document.docx unpacked/
```

### Converting to Images

```bash
python scripts/office/soffice.py --headless --convert-to pdf document.docx
pdftoppm -jpeg -r 150 document.pdf page
```

### Accepting Tracked Changes

```bash
python scripts/accept_changes.py input.docx output.docx
```

### Validation

After creating a file, always validate:
```bash
python scripts/office/validate.py doc.docx
```

---

## Creating New Documents

Generate .docx files with JavaScript. Install: `npm install -g docx`

Key patterns:
- **Page size**: Always set explicitly — docx-js defaults to A4, not US Letter (12240×15840 DXA)
- **Lists**: Never use unicode bullets — use `LevelFormat.BULLET` with numbering config
- **Tables**: Need dual widths — `columnWidths` on table AND `width` on each cell; always use `WidthType.DXA`
- **Images**: `type` parameter is required on `ImageRun`
- **Page breaks**: Must be inside a `Paragraph`
- **Shading**: Use `ShadingType.CLEAR`, never `SOLID`
- **TOC**: Headings must use `HeadingLevel` only — no custom styles
- **Styles**: Override built-in styles using exact IDs: "Heading1", "Heading2", etc. Include `outlineLevel` for TOC

For complete code examples (page size, styles, lists, tables, images, hyperlinks, footnotes, tab stops, multi-column, TOC, headers/footers) → `references/docx_reference.md`

---

## Editing Existing Documents

**Follow all 3 steps in order.**

### Step 1: Unpack
```bash
python scripts/office/unpack.py document.docx unpacked/
```

### Step 2: Edit XML

Edit files in `unpacked/word/`. Use the Edit tool directly — do not write Python scripts.

Use **"Claude"** as the author for tracked changes and comments (unless user requests otherwise).

Use XML entities for smart quotes: `&#x2019;` (apostrophe), `&#x201C;` `&#x201D;` (double quotes).

For comments, use `comment.py` to handle boilerplate, then add markers to document.xml.

Key pitfalls:
- Replace entire `<w:r>` elements when adding tracked changes
- Preserve `<w:rPr>` formatting in tracked change runs
- `<w:commentRangeStart/End>` are siblings of `<w:r>`, never inside it
- When deleting entire paragraphs, also add `<w:del/>` inside `<w:pPr><w:rPr>`

### Step 3: Pack
```bash
python scripts/office/pack.py unpacked/ output.docx --original document.docx
```

For complete XML reference (tracked changes, comments, images, schema compliance) → `references/docx_reference.md`

---

## Dependencies

- **pandoc**: Text extraction
- **docx**: `npm install -g docx` (new documents)
- **LibreOffice**: PDF conversion (auto-configured via `scripts/office/soffice.py`)
- **Poppler**: `pdftoppm` for images
