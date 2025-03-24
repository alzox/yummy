import json
import time
import os

from msvcrt import getch

import fp_db as db
from fp_utils import (
    MEALS, WEEKDAYS_LOWER, 
    pressed_arrow_key, pressed_up_arrow, pressed_down_arrow,
    clear_terminal, weekday_to_index, index_page,
    print_plan, print_meals) #! why two print_plan functions?

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
    
def db_meals():
    'Show and edite the current meals:  DB_MEALS'
    db_viewer()
    
    
def grocery():
    "Add ingredients to grocery list:  GROCERY"
    print('Adding ingredients to grocery list')
    GROCERY_PATH = r"C:\Users\commo\OneDrive - University of Virginia\School\STEM\CS\Coding Projects 2025\Food-Planner\docs\grocery.csv"
    setup_grocery()
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print_grocery()
        ingredient = input('Enter ingredient: ').title()
        if ingredient == 'exit':
            break
        quantity = input('Enter quantity: ')
        if quantity == 'exit':
            break
        with open(GROCERY_PATH, 'a') as f:
            f.write(f'{ingredient},{quantity}\n')
            f.close()
        
def setup_grocery():
    'Setup grocery list:  SETUP_GROCERY'
    GROCERY_PATH = r"C:\Users\commo\OneDrive - University of Virginia\School\STEM\CS\Coding Projects 2025\Food-Planner\docs\grocery.csv"
    with open(GROCERY_PATH, 'w') as f:
        print('Grocery list setup')
        f.close()
    return

def import_json(file):
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
    
    
 
def export_json():
    'Export plans to JSON'
    JSON_PATH=r"C:\Users\commo\OneDrive - University of Virginia\School\STEM\CS\alzox\yummy\docs\plans.json"
    print('Exporting plans to JSON')

    plans = db.export_plans()
    plans_arr = [{'weekday': plan[0], 'breakfast': plan[1], 'lunch': plan[2], 'dinner': plan[3]} for plan in plans]
    meals = db.get_meals()
    meals_arr = [{'id': meal[0], 'name': meal[1]} for meal in meals]

    json_dict = {"plans": plans_arr, "meals": meals_arr}
    with open(JSON_PATH, 'w') as f:
        json.dump(json_dict, f)
    print('Plans exported to docs/plans.json\n')
    
"""Helper Functions"""
def meal_select():
    'Page through existing recipes'
    data = db.get_meals()
    page = 0
    digit_buffer = ''
    while True:
        if page < 0:
            page = 0
            
        clear_terminal()
        print_page(page, data)
        print(f'\nEnter meal #: {digit_buffer}', end='')
        
        key = getch()
        
        match key:
            case b'n':
                page += 1
            case b'p':
                page -= 1
            case b'q':
                return None
            case b'\x08':
                digit_buffer = digit_buffer[:-1]
            case b'\r':
                return data[int(digit_buffer)][1]
            case _ if key.isdigit():
                digit_buffer += key.decode('utf-8')
            case _:
                pass

def db_viewer():
    'View all meals'
    
    index = 0 
    page = 0
    while True:
        if page < 0:
            page = 0
        data = db.get_meals()
        data_index = index_page(page, index)
         
        clear_terminal()
        print_page(page, data, data_index)
        print('(enter: edit | d: delete | a: add)\n')
        
        key = getch()
        
        match key:
            case b'\xe0':
                key = getch()
                if pressed_up_arrow(key):
                    if index == 0:
                        index = 4
                    else:
                        index -= 1
                elif pressed_down_arrow(key):
                    if index == 4:
                        index = 0
                    else:
                        index += 1
            case b'\r':
                meal = input(f'Edit {data[data_index][1]}: ')
                if meal is None:
                    continue
                else:
                    db.edit_meal(data[data_index][0], meal)  
                    continue 
            case b'd':
                db.delete_meal(data[data_index][0])
                continue
            case b'a':
                db.insert_meal(input('Add meal: '))
                continue

        match key:
            case b'n':
                page += 1
            case b'p':
                page -= 1
            case b'q':
                return
            case _:
                pass
            
"""Helper Print Functions"""
def print_grocery():
    GROCERY_PATH = r"C:\Users\commo\OneDrive - University of Virginia\School\STEM\CS\Coding Projects 2025\Food-Planner\docs\grocery.csv"
    print('=' * 20)
    print('Grocery List')
    with open(GROCERY_PATH, 'r') as f:
        for line in f.readlines():
            data = line.strip().split(',')
            print(f'{data[1]}x: {data[0]}')
    print('=' * 20)
    print('Type "exit" to exit')

def print_plan_option():
    print('\n') 
    print('=' * 20)
    print('"suggest" for recipe suggestions')
    print('"select" to select from existing recipes')
    print('"exit" to exit planning')
    
def print_edit(plan, index):
    print('=' * 20)
    for i in range(3):
        if i == index:
            print(f'{meals[i].title()}: {db.find_meal(plan[i + 2])} <')
        else:
            print(f'{meals[i].title()}: {db.find_meal(plan[i + 2])}')
    print('=' * 20)
    print('Select meal to edit')
    print('Use up and down arrows to navigate')
    print('Press enter to edit and escape to exit')

    
def print_page(page, data, index=None):
    print(f'Page {page}')
    print('=' * 20)
    for i in range(page * 5, min((page + 1) * 5, len(data))):
        if i == index:
            print(f'\033[1m{i}: {data[i][1]} <\033[0m')
        else:
            print(f'{i}: {data[i][1]}')
    print('=' * 20)
    print('(n: next page | p: previous page | q: quit)')
       
if __name__ == '__main__':
    pass