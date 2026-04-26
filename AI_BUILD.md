# 🛠️ AI Narrator Build Plan — Hybrid System / Stage 3 Chaining

This document captures the design and implementation plan for **chaining** a Gemma neural network (Stage 3) onto the existing classical ML pipeline (Stages 1 + 2) — turning the True Love AI app into a true **hybrid system**.

---

## 🎯 Goal

After a user receives a classical ML prediction (Decision Tree + Polynomial Ridge), allow them to **click a sparkle icon** to invoke the **Stage 3 neural network** (Gemma LLM). The neural network is **chained** to the upstream classical ML output — it receives the category + months + features and produces a 4-5 sentence narrative.

### Hybrid Architecture

```
  Stage 1                Stage 2                Stage 3
  Classical ML           Classical ML           Neural Network
  Decision Tree    →     Polynomial Ridge →     Gemma LLM
  (sklearn)              (sklearn)              (transformer)
  → category             → months               → narrative
```

This is the **chaining handoff**: classical ML's structured numbers feed the neural network's natural-language reasoning. Two different model families, working as one hybrid system.

**Why on-demand (not auto):**
- Saves Gemini API quota (free tier: 15 req/min, 1500/day)
- Instant ML prediction display preserved
- Creates curiosity/engagement
- Reinforces ML vs GenAI distinction (separate user actions)
- Failure-safe (only fails if user opts in)

---

## 📐 Design Decisions

| Decision | Choice |
|----------|--------|
| **Trigger** | Floating sparkle icon (top-right of prediction card) |
| **Gemini Model** | `gemma-3n-e4b-it` (proven in RJ_BLP_1) |
| **Length** | 4-5 sentences (medium) |
| **Loading** | On-demand AJAX after click |
| **Failure mode** | Show friendly "AI Narrator is sleeping" message |
| **API Key** | `config.py` (gitignored), manually placed on PythonAnywhere |
| **Tone** | Warm, playful, lightly witty — never creepy or discouraging |

---

## 🎨 UX Flow

### **State 1: Initial prediction display**

```
┌──────────────────────────────────┐
│ ✨ Soon ✨                    ✨ │  ← sparkle icon (top-right, clickable)
│ Estimated: 4.2 months            │
│                                  │
│ Why This Prediction?             │
│   [existing reasons list]        │
└──────────────────────────────────┘
```

### **State 2: After clicking sparkle (loading)**

```
┌──────────────────────────────────┐
│ ✨ Soon ✨                    ⏳ │  ← icon shows spinning state
│ ...                              │
│                                  │
│ ┌──────────────────────────────┐ │
│ │ 💭 AI Narrator is thinking…  │ │
│ └──────────────────────────────┘ │
└──────────────────────────────────┘
```

### **State 3: Response loaded**

```
┌──────────────────────────────────┐
│ ✨ Soon ✨                       │  ← icon fades / hides after success
│ ...                              │
│                                  │
│ ┌──────────────────────────────┐ │
│ │ 💭 AI Narrator says:         │ │
│ │                              │ │
│ │ "You're in a sweet spot..."  │ │
│ │                              │ │
│ │ ℹ️ Powered by Gemini AI      │ │
│ └──────────────────────────────┘ │
└──────────────────────────────────┘
```

### **State 4: Error**

```
│ ┌──────────────────────────────┐ │
│ │ 💭 AI Narrator is sleeping   │ │
│ │ right now. Try again soon 😴 │ │
│ └──────────────────────────────┘ │
```

---

## 🏗️ Technical Architecture

### **New endpoint:** `POST /ai_narrate`

**Request body (JSON):**
```json
{
  "category": "Soon",
  "months": 4.2,
  "social_activity": 5,
  "confidence_level": 5,
  "hobbies_count": 3,
  "screen_time": 4,
  "goes_out_per_week": 2,
  "talks_to_new_people": 5
}
```

**Response (success):**
```json
{
  "success": true,
  "narrative": "You're in a sweet spot, friend! ..."
}
```

**Response (error):**
```json
{
  "success": false,
  "message": "AI Narrator is sleeping right now. Try again soon 😴"
}
```

### **Prompt Template** (`ai_narrator.py`)

Uses the proven ROLE/CONTEXT/TASK/INPUT pattern from RJ_BLP_1:

```
### ROLE ###
You are a warm, playful, slightly witty "love life narrator" speaking
to a Year 12 Software Engineering student. Your tone is encouraging,
never creepy or patronizing, with light humor. You're commenting on
a fun ML demo, NOT giving real life advice.

### CONTEXT ###
This is a playful machine learning demo predicting "when will someone
find true love" based on lifestyle data. The backend uses:
- Decision Tree Classifier (sklearn) → category
- Polynomial Ridge Regression (sklearn) → months estimate

Categories: Very Soon, Soon, Eventually, Keep Trying

### TASK ###
1. Write a 4-5 sentence narrative explaining the prediction in plain English.
2. Reference at least TWO of the user's actual input values (specific, not generic).
3. Mention that this is a fun demo, not real-life advice.
4. End with light encouragement.
5. Never be discouraging, mean, or judgmental.
6. Format Output: Provide your response as a single, clean JSON object.
   Do not include any text or markdown before or after the JSON.
   The JSON must have this exact key: `narrative`.

### INPUT ###
* Predicted category: {category}
* Estimated months: {months}
* Social Activity Level: {social_activity}/10
* Confidence Level: {confidence_level}/10
* Hobbies count: {hobbies_count}
* Screen time: {screen_time} hours/day
* Goes out per week: {goes_out_per_week}
* Talks to new people: {talks_to_new_people}/10
```

