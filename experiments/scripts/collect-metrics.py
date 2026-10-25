import csv
import json
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

PROMETHEUS_URL = "http://host.docker.internal:9090"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "datasets"

QUERIES = {
    "request_rate_rps": """
        sum(rate(http_server_requests_seconds_count{job="order-service"}[1m]))
    """,
    "p95_latency_ms": """
        1000 * histogram_quantile(
            0.95,
            sum by (le) (
                rate(http_server_requests_seconds_bucket{job="order-service"}[1m])
            )
        )
    """,
    "jvm_memory_mb": """
        sum(jvm_memory_used_bytes{job="order-service"}) / 1024 / 1024
    """,
    "total_requests": """
        sum(http_server_requests_seconds_count{job="order-service"})
    """,
    "process_cpu_usage": """
        process_cpu_usage{job="order-service"}
    """,
    "system_cpu_usage": """
        system_cpu_usage{job="order-service"}
    """,
}


def query_prometheus(query):
    params = urllib.parse.urlencode({"query": query})
    url = f"{PROMETHEUS_URL}/api/v1/query?{params}"

    with urllib.request.urlopen(url, timeout=10) as response:
        payload = json.loads(response.read().decode("utf-8"))

    if payload.get("status") != "success":
        raise RuntimeError(f"Prometheus query failed: {payload}")

    results = payload["data"]["result"]
    if not results:
        return None

    return float(results[0]["value"][1])


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    experiment = input(
        "Experiment label (constant/ramp-up/spike/periodic): "
    ).strip().lower()

    if experiment not in {"constant", "ramp-up", "spike", "periodic"}:
        raise ValueError("Use constant, ramp-up, spike, or periodic.")

    duration = int(input("Collection duration in seconds (e.g. 180): "))
    interval = 5

    if duration <= 0:
        raise ValueError("Duration must be greater than zero.")

    output_file = OUTPUT_DIR / f"{experiment}-traffic.csv"
    fields = ["timestamp_utc", "experiment", *QUERIES.keys()]

    print(f"Collecting metrics every {interval}s for {duration}s.")
    print(f"Output: {output_file}")
    print("Start the matching k6 test in another terminal now.")

    start = time.monotonic()
    next_sample = start

    with output_file.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()

        while time.monotonic() - start < duration:
            row = {
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "experiment": experiment,
            }

            for name, query in QUERIES.items():
                try:
                    row[name] = query_prometheus(query)
                except Exception as error:
                    print(f"Warning: {name}: {error}")
                    row[name] = None

            writer.writerow(row)
            file.flush()

            print(row)
            next_sample += interval
            time.sleep(max(0, next_sample - time.monotonic()))

    print(f"\nCollection finished. Saved {output_file}")


if __name__ == "__main__":
    main()
