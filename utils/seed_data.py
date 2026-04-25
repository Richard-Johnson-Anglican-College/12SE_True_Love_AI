import sqlite3
import random

def init_database():
    """Initialize SQLite database with dating_profile table"""
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dating_profile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            social_activity INTEGER,
            confidence_level INTEGER,
            hobbies_count INTEGER,
            screen_time REAL,
            goes_out_per_week INTEGER,
            talks_to_new_people INTEGER,
            outcome TEXT,
            months_to_love REAL
        )
    ''')
    
    conn.commit()
    conn.close()
    print("[OK] Database initialized")

def generate_seed_data(num_records=60):
    """Generate realistic training data with varied outcomes"""
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM dating_profile')
    
    outcomes = ['Very Soon', 'Soon', 'Eventually', 'Keep Trying']
    
    for i in range(num_records):
        social_activity = random.randint(1, 10)
        confidence_level = random.randint(1, 10)
        hobbies_count = random.randint(0, 8)
        screen_time = round(random.uniform(1, 12), 1)
        goes_out_per_week = random.randint(0, 7)
        talks_to_new_people = random.randint(1, 10)
        
        social_score = (social_activity + confidence_level + talks_to_new_people) / 3
        activity_score = (goes_out_per_week * 1.5) + (hobbies_count * 0.5)
        penalty = screen_time * 0.3
        
        total_score = social_score + activity_score - penalty
        
        if total_score > 15:
            outcome = 'Very Soon'
            months = round(random.uniform(1, 4), 1)
        elif total_score > 10:
            outcome = 'Soon'
            months = round(random.uniform(4, 8), 1)
        elif total_score > 6:
            outcome = 'Eventually'
            months = round(random.uniform(8, 15), 1)
        else:
            outcome = 'Keep Trying'
            months = round(random.uniform(15, 30), 1)
        
        noise = random.uniform(-0.8, 0.8)
        months = max(1, months + noise)
        
        if random.random() < 0.15:
            outcome = random.choice(outcomes)
            months = round(random.uniform(1, 25), 1)
        
        name = f"Person {i+1}" if random.random() < 0.3 else ""
        
        cursor.execute('''
            INSERT INTO dating_profile 
            (name, social_activity, confidence_level, hobbies_count, 
             screen_time, goes_out_per_week, talks_to_new_people, outcome, months_to_love)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, social_activity, confidence_level, hobbies_count, 
              screen_time, goes_out_per_week, talks_to_new_people, outcome, months))
    
    conn.commit()
    conn.close()
    print(f"[OK] Generated {num_records} training records")

if __name__ == '__main__':
    init_database()
    generate_seed_data(60)
    print("\n[SUCCESS] Database seeded successfully!")
