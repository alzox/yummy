import sqlite3
file = r"C:\Users\commo\OneDrive - University of Virginia\School\STEM\CS\alzox\yummy\food.db"
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
    
def edit_plan(weekday_id, meal_str, meal_id):
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
        
        
def edit_meal(meal_id, meal):
    conn = sqlite3.connect(file)
    c = conn.cursor()
    c.execute("UPDATE Meals SET meal_name=? WHERE meal_id=?", (meal, meal_id))
    conn.commit()
    conn.close()
    
def insert_grocery(meal_id, grocery, quantity):
    conn = sqlite3.connect(file)
    c = conn.cursor()
    c.execute("INSERT INTO Groceries (meal_id, grocery_name, grocery_qty) VALUES (?,?,?)", (meal_id, grocery, quantity))
    conn.commit()
    conn.close()
    
def edit_grocery(grocery_id, grocery, quantity):
    conn = sqlite3.connect(file)
    c = conn.cursor()
    c.execute("UPDATE Groceries SET grocery_name=?, grocery_qty=? WHERE grocery_id=?", (grocery, quantity, grocery_id))
    conn.commit()
    conn.close()
    
"""Delete Functions"""

def delete_meal(meal_id):
    conn = sqlite3.connect(file)
    c = conn.cursor()
    c.execute("DELETE FROM Meals WHERE meal_id=?", (meal_id,))
    conn.commit()
    conn.close()
    
def delete_grocery(grocery_id):
    conn = sqlite3.connect(file)
    c = conn.cursor()
    c.execute("DELETE FROM Groceries WHERE grocery_id=?", (grocery_id,))
    conn.commit()
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

def get_planner_meals():
    conn = sqlite3.connect(file)
    c = conn.cursor()
    c.execute("SELECT * FROM Meals WHERE meal_id IN (SELECT breakfast_id FROM Plans UNION SELECT lunch_id FROM Plans UNION SELECT dinner_id FROM Plans)")
    meals = c.fetchall()
    conn.close()
    return meals

def get_groceries(meal_id):
    conn = sqlite3.connect(file)
    c = conn.cursor()
    c.execute("SELECT * FROM Groceries WHERE meal_id=?", (meal_id,))
    groceries = c.fetchall()
    conn.close()
    return groceries
    
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

def find_plan_print(weekday_id):
    conn = sqlite3.connect(file)
    c = conn.cursor()
    # select plans but now join with meals to get the meal names
    c.execute("SELECT Meals.meal_name, Meals2.meal_name, Meals3.meal_name FROM Plans LEFT JOIN Meals ON Plans.breakfast_id = Meals.meal_id LEFT JOIN Meals Meals2 ON Plans.lunch_id = Meals2.meal_id LEFT JOIN Meals Meals3 ON Plans.dinner_id = Meals3.meal_id WHERE Plans.weekday_id = (?)", (weekday_id,))
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


"""Summary Functions"""

def summary():
    conn = sqlite3.connect(file)
    c = conn.cursor()
    c.execute("SELECT * FROM Meals")
    meals = c.fetchall()
    c.execute("SELECT * FROM Plans")
    plans = c.fetchall()
    c.execute("SELECT * FROM Groceries")
    groceries = c.fetchall()
    conn.close()
    return meals, plans, groceries

if __name__ == "__main__":
    find_plan_print(1)