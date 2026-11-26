"""Mutation tests for the QA harness (QA round 2). Run: python -m unittest discover -s tests

Every test damages a COPY (temporary folder) of the approved PDF, the sources or a log, runs the real
command line and asserts that (1) the run exits 1 and (2) the specific check reports the fail.
The tracked PDF and the sources are only read; tearDownModule verifies the PDF's hash.

The LaTeX and Biber logs below are SYNTHETIC FIXTURES, written by this file. No TeX build is run, so a
pass here says nothing about a real build log. IDs are fake and assembled at run time, so that this file
itself holds no nine-digit number.
"""
import hashlib, json, os, re, shutil, subprocess, sys, tempfile, unittest
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "pdf/behind-the-playlist.pdf"
FAKE = "31" + "4159" + "265"
def _valid():
    """Nine fake digits with a correct check digit, computed so that no such number is written in this file."""
    s = FAKE[:8]; t = sum(x if x < 10 else x - 9 for x in (int(c) * (1 + i % 2) for i, c in enumerate(s)))
    return s + str(-t % 10)
VALID = _valid()
SYNTHETIC_LOG = ("This is LuaHBTeX, Version 1.24.0 (SYNTHETIC TEST FIXTURE)\n"
                 "Document Class: behind-the-playlist 2026/11/18 v1.1 Behind the Playlist book class\n"
                 "Output written on main.pdf (20 pages, 333333 bytes).\n")
SYNTHETIC_BLG = "[0] Config.pm:307> INFO - This is Biber 2.21 (SYNTHETIC TEST FIXTURE)\nINFO - Output to main.bbl\n"
BLACK, WHITE, BG = (0, 0, 0), (1, 1, 1), (242 / 255,) * 3


def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def setUpModule():
    global TMP, PROJ, PDF_SHA, _tmp
    PDF_SHA = sha(PDF)
    _tmp = tempfile.TemporaryDirectory(prefix="qa-mut-"); TMP = Path(_tmp.name); PROJ = TMP / "project"
    skip = {".git", ".venv", "Library", "build", "submission", "backups", "__pycache__"}
    def ignore(d, names):
        rel = Path(d).relative_to(ROOT).as_posix()
        return [n for n in names if n in skip or n.endswith((".ttf", ".otf")) or (f"{rel}/".startswith("docs/qa/") and n.endswith(".png"))]
    shutil.copytree(ROOT, PROJ, ignore=ignore)
    for f in PROJ.rglob("*.jsonl"): f.write_text("{}\n")     # large transcripts: kept as link targets only


def tearDownModule():
    _tmp.cleanup()
    assert sha(PDF) == PDF_SHA, "the tracked PDF was changed by a test"


class Case(unittest.TestCase):
    def setUp(self):
        self.dir = Path(tempfile.mkdtemp(dir=TMP)); self.out = self.dir / "out"
        self.log(SYNTHETIC_LOG)
        self.addCleanup(lambda: self.assertEqual(sha(PDF), PDF_SHA))

    # --- fixtures
    def log(self, text, name="main.log", blg=SYNTHETIC_BLG):
        self.logfile = self.dir / name; self.logfile.write_text(text, encoding="utf-8")
        if blg is not None: (self.dir / "main.blg").write_text(blg, encoding="utf-8")

    def pdf(self, edit, name="m.pdf"):
        d = pymupdf.open(PDF); edit(d); p = self.dir / name; d.save(p); d.close(); return p

    def rect(self, n, r, colour):
        return self.pdf(lambda d: d[n-1].draw_rect(pymupdf.Rect(r), color=None, fill=colour))

    def wipe(self, *areas):
        def edit(d):
            for n, r in areas:
                d[n-1].add_redact_annot(pymupdf.Rect(r), fill=False); d[n-1].apply_redactions(images=0, graphics=0)
        return self.pdf(edit)

    def text(self, n, pos, s, **kw):
        return self.pdf(lambda d: d[n-1].insert_text(pos, s, fontsize=kw.pop("size", 11), **kw))

    def source(self, rel, change):
        """Edit a file of the project copy; restored after the test. change(None-or-str) -> str, or None = delete."""
        f = PROJ / rel; old = f.read_bytes() if f.exists() else None
        def restore():
            if old is None: f.unlink(missing_ok=True)
            else: f.parent.mkdir(parents=True, exist_ok=True); f.write_bytes(old)
        self.addCleanup(restore)
        new = change(old.decode("utf-8").replace("\r\n", "\n") if old is not None else None)
        f.parent.mkdir(parents=True, exist_ok=True)
        if new is None: f.unlink()
        else: f.write_bytes(new if isinstance(new, bytes) else new.encode("utf-8"))

    def append(self, rel, s): self.source(rel, lambda t: t + "\n" + s + "\n")

    # --- running
    def cli(self, *args, root=None, env=None):
        e = dict(os.environ, PYTHONDONTWRITEBYTECODE="1"); e.update(env or {}); e = {k: v for k, v in e.items() if v is not None}
        return subprocess.run([sys.executable, str((root or PROJ) / "tools/qa/qa_lib.py"), *map(str, args)],
                              capture_output=True, text=True, encoding="utf-8", errors="replace", env=e, cwd=str(PROJ))

    def run_qa(self, pdf=None, checks="all", log=True, extra=(), root=None, env=None, absolute=False):
        pdf = pdf or (root or PROJ) / "pdf/behind-the-playlist.pdf"
        if not absolute and root is None: pdf = os.path.relpath(pdf, PROJ)      # the old code crashed on absolute outside paths (L3)
        a = ["--pdf", pdf, "--checks", checks, "--out", self.out, *extra]
        r = self.cli(*a, *(["--log", self.logfile] if log else ["--no-log"]), root=root, env=env)
        f = self.out / "findings.json"
        self.found = json.loads(f.read_text(encoding="utf-8"))["findings"] if f.exists() else None
        return r

    def fails(self, name, where=""):
        return [f for f in self.found or [] if f.get("name") == name and f["status"] == "fail" and where in f["where"]]

    def assertFails(self, name, pdf=None, where="", **kw):
        r = self.run_qa(pdf, **kw); blob = r.stdout + r.stderr + json.dumps(self.found, ensure_ascii=False)
        msg = f"\n[totals] {r.stdout.strip()} exit={r.returncode} {r.stderr[-300:]}"
        self.assertTrue(self.fails(name, where), f"check {name} did not fail{msg}; failed: {sorted({f.get('name') for f in self.found or [] if f['status'] == 'fail'}, key=str)}")
        self.assertEqual(r.returncode, 1, msg)
        self.assertNotIn(FAKE, blob, "a report printed an ID value")
        return r


