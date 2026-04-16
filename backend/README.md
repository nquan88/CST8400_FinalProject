# Backend

LLM integration
- Set `HF_API_KEY` in your environment or in a `.env` file to enable Hugging Face Inference API usage.
- Optionally set `HF_MODEL` (default: `google/flan-t5-small`).

Google Generative API
- Set `GOOGLE_API_KEY` (or `GOOGLE_KEY`) and optionally `GOOGLE_MODEL` (default: `models/text-bison-001`) to use Google Generative API instead of Hugging Face.

Example `.env` entries for Google:

```
GOOGLE_API_KEY=AIza...
GOOGLE_MODEL=models/text-bison-001
```

`.env.example` (copy to `.env` and fill in your keys):

```
# Choose either Google or Hugging Face API keys (Google preferred).
GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY_HERE
GOOGLE_MODEL=models/text-bison-001

# Or, for Hugging Face fallback:
HF_API_KEY=hf_XXXXXXXXXXXXXXXXXXXX
HF_MODEL=google/flan-t5-small
```

Example `.env` entries:

```
HF_API_KEY=hf_XXXXXXXXXXXX
HF_MODEL=google/flan-t5-small
```

Behavior
- When `HF_API_KEY` is present, the backend will attempt to call the HF Inference API to generate insights from analytics.
- If the LLM call fails or `HF_API_KEY` is missing, the system falls back to deterministic, rule-based insights.
 - If `GOOGLE_API_KEY` is present the backend will call Google's Generative API (`GOOGLE_MODEL`), otherwise it will use Hugging Face if `HF_API_KEY` is present. If neither key is present the backend will fall back to deterministic, rule-based insights.

Run tests

Use the venv Python to run the unit tests:

```powershell
\.\venv\Scripts\python -m unittest discover -v
```
