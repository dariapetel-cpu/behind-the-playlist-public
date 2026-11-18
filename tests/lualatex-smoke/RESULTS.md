# LuaLaTeX smoke test: results, 2026-11-18

**Test:** `smoke.tex`, one isolated page that touches nothing in `book/` or `submission/`.
**PDF:** `tests/lualatex-smoke/smoke.pdf`
**Toolchain:**
- LuaHBTeX 1.24 (TeX Live 2026 BasicTeX, macOS) and Biber 2.22.
- `biblatex-ieee` v1.4g, installed by the user on 2026-11-18.
- Babel with `bidi=basic,layout=graphics` and `onchar=ids fonts`.
- macOS fonts (Times New Roman, Arial Hebrew), used for this test only.

**Build:** `lualatex → biber → lualatex → lualatex`, from a clean start (earlier auxiliary files were renamed to `*.prev`).

## Final run (style=ieee)

| Check | Method | Result |
|---|---|---|
| Build | exit codes; log | ✅ exit 0 on every pass; 0 errors; **0 missing characters**; 0 undefined citations; 0 overfull boxes; biber 0 warnings |
| Citation ↔ bibliography | glyphs at the end of the cited line; bibliography entry text | ✅ In-text `[1]` (reads „…שונות [1]." with mirrored brackets) matches entry **[1] Y. Hu, Y. Koren, and C. Volinsky, “Collaborative filtering for implicit feedback datasets”, in *2008 Eighth IEEE ICDM*, IEEE, 2008, pp. 263–272, doi: 10.1109/ICDM.2008.22**, which is `hu2008collaborative`, the only key cited |
| IEEE format | entry text | ✅ Initials before surnames, quoted title, "in" + italic venue, pages, doi, "Accessed: … [Online]. Available:", all IEEE features (biblatex-ieee) |
| Mixed Hebrew-English sentence | glyph x-order + 140 dpi render | ✅ Reads right to left; "Spotify" and "Radiohead" stay left to right inside the Hebrew |
| Number in parentheses | glyph order around "344" | ✅ Mirrored correctly: „של (344 שירים)," |
| Formula | render + glyphs | ✅ Legible: cos(θ) = a·b / (‖a‖‖b‖) = 26 / (√30·5) ≈ 0.95, with Latin glyphs present |
| Hebrew TikZ labels | glyphs collected inside each drawn box | ✅ Right box: „איסוף אותות"; left box: „דירוג מועמדים"; every glyph fully inside its box; no label glyphs outside the boxes |
| Pages | PDF | ✅ 1 page |

## Open findings (not fixed in this isolated test)

1. **The bibliography list is shifted into the left margin.** The English bibliography block runs from x = 48.6 pt to 502.1 pt, while the text block runs from 70.9 to 524.4 pt, so it is 22 pt too far left. Nothing is clipped. This is likely the list indentation being applied on the wrong side for an English list inside an RTL document. **Fix in the CLS stage** (`TODO.md` P2).
2. **Arial Hebrew has no italic.** A font-shape warning; IEEE italics in Hebrew context fall back to upright. This will be resolved by the open-licence font choice (decision F-2), which needs a bold/number/punctuation glyph test.
3. **The bibliography heading is the English "References"**, because the list sits in an `english` block. The book uses the Hebrew heading „מקורות"; this needs handling in the CLS stage.

## Problems found while building the test (preliminary runs, 2026-11-18)

These are recorded in `docs/prompts.md`, Prompt 15. Incident reports are pending (`docs/incidents/README.md`).

| # | Finding | Isolated by | Resolution in this test |
|---|---|---|---|
| a | **New Peninim MT** (the book's current body font) under LuaLaTeX: any `\section` makes the following text vanish (blank page, overfull vbox) | Bisection: plain bold works; Arial Hebrew, Arial and Times work | Not used; the open-licence fonts replace it (F-2) |
| b | Under `bidi=basic`, TikZ node labels away from the picture origin land **outside their boxes** | Variants: plain/align/text width all fail; language wrappers fix placement but leave brackets unmirrored | `layout=graphics` fixes both |
| c | Without `onchar=ids fonts`: Latin glyphs are missing and brackets are not mirrored | Minimal paragraph test | `onchar=ids fonts` |
| d | `cos` in math was set in the Hebrew font (no Latin glyphs) | Log "Missing character: c" | `\setmathrm{Times New Roman}` |
| e | One probe sequence produced an empty `.bbl` (biber read a control file without the citation) | Re-running biber | The final clean run is correct |

## Still unverified

- **MiKTeX compatibility** (decision F-4; risk R-1).
- **Open-licence fonts**, not yet chosen or tested (F-2).
- **The full book under LuaLaTeX**, including the cover, boxes, floats, footer, the graph PDF and the 20-page layout. Only this one page has been built.
- **Byte-identical rebuilds** (A2 p. 5).

## Update 2026-11-18 (Prompt 17, recorded separately in `tests/font-compare/RESULTS.md`)

Open finding 1 (the bibliography list shifted 22 pt into the left margin) **has a verified fix**: babel `layout=lists`, i.e. `layout=graphics.lists`. In the font-comparison builds the bibliography starts exactly at the text edge. `smoke.tex` itself was not changed.
