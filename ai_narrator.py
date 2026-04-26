"""
AI Narrator Module — Gemini-powered playful explanations for ML predictions.

Uses the proven ROLE / CONTEXT / TASK / INPUT prompt pattern.
Gracefully degrades if config.py or API key is missing.
"""

import json
import google.generativeai as genai

# Try to load API key from config.py (gitignored)
_API_KEY_AVAILABLE = False
try:
    import config
    if hasattr(config, 'GEMINI_API_KEY') and config.GEMINI_API_KEY and config.GEMINI_API_KEY != "YOUR_GEMINI_API_KEY_HERE":
        genai.configure(api_key=config.GEMINI_API_KEY)
        _API_KEY_AVAILABLE = True
        print("[AI Narrator] Gemini API key loaded successfully.")
    else:
        print("[AI Narrator] WARNING: config.py exists but GEMINI_API_KEY is not set.")
except ImportError:
    print("[AI Narrator] WARNING: config.py not found. AI Narrator will be unavailable.")
except Exception as e:
    print(f"[AI Narrator] WARNING: Failed to configure Gemini: {e}")


MODEL_NAME = 'gemma-3n-e4b-it'

FRIENDLY_FAILURE_MESSAGE = "💭 The AI Narrator is sleeping right now. Try again in a moment! 😴"


def is_available() -> bool:
    """Check whether the AI Narrator is configured and ready to use."""
    return _API_KEY_AVAILABLE


def build_prompt(prediction_data: dict) -> str:
    """
    Build the structured prompt for Gemini.

    prediction_data must include:
        category, months, social_activity, confidence_level, hobbies_count,
        screen_time, goes_out_per_week, talks_to_new_people
    """
    return f"""### ROLE ###
You are a warm, playful, slightly witty "love life narrator" speaking to a Year 12 Software Engineering student. Your tone is encouraging, never creepy or patronizing, with light humor. You're commenting on a fun ML demo, NOT giving real life advice.

### CONTEXT ###
This is a playful machine learning demo predicting "when will someone find true love" based on lifestyle data. The backend uses:
- Decision Tree Classifier (sklearn) → predicts the category
- Polynomial Ridge Regression (sklearn) → predicts months estimate

Categories the model can output: Very Soon, Soon, Eventually, Keep Trying.

### TASK ###
1. Write a 4-5 sentence narrative explaining the prediction in plain English.
2. Reference at least TWO of the user's actual input values (specific numbers, not generic advice).
3. Briefly mention that this is a fun ML demo, not real-life advice.
4. End with light, kind encouragement.
5. Never be discouraging, mean, judgmental, or creepy.
6. Format Output: Provide your response as a single, clean JSON object.
   Do not include any text or markdown before or after the JSON.
   The JSON must have this exact key: `narrative`.

### INPUT ###
* Predicted category: {prediction_data['category']}
* Estimated months: {prediction_data['months']}
* Social Activity Level: {prediction_data['social_activity']}/10
* Confidence Level: {prediction_data['confidence_level']}/10
* Hobbies count: {prediction_data['hobbies_count']}
* Screen time: {prediction_data['screen_time']} hours/day
* Goes out per week: {prediction_data['goes_out_per_week']} times
* Talks to new people: {prediction_data['talks_to_new_people']}/10
"""


def generate_narrative(prediction_data: dict) -> dict:
    """
    Generate a playful AI narrative for the given prediction.

    Returns:
        {'success': True, 'narrative': '...'}  on success
        {'success': False, 'message': '...'}   on any failure
    """
    if not _API_KEY_AVAILABLE:
        return {
            'success': False,
            'message': FRIENDLY_FAILURE_MESSAGE
        }

    try:
        prompt = build_prompt(prediction_data)
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)

        # Strip any code fences the model might add
        text = response.text.strip()
        if text.startswith('```'):
            # Remove leading fence (```json or just ```)
            text = text.split('\n', 1)[1] if '\n' in text else text
        if text.endswith('```'):
            text = text.rsplit('```', 1)[0]
        text = text.strip()

        # Parse JSON
        data = json.loads(text)

        narrative = data.get('narrative', '').strip()
        if not narrative:
            return {
                'success': False,
                'message': FRIENDLY_FAILURE_MESSAGE
            }

        return {
            'success': True,
            'narrative': narrative
        }

    except json.JSONDecodeError as e:
        print(f"[AI Narrator] JSON parse error: {e}")
        # Last-ditch attempt: use the raw text if it looks reasonable
        try:
            raw = response.text.strip()
            if 30 < len(raw) < 800:
                return {'success': True, 'narrative': raw}
        except Exception:
            pass
        return {
            'success': False,
            'message': FRIENDLY_FAILURE_MESSAGE
        }
    except Exception as e:
        print(f"[AI Narrator] Generation error: {e}")
        return {
            'success': False,
            'message': FRIENDLY_FAILURE_MESSAGE
        }
