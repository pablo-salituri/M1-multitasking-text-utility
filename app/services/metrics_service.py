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
    "estimated_cost_usd"
]


def log_metrics(metrics_data: dict):
    file_exists = METRICS_FILE.exists()
    
    with open(METRICS_FILE, mode="a", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=FIELDNAMES)
        
        if not file_exists:
            writer.writeheader()
            
        writer.writerow(metrics_data)