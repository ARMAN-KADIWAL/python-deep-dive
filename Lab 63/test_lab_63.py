import io
import subprocess
import sys
import tempfile
import tokenize
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

SCRIPT = Path(__file__).with_name("lab_63.py")
EXPECTED = {
    "product_a_sales.png", "all_products_sales.png", "annual_sales_bar.png",
    "marketing_spend_barh.png", "customized_line_chart.png",
    "customized_bar_chart.png", "histograms.png", "scatter_plots.png",
    "correlation_matrix.csv", "correlation_heatmaps.png",
    "correlation_strengths.png", "sales_dashboard.png", "sales_dashboard.jpg",
    "sales_dashboard.pdf", "monthly_sales_trends.png",
    "marketing_effectiveness.png", "sales_distributions.png",
}


class Lab63Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.directory = tempfile.TemporaryDirectory(prefix="lab63-check-")
        cls.folder = Path(cls.directory.name)
        cls.process = subprocess.run(
            [sys.executable, str(SCRIPT)],
            cwd=cls.folder,
            text=True,
            capture_output=True,
            timeout=180,
            check=False,
        )

    @classmethod
    def tearDownClass(cls):
        cls.directory.cleanup()

    def test_script_has_no_comment_tokens(self):
        source = SCRIPT.read_text(encoding="utf-8")
        tokens = tokenize.generate_tokens(io.StringIO(source).readline)
        comments = [token for token in tokens if token.type == tokenize.COMMENT]
        self.assertEqual(comments, [])

    def test_script_executes_successfully(self):
        self.assertEqual(
            self.process.returncode, 0,
            msg=self.process.stdout + self.process.stderr,
        )
        self.assertIn("LAB 63 TASK 6 COMPLETED!", self.process.stdout)

    def test_exact_expected_outputs(self):
        self.assertEqual({item.name for item in self.folder.iterdir()}, EXPECTED)
        self.assertEqual(len(EXPECTED), 17)

    def test_files_have_valid_signatures(self):
        signatures = {".png": b"\x89PNG\r\n\x1a\n", ".jpg": b"\xff\xd8",
                      ".pdf": b"%PDF-"}
        for name in EXPECTED:
            path = self.folder / name
            self.assertGreater(path.stat().st_size, 50, msg=name)
            if path.suffix in signatures:
                self.assertTrue(path.read_bytes().startswith(signatures[path.suffix]),
                                msg=name)

    def test_correlation_is_symmetric_and_expected(self):
        matrix = pd.read_csv(self.folder / "correlation_matrix.csv", index_col=0)
        self.assertEqual(matrix.shape, (5, 5))
        self.assertTrue(np.allclose(matrix, matrix.T))
        self.assertTrue(np.allclose(np.diag(matrix), 1.0))
        self.assertAlmostEqual(
            float(matrix.loc["Product_A_Sales", "Product_B_Sales"]),
            -0.713, delta=0.002,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
