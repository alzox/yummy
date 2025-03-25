#!/usr/bin/env python3

import sqlite3
import os

file = "food.db"

if os.path.exists(file):
    os.remove(file)
    with open(file, 'w') as f:
        pass
else:
    with open(file, 'w') as f:
        pass

conn = sqlite3.connect(file)
cur = conn.cursor()

# Clear tables
cur.execute('DROP TABLE IF EXISTS Weekdays')
cur.execute('DROP TABLE IF EXISTS Meals')
cur.execute('DROP TABLE IF EXISTS Plans')
cur.execute('DROP TABLE IF EXISTS Groceries')

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
    meal_name TEXT NOT NULL UNIQUE
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

# Create Groceries table
cur.execute('''
CREATE TABLE IF NOT EXISTS Groceries (
    grocery_id INTEGER PRIMARY KEY,
    grocery_name TEXT NOT NULL UNIQUE,
    grocery_qty INTEGER NOT NULL,
    meal_id INTEGER,
    FOREIGN KEY (meal_id) REFERENCES Meals(meal_id)
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

# Initialize Plans to NULL
cur.executemany('''
INSERT INTO Plans (weekday_id, breakfast_id, lunch_id, dinner_id) VALUES (?, ?, ?, ?)
''', [
    (1, None, None, None),
    (2, None, None, None),
    (3, None, None, None),
    (4, None, None, None),
    (5, None, None, None),
    (6, None, None, None),
    (7, None, None, None)
])

conn.commit()
conn.close()