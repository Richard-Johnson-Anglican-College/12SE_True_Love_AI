# 💘 Spec v6: When Will I Find True Love? (Classroom-Proof)

## ✅ Implementation Status

**Status:** FULLY IMPLEMENTED with enhancements

This specification has been completely implemented with additional features beyond the original requirements:

### Core Features (100% Complete)
- ✅ Flask web application with all routes
- ✅ Decision Tree Classifier (max_depth=4, min_samples_leaf=3)
- ✅ Polynomial Ridge Regression (degree=2, alpha=1.5)
- ✅ Gemma neural network narration stage (`gemma-3n-e4b-it` via Gemini API)
- ✅ CSV-based data storage (simplified from SQLite)
- ✅ Model persistence with pickle
- ✅ Admin dashboard with metrics and visualizations
- ✅ Prediction interface with explanations

### Enhancements Beyond Spec
- ✅ **Hybrid AI Chaining** - 3-stage pipeline: classical ML outputs feed a neural network narrator
- ✅ **On-Demand AI Narrator** - Sparkle-triggered Stage 3 response with witty/sarcastic tone
- ✅ **ML Transparency Features** - Admin dashboard shows actual sklearn model parameters
- ✅ **Visual ML Charts** - Polynomial curve, decision tree diagram, feature interaction heatmap (matplotlib)
- ✅ **Hybrid Admin Teaching Layer** - Pipeline diagram, chain demo, comparison table, prompt inspector
- ✅ **Enhanced Explanations** - Detailed, ML-driven reasoning with categorized feedback
- ✅ **Input Validation** - Server-side range checking with warnings
- ✅ **Typography Improvements** - Enhanced visual hierarchy and readability
- ✅ **Comprehensive Documentation** - ML_EXPLAINED.md (teaching guide) and OPTIMAL_PREDICTIONS.md
- ✅ **Research-Backed Features** - Academic citations linking features to relationship psychology
- ✅ **Optimization Tools** - Scripts to find optimal input combinations
- ✅ **Data Quality Analysis** - Automated testing and validation tools

---

This is the smart play. Using **Option B (Ridge)** future-proofs the app in case a highly motivated student dumps 500 rows of data into the system, while adding the leaf constraints keeps the tree from memorizing the database. Keeping the CSV flow is also great for education because it gives students a tangible file they can open in Excel to *see* what the AI is reading.

---

## 1. 🎯 Project Overview
* **App Name:** When Will I Find True Love?
* **Tech Stack:** Flask (Python), Pandas, Scikit-Learn, Gemini API (Gemma), CSV data storage
* **Core Idea:** A playful hybrid AI app predicting when someone will find "true love" using chained stages.
* **Architecture:** Hybrid 3-stage chaining over CSV-only data (no database required)

### Hybrid Chaining Architecture

1. **Stage 1 (Classical ML):** Decision Tree Classifier → `category`
2. **Stage 2 (Classical ML):** Polynomial Ridge Regression → `months`
3. **Stage 3 (Neural Network):** Gemma LLM narrator consumes Stage 1 + Stage 2 + raw features → witty narrative

---

## 2. ⚠️ Disclaimer (Display in App)
> "This is a fun machine learning demo. It does NOT predict real-life outcomes. (If it says 100 months, please don't panic)."

---

## 3. 📊 Data Structure (CSV Format)

CSV file: `data.csv`

| Field | Type | Description |
| :--- | :--- | :--- |
| `social_activity` | Integer (1–10) | Social level |
| `confidence_level`| Integer (1–10) | Confidence |
| `hobbies_count` | Integer (0-10) | Number of hobbies |
| `screen_time` | Float (0-24) | Hours per day |
| `goes_out_per_week`| Integer (0-7) | Nights out |
| `talks_to_new_people`| Integer (1–10) | Social initiative |
| **`outcome`** | **String** | **Target 1:** Label (Very Soon, Soon, Eventually, Keep Trying) |
| **`months_to_love`**| **Float** | **Target 2:** Number (e.g., 2.5) |

