import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "experiments" / "datasets"
OUTPUT_DIR = DATA_DIR / "processed"
OUTPUT_FILE = OUTPUT_DIR / "traffic-dataset.csv"

INPUT_FILES = [
    "constant-traffic.csv",
    "ramp-up-traffic.csv",
    "spike-traffic.csv",
    "periodic-traffic.csv",
]

REQUIRED_COLUMNS = [
    "timestamp_utc",
    "experiment",
    "request_rate_rps",
    "p95_latency_ms",
    "jvm_memory_mb",
    "total_requests",
]


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    combined_rows = []

    for filename in INPUT_FILES:
        path = DATA_DIR / filename

        if not path.exists():
            raise FileNotFoundError(f"Dataset not found: {path}")

        with path.open("r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            if reader.fieldnames is None:
                raise ValueError(f"Missing CSV header: {filename}")

            missing_columns = set(REQUIRED_COLUMNS) - set(reader.fieldnames)
            if missing_columns:
                raise ValueError(
                    f"{filename} is missing columns: {sorted(missing_columns)}"
                )

            for line_number, row in enumerate(reader, start=2):
                for column in REQUIRED_COLUMNS:
                    if row.get(column) is None or not row[column].strip():
                        raise ValueError(
                            f"Missing {column} in {filename}, line {line_number}"
                        )

                # Validate numeric features before including the row.
                for column in (
                    "request_rate_rps",
                    "p95_latency_ms",
                    "jvm_memory_mb",
                    "total_requests",
                ):
                    try:
                        value = float(row[column])
                    except ValueError as error:
                        raise ValueError(
                            f"Invalid {column} in {filename}, line {line_number}"
                        ) from error

                    if value < 0:
                        raise ValueError(
                            f"Negative {column} in {filename}, line {line_number}"
                        )

                combined_rows.append(
                    {column: row[column] for column in REQUIRED_COLUMNS}
                )

    # Keep chronological order within the combined dataset.
    combined_rows.sort(key=lambda row: row["timestamp_utc"])

    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=REQUIRED_COLUMNS)
        writer.writeheader()
        writer.writerows(combined_rows)

    print(f"Dataset created: {OUTPUT_FILE}")
    print(f"Input datasets: {len(INPUT_FILES)}")
    print(f"Total rows: {len(combined_rows)}")
    print("Missing values: 0 (validated)")
    print("Numeric features: validated")


if __name__ == "__main__":
    main()