class ValidInput(Case):
    def test_valid_project_passes_with_synthetic_log(self):
        r = self.run_qa(root=ROOT)
        self.assertEqual((r.returncode, [f for f in self.found if f["status"] == "fail"]), (0, []), r.stdout + r.stderr)

    def test_valid_project_passes_without_log_and_log_checks_are_na(self):
        r = self.run_qa(root=ROOT, log=False)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        st = {f["name"]: f["status"] for f in self.found}
        self.assertEqual([st[k] for k in ("typeset.log", "typeset.biber", "cls.log")], ["n/a"] * 3)

    def test_valid_project_copy_passes(self):
        r = self.run_qa(); self.assertEqual(r.returncode, 0, r.stdout + r.stderr + str([f for f in self.found if f["status"] == "fail"]))

    def test_valid_passes_in_the_machine_locale(self):
        r = self.run_qa(log=False, env={"PYTHONUTF8": None, "PYTHONIOENCODING": None})
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_tracked_pdf_is_the_approved_one(self):
        b = json.loads((ROOT / "tools/qa/visual_baseline.json").read_text(encoding="utf-8"))
        self.assertEqual(sha(PDF), b["sha256"])


class H1Visual(Case):
    """D4 H1, N1, N2, N3, N6: what the reader sees, not what the text layer says."""
    def both(self, n, r, name, where):
        for c in (BLACK, WHITE):
            with self.subTest(colour=c): self.assertFails(name, self.rect(n, r, c), where)
    def test_h1_cover_covered(self): self.both(1, (40, 40, 555, 800), "visual.contrast", "p.1")
    def test_h1_fig21_covered(self): self.both(7, (75, 80, 521, 276), "visual.region.fig-2.1", "p.7")
    def test_h1_p9_formulas_covered(self): self.both(9, (85, 262, 507, 354), "visual.region.formulas-p9", "p.9")
    def test_h1_table41_covered(self): self.both(11, (71, 192, 524, 326), "visual.region.table-4.1", "p.11")
    def test_h1_p12_prose_covered(self): self.both(12, (71, 300, 524, 745), "visual.contrast", "p.12")
    def test_h1_fig61_covered(self):
        self.both(14, (71, 425, 524, 588), "visual.region.fig-6.1", "p.14")
        self.both(14, (71, 425, 529, 588), "visual.region.fig-6.1", "p.14")
    def test_h1_fig21_bars_only_covered(self):
        self.assertFails("visual.region.fig-2.1", self.rect(7, (110, 112, 512, 238), BG))
    def test_h1_p12_text_removed(self): self.assertFails("typeset.text-complete", self.wipe((12, (60, 300, 535, 745))), "05-hasha")
    def test_one_removed_line_fails(self): self.assertFails("typeset.text-complete", self.wipe((12, (60, 500, 535, 512))), "05-hasha")
    def test_n1_every_page_white(self):
        def edit(d):
            for p in d: p.draw_rect(p.rect, color=None, fill=WHITE)
        self.assertFails("visual.contrast", self.pdf(edit)); self.assertEqual(len(self.fails("visual.contrast")), 20)
        self.assertTrue(self.fails("visual.fingerprint"))
    def test_n2_body_removed_per_page(self):
        for n, f in ((2, "00-abs"), (5, "01-boker"), (13, "05-hasha"), (15, "06-shmone"), (17, "07-bua"), (18, "08-play")):
            with self.subTest(page=n):
                def edit(d):
                    r = pymupdf.Rect(60, 70, 535, 750); d[n-1].add_redact_annot(r, fill=WHITE); d[n-1].apply_redactions()
                self.assertFails("typeset.text-complete", self.pdf(edit), f)
    def test_n2_contents_page_removed(self): self.assertFails("typeset.toc-page", self.wipe((3, (60, 70, 535, 750))))
    def test_n2_bibliography_text_removed(self): self.assertFails("typeset.bib-titles", self.wipe((19, (120, 200, 535, 750))))
    def test_n3_p19_footer_covered(self): self.assertFails("footer.p19", self.rect(19, (60, 775, 535, 800), WHITE)); self.assertTrue(self.fails("footer.visible"))
    def test_n3_pdf_cut(self):
        for k in (1, 10):
            with self.subTest(pages=k): self.assertFails("footer.p19", self.pdf(lambda d: d.select(range(k))), checks="footer")
    def test_n6_rotated_page(self): self.assertFails("visual.page-geometry", self.pdf(lambda d: d[11].set_rotation(180)))
    def test_n6_wrong_image_over_formulas(self):
        pix = pymupdf.open(PDF)[1].get_pixmap(dpi=50)
        self.assertFails("visual.region.formulas-p9", self.pdf(lambda d: d[8].insert_image(pymupdf.Rect(85, 262, 507, 354), pixmap=pix, keep_proportion=False)))
        self.assertTrue(self.fails("visual.raster-images"))
    def test_n6_annotation_over_table(self):
        def edit(d):
            a = d[10].add_rect_annot(pymupdf.Rect(71, 192, 524, 326)); a.set_colors(stroke=BLACK, fill=BLACK); a.update()
        self.assertFails("visual.annotations", self.pdf(edit)); self.assertTrue(self.fails("visual.region.table-4.1"))
    def test_n6_text_over_prose(self):
        self.assertFails("visual.overlap", self.text(12, (80, 403), "OVERPRINT OVERPRINT OVER", size=20)); self.assertTrue(self.fails("typeset.text-complete"))
    def test_n18_near_white_text(self):
        p = self.text(12, (80, 760), "hidden words here", color=(.99, .99, .99))
        self.assertFails("typeset.check-pdf", p); self.assertTrue(self.fails("visual.contrast"))
        self.assertIn("low contrast", self.fails("typeset.check-pdf")[0]["evidence"])     # N8: the reason is kept
    def test_shifted_page_changes_the_fingerprint(self):
        def edit(d):
            src = pymupdf.open(PDF); p = d[11]; p.clean_contents(); p.draw_rect(p.rect, color=None, fill=BG); p.show_pdf_page(p.rect + (0, 6, 0, 6), src, 11)
        self.assertFails("visual.fingerprint", self.pdf(edit))
    def test_removed_arrow_changes_the_fingerprint(self): self.assertFails("visual.fingerprint", self.rect(14, (388, 445, 411, 465), BG))
    def test_resaved_pdf_keeps_the_fingerprint(self):
        p = self.dir / "r.pdf"; d = pymupdf.open(PDF); d.save(p, garbage=4, deflate=True, clean=True); d.close()
        self.assertEqual(self.run_qa(p).returncode, 0, str([f for f in self.found if f["status"] == "fail"]))
    def test_cover_title_removed(self): self.assertFails("typeset.cover-text", self.wipe((1, (300, 60, 560, 150))))
    def test_pages_swapped(self): self.assertFails("footer.numbers", self.pdf(lambda d: d.select([*range(11), 12, 11, *range(13, 20)])))
    def test_baseline_is_never_written_without_approval(self):
        b = PROJ / "tools/qa/visual_baseline.json"; before = b.read_bytes()
        r = self.cli("--pdf", PROJ / "pdf/behind-the-playlist.pdf", "--write-visual-baseline")
        self.assertEqual((r.returncode, b.read_bytes() == before), (2, True))
    def test_missing_baseline_fails(self):
        self.source("tools/qa/visual_baseline.json", lambda t: None); self.assertFails("visual.fingerprint")


