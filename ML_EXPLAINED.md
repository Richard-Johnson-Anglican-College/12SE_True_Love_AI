# How the Machine Learning Works (Teacher's Guide)

A simple, jargon-free explanation of the ML models powering "When Will I Find True Love?"

---

## 🎯 The Big Picture

This app uses a **hybrid AI system** with **three chained models**:

1. **Decision Tree** - Decides the category (Very Soon, Soon, Eventually, Keep Trying)
2. **Polynomial Ridge Regression** - Calculates the exact number of months
3. **Gemma Neural Network (LLM)** - Turns the ML output into a witty natural-language narrative

Think of it like asking three experts in sequence: one gives a category, one gives a number, and one explains it like a human.

### 🔗 Chaining Flow

```text
Stage 1 (Classical ML): Decision Tree           -> category
Stage 2 (Classical ML): Polynomial Ridge        -> months
Stage 3 (Neural Network): Gemma (Gemini API)    -> narrative
```

The key idea is **chaining**: Stage 1 + Stage 2 outputs are injected into the Stage 3 prompt.

---

## 🌳 Model 1: Decision Tree Classifier

### What It Does
Classifies people into 4 categories based on their answers.

### How It Works (Simple Analogy)

Imagine a flowchart with yes/no questions:

```
Start Here
    ↓
Does person talk to new people often (≥8)?
    ├─ YES → Do they go out frequently (≥5x/week)?
    │           ├─ YES → "Very Soon" ✨
    │           └─ NO → "Soon" 
    └─ NO → Is screen time high (≥10 hrs)?
                ├─ YES → "Keep Trying" 
                └─ NO → "Eventually"
```

**Real Example:**
- Input: Talks to new people = 10, Goes out = 7x
- Tree follows: YES → YES → **"Very Soon"**

### Why It's Called a "Tree"
- **Root:** Starting question
- **Branches:** Each decision path
- **Leaves:** Final answers (10 leaves in our model)
- **Nodes:** Decision points (19 nodes total)

### Our Tree's Settings
- **Max Depth:** 4 levels deep (prevents memorizing data)
- **Min Samples per Leaf:** 3 people (ensures reliable patterns)
- **Total Nodes:** 19 decision points
- **Leaf Nodes:** 10 final outcomes

### How It Gives Probabilities

Each leaf contains training examples. If a leaf has:
- 6 "Very Soon" examples
- 1 "Soon" example
- 0 others

Then prediction = **86% Very Soon, 14% Soon**

**Teaching Moment:** This is why you sometimes see 100% confidence - the leaf only has one type of outcome!

---

## 📈 Model 2: Polynomial Ridge Regression

### What It Does
Predicts the exact number of months (e.g., 2.1 months, 9.5 months).

### How It Works (Simple Analogy)

Imagine drawing a curved line through dots on a graph:

```
Months
  ↑
65|                              • (worst case)
  |
30|              •
  |         •
10|    •  •
  |  •
 1| •                            • (best case)
  └────────────────────────────→
    Low                    High
        Social Score
```

The model finds the **best-fitting curve** through all 80 training examples.

### Why "Polynomial"?

Instead of a straight line, it uses a **curved line** (degree 2):

**Straight line (boring):**
```
months = 10 - (social_activity × 0.5)
```

**Polynomial (better):**
```
months = 15 - (social × 2) + (social² × 0.1) - (social × confidence × 0.3)
```

The `social²` and `social × confidence` parts capture **interactions** between features.

**Real Example:**
- High social (10) + High confidence (10) = Extra bonus!
- The model learns: "These two together are better than the sum of parts"

### Feature Expansion

Our model expands **6 inputs into 28 features**:

**Original 6:**
1. social_activity
2. confidence_level
3. hobbies_count
4. screen_time
5. goes_out_per_week
6. talks_to_new_people

