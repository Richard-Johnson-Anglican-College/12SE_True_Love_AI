from flask import Flask, render_template, request, jsonify
import pandas as pd
from datetime import datetime
from ml_engine import TrueLovePredictor, explain
import os

app = Flask(__name__)
predictor = TrueLovePredictor()

def get_csv_record_count():
    """Get record count from CSV file"""
    if os.path.exists('data.csv'):
        df = pd.read_csv('data.csv')
        return len(df)
    return 0

@app.route('/')
def index():
    """Main prediction page"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handle prediction request"""
    try:
        # Get raw input
        data = {
            'social_activity': int(request.form.get('social_activity', 5)),
            'confidence_level': int(request.form.get('confidence_level', 5)),
            'hobbies_count': int(request.form.get('hobbies_count', 3)),
            'screen_time': float(request.form.get('screen_time', 4)),
            'goes_out_per_week': int(request.form.get('goes_out_per_week', 2)),
            'talks_to_new_people': int(request.form.get('talks_to_new_people', 5))
        }
        
        # Validate and cap inputs to realistic ranges
        validation_errors = []
        
        if not (1 <= data['social_activity'] <= 10):
            validation_errors.append("Social Activity must be between 1-10")
            data['social_activity'] = max(1, min(10, data['social_activity']))
        
        if not (1 <= data['confidence_level'] <= 10):
            validation_errors.append("Confidence Level must be between 1-10")
            data['confidence_level'] = max(1, min(10, data['confidence_level']))
        
        if not (0 <= data['hobbies_count'] <= 10):
            validation_errors.append("Hobbies must be between 0-10 (capped at 10 for realism)")
            data['hobbies_count'] = max(0, min(10, data['hobbies_count']))
        
        if not (0 <= data['screen_time'] <= 24):
            validation_errors.append("Screen Time must be between 0-24 hours")
            data['screen_time'] = max(0, min(24, data['screen_time']))
        
        if not (0 <= data['goes_out_per_week'] <= 7):
            validation_errors.append("Goes Out must be between 0-7 days")
            data['goes_out_per_week'] = max(0, min(7, data['goes_out_per_week']))
        
        if not (1 <= data['talks_to_new_people'] <= 10):
            validation_errors.append("Talks to New People must be between 1-10")
            data['talks_to_new_people'] = max(1, min(10, data['talks_to_new_people']))
        
        # Warning for unrealistic combinations
        if data['hobbies_count'] >= 8:
            validation_errors.append("Warning: 8+ hobbies may leave little time for dating!")
        
        if data['screen_time'] > 12:
            validation_errors.append("Warning: 12+ hours screen time detected!")
        
        if not predictor.is_trained:
            if os.path.exists('models.pkl'):
                predictor.load_models()
            else:
                if os.path.exists('data.csv'):
                    predictor.train('data.csv')
                    predictor.save_models()
                else:
                    raise ValueError("No training data found. Please ensure data.csv exists.")
        
        prediction = predictor.predict(data)
        reasons = explain(data, prediction)
        
        return render_template('index.html', 
                             prediction=prediction,
                             reasons=reasons,
                             form_data=data,
                             validation_warnings=validation_errors if validation_errors else None)
    
    except Exception as e:
        return render_template('index.html', 
                             error=f"Prediction error: {str(e)}")

@app.route('/admin')
def admin():
    """Admin dashboard with metrics and visualizations"""
    record_count = get_csv_record_count()
    
    if not predictor.is_trained:
        if os.path.exists('models.pkl'):
            predictor.load_models()
        else:
            if record_count > 0 and os.path.exists('data.csv'):
                predictor.train('data.csv')
                predictor.save_models()
    
    last_trained = "Never"
    if os.path.exists('models.pkl'):
        timestamp = os.path.getmtime('models.pkl')
        dt = datetime.fromtimestamp(timestamp)
        last_trained = dt.strftime('%Y-%m-%d %H:%M')
    
    feature_importance = predictor.feature_importance if predictor.is_trained else {}
    
    sorted_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
    
    feature_labels = {
        'social_activity': 'Social Activity',
        'confidence_level': 'Confidence Level',
        'hobbies_count': 'Hobbies Count',
        'screen_time': 'Screen Time',
        'goes_out_per_week': 'Goes Out Per Week',
        'talks_to_new_people': 'Talks to New People'
    }
    
    chart_data = [
        {
            'label': feature_labels.get(name, name),
            'value': round(importance, 2)
        }
        for name, importance in sorted_features
    ]
    
    # Get actual model parameters to prove ML is real
    model_details = {}
    if predictor.is_trained:
        # Decision Tree details
        tree = predictor.tree_model
        model_details['tree'] = {
            'max_depth': tree.max_depth,
            'min_samples_leaf': tree.min_samples_leaf,
            'n_leaves': tree.get_n_leaves(),
            'n_nodes': tree.tree_.node_count,
            'classes': list(tree.classes_)
        }
        
        # Polynomial Ridge details
        poly_pipeline = predictor.poly_model
        ridge = poly_pipeline.named_steps['ridge']
        poly_features = poly_pipeline.named_steps['polynomialfeatures']
        model_details['ridge'] = {
            'degree': poly_features.degree,
            'alpha': ridge.alpha,
            'n_features_in': ridge.n_features_in_,
            'n_features_out': poly_features.n_output_features_
        }
    
    # Sample prediction to show probabilities (using average profile for mixed probabilities)
    sample_probs = None
    if predictor.is_trained:
        sample_input = {
            'social_activity': 5,
            'confidence_level': 5,
            'hobbies_count': 3,
            'screen_time': 6,
            'goes_out_per_week': 3,
            'talks_to_new_people': 5
        }
        sample_pred = predictor.predict(sample_input)
        sample_probs = {k: round(v * 100, 1) for k, v in sample_pred['probabilities'].items()}
    
    return render_template('admin.html',
                         record_count=record_count,
                         last_trained=last_trained,
                         tree_accuracy=round(predictor.training_accuracy, 1) if predictor.is_trained else 0,
                         poly_error=round(predictor.training_error, 2) if predictor.is_trained else 0,
                         feature_importance=chart_data,
                         probabilities=sample_probs,
                         model_details=model_details)

@app.route('/retrain', methods=['POST'])
def retrain():
    """Retrain models with current CSV data"""
    try:
        record_count = get_csv_record_count()
        
        if record_count < 10:
            return jsonify({
                'success': False,
                'message': f'Not enough data to train. Need at least 10 records, have {record_count}.'
            })
        
        metrics = predictor.train('data.csv')
        predictor.save_models()
        
        return jsonify({
            'success': True,
            'message': f'Models retrained successfully with {record_count} records!',
            'metrics': metrics
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Training failed: {str(e)}'
        })

if __name__ == '__main__':
    if not os.path.exists('data.csv'):
        print("Training data not found!")
        print("Please ensure data.csv exists in the project directory")
        print("You can run 'python seed_data.py' to generate sample data")
    else:
        print(f"[OK] Found data.csv with {get_csv_record_count()} records")
        app.run(debug=True, port=5000)