class H2NoSilentSkips(Case):
    def test_p9_table_removed(self): self.assertFails("table.p9-columns", self.wipe((9, (345, 166, 510, 235))))
    def test_p9_header_removed(self): self.assertFails("table.p9-columns", self.wipe((9, (345, 166, 510, 183))))
    def test_p9_one_number_removed(self): self.assertFails("table.p9-values", self.wipe((9, (430, 190, 440, 203))))
    def test_table41_header_removed_although_words_are_in_the_prose(self): self.assertFails("table.4.1-columns", self.wipe((11, (71, 196, 524, 211))))
    def test_blg_absent(self):
        (self.dir / "main.blg").unlink(); self.assertFails("typeset.biber")
    def test_blg_warning(self): self.log(SYNTHETIC_LOG, blg=SYNTHETIC_BLG + "WARN - x\n"); self.assertFails("typeset.biber")
    def test_blg_unrelated_text(self): self.log(SYNTHETIC_LOG, blg="INFO - stub\n"); self.assertFails("typeset.biber")
    def test_fig61_labels_removed_and_blamed_on_p14(self):
        p = self.wipe((14, (71, 428, 530, 560)))
        self.assertFails("img.blocks", p, "p.14"); self.assertFalse([f for f in self.found if f["status"] == "fail" and "p.15" in f["where"]])
        self.assertEqual(len(self.fails("bidi.phrase.diagram", "p.14")), 8)
    def test_fig61_labels_and_p15_words_removed(self):
        words = pymupdf.open(PDF)[14].search_for("לולאת") + pymupdf.open(PDF)[14].search_for("ולמידה")
        self.assertFails("img.blocks", self.wipe((14, (71, 428, 530, 560)), *[(15, r) for r in words]), "p.14")
    def test_crash_becomes_a_fail(self):
        self.source("tools/qa/expectations.json", lambda t: t.replace('"p9_rows"', '"p9_rows_x"')); self.assertFails("table.crash")
    def test_declared_minimum_is_enforced(self):
        self.source("tools/qa/expectations.json", lambda t: re.sub(r'"footer": \d+', '"footer": 99', t)); self.assertFails("footer.min-findings")


