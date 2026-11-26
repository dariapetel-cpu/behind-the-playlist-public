# D5 Verifier: independent recheck of the Fixer's QA changes

You are an independent verification agent (Detector definition, recheck mode), separate from D4 and F2. Try to break the new harness; do not trust `fix/fixer-report.md` or its tests. Do not edit anything except `docs/qa/round-02/recheck/recheck-report.md`. No installs, downloads, TeX, commit or push; fake IDs only. Work on a copy of the working tree in scratch.

1. Run `tests/test_feedback_label.py` and `tests/test_qa_mutations.py` yourself, once each, output saved to scratch; quote the real totals.
2. Run the harness on the real `pdf/behind-the-playlist.pdf` with `--no-log`; record totals and exit code, and read the evidence of the passing checks.
3. Write your own mutations (not the tests' code) for H1, H2, H3, M3, M4, M5, L3 and at least N1, N2, N3, N6, N9, N10, N11, N12; use different positions, pages, colours and partial covers. For each: check that failed and exit code, or MISSED.
4. False alarms: render-neutral changes that must still pass (re-save with garbage=4, deflate; metadata title; hash-like or DOI numbers in text; a comment containing `\vspace`).
5. Test strength: in a copy, disable each of at least six fixes one at a time (e.g. skip the visibility check, return exit 0, accept an empty log) and report whether the test suite then fails. Run only the relevant test classes to save time.
6. Read the diff: any weakened expectation, broad allow-list, threshold tuned to hide a miss, or a Skill text that claims more than the code does?
7. Check `git diff --stat -- book pdf figures` is empty and the PDF SHA-256 starts 7ab8276a.

Report every item with observed results, then VERIFIED / NOT VERIFIED per D4 finding, new findings with severity, and a "not verified" list. Final reply: at most 12 lines.
