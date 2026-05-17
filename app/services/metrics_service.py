import csv
from pathlib import Path

METRICS_FILE = Path("metrics/metrics.csv")


def log_metrics(metrics_data: dict):
    file_exists = METRICS_FILE.exists()
    
    with open(METRICS_FILE, mode="a", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=metrics_data.keys()
        )
        
        if not file_exists:
            writer.writeheader()
            
        writer.writerow(metrics_data)