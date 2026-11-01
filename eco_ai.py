
import csv
import time
from datetime import datetime
from pathlib import Path

import requests

# ---------------- ECO-AI SETTINGS ----------------

OLLAMA_URL = "http://localhost:11434/api/generate"

SMALL_MODEL = "llama3.2:1b"
LARGE_MODEL = "llama3.2:3b"

# Keep the model loaded for reuse between questions.
KEEP_ALIVE = "10m"

# Limit response length to help keep demonstrations manageable.
MAX_RESPONSE_TOKENS = 120

# Maximum wait for one response, in seconds.
REQUEST_TIMEOUT = 300

LOG_FILE = Path(__file__).with_name("eco_ai_results.csv")


# ---------------- MODEL ROUTING ----------------

def choose_model(question):
    """Choose a model using a simple, explainable rule."""

    word_count = len(question.split())

    detailed_keywords = [
        "explain", "compare", "analyze", "analyse",
        "evaluate", "detailed", "in detail",
        "calculate", "difference between"
    ]

    needs_detail = any(
        keyword in question.lower()
        for keyword in detailed_keywords
    )

    if word_count > 25 or needs_detail:
        return LARGE_MODEL, "FULL"

    return SMALL_MODEL, "ECO"


# ---------------- AI RESPONSE ----------------

def ask_ollama(question, model):
    """Ask Ollama to generate an answer."""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": model,
            "prompt": question,
            "stream": False,
            "keep_alive": KEEP_ALIVE,
            "options": {
                "num_predict": MAX_RESPONSE_TOKENS
            }
        },
        timeout=REQUEST_TIMEOUT
    )

    response.raise_for_status()
    result = response.json()

    answer = result.get("response", "").strip()

    # Ollama may provide these timing measurements in nanoseconds.
    total_duration = result.get("total_duration")
    eval_count = result.get("eval_count")

    return answer, total_duration, eval_count


# ---------------- SAVE TEST RESULTS ----------------

def save_result(question, model, mode, elapsed, status,
                ollama_duration=None, tokens=None):
    """Append one test result to a CSV file."""

    file_exists = LOG_FILE.exists()

    with LOG_FILE.open(
        "a", newline="", encoding="utf-8"
    ) as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "timestamp",
                "question",
                "mode",
                "model",
                "response_time_seconds",
                "ollama_total_seconds",
                "output_tokens",
                "status",
                "power_watts",
                "temperature_celsius"
            ])

        writer.writerow([
            datetime.now().isoformat(timespec="seconds"),
            question,
            mode,
            model,
            round(elapsed, 2),
            (
                round(ollama_duration / 1_000_000_000, 2)
                if ollama_duration is not None else ""
            ),
            tokens if tokens is not None else "",
            status,
            "NOT MEASURED",
            "NOT MEASURED"
        ])


# ---------------- SOFTWARE DASHBOARD ----------------

def show_dashboard(mode, model, elapsed=None, status="Ready"):
    """Display the latest ECO-AI status."""

    print("\n" + "=" * 44)
    print("             ECO-AI DASHBOARD")
    print("=" * 44)
    print(f"Status:              {status}")
    print(f"Selected mode:       {mode}")
    print(f"Selected model:      {model}")

    if elapsed is None:
        print("Response time:       Waiting for result")
    else:
        print(f"Response time:       {elapsed:.2f} seconds")

    print("Power consumption:   Not measured")
    print("CPU temperature:     Not measured")
    print("=" * 44 + "\n")


# ---------------- MAIN PROGRAM ----------------

def main():
    print("\nWelcome to ECO-AI")
    print("Automatic AI model selection prototype")
    print("Type 'exit' to quit.\n")

    # Check whether Ollama is reachable.
    try:
        check = requests.get(
            "http://localhost:11434/api/tags",
            timeout=5
        )
        check.raise_for_status()

    except requests.exceptions.RequestException:
        print("Cannot connect to Ollama.")
        print("Please make sure Ollama is running.")
        return

    while True:
        try:
            question = input("Your question: ").strip()

        except (KeyboardInterrupt, EOFError):
            print("\nECO-AI closed.")
            break

        if question.lower() == "exit":
            print("Thank you for testing ECO-AI!")
            break

        if not question:
            print("Please enter a question.\n")
            continue

        model, mode = choose_model(question)

        show_dashboard(
            mode, model, status="Generating answer..."
        )

        print("Please wait while the selected model responds.\n")

        start_time = time.perf_counter()

        try:
            answer, ollama_duration, tokens = ask_ollama(
                question, model
            )

            elapsed = time.perf_counter() - start_time

            show_dashboard(
                mode, model, elapsed, status="Completed"
            )

            print("ECO-AI ANSWER")
            print("-" * 44)
            print(answer if answer else "(No answer returned)")
            print("-" * 44)

            save_result(
                question, model, mode, elapsed, "success",
                ollama_duration, tokens
            )

            print(f"\nResults saved to: {LOG_FILE.name}\n")

        except requests.exceptions.Timeout:
            elapsed = time.perf_counter() - start_time

            show_dashboard(
                mode, model, elapsed, status="Timed out"
            )

            print("This answer took too long.")
            print("Try a shorter question or a smaller model.\n")

            save_result(
                question, model, mode, elapsed, "timeout"
            )

        except requests.exceptions.ConnectionError:
            elapsed = time.perf_counter() - start_time

            print("Connection to Ollama was lost.")
            save_result(
                question, model, mode, elapsed,
                "connection_error"
            )

        except requests.exceptions.RequestException as error:
            elapsed = time.perf_counter() - start_time

            print(f"Request failed: {error}")
            save_result(
                question, model, mode, elapsed,
                "request_error"
            )


if __name__ == "__main__":
    main()
