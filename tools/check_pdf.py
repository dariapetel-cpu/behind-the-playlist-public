"""Automated PDF checks for the book (Boss tool; also feeds the Reviewer and qa_lib.py).

Usage: .venv/bin/python tools/check_pdf.py <pdf> <log> <pages_dir>
       .venv/bin/python tools/check_pdf.py <pdf> --no-log <pages_dir>
- LaTeX log: must be a completed LuaLaTeX log of this book's class whose page count equals the
  PDF's; errors (classic and file:line:), fatal errors, rerun requests, "Missing character",
  overfull/underfull boxes, undefined refs/citations. Lines wrapped at 79 columns are rejoined.
- PDF: page count, text outside the page, text too faint for its background
  (the [heb]+colour TikZ bug, PRD §6), fonts used
- Renders every page to <pages_dir>/page-NN.png (110 dpi) for visual review.
Exit codes: 0 = pass; 1 = a hard check failed; 2 = usage error.
With --no-log nothing is said about the build: log checks are reported as "log=n/a".
"""
import re, sys
from pathlib import Path
import pymupdf

CLASS = "behind-the-playlist"
MIN_LUM_DIFF = 40      # text vs. background luminance (0-255); near-white on white is < 5
SRC_EXT = r"(?:tex|cls|sty|bbl|bib|cfg|def|ltx|lua|aux|toc|clo|fd)"


def unwrap(text):
    """Rejoin log lines that TeX wrapped at max_print_line = 79 (characters, or bytes for Hebrew).
    The last piece of a wrapped line is shorter than 79, so joining stops there."""
    out, buf = [], ""
    for line in text.splitlines():
        buf += line
        if 79 in (len(line), len(line.encode("utf-8", "replace"))):
            continue
        out.append(buf); buf = ""
    if buf: out.append(buf)
    return "\n".join(out)


def parse_log(raw, pdf_pages):
    """Returns (stats, reasons). An empty reasons list means that the log is acceptable.
    Each pattern is counted on the raw and on the unwrapped text (the larger count), because a
    line of exactly 79 columns may be a complete line and must not swallow the next one."""
    joined = unwrap(raw)
    def count(rx): return max(len(re.findall(rx, t, re.M)) for t in (raw, joined))
    stats = {
        "errors": count(r"^! ") + count(r"^(?:[A-Za-z]:)?[^:\s][^:\n]*\." + SRC_EXT + r":\d+: ") +
                  count(r"^\[(?:\\directlua|string [^\]\n]*)\]:\d+: |^(?!! ).*LuaTeX error"),
        "fatal": count(r"Fatal error occurred|Emergency stop|no output PDF file produced|No pages of output"),
        "reruns": count(r"Rerun to get|Rerun LaTeX|Label\(s\) may have changed|Please \(?re-?\)?run|"
                        r"Package rerunfilecheck Warning"),
        "duplicate_labels": count(r"multiply[- ]defined"),
        "empty_bib": count(r"Empty bibliography"),
        "missing_chars": count(r"Missing character"),
        "overfull": count(r"^Overfull \\[hv]box"),
        "underfull": count(r"^Underfull \\hbox"),
        "undef_refs": count(r"Reference .* undefined|undefined references"),
        "undef_cites": count(r"Citation .* undefined|undefined citations"),
    }
    reasons = [f"{k}={stats[k]}" for k in ("errors", "fatal", "reruns", "duplicate_labels", "empty_bib", "missing_chars", "undef_refs", "undef_cites")
               if stats[k]]
    over = {m.group(1) for t in (raw, joined) for m in re.finditer(r"^(Overfull \\[hv]box \([\d.]+pt[^\n]{0,60})", t, re.M)}
    for m in sorted(over):
        if float(re.search(r"\(([\d.]+)pt", m).group(1)) > 2.0: reasons.append("overfull>2pt: " + m)
    if not re.search(r"^This is Lua\w*TeX", raw, re.M): reasons.append("log: not a LuaLaTeX log")
    if f"Document Class: {CLASS} " not in joined: reasons.append(f"log: class {CLASS} not loaded")
    if len(re.findall(r"^This is Lua\w*TeX", raw, re.M)) > len(re.findall(r"^Output written on ", joined, re.M)):
        reasons.append("log: a run started but did not finish ('This is Lua...' without 'Output written on')")
    pages = re.findall(r"Output written on .*?\((\d+) pages?", joined, re.S)
    if not pages: reasons.append("log: no 'Output written on' line (the build did not complete)")
    elif int(pages[-1]) != pdf_pages: reasons.append(f"log: {pages[-1]} pages written, but the PDF has {pdf_pages}")
    return stats, reasons


def lum(rgb): return 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]


def shown(txt):
    """Text quoted in a report; digits are hidden so that a report can never leak an ID or a date."""
    return re.sub(r"\d", "#", txt[:30])


def main(argv):
    for s in (sys.stdout, sys.stderr):
        if hasattr(s, "reconfigure"): s.reconfigure(encoding="utf-8", errors="replace")
    if len(argv) != 3:
        print("usage: check_pdf.py <pdf> <log>|--no-log <pages_dir>", file=sys.stderr); return 2
    pdf, log, outdir = Path(argv[0]), (None if argv[1] == "--no-log" else Path(argv[1])), Path(argv[2])
    if not pdf.is_file() or (log and not log.is_file()):
        print("usage error: PDF or log not found", file=sys.stderr); return 2
    doc = pymupdf.open(pdf)
    fail, stats = [], {}
    if log: stats, fail = parse_log(log.read_text(encoding="utf-8", errors="replace"), doc.page_count)
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
                        fail.append(f"p{i}: text outside page: {shown(txt)}")
                    # Faint text (PRD §6 [heb]+colour bug): the declared text colour against the
                    # median of the rendered surroundings (the ink itself covers less than half).
                    ink = lum((s["color"] >> 16 & 255, s["color"] >> 8 & 255, s["color"] & 255))
                    if ink < 160: continue
                    pix = page.get_pixmap(dpi=72, clip=pymupdf.Rect(x0 - 2, y0 - 2, x1 + 2, y1 + 2) & r)
                    if not pix.width or not pix.height: continue
                    ls = sorted(lum(pix.pixel(x, y)) for x in range(pix.width) for y in range(pix.height))
                    if abs(ls[len(ls) // 2] - ink) < MIN_LUM_DIFF:
                        fail.append(f"p{i}: WHITE text on light background (low contrast): {shown(txt)}")
    print(f"pages={doc.page_count}", " ".join(f"{k}={v}" for k, v in stats.items()) if log else "log=n/a (--no-log)")
    print("fonts:", ", ".join(sorted(fonts)))
    print(f"rendered -> {outdir}/page-NN.png")
    if fail:
        print("FAIL:")
        for f in fail: print("  -", f)
        return 1
    print("PASS (automated checks). Visual inspection still required.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
