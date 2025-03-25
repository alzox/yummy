import json
import requests
import os

from msvcrt import getch

try:
    from . import yummy_db as db
    from .yummy_utils import (
        MEALS, WEEKDAYS_LOWER, 
        pressed_arrow_key, pressed_up_arrow, pressed_down_arrow,
        clear_terminal, weekday_to_index, index_page,
        print_plan, print_meals, print_page_groceries, print_page_meals)
except ImportError:
    import src.yummy_db as db
    from src.yummy_utils import (
        MEALS, WEEKDAYS_LOWER, 
        pressed_arrow_key, pressed_up_arrow, pressed_down_arrow,
        clear_terminal, weekday_to_index, index_page,
        print_plan, print_meals, print_page_groceries, print_page_meals)

# --- PATHS ---

JSON_PATH = os.getcwd() + '/docs/plans.json'
GROCERY_PATH = os.getcwd() + '/docs/grocery.csv'


# --- FUNCTIONS ---

def plan(weekday):
    'Plan a day:  PLAN day_of_week'
    index = 0
    while True:
        db_plan = db.find_plan_print(weekday_to_index(weekday))
        clear_terminal()
        print_plan(db_plan, index, weekday)
        
        key = getch()
        
        match key:
            case b'\xe0':
                key = getch()
                if pressed_up_arrow(key):
                    if index == 0:
                        index = 2
                    else:
                        index -= 1
                elif pressed_down_arrow(key):
                    if index == 2:
                        index = 0
                    else:
                        index += 1
            case b'q': 
                return
            case b'\r':
                meal = input(f'What\'s for {MEALS[index]}? ("idk" to use db): ')
                
                if meal == 'idk':
                    meal = meal_select()
                
                if meal is None:
                    continue
                else:
                    db.insert_meal(meal)
                    db.edit_plan(weekday_to_index(weekday), MEALS[index], db.find_mealid(meal))
                    continue 

def show(weekday='all'):
    'Show the current plan:  SHOW'
    print('\n')
    if weekday == 'all':
        print_plan_all() #!STUBBED, print all plans in db
    else:
        plan = db.find_plan_print(weekday_to_index(weekday))
        print_meals(weekday, plan)
    print('\n')
   
def db_summary():
    'Show a summary of the database:  DB_SUMMARY'
    meals, plans, groceries = db.summary()
    print(f'Meals Table Summary: Rows: {meals}, Columns: 2')
    print(f'Plans Table Summary: Rows: {plans}, Columns: 4')
    print(f'Groceries Table Summary: Rows: {groceries}, Columns: 3')
    
    meals_planned = 0
    for plan in db.get_planner_meals():
        for meal in plan[1:]:
            if meal:
                meals_planned += 1
    
    print(f'Meals Planned: {meals_planned}/21!\n')
    
 
def db_meals():
    'Show and edit the current meals:  DB_MEALS'
    actions = {
        b'\r': lambda: db.edit_meal(
            DATA[DATA_INDEX][0], 
            input(f'Edit {DATA[DATA_INDEX][1]}: ')
        ),
        b'd': lambda: db.delete_meal(DATA[DATA_INDEX][0]),
        b'a': lambda: db.insert_meal(input('Add meal: '))
    }

    viewer = DBViewer(db, 'meals', match=actions)
    viewer.view()
     
def grocery():
    'View all meals and edit their groceries status:  GROCERY'
    grocery_actions = {
        b'\r': lambda: db.edit_grocery(
            DATA[DATA_INDEX][0],
            input(f'Edit {DATA[DATA_INDEX][1]} Name: '),
            input(f'Edit {DATA[DATA_INDEX][1]} Quantity: ')),
        b'd': lambda: db.delete_grocery(DATA[DATA_INDEX][0]),
        b'a': lambda: db.insert_grocery(SELECTION, input('Add grocery: '), input('Add quantity: '))
    }
    
    
        
    actions = {
        b'\r': lambda: (DBViewer(db, 'grocery', match=grocery_actions, print_func=print_page_groceries).view())
    }
    viewer = DBViewer(db, 'planner', match=actions)
    viewer.view()

# --- IMPORT/EXPORT FUNCTIONS ---
#! is there a way to auto gen schemas so there doesn't need to be duplicate code?

def import_json(file): #* the file should be in the format: meals, plans
    'Import meals from JSON:  IMPORT_JSON file'
    data = json.load(open(file))
    
    for meal_obj in data['meals']:
        db.insert_meal(meal_obj['name'])
    print('Meals imported from JSON')
    
    for plan_obj in data['plans']:
        db.edit_plan(weekday_to_index(plan_obj['weekday']), 'breakfast', plan_obj['breakfast'])
        db.edit_plan(weekday_to_index(plan_obj['weekday']), 'lunch', plan_obj['lunch'])
        db.edit_plan(weekday_to_index(plan_obj['weekday']), 'dinner', plan_obj['dinner'])
    print('Plans imported from JSON')
    
    print('Import complete\n')
    
def import_json_url(url):
    'Import meals from JSON:  IMPORT_JSON_URL url'
    data = requests.get(url).json()
    
    for meal_obj in data['meals']:
        db.insert_meal(meal_obj['name'])
    print('Meals imported from JSON')
    
    for plan_obj in data['plans']:
        db.edit_plan(weekday_to_index(plan_obj['weekday']), 'breakfast', plan_obj['breakfast'])
        db.edit_plan(weekday_to_index(plan_obj['weekday']), 'lunch', plan_obj['lunch'])
        db.edit_plan(weekday_to_index(plan_obj['weekday']), 'dinner', plan_obj['dinner'])
    print('Plans imported from JSON')
    
    print('Import complete\n')
    
