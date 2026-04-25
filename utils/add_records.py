import sqlite3

def add_keep_trying_records():
    """Add 20 'Keep Trying' records to balance the database"""
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    records = [
        (1, 2, 0, 14.5, 0, 1, 'Keep Trying', 48.5),
        (2, 3, 1, 12.0, 0, 2, 'Keep Trying', 36.2),
        (1, 1, 0, 16.2, 0, 1, 'Keep Trying', 60.0),
        (3, 4, 2, 10.5, 1, 2, 'Keep Trying', 32.4),
        (2, 2, 0, 13.8, 0, 1, 'Keep Trying', 42.1),
        (1, 3, 1, 11.5, 0, 1, 'Keep Trying', 38.9),
        (2, 1, 0, 15.0, 0, 1, 'Keep Trying', 55.3),
        (3, 2, 1, 12.2, 0, 2, 'Keep Trying', 35.0),
        (1, 4, 0, 14.1, 0, 1, 'Keep Trying', 45.6),
        (2, 2, 1, 13.0, 1, 2, 'Keep Trying', 39.5),
        (1, 1, 0, 15.5, 0, 1, 'Keep Trying', 58.2),
        (2, 3, 2, 11.8, 0, 2, 'Keep Trying', 34.7),
        (3, 1, 0, 14.7, 0, 1, 'Keep Trying', 47.8),
        (1, 2, 1, 13.4, 0, 2, 'Keep Trying', 41.2),
        (2, 4, 0, 12.5, 0, 1, 'Keep Trying', 37.1),
        (1, 1, 0, 16.8, 0, 1, 'Keep Trying', 65.0),
        (3, 2, 1, 11.2, 1, 2, 'Keep Trying', 31.5),
        (2, 3, 0, 14.0, 0, 1, 'Keep Trying', 44.4),
        (1, 2, 0, 15.2, 0, 1, 'Keep Trying', 52.9),
        (2, 1, 1, 13.6, 0, 1, 'Keep Trying', 49.1)
    ]
    
    for record in records:
        cursor.execute('''
            INSERT INTO dating_profile 
            (social_activity, confidence_level, hobbies_count, screen_time, 
             goes_out_per_week, talks_to_new_people, outcome, months_to_love)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', record)
    
    conn.commit()
    
    cursor.execute('SELECT COUNT(*) FROM dating_profile')
    count = cursor.fetchone()[0]
    
    conn.close()
    print(f"[OK] Added 20 records. Total now: {count}")

if __name__ == '__main__':
    add_keep_trying_records()
