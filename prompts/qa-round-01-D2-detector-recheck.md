# Task D2: Detector recheck of the Fixer's candidate (sent by Boss, 2026-11-18)

Run via the Agent tool, `subagent_type: detector` (registered type), using the Skill `detector` in **recheck mode**. The task text is below the line.

---

Task D2 (2026-11-18): recheck the Fixer's candidate for QA round 1.

- Candidate PDF: `build/behind-the-playlist-candidate.pdf`; its log: `build/candidate/main.log` (and `.blg`)
- Inputs to compare: `docs/qa/round-01/detect/detector-report.md` (D1) and `docs/qa/round-01/fix/fixer-report.md` (F1)
- Approved PDF for comparison (do not modify): `submission/behind-the-playlist.pdf`
- Report directory: `docs/qa/round-01/recheck/`

Do:
1. Run qa-super with `--checks all` on the candidate and its log, writing to the report directory. That covers the 20-page count, the page-19 footer regression and the stricter bibliography check.
2. Verify each Fixer change:
   - **D1-02:** the new bibliography check genuinely detects the heading on p.19 and would fail without it. Read the code; do not trust the Fixer's claim.
   - **D1-03:** look at the rendered pp. 19–20 of the candidate. No URL may break inside "https://", and no new layout problem may appear.
3. Compare the candidate with the approved PDF. List which pages differ (extracted text per page) and confirm that only the expected pages changed.
4. Write `docs/qa/round-01/recheck/recheck-report.md`:
   - per finding: verified fixed / not fixed / still open (flagged for the users);
   - the page count;
   - the page-19 result;
   - a final verdict: **candidate acceptable** or **not acceptable**.

Write only inside the report directory. Never write student ID numbers.
