import os

# --- CONSTS ---

WEEKDAYS_LOWER = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
MEALS = ['breakfast', 'lunch', 'dinner']

# --- UTILITY FUNCTIONS ---

def is_valid_weekday(weekday):
    return weekday.lower() in WEEKDAYS_LOWER

def weekday_to_index(weekday):
    return WEEKDAYS_LOWER.index(weekday.lower()) + 1

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def pressed_arrow_key(key):
    return key == b'\xe0'

def pressed_up_arrow(key):
    return key == b'H'

def pressed_down_arrow(key):
    return key == b'P'

def index_page(page, index):
    if page == 0:
        return index
    else:
        return page * 5 + index % 5
    
# --- AUTO-COMPLETE FUNCTIONS ---

def recursive_listdir(extension = None):
    if extension is None:
        return os.listdir()
    else:   
        items = []
        for file in os.listdir():
            if file.endswith(extension):
                items.append(file)
            if os.path.isdir(file):
                path = os.getcwd()
                os.chdir(file)
                inner_items = recursive_listdir(extension)
                for inner_item in inner_items:
                    items.append(file + '/' + inner_item)
                os.chdir(path)
        return items
       
    
# --- PRESENTATION FUNCTIONS ---

def print_plan(plans = None, index = 0, weekday = None):
    print(f'Meal Plan for {str.title(weekday)}')
    print('=' * 20)
    
    if plans is None:
        for i in range(3):
            if i == index:
                print(f'\033[1m{str.title(MEALS[i])}: Not Planned < \033[0m')
            else:
                print(f'{str.title(MEALS[i])}: Not Planned')    
    else:
        for i, plan in enumerate(plans):
            if i == index:
                print(f'\033[1m{str.title(MEALS[i])}: {plan} < \033[0m')
            else:
                print(f'{str.title(MEALS[i])}: {plan}')
    
    print('=' * 20)
    print('(arrow keys to move | enter: edit | q: quit)')
    print('\n')
    
def print_meals(weekday, meal_arr):
    print(f'{str.title(weekday)}\'s Plan')
    print('=' * 20)
    print('Breakfast: ' + meal_arr[0])
    print('Lunch: ' + meal_arr[1])
    print('Dinner: ' + meal_arr[2])
    print('=' * 20)