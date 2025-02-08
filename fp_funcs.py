def plan(weekday):
    'Plan a day:  PLAN day_of_week'
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekdays_lower = [day.lower() for day in weekdays]
    weekday_lower = weekday.lower()
    if weekday_lower not in weekdays_lower:
        print('Invalid weekday')
    print('Planning', weekday)
    
if __name__ == '__main__':
    "Short tests"
    plan('Monday')