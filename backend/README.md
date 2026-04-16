# Backend

LLM integration
- Set `HF_API_KEY` in your environment or in a `.env` file to enable Hugging Face Inference API usage.
- Optionally set `HF_MODEL` (default: `google/flan-t5-small`).

Example `.env` entries:

```
HF_API_KEY=hf_XXXXXXXXXXXX
HF_MODEL=google/flan-t5-small
```

Behavior
- When `HF_API_KEY` is present, the backend will attempt to call the HF Inference API to generate insights from analytics.
- If the LLM call fails or `HF_API_KEY` is missing, the system falls back to deterministic, rule-based insights.

Run tests

Use the venv Python to run the unit tests:

```powershell
\.\venv\Scripts\python -m unittest discover -v
```
