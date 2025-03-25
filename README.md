# yummy

yummy is a personal meal planning and grocery management tool designed to simplify weekly food planning. It allows users to create, edit, and view meal plans for each day of the week, manage grocery lists, and interact with a database of meals and groceries. The project includes a command-line interface (CLI) for managing plans and a web-based interface for visualizing meal plans and grocery lists.

## Features

- Plan meals for each day of the week.
- Manage a database of meals and groceries.
- Export and import plans and groceries in JSON or CSV formats.
- Interactive CLI for meal planning and database management.
- Web-based interface with dynamic updates using JavaScript.
- Persistent storage using SQLite.

## Requirements

```bash
pip install -t requirements.txt
```

- Python 3.x
- pyreadline3
- sqlite3

## Usage

```bash
python3 db-setup.py
python3 yummy.py
```

- Add os.cwd() to PATH if you want to run it from anywhere
- Open/Install liveserver to see planner site after exports
- 

## Personal To-dos

- add platform dependent imports for getch
- YOU NEED TO REFACTOR
- more stylistic prints
- review ui flow
- review set-up and run scripts
- review db location?
- review directory structure for scripts and resources

UI FLOW AND NOTES ABOUT PRINTS

refactor all help strings to be more informative

db:
index can go beyond what exists for the current page
    * this can cause index out of range
edit statement should be edit name:

export:
autocomplete could be a bit better

grocery:
index can go beyond what exists for the current page
edit statement should be edit name
edit prints for the planner page

import:
error handling for mischema'd json files
fix export and import dependence