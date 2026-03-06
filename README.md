# Gym Log CLI

## Overview

**Gym Log CLI** is a command-line tool for tracking the most recent working weight used for each exercise. It allows users to quickly record lifts during or after workouts and view progress over time from the terminal.

The application stores workout data in a JSON file so that exercise history persists between runs.

This project was built as part of a structured learning roadmap focused on transitioning from small scripts to modular, production-style programs.

---

## Key Features

- Add new exercises
- Log the latest working weight for a lift
- View a summary of all exercises and current weights
- Automatic saving after every change
- Delete exercises from the log
- Configurable data storage location
- Defensive input validation
- Clean modular architecture

---

## Example Usage

```
Gym Log
-------
1) Add Exercise
2) Log Weight
3) View Summary
4) Delete Exercise
5) Exit & Save
```

Example summary output:

```
Gym Log Summary
---------------
bench press: 185 lbs
rdl: 225 lbs
lat pulldown: 140 lbs
```

---

## Project Architecture

The program follows a simple layered architecture separating user interaction, business logic, and persistence.

```
gym_log/
│
├── main.py        # CLI interface and menu loop
├── logic.py       # Core exercise and weight manipulation
├── storage.py     # File management, config loading, persistence
├── config.json    # Configurable data settings
└── data/
    └── gym_data.json   # Auto-generated data file
```

### main.py
Handles the interactive command-line interface and user input.

### logic.py
Contains the core business logic including:
- exercise normalization
- weight validation
- logging entries
- generating summaries

### storage.py
Responsible for:
- loading configuration
- ensuring data directories exist
- reading/writing JSON safely

---

## Configuration

The `config.json` file controls where the program stores data.

Example:

```
{
  "data_file": "gym_data.json",
  "data_folder": "data"
}
```

Fields:

| Key | Description |
|----|----|
| data_folder | Directory where workout data is stored |
| data_file | Name of the JSON file containing exercise data |

If the folder does not exist, the program automatically creates it.

---

## Data Format

Workout data is stored in JSON using a simple dictionary structure:

```
{
  "bench press": 185,
  "rdl": 225,
  "lat pulldown": 140
}
```

Each exercise maps to the most recently logged working weight.

---

## Running the Program

Navigate to the project directory and run:

```
python3 main.py
```

Python 3.9+ is recommended.

---

## Design Goals

This project focuses on demonstrating several core software engineering practices:

- Modular program design
- Separation of concerns
- Defensive programming
- Persistent data storage
- CLI application structure

It serves as a foundational project before moving on to more complex applications.

---

## Possible Future Improvements

Potential future upgrades include:

- tracking sets and reps
- historical lift tracking
- personal record detection
- CSV export
- graphical interface or web dashboard

---

## License

This project is provided for educational and portfolio purposes.

---

## Author

James Charron

Built as part of a daily software engineering practice routine focused on becoming job-ready as a developer.