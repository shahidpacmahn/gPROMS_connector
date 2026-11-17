"""Run the gPROMS CSV connector from the command line."""

import argparse
import json
from pathlib import Path

from .analysis import analyze_results
from .connector import load_results


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analyze a synthetic or exported gPROMS results CSV."
    )
    parser.add_argument("csv_file", type=Path, help="path to a simulation results CSV")
    parser.add_argument(
        "--output",
        type=Path,
        help="write the JSON report to this file (prints to stdout if omitted)",
    )
    args = parser.parse_args()

    try:
        points = load_results(args.csv_file)
        report = {
            "source_file": args.csv_file.name,
            "metrics": analyze_results(points),
        }
    except (OSError, ValueError) as error:
        parser.error(str(error))

    report_json = json.dumps(report, indent=2)
    if args.output:
        args.output.write_text(report_json + "\n", encoding="utf-8")
        print(f"Report written to {args.output}")
    else:
        print(report_json)


if __name__ == "__main__":
    main()
