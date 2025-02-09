import os
import msvcrt

def plan(weekday):
    'Plan a day:  PLAN day_of_week'
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekdays_lower = [day.lower() for day in weekdays]
    weekday_lower = weekday.lower()
    if weekday_lower not in weekdays_lower:
        print('Invalid weekday')
        return
    
    print('Type suggest to get 5 suggestions')
    meals = ['breakfast', 'lunch', 'dinner']
    index = 0
    while True:
        # flush the input buffer from previous (y/n) input
        os.system('cls' if os.name == 'nt' else 'clear')
        
        meal = input('Enter ' + meals[index] + ': ')
        if meal == 'suggest':
            suggest()
        else:
            print('Confirm ' + meal + ' (y/n): ', end='', flush=True)
            while True:
                if msvcrt.kbhit():
                    key = msvcrt.getch().decode('utf-8').lower()
                    if key == 'y':
                        index += 1
                        break
                    elif key == 'n':
                        break
        if index == 3:
            break
    
    print(f'{weekday_lower} planned')
    print('Breakfast: ' + meals[0])
    print('Lunch: ' + meals[1])
    print('Dinner: ' + meals[2])

'''helper function'''
def suggest():
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