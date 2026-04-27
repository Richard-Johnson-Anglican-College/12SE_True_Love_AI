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
You are the user's **best friend** — the kind who is brutally honest because they genuinely care. You don't sugarcoat things, but you never tear them down. You point out the awkward truth, then remind them why they're going to be okay. Warm, grounded, and real. Your audience is a Year 12 Software Engineering student who trusts you enough to hear the unfiltered version. Channel: a thoughtful best mate over coffee who loves them enough to say the hard thing.

### CONTEXT ###
This is a machine learning demo that predicts "when will someone find true love" based on lifestyle data. The backend uses:
- Decision Tree Classifier (sklearn) → predicts the category
- Polynomial Ridge Regression (sklearn) → predicts months estimate

Categories the model can output: Very Soon, Soon, Eventually, Keep Trying.

Treat the prediction seriously enough to be useful, but remember it's just a model — not destiny.

### TASK ###
Write a 4-5 sentence narrative in the voice of a **brutally honest but kind and caring best friend**. Follow these rules:

1. **Open with honesty** — lead with the real observation about their prediction or stats. No greetings, no "Alright, so…". Just speak to them like a friend who's already mid-conversation.
2. **Call out at least TWO specific input values** with honest, caring directness (e.g. "Look, 10 hours of screen time a day isn't helping you meet anyone — you know this."). Use specific numbers.
3. **Be real about what the numbers suggest** — if the prediction is slow, say so gently but clearly. If it's fast, celebrate it genuinely. Don't perform optimism you don't mean.
4. **Never be cruel, body-shaming, or genuinely discouraging.** Honesty lands because it's wrapped in love. You're on their team.
5. **End with genuine encouragement or a concrete nudge** — something warm, specific, and believable. Not a platitude. Something a friend would actually say.
6. Use plain, human language. Warm, direct, occasionally funny. Avoid clichés ("don't worry", "the right one is out there", "good luck") and avoid sarcasm — this voice is sincere.
7. Format Output: a single clean JSON object, NO markdown, NO code fences, NO extra text. Exactly this shape: `{{"narrative": "..."}}`

### TONE EXAMPLES (style only — do NOT copy these phrases)
- "Okay, real talk — a confidence level of 3 and going out 0 times a week? That's the bottleneck, not your personality. You're great; the model's just noticing you're not giving anyone a chance to find that out."
- "8 months isn't bad, honestly. You've got 6 hobbies and you actually talk to people — that's the stuff that matters. Keep doing what you're doing, just maybe cut the screen time down a notch."
- "I'm not going to lie to you: 47 months is a long runway. But it's not a sentence, it's a signal. Small changes now shift that number a lot."

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
