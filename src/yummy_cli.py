import cmd, sys, os, re
from .yummy_funcs import * 
from .yummy_utils import is_valid_weekday, recursive_listdir

class Yummy(cmd.Cmd):
    intro = '\nWelcome to the yummy food planning cli :)!\nType help or ? to list commands.\n'
    
    prompt = '(yummy) '
    file = None
    
    def do_plan(self, arg):
        'Plan a day:  PLAN day_of_week'
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
        'Show the current plan:  SHOW'
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
        
    def do_db(self, arg):
        'Show and manage the meals in the database:  DB'
        db_meals()
                
    def do_grocery(self, arg):
        'Plan the whole grocery-list:  GROCERY item'
        grocery(*parse(arg))
        
    def do_import(self, arg=None):
        'Import into SQL from JSON:  IMPORT'
        if re.search('.json', arg):
            import_json(arg)
        else:
            print('Invalid file type\n')
            return
    
    def complete_import(self, text, line, begidx, endidx):
        both_extensions = recursive_listdir(".json") 
        if text:
            return [file for file in both_extensions if file.startswith(text)]
        else:
            return both_extensions
    
        
    def do_export(self, arg=None):
        'Export the current plan:  EXPORT'
        export_json()
        
    def do_exit(self, arg):
        'Exit the shell:  EXIT'
        print('Thank you for using the food planner\n')
        return True

def parse(arg):
    'Convert a series of zero or more strings to an argument tuple'
    return tuple(map(str, arg.split()))

if __name__ == '__main__':
    FPShell().cmdloop()