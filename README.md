# yummy

yummy is a personal meal planning and grocery management tool designed to simplify weekly food planning. It allows users to create, edit, and view meal plans for each day of the week, manage grocery lists, and interact with a database of meals and groceries. The project includes a command-line interface (CLI) for managing plans and a web-based interface for visualizing meal plans and grocery lists.

## Features

- Plan meals for each day of the week.
- Manage a database of meals and groceries.
- Export and import plans and groceries in JSON or CSV formats.
- Interactive CLI for meal planning and database management.
- Web-based interface to track plan hosted on Github Pages.
- Persistent local storage using SQLite.

## Requirements

```bash
pip install -t requirements.txt
```

- Python 3.x
- pyreadline3
- requests

## Usage

```bash
python3 db-setup.py
python3 yummy.py
```

- Add os.cwd() to PATH if you want to run it from anywhere
- Open/Install liveserver to see planner site after exports

```bash
(yummy) import https://raw.githubusercontent.com/alzox/yummy/refs/heads/master/docs/plans.json  
(yummy) import https://raw.githubusercontent.com/alzox/yummy/refs/heads/master/docs/grocery.csv 
```

- Import above if you want something to get started with or clone as template to save "locally"

## Personal To-dos

- Make it work on linux
