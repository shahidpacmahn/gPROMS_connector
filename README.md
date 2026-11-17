# gPROMS Python Connector Demo

A small, dependency-free example of connecting a Python analysis step to
simulation results exported from gPROMS. It validates a CSV export, calculates
a few process metrics, and emits a JSON report.

> **Scope:** This demo uses a synthetic CSTR dataset and a CSV export boundary.
> It does not launch gPROMS or use an official/live gPROMS API. The sample data
> is illustrative, not the output of a validated process model. For live
> coupling, connect `load_results` to the supported interface available in your
> licensed gPROMS installation.

## Run

Requires Python 3.10 or newer; there are no third-party dependencies.

```powershell
py -m gproms_connector data/cstr_results.csv
```

Write the report to a file:

```powershell
py -m gproms_connector data/cstr_results.csv --output cstr_report.json
```

Run the tests:

```powershell
py -m unittest discover -s tests -v
```

## CSV format

The loader expects one row per simulation time point with these columns:

| Column | Unit |
| --- | --- |
| `time_min` | min |
| `reactor_temperature_C` | °C |
| `reactant_A_mol_L` | mol/L |
| `product_B_mol_L` | mol/L |
| `cooling_duty_kW` | kW |

Time values must increase strictly, concentrations must be non-negative, and
the initial reactant concentration must be positive. The analyzer reports run
duration, conversion based on the initial and final reactant concentrations,
maximum temperature and cooling duty, and the final product concentration.

## Project layout

```text
gproms_connector/  CSV loader, validation, analysis, and CLI
data/              Synthetic CSTR results export
tests/             Standard-library unit tests
```

## Using real results

Export the relevant variables from a gPROMS run to CSV using the column names
above, then pass that file to the CLI. Keep credentials, licensed model files,
and proprietary simulation data out of a public showcase repository.
