import sqlite3
file = "food.db"

def clear_plans():
    conn = sqlite3.connect(file)
    c = conn.cursor()
    c.execute("DELETE FROM Plans")
    conn.commit()
    conn.close()