**Becomes 28 features including:**
- Original 6
- Squares: social², confidence², etc. (6 more)
- Interactions: social × confidence, social × hobbies, etc. (15 more)
- Constant term (1 more)

**Total:** 6 + 6 + 15 + 1 = 28 features

### Why "Ridge"?

Ridge = **Regularization** = Prevents the model from being too confident.

**Without Ridge:**
- Model might predict: "10 social = 0.001 months" (unrealistic!)

**With Ridge (alpha = 1.5):**
- Model predicts: "10 social = 1.1 months" (more realistic)

It adds a "penalty" for extreme predictions, keeping results sensible.

---

## 🧠 Model 3: Gemma Neural Network Narrator (Stage 3)

### What It Does
Converts the structured ML output into a readable explanation with personality.

### Why We Need It
- Stage 1 + 2 are great at numbers and categories
- But they do not write natural language
- Stage 3 (Gemma) bridges that gap

### How It Is Chained

The app builds a prompt using a structured template:
- `ROLE`
- `CONTEXT`
- `TASK`
- `INPUT`

Inside `INPUT`, it includes:
- Predicted category (from Decision Tree)
- Predicted months (from Polynomial Ridge)
- Original 6 user features

So Stage 3 is not guessing blindly; it is reasoning over the upstream ML outputs.

### Runtime Notes (Classroom-Friendly)
- Model: `gemma-3n-e4b-it`
- Accessed via Gemini API
- On-demand (sparkle button), not auto-run
- If API key is missing, app degrades gracefully with a friendly message

---

## ⚖️ Feature Importance (What Matters Most)

The Decision Tree learns which questions are most important:

| Feature | Importance | What This Means |
|---------|------------|-----------------|
| **Screen Time** | 0.43 (43%) | Most important! High screen time = bad |
| **Talks to New People** | 0.21 (21%) | Very important! This is the #1 social skill |
| **Goes Out Per Week** | 0.15 (15%) | Important! More outings = more chances |
| **Confidence Level** | 0.13 (13%) | Helpful! Confidence attracts people |
| **Social Activity** | 0.08 (8%) | Minor role! General social vibe |
| **Hobbies Count** | 0.00 (0%) | Tree ignores it — but the Polynomial model uses it heavily! (See below) |

### 🤔 The Hobbies Mystery: Two Models Disagree!

The Decision Tree assigns **0% importance** to hobbies, but does that mean hobbies don't matter? **No!** Here's the surprising truth:

**Decision Tree says:** "I never use hobbies to make decisions" (0% importance)
**Polynomial Ridge says:** "Hobbies actually matter A LOT — there's a sweet spot!"

When we hold all other features constant and vary only hobbies, the Polynomial model produces this curve:

| Hobbies | Predicted Months | Insight |
|---------|------------------|---------|
| 0 | 13.0 | No common ground with people |
| 2 | 10.5 | Some shared interests |
| 4 | 8.9 | Good variety |
| **6** | **8.1** | ⭐ **Sweet spot!** |
| 8 | 8.1 | Still optimal |
| 10 | 8.9 | Going UP — too busy to date! |

**This is a U-shaped curve!** It captures real-world wisdom:
- 🚫 **Too few hobbies (0-2):** Nothing to talk about, no shared activities
- ✅ **Just right (4-8):** Diverse interests, opportunities to meet people
- 🚫 **Too many (9-10):** Schedule is too packed for relationships

### Why the Models Disagree

- **Decision Trees** use *hard splits* (e.g., "is hobbies > 5?"). If no single threshold cleanly separates the data, hobbies gets ignored.
- **Polynomial Ridge** uses *smooth curves* and creates **28 features** from 6 inputs — including interactions like `hobbies × confidence` and `hobbies²`. This captures subtle effects.

**Plain-English interpretation:** In this trained tree, on this dataset and with this depth/leaf configuration, `hobbies` never produced a strong enough hard split to be selected. So tree importance becomes `0%` — which means "not chosen by this tree," not "useless in real life."

