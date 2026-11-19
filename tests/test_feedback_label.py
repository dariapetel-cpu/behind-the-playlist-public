"""D3-01 regression tests against the public PDF. Run: python tests/test_feedback_label.py"""
from pathlib import Path
import sys
import unittest

import pymupdf

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools/qa"))
import qa_lib

LABEL = "לולאת משוב"


class FeedbackLabelTest(unittest.TestCase):
    def setUp(self):
        self.doc = pymupdf.open(ROOT / "pdf/behind-the-playlist.pdf")
        self.addCleanup(self.doc.close)
        qa_lib.findings.clear()
        self.addCleanup(qa_lib.findings.clear)

    def check_result(self):
        qa_lib.check_bidi(self.doc)
        return next(f for f in qa_lib.findings if LABEL in f["evidence"])

    def test_approved_plot_passes_at_page_14(self):
        result = self.check_result()
        self.assertEqual(result["status"], "pass", result)
        self.assertIn("[14]", result["where"])

    def test_missing_rotated_label_fails_despite_page_15_prose(self):
        figure = self.doc[13]
        line, = [line for line, _ in qa_lib.page_lines(figure) if line["dir"][1] < -0.99]
        figure.add_redact_annot(line["bbox"])
        figure.apply_redactions(images=0, graphics=0)
        self.assertIn(qa_lib.norm(LABEL), qa_lib.norm(qa_lib.page_text_rtl(self.doc[14])))
        result = self.check_result()
        self.assertEqual(result["status"], "fail", result)
        self.assertIn("[14]", result["where"])


if __name__ == "__main__":
    unittest.main()
