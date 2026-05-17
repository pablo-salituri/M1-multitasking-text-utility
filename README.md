# M1-multitasking-text-utility

A minimal AI-powered customer support triage assistant built with FastAPI and OpenAI.

The application receives a customer support question and returns a structured JSON response including:

- category
- priority
- answer
- confidence
- recommended actions

The system also logs execution metrics such as token usage, latency, and estimated cost.

---

# Features

- FastAPI REST API
- OpenAI integration
- Structured JSON responses
- Prompt engineering with few-shot examples
- JSON validation and fallback handling
- Metrics logging to CSV
- Automated tests with pytest
- Environment-based configuration

---

# Project Structure

```text
app/
├── api/
├── core/
├── models/
├── providers/
├── services/
└── main.py

metrics/
prompts/
reports/
tests/
```

---

# Requirements

- Python 3.11+
- OpenAI API key

---

# Installation

Clone the repository:

```bash
git clone <repository-url>
cd M1-multitasking-text-utility
```

Create virtual environment:

```bash
python -m venv .venv
```

Activate virtual environment.

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file based on `.env.example`.

Example:

```env
OPENAI_API_KEY=your_api_key_here

MODEL_PROVIDER=openai
MODEL_PROFILE=cheap

OPENAI_TEMPERATURE=0.2
MAX_COMPLETION_TOKENS=300
```

---

# Running the API

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

Swagger UI:

```text
http://localhost:8000/docs
```

Health check endpoint:

```text
GET /health
```

Query endpoint:

```text
POST /query
```

Example request:

```json
{
  "question": "I was charged twice"
}
```

Example response:

```json
{
  "request_id": "uuid",
  "timestamp_utc": "2026-05-17T15:32:17.159927+00:00",
  "provider_name": "openai",
  "model_used": "gpt-4.1-mini",
  "category": "billing",
  "priority": "high",
  "answer": "It appears you may have been charged twice.",
  "confidence": 0.9,
  "actions": [
    "Review your billing history",
    "Contact billing support if duplicate charges remain"
  ]
}
```

---

# Metrics Logging

Metrics are automatically stored in:

```text
metrics/metrics.csv
```

Logged fields:

- timestamp_utc
- model
- prompt_tokens
- completion_tokens
- total_tokens
- latency_ms
- estimated_cost_usd

Example:

```csv
timestamp_utc,model,prompt_tokens,completion_tokens,total_tokens,latency_ms,estimated_cost_usd
2026-05-17T15:41:20.512000+00:00,gpt-4.1-mini,467,65,532,4812.3,0.000291
```

---

# Running Tests

Run all tests:

```bash
pytest
```

Current tests validate:

- valid JSON parsing
- invalid JSON fallback handling

---

# Prompt Engineering

The project uses:

- instruction-based prompting
- few-shot prompting
- explicit JSON schema guidance

The prompt is stored in:

```text
prompts/main_prompt.md
```

---

# Known Limitations

- Estimated token pricing is manually approximated
- The application currently supports only OpenAI
- No database persistence
- No moderation/safety layer implemented yet
- LLM outputs are probabilistic and may vary slightly between executions

---

# Future Improvements

- Multi-provider support
- Safety and moderation layer
- Retry mechanisms
- Structured output enforcement
- Docker support
- CI/CD pipeline
- Advanced observability dashboards