### 🎓 Teaching Moment

**"0% importance ≠ no impact!"**

This is a great lesson about ML:
- Different models see the same data differently
- Feature importance from one model doesn't tell the whole story
- Interaction effects can hide a feature's true contribution
- Always validate findings with multiple approaches

### How Importance is Calculated

The tree tracks: **"How much does this question reduce uncertainty?"**

**Example:**
- Before asking about screen time: 50% unsure about outcome
- After asking: 20% unsure
- **Reduction:** 30% → Screen time gets 0.30 importance

### Teaching Moment: Why Hobbies = 0%?

Hobbies don't split the tree well by themselves, BUT they matter in **polynomial interactions**:
- `hobbies × social_activity` = Important!
- `hobbies` alone = Not important

This shows students: **Context matters in ML!**

---

## 🎓 How the Models Learn (Training Process)

### Step 1: Load Training Data
- 80 real profiles from `data.csv`
- Each has 6 features + 2 outcomes (category + months)

### Step 2: Decision Tree Learning

The tree asks: **"What question best splits the data?"**

**Example iteration:**
1. Try splitting on "talks_to_new_people ≥ 7"
   - Left branch: 30 people → 80% "Very Soon"
   - Right branch: 50 people → 60% "Keep Trying"
   - **Good split!** Clear separation

2. Try splitting on "hobbies ≥ 5"
   - Left branch: 40 people → 50% "Soon", 50% "Eventually"
   - Right branch: 40 people → 50% "Soon", 50% "Eventually"
   - **Bad split!** No clear pattern

The tree picks the best split at each level, 4 levels deep.

### Step 3: Polynomial Ridge Learning

The regression model asks: **"What curve fits the data best?"**

**Process:**
1. Expand 6 features → 28 polynomial features
2. Try different coefficients (weights) for each feature
3. Calculate error: How far off are predictions?
4. Adjust coefficients to minimize error
5. Add ridge penalty to prevent overfitting
6. Repeat until error stops improving

**Result:** A formula like:
```
months = 20.5 
         - (talks_to_new × 1.8)
         + (screen_time × 0.9)
         - (goes_out × 0.6)
         + (social × confidence × 0.15)
         ... (28 terms total)
```

### Step 4: Validation

Check accuracy on the training data:
- **Decision Tree:** 80% accuracy (intentionally not 100% to avoid memorization)
- **Polynomial Ridge:** ±2.47 months average error

---

## 🔍 Real Prediction Example (Step-by-Step)

**User Input:**
- Social Activity: 8
- Confidence: 8
- Hobbies: 6
- Screen Time: 2.0 hrs
- Goes Out: 7x/week
- Talks to New People: 10

### Decision Tree Process

**Level 1:** Is talks_to_new_people ≥ 7?
- Answer: YES (10 ≥ 7)
- Go to right branch

**Level 2:** Is screen_time ≤ 5?
- Answer: YES (2.0 ≤ 5)
- Go to left branch

**Level 3:** Is goes_out ≥ 5?
- Answer: YES (7 ≥ 5)
- Go to right branch

**Level 4:** Reached Leaf Node #15
- Contains: 8 "Very Soon" examples, 0 others
- **Prediction: "Very Soon" with 100% confidence**

### Polynomial Ridge Process

**Step 1:** Expand features
```
Original: [8, 8, 6, 2.0, 7, 10]
Expanded: [8, 8, 6, 2.0, 7, 10, 64, 64, 36, 4.0, 49, 100, 
           64, 48, 16, 56, 80, 48, 12, 14, 60, ...]
           (28 features total)
```

**Step 2:** Apply learned formula
```
months = 20.5 
         - (10 × 1.8)      [talks_to_new]
         + (2.0 × 0.9)     [screen_time]
         - (7 × 0.6)       [goes_out]
         + (8 × 8 × 0.15)  [social × confidence]
         + ... (24 more terms)
       = 1.10 months
```

