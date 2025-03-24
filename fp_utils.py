import os

# --- CONSTS ---

WEEKDAYS_LOWER = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
MEALS = ['breakfast', 'lunch', 'dinner']

# --- UTILITY FUNCTIONS ---

def is_valid_weekday(weekday):
    return weekday.lower() in WEEKDAYS_LOWER

def weekday_to_index(weekday):
    return WEEKDAYS_LOWER.index(weekday.lower())

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')
    
# --- PRESENTATION FUNCTIONS ---

def print_plan(plans = None, index = 0, weekday = None):
    print(f'Meal Plan for {weekday}')
    print('-' * 20)
    
    if plans is None:
        for i in range(3):
            if i == index:
                print(f'\033[1m{MEALS[i]}: Not Planned\033[0m')
            else:
                print(f'{MEALS[i]}: Not Planned')    
    else:
        for i, plan in enumerate(plans):
            if i == index:
                print(f'\033[1m{MEALS[i]}: {plan}\033[0m')
            else:
                print(f'{MEALS[i]}: {plan}')