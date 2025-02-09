#!/bin/python3

import sqlite3

file = "food.db"

conn = sqlite3.connect(file)
cur = conn.cursor()

# Create Weekdays table
cur.execute('''
CREATE TABLE IF NOT EXISTS Weekdays (
    weekday_id INTEGER PRIMARY KEY,
    weekday_name TEXT NOT NULL UNIQUE
)
''')

# Create Meals table
cur.execute('''
CREATE TABLE IF NOT EXISTS Meals (
    meal_id INTEGER PRIMARY KEY,
    meal_name TEXT NOT NULL,
    meal_type TEXT NOT NULL
)
''')

# Create Plans table
cur.execute('''
CREATE TABLE IF NOT EXISTS Plans (
    plan_id INTEGER PRIMARY KEY,
    weekday_id INTEGER,
    breakfast_id INTEGER,
    lunch_id INTEGER,
    dinner_id INTEGER,
    FOREIGN KEY (weekday_id) REFERENCES Weekdays(weekday_id),
    FOREIGN KEY (breakfast_id) REFERENCES Meals(meal_id),
    FOREIGN KEY (lunch_id) REFERENCES Meals(meal_id),
    FOREIGN KEY (dinner_id) REFERENCES Meals(meal_id)
)
''')

# Insert weekdays into Weekdays table
cur.executemany('''
INSERT OR IGNORE INTO Weekdays (weekday_id, weekday_name) VALUES (?, ?)
''', [
    (1, 'Monday'),
    (2, 'Tuesday'),
    (3, 'Wednesday'),
    (4, 'Thursday'),
    (5, 'Friday'),
    (6, 'Saturday'),
    (7, 'Sunday')
])

conn.commit()
conn.close()