from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from datetime import datetime
from ml_engine import TrueLovePredictor, explain
import ai_narrator
import os
import io
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree

app = Flask(__name__)
predictor = TrueLovePredictor()

# Color palette matching the UI
COLORS = {
    'primary': '#d3a999',      # dusty rose
    'secondary': '#a5aeb7',    # cool gray-blue
    'text': '#211d1e',         # deep charcoal
    'bg': '#e9e6e1',           # warm cream
    'accent': '#c89784',       # darker rose
}


def fig_to_base64(fig):
    """Convert matplotlib figure to base64 string for HTML embedding"""
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png', bbox_inches='tight', dpi=100,
                facecolor='white', edgecolor='none')
    buffer.seek(0)
    img_str = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close(fig)
    return img_str


def generate_polynomial_curve():
    """Generate polynomial regression curve showing screen_time vs predicted months"""
    if not predictor.is_trained:
        return None

    # Vary screen_time, hold others at average
    screen_times = np.linspace(0, 16, 60)
    months_predictions = []

    for st in screen_times:
        sample = {
            'social_activity': 5,
            'confidence_level': 5,
            'hobbies_count': 3,
            'screen_time': float(st),
            'goes_out_per_week': 3,
            'talks_to_new_people': 5
        }
        pred = predictor.predict(sample)
        months_predictions.append(pred['months'])

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(screen_times, months_predictions, color=COLORS['primary'],
            linewidth=3, label='Polynomial Ridge (degree=2)')
    ax.fill_between(screen_times, months_predictions,
                    alpha=0.2, color=COLORS['primary'])

    # Add markers for key points
    ax.scatter([2, 6, 12], [
        predictor.predict({'social_activity': 5, 'confidence_level': 5, 'hobbies_count': 3,
                           'screen_time': 2, 'goes_out_per_week': 3, 'talks_to_new_people': 5})['months'],
        predictor.predict({'social_activity': 5, 'confidence_level': 5, 'hobbies_count': 3,
                           'screen_time': 6, 'goes_out_per_week': 3, 'talks_to_new_people': 5})['months'],
        predictor.predict({'social_activity': 5, 'confidence_level': 5, 'hobbies_count': 3,
                           'screen_time': 12, 'goes_out_per_week': 3, 'talks_to_new_people': 5})['months'],
    ], color=COLORS['accent'], s=100, zorder=5, edgecolors='white', linewidths=2)

    ax.set_xlabel('Screen Time (hours/day)', fontsize=12, color=COLORS['text'])
    ax.set_ylabel('Predicted Months to Love', fontsize=12, color=COLORS['text'])
    ax.set_title('Polynomial Ridge Regression: How Screen Time Affects Predictions',
                 fontsize=13, color=COLORS['text'], pad=15, fontweight='bold')
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_facecolor('#fafaf8')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(COLORS['secondary'])
    ax.spines['bottom'].set_color(COLORS['secondary'])
    ax.tick_params(colors=COLORS['text'])
    ax.legend(loc='upper left', frameon=False, fontsize=10)

    # Annotation
    ax.annotate('Notice the curve!\n(Not a straight line)',
                xy=(8, months_predictions[30]), xytext=(10, max(months_predictions) * 0.6),
                fontsize=10, color=COLORS['text'],
                arrowprops=dict(arrowstyle='->', color=COLORS['secondary']))

    return fig_to_base64(fig)


def generate_decision_tree_chart():
    """Generate visualization of the actual decision tree structure"""
    if not predictor.is_trained:
        return None

    fig, ax = plt.subplots(figsize=(16, 9))
    feature_names = ['Social', 'Confidence', 'Hobbies', 'Screen', 'GoesOut', 'TalksToNew']

    plot_tree(predictor.tree_model,
              feature_names=feature_names,
              class_names=list(predictor.tree_model.classes_),
              filled=True,
              rounded=True,
              fontsize=9,
              ax=ax,
              proportion=False,
              impurity=False)

    ax.set_title('Decision Tree Structure (Actual sklearn Model)',
                 fontsize=13, color=COLORS['text'], pad=15, fontweight='bold')

    return fig_to_base64(fig)


