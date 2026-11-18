# Bundled fonts: Pairing A (chosen by the user, 2026-11-18, Prompt 18)

These are byte-identical to the files tested in `tests/font-compare/` (see `SHA256SUMS`). All are under the **SIL Open Font License 1.1**; each folder contains its `OFL.txt`.

| Role | Font | Folder | Source (pinned) |
|---|---|---|---|
| Hebrew body (serif) | Frank Ruhl Libre (Regular, Bold) | `FrankRuhlLibre/` | https://github.com/fontef/frankruhllibre @ `2372d1998e51dc011f86554c0d23f1ccf44afddf` (`fonts/ttf/`) |
| Hebrew and Latin headings (sans) | Heebo (Regular, Bold) | `Heebo/` | https://github.com/OdedEzer/heebo @ `76c7d538568d3e6d7f052a12c5675c84430df25f` (`fonts/ttf/`) |
| English text, italics, math roman | Libertinus Serif (Regular, Italic, Bold, BoldItalic) | `LibertinusSerif/` | https://github.com/alerque/libertinus release v7.051 (`static/OTF/`) |

The settings that passed the comparison (`tests/font-compare/pairA.tex`) are applied in `book/behind-the-playlist.cls`:
- Scales: Frank Ruhl Libre 0.96, Heebo 0.97, Libertinus Serif 1.03.
- Babel: `bidi=basic`, `layout=graphics.lists` and `onchar=ids fonts`.
