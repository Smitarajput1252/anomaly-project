import google.generativeai as genai
import json
from config import GEMINI_API_KEY

# Some API keys or versions may not support the 'gemini-pro' alias,
# causing NotFound errors; use a more stable model name and provide a
# fallback classification when the model is unreachable.

from google.api_core.exceptions import NotFound

genai.configure(api_key=GEMINI_API_KEY)

# switch to a generally available model for the v1beta API
# (run ListModels if you're unsure what names your key supports)
model = genai.GenerativeModel("gemini-1")

def analyze_vitals(vitals):
    prompt = f"""
    Analyze patient vitals:

    Heart Rate: {vitals['heart_rate']}
    SpO2: {vitals['spo2']}
    Temperature: {vitals['temperature']}
    Blood Pressure: {vitals['bp_systolic']}

    Classify severity strictly as LOW, MEDIUM, or HIGH.
    Provide short medical reasoning.

    Return JSON:
    {{
        "severity": "...",
        "reason": "..."
    }}
    """

    try:
        response = model.generate_content(prompt)
        cleaned = response.text.strip("```json").strip("```")
        return json.loads(cleaned)
    except NotFound:
        # model name not available for this API version
        print("model not found, using rule-based fallback")
    except Exception as err:
        # generic fallback in case of parse errors or other API issues
        print(f"vitals analysis failed: {err}")

    # simple heuristic fallback when the API call fails
    hr = vitals.get("heart_rate", 0)
    spo2 = vitals.get("spo2", 0)
    if hr > 120 or spo2 < 90:
        severity = "HIGH"
        reason = "rules: extreme vitals"
    elif hr > 100 or spo2 < 94:
        severity = "MEDIUM"
        reason = "rules: elevated vitals"
    else:
        severity = "LOW"
        reason = "rules: normal vitals"
    return {"severity": severity, "reason": reason}