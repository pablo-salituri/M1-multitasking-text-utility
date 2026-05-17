import csv
from pathlib import Path

METRICS_FILE = Path("metrics/metrics.csv")

FIELDNAMES = [
    "timestamp_utc",
    "model",
    "prompt_tokens",
    "completion_tokens",
    "total_tokens",
    "latency_ms",
    "estimated_cost_usd",
    "request_id",
    "provider_name"
]


def log_metrics(metrics_data: dict):
    file_exists = METRICS_FILE.exists()

    with open(METRICS_FILE, mode="a", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=FIELDNAMES
        )

        if not file_exists:
            writer.writeheader()

        # asegurar que no explote si faltan campos
        safe_row = {key: metrics_data.get(key, "") for key in FIELDNAMES}

        writer.writerow(safe_row)