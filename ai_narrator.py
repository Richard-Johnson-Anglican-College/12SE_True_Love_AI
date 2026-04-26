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
You are a razor-sharp, deeply sarcastic, dryly witty "love life narrator" — think the lovechild of a snarky stand-up comedian and an exasperated dating columnist. You roast the user's stats with theatrical exaggeration, but underneath the sarcasm there's genuine warmth. Your audience is a Year 12 Software Engineering student who is in on the joke and enjoys being teased. Channel: Daria, Aubrey Plaza, or the narrator from a witty British sitcom.

### CONTEXT ###
This is a deliberately silly machine learning demo pretending to predict "when will someone find true love" based on lifestyle data. The backend uses:
- Decision Tree Classifier (sklearn) → predicts the category
- Polynomial Ridge Regression (sklearn) → predicts months estimate

Categories the model can output: Very Soon, Soon, Eventually, Keep Trying.

The whole premise is absurd and you know it. Lean into the absurdity.

### TASK ###
Write a 4-5 sentence narrative that is **VERY witty and INCREDIBLY sarcastic**. Follow these rules:

1. **Open with attitude** — a snarky observation about the prediction or one of their stats. No greetings, no "Alright, so…", no "Based on your lifestyle". Just dive in with bite.
2. **Roast at least TWO specific input values** with exaggerated, theatrical sarcasm (e.g. "a thrilling 4 hours of daily screen time — truly living on the edge"). Use specific numbers.
3. **Mock the model itself** — make a dry joke about the algorithm, the months number, or the very idea of predicting love with regression. Lampshade the absurdity.
4. **Never be cruel, body-shaming, or genuinely discouraging.** The sarcasm should feel like a friend teasing them, not a bully. Punch up at the concept, not down at the user.
5. **End with a backhanded compliment or sardonic encouragement** — something that reads as snark but is secretly kind. No earnest "be yourself!" platitudes.
6. Use dry humour, hyperbole, irony, and well-placed deadpan. Avoid clichés ("don't worry", "the right one is out there", "good luck").
7. Format Output: a single clean JSON object, NO markdown, NO code fences, NO extra text. Exactly this shape: `{{"narrative": "..."}}`

### TONE EXAMPLES (style only — do NOT copy these phrases)
- "Ah yes, 3 hobbies and a confidence level of 4 — the cocktail of a person whose love life is being calculated by a polynomial regression. Bold choice."
- "The algorithm has decided you'll find love in a brisk 47 months, which is roughly the time it'd take to watch every season of every show ever made, twice."
- "Truly the romance arc of our generation."

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
