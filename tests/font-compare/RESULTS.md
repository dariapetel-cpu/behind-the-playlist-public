# Font pairing comparison: results, 2026-11-18 (Prompt 17)

**PDF:** `tests/font-compare/comparison.pdf`, one A4-landscape page.
- The two columns are the real builds `pairA.pdf` and `pairB.pdf`, placed at **100% scale**, so the size is the actual reading size.
- Body text is 11 pt, with the Hebrew scaled to the book's current letter height (New Peninim × 1.12): Frank Ruhl Libre 0.96, Noto Serif Hebrew 0.87, Heebo 0.97, Noto Sans Hebrew 0.94. Latin is matched to the current Times x-height (Libertinus 1.03, Noto Serif/Sans 0.84).
- Line spacing is 1.22, as in the book.

**Engine:** LuaLaTeX + Biber + biblatex-ieee. Babel options: `bidi=basic`, `layout=graphics.lists`, `onchar=ids fonts`.
**Content:** the opening of Chapter 2, verbatim (macros simplified), plus the numbers sentence and two IEEE references (Hu et al. 2008; Schwartz 2004, which has an italic book title). The page includes a bold Hebrew heading, mixed Hebrew–English text, parentheses, numbers, two TikZ labels and the approved palette.

**Fonts:** sources, licences and checksums are in `fonts/SOURCES.md` and `fonts/SHA256SUMS`.

| | Pairing A | Pairing B |
|---|---|---|
| Hebrew body (serif) | Frank Ruhl Libre | Noto Serif Hebrew |
| Hebrew headings (sans) | Heebo Bold | Noto Sans Hebrew Bold |
| Latin, italic, digits | Libertinus Serif (true italic) | Noto Serif / Noto Sans (true italic) |
| Digits and punctuation inside Hebrew | from the fonts themselves | **fallback font required** (the Hebrew Noto fonts contain none) |

## Checks

| Check | A | B | Method |
|---|---|---|---|
| Build | ✅ 0 errors, 0 missing chars, 0 overfull | ✅ same | log |
| Bold Hebrew heading „כל דילוג נספר" | ✅ Heebo-Bold | ✅ NotoSansHebrew-Bold | glyph reading order + fonts used |
| Mixed Hebrew/English: „(explicit feedback)", „(implicit feedback)" | ✅ | ✅ | glyph reading order, mirrored brackets |
| Numbers 02, 30, 344, 245, 99, 28.8% | ✅ (Libertinus digits) | ✅ (Noto Serif digits via fallback) | glyphs + render |
| Parentheses „(הגדרה בדיונית)" (wraps across lines) | ✅ visually | ✅ visually | render (my line reader can't follow line breaks) |
| TikZ labels | ✅ „איסוף אותות", „דירוג מועמדים", each fully inside its box | ✅ same | glyphs inside box rectangles |
| Citations [1], [2] ↔ entries | ✅ | ✅ | glyphs + render |
| IEEE italic English title | ✅ LibertinusSerif-Italic | ✅ NotoSerif-Italic | fonts used |
| Missing characters | 0 | 0 (only with the fallback; without it, 1,375 missing) | log |

## Issues found during the test

1. **Noto Hebrew fonts have no digits or punctuation.** The luaotfload fallback only loads when given as `"[absolute path]"`; the `file:` and `kpse:` forms fail with "metric data not found".
2. **The bibliography labels `[1]`/`[2]` were clipped** at the left edge in both columns. This is the 22 pt left shift seen in the smoke test. **Fixed by babel `layout=lists`**: the bibliography now starts exactly at the text edge (x = 14.2 pt in both columns). This resolves open finding 1 of `tests/lualatex-smoke/RESULTS.md`; `smoke.tex` itself was not changed.
3. A preamble bug of mine (`\makeatletter` inside `\AtBeginDocument`) broke Pairing A's first build. Fixed.

## Recommendation

**Pairing A (Frank Ruhl Libre + Heebo, with Libertinus Serif for Latin)**:
- It has every glyph the book needs inside the fonts themselves, so no fallback machinery is needed and the build is simpler and more reproducible.
- Its classic book look is closest to the current design.

**Visible difference:** Frank Ruhl Libre gives a classic, book-like Hebrew page with sharper thick–thin strokes and slightly tighter lines, while Noto Serif Hebrew looks rounder, wider and more uniform, and borrows every digit and punctuation mark from another font.

## Not verified here

- The full 20-page book with either pairing.
- MiKTeX.
- Print output.

The decision is the user's.
