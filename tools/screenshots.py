"""Screenshots and page map from the final PDF (Boss tool).

Usage:
  .venv/bin/python tools/screenshots.py <pdf> mask-cover <out.png>
  .venv/bin/python tools/screenshots.py <pdf> readme <out_dir> <pagemap.json>

Privacy: every 9-digit number on the cover (student IDs) is covered with a solid
box labelled in the image. IDs are detected by pattern, so they are never written in this
file, the README or any log. Elements are found by searching the PDF text, so page numbers
in the README come from the actual PDF, not from the plan.
"""
import json, re, sys
from pathlib import Path
import pymupdf

PDF = Path(sys.argv[1]); MODE = sys.argv[2]
# --expect-ids N: number of 9-digit student IDs expected on the cover (2 = submission edition, 0 = public edition)
EXPECT_IDS = int(sys.argv[sys.argv.index("--expect-ids") + 1]) if "--expect-ids" in sys.argv else 2
if "--expect-ids" in sys.argv:
    i = sys.argv.index("--expect-ids"); del sys.argv[i:i + 2]
doc = pymupdf.open(PDF)

def id_rects(page):
    """Bounding boxes of 9-digit runs, built from glyph positions (works for RTL lines)."""
    rects = []
    for b in page.get_text("rawdict")["blocks"]:
        for l in b.get("lines", []):
            cs = sorted([c for s in l["spans"] for c in s["chars"]], key=lambda c: c["origin"][0])
            txt = "".join(c["c"] for c in cs)
            for m in re.finditer(r"\d{9}", txt):
                r = pymupdf.Rect(cs[m.start()]["bbox"])
                for c in cs[m.start():m.end()]: r |= pymupdf.Rect(c["bbox"])
                rects.append(r + (-1, -2, 1, 2))  # tight horizontally so ת״ז stays visible
    return rects

def render(page, clip=None, dpi=150, mask=False, out=None):
    if mask:
        # Draw the masks on a temporary copy, never on the source PDF.
        tmp = pymupdf.open(); tmp.insert_pdf(doc, from_page=page.number, to_page=page.number)
        p = tmp[0]
        rects = id_rects(p)
        for r in rects:
            p.draw_rect(r, color=(0.42, 0.45, 0.5), fill=(0.42, 0.45, 0.5))
            p.insert_textbox(r, "ID hidden", fontsize=6.5, color=(1, 1, 1), align=1)
        pix = p.get_pixmap(dpi=dpi, clip=clip)
        n = len(rects)
    else:
        pix = page.get_pixmap(dpi=dpi, clip=clip); n = 0
    pix.save(out)
    return n

def find_page(*needles):
    """First page whose text contains all needles (logical order, as PyMuPDF returns it)."""
    for p in doc:
        t = p.get_text()
        if all(n in t for n in needles): return p
    raise SystemExit(f"not found: {needles}")

def block_bbox(page, pred):
    r = None
    for b in page.get_text("blocks"):
        if pred(b[4]):
            r = pymupdf.Rect(b[:4]) if r is None else r | pymupdf.Rect(b[:4])
    return r

if MODE == "mask-cover":
    n = render(doc[0], mask=True, dpi=110, out=sys.argv[3])
    print(f"cover rendered with {n} ID(s) masked -> {sys.argv[3]}")
    if n != EXPECT_IDS: raise SystemExit(f"expected exactly {EXPECT_IDS} student IDs on the cover, found {n}")

elif MODE == "readme":
    out = Path(sys.argv[3]); out.mkdir(parents=True, exist_ok=True)
    pm = {}
    # 1 cover (masked)
    n = render(doc[0], mask=True, dpi=90, out=out / "cover.png"); pm["cover"] = 1
    assert n == EXPECT_IDS, f"expected exactly {EXPECT_IDS} student IDs on the cover, found {n}"
    # 2 graph: page with the figure caption of fig 2.1; crop drawing area + caption
    p = find_page("נתונים בדיוניים", "שעה ביום")
    cap = block_bbox(p, lambda t: "השבוע של נועה" in t)  # caption wording, not body references
    g = None
    for d in p.get_drawings():           # the embedded matplotlib figure lies above its caption
        r = d["rect"]
        if r.y1 <= cap.y0 + 1 and r.y0 > 60:
            g = r if g is None else g | r
    clip = (g | cap) + (-8, -8, 8, 22)    # +22pt below keeps the "נתונים בדיוניים" tag of the caption
    render(p, clip=clip, out=out / "graph.png"); pm["graph"] = p.number + 1
    # 3 formula: the lab box (title "מעבדה: דמיון קוסינוס") across its pages
    p = find_page("מעבדה", "דמיון קוסינוס")
    top = block_bbox(p, lambda t: "מעבדה" in t)
    clip = pymupdf.Rect(p.rect.x0 + 60, top.y0 - 10, p.rect.x1 - 60, p.rect.y1 - 70)
    render(p, clip=clip, out=out / "formula-1.png"); pm["formula"] = p.number + 1
    p2 = doc[p.number + 1]
    concl = block_bbox(p2, lambda t: "המסקנה" in t)
    # end just above the next section heading, which follows the lab box
    nxt = block_bbox(p2, lambda t: "משכנים לגורמים נסתרים" in t)
    bottom = (nxt.y0 - 6) if nxt else ((concl.y1 + 26) if concl else 520)
    clip2 = pymupdf.Rect(p2.rect.x0 + 60, 70, p2.rect.x1 - 60, bottom)
    render(p2, clip=clip2, out=out / "formula-2.png"); pm["formula_example"] = p2.number + 1
    # 4 comparison table
    p = find_page("טבלה", "שילוב גישות")
    cap = block_bbox(p, lambda t: "שלוש גישות להמלצה במבט אחד" in t)
    rules = [d["rect"] for d in p.get_drawings()
             if d["rect"].width > 400 and d["rect"].height < 3 and d["rect"].y0 > cap.y0]  # booktabs rules only
    rules = [r for r in rules if r.y0 < cap.y1 + 260]
    bottom = max(r.y1 for r in rules)
    clip = pymupdf.Rect(p.rect.x0 + 60, cap.y0 - 7, p.rect.x1 - 60, bottom + 8)
    render(p, clip=clip, out=out / "table.png"); pm["table"] = p.number + 1
    # 5 eight-block diagram + caption
    p = find_page("לולאת משוב", "ולמידה", "איור")
    cap = block_bbox(p, lambda t: "תהליך ההמלצה בשמונה תחנות" in t)
    boxes = [d["rect"] for d in p.get_drawings()
             if d["rect"].y1 <= cap.y0 + 1 and d["rect"].y0 >= cap.y0 - 300]   # diagram only
    top = min(r.y0 for r in boxes)
    clip = pymupdf.Rect(p.rect.x0 + 60, top - 10, p.rect.x1 - 60, cap.y1 + 18)
    render(p, clip=clip, out=out / "diagram.png"); pm["diagram"] = p.number + 1
    # page map for README checklist
    def pg(*n): return find_page(*n).number + 1
    pm.update({"abstract": pg("תקציר", "מה קורה בשנייה"), "toc": pg("תוכן העניינים"),
               "bibliography_start": pg("מקורות", "[1]"), "pages": doc.page_count,
               "chapters": {}})
    toc = doc.get_toc()
    for lvl, title, page in toc:
        pm["chapters"][title] = page
    Path(sys.argv[4]).write_text(json.dumps(pm, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(pm, ensure_ascii=False, indent=1))
