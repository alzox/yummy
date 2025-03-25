import cmd, re

from .funcs import * 
from .utils import is_valid_weekday, recursive_listdir

class Yummy(cmd.Cmd):
    intro = '\nWelcome to the yummy (meal planning) cli :)!\nType help or ? to list commands.\n'
    
    prompt = '(yummy) '
    file = None
    
    def do_plan(self, arg):
        'Plan the meals for a weekday: PLAN weekday'
        if not arg:
            print('No weekday specified\n')
            return
        weekday = parse(arg)[0]
        if not is_valid_weekday(weekday):
            print('Invalid weekday\n')
            return
        plan(weekday)
        
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            
    def complete_plan(self, text, line, begidx, endidx):
        if text:
            return [weekday for weekday in self.weekdays if weekday.startswith(text)]
        else:
            return self.weekdays[:]
        
    def do_show(self, arg):
        'Show the planned meals for a weekday: SHOW weekday'
        if not arg:
            show()
            return
        weekday = parse(arg)[0]
        if not is_valid_weekday(weekday) and weekday != 'all':
            print('Invalid weekday\n')
            return
        show(weekday)
        
    def complete_show(self, text, line, begidx, endidx):
        if text:
            return [weekday for weekday in self.weekdays + ["all"] if weekday.startswith(text)]
        else:
            return self.weekdays[:] + ["all"]
        
    def do_meals(self, arg):
        'View and edit the database of meals: MEALS'
        meals()
                
    def do_grocery(self, arg):
        'View and edit the grocery list for planned meals: GROCERY'
        grocery(*parse(arg))
        
    def do_import(self, arg=None):
        'Import a meal plan or grocery list into sqlite: IMPORT file'
        args = parse(arg)
        if len(args) == 0:
            print('No file specified\n')
            return
        if len(args) > 1:
            print('Too many arguments\n')
            return
        if re.search('http', arg):
            if re.search('.json', arg):
                import_json_url(args[0])
            if re.search('.csv', arg):
                import_csv_url(args[0])
        else:
            if re.search('.json', arg):
                import_json(args[0])
            if re.search('.csv', arg):
                import_csv(args[0])
        return
    
    def complete_import(self, text, line, begidx, endidx):
        both_extensions = recursive_listdir(".json") 
        if text:
            return [file for file in both_extensions if file.startswith(text)]
        else:
            return both_extensions
    
    def do_export(self, arg):
        'Export the meal plan or grocery list to a file: EXPORT [grocery|plan] [json|csv]'
        #! there has to be a better way to do this
        args = parse(arg)
        
        if len(args) == 2:
            if args[0] not in ['grocery', 'plan']:
                print('Invalid export option\n')
                return
            elif args[0] == 'grocery':
                export_grocery(args[1])
            elif args[0] == 'plan':
                export_plans(args[1])
             
        if args[0] not in ['grocery', 'plan']:
            print('Invalid export option\n')
            return
        elif args[0] == 'grocery':
            export_grocery()
        elif args[0] == 'plan':
            export_plans() 
       
    def complete_export(self, text, line, begidx, endidx):
        words = ["grocery", "plan", "json", "csv"]
        if text:
            return [word for word in words if word.startswith(text)]
        else:
            return words 
        
    def do_summary(self, arg):
        'View a summary of the database: SUMMARY'
        summary()
        
    def do_exit(self, arg):
        'Exit the shell: EXIT'
        print('Thank you for using the meal planner\n')
        return True

def parse(arg):
    'Convert a series of zero or more strings to an argument tuple'
    return tuple(map(str, arg.split()))

if __name__ == '__main__':
    FPShell().cmdloop()