def generate_feature_interaction_chart():
    """Generate 2D heatmap showing how two features interact"""
    if not predictor.is_trained:
        return None

    # Vary social_activity and screen_time
    social_range = np.arange(1, 11)
    screen_range = np.linspace(0, 14, 15)

    grid = np.zeros((len(social_range), len(screen_range)))

    for i, soc in enumerate(social_range):
        for j, st in enumerate(screen_range):
            sample = {
                'social_activity': int(soc),
                'confidence_level': 5,
                'hobbies_count': 3,
                'screen_time': float(st),
                'goes_out_per_week': 3,
                'talks_to_new_people': 5
            }
            pred = predictor.predict(sample)
            grid[i, j] = pred['months']

    fig, ax = plt.subplots(figsize=(10, 6))
    im = ax.imshow(grid, aspect='auto', origin='lower', cmap='RdYlGn_r',
                   extent=[0, 14, 1, 10])

    ax.set_xlabel('Screen Time (hours/day)', fontsize=12, color=COLORS['text'])
    ax.set_ylabel('Social Activity (1-10)', fontsize=12, color=COLORS['text'])
    ax.set_title('Feature Interaction: Social Activity × Screen Time → Months',
                 fontsize=13, color=COLORS['text'], pad=15, fontweight='bold')

    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Predicted Months', fontsize=11, color=COLORS['text'])

    ax.tick_params(colors=COLORS['text'])

    return fig_to_base64(fig)

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
                             ai_available=ai_narrator.is_available(),
                             validation_warnings=validation_errors if validation_errors else None)
    
    except Exception as e:
        return render_template('index.html', 
                             error=f"Prediction error: {str(e)}")


@app.route('/ai_narrate', methods=['POST'])
def ai_narrate():
    """Generate a playful AI narrative for a prediction (on-demand)."""
    try:
        payload = request.get_json(silent=True) or {}

        # Validate required fields
        required = ['category', 'months', 'social_activity', 'confidence_level',
                    'hobbies_count', 'screen_time', 'goes_out_per_week',
                    'talks_to_new_people']
        for field in required:
            if field not in payload:
                return jsonify({
                    'success': False,
                    'message': f'Missing field: {field}'
                })

        result = ai_narrator.generate_narrative(payload)
        return jsonify(result)

    except Exception as e:
        print(f"[/ai_narrate] Error: {e}")
        return jsonify({
            'success': False,
            'message': ai_narrator.FRIENDLY_FAILURE_MESSAGE
        })


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
    sample_input = None
    sample_category = None
    sample_months = None
    sample_prompt_preview = None
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
        sample_category = sample_pred['category']
        sample_months = sample_pred['months']

        # Build the Stage 3 prompt preview (shows how Stage 1+2 outputs chain into the LLM prompt)
        prompt_payload = {**sample_input,
                          'category': sample_category,
                          'months': sample_months}
        sample_prompt_preview = ai_narrator.build_prompt(prompt_payload)

    # Generate visualization charts
    polynomial_chart = generate_polynomial_curve() if predictor.is_trained else None
    tree_chart = generate_decision_tree_chart() if predictor.is_trained else None
    interaction_chart = generate_feature_interaction_chart() if predictor.is_trained else None

    return render_template('admin.html',
                         record_count=record_count,
                         last_trained=last_trained,
                         tree_accuracy=round(predictor.training_accuracy, 1) if predictor.is_trained else 0,
                         poly_error=round(predictor.training_error, 2) if predictor.is_trained else 0,
                         feature_importance=chart_data,
                         probabilities=sample_probs,
                         model_details=model_details,
                         polynomial_chart=polynomial_chart,
                         tree_chart=tree_chart,
                         interaction_chart=interaction_chart,
                         ai_available=ai_narrator.is_available(),
                         sample_input=sample_input,
                         sample_category=sample_category,
                         sample_months=sample_months,
                         sample_prompt_preview=sample_prompt_preview)

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
