import csv
from collections import defaultdict
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = (
    ROOT / "experiments" / "datasets" / "processed"
    / "traffic-dataset.csv"
)

WINDOW = 3
groups = defaultdict(list)

with DATA_FILE.open(newline="", encoding="utf-8") as file:
    for row in csv.DictReader(file):
        groups[row["experiment"]].append({
            "timestamp": row["timestamp_utc"],
            "rps": float(row["request_rate_rps"]),
        })

print(f"Moving-average baseline (window={WINDOW})")
print("=" * 60)

for workload, rows in sorted(groups.items()):
    rows.sort(key=lambda row: row["timestamp"])
    actual = []
    predicted = []

    for i in range(WINDOW, len(rows)):
        history = [row["rps"] for row in rows[i - WINDOW:i]]
        predicted.append(mean(history))
        actual.append(rows[i]["rps"])

    errors = [
        a - p for a, p in zip(actual, predicted)
    ]

    mae = mean(abs(error) for error in errors)
    rmse = mean(error ** 2 for error in errors) ** 0.5

    print(f"\nWorkload: {workload}")
    print(f"Forecast pairs: {len(actual)}")
    print(f"MAE:  {mae:.3f} RPS")
    print(f"RMSE: {rmse:.3f} RPS")

print("\nMoving-average evaluation complete.")
