# PI Report — Multitasking Text Utility

## Overview

This project implements a minimal AI-powered customer support triage assistant using FastAPI and OpenAI APIs.

The system receives a customer support question and returns a structured JSON response containing:

- category
- priority
- answer
- confidence
- recommended actions

Additionally, the application records operational metrics such as latency, token usage, and estimated execution cost.

The primary objective of the project was to build a reliable MVP demonstrating structured LLM integration, prompt engineering, observability, and basic validation mechanisms.

---

# Architecture

The application follows a modular architecture organized by responsibility.

## Main Components

### API Layer

`app/api/routes.py`

Handles HTTP requests through FastAPI endpoints.

Endpoints:

- `GET /health`
- `POST /query`

The `/query` endpoint:

1. receives the user question,
2. calls the OpenAI provider,
3. validates the response schema,
4. logs execution metrics,
5. returns a structured JSON response.

---

### Provider Layer

`app/providers/openai_provider.py`

Responsible for:

- loading prompts,
- calling OpenAI APIs,
- measuring latency,
- collecting token usage,
- estimating cost,
- parsing raw LLM output,
- handling provider failures.

This layer isolates provider-specific logic from the API layer, improving maintainability and future extensibility.

---

### Service Layer

Services are separated by responsibility:

- `prompt_service.py`
  - loads the main prompt template.

- `metrics_service.py`
  - persists execution metrics into CSV format.

- `response_parser.py`
  - validates and parses raw JSON responses from the model.

---

### Models

Pydantic models are used to define and validate contracts for:

- requests,
- API responses,
- LLM responses.

This ensures downstream systems always receive consistent JSON structures.

---

# Prompt Engineering Strategy

The project uses a combination of:

- instruction-based prompting,
- few-shot prompting,
- explicit schema guidance.

The prompt explicitly defines:

- behavioral rules,
- allowed categories,
- allowed priorities,
- JSON output format,
- multilingual constraints,
- fallback behavior for ambiguous questions.

Three few-shot examples were included to improve output consistency and reduce hallucinations.

Examples were intentionally selected to represent:

1. billing issues,
2. account management issues,
3. ambiguous technical support requests.

This approach improved:

- JSON formatting consistency,
- confidence calibration,
- multilingual response quality,
- clarification behavior for vague prompts.

---

# Structured Output Design

The application treats the LLM output as a strict contract.

Expected fields:

```json
{
  "category": "billing",
  "priority": "medium",
  "answer": "string",
  "confidence": 0.85,
  "actions": ["string"]
}
```

Validation is performed using Pydantic models.

If the model returns invalid JSON or an invalid schema, the system automatically generates a fallback response instead of failing silently.

This design improves reliability for downstream consumers.

---

# Metrics and Observability

Each execution stores operational metrics in:

```text
metrics/metrics.csv
```

Recorded metrics:

- timestamp_utc
- model
- prompt_tokens
- completion_tokens
- total_tokens
- latency_ms
- estimated_cost_usd

Example metric entry:

```csv
timestamp_utc,model,prompt_tokens,completion_tokens,total_tokens,latency_ms,estimated_cost_usd
2026-05-17T16:57:48.763118+00:00,gpt-4.1-mini,467,64,531,5637.3,0.000289
```

These metrics allow monitoring:

- API usage,
- cost,
- response speed,
- token consumption trends.

Estimated costs are currently calculated manually using approximate token pricing.

---

# Error Handling

The project includes multiple fallback mechanisms.

## Invalid JSON Handling

If the model generates invalid JSON:

- the response parser catches the exception,
- a safe fallback response is returned.

## Provider Failure Handling

If OpenAI becomes unavailable:

- the provider layer catches the exception,
- a structured fallback response is generated.

## Schema Validation

If a response does not match the expected schema:

- Pydantic validation raises an exception,
- the API returns a controlled fallback response.

This prevents malformed outputs from propagating to consumers.

---

# Automated Testing

The project includes automated tests using pytest.

Implemented tests:

- valid JSON parsing,
- invalid JSON fallback handling.

The tests verify that the parsing layer behaves correctly under both normal and failure conditions.

---

# Challenges and Tradeoffs

## Token Consumption

Prompt engineering improved reliability but increased prompt token usage.

The final prompt prioritizes output consistency over minimal token consumption.

---

## Structured Output Reliability

LLMs are probabilistic systems and may occasionally generate malformed outputs.

Additional validation and fallback layers were required to guarantee consistent JSON responses.

---

## Cost Estimation

The project uses manually estimated pricing instead of real-time provider billing APIs.

This simplifies implementation but reduces pricing precision.

---

# Possible Improvements

Future iterations could include:

- multi-provider support,
- moderation and safety layers,
- retry mechanisms,
- Dockerization,
- CI/CD integration,
- persistent database storage,
- stricter structured output enforcement,
- advanced observability dashboards,
- provider abstraction layer.

---

# Conclusion

The project successfully demonstrates a complete end-to-end LLM integration workflow including:

- API integration,
- prompt engineering,
- structured outputs,
- metrics collection,
- validation,
- automated testing,
- fallback handling.

The resulting MVP is modular, reproducible, and extensible, providing a solid foundation for future AI engineering projects.
