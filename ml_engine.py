import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
import pickle
import os

class TrueLovePredictor:
    def __init__(self):
        self.tree_model = DecisionTreeClassifier(
            max_depth=4,
            min_samples_leaf=3,
            random_state=42
        )
        
        self.poly_model = make_pipeline(
            PolynomialFeatures(degree=2),
            Ridge(alpha=1.5)
        )
        
        self.feature_names = [
            'social_activity',
            'confidence_level',
            'hobbies_count',
            'screen_time',
            'goes_out_per_week',
            'talks_to_new_people'
        ]
        
        self.is_trained = False
        self.training_accuracy = 0
        self.training_error = 0
        self.feature_importance = {}
    
    def train(self, csv_path='data.csv'):
        """Train both models on data from CSV"""
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"Training data not found: {csv_path}")
        
        df = pd.read_csv(csv_path)
        
        X = df[self.feature_names].values
        y_class = df['outcome'].values
        y_reg = df['months_to_love'].values
        
        self.tree_model.fit(X, y_class)
        self.poly_model.fit(X, y_reg)
        
        self.training_accuracy = self.tree_model.score(X, y_class) * 100
        
        y_pred = self.poly_model.predict(X)
        self.training_error = np.mean(np.abs(y_pred - y_reg))
        
        importances = self.tree_model.feature_importances_
        self.feature_importance = {
            name: float(imp) for name, imp in zip(self.feature_names, importances)
        }
        
        self.is_trained = True
        
        return {
            'records': len(df),
            'tree_accuracy': round(self.training_accuracy, 1),
            'poly_error': round(self.training_error, 2),
            'feature_importance': self.feature_importance
        }
    
    def predict(self, data):
        """Make prediction on new data"""
        if not self.is_trained:
            raise ValueError("Models not trained. Call train() first.")
        
        X = np.array([[
            data['social_activity'],
            data['confidence_level'],
            data['hobbies_count'],
            data['screen_time'],
            data['goes_out_per_week'],
            data['talks_to_new_people']
        ]])
        
        category = self.tree_model.predict(X)[0]
        months = float(self.poly_model.predict(X)[0])
        months = max(1, round(months, 1))
        
        probabilities = self.tree_model.predict_proba(X)[0]
        classes = self.tree_model.classes_
        prob_dict = {cls: float(prob) for cls, prob in zip(classes, probabilities)}
        
        return {
            'category': category,
            'months': months,
            'probabilities': prob_dict
        }
    
    def save_models(self, path='models.pkl'):
        """Save trained models to disk"""
        with open(path, 'wb') as f:
            pickle.dump({
                'tree': self.tree_model,
                'poly': self.poly_model,
                'feature_importance': self.feature_importance,
                'training_accuracy': self.training_accuracy,
                'training_error': self.training_error
            }, f)
    
    def load_models(self, path='models.pkl'):
        """Load trained models from disk"""
        if os.path.exists(path):
            with open(path, 'rb') as f:
                data = pickle.load(f)
                self.tree_model = data['tree']
                self.poly_model = data['poly']
                self.feature_importance = data['feature_importance']
                self.training_accuracy = data['training_accuracy']
                self.training_error = data['training_error']
                self.is_trained = True
            return True
        return False