---

## 📁 File Changes

| File | Action | Purpose |
|------|--------|---------|
| `requirements.txt` | Modify | Add `google-generativeai` |
| `config.py` | Create (gitignored) | Store `GEMINI_API_KEY` |
| `.gitignore` | Modify | Add `config.py` |
| `ai_narrator.py` | Create | Module: prompt builder + Gemini caller |
| `app.py` | Modify | Add `/ai_narrate` route |
| `templates/index.html` | Modify | Add sparkle icon + AJAX |
| `static/css/style.css` | Modify | Style sparkle icon + narrator card |
| `DEPLOY.md` | Modify | Add API key setup section |
| `CHANGELOG.md` | Modify | Document this feature |

---

## 🔐 Security & Config

### Local development
- Create `config.py` in project root:
  ```python
  GEMINI_API_KEY = "your-key-here"
  ```
- Already gitignored — never committed.

### PythonAnywhere deployment
- After `git pull`, manually create `config.py` on the server (one time):
  ```bash
  cd ~/12SE_True_Love_AI
  nano config.py
  # Paste: GEMINI_API_KEY = "your-key-here"
  # Save: Ctrl+O, Enter, Ctrl+X
  ```
- Reload web app.

### Graceful degradation
If `config.py` is missing or `GEMINI_API_KEY` not set:
- Sparkle icon still appears (don't break UI)
- Click → returns `{success: false, message: "..."}` with friendly text
- Server logs warning at startup but doesn't crash

---

## 🛡️ Error Handling

| Scenario | Behaviour |
|----------|-----------|
| API key missing | Friendly message: "AI Narrator unavailable" |
| Gemini API timeout | Friendly message: "AI is sleeping" |
| Malformed JSON response | Strip fences, retry parse, fallback message |
| Rate limit hit (429) | "Too many requests, try again in a minute" |
| Network failure | Friendly fallback message |

All failures: log server-side, return 200 with `{success: false}` (never 500).

---

## ✅ Implementation Order

1. **AI_BUILD.md** — this document (done)
2. **`requirements.txt`** — add `google-generativeai`
3. **`.gitignore`** — add `config.py`
4. **`config.py`** — create local copy with API key
5. **`ai_narrator.py`** — module with prompt builder + Gemini call
6. **`app.py`** — add `/ai_narrate` route
7. **`templates/index.html`** — sparkle icon + AJAX JS
8. **`static/css/style.css`** — styling
9. **Local test** — verify all routes still work + AI narrator works
10. **`DEPLOY.md`** — add API key setup section
11. **`CHANGELOG.md`** — document feature
12. **Commit + push** — ready for PA deployment

**Estimated time:** ~45 minutes total.

---

## 🎓 Educational Value (for Year 12 SE)

This feature teaches:
1. **Hybrid AI architecture** — combining classical ML + GenAI
2. **API integration** — calling external services from Flask
3. **Prompt engineering** — structured ROLE/CONTEXT/TASK/INPUT pattern
4. **Async UX** — on-demand AJAX vs blocking renders
5. **Secrets management** — `.gitignore`, `config.py`, manual server setup
6. **Graceful degradation** — building software that doesn't break when one part fails

Perfect alignment with the Software Engineering syllabus.

---

## 🧠 Admin Dashboard Hybrid Teaching Features (Cross-Reference)

After the core AI narrator build, the admin dashboard was extended to make the **hybrid system** and **chaining** process visible for students.

### Added in `templates/admin.html`
- **Hybrid Pipeline Diagram (top of admin page)**
  - Stage 1 Decision Tree → Stage 2 Polynomial Ridge → Stage 3 Gemma neural network
- **Stage 3 Gemma Architecture Card**
  - Model ID, transformer architecture, status indicator, and chaining explanation
- **Chain in Action Live Demo**
  - Shows sample input, Stage 1+2 outputs, and calls Stage 3 on demand
- **Classical ML vs Neural Network Comparison Table**
  - Side-by-side view of architecture, training style, outputs, determinism, and runtime
- **Prompt Inspector**
  - Collapsible view of the actual ROLE/CONTEXT/TASK/INPUT prompt sent to Gemma

### Supporting Backend + Styling
- `app.py`: passes `ai_available`, `sample_input`, `sample_category`, `sample_months`, `sample_prompt_preview`
- `static/css/style.css`: styles all hybrid admin modules (pipeline, stage tags, chain flow, comparison table, prompt preview)

### Related Documentation
- `README.md` → Admin Features section (hybrid-chain additions)
- `CHANGELOG.md` → "Admin Dashboard: Hybrid Chain Visual Teaching Layer"
