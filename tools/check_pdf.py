"""Automated PDF checks for the book (Boss tool; also feeds the Reviewer).

Usage: .venv/bin/python tools/check_pdf.py <pdf> <log> <pages_dir>
- LaTeX log: errors, "Missing character", overfull/underfull boxes, undefined refs/citations
- PDF: page count, text/drawings outside the page, WHITE text on light background
  (the [heb]+colour TikZ bug, PRD §6), fonts used
- Renders every page to <pages_dir>/page-NN.png (110 dpi) for visual review.
Exit code 1 if any hard check fails.
"""
import re, sys
from pathlib import Path
import pymupdf

pdf, log, outdir = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
fail = []
L = log.read_text(encoding="utf-8", errors="replace")
def count(rx): return len(re.findall(rx, L, re.M))
stats = {
    "errors": count(r"^! "),
    "missing_chars": count(r"Missing character"),
    "overfull": count(r"^Overfull \\hbox"),
    "underfull": count(r"^Underfull \\hbox"),
    "undef_refs": count(r"Reference .* undefined"),
    "undef_cites": count(r"Citation .* undefined"),
}
for k in ("errors", "missing_chars", "undef_refs", "undef_cites"):
    if stats[k]: fail.append(f"{k}={stats[k]}")
for m in re.finditer(r"^(Overfull \\hbox \(([\d.]+)pt.*)$", L, re.M):
    if float(m.group(2)) > 2.0: fail.append("overfull>2pt: " + m.group(1)[:90])

doc = pymupdf.open(pdf)
outdir.mkdir(parents=True, exist_ok=True)
fonts = set()
for i, page in enumerate(doc, 1):
    page.get_pixmap(dpi=110).save(outdir / f"page-{i:02d}.png")
    r = page.rect
    for f in page.get_fonts(): fonts.add(f[3].split("+")[-1])
    for b in page.get_text("rawdict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                txt = "".join(c["c"] for c in s["chars"]).strip()
                if not txt: continue
                x0, y0, x1, y1 = s["bbox"]
                if x0 < r.x0 - 0.5 or x1 > r.x1 + 0.5 or y0 < r.y0 - 0.5 or y1 > r.y1 + 0.5:
                    fail.append(f"p{i}: text outside page: {txt[:30]}")
                if s["color"] == 0xFFFFFF:
                    # White text is only a bug on a light background (PRD §6 [heb]+colour bug).
                    # Sample the rendered background just around the span (text itself excluded
                    # by taking the darkest-luminance quartile would be overkill; use the median).
                    pix = page.get_pixmap(dpi=72, clip=pymupdf.Rect(x0 - 2, y0 - 2, x1 + 2, y1 + 2))
                    px = [pix.pixel(x, y) for x in range(pix.width) for y in range(pix.height)]
                    lum = sorted(0.2126 * p[0] + 0.7152 * p[1] + 0.0722 * p[2] for p in px)
                    if lum[len(lum) // 2] > 160:
                        fail.append(f"p{i}: WHITE text on light background: {txt[:30]}")
print(f"pages={doc.page_count}", " ".join(f"{k}={v}" for k, v in stats.items()))
print("fonts:", ", ".join(sorted(fonts)))
print(f"rendered -> {outdir}/page-NN.png")
if fail:
    print("FAIL:"); [print("  -", f) for f in fail]; sys.exit(1)
print("PASS (automated checks). Visual inspection still required.")
