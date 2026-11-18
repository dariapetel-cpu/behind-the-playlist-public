> Author: Fixer agent · 2026-11-18 · input: docs/qa/round-01/detect/detector-report.md (+ findings.json)

# Fixer report, red-team QA round 1 (Task F1)

**Summary:** 2 fixed (D1-02 skill, D1-03 template), 2 flagged for the users (D1-01 packaging, D1-04 content figure), 55 automated passes needed no action.
**Candidate:** `build/behind-the-playlist-candidate.pdf` (SHA-256 34334e9d15ab…), 20 pages, class v1.1, built with `make candidate` into `build/candidate/`.
**Approved PDF untouched:** `submission/behind-the-playlist.pdf` and `build/behind-the-playlist-lualatex.pdf` still have SHA-256 43608a86aae3… (checked after both builds). I edited no file under `book/chapters/`, `book/main.tex`, `book/references.bib`, `submission/` or `backups/`.

## Decisions per finding

| ID | Kind | Decision | Files changed |
|---|---|---|---|
| D1-01 (qa-infra-56) | packaging | **Flagged for the users** | none |
| D1-02 | skill | **Fixed** | `tools/qa/qa_lib.py`, `.claude/skills/qa-typeset/SKILL.md` |
| D1-03 | template | **Fixed** | `book/behind-the-playlist.cls` (v1.0 → v1.1) |
| D1-04 | content (figure file) | **Flagged for the users** | none |
| all other 55 checks | none | No action needed (pass / honest n/a) | none |

### D1-01: stale source ZIP (major, packaging): flagged
`submission/project-source.zip` dates from 2026-11-14. It holds an older PDF (256,033 B, not the approved 267,398 B) and no `.cls`.
**Recommendation for the users:** rebuild the ZIP from the current tree so that it contains `submission/behind-the-playlist.pdf` (SHA 43608a86…) and `book/behind-the-playlist.cls`. Then rerun qa-infra. Decide first whether the ZIP should carry class v1.0 (matches the approved PDF) or v1.1 (only if you approve the candidate, see D1-03). The ZIP and the PDF in it must use the same class version. The Fixer must not write to `submission/`.

### D1-02: bibliography check reported the wrong page (minor, skill): fixed
- **Cause:** `check_bib` took the last page whose first 30 characters contained "מקורות". That is p.20's running header. It never compared the page with `chapter_starts`, so a missing or moved heading would still have passed.
- **Fix (`tools/qa/qa_lib.py`, `check_bib`):** the heading is now a line whose text is exactly "מקורות" and whose font size is at least 16 pt. That size excludes the 8.7 pt running header, the 10.5 pt TOC line and body text. The check passes only if that heading is found on exactly one page and that page equals `EXP["chapter_starts"]["מקורות"]` (19). The evidence and expected strings now state the page. The entry count and margin logic is unchanged. `expectations.json` is **unchanged**, so no expectation was weakened; the check is stricter.
- **Skill text:** in `.claude/skills/qa-typeset/SKILL.md`, the bibliography sentence now says the heading must be at heading size on the expected page (19), not just in the running header.
- **Verification:**
  - Approved PDF → pass, "heading 'מקורות' on p.19; 18 entries; min x0=70.9".
  - Negative test 1, approved PDF with p.19 deleted → **fail**.
  - Negative test 2, approved PDF with the p.19 heading redacted → **fail**. The old check would have passed this case because of the p.20 running header.

### D1-03: URL broke after `https:` (low, cosmetic, template): fixed in class v1.1
- **Root cause:** this differs from the Detector's guess. The `biburl{num,uc,lc}penalty = 0` counters only control breaks after digits and letters, and are 0 (inactive). The break came from biblatex's default `\UrlBigBreaks{\do\:\do\-}`, which allows a break after every `:` (penalty 100). LaTeX's default math code also makes `:` a relation, so simply removing it from `\UrlBigBreaks` did **not** help. My first attempt confirmed this: `https:` still ended the line.
- **Fix (`book/behind-the-playlist.cls`):** I appended code to `\biburlsetup`.
  - `\UrlBigBreaks` is now `{\do\-}`.
  - Two `\UrlSpecials` were added. `:` is set as an ordinary character and arms a counter. The next two `/` after a `:` are set as ordinary characters. Every other `/` keeps its normal break (bin, `biburlbreakpenalty` 200).
  - Result: no break point anywhere inside `scheme://`. Breaks at `.`, other `/`, `-` etc. are unchanged.
  - Documented side effect: after a `:` elsewhere in a URL, the next two `/` cannot break. None of the 18 sources has such a URL.
