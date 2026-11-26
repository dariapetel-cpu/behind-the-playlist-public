# QA round 2: the QA harness itself (2026-11-25, branch `roni-qa-improvements`)

**Target:** `tools/qa/qa_lib.py`, `tools/check_pdf.py` and the qa-* Skills. The book, its sources and `pdf/behind-the-playlist.pdf` (SHA-256 `7ab8276a…`) were not changed. Requested by Roni Sagi; prompts: `prompts/qa-round-02-*.md`. Nothing was committed while this was written.

| Step | Who | Result |
|---|---|---|
| Audit | main Claude Code session | reported the first failures |
| D4 | `detector` agent | [report](detect/detector-report.md): H1-H3, M2-M5 reproduced, L3 partly; 18 new findings |
| F2 | `fixer` agent | [report](fix/fixer-report.md): 25 of 26 rows reported fixed, N7 partly |
| D5 | `detector` agent as verifier | **stopped by the coordinator on the user's instruction; it wrote no report.** Its raw output is kept in [recheck/raw](recheck/raw/) (local paths shortened) |
| Targeted fixes | **coordinator, not a Fixer agent** | D5 gaps 1, 2, 3 and 7; verified by the coordinator only, with no independent agent |

## Results that were actually run

| Run | Result |
|---|---|
| F2, full suite at that time | 116 tests, OK (588 s) |
| F2, same tests on commit 12efa82 | 147 failures, 3 errors (sub-tests counted); by F2's count 106 of 114 mutation tests. Partly because the old findings have no check names: not a bug count |
| D5, same suite, independently | 114 + 2 tests, OK (1676 s, parallel load) |
| D5, own PDF mutations, first batch | 47 of 60 reported. Two more (a removed word, half of a line) were caught when D5 repeated them with corrected mutations |
| D5, harmless PDF changes | 4 of 4 pass |
| D5, one fix disabled at a time | 15 of 20 noticed by the tests |
| Coordinator, focused pass (before the last README edit) | 53 + 35 = 88 tests, OK; `test_feedback_label.py` 2, OK |
| Coordinator, full suite (pre-commit review, 2026-11-25) | 141 tests: 132 pass, 9 fail, 0 skipped. All 9 were caused by the test copy omitting `docs/qa/`, which the README had just started linking to; fixed in `setUpModule` |
| Coordinator, full suite after that fix (2026-11-26) | **incomplete**: Claude Code stopped it for low system memory. **69 pass, 0 fail, 0 skipped, 72 not run** (`Privacy`, `Recheck*`, `Skills`, `Sources`, `ValidInput` and the rest of `H3Logs`) |
| Coordinator, the 5 fixes D5 found unprotected, disabled again | 5 of 5 noticed |
| Coordinator, the 25 new tests on the F2 code | 17 fail. 16 are the gaps; `test_ordinary_numbers_pass` most likely failed only because that trimmed copy lacked files the README links to (not investigated). The other 8 cover rules that already worked |
| Real project, `--no-log` | 107 pass, 0 fail, 5 n/a, exit 0 |

The focused pass ran the test classes touched by the change (`Recheck*`, `Privacy`, `Cli`, `ValidInput`, `H2NoSilentSkips`, `H3Logs`, `Skills`). **The final code has no complete test run.** Of the full run after the copy fix, the 69 finished tests (`test_feedback_label`, `Cli`, `Figures`, `H1Visual`, `H2NoSilentSkips`, 14 of `H3Logs`) passed; the 72 others were not run. Six of the nine earlier failures are among them, so their fix is not verified. `test_ordinary_numbers_pass` was among the nine; its earlier failure on the F2 code is still not explained.

Two D5 observations were not usable. Its first iron-law batch and several false-alarm rows were contaminated by a leftover file of the experiment. Its "STALE" for `--edition submission` came from its own test for the word "old": a new test shows that a seeded result is replaced.

## What the targeted fixes changed
1. **Privacy:** IDs with dots, slashes, commas, underscores, `&nbsp;`, several spaces, a line break, next to other numbers or glued to letters; PDF info keys and attachment content; new check `infra.pdf-hidden-content` (attachments, layers, JavaScript, launch actions).
2. **Logs:** Windows paths, Lua errors, unfinished second run, multiply-defined labels, empty bibliography, unfinished or fatal biber.
3. **Stale result:** removed before anything can crash; encrypted PDFs and abbreviated `--out` are usage errors.
4. **Tests (issue 7):** class rule, XMP, bookmarks, annotations, form fields, two footer-dot rules.

## Known limitations
- **No real LaTeX or biber log was ever checked**; all log tests use synthetic fixtures. No TeX build was run. A real log might trigger a false alarm.
- Submission edition (except one footer run on the public PDF), Linux and macOS: not run.
- Loose ID forms need a valid check digit or an ID word. Not found: an ID after a decimal point, in a longer digit run, glued to letters that all look hexadecimal, or inside images, archives or small vector drawings.
- **False alarms (issue 6, not fixed):** any plain nine-digit number (e.g. a DOI part or a file size) fails; about one in ten loosely grouped numbers could too.
- **Issue 4, not fixed:** very small covers pass (D5: a 1.5 pt strip, half the height of a few words).
- **Issue 5, not fixed:** iron-law and code lists are incomplete (e.g. `\needspace`, `\vtop`, `tcblisting`).
- A log of another 20-page build of the same class is accepted (N7).
- The visual fingerprint needs PyMuPDF 1.28.2 and a newly approved baseline after any intended layout change.
- No full transcripts were archived for D4, F2 and D5.
- The new privacy scan skips images, fonts and archives (the old one searched their raw bytes for the declared IDs); PDFs are now scanned as text.

## Waiting for the users
Approval of `tools/qa/expectations.json` and `tools/qa/visual_baseline.json`; the two layout exceptions in chapter 2.
