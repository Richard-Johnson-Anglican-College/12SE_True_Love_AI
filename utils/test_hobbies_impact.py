"""Quick test: does hobbies_count actually affect predictions?"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ml_engine import TrueLovePredictor

p = TrueLovePredictor()
p.load_models()

print('=' * 60)
print('DECISION TREE FEATURE IMPORTANCE:')
print('=' * 60)
for k, v in sorted(p.feature_importance.items(), key=lambda x: -x[1]):
    print(f'  {k:25s}: {v:.4f} ({v*100:.1f}%)')

print()
print('=' * 60)
print('POLYNOMIAL RIDGE - Vary Hobbies Only (others held constant):')
print('=' * 60)
base = {
    'social_activity': 5,
    'confidence_level': 5,
    'hobbies_count': 0,
    'screen_time': 6,
    'goes_out_per_week': 3,
    'talks_to_new_people': 5,
}
for h in [0, 1, 2, 3, 4, 5, 6, 8, 10]:
    pred = p.predict({**base, 'hobbies_count': h})
    print(f'  hobbies={h:2d}: {pred["months"]:.2f} months | {pred["category"]}')
