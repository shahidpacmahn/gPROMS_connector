"""Basic process metrics for a single simulation run."""

from .connector import SimulationPoint


def analyze_results(points: list[SimulationPoint]) -> dict[str, float | int]:
    """Summarize conversion and operating extremes from validated data."""
    if not points:
        raise ValueError("at least one simulation point is required")

    initial_reactant = points[0].reactant_A_mol_L
    if initial_reactant <= 0:
        raise ValueError("initial reactant_A_mol_L must be greater than zero")

    conversion = (
        (initial_reactant - points[-1].reactant_A_mol_L) / initial_reactant
    )
    return {
        "sample_count": len(points),
        "run_duration_min": points[-1].time_min - points[0].time_min,
        "conversion_fraction": conversion,
        "conversion_percent": conversion * 100,
        "maximum_temperature_C": max(point.reactor_temperature_C for point in points),
        "maximum_cooling_duty_kW": max(point.cooling_duty_kW for point in points),
        "final_product_B_mol_L": points[-1].product_B_mol_L,
    }
