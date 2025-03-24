import cmd, sys, os
from fp_funcs import * 
from fp_utils import is_valid_weekday

class FPShell(cmd.Cmd):
    intro = '\nWelcome to the yummy food planning cli :)!\nType help or ? to list commands.\n'
    
    prompt = '(yummy) '
    file = None
    
    def do_plan(self, arg):
        'Plan a day:  PLAN day_of_week'
        weekday = parse(arg)[0]
        if not is_valid_weekday(weekday):
            print('Invalid weekday\n')
            return
        plan(weekday)
        self.do_export()
        
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            
    def complete_plan(self, text, line, begidx, endidx):
        if text:
            return [weekday for weekday in self.weekdays if weekday.startswith(text)]
        else:
            return self.weekdays[:]
        
    def do_show(self, arg):
        'Show the current plan:  SHOW'
        weekday = parse(arg)[0]
        if not is_valid_weekday(weekday):
            print('Invalid weekday\n')
            return
        show(weekday)
        
    def complete_show(self, text, line, begidx, endidx):
        if text:
            return [weekday for weekday in self.weekdays + ["all"] if weekday.startswith(text)]
        else:
            return self.weekdays[:] + ["all"]
        
    def do_edit(self, arg):
        'Edit a day:  EDIT day_of_week'
        edit(*parse(arg))
        self.do_export()
    
    def complete_edit(self, text, line, begidx, endidx):
        if text:
            return [weekday for weekday in self.weekdays if weekday.startswith(text)]
        else:
            return self.weekdays[:]
        
    def do_grocery(self, arg):
        'Plan the whole grocery-list:  GROCERY item'
        grocery(*parse(arg))
        
    def do_export(self, arg=None):
        'Export the current plan:  EXPORT'
        plan_to_json()
        
    def do_exit(self, arg):
        'Exit the shell:  EXIT'
        print('Thank you for using the food planner')
        return True

def parse(arg):
    'Convert a series of zero or more strings to an argument tuple'
    return tuple(map(str, arg.split()))

if __name__ == '__main__':
    FPShell().cmdloop()