class H3Logs(Case):
    def bad(self, text, reason, **kw):
        self.log(text, **kw); self.assertFails("typeset.check-pdf"); self.assertIn(reason, self.fails("typeset.check-pdf")[0]["evidence"])
        r = subprocess.run([sys.executable, str(PROJ / "tools/check_pdf.py"), str(PDF), str(self.logfile), str(self.dir / "pg")],
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        self.assertEqual(r.returncode, 1, r.stdout)
    def test_empty_log(self): self.bad("", "not a LuaLaTeX log")
    def test_file_line_error(self): self.bad(SYNTHETIC_LOG + "./chapters/05-hasha.tex:12: error: Undefined control sequence.\n./main.tex:30: Undefined control sequence.\n", "errors=2")
    def test_classic_error(self): self.bad(SYNTHETIC_LOG + "! Undefined control sequence.\n", "errors=1")
    def test_overfull_vbox(self): self.bad(SYNTHETIC_LOG + "Overfull \\vbox (50.0pt too high) has occurred while \\output is active []\n", "overfull>2pt")
    def test_overfull_hbox(self): self.bad(SYNTHETIC_LOG + "Overfull \\hbox (50.0pt too wide) in paragraph at lines 1--2\n", "overfull>2pt")
    def test_small_overfull_is_tolerated(self):
        self.log(SYNTHETIC_LOG + "Overfull \\vbox (1.5pt too high) detected at line 3\n"); self.assertEqual(self.run_qa().returncode, 0)
    def test_n7_unrelated_text(self): self.bad("shopping list\n" * 30, "not a LuaLaTeX log")
    def test_n7_fatal(self): self.bad(SYNTHETIC_LOG + "!  ==> Fatal error occurred, no output PDF file produced!\n", "fatal=")
    def test_n7_rerun(self): self.bad(SYNTHETIC_LOG + "LaTeX Warning: Label(s) may have changed. Rerun to get cross-references right.\n", "reruns=")
    def test_n7_incomplete_build(self): self.bad(SYNTHETIC_LOG.rsplit("Output", 1)[0], "did not complete")
    def test_n7_pages_differ(self): self.bad(SYNTHETIC_LOG.replace("20 pages", "19 pages"), "19 pages written")
    def test_n7_wrapped_undefined_reference(self):
        line = "LaTeX Warning: Reference `fig:" + "x" * 34 + "' on page 12 undefined on input line 5."
        line = line.replace("x" * 34, "x" * (34 + 79 - line.index("undefined") - 4))      # the break falls inside "undefined"
        self.bad(SYNTHETIC_LOG + line[:79] + "\n" + line[79:] + "\n", "undef_refs=")
    def test_n7_wrapped_undefined_citation(self):
        line = "LaTeX Warning: Citation 'abc' on page 12 "; line += "z" * (76 - len(line)) + " undefined on input line 5."
        self.bad(SYNTHETIC_LOG + line[:79] + "\n" + line[79:] + "\n", "undef_cites=")
    def test_complete_79_column_line_does_not_swallow_an_error(self): self.bad(SYNTHETIC_LOG + "y" * 79 + "\n! Emergency stop.\n", "errors=1")
    def test_n7_unrelated_one_page_pdf(self):
        d = pymupdf.open(); d.new_page().insert_text((72, 72), "other"); p = self.dir / "o.pdf"; d.save(p)
        self.assertFails("typeset.check-pdf", p); self.assertTrue(self.fails("typeset.pages"))
    def test_n9_log_named_txt_is_not_a_biber_log(self):
        self.log(SYNTHETIC_LOG, name="main.txt"); self.assertFails("typeset.biber")
    def test_version_in_log_differs(self): self.log(SYNTHETIC_LOG.replace("v1.1", "v1.0")); self.assertFails("cls.log")


class Cli(Case):
    """H3 exit codes, L3, N10, N11."""
    def seed(self): self.out.mkdir(parents=True, exist_ok=True); (self.out / "findings.json").write_text('{"findings":[]}')
    def usage(self, *args):
        self.seed(); r = self.cli(*args, "--out", self.out)
        self.assertEqual(r.returncode, 2, r.stdout + r.stderr); self.assertFalse((self.out / "findings.json").exists(), "stale findings.json left")
    def test_n11_unknown_check(self): self.usage("--pdf", PDF, "--no-log", "--checks", "typest")
    def test_n10_log_absent(self): self.usage("--pdf", PDF, "--log", self.dir / "nope.log")
    def test_no_log_argument(self): self.usage("--pdf", PDF)
    def test_log_and_no_log(self): self.usage("--pdf", PDF, "--no-log", "--log", self.logfile)
    def test_pdf_absent(self): self.usage("--pdf", self.dir / "nope.pdf", "--no-log")
    def test_pdf_damaged(self):
        p = self.dir / "x.pdf"; p.write_bytes(b"not a pdf"); self.usage("--pdf", p, "--no-log")
    def test_l3_outside_absolute_path(self):
        p = self.pdf(lambda d: None); r = self.run_qa(p, absolute=True); self.assertIsNotNone(self.found, r.stderr)
        self.assertEqual(r.returncode, 0, str([f for f in self.found if f["status"] == "fail"]))
    def test_l3_outside_relative_path(self):
        p = self.pdf(lambda d: None); r = self.run_qa(os.path.relpath(p, PROJ), checks="code", absolute=True); self.assertEqual(r.returncode, 0, r.stderr)
    def test_n11_submission_edition_on_public_pdf(self):
        self.assertFails("typeset.cover-mask", extra=("--edition", "submission"))


class Privacy(Case):
    """D4 M3, N11, N12, N13."""
    def test_m3_id_in_file_not_declared_in_main(self): self.source("docs/leak.txt", lambda t: f"x {FAKE} y"); self.assertFails("infra.privacy-files")
    def test_m3_git_and_venv_are_excluded(self):
        for d in (".git", ".venv"): self.source(f"{d}/leak.txt", lambda t: FAKE)
        self.source("book/main.tex", lambda t: t + f"% \\studentid{{{FAKE}}}\n")
        self.assertFails("infra.privacy-files"); self.assertNotIn("leak", self.fails("infra.privacy-files")[0]["evidence"])
    def test_similar_folder_name_is_not_excluded(self):
        self.source("docs/.gitnotes/leak.txt", lambda t: FAKE); self.addCleanup(shutil.rmtree, PROJ / "docs/.gitnotes", True); self.assertFails("infra.privacy-files")
    def test_n13_spaced_hyphenated_grouped(self):
        for s in (FAKE[:3] + " " + FAKE[3:6] + " " + FAKE[6:], FAKE[:8] + "-" + FAKE[8:], " ".join(FAKE), "ID: " + FAKE[:5] + "-" + FAKE[5:],
                  FAKE[:4] + "\u200f" + FAKE[4:], "id" + FAKE, '{"a":"line\\n' + FAKE + '"}'):
            with self.subTest(form=re.sub(r"\d", "#", s)):
                self.source("docs/leak.txt", lambda t: s); self.assertFails("infra.privacy-files", checks="infra")
    def test_n13_utf16(self):
        for enc in ("utf-16", "utf-16-le", "utf-16-be"):
            with self.subTest(enc=enc): self.source(f"docs/leak-{enc[-2:]}.txt", lambda t: f"abc {FAKE} def".encode(enc)); self.assertFails("infra.privacy-files", checks="infra")
    def test_n13_file_name(self): self.source(f"docs/leak{FAKE}.txt", lambda t: "x"); self.assertFails("infra.privacy-names")
    def test_n13_studentid_with_space(self): self.append("book/main.tex", f"% \\studentid {{{FAKE}}}"); self.assertFails("infra.privacy-files")
    def test_id_in_a_tracked_pdf_of_the_tree(self):
        d = pymupdf.open(); d.new_page().insert_text((72, 72), FAKE); self.source("docs/x.pdf", lambda t: d.tobytes()); self.assertFails("infra.privacy-files")
    def test_hash_uuid_base64_are_not_ids(self):
        self.source("docs/ok.txt", lambda t: f"sha ab{FAKE}cd uuid 75893912-2f2f x{FAKE}y 0.{FAKE} 10.1145/138859.138867 2026-11-14 18:30"); self.assertEqual(self.run_qa(checks="infra").returncode, 0, str(self.found))
    def test_allow_list_is_bound_to_its_file(self): self.source("docs/leak.txt", lambda t: "collections/catalog/" + FAKE); self.assertFails("infra.privacy-files")
    def test_n11_id_on_cover_reports(self):
        self.assertFails("bidi.public-cover", self.text(1, (80, 700), FAKE, color=WHITE)); self.assertTrue(self.fails("typeset.cover-mask"))
        self.assertFalse((self.out / "pages/page-01.png").exists(), "an unmasked cover render was left")
    def test_n12_hyphenated_id_on_cover(self):
        self.assertFails("bidi.public-cover", self.text(1, (80, 700), FAKE[:8] + "-" + FAKE[8:], color=WHITE))
        self.assertTrue(self.fails("infra.privacy-pdf")); self.assertFalse((self.out / "pages/page-01.png").exists())
    def test_n12_spaced_id_on_cover(self): self.assertFails("bidi.public-cover", self.text(1, (80, 700), FAKE[:3] + " " + FAKE[3:], color=WHITE))
    def test_n12_id_on_p5(self):
        self.assertFails("infra.privacy-pdf", self.text(5, (80, 700), FAKE)); self.assertFalse((self.out / "pages/page-05.png").exists())
    def test_n12_id_in_metadata(self): self.assertFails("infra.privacy-pdf", self.pdf(lambda d: d.set_metadata({"keywords": FAKE})))
    def test_n12_id_in_link(self): self.assertFails("infra.privacy-pdf", self.pdf(lambda d: d[4].insert_link({"kind": pymupdf.LINK_URI, "from": pymupdf.Rect(80, 600, 100, 620), "uri": "https://x.org/" + FAKE})))
    def test_n12_raster_id_on_cover(self):
        t = pymupdf.open(); t.new_page(width=120, height=30).insert_text((5, 20), FAKE)
        self.assertFails("visual.raster-images", self.pdf(lambda d: d[0].insert_image(pymupdf.Rect(80, 690, 200, 720), pixmap=t[0].get_pixmap())))
    def test_n12_iso_date_on_cover(self): self.assertFails("bidi.public-cover", self.text(1, (80, 700), "2026-11-18", color=WHITE))
    def test_pdf_file_name(self): self.assertFails("infra.privacy-pdf", self.pdf(lambda d: None, name=f"a-{FAKE}.pdf"))


class RecheckPrivacy(Case):
    """D5 gaps, item 1 (and item 7: scans that no test protected)."""
    def test_loose_forms_with_valid_check_digit(self):
        v = VALID; abc = (v[:3], v[3:6], v[6:])
        forms = {"dots": ".".join(abc), "slash": v[:8] + "/" + v[8:], "commas": ",".join(abc), "line break": v[:5] + "\n" + v[5:],
                 "nbsp": "&nbsp;".join(abc), "spaces": "  ".join(abc), "letters after": v + "x", "letters before": "num" + v,
                 "year before": "2026 " + v, "digit after": v + " 1", "date after": v + " 2026-11-25", "two IDs": v + " " + v, "number before": "1 " + v}
        for n, s in forms.items():
            with self.subTest(form=n):
                self.source("docs/leak.txt", lambda t: f"x {s} y"); self.assertFails("infra.privacy-files", checks="infra")
                self.assertNotIn(v, json.dumps(self.found))
    def test_ordinary_numbers_pass(self):
        bad = VALID[:8] + str((int(VALID[8]) + 1) % 10)
        self.source("docs/ok.txt", lambda t: f"333,333,333 bytes; 192.168.100.123; 978-0-262-03384-8; {bad[:3]}.{bad[3:6]}.{bad[6:]}; num{bad}; hash a{VALID}b; 2026-11-25 10:11:12")
        self.assertEqual(self.run_qa(checks="infra").returncode, 0, str([f for f in self.found if f["status"] == "fail"]))
    def pdf_hit(self, edit, label, name="infra.privacy-pdf"):
        self.assertFails(name, self.pdf(edit), checks="infra"); self.assertIn(label, self.fails(name)[0]["evidence"])
    def test_xmp(self): self.pdf_hit(lambda d: d.set_xml_metadata(f"<x>{FAKE}</x>"), "XMP")
    def test_bookmark(self): self.pdf_hit(lambda d: d.set_toc(d.get_toc() + [[1, FAKE, 1]]), "bookmarks")
    def test_annotation(self): self.pdf_hit(lambda d: d[4].add_text_annot((80, 700), FAKE), "p.5 annotations")
    def test_form_field(self):
        def edit(d):
            w = pymupdf.Widget(); w.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT; w.field_name = "f"; w.field_value = FAKE
            w.rect = pymupdf.Rect(80, 700, 200, 715); d[4].add_widget(w)
        self.pdf_hit(edit, "p.5 form fields")
    def test_custom_info_key(self):
        def edit(d): d.xref_set_key(int(d.xref_get_key(-1, "Info")[1].split()[0]), "StudentNo", f"({FAKE})")
        self.pdf_hit(edit, "document info keys")
    def test_metadata_dotted(self): self.pdf_hit(lambda d: d.set_metadata({"keywords": f"{VALID[:3]}.{VALID[3:6]}.{VALID[6:]}"}), "metadata")
    def test_attachment_content(self): self.pdf_hit(lambda d: d.embfile_add("a.txt", FAKE.encode()), "attachments")
    def test_attachment_without_id(self): self.pdf_hit(lambda d: d.embfile_add("a.txt", b"x"), "attachments", "infra.pdf-hidden-content")
    def test_javascript(self):
        def edit(d): d.xref_set_key(d.pdf_catalog(), "OpenAction", "<</S/JavaScript/JS(x)>>")
        self.pdf_hit(edit, "JavaScript", "infra.pdf-hidden-content")
    def test_layer_switched_off(self):
        def edit(d): d[7].insert_text((80, 700), FAKE, oc=d.add_ocg("x", on=False))
        self.pdf_hit(edit, "optional-content", "infra.pdf-hidden-content")


class RecheckLogs(Case):
    """D5 gaps, item 2, and the class rule (item 7)."""
    def bad(self, text, reason): H3Logs.bad(self, text, reason)
    def test_windows_path_error(self):
        for p in ("C:/x/book/main.tex", "C:\\x\\book\\main.tex"):
            with self.subTest(path=p): self.bad(SYNTHETIC_LOG + p + ":12: Undefined control sequence.\n", "errors=1")
    def test_lua_error(self): self.bad(SYNTHETIC_LOG + "[\\directlua]:1: attempt to call a nil value\n", "errors=1")
    def test_second_run_killed(self): self.bad(SYNTHETIC_LOG + SYNTHETIC_LOG.split("Output")[0], "did not finish")
    def test_multiply_defined(self): self.bad(SYNTHETIC_LOG + "LaTeX Warning: There were multiply-defined labels.\n", "duplicate_labels=1")
    def test_empty_bibliography(self): self.bad(SYNTHETIC_LOG + "LaTeX Warning: Empty bibliography on input line 5.\n", "empty_bib=1")
    def test_other_class(self): self.bad(SYNTHETIC_LOG.replace("Class: behind-the-playlist", "Class: article"), "class behind-the-playlist not loaded")
    def test_biber_killed(self):
        for blg in (SYNTHETIC_BLG + "FATAL - x\n", SYNTHETIC_BLG.split("INFO - Output")[0]):
            with self.subTest(blg=blg[-12:]): self.log(SYNTHETIC_LOG, blg=blg); self.assertFails("typeset.biber", checks="typeset")


class RecheckCli(Case):
    """D5 gaps, item 3: no stale findings.json."""
    seed = lambda self: Cli.seed(self)
    def test_encrypted_pdf(self):
        p = self.dir / "enc.pdf"; d = pymupdf.open(PDF); d.save(p, encryption=pymupdf.PDF_ENCRYPT_AES_256, user_pw="a", owner_pw="b"); d.close()
        Cli.usage(self, "--pdf", p, "--no-log")
    def test_abbreviated_out(self):
        for o in ("--o", "--ou"):
            self.seed(); r = self.cli("--pdf", PDF, "--no-log", o, self.out)
            self.assertEqual(r.returncode, 2); self.assertFalse((self.out / "findings.json").exists())
    def test_broken_expectations(self):
        self.source("tools/qa/expectations.json", lambda t: "{"); self.seed(); r = self.cli("--pdf", PDF, "--no-log", "--out", self.out)
        self.assertNotEqual(r.returncode, 0); self.assertFalse((self.out / "findings.json").exists())
    def test_submission_edition_result_is_fresh(self):
        self.seed(); r = self.run_qa(checks="footer", log=False, extra=("--edition", "submission"))
        self.assertEqual(r.returncode, 0); self.assertTrue(self.found, "seeded empty result was kept")


class RecheckFooter(Case):
    """D5 gaps, item 7: the two dot rules."""
    def test_dot_covered_by_grey(self):
        dot = next(x["rect"] for x in pymupdf.open(PDF)[18].get_drawings() if x["rect"].y0 > 760 and x["rect"].width < 8 and x.get("fill") and x["fill"][0] > .9 and x["fill"][1] < .3)
        self.assertFails("footer.visible", self.rect(19, dot, (.8, .8, .8)), checks="footer"); self.assertFalse(self.fails("footer.numbers"))
    def test_dot_order(self): self.assertFails("footer.dot", self.pdf(lambda d: d.select([*range(11), 12, 11, *range(13, 20)])), checks="footer")


class Sources(Case):
    """D4 M4, M5, N14, N15, N16."""
    CH = "book/chapters/05-hasha.tex"
    def test_m4_n16_layout_commands(self):
        for c in ("\\vspace{2cm}", "\\resizebox{1cm}{!}{x}", "\\newpage", "\\begin{wrapfigure}{r}{2cm}x\\end{wrapfigure}", "\\hspace*{1cm}", "\\setlength{\\parskip}{0pt}",
                  "\\begin{figure}[H]\\end{figure}", "\\begin{figure}[ht!]\\end{figure}", "\\begin {minipage}{2cm}\\end{minipage}",
                  "\\includegraphics[width=3cm]{noa_week.pdf}", "\\begin{tikzpicture}\\end{tikzpicture}", "\\begin{minipage}{2cm}x\\end{minipage}"):
            with self.subTest(code=c):
                orig = (PROJ / self.CH).read_bytes(); (PROJ / self.CH).write_bytes(orig + b"\n" + c.encode() + b"\n")
                try: self.assertFails("infra.iron-law", checks="infra")
                finally: (PROJ / self.CH).write_bytes(orig)
    def test_m4_all_checks_run(self): self.append(self.CH, "\\vspace{2cm}"); self.assertFails("infra.iron-law")
    def test_n16_comment_is_not_layout(self):
        self.append(self.CH, "% \\begin{minipage}{2cm} \\vspace{1cm}"); self.assertEqual(self.run_qa(checks="infra").returncode, 0, str(self.found))
    def test_escaped_percent_is_not_a_comment(self): self.append(self.CH, "5\\% \\vspace{1cm}"); self.assertFails("infra.iron-law")
    def test_allowed_figure_is_allowed_once_only(self): self.append("book/chapters/02-kol-dilug.tex", "\\begin{figure}[t]\\end{figure}"); self.assertFails("infra.iron-law")
    def test_m5_code_environments(self):
        for c in ("\\begin{lstlisting}\nx\n\\end{lstlisting}", "\\begin{verbatim}\nx\n\\end{verbatim}", "\\begin{pythonbox}\nx\n\\end{pythonbox}", "\\begin{minted}{python}\nx\n\\end{minted}", "\\verb|x|"):
            with self.subTest(code=c.split("\n")[0]):
                orig = (PROJ / self.CH).read_bytes(); (PROJ / self.CH).write_bytes(orig + b"\n" + c.encode() + b"\n")
                try: self.assertFails("code.boxes", checks="code")
                finally: (PROJ / self.CH).write_bytes(orig)
    def test_m5_all_checks_run(self): self.append(self.CH, "\\begin{verbatim}\nx\n\\end{verbatim}"); self.assertFails("code.boxes")
    def test_m5_commented_code_is_na(self):
        self.append(self.CH, "% \\begin{lstlisting}"); self.assertEqual(self.run_qa(checks="code").returncode, 0); self.assertEqual(self.found[0]["status"], "n/a")
    def test_n14_chapters_deleted(self):
        for n in ("00-abstract", "02-kol-dilug", "08-play"): self.source(f"book/chapters/{n}.tex", lambda t: None)
        self.assertFails("infra.chapters")
    def test_n14_chapter_emptied(self): self.source(self.CH, lambda t: "% nothing\n"); self.assertFails("infra.chapters"); self.assertTrue(self.fails("typeset.text-complete"))
    def test_n14_bib_emptied(self): self.source("book/references.bib", lambda t: ""); self.assertFails("infra.bib"); self.assertTrue(self.fails("typeset.bib-titles"))
    def test_bib_entry_commented_out(self): self.source("book/references.bib", lambda t: t.replace("@article{goldberg", "%@article{goldberg", 1)); self.assertFails("infra.bib")
    def test_n14_class_body_removed(self):
        def cut(t): i = t.index("\\LoadClass"); return t[:i] + "\\endinput\n"
        self.source("book/behind-the-playlist.cls", cut); self.assertFails("infra.class-interface")
    def test_chapter_not_loaded_by_main(self): self.source("book/main.tex", lambda t: t.replace("\\InputIfFileExists{chapters/05", "%\\InputIfFileExists{chapters/05")); self.assertFails("infra.main")
    def test_class_changelog_differs(self): self.source("book/behind-the-playlist.cls", lambda t: t.replace("[2026/11/18 v1.1", "[2026/11/18 v1.2")); self.assertFails("cls.source")
    def test_n15_readme_emptied(self): self.source("README.md", lambda t: ""); self.assertFails("infra.readme")
    def test_n15_readme_links(self):
        for s in ('<img src="docs/nope.png">', "[t][ref]\n\n[ref]: docs/nope.md", "![x](docs/nope.png)", "[a](nope.md)", "[t][undefined-ref]"):
            with self.subTest(link=s):
                orig = (PROJ / "README.md").read_bytes(); (PROJ / "README.md").write_bytes(orig + b"\n\n" + s.encode() + b"\n")
                try: self.assertFails("infra.readme", checks="infra")
                finally: (PROJ / "README.md").write_bytes(orig)
    def test_n15_all_checks_run(self): self.append("README.md", '<img src="docs/nope.png">'); self.assertFails("infra.readme")


class Figures(Case):
    """D4 N4, N5, N17."""
    def test_n4_fig21_text_removed(self):
        self.assertFails("bidi.phrase.graph", self.wipe((7, (75, 80, 521, 276)))); self.assertEqual(len(self.fails("bidi.phrase.graph")), 6)
        self.assertTrue(self.fails("visual.region.fig-2.1"))
    def test_n5_captions_on_their_pages(self):
        r = self.run_qa(); w = {f.get("name"): f["where"] for f in self.found}
        self.assertEqual((r.returncode, w.get("img.caption-2.1"), w.get("img.caption-6.1")), (0, "Fig. 2.1 p.7", "Fig. 6.1 p.14"))
    def test_fig21_caption_removed(self): self.assertFails("img.caption-2.1", self.wipe((7, (70, 288, 525, 313))))
    def test_fig61_blocks_swapped_order(self):
        # wiping one label must not be satisfied by the same words in the list below the figure
        self.assertFails("bidi.phrase.diagram", self.wipe((14, (442, 440, 470, 468))), "block 1")
    def test_n17_margin_ink(self):
        for y0, y1, c in ((757, 779, BLACK), (10, 70, BLACK), (300, 330, (.85, .9, .9)), (300, 330, BLACK)):
            with self.subTest(y=y0, colour=c): self.assertFails("img.margins", self.rect(12, (20, y0, 50, y1), c))
    def test_dark_page_background(self):
        def edit(d):
            p = d[11]; p.draw_rect(p.rect, color=None, fill=(.3, .3, .3), overlay=False); p.clean_contents()
            p.draw_rect(pymupdf.Rect(0, 0, 60, 842), color=None, fill=(.3, .3, .3)); p.draw_rect(pymupdf.Rect(535, 0, 596, 842), color=None, fill=(.3, .3, .3))
        self.assertFails("img.margins", self.pdf(edit))


class Skills(unittest.TestCase):
    """D4 M2. Standard-library check of the one YAML rule that broke: a plain (unquoted) scalar must not hold ': ' or ' #'."""
    def test_m2_frontmatter_scalars(self):
        bad = []
        for f in sorted((ROOT / ".claude/skills").glob("*/SKILL.md")) + sorted((ROOT / ".claude/agents").glob("*.md")):
            lines = f.read_text(encoding="utf-8").splitlines()
            head = lines[1:lines.index("---", 1)] if lines[0] == "---" else []
            if not any(l.startswith("description:") for l in head): bad.append(f"{f.parent.name}: no description")
            for l in head:
                v = l.partition(":")[2].strip()
                if v[:1] == '"':
                    try: json.loads(v)
                    except ValueError: bad.append(f.parent.name)
                elif ": " in v or " #" in v: bad.append(f.parent.name)
        self.assertEqual(bad, [])
    def test_every_family_has_a_skill_and_a_declared_minimum(self):
        src = (ROOT / "tools/qa/qa_lib.py").read_text(encoding="utf-8")
        families = re.findall(r'"([a-z-]+)": lambda d, a:', src)
        self.assertIn("visual", families)
        exp = json.loads((ROOT / "tools/qa/expectations.json").read_text(encoding="utf-8"))
        self.assertEqual(sorted(exp.get("min_findings", {})), sorted(families))
        self.assertEqual([x for x in families if not (ROOT / f".claude/skills/qa-{x}/SKILL.md").is_file()], [])


if __name__ == "__main__":
    unittest.main()
