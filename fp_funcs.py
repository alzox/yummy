import keyboard
import msvcrt
import fp_db as db

def plan(weekday):
    'Plan a day:  PLAN day_of_week'
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekdays_lower = [day.lower() for day in weekdays]
    weekday_lower = weekday.lower()
    if weekday_lower not in weekdays_lower:
        print('Invalid weekday')
        
    print('Type suggest to get 5 suggestions')
    print('Type select to select from existing recipes')
    meals = ['breakfast', 'lunch', 'dinner']
    meal_arr = []
    index = 0
    while True:        
        meal = input('Enter ' + meals[index] + ': ')
        if meal == 'exit':
            return
        if meal == 'suggest':
            suggest()
            meal = None
        elif meal == 'select':
            meal = select()
            
        if meal is None:
            continue
        else:
            print('Confirm ' + meal + ' (y/n): ')
            
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
    
    print(f'{weekday_lower} planned')
    print('Breakfast: ' + meal_arr[0])
    print('Lunch: ' + meal_arr[1])
    print('Dinner: ' + meal_arr[2])
    db.insert_plan(weekdays_lower.index(weekday_lower) + 1, db.find_mealid(meal_arr[0]), db.find_mealid(meal_arr[1]), db.find_mealid(meal_arr[2]))

def show(weekday):
    'Show the current plan:  SHOW'
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekdays_lower = [day.lower() for day in weekdays]
    weekday_lower = weekday.lower()
    if weekday_lower not in weekdays_lower or not weekday_lower == 'all':
        print('Invalid input')
        
    if weekday_lower == 'all':
        for day in weekdays:
            show(day)
    else:
        plan = db.find_plan(weekdays_lower.index(weekday_lower) + 1)
        if plan is None:
            print(f'{weekday_lower} not planned')
        else:
            print(f'{weekday_lower} Plan')
            print('Breakfast: ' + db.find_meal(plan[1]))
            print('Lunch: ' + db.find_meal(plan[2]))
            print('Dinner: ' + db.find_meal(plan[3]))
            
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
        for i in range(page * 5, min((page + 1) * 5, len(data))):
            print(f'{i + 1}: {data[i][1]}')
        print(f'Page {page}')
        print('n: next page | p: previous page | q: quit')
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
                    print(f'Selecting Item: {digit_buffer}')
                elif key == '\x08':
                    digit_buffer = digit_buffer[:-1]
                    print(f'Selecting Item: {digit_buffer}')
                elif key == '\r':
                    return data[int(digit_buffer) - 1][1]
    return None
        
    
if __name__ == '__main__':
    "Short tests"
    plan('Monday')