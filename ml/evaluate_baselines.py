import csv
import math
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = (
    ROOT / "experiments" / "datasets" / "processed"
    / "traffic-dataset.csv"
)
OUTPUT_FILE = (
    ROOT / "experiments" / "datasets" / "processed"
    / "baseline-evaluation.csv"
)

WINDOW = 3
TRAIN_RATIO = 0.70


def mae(actual, predicted):
    return mean(abs(a - p) for a, p in zip(actual, predicted))


def rmse(actual, predicted):
    return math.sqrt(
        mean((a - p) ** 2 for a, p in zip(actual, predicted))
    )


groups = {}

with DATA_FILE.open(newline="", encoding="utf-8") as file:
    for row in csv.DictReader(file):
        groups.setdefault(row["experiment"], []).append({
            "timestamp": row["timestamp_utc"],
            "rps": float(row["request_rate_rps"]),
        })

results = []

for workload, rows in sorted(groups.items()):
    rows.sort(key=lambda row: row["timestamp"])

    split = int(len(rows) * TRAIN_RATIO)
    test_actual = []
    naive_predictions = []
    moving_predictions = []

    # Test only the final 30%. Use prior observations as history.
    for i in range(max(split, WINDOW), len(rows)):
        actual = rows[i]["rps"]
        history = [rows[j]["rps"] for j in range(i - WINDOW, i)]

        test_actual.append(actual)
        naive_predictions.append(history[-1])
        moving_predictions.append(mean(history))

    for model, predictions in [
        ("previous_sample", naive_predictions),
        ("moving_average_3", moving_predictions),
    ]:
        results.append({
            "experiment": workload,
            "model": model,
            "train_samples": split,
            "test_samples": len(test_actual),
            "mae_rps": round(mae(test_actual, predictions), 6),
            "rmse_rps": round(rmse(test_actual, predictions), 6),
        })

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=[
        "experiment",
        "model",
        "train_samples",
        "test_samples",
        "mae_rps",
        "rmse_rps",
    ])
    writer.writeheader()
    writer.writerows(results)

print("Chronological baseline evaluation")
print("=" * 70)

for row in results:
    print(
        f"{row['experiment']:10} | "
        f"{row['model']:18} | "
        f"test={row['test_samples']:2} | "
        f"MAE={row['mae_rps']:.3f} RPS | "
        f"RMSE={row['rmse_rps']:.3f} RPS"
    )

print(f"\nSaved results to: {OUTPUT_FILE}")