**Final Result:**
- **Category:** Very Soon (from Decision Tree)
- **Months:** 1.10 (from Polynomial Ridge)

---

## 🎯 Why Use a 3-Stage Hybrid System?

### Decision Tree Strengths
✅ Easy to understand (flowchart logic)
✅ Handles categories well
✅ Shows clear decision rules
✅ Fast predictions

### Decision Tree Weaknesses
❌ Can only predict categories (not exact numbers)
❌ Tends to overfit (memorize data)
❌ Predictions are "steppy" (jumps between values)

### Polynomial Ridge Strengths
✅ Predicts exact numbers (1.1, 2.5, 9.8 months)
✅ Smooth predictions (no jumps)
✅ Captures feature interactions
✅ Regularization prevents overfitting

### Polynomial Ridge Weaknesses
❌ Hard to interpret (complex formula)
❌ Can't explain "why" in simple terms
❌ Requires numerical targets (not categories)

### Gemma Stage 3 Strengths
✅ Explains outputs in plain language
✅ Improves engagement and readability
✅ Can reference multiple input features naturally

### Gemma Stage 3 Weaknesses
❌ Not deterministic (wording varies)
❌ Depends on API availability and quota
❌ Should not replace numeric models for core prediction math

### Together They're Better
- Stage 1 predicts **WHAT bucket** (category)
- Stage 2 predicts **WHEN** (exact timeline)
- Stage 3 explains **SO WHAT** (human-readable narrative)

That combination is why this project is a **hybrid system**.

---

## 📊 Model Performance Metrics

### Decision Tree Accuracy: 80%

**What this means:**
- Out of 80 training examples, it correctly predicts 64 categories
- 16 are misclassified (e.g., "Soon" predicted as "Eventually")

**Why not 100%?**
- 100% = Memorization (overfitting)
- 80% = Learning patterns (good generalization)

**Teaching Moment:** Show students that perfect scores can be bad!

### Polynomial Ridge Error: ±2.47 months

**What this means:**
- Average prediction is off by 2.47 months
- Example: True = 10 months, Predicted = 12.47 months

**Why is there error?**
- Real life is messy! Not everyone follows exact patterns
- Model finds the "best fit" line, not a perfect fit

**Teaching Moment:** All models have error - it's about minimizing it!

---

## 🚨 Common Misconceptions (Teaching Points)

### Misconception 1: "The model is just if-else statements"
**Truth:** The tree structure is learned from data, not hardcoded. Different data = different tree!

### Misconception 2: "More data always = better model"
**Truth:** Quality > Quantity. 80 good examples beats 1000 messy examples.

### Misconception 3: "100% accuracy = best model"
**Truth:** 100% = overfitting. The model memorized instead of learned.

### Misconception 4: "All features are equally important"
**Truth:** Screen time (43%) matters way more than hobbies (0%).

### Misconception 5: "The model knows about dating"
**Truth:** It only knows patterns in the training data. Garbage in = garbage out!

---

## 🔬 Overfitting Demonstration (Built-In!)

This app is **intentionally designed** to show overfitting:

### Why Our Model Overfits
1. **Small dataset:** Only 80 examples (real ML uses thousands)
2. **High tree depth:** 4 levels (could be shallower)
3. **Training on same data we test on:** No separate validation set

### How to Show Students

**Test 1:** Input exact training example
- Result: 100% confidence, perfect prediction
- **Why?** Model memorized this exact case!

**Test 2:** Input slightly different values
- Result: Lower confidence, different prediction
- **Why?** Model hasn't seen this exact combination!

**Teaching Moment:** This is why real ML uses train/test splits!

---

## 💡 Classroom Activities

### Activity 1: Feature Importance Experiment
1. Students predict which feature matters most
2. Check the feature importance chart
3. Discuss why screen time > hobbies

