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
    
    if find_plan(weekday_id) is not None:
        update_plan(weekday_id, breakfast_id, lunch_id, dinner_id)
    else:
        c.execute("INSERT INTO Plans (weekday_id, breakfast_id, lunch_id, dinner_id) VALUES (?, ?, ?, ?)", (weekday_id, breakfast_id, lunch_id, dinner_id))
    conn.commit()
    conn.close()
    
def update_plan(weekday_id, breakfast_id, lunch_id, dinner_id):
    conn = sqlite3.connect(file)
    c = conn.cursor()
    c.execute("UPDATE Plans SET breakfast_id=?, lunch_id=?, dinner_id=? WHERE weekday_id=?", (breakfast_id, lunch_id, dinner_id, weekday_id))
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

def get_meals():
    conn = sqlite3.connect(file)
    c = conn.cursor()
    c.execute("SELECT * FROM Meals")
    meals = c.fetchall()
    conn.close()
    return meals
    
def find_mealid(meal):
    conn = sqlite3.connect(file)
    c = conn.cursor()
    c.execute("SELECT meal_id FROM Meals WHERE meal_name=?", (meal,))
    meal_id = c.fetchone()[MEALID_INDEX]
    conn.close()
    return meal_id

def find_meal(meal_id):
    conn = sqlite3.connect(file)
    c = conn.cursor()
    c.execute("SELECT meal_name FROM Meals WHERE meal_id=?", (meal_id,))
    meal = c.fetchone()[MEALNAME_INDEX]
    conn.close()
    return meal

def find_plan(weekday_id):
    conn = sqlite3.connect(file)
    c = conn.cursor()
    c.execute("SELECT * FROM Plans WHERE weekday_id=?", (weekday_id,))
    plan = c.fetchone()
    conn.close()
    return plan

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
    
    insert_meal("Hot Dog")
    insert_meal("Hamburger")
    insert_meal("Pizza")
    insert_meal("Taco")
    insert_meal("Burrito")
    
    print(len(get_meals()))
    print(get_meals())
    # clear_meals()
    # clear_plans()   