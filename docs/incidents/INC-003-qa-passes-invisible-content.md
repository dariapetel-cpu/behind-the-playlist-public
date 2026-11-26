# INC-003 — The QA harness passed a book whose content could not be seen

| Field | Value |
|---|---|
| Status | **Fixed for the reproduced cases; residual limits below.** Awaiting the users' review (2026-11-25) |
| Found by | The independent audit requested by Roni Sagi (Claude Code session); reproduced by the **Detector** agent (D4) |
| Introduced by | The harness of QA round 1 (Prompt 22) |
| Fixed by | The **Fixer** agent (F2); four remaining groups by the coordinator after D5 |
| Verified by | F2's tests, an unfinished independent recheck (D5), one focused coordinator pass and an incomplete full run (69 pass, 0 fail, 72 not run) |
| Affected | `tools/qa/qa_lib.py`, `tools/check_pdf.py`, eight qa-* Skills. **No defect was found in the book itself** (D4, contact sheets at 75 dpi) |
| Sources | [round-02 README](../qa/round-02/README.md), [D4](../qa/round-02/detect/detector-report.md), [F2](../qa/round-02/fix/fixer-report.md), [raw D5 output](../qa/round-02/recheck/raw/) |

## Symptom
On copies of the approved PDF, the old harness (D4, stub log) reported 55 pass, 0 fail, exit 0 with:
- the cover, Fig. 2.1, Table 4.1, the formulas or Fig. 6.1 covered by an opaque rectangle, and even with **every page white**;
- most of the text of p. 12 deleted.

Deleting the p. 9 table made its check disappear (54 pass, 0 fail). Runs with real fails still exited 0. An empty log passed `check_pdf.py`. A fake ID in a file of the public edition was not found.

## How it was found
The audit damaged copies of the PDF instead of only running the checks on the good one. D4 repeated each claim and found 18 further cases.

## Root cause
1. **Wrong object measured.** Checks read mostly the PDF text layer and drawing list, which an overlay does not change. Little besides the side margins was rendered.
2. **Absence treated as success.** `if target:` without `else` skipped a missing table, figure or `.blg`.
3. **No contract.** No exit code, no expected number of checks, no proof that the log was complete.
4. **Self-referential privacy scan.** It searched for the IDs declared in `main.tex`; the public edition removed them, so it searched for nothing.
5. **Checks were proven mainly on the valid book.** Apart from the D3-01 test, the repository held no negative test.

## Why the existing Detector missed it
- It ran the checks on a **correct** PDF, where a blind check and a working one both say PASS. Its visual review of that PDF found nothing hidden, because nothing was.
- Its Skill asked for defects in the book; nothing told it to attack the harness systematically.
- INC-002 had already concluded that every new check needs a negative test. That lesson stayed in a report: no Skill and no test enforced it.
- Totals looked stable; nothing asserted that a check had not vanished.
- Eight Skills had invalid YAML and were listed without descriptions in the audit session. This is a separate defect found on the way, not shown to be a cause.

## Corrective action (through Skills and tools; no chapter or class edits)
- New family and Skill `qa-visual`: each character must be visible in the render; figure and table regions; approved fingerprint.
- Chapter text compared with the PDF; missing targets fail; a minimum count per family; a crash is a fail.
- Exit codes 0/1/2; a completed log, or an explicit `--no-log` that gives n/a.
- ID scan by pattern; hidden PDF content; stale results removed first.
- Detector Skill: read the evidence of passes, each check needs a negative test. Fixer Skill: a mutation test per harness fix.
- `tests/test_qa_mutations.py`: 139 tests.

**First attempt was incomplete.** F2 reported 25 of 26 rows fixed and its 116 tests passed. D5's own mutations still got through in privacy, logs and stale results, and five fixes could be disabled unnoticed. The coordinator then fixed these. The first version of the new privacy rule raised a false alarm on image data in a transcript and was corrected before the focused pass.

## Verification
All figures are in the [round-02 README](../qa/round-02/README.md). In short: focused pass 88 tests OK; 5 of 5 disabled fixes noticed; real project 107 pass, 0 fail, 5 n/a; PDF hash unchanged. The final full run was stopped for low memory after 69 passing tests, with 72 not run; there is no complete run of the final code, and the coordinator's fixes had no independent verifier.

## Residual limits and prevention
Very small covers, incomplete command lists, false alarms on nine-digit numbers, no real build log: see the README above. Rule for every future check: show that it **fails** on a damaged copy, and treat "nothing found to check" as a fail.
