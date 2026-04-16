import os
import json
import requests

def generate_insights_via_hf(metrics, timeout=30):
    """Call Hugging Face Inference API to turn analytics into a JSON list of insights.

    Returns a Python list of insight dicts on success. Raises on failure.
    """
    HF_API = os.getenv('HF_API_KEY')
    HF_MODEL = os.getenv('HF_MODEL', 'google/gemini-2.0-flash')  # default to a strong open model if not set

    if not HF_API:
        raise RuntimeError('HF_API_KEY not set')
    prompt = (
        "You are an assistant that converts reading analytics into a JSON array.\n"
        "Each item must be an object with: type, icon, title, message.\n"
        "Return only valid JSON (a single array).\n\n"
        "Input metrics (JSON):\n" + json.dumps(metrics, default=str)
    )

    headers = {'Authorization': f'Bearer {HF_API}'}
    payload = {'inputs': prompt, 'options': {'wait_for_model': True}}
    url = f'https://api-inference.huggingface.co/models/{HF_MODEL}'

    resp = requests.post(url, headers=headers, json=payload, timeout=timeout)
    resp.raise_for_status()

    # Best-effort: many HF endpoints return a JSON list with 'generated_text'
    try:
        body = resp.json()
        if isinstance(body, list) and body and isinstance(body[0], dict) and 'generated_text' in body[0]:
            text = body[0]['generated_text']
        elif isinstance(body, str):
            text = body
        else:
            # fallback to raw text
            text = resp.text
    except ValueError:
        text = resp.text

    # Extract JSON array from model output
    start = text.find('[')
    if start == -1:
        raise ValueError('Model did not return a JSON array')
    json_text = text[start:]
    return json.loads(json_text)
