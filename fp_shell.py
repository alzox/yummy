import cmd, sys
from fp_funcs import * 

class FPShell(cmd.Cmd):
    intro = 'Welcome to the food planning shell.   Type help or ? to list commands.\n'
    prompt = '(planner) '
    file = None
    
    "-- basic food planning commands --"
    def do_plan(self, arg):
        'Plan a day:  PLAN day_of_week'
        plan(*parse(arg))
        
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            
    def complete_plan(self, text, line, begidx, endidx):
        if text:
            return [weekday for weekday in self.weekdays if weekday.startswith(text)]
        else:
            return self.weekdays[:]
        
    def do_show(self, arg):
        'Show the current plan:  SHOW'
        show(*parse(arg))
        
    def do_exit(self, arg):
        'Exit the shell:  EXIT'
        print('Thank you for using the food planner')
        return True

def parse(arg):
    'Convert a series of zero or more strings to an argument tuple'
    return tuple(map(str, arg.split()))

if __name__ == '__main__':
    FPShell().cmdloop()