# Behind the Playlist: build (LuaLaTeX + Biber + biblatex-ieee, class book/behind-the-playlist.cls).
# Requires TeX Live 2026 (BasicTeX + the packages listed in README) and the .venv (requirements.txt).
# Fonts are bundled in book/fonts/ (OFL); no system fonts are needed.
# The XeLaTeX build (book/style.sty) was retired on 2026-11-18; its last PDF is kept in backups/.
TEX    := /Library/TeX/texbin
PY     := .venv/bin/python
PDF    := build/behind-the-playlist-lualatex.pdf
OUT    := build/lualatex

.PHONY: all figures pdf lualatex check screenshots submission clean candidate
all: pdf

figures: book/figures/noa_week.pdf
book/figures/noa_week.pdf: figures/noa_week.py figures/data/noa_week.csv
	$(PY) figures/noa_week.py

# graph -> lualatex -> biber -> lualatex (latexmk decides the passes) -> automated checks
pdf: figures
	cd book && PATH=$(TEX):$$PATH latexmk -lualatex -interaction=nonstopmode -halt-on-error \
	  -outdir=../$(OUT) main.tex
	cp $(OUT)/main.pdf $(PDF)
	$(PY) tools/check_pdf.py $(PDF) $(OUT)/main.log $(OUT)/pages

lualatex: pdf

check:
	$(PY) tools/check_pdf.py $(PDF) $(OUT)/main.log $(OUT)/pages

# README screenshots (student IDs masked) + page map, from the built PDF
screenshots: pdf
	$(PY) tools/screenshots.py $(PDF) readme docs/screenshots docs/screenshots/pagemap.json

# Build, check, screenshots, then copy into submission/ (only after the PDF is approved)
submission: pdf screenshots
	mkdir -p submission && cp $(PDF) submission/behind-the-playlist.pdf

clean:
	cd book && PATH=$(TEX):$$PATH latexmk -C -outdir=../$(OUT) main.tex; rm -rf $(OUT)/pages $(PDF)

# QA candidate (Fixer): separate build folder and PDF; never touches submission/ or the approved preview.
CAND := build/behind-the-playlist-candidate.pdf
candidate: figures
	cd book && PATH=$(TEX):$$PATH latexmk -lualatex -interaction=nonstopmode -halt-on-error \
	  -outdir=../build/candidate main.tex
	cp build/candidate/main.pdf $(CAND)

