# D4 Detector: reproduce the QA-harness failures (before any fix)

You are the Detector in QA round 2, in the repository root. Follow `.claude/skills/detector/SKILL.md`; the target this time is the QA harness itself (`tools/qa/qa_lib.py`, `tools/check_pdf.py`). An audit claims the failures below. Do not trust it: reproduce or refute each one by execution.

Claims:
- H1 visual blindness: opaque rectangles over the cover, Fig. 2.1 (p.7), p.9 formulas, Table 4.1 (p.11), p.12 prose, Fig. 6.1 (p.14) give 0 failures; deleting p.12 prose from the text layer too.
- H2 silent skips: deleting the p.9 data table text removes a check instead of failing it; a missing `.blg` does the same; the same for Fig. 6.1 in `check_img`.
- H3 exit codes and logs: `qa_lib.py` exits 0 with failures; `check_pdf.py` passes an empty log, does not count `file:line: error` lines, and passes `Overfull \vbox` of 50pt.
- M3 the ID scan has no IDs to search for in the public edition, and its `/.git` exclusion uses POSIX separators.
- M4 iron law: `\vspace`, `\resizebox`, `\newpage`, `wrapfigure` in a chapter pass.
- M5 `qa-code` returns n/a even when a chapter contains a code environment.
- L3 a PDF outside the project makes `qa_lib.py` crash.
- M2 eight qa-* Skills have YAML frontmatter that does not parse.

How: work on a copy under your scratch directory (`git clone` of this repo), never mutate tracked files here. Interpreter: the PYTHON path given in the launch message. Set PYTHONUTF8=1 and PYTHONDONTWRITEBYTECODE=1. No build log exists in the repo and no TeX build is allowed, so use a stub log and say so. Never install anything. Use only fake IDs.

Look for further harness weaknesses of the same classes (silent skip, vacuous pass, wrong evidence); report only what you executed.

Write only `docs/qa/round-02/detect/detector-report.md` (real repo): per claim, the exact mutation, the observed totals and exit code, and the verdict REPRODUCED / NOT REPRODUCED / PARTLY; plus new findings and a "not verified" list. Do not propose code and do not fix anything. Final reply: at most 12 lines.
