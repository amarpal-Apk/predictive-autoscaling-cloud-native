import csv
from collections import defaultdict
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = (
    ROOT / "experiments" / "datasets" / "processed"
    / "traffic-dataset.csv"
)

groups = defaultdict(list)

with DATA_FILE.open(newline="", encoding="utf-8") as file:
    for row in csv.DictReader(file):
        groups[row["experiment"]].append({
            "timestamp": row["timestamp_utc"],
            "rps": float(row["request_rate_rps"]),
        })

print("Naive traffic forecasting baseline")
print("Prediction: next sample RPS = current sample RPS")
print("=" * 65)

for workload, rows in sorted(groups.items()):
    # Sort and evaluate only within this workload.
    rows.sort(key=lambda row: row["timestamp"])

    actual = []
    predicted = []

    for current, following in zip(rows, rows[1:]):
        predicted.append(current["rps"])
        actual.append(following["rps"])

    errors = [
        abs(a - p) for a, p in zip(actual, predicted)
    ]

    mae = mean(errors)
    rmse = mean(
        (a - p) ** 2 for a, p in zip(actual, predicted)
    ) ** 0.5

    print(f"\nWorkload: {workload}")
    print(f"Forecast pairs: {len(actual)}")
    print(f"MAE:  {mae:.3f} RPS")
    print(f"RMSE: {rmse:.3f} RPS")

print("\nBaseline evaluation complete.")
