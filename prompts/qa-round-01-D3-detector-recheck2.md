# Task D3: Detector recheck after the users' figure decision (sent by Boss, 2026-11-18)

Run via the Agent tool, `subagent_type: detector`, using the Skill `detector` in recheck mode. The task text is below the line.

---

Task D3 (2026-11-18): recheck the candidate after the users' decision on finding D1-04.

**Change being checked.** The users asked for „לולאת משוב" to move right to leave about 2 mm to the dashed loop line (Prompt 24). The coordinator changed `book/figures/pipeline.tex` (label position + a phantom copy that keeps the picture's bounding box). The class and the chapters are unchanged.

- Candidate PDF: `build/behind-the-playlist-candidate.pdf`; log: `build/candidate/main.log`
- Approved PDF for comparison (do not modify): `submission/behind-the-playlist.pdf`
- Report directory: `docs/qa/round-01/recheck-2/`

Verify:
1. Run qa-super `--checks all` on the candidate (20 pages, p.19 footer, bibliography, bidi incl. „לולאת משוב").
2. **Label readable.** Open a high-resolution render of p.14 around the label. It must be fully legible, not clipped or overlapping, and correct Hebrew.
3. **Gap.** Measure the gap from glyph positions and the dashed line's drawing: about 2 mm expected.
4. **All eight blocks in place.** Compare the 8 block rectangles and the dashed line on p.14 with the approved PDF: identical coordinates expected.
5. **Margin.** Report exactly how far the label extends past the text block's right edge (x = 524.4 pt), even if the margin check passes.
6. **Differences.** Pages whose extracted text differs from the approved PDF (only p.20 is expected, from class v1.1).

Write `docs/qa/round-01/recheck-2/recheck-report.md` with a verdict: **candidate acceptable** or **not acceptable**. Write only inside the report directory.
