import csv
import tempfile
import unittest
from pathlib import Path

from gproms_connector import analyze_results, load_results


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SAMPLE_CSV = PROJECT_ROOT / "data" / "cstr_results.csv"


class LoadResultsTests(unittest.TestCase):
    def test_loads_sample_export(self) -> None:
        points = load_results(SAMPLE_CSV)

        self.assertEqual(len(points), 8)
        self.assertEqual(points[0].time_min, 0)
        self.assertEqual(points[-1].reactant_A_mol_L, 0.4)

    def test_rejects_non_increasing_time(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            csv_path = Path(temporary_directory) / "invalid.csv"
            with csv_path.open("w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(
                    [
                        "time_min",
                        "reactor_temperature_C",
                        "reactant_A_mol_L",
                        "product_B_mol_L",
                        "cooling_duty_kW",
                    ]
                )
                writer.writerow([0, 80, 2, 0, 0.8])
                writer.writerow([0, 81, 1, 0.5, 1])

            with self.assertRaisesRegex(ValueError, "increase strictly"):
                load_results(csv_path)


class AnalysisTests(unittest.TestCase):
    def test_calculates_conversion_and_run_duration(self) -> None:
        metrics = analyze_results(load_results(SAMPLE_CSV))

        self.assertEqual(metrics["sample_count"], 8)
        self.assertEqual(metrics["run_duration_min"], 14)
        self.assertAlmostEqual(metrics["conversion_fraction"], 0.8)
        self.assertAlmostEqual(metrics["conversion_percent"], 80.0)
        self.assertEqual(metrics["maximum_temperature_C"], 86.2)

    def test_rejects_empty_results(self) -> None:
        with self.assertRaisesRegex(ValueError, "at least one"):
            analyze_results([])


if __name__ == "__main__":
    unittest.main()
