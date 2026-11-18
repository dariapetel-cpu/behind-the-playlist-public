# INC-002 — The QA bibliography check could pass without the bibliography heading

| Field | Value |
|---|---|
| Status | **Closed** (fixed and verified 2026-11-18) |
| Found by | The **Detector** agent in QA round 1 (finding D1-02), while reading the evidence of a check that *passed* |
| Introduced by | The coordinator (Boss), who wrote `tools/qa/qa_lib.py` earlier the same day (Prompt 22) |
| Fixed by | The **Fixer** agent (F1), in `tools/qa/qa_lib.py` and `.claude/skills/qa-typeset/SKILL.md` |
| Verified by | The **Detector** recheck (D2): it read the code and ran negative tests on modified copies |
| Sources | `docs/qa/round-01/detect/detector-report.md` (D1-02); `fix/fixer-report.md`; `recheck/recheck-report.md` |

**Symptom.** The check reported the heading „מקורות" on p.20, but the heading is on p.19.

**Root cause.** The check looked for "מקורות" anywhere in the first characters of a page. It therefore matched the **running header** of p.20 and never compared the page number with the expected one. Had the real heading gone missing, the check would still have passed.

**Why it was missed.** The coordinator's dry runs looked only at failures. A *passing* check with wrong evidence ("p.20") went unnoticed until the Detector read the evidence.

**Fix.** The check now requires a line reading exactly "מקורות" at heading size (≥ 16 pt) on the expected page (p.19), and nowhere else.

**Verification (D2).** Code review plus negative tests on copies: p.19 deleted → fail; heading blanked → fail; heading moved to p.18 → fail. The old check would have passed the last two.

**Prevention.** Read the evidence of passing checks, not only the failures. Every new check should get at least one negative test.
