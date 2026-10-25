import csv
from collections import defaultdict
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = (
    ROOT / "experiments" / "datasets" / "processed"
    / "traffic-dataset.csv"
)

metrics = [
    "request_rate_rps",
    "p95_latency_ms",
    "jvm_memory_mb",
]

groups = defaultdict(list)

with DATA_FILE.open(newline="", encoding="utf-8") as file:
    for row in csv.DictReader(file):
        for metric in metrics:
            row[metric] = float(row[metric])
        groups[row["experiment"]].append(row)

print("Traffic dataset analysis")
print("=" * 70)

for workload, rows in sorted(groups.items()):
    print(f"\nWorkload: {workload}")
    print(f"Samples: {len(rows)}")

    for metric in metrics:
        values = [row[metric] for row in rows]
        print(
            f"  {metric:20s}"
            f" mean={mean(values):10.3f}"
            f" min={min(values):10.3f}"
            f" max={max(values):10.3f}"
        )

print("\nAnalysis complete.")
