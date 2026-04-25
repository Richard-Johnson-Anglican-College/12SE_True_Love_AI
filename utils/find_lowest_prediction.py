import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml_engine import TrueLovePredictor

predictor = TrueLovePredictor()
data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data.csv')
predictor.train(data_path)

print("Searching for combinations that give < 2.1 months...")
print("=" * 60)

results = []

# Test all high-performing combinations
for social in range(8, 11):
    for conf in range(8, 11):
        for hobbies in range(6, 11):
            for screen in [0.5, 1.0, 1.5, 2.0]:
                for goes_out in range(6, 8):
                    for talks in range(9, 11):
                        test = {
                            'social_activity': social,
                            'confidence_level': conf,
                            'hobbies_count': hobbies,
                            'screen_time': screen,
                            'goes_out_per_week': goes_out,
                            'talks_to_new_people': talks
                        }
                        pred = predictor.predict(test)
                        if pred['months'] < 2.1:
                            results.append((pred['months'], test))

# Sort by months (first element of tuple)
results.sort(key=lambda x: x[0])

print(f"\nFound {len(results)} combinations under 2.1 months\n")
print("Top 10 LOWEST predictions:")
print("-" * 60)

for i, (months, test) in enumerate(results[:10], 1):
    print(f"\n{i}. {months:.2f} months")
    print(f"   Social: {test['social_activity']}, Confidence: {test['confidence_level']}, Hobbies: {test['hobbies_count']}")
    print(f"   Screen: {test['screen_time']} hrs, Goes Out: {test['goes_out_per_week']}x, Talks: {test['talks_to_new_people']}")

if results:
    print("\n" + "=" * 60)
    print("ABSOLUTE LOWEST PREDICTION:")
    print("=" * 60)
    lowest_months, lowest_test = results[0]
    print(f"\n{lowest_months:.2f} months")
    print(f"Social Activity: {lowest_test['social_activity']}/10")
    print(f"Confidence: {lowest_test['confidence_level']}/10")
    print(f"Hobbies: {lowest_test['hobbies_count']}")
    print(f"Screen Time: {lowest_test['screen_time']} hours/day")
    print(f"Goes Out: {lowest_test['goes_out_per_week']}x per week")
    print(f"Talks to New People: {lowest_test['talks_to_new_people']}/10")
else:
    print("\nNo combinations found under 2.1 months with these parameters.")
    print("The model's minimum prediction appears to be around 2.1 months.")
