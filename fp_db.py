import sqlite3
file = "food.db"

"""Clear Functions"""

def clear_plans():
    conn = sqlite3.connect(file)
    c = conn.cursor()
    c.execute("DELETE FROM Plans")
    conn.commit()
    conn.close()
    
def clear_meals():
    conn = sqlite3.connect(file)
    c = conn.cursor()
    c.execute("DELETE FROM Meals")
    conn.commit()
    conn.close()
    
"""Insert Functions"""

def insert_plan(weekday_id, breakfast_id, lunch_id, dinner_id):
    conn = sqlite3.connect(file)
    c = conn.cursor()
    c.execute("INSERT INTO Plans (weekday_id, breakfast_id, lunch_id, dinner_id) VALUES (?, ?, ?, ?)", (weekday_id, breakfast_id, lunch_id, dinner_id))
    conn.commit()
    conn.close()
    
def insert_meal(meal):
    conn = sqlite3.connect(file)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO Meals (meal_name) VALUES (?)", (meal,))
        conn.commit()
    except sqlite3.IntegrityError as e:
        if 'UNIQUE constraint failed' in str(e):
            print(f"Error: The meal '{meal}' already exists.")
        else:
            raise
    finally:
        conn.close()
    
"""Find Functions"""

MEALID_INDEX = 0
MEALNAME_INDEX = 1
    
def find_mealid(meal):
    conn = sqlite3.connect(file)
    c = conn.cursor()
    c.execute("SELECT meal_id FROM Meals WHERE meal_name=?", (meal,))
    meal_id = c.fetchone()[MEALID_INDEX]
    conn.close()
    return meal_id

if __name__ == "__main__":
    clear_plans()
    clear_meals()
    insert_plan(1, 1, 2, 3)
    insert_meal("Chicken Alfredo")
    insert_meal("Spaghetti Carbonara")
    insert_meal("Chicken Parmesan")
    insert_meal("Chicken Marsala")
    insert_meal("Chicken Piccata")
    print(find_mealid("Chicken Alfredo"))
    print(find_mealid("Spaghetti Carbonara"))
    print(find_mealid("Chicken Parmesan"))
    print(find_mealid("Chicken Marsala"))
    print(find_mealid("Chicken Piccata"))
    clear_meals()
    clear_plans()   