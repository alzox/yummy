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
    
def update_plan(weekday_id, meal_str, meal_id):
    conn = sqlite3.connect(file)
    c = conn.cursor()
    match meal_str:
        case 'breakfast':
            c.execute("UPDATE Plans SET breakfast_id=? WHERE weekday_id=?", (meal_id, weekday_id))
        case 'lunch':
            c.execute("UPDATE Plans SET lunch_id=? WHERE weekday_id=?", (meal_id, weekday_id))
        case 'dinner':
            c.execute("UPDATE Plans SET dinner_id=? WHERE weekday_id=?", (meal_id, weekday_id))
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
            pass
        else:
            raise
    finally:
        conn.close()
    
"""Find Functions"""

FIRST_ELEMENT = 0

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
    meal_id = c.fetchone()[FIRST_ELEMENT]
    conn.close()
    return meal_id

def find_meal(meal_id):
    conn = sqlite3.connect(file)
    c = conn.cursor()
    c.execute("SELECT meal_name FROM Meals WHERE meal_id=?", (meal_id,))
    meal = c.fetchone()[0]
    conn.close()
    return meal

def find_plan(weekday_id):
    conn = sqlite3.connect(file)
    c = conn.cursor()
    c.execute("SELECT * FROM Plans WHERE weekday_id=?", (weekday_id,))
    plan = c.fetchone()
    conn.close()
    return plan

"""Aggregate Functions"""

def export_plans():
    conn = sqlite3.connect(file)
    c = conn.cursor()
    # Left Join to get the meal names for all breakfast, lunch, dinner ids and Left Join weekday_id to get the weekday name
    c.execute("SELECT Weekdays.weekday_name, Meals.meal_name, Meals2.meal_name, Meals3.meal_name FROM Plans LEFT JOIN Meals ON Plans.breakfast_id = Meals.meal_id LEFT JOIN Meals Meals2 ON Plans.lunch_id = Meals2.meal_id LEFT JOIN Meals Meals3 ON Plans.dinner_id = Meals3.meal_id LEFT JOIN Weekdays ON Plans.weekday_id = Weekdays.weekday_id")
    plans = c.fetchall()
    conn.close()
    return plans

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