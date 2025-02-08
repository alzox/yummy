import cmd, sys
from fp_funcs import * 

class FPShell(cmd.Cmd):
    intro = 'Welcome to the food planning shell.   Type help or ? to list commands.\n'
    prompt = '(planner) '
    file = None
    
    "-- basic food planning commands --"
    def do_add(self, arg):
        'Add a food item to the list:  ADD "Spaghetti"'
        add(*parse(arg))

def parse(arg):
    'Convert a series of zero or more strings to an argument tuple'
    return tuple(map(str, arg.split()))

if __name__ == '__main__':
    FPShell().cmdloop()