def explain(data, prediction_result=None):
    """Generate detailed ML-driven explanation for prediction"""
    reasons = []
    
    # Positive factors (help prediction)
    positive_factors = []
    negative_factors = []
    neutral_factors = []
    
    # Analyze each feature with specific thresholds and context
    
    # Social Activity (1-10)
    if data['social_activity'] >= 8:
        positive_factors.append(f"High social activity level ({data['social_activity']}/10) - you're actively engaging with others")
    elif data['social_activity'] <= 3:
        negative_factors.append(f"Low social activity ({data['social_activity']}/10) - consider joining more social events")
    else:
        neutral_factors.append(f"Moderate social activity ({data['social_activity']}/10)")
    
    # Confidence Level (1-10)
    if data['confidence_level'] >= 8:
        positive_factors.append(f"Strong confidence level ({data['confidence_level']}/10) - confidence is attractive!")
    elif data['confidence_level'] <= 3:
        negative_factors.append(f"Low confidence ({data['confidence_level']}/10) - building self-confidence helps")
    
    # Talks to New People (1-10) - MOST IMPORTANT FEATURE
    if data['talks_to_new_people'] >= 8:
        positive_factors.append(f"Excellent at meeting new people ({data['talks_to_new_people']}/10) - this is the #1 predictor!")
    elif data['talks_to_new_people'] >= 6:
        positive_factors.append(f"Good at talking to new people ({data['talks_to_new_people']}/10) - keep it up!")
    elif data['talks_to_new_people'] <= 3:
        negative_factors.append(f"Rarely talk to new people ({data['talks_to_new_people']}/10) - this is holding you back the most")
    else:
        neutral_factors.append(f"Occasionally talk to new people ({data['talks_to_new_people']}/10)")
    
    # Goes Out Per Week (0-7)
    if data['goes_out_per_week'] >= 5:
        positive_factors.append(f"Very active social calendar ({data['goes_out_per_week']}x/week) - more opportunities!")
    elif data['goes_out_per_week'] >= 3:
        positive_factors.append(f"Regular outings ({data['goes_out_per_week']}x/week) - good exposure")
    elif data['goes_out_per_week'] <= 1:
        negative_factors.append(f"Rarely go out ({data['goes_out_per_week']}x/week) - limited opportunities to meet people")
    
    # Screen Time (0-24 hours)
    if data['screen_time'] >= 12:
        negative_factors.append(f"Very high screen time ({data['screen_time']} hrs/day) - less time for real connections")
    elif data['screen_time'] >= 8:
        negative_factors.append(f"High screen time ({data['screen_time']} hrs/day) - could reduce for more social time")
    elif data['screen_time'] <= 4:
        positive_factors.append(f"Low screen time ({data['screen_time']} hrs/day) - more time for in-person interactions")
    
    # Hobbies Count (0-10)
    if data['hobbies_count'] >= 6:
        positive_factors.append(f"Many hobbies ({data['hobbies_count']}) - diverse interests create conversation topics")
    elif data['hobbies_count'] >= 4:
        positive_factors.append(f"Several hobbies ({data['hobbies_count']}) - good for meeting like-minded people")
    elif data['hobbies_count'] <= 1:
        neutral_factors.append(f"Few hobbies ({data['hobbies_count']}) - consider exploring new interests")
    
    # Build explanation with ML context
    if prediction_result:
        reasons.append(f"Model Analysis: Decision Tree classified you as '{prediction_result['category']}' with {max(prediction_result['probabilities'].values())*100:.0f}% confidence")
        reasons.append(f"Timeline Prediction: Polynomial Ridge Regression calculated {prediction_result['months']:.1f} months based on feature interactions")
    
    # Add positive factors first
    if positive_factors:
        reasons.append("✓ Strengths:")
        reasons.extend([f"  • {factor}" for factor in positive_factors])
    
    # Add negative factors
    if negative_factors:
        reasons.append("⚠ Areas to Improve:")
        reasons.extend([f"  • {factor}" for factor in negative_factors])
    
    # Add neutral observations
    if neutral_factors and len(positive_factors) < 2:
        reasons.append("→ Observations:")
        reasons.extend([f"  • {factor}" for factor in neutral_factors])
    
    # Add ML insight about feature importance
    reasons.append("🔬 ML Insight: The model weighs 'talks to new people' and 'screen time' most heavily in predictions")
    
    # Fallback if somehow no reasons
    if len(reasons) <= 1:
        reasons.append("Balanced lifestyle profile - model sees average characteristics")
    
    return reasons
