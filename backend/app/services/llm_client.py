import os
import json
import requests


def generate_insights_via_gemini(metrics, timeout=30):
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise RuntimeError('GEMINI_API_KEY not set')

    model = os.getenv('GEMINI_MODEL', 'gemini-2.5-flash')
    url = (
        f'https://generativelanguage.googleapis.com/v1beta/models/'
        f'{model}:generateContent?key={api_key}'
    )

    prompt = (
        "You are an assistant that converts reading analytics into a JSON array of insight cards.\n"
        "Return ONLY a valid JSON array — no markdown, no explanation, just the raw JSON.\n"
        "Each item must be an object with exactly these keys:\n"
        "  type   (one of: success, info, warning, tip)\n"
        "  icon   (one of: fire, trophy, bolt, bullseye, clock, lightbulb, chart-line,\n"
        "          exclamation-triangle, sun, cloud-sun, moon, star, layer-group, compass,\n"
        "          calendar-alt, book)\n"
        "  title  (short heading, max 8 words)\n"
        "  message (one or two sentences of actionable advice)\n\n"
        "Reading analytics:\n" + json.dumps(metrics, default=str)
    )

    payload = {
        'contents': [{'parts': [{'text': prompt}]}],
        'generationConfig': {
            'temperature': 0.4,
            'maxOutputTokens': 1024,
        },
    }

    resp = requests.post(url, json=payload, timeout=timeout)
    resp.raise_for_status()

    body = resp.json()
    text = body['candidates'][0]['content']['parts'][0]['text'].strip()

    if text.startswith('```'):
        text = text.split('\n', 1)[-1]
        text = text.rsplit('```', 1)[0]

    start = text.find('[')
    if start == -1:
        raise ValueError('Model did not return a JSON array')

    return json.loads(text[start:])
