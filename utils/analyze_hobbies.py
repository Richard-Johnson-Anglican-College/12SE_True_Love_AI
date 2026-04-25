import pandas as pd

df = pd.read_csv('data.csv')

print("=" * 60)
print("HOBBIES ANALYSIS BY OUTCOME")
print("=" * 60)

for outcome in ['Very Soon', 'Soon', 'Eventually', 'Keep Trying']:
    subset = df[df['outcome'] == outcome]
    if len(subset) > 0:
        print(f"\n{outcome}:")
        print(f"  Count: {len(subset)} records")
        print(f"  Hobbies - Mean: {subset['hobbies_count'].mean():.1f}, Median: {subset['hobbies_count'].median():.0f}")
        print(f"  Range: {subset['hobbies_count'].min():.0f} - {subset['hobbies_count'].max():.0f}")
        print(f"  Distribution: {dict(subset['hobbies_count'].value_counts().sort_index())}")

print("\n" + "=" * 60)
print("SWEET SPOT ANALYSIS")
print("=" * 60)

very_soon = df[df['outcome'] == 'Very Soon']
print(f"\nFor 'Very Soon' predictions:")
print(f"  Most common hobbies: {very_soon['hobbies_count'].mode().values}")
print(f"  Average hobbies: {very_soon['hobbies_count'].mean():.1f}")
print(f"  Median hobbies: {very_soon['hobbies_count'].median():.0f}")

print("\nFull 'Very Soon' profiles:")
print(very_soon[['social_activity', 'confidence_level', 'hobbies_count', 
                 'screen_time', 'goes_out_per_week', 'talks_to_new_people', 'months_to_love']].to_string())
