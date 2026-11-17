"""CSV boundary for simulation results exported from gPROMS."""

import csv
import math
from dataclasses import dataclass
from pathlib import Path


REQUIRED_COLUMNS = (
    "time_min",
    "reactor_temperature_C",
    "reactant_A_mol_L",
    "product_B_mol_L",
    "cooling_duty_kW",
)


@dataclass(frozen=True)
class SimulationPoint:
    time_min: float
    reactor_temperature_C: float
    reactant_A_mol_L: float
    product_B_mol_L: float
    cooling_duty_kW: float


def load_results(csv_path: str | Path) -> list[SimulationPoint]:
    """Load and validate a CSV exported from a simulation run."""
    path = Path(csv_path)
    points: list[SimulationPoint] = []

    with path.open("r", encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        columns = reader.fieldnames or []
        missing = [column for column in REQUIRED_COLUMNS if column not in columns]
        if missing:
            raise ValueError(f"{path}: missing required columns: {', '.join(missing)}")

        for line_number, row in enumerate(reader, start=2):
            try:
                values = {
                    column: float(row[column])
                    for column in REQUIRED_COLUMNS
                }
            except (TypeError, ValueError) as error:
                raise ValueError(
                    f"{path}: invalid or missing numeric value on line {line_number}"
                ) from error

            if not all(math.isfinite(value) for value in values.values()):
                raise ValueError(f"{path}: non-finite numeric value on line {line_number}")
            if values["reactant_A_mol_L"] < 0 or values["product_B_mol_L"] < 0:
                raise ValueError(f"{path}: concentrations cannot be negative on line {line_number}")
            if points and values["time_min"] <= points[-1].time_min:
                raise ValueError(
                    f"{path}: time_min must increase strictly (line {line_number})"
                )

            points.append(SimulationPoint(**values))

    if not points:
        raise ValueError(f"{path}: no simulation data rows found")
    if points[0].reactant_A_mol_L <= 0:
        raise ValueError(f"{path}: initial reactant_A_mol_L must be greater than zero")

    return points
