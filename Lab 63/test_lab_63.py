"""Automated checks for Lab 63's synthetic data and exported charts."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np

from lab_63 import COLUMNS, EXPECTED_FILES, PRODUCTS, make_sales_data

SCRIPT = Path(__file__).with_name("lab_63.py")


class Lab63Tests(unittest.TestCase):
    def test_sample_data_is_reproducible(self):
        first = make_sales_data()
        second = make_sales_data()
        self.assertTrue(first.equals(second))
        self.assertEqual(first.shape, (12, 6))
        self.assertEqual(first["Month"].iloc[0], "Jan")
        self.assertEqual(int(first[PRODUCTS[0]].iloc[0]), 4174)
        self.assertFalse(first.isna().any().any())

    def test_correlation_matrix_properties(self):
        corr = make_sales_data()[COLUMNS].corr()
        self.assertEqual(corr.shape, (5, 5))
        self.assertTrue(np.allclose(corr, corr.T))
        self.assertTrue(np.allclose(np.diag(corr), 1.0))
        self.assertTrue((corr.abs() <= 1.00000001).all().all())

    def test_dpi_validation(self):
        process = subprocess.run(
            [sys.executable, str(SCRIPT), "--dpi", "10"],
            capture_output=True, text=True, timeout=30
        )
        self.assertNotEqual(process.returncode, 0)
        self.assertIn("--dpi must be", process.stderr)

    def test_end_to_end_exports(self):
        with tempfile.TemporaryDirectory() as temporary:
            process = subprocess.run(
                [sys.executable, str(SCRIPT),
                 "--output-dir", temporary, "--dpi", "72"],
                capture_output=True, text=True, timeout=180
            )
            self.assertEqual(process.returncode, 0,
                             msg=process.stdout + process.stderr)
            self.assertIn("SUCCESS: 18 output files verified",
                          process.stdout)
            found = {p.name for p in Path(temporary).iterdir()}
            self.assertEqual(found, set(EXPECTED_FILES))
            magic = {".png": b"\x89PNG", ".jpg": b"\xff\xd8",
                     ".pdf": b"%PDF"}
            for name in EXPECTED_FILES:
                path = Path(temporary) / name
                self.assertGreater(path.stat().st_size, 50)
                if path.suffix in magic:
                    self.assertTrue(
                        path.read_bytes().startswith(magic[path.suffix]),
                        msg=name
                    )


if __name__ == "__main__":
    unittest.main(verbosity=2)
