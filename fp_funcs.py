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
    meals = ['breakfast', 'lunch', 'dinner']
    meal_arr = []
    index = 0
    while True:        
        meal = input('Enter ' + meals[index] + ': ')
        if meal == 'suggest':
            suggest()
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
    
    
    
'''helper function'''
def suggest():
    #!STUBBED
    'Suggest 5 random recipes'
    print('Suggesting 5 random recipes')
    print('Recipe 1: Chicken Alfredo')
    print('Recipe 2: Spaghetti Carbonara')
    print('Recipe 3: Chicken Parmesan')
    print('Recipe 4: Chicken Marsala')
    print('Recipe 5: Chicken Piccata')
    
if __name__ == '__main__':
    "Short tests"
    plan('Monday')