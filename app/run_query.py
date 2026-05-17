import sys
import time
import threading
from uuid import uuid4
from datetime import datetime, timezone

from app.core.config import MODEL_PROVIDER, MODEL_NAME
from app.providers.provider_manager import ProviderManager


def loading_animation(stop_event):
    chars = "|/-\\"
    idx = 0

    while not stop_event.is_set():
        sys.stdout.write(f"\rProcessing {chars[idx % len(chars)]}")
        sys.stdout.flush()
        idx += 1
        time.sleep(0.1)

    sys.stdout.write("\r" + " " * 20 + "\r")


def main():
    print("\n=== Multitasking Text Utility CLI ===\n")
    print("Type your question below.")
    print("Type 'exit' to quit.\n")

    provider = ProviderManager(
        provider_name=MODEL_PROVIDER,
        model_name=MODEL_NAME
    )

    while True:
        question = input("User > ").strip()

        if question.lower() in ["exit", "quit"]:
            print("Bye 👋")
            sys.exit(0)

        if not question:
            print("Please enter a valid question.\n")
            continue

        stop_event = threading.Event()
        loader = threading.Thread(target=loading_animation, args=(stop_event,))
        loader.start()

        result = provider.query(question)

        stop_event.set()
        loader.join()

        response = result["llm_response"]
        metrics = result["metrics"]

        # LOG METRICS (shared with FastAPI)
        from app.services.metrics_service import log_metrics
        log_metrics(metrics)

        output = {
            "request_id": str(uuid4()),
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "provider_name": MODEL_PROVIDER,
            "model_used": MODEL_NAME,
            **response
        }

        print("\nResponse:\n")
        print(output)
        print("\n")


if __name__ == "__main__":
    main()