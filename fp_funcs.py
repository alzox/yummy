import json
import time
import os

from msvcrt import getch

import fp_db as db
from fp_utils import (
    MEALS, WEEKDAYS_LOWER, 
    pressed_arrow_key, pressed_up_arrow, pressed_down_arrow,
    clear_terminal, weekday_to_index, print_plan)

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
    if weekday == 'all':
        print_plan_all() #!STUBBED, print all plans in db
    else:
        plan = db.find_plan_print(weekday_to_index(weekday))
        print_meals(weekday, plan)
    
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
    
def plan_to_json():
    'Export plans to JSON'
    JSON_PATH = r"C:\Users\commo\OneDrive - University of Virginia\School\STEM\CS\Coding Projects 2025\Food-Planner\docs\plans.json"
    print('Exporting plans to JSON')
    plans = db.export_plans()
    # Serialize tuple (weekday, breakfast, lunch, dinner) to JSON
    plans_dict = [{'weekday': plan[0], 'breakfast': plan[1], 'lunch': plan[2], 'dinner': plan[3]} for plan in plans]
    with open(JSON_PATH, 'w') as f:
        json.dump(plans_dict, f)
    print('Plans exported to docs/plans.json')
    
"""Helper Functions"""
def suggest():
    #!STUBBED
    'Suggest 5 random recipes'
    print('Suggesting 5 random recipes')
    print('Recipe 1: Chicken Alfredo')
    print('Recipe 2: Spaghetti Carbonara')
    print('Recipe 3: Chicken Parmesan')
    print('Recipe 4: Chicken Marsala')
    print('Recipe 5: Chicken Piccata')
    
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
        
        key = getch().decode('utf-8').lower()
        
        match key:
            case 'n':
                page += 1
            case 'p':
                page -= 1
            case 'q':
                return None
            case '\x08':
                digit_buffer = digit_buffer[:-1]
            case '\r':
                return data[int(digit_buffer)][1]
            case _ if key.isdigit():
                digit_buffer += key
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

def print_meals(weekday, meal_arr):
    print('=' * 20)
    print(f'{weekday} Planned!')
    print('Breakfast: ' + meal_arr[0])
    print('Lunch: ' + meal_arr[1])
    print('Dinner: ' + meal_arr[2])
    print('=' * 20)
    
def print_page(page, data):
    print(f'Page {page}')
    print('=' * 20)
    for i in range(page * 5, min((page + 1) * 5, len(data))):
        print(f'{i}: {data[i][1]}')
    print('=' * 20)
    print('(n: next page | p: previous page | q: quit)')
       
if __name__ == '__main__':
    plan('monday')
    show('monday')