### Activity 2: Overfitting Hunt
1. Find a training example in `data.csv`
2. Input exact values → Get 100% confidence
3. Change one value slightly → Watch confidence drop
4. Discuss: Is this good or bad?

### Activity 3: Model Comparison
1. Make same prediction with both models
2. Compare category (tree) vs. months (ridge)
3. Discuss: Why do we need both?

### Activity 4: Chain Inspection Lab
1. Open the admin dashboard pipeline diagram
2. Run "Chain in Action" to execute Stage 1 → Stage 2 → Stage 3
3. Expand the Prompt Inspector
4. Highlight where `category` and `months` are chained into Stage 3
5. Discuss: Which part is deterministic vs. generative?

### Activity 5: Edge Case Testing
1. Input all 10s → What happens?
2. Input all 1s → What happens?
3. Input realistic values → Compare results
4. Discuss: Model limitations

---

## 📚 Key Vocabulary (Student-Friendly)

| Term | Simple Definition | Example |
|------|-------------------|---------|
| **Decision Tree** | A flowchart that makes decisions | "If talks_to_new ≥ 7, go right" |
| **Regression** | Predicting a number | "You'll find love in 5.2 months" |
| **Classification** | Predicting a category | "Very Soon" vs "Keep Trying" |
| **Feature** | An input to the model | Social activity, screen time, etc. |
| **Training** | Teaching the model from examples | Showing it 80 profiles |
| **Prediction** | Model's guess for new data | "Eventually, 9.5 months" |
| **Overfitting** | Memorizing instead of learning | 100% accuracy on training data |
| **Regularization** | Preventing overconfidence | Ridge penalty keeps predictions realistic |
| **Feature Importance** | Which inputs matter most | Screen time = 43%, hobbies = 0% |
| **Polynomial** | Curved relationship | social² captures "more is better, but diminishing returns" |
| **Hybrid System** | Combining model families | Classical ML + neural network in one app |
| **Chaining** | Passing one model's output into another | category + months injected into LLM prompt |
| **Neural Network (LLM)** | A language model with many parameters | Gemma writes the narrative explanation |
| **Transformer** | Neural architecture used by modern LLMs | Gemma is a decoder-only transformer |
| **Prompt Engineering** | Structuring instructions for an LLM | ROLE/CONTEXT/TASK/INPUT |

---

## 🎓 Learning Outcomes

After using this app, students should understand:

1. ✅ **ML models learn from data** (not hardcoded rules)
2. ✅ **Different models have different strengths** (tree vs regression)
3. ✅ **Feature importance varies** (some inputs matter more)
4. ✅ **Overfitting is a real problem** (100% accuracy can be bad)
5. ✅ **Models have limitations** (prediction floor/ceiling)
6. ✅ **Context matters** (hobbies alone ≠ important, but hobbies × social = important)
7. ✅ **Real ML requires validation** (train/test splits)
8. ✅ **Hybrid architecture benefits** (classical ML + neural network)
9. ✅ **Chaining mechanics** (Stage 1+2 outputs become Stage 3 inputs)
10. ✅ **Deterministic vs generative behavior** (stable math vs variable language)

---

## 🔧 Technical Details (For Advanced Students)

### Scikit-Learn Implementation

**Decision Tree:**
```python
from sklearn.tree import DecisionTreeClassifier

model = DecisionTreeClassifier(
    max_depth=4,              # 4 levels deep
    min_samples_leaf=3,       # At least 3 examples per leaf
    random_state=42           # Reproducible results
)
```

**Polynomial Ridge:**
```python
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline

model = Pipeline([
    ('polynomialfeatures', PolynomialFeatures(degree=2)),
    ('ridge', Ridge(alpha=1.5))
])
```

### Model Persistence
Models are saved to `models.pkl` using Python's `pickle` module, so they don't need to be retrained every time.

---

*This guide is designed for Year 12 Software Engineering students learning about Machine Learning.*
*Feel free to adapt the complexity based on your class level!*
