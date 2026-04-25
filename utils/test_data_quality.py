import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def analyze_dataset():
    """Analyze data.csv for outliers and distribution issues"""
    
    print("=" * 60)
    print("DATA QUALITY ANALYSIS")
    print("=" * 60)
    
    # Load data
    df = pd.read_csv('data.csv')
    print(f"\n1. DATASET SIZE: {len(df)} records\n")
    
    # Check outcome distribution
    print("2. OUTCOME DISTRIBUTION:")
    print("-" * 40)
    outcome_counts = df['outcome'].value_counts()
    for outcome, count in outcome_counts.items():
        percentage = (count / len(df)) * 100
        print(f"   {outcome:15s}: {count:3d} ({percentage:5.1f}%)")
    
    # Check for class imbalance
    max_count = outcome_counts.max()
    min_count = outcome_counts.min()
    imbalance_ratio = max_count / min_count
    print(f"\n   Imbalance Ratio: {imbalance_ratio:.2f}x")
    if imbalance_ratio > 3:
        print("   [WARNING] Significant class imbalance detected!")
    else:
        print("   [OK] Classes are reasonably balanced")
    
    # Feature statistics
    print("\n3. FEATURE STATISTICS:")
    print("-" * 40)
    features = ['social_activity', 'confidence_level', 'hobbies_count', 
                'screen_time', 'goes_out_per_week', 'talks_to_new_people']
    
    for feature in features:
        mean = df[feature].mean()
        std = df[feature].std()
        min_val = df[feature].min()
        max_val = df[feature].max()
        print(f"   {feature:20s}: mean={mean:5.2f}, std={std:5.2f}, range=[{min_val:5.1f}, {max_val:5.1f}]")
    
    # Check for outliers using IQR method
    print("\n4. OUTLIER DETECTION (IQR Method):")
    print("-" * 40)
    outlier_indices = set()
    
    for feature in features:
        Q1 = df[feature].quantile(0.25)
        Q3 = df[feature].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = df[(df[feature] < lower_bound) | (df[feature] > upper_bound)]
        if len(outliers) > 0:
            print(f"   {feature:20s}: {len(outliers)} outliers")
            outlier_indices.update(outliers.index.tolist())
        else:
            print(f"   {feature:20s}: No outliers")
    
    # Check months_to_love distribution
    print("\n5. TARGET VARIABLE (months_to_love):")
    print("-" * 40)
    print(f"   Mean: {df['months_to_love'].mean():.2f} months")
    print(f"   Median: {df['months_to_love'].median():.2f} months")
    print(f"   Std Dev: {df['months_to_love'].std():.2f} months")
    print(f"   Range: [{df['months_to_love'].min():.1f}, {df['months_to_love'].max():.1f}]")
    
    # Check for extreme values
    extreme_high = df[df['months_to_love'] > 50]
    extreme_low = df[df['months_to_love'] < 2]
    print(f"\n   Records > 50 months: {len(extreme_high)}")
    print(f"   Records < 2 months: {len(extreme_low)}")
    
    # Correlation with outcome
    print("\n6. MONTHS BY OUTCOME CATEGORY:")
    print("-" * 40)
    for outcome in df['outcome'].unique():
        subset = df[df['outcome'] == outcome]['months_to_love']
        print(f"   {outcome:15s}: mean={subset.mean():5.1f}, range=[{subset.min():5.1f}, {subset.max():5.1f}]")
    
    # Check for data quality issues
    print("\n7. DATA QUALITY CHECKS:")
    print("-" * 40)
    
    # Missing values
    missing = df.isnull().sum().sum()
    print(f"   Missing values: {missing}")
    
    # Duplicate rows
    duplicates = df.duplicated().sum()
    print(f"   Duplicate rows: {duplicates}")
    
    # Feature range violations
    violations = 0
    if (df['social_activity'] < 1).any() or (df['social_activity'] > 10).any():
        violations += 1
        print("   [WARNING] social_activity out of range [1-10]")
    if (df['confidence_level'] < 1).any() or (df['confidence_level'] > 10).any():
        violations += 1
        print("   [WARNING] confidence_level out of range [1-10]")
    if (df['talks_to_new_people'] < 1).any() or (df['talks_to_new_people'] > 10).any():
        violations += 1
        print("   [WARNING] talks_to_new_people out of range [1-10]")
    
    if violations == 0:
        print("   [OK] All features within expected ranges")
    
    print("\n" + "=" * 60)
    print("RECOMMENDATIONS:")
    print("=" * 60)
    
    if imbalance_ratio > 3:
        print("• Consider adding more records to underrepresented categories")
    
    if len(outlier_indices) > 5:
        print(f"• Review {len(outlier_indices)} records with outlier values")
    
    if df['months_to_love'].std() > 15:
        print("• High variance in target variable - consider data normalization")
    
    print("\n")

def test_predictions():
    """Test edge cases to check for model skew"""
    from ml_engine import TrueLovePredictor
    
    print("=" * 60)
    print("EDGE CASE PREDICTION TESTS")
    print("=" * 60)
    
    predictor = TrueLovePredictor()
    
    # Train if not already trained
    if not predictor.is_trained:
        print("\nTraining models...")
        predictor.train('data.csv')
    
    test_cases = [
        {
            'name': 'Perfect Social Profile',
            'data': {'social_activity': 10, 'confidence_level': 10, 'hobbies_count': 8, 
                    'screen_time': 2, 'goes_out_per_week': 7, 'talks_to_new_people': 10}
        },
        {
            'name': 'Worst Case Scenario',
            'data': {'social_activity': 1, 'confidence_level': 1, 'hobbies_count': 0, 
                    'screen_time': 16, 'goes_out_per_week': 0, 'talks_to_new_people': 1}
        },
        {
            'name': 'Average Profile',
            'data': {'social_activity': 5, 'confidence_level': 5, 'hobbies_count': 3, 
                    'screen_time': 6, 'goes_out_per_week': 3, 'talks_to_new_people': 5}
        },
        {
            'name': 'High Screen Time Only',
            'data': {'social_activity': 7, 'confidence_level': 7, 'hobbies_count': 5, 
                    'screen_time': 14, 'goes_out_per_week': 4, 'talks_to_new_people': 6}
        },
        {
            'name': 'Social but Lazy',
            'data': {'social_activity': 8, 'confidence_level': 8, 'hobbies_count': 2, 
                    'screen_time': 8, 'goes_out_per_week': 1, 'talks_to_new_people': 9}
        }
    ]
    
    print("\nTest Results:")
    print("-" * 60)
    
    for test in test_cases:
        result = predictor.predict(test['data'])
        print(f"\n{test['name']}:")
        print(f"  Category: {result['category']}")
        print(f"  Months: {result['months']}")
        print(f"  Probabilities: {result['probabilities']}")
    
    print("\n" + "=" * 60)

if __name__ == '__main__':
    analyze_dataset()
    print("\n")
    test_predictions()