- **Version and changelog:** `\ProvidesClass` and `\bookclassversion` are now v1.1, with a CHANGELOG line "v1.1 2026-11-18 QA round 1 (Fixer, finding D1-03) …". qa-cls-version on the candidate: v1.1 / v1.1 / v1.1, pass.
- **Diff summary:** +3 CHANGELOG lines, 2 version strings, +13 lines after the `biburl*penalty` counters (5 of them comments).
- **Effect in the candidate:**
  - Entry [13] (p.20) now reads "… [Online]. Available:" / `https://developers.google.com/machine-` / `learning/recommendation/overview/types`. It is one line longer and stays inside the margins.
  - Entries [1]–[11] are still on p.19 and [12]–[18] on p.20.
  - Extracted text is byte-identical to the approved PDF on pp.1–19. Only p.20 differs.
  - The link targets (URIs) are unchanged.
- **Still not changed:** the `machine-` | `learning` break in [9] (p.19) and [13] (p.20) is a break after a hyphen in the URL. The Detector accepted it as fine.
- **For the users:** v1.1 changes only the candidate. Adopting it as the submission is your decision. If you do, it needs a new approval, the new SHA in the docs, and a rebuilt ZIP.

### D1-04: Fig. 6.1 label "לולאת משוב" almost touches the dashed loop (low, cosmetic, content): flagged
The label is placed in `book/figures/pipeline.tex` l.41. That is a figure source under `book/`, outside the Fixer's editable files, and the Detector classed it as content.
**Recommendation for the users (optional):** add a small offset to that label node, about 2–3 pt away from the dashed line (for example a slightly larger `xshift` or `inner sep`), then rerun qa-img and qa-bidi (phrase "לולאת משוב"). This does not block submission.

## Candidate QA (automated, my own pre-check, not a replacement for the Detector)
`.venv/bin/python tools/qa/qa_lib.py --pdf build/behind-the-playlist-candidate.pdf --log build/candidate/main.log --checks all --out <scratch>`:
- Result: **55 pass, 1 fail, 1 n/a**.
- The only fail is qa-infra-56 (ZIP). It is the same packaging finding as D1-01 and does not depend on the candidate.
- Build checks: 0 errors, 0 overfull, 20 pages, 10 chapter starts, bibliography heading on p.19 (new check), 18 entries, min x0 = 70.9, 0 biber warnings.
- Footer: p.19 regression pass, dot strictly right-to-left.

## Recheck request for the Detector
Run on `build/behind-the-playlist-candidate.pdf` with log `build/candidate/main.log`:
1. **qa-typeset** (full): especially the new heading-page evidence ("p.19"), and that the overfull and margin checks still give 0.
2. **qa-cls-version**: v1.1 in `\ProvidesClass`, CHANGELOG and log.
3. **qa-footer**: pp.19–20, including the p.19 regression.
4. **qa-bidi**: p.19–20 running header and citations, as a sanity check.
5. **Red team, pp.19–20:** view all URL line breaks in [1], [4], [6], [9], [11], [13]. Confirm no break inside `https://`, nothing in the margins, and [12]–[18] still on p.20 with the bottom of the page clear.
6. **qa-super** once in full, to confirm nothing else moved. Extracted text on pp.1–19 should be identical to the approved PDF.
7. Also review the stricter `check_bib` in `tools/qa/qa_lib.py` (red-team the skill fix itself).

D1-01 and D1-04 are left for the users. No recheck is possible until they act.