**Note:** Data is stored directly in CSV format for easy inspection and editing. No database required.

---

## 4. 🌳 Machine Learning Models (Classroom-Safe)

**Model 1: Decision Tree (The Vibe Classifier)**
*Fixed: Added `min_samples_leaf=3` to prevent the model from memorizing individual student profiles.*
```python
from sklearn.tree import DecisionTreeClassifier

tree_model = DecisionTreeClassifier(
    max_depth=4, 
    min_samples_leaf=3, 
    random_state=42
)
```

**Model 2: Polynomial Ridge Regression (The Timeline Estimator)**
*Fixed: Swapped `LinearRegression` for `Ridge` to handle dimensionality explosion while allowing curves, keeping math stable even with small/growing datasets.*
```python
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline

poly_model = make_pipeline(
    PolynomialFeatures(degree=2),
    Ridge(alpha=1.5)
)
```

**Model 3: Gemma Neural Network Narrator (Stage 3)**
*Chained onto classical outputs; transforms numeric predictions into natural language explanation.*

- Model: `gemma-3n-e4b-it`
- Access: Gemini API
- Prompt pattern: `ROLE / CONTEXT / TASK / INPUT`
- Input includes Stage 1+2 outputs plus the six raw features
- Output contract: JSON with key `narrative`

---

## 5. 🔄 Simplified App Flow (CSV + Hybrid Chaining)
*CSV provides a tangible file students can open and inspect; chaining shows model-family collaboration.*

1. **Data Editing:** Users edit `data.csv` directly (add/modify/delete records)
2. **Retrain:** Click "Retrain Models" button in admin dashboard
3. **Train:** Pandas reads `data.csv`. Models `fit()` on fresh data. Saves to `models.pkl`
4. **Predict (Stages 1+2):** Enter new data → models output Category + Months with detailed explanations
5. **Narrate (Stage 3, on-demand):** User clicks sparkle icon → `/ai_narrate` sends chained payload to Gemma → receives witty narrative

**Benefits:**
- No database setup required
- Students can see training data directly
- Easy to add/modify examples
- Transparent data flow

---

## 6. 🧾 Explanation Function (Enhanced ML-Driven)
The explanation system provides detailed, context-aware reasoning:

**Features:**
- Model confidence display (e.g., "Decision Tree classified you as 'Very Soon' with 100% confidence")
- Polynomial Ridge timeline mention (e.g., "calculated 2.1 months based on feature interactions")
- Categorized feedback:
  - ✓ **Strengths:** Positive factors (e.g., "Excellent at meeting new people (10/10) - this is the #1 predictor!")
  - ⚠ **Areas to Improve:** Negative factors (e.g., "High screen time (12 hrs/day) - less time for real connections")
  - → **Observations:** Neutral characteristics
- Feature-specific thresholds based on training data patterns
- ML insight about feature importance

**Example output:**
```
Model Analysis: Decision Tree classified you as 'Very Soon' with 100% confidence
Timeline Prediction: Polynomial Ridge Regression calculated 2.1 months based on feature interactions

✓ Strengths:
  • Excellent at meeting new people (10/10) - this is the #1 predictor!
  • Very active social calendar (7x/week) - more opportunities!
  • Low screen time (2.0 hrs/day) - more time for in-person interactions

🔬 ML Insight: The model weighs 'talks to new people' and 'screen time' most heavily in predictions
```

---

## 7. 🧠 Admin Dashboard (Model Lab with ML Transparency)
*Demonstrates real ML with actual sklearn model parameters*

**Hybrid System Overview** ⭐ NEW
* Top-of-page 3-stage pipeline diagram (Stage 1 → Stage 2 → Stage 3)
* Explicit chaining handoff explanation (`category` + `months` injected into Stage 3 prompt)

