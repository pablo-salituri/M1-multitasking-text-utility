import sys
import time
import threading
import json
from uuid import uuid4
from datetime import datetime, timezone

from app.core.config import MODEL_PROVIDER, MODEL_NAME
from app.providers.openai_provider import OpenAIProvider
from app.services.metrics_service import log_metrics


def loading_animation(stop_event):
    chars = "|/-\\"
    idx = 0

    while not stop_event.is_set():
        sys.stdout.write(f"\rProcessing {chars[idx % len(chars)]}")
        sys.stdout.flush()
        idx += 1
        time.sleep(0.1)

    sys.stdout.write("\r" + " " * 30 + "\r")
    sys.stdout.flush()


def main():
    print("\n=== Multitasking Text Utility CLI ===\n")
    print("Type your question and press Enter.")
    print("Type 'exit' to quit.\n")

    provider = OpenAIProvider(model=MODEL_NAME)

    while True:
        question = input("User > ").strip()

        if question.lower() in ["exit", "quit"]:
            print("Bye 👋")
            sys.exit(0)

        if not question:
            print("Please enter a valid question.\n")
            continue

        # start loader
        stop_event = threading.Event()
        loader = threading.Thread(target=loading_animation, args=(stop_event,))
        loader.start()

        # query provider
        result = provider.query(question)

        # stop loader
        stop_event.set()
        loader.join()

        response = result["llm_response"]
        metrics = result["metrics"]

        # enrich metrics with CLI-level metadata
        metrics["request_id"] = str(uuid4())
        metrics["provider_name"] = MODEL_PROVIDER
        metrics["timestamp_utc"] = datetime.now(timezone.utc).isoformat()

        log_metrics(metrics)

        print("\nResponse:\n")
        print(json.dumps({
            "request_id": metrics["request_id"],
            "timestamp_utc": metrics["timestamp_utc"],
            "provider_name": MODEL_PROVIDER,
            "model_used": MODEL_NAME,
            **response
        }, indent=2, ensure_ascii=False))

        print("\n")


if __name__ == "__main__":
    main()