import json
import os
import msvcrt
import fp_db as db

weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
weekdays_lower = [day.lower() for day in weekdays]
meals = ['breakfast', 'lunch', 'dinner']

def plan(weekday):
    'Plan a day:  PLAN day_of_week'
    
    weekday_lower = weekday.lower()
    if weekday_lower not in weekdays_lower:
        print('Invalid weekday')
        return
    print_plan_option()
    meal_arr = []
    index = 0
    while True:        
        print('=' * 20)
        meal = input('Enter ' + meals[index] + ': ')
        
        match meal:
            case 'exit':
                return
            case 'suggest':
                suggest()
                meal = None
            case 'select':
                meal = select()
            
        if meal is None:
            continue
        else:
            print('Confirm ' + meal + '? (y/n)')
            
            while True:
                if msvcrt.kbhit():
                    key = msvcrt.getch().decode('utf-8').lower()
                    if key == 'y':
                        meal_arr.append(meal)
                        db.insert_meal(meal)
                        index += 1
                        break
                    elif key == 'n':
                        break
        if index == 3:
            break
    print_meals(weekday, meal_arr)
    db.insert_plan(weekdays_lower.index(weekday_lower) + 1, db.find_mealid(meal_arr[0]), db.find_mealid(meal_arr[1]), db.find_mealid(meal_arr[2]))

def edit(weekday):
    'Edit a day:  EDIT day_of_week'
    
    weekday_lower = weekday.lower()
    if weekday_lower not in weekdays_lower:
        print('Invalid weekday')
        return
    print('=' * 20)
    print("Editing: " + weekday)
    
    plan = db.find_plan(weekdays_lower.index(weekday_lower) + 1)
    if plan is None:
        print(f'{weekday} Not Planned')
        return
    
    index = 0
    print_edit(plan, index)
    while True:
        if index < 0:
            index = 2
        elif index > 2:
            index = 0
            
        if msvcrt.kbhit():
            
            # decode arrow to str
            key = msvcrt.getch()
            if key == b'\xe0':
                key = msvcrt.getch()
                # up arrow
                if key == b'H':
                    index -= 1
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print_edit(plan, index)
                # down arrow
                elif key == b'P':
                    index += 1
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print_edit(plan, index)
            # escape
            elif key == b'\x1b':
                return
            # enter
            elif key == b'\r':
                print_plan_option()
                meal = input('Editing ' + meals[index] + ': ')
                
                match meal:
                    case 'exit':
                        return
                    case 'suggest':
                        suggest()
                        meal = None
                    case 'select':
                        meal = select()
                        
                if meal is None:
                    continue
                else:
                    print('Confirm ' + meal + '? (y/n)')
                    
                    db.insert_meal(meal)
                    
                    while True:
                        if msvcrt.kbhit():
                            key = msvcrt.getch().decode('utf-8').lower()
                            if key == 'y':
                                db.update_plan(weekdays_lower.index(weekday_lower) + 1, meals[index], db.find_mealid(meal))
                                return
                            elif key == 'n':
                                break
                
def show(weekday='all'):
    'Show the current plan:  SHOW'
    
    weekday_lower = weekday.lower()
    if weekday_lower not in weekdays_lower and not weekday_lower == 'all':
        print('Invalid input')
        return 
    
    if weekday_lower == 'all':
        for day in weekdays:
            show(day)
    else:
        plan = db.find_plan(weekdays_lower.index(weekday_lower) + 1)
        if plan is None:
            print('=' * 20)
            print(f'{weekday} Not Planned')
        else:
            print_plan(weekday, plan)
    
    
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
    
def clear():
    'Clear all plans'
    db.clear_plans()
    print('All plans cleared')
    
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
    
def select():
    'Page through existing recipes'
    data = db.get_meals()
    page = 0
    while True:
        if page < 0:
            page = 0
        os.system('cls' if os.name == 'nt' else 'clear')
        print_page(page, data)
        digit_buffer = ''
        while True:
            if msvcrt.kbhit():
                key = msvcrt.getch().decode('utf-8').lower()
                if key == 'n':
                    page += 1
                    break
                elif key == 'p':
                    page -= 1
                    break
                elif key == 'q':
                    return None
                elif key.isdigit():
                    digit_buffer += key
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print_page(page, data)
                    print(f'Selecting Item: {digit_buffer}')
                elif key == '\x08':
                    digit_buffer = digit_buffer[:-1]
                    print(f'Selecting Item: {digit_buffer}')
                elif key == '\r':
                    return data[int(digit_buffer) - 1][1]
    return None

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
    
def print_plan(weekday, plan):
    print('=' * 20)
    print(f'{weekday} Plan')
    print('Breakfast: ' + db.find_meal(plan[2]))
    print('Lunch: ' + db.find_meal(plan[3]))
    print('Dinner: ' + db.find_meal(plan[4]))
    
def print_page(page, data):
    print('=' * 20)
    for i in range(page * 5, min((page + 1) * 5, len(data))):
        print(f'{i + 1}: {data[i][1]}')
    print('=' * 20)
    print(f'Page {page}')
    print('n: next page | p: previous page | q: quit')
       
if __name__ == '__main__':
    grocery()