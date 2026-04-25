# 💘 When Will I Find True Love?

A playful machine learning web application that predicts when someone will find "true love" based on lifestyle data. Built for educational purposes to demonstrate classification and regression models.

## 🎯 Features

- **Dual ML Models:**
  - Decision Tree Classifier (predicts category: Very Soon, Soon, Eventually, Keep Trying)
  - Polynomial Ridge Regression (predicts timeline in months)
  - Model architecture transparency (19 nodes, 10 leaves, 28 polynomial features)
  
- **Interactive Web Interface:**
  - Modern, elegant UI with enhanced typography and visual hierarchy
  - Real-time predictions with detailed, ML-driven explanations
  - Admin dashboard with model metrics, ML transparency features
  - Visual ML charts: polynomial curve, decision tree diagram, interaction heatmap
  - Input validation with realistic range checking

- **Educational Focus:**
  - Demonstrates overfitting concepts
  - Shows feature importance with actual weights
  - Includes training metrics and warnings
  - Comprehensive teaching documentation (ML_EXPLAINED.md)
  - Optimization analysis guide (OPTIMAL_PREDICTIONS.md)
  - Proves real ML is used (not hardcoded JavaScript)

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Prepare Training Data

**Option A:** Use the existing `data.csv` (80 records included)

**Option B:** Generate fresh data:
```bash
python utils/seed_data.py
```

This creates sample data and exports to `data.csv`.

### 3. Run the Application

```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

## 📁 Project Structure

```
12SE_True_Love_AI/
├── app.py                      # Flask routes and server
├── ml_engine.py                # ML models (Decision Tree + Ridge)
├── requirements.txt            # Python dependencies
├── data.csv                    # Training data (CSV format) ⭐ PRIMARY DATA SOURCE
├── models.pkl                  # Trained models (auto-generated)
├── CHANGELOG.md                # Project history and updates
├── README.md                   # Main documentation (this file)
├── SPEC.md                     # Original specification
├── ML_EXPLAINED.md             # Teaching guide (jargon-free) ⭐ NEW
├── OPTIMAL_PREDICTIONS.md      # Optimization analysis ⭐ NEW
├── static/
│   └── css/
│       └── style.css           # Application styles
├── templates/
│   ├── index.html              # Main prediction interface
│   └── admin.html              # Admin dashboard with ML transparency
└── utils/                      # Utility scripts
    ├── seed_data.py            # Generate sample training data
    ├── test_data_quality.py    # Automated data analysis
    ├── analyze_hobbies.py      # Feature analysis tool
    ├── find_lowest_prediction.py # Optimization script ⭐ NEW
    └── TESTING_GUIDE.md        # Testing documentation
```

## 🎨 UI Design

- **Typography:** Lora (serif) + Roboto (sans-serif)
- **Color Palette:**
  - Background: `rgb(233, 230, 225)` with gradient
  - Accent: `rgb(211, 169, 153)` (dusty rose)
  - Secondary: `rgb(165, 174, 183)` (cool gray-blue)
- **Style:** Contemporary, glassmorphism, smooth animations

## 🧠 How It Works

1. **Data Collection:** User inputs 6 lifestyle features (validated server-side)
2. **Prediction:** 
   - Decision Tree classifies into outcome category (with probability distribution)
   - Polynomial Ridge Regression estimates months to love (with feature interactions)
3. **Explanation:** ML-driven system provides detailed reasoning:
   - Model confidence levels
   - Feature-specific analysis (✓ Strengths, ⚠ Areas to Improve)
   - Contextual insights based on training data patterns
   - Both models explicitly mentioned
4. **Training Pipeline:**
   - CSV data → Model training → Pickle storage
   - Edit `data.csv` directly to add/modify training data
   - Click "Retrain Models" in admin to update predictions
   - Models persist between sessions for fast startup

## 📊 Machine Learning Details

### Decision Tree Classifier
- `max_depth=4` - Prevents deep memorization
- `min_samples_leaf=3` - Requires minimum samples per leaf
- Purpose: Prevents overfitting on small datasets

### Polynomial Ridge Regression
- `degree=2` - Captures non-linear relationships
- `alpha=1.5` - Regularization to prevent overfitting
- Purpose: Stable predictions even with small/growing datasets

## 🔧 Admin Features

- **Dataset Summary:** Record count from CSV, last training time, feature count
- **ML Model Architecture Display:** ⭐ NEW
  - Decision Tree: max_depth, min_samples_leaf, node count, leaf count, learned classes
  - Polynomial Ridge: degree, alpha, feature expansion (6→28)
  - Real-time parameters from sklearn objects
- **Live Model Prediction Example:** ⭐ NEW
  - Sample prediction with actual probability distribution
  - Demonstrates real `predict_proba()` calculations
  - Proves ML is not hardcoded
- **Visual ML Charts:** ⭐ NEW
  - **Polynomial Regression Curve:** Shows the actual curve learned by Ridge regression
  - **Decision Tree Diagram:** Renders the real sklearn tree structure (`plot_tree`)
  - **Feature Interaction Heatmap:** 2D visualization showing how features combine
  - All charts generated from live model predictions (matplotlib)
- **Model Metrics:** Training accuracy and error with overfitting warnings
- **Feature Importance:** Visual bar chart with actual weights
- **Retrain Button:** Retrain models with current CSV data

## 📝 Adding Training Data

Simply edit `data.csv` directly:

```csv
social_activity,confidence_level,hobbies_count,screen_time,goes_out_per_week,talks_to_new_people,outcome,months_to_love
8,7,5,4.5,3,6,Soon,5.2
```

Then click "Retrain Models" in the admin dashboard to incorporate changes.

## ⚠️ Educational Notes

- **Overfitting Warning:** 100% training accuracy = memorization
- **Small Dataset:** 60 records is intentionally small for teaching
- **No Validation Split:** Simplified for classroom use
- **Disclaimer:** Predictions are not real-life outcomes!

## 🎓 Teaching Hooks

1. **The "Cheat Test":** Can students game the model by changing screen time?
2. **The "Accuracy Illusion":** Why does 80% accuracy beat 100%?
3. **Feature Importance:** Which lifestyle factors matter most? (Screen time: 43%!)
4. **ML Transparency:** Show students the actual sklearn model parameters
5. **Optimization Challenge:** Find the combination that gives < 2 months (see OPTIMAL_PREDICTIONS.md)
6. **Overfitting Demo:** Input exact training data → 100% confidence (memorization!)

## 📚 Documentation

- **`ML_EXPLAINED.md`** - Complete teaching guide (jargon-free)
  - Simple analogies for Decision Tree and Polynomial Ridge
  - Feature importance breakdown
  - Real prediction walkthrough
  - 4 classroom activities
  - Common misconceptions
  - Student-friendly vocabulary
  
- **`OPTIMAL_PREDICTIONS.md`** - Optimization analysis
  - Absolute lowest prediction (1.10 months)
  - Top 10 combinations
  - Feature importance insights
  - Surprising findings (why maxing everything ≠ best!)
  
- **`TESTING_GUIDE.md`** - Testing procedures
  - Edge case testing
  - Data quality checks
  - Model validation

## 🎨 UI Enhancements

- **Enhanced Typography:** Clear visual hierarchy with Lora (serif) + Roboto (sans-serif)
- **Detailed Explanations:** ML-driven reasoning with categorized feedback
- **Input Validation:** Server-side range checking with helpful warnings
- **Interactive Elements:** Hover effects, smooth transitions, glassmorphism

## 📝 License

Educational project for classroom use.
