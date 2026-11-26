"""Put the whole publishing kit into one Word file: channel set-up, every episode's posts, and all
rendered subtitles.

    python3 make_publish_kit.py && python3 kit_to_docx.py

Output: publishing-kit-complete.docx
"""
import glob, os, re
from docx import Document
from docx.enum.text import WD_BREAK
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor

HERE = os.path.dirname(os.path.abspath(__file__))
HINDI_FONT = "Nirmala UI"   # ships with Windows; phones and Macs substitute their own Devanagari font


def set_font(run, size=None, mono=False, bold=None):
    run.font.name = "Consolas" if mono else "Calibri"
    rpr = run._element.get_or_add_rPr()
    fonts = rpr.find(qn("w:rFonts"))
    if fonts is None:
        fonts = rpr.makeelement(qn("w:rFonts"), {}); rpr.append(fonts)
    fonts.set(qn("w:cs"), HINDI_FONT)
    if size:
        run.font.size = Pt(size)
        szcs = rpr.makeelement(qn("w:szCs"), {qn("w:val"): str(int(size * 2))}); rpr.append(szcs)
    if bold is not None: run.bold = bold


def inline(par, text, size=None):
    """Add text with **bold**, *italic* and `code` spans."""
    for tok in re.split(r"(\*\*[^*]+\*\*|`[^`]+`|\*[^*]+\*)", text):
        if not tok: continue
        if tok.startswith("**"):
            r = par.add_run(tok[2:-2]); set_font(r, size, bold=True)
        elif tok.startswith("`"):
            r = par.add_run(tok[1:-1]); set_font(r, size, mono=True)
        elif tok.startswith("*") and len(tok) > 2:
            r = par.add_run(tok[1:-1]); r.italic = True; set_font(r, size)
        else:
            r = par.add_run(tok); set_font(r, size)


def copy_box(doc, lines):
    """A shaded box the user can select and copy."""
    t = doc.add_table(rows=1, cols=1); t.style = "Table Grid"
    cell = t.rows[0].cells[0]
    shd = cell._element.get_or_add_tcPr().makeelement(qn("w:shd"), {qn("w:val"): "clear", qn("w:fill"): "F4EFE6"})
    cell._element.get_or_add_tcPr().append(shd)
    p = cell.paragraphs[0]
    for i, l in enumerate(lines):
        r = p.add_run(l); set_font(r, 10)
        if i < len(lines) - 1: r.add_break(WD_BREAK.LINE)
    doc.add_paragraph()


def table(doc, rows):
    cells = [[c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", r.strip().strip("|"))] for r in rows]
    cells = [c for c in cells if not all(re.fullmatch(r"-+", x) for x in c)]
    t = doc.add_table(rows=len(cells), cols=len(cells[0])); t.style = "Table Grid"
    for i, row in enumerate(cells):
        for j, val in enumerate(row[:len(cells[0])]):
            p = t.rows[i].cells[j].paragraphs[0]
            inline(p, f"**{val}**" if i == 0 else val, 10)
    doc.add_paragraph()


def md_to_doc(doc, md):
    lines = md.splitlines(); i = 0
    while i < len(lines):
        l = lines[i]
        if l.startswith("```"):
            j = i + 1
            while not lines[j].startswith("```"): j += 1
            copy_box(doc, lines[i + 1:j]); i = j + 1; continue
        if l.startswith("|"):
            j = i
            while j < len(lines) and lines[j].startswith("|"): j += 1
            table(doc, lines[i:j]); i = j; continue
        m = re.match(r"(#+) (.+)", l)
        if m:
            lvl = len(m.group(1))
            if lvl == 3 and m.group(2).startswith("E"):
                doc.add_page_break()
            h = doc.add_heading(level=lvl); inline(h, m.group(2))
        elif l.startswith("- "):
            inline(doc.add_paragraph(style="List Bullet"), l[2:])
        elif l.strip():
            inline(doc.add_paragraph(), l)
        i += 1


def main():
    doc = Document()
    st = doc.styles["Normal"]; st.font.name = "Calibri"; st.font.size = Pt(11)
    st.element.rPr.rFonts.set(qn("w:cs"), HINDI_FONT)
    for s in ("Heading 1", "Heading 2", "Heading 3"):
        doc.styles[s].element.get_or_add_rPr()
        doc.styles[s].font.color.rgb = RGBColor(0x8A, 0x2B, 0x0E)
    md = open(os.path.join(HERE, "publishing-kit.md"), encoding="utf-8").read()
    head, eps = md.split("## 6. Every episode", 1)
    md_to_doc(doc, head.replace("# YouTube upload kit: सूर्यवंश कथा",
                                "# सूर्यवंश कथा: YouTube publishing kit (episodes 1-20)", 1))
    doc.add_page_break()
    md_to_doc(doc, "## 6. Every episode" + eps)

    srts = sorted(glob.glob(os.path.join(HERE, "captions", "ep*.srt")))
    doc.add_page_break()
    doc.add_heading("7. Subtitles (Hindi, timed)", level=2)
    inline(doc.add_paragraph(),
           "Subtitles exist for episodes whose narration is already rendered "
           f"({', '.join('E' + os.path.basename(s)[2:4] for s in srts)}). To upload one: copy its box into a plain "
           "text file named `epNN.srt` (Notepad: Save as, encoding UTF-8), then YouTube Studio → Subtitles → "
           "Hindi → Upload file → With timing. The `.srt` files are also in the repository under `captions/`. "
           "The other episodes get theirs when their narration is made.")
    for s in srts:
        doc.add_page_break()
        doc.add_heading(f"E{os.path.basename(s)[2:4]} subtitles", level=3)
        copy_box(doc, open(s, encoding="utf-8").read().rstrip().splitlines())
    out = os.path.join(HERE, "publishing-kit-complete.docx")
    doc.save(out); print("wrote", out)


if __name__ == "__main__":
    main()