**Dataset Summary**
* Records: 80 (from CSV)
* Last trained: *timestamp*
* Features: 6
* Model Status: ✓ Ready
* `[ Retrain Models Button ]`

**ML Model Architecture Display** ⭐ NEW
* **Decision Tree Classifier (sklearn):**
  - Max Depth: 4
  - Min Samples/Leaf: 3
  - Tree Nodes: 19
  - Leaf Nodes: 10
  - Classes Learned: Eventually, Keep Trying, Soon, Very Soon
* **Polynomial Ridge Regression (sklearn):**
  - Polynomial Degree: 2
  - Alpha (Regularization): 1.5
  - Input Features: 6
  - Polynomial Features: 28 (includes interactions)
* **Gemma Neural Network (Gemini API):**
  - Model ID: `gemma-3n-e4b-it`
  - Architecture: Transformer (decoder-only)
  - Role in chain: Converts Stage 1+2 outputs into natural-language narrative
  - Runtime status shown in dashboard (`ai_available`)

**Chain in Action Demo** ⭐ NEW
* Shows sample input and Stage 1+2 outputs
* "Run the Full Chain" button triggers live Stage 3 call
* Displays end-to-end hybrid output in one panel

**Classical ML vs Neural Network Comparison Table** ⭐ NEW
* Side-by-side teaching comparison of architecture, training mode, output type, determinism, and compute runtime

**Stage 3 Prompt Inspector** ⭐ NEW
* Collapsible panel showing the actual chained prompt sent to Gemma
* Makes prompt engineering transparent for students

**Live Model Prediction Example** ⭐ NEW
* Sample input with actual probability distribution
* Shows real `predict_proba()` output
* Proves ML is not hardcoded JavaScript

**Model Performance (Training Metrics)**
* **Decision Tree (Training Accuracy):** 80% *(Note: 100% means it memorized the data!)*
* **Polynomial Ridge (Training Error):** ±2.47 months *(Lower is better, but too low = overfitting)*

**Visualizations** ⭐ NEW
* Feature importance bar chart (with actual weights)
* Probability distribution bars (real-time calculations)
* **Polynomial Regression Curve** - Visual proof of the polynomial model (matplotlib)
* **Decision Tree Diagram** - Actual sklearn tree structure (`plot_tree`)
* **Feature Interaction Heatmap** - 2D visualization of feature combinations

---

## 8. 🎨 UI Design (Implemented)
* **Style:** Light mode, elegant, glassmorphism, contemporary, smooth animations
* **Typography:**
  * Headings: Lora (serif, elegant)
  * Body: Roboto (sans-serif, clean)
* **Colors:**
  * Background: `rgb(233, 230, 225)` (warm cream with gradient)
  * Accent: `rgb(211, 169, 153)` (dusty rose)
  * Secondary: `rgb(165, 174, 183)` (cool gray-blue)
  * Text: `rgb(33, 29, 30)` (deep charcoal)
* **Effects:**
  * Glassmorphism cards with backdrop blur
  * Gradient buttons and backgrounds
  * Hover effects with smooth transitions
  * Enhanced visual hierarchy with smart font sizing

---

## 9. 🧠 Teaching Hooks
* **The "Cheat" Test:** Can you change your screen time to trick the model into saying "Very soon"?
* **The "Accuracy" Illusion:** Why is the Training Accuracy 95% on the dashboard, but the predictions feel wrong? (Answer: Overfitting small data).

---

## 10. 📁 Folder Structure
```text
true-love-app/
├── app.py              # Flask Routes
├── ml_engine.py        # Ridge & Tree Logic
├── ai_narrator.py      # Stage 3 Gemma prompt + API caller
├── config.example.py   # Template for GEMINI_API_KEY
├── seed_data.py        # Script to generate initial rows
├── data.csv            # Exported flat-file for training
├── static/css/style.css
└── templates/
    ├── index.html
    └── admin.html
```