# Testing Guide: Checking for Outliers & Data Skew

## Quick Start

Run the automated analysis script:
```bash
python test_data_quality.py
```

This will show you:
- Outcome distribution (class balance)
- Feature statistics and outliers
- Target variable distribution
- Edge case predictions

---

## Manual Testing Steps

### Step 1: Check Dataset Balance

**In Browser:**
1. Go to `http://localhost:5000/admin`
2. Look at the record count (should be 81)
3. Click "Retrain Models"
4. Note the training accuracy

**What to look for:**
- Training accuracy > 95% = likely overfitting
- Training accuracy < 70% = data quality issues

---

### Step 2: Test Edge Cases

**Test these profiles in the main form:**

#### Test A: Perfect Profile (Should predict "Very Soon")
- Social Activity: 10
- Confidence: 10
- Hobbies: 8
- Screen Time: 2
- Goes Out: 7
- Talks to New People: 10

**Expected:** Very Soon, 1-4 months

#### Test B: Worst Case (Should predict "Keep Trying")
- Social Activity: 1
- Confidence: 1
- Hobbies: 0
- Screen Time: 16
- Goes Out: 0
- Talks to New People: 1

**Expected:** Keep Trying, 30-65 months

#### Test C: Average Profile (Should predict "Soon" or "Eventually")
- Social Activity: 5
- Confidence: 5
- Hobbies: 3
- Screen Time: 6
- Goes Out: 3
- Talks to New People: 5

**Expected:** Soon/Eventually, 5-12 months

#### Test D: High Screen Time Test
- Social Activity: 7
- Confidence: 7
- Hobbies: 5
- Screen Time: 14 ⚠️
- Goes Out: 4
- Talks to New People: 6

**Expected:** Should penalize for screen time → Eventually/Keep Trying

---

### Step 3: Check for Unrealistic Predictions

**Red Flags:**
- ❌ Perfect profile predicting > 10 months
- ❌ Worst profile predicting < 20 months
- ❌ All predictions clustering around same value
- ❌ Months > 100 or < 1
- ❌ Same category for wildly different inputs

---

### Step 4: Inspect Training Data

**Open `data.csv` and check:**

```bash
# Count outcomes
grep "Very Soon" data.csv | wc -l
grep "Soon" data.csv | wc -l
grep "Eventually" data.csv | wc -l
grep "Keep Trying" data.csv | wc -l
```

**Or in Python:**
```python
import pandas as pd
df = pd.read_csv('data.csv')
print(df['outcome'].value_counts())
print(df['months_to_love'].describe())
```

**Look for:**
- Balanced distribution (each category 15-25 records)
- Months range: 1-65
- No duplicate rows
- No missing values

---

### Step 5: Visual Inspection

**Create a quick visualization:**

```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data.csv')

# Plot outcome distribution
df['outcome'].value_counts().plot(kind='bar')
plt.title('Outcome Distribution')
plt.show()

# Plot months distribution
df['months_to_love'].hist(bins=20)
plt.title('Months to Love Distribution')
plt.xlabel('Months')
plt.show()

# Boxplot for outliers
df[['social_activity', 'confidence_level', 'screen_time', 
    'goes_out_per_week', 'talks_to_new_people']].boxplot()
plt.title('Feature Outliers')
plt.xticks(rotation=45)
plt.show()
```

---

## Common Issues & Fixes

### Issue 1: Model Always Predicts "Very Soon"
**Cause:** Dataset skewed toward positive outcomes
**Fix:** Add more "Keep Trying" and "Eventually" records

### Issue 2: Predictions Don't Make Sense
**Cause:** Outliers or data entry errors
**Fix:** Run `test_data_quality.py` and review flagged records

### Issue 3: Training Accuracy = 100%
**Cause:** Overfitting (model memorized data)
**Fix:** This is expected with small datasets - it's a teaching point!

### Issue 4: Huge Variance in Predictions
**Cause:** Inconsistent labeling in training data
**Fix:** Review data.csv for logical consistency

---

## Expected Results (With Balanced Dataset)

**Outcome Distribution:**
- Very Soon: ~20-25%
- Soon: ~25-30%
- Eventually: ~20-25%
- Keep Trying: ~25-30%

**Months Range:**
- Very Soon: 1-4 months
- Soon: 4-8 months
- Eventually: 8-20 months
- Keep Trying: 20-65 months

**Feature Importance (Typical):**
1. talks_to_new_people (0.6-0.9)
2. goes_out_per_week (0.5-0.8)
3. social_activity (0.4-0.7)
4. screen_time (0.2-0.4)
5. confidence_level (0.3-0.6)
6. hobbies_count (0.2-0.5)

---

## Automated Test Command

```bash
# Run full analysis
python test_data_quality.py

# Check if app is running
curl http://localhost:5000

# Test prediction API (if you add one)
curl -X POST http://localhost:5000/predict -d "social_activity=5&confidence_level=5..."
```

---

## What Good Data Looks Like

✅ **Balanced classes** (no category > 35% of total)
✅ **Logical consistency** (high social activity → lower months)
✅ **Smooth distribution** (not all clustered at extremes)
✅ **No missing values**
✅ **Features in valid ranges** (1-10 for scales, 0-24 for hours)
✅ **Realistic months** (1-65 range)

---

## Teaching Moment

**This is intentional for classroom use:**
- Small dataset (81 records) → Shows overfitting
- High training accuracy → Demonstrates memorization
- Imperfect predictions → Teaches model limitations

The goal is to show students that ML models aren't magic!