def export_plans_json():
    'Export plans to JSON'
    print('Exporting plans to JSON')

    plans = db.export_plans()
    plans_arr = [{'weekday': plan[0], 'breakfast': plan[1], 'lunch': plan[2], 'dinner': plan[3]} for plan in plans]
    meals = db.get_meals()
    meals_arr = [{'id': meal[0], 'name': meal[1]} for meal in meals]

    json_dict = {"plans": plans_arr, "meals": meals_arr}
    with open(JSON_PATH, 'w') as f:
        json.dump(json_dict, f)
    print('Plans exported to docs/plans.json\n')
    
def export_plans_csv():
    'Export plans to CSV'
    print('Exporting plans to CSV')

    plans = db.export_plans()
    with open('docs/plans.csv', 'w') as f:
        for plan in plans:
            f.write(f'{plan[0]},{plan[1]},{plan[2]},{plan[3]}\n')
    print('Plans exported to docs/plans.csv\n')
    
def export_plans(extension='json'):
    'Export plans to CSV or JSON:  EXPORT_PLANS [csv|json]'
    if extension == 'csv':
        export_plans_csv()
    elif extension == 'json':
        export_plans_json()
    else:
        print('Invalid extension\n')
  
def import_csv(file): #* the file should be in the format: meal_id, name, quantity
    'Import groceries from CSV:  IMPORT_CSV file'
    with open(file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.split(',')
            db.insert_grocery(line[0], line[1], line[2])
    print('Groceries imported from CSV\n')

def import_csv_url(url):
    'Import groceries from CSV:  IMPORT_CSV_URL url'
    data = requests.get(url).text.split('\n')
    for line in data:
        line = line.split(',')
        db.insert_grocery(line[0], line[1], line[2])
    print('Groceries imported from CSV\n')
    
def export_grocery_csv():
    'Export groceries to CSV'
    print('Exporting groceries to CSV')
    groceries = db.export_groceries()
    with open(GROCERY_PATH, 'w') as f:
        for grocery in groceries:
            f.write(f'{grocery[0]},{grocery[1]},{grocery[2]}')
    print('Groceries exported to docs/grocery.csv\n')
    
def export_grocery_json():
    'Export groceries to JSON'
    print('Exporting groceries to JSON')
    groceries = db.export_groceries()
    groceries_arr = [{'meal_id': grocery[0], 'name': grocery[1], 'quantity': grocery[2]} for grocery in groceries]
    with open('docs/groceries.json', 'w') as f:
        json.dump(groceries_arr, f)
    print('Groceries exported to docs/groceries.json\n')
    
def export_grocery(extension='csv'):
    'Export groceries to CSV or JSON:  EXPORT_GROCERY [csv|json]'
    print(extension)
    if extension == 'csv':
        export_grocery_csv()
    elif extension == 'json':
        export_grocery_json()
    else:
        print('Invalid extension\n')
   
 
# --- DBVIEWER CLASS -- 

def meal_select():
    'Page through existing recipes'
    global DATA_INDEX
    global DATA
    # case b'\r':
    #             return data[int(digit_buffer)][1]
    viewer = DBViewer(db, 'meals')
    viewer.view()
    return DATA[DATA_INDEX][1]

DATA_INDEX = 0
SELECTION = None
SELECTION_NAME = None
DATA = None
class DBViewer:
    def __init__(self, db, data_source, match=None, print_func=print_page_meals):
        self.db = db 
        self.index = 0
        self.page = 0
        self.data_source = data_source
        self.match = match
        self.print_func = print_func
        
    def set_data(self):
        global DATA
        global DATA_INDEX
        global SELECTION
        global SELECTION_NAME
        match self.data_source:
            case 'meals':
                DATA = self.db.get_meals()
            case 'planner':
                DATA = self.db.get_planner_meals()
                SELECTION = None
                SELECTION_NAME = None
            case 'grocery':
                if SELECTION is None:
                    SELECTION = DATA[DATA_INDEX][0]
                    SELECTION_NAME = DATA[DATA_INDEX][1]
                DATA = self.db.get_groceries(SELECTION)
            case _:
                pass
    
    def run_match(self, key):
        if self.match is not None:
            if key in self.match:
                self.match[key]()
                return True
        return False
    
    def view(self):
        'View all meals'
        global DATA_INDEX
        global DATA
        global SELECTION
        global SELECTION_NAME
        while True:
            if self.page < 0:
                self.page = 0
            self.set_data()
            DATA_INDEX = index_page(self.page, self.index)

            clear_terminal()
            self.print_func(self.page, DATA, DATA_INDEX, SELECTION_NAME)

            key = getch()
            
            if self.run_match(key):
                continue

            match key:
                case b'\xe0':
                    key = getch()
                    if pressed_up_arrow(key):
                        if self.index == 0:
                            self.index = 4
                        else:
                            self.index -= 1
                    elif pressed_down_arrow(key):
                        if self.index == 4:
                            self.index = 0
                        else:
                            self.index += 1
                
            match key:
                case b'n':
                    self.page += 1
                case b'p':
                    self.page -= 1
                case b'q':
                    return
                case b'\r':
                    return
                case _:
                    pass
if __name__ == '__main__':
    plan('monday')