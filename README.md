# Gym Log CLI (V2)

## Overview

**Gym Log CLI** is a command-line application for tracking full workout sessions, including exercises and sets (reps + weight). It allows users to log complete workouts, review current sessions, and explore past training history directly from the terminal.

Workout data is stored in a JSON file, ensuring persistence between runs.

This project is part of a structured roadmap focused on building real-world, modular applications and evolving them over time.

---

## Key Features

- Start and manage workout sessions
- Add exercises to a session (duplicate prevention)
- Log multiple sets per exercise (reps + weight)
- View the current session in a clean, structured format
- View session history (with exercise counts)
- View exercise history across all sessions
- Delete sessions (with automatic cleanup of empty sessions)
- Defensive input validation for all user inputs
- Automatic data persistence using JSON
- Clean modular architecture (main / logic / storage)

---

## Example Usage

```
Gym Log
-------
1) Start New Session
2) View History
3) Exit & Save
```

Session flow example:

```
Current Session
---------------
1) Add Exercise
2) View Current Session
3) Delete Session
4) Finish Session
```

Example session output:

```
Session 11 - 2026-04-16
----------------------
bench press
  Set 1: 10 reps @ 185 lbs
  Set 2: 10 reps @ 175 lbs
  Set 3: 10 reps @ 165 lbs
```

Example session history:

```
Session 11 - 2026-04-16 (1 exercise)
Session 10 - 2026-04-15 (3 exercises)
```

Example exercise history:

```
bench press: logged in 6 sessions
lat pulldown: logged in 2 sessions
```

---

## Project Architecture

The program follows a layered architecture separating user interaction, business logic, and persistence.

```
gym_log/
│
├── main.py        # CLI interface and menu flow
├── logic.py       # Core session, exercise, and set logic
├── storage.py     # File handling and persistence
├── config.json    # Configurable data settings
└── data/
    └── gym_data.json   # Auto-generated data file
```

### main.py
Handles the command-line interface, menu navigation, and user input.

### logic.py
Contains the core business logic, including:
- session creation and deletion
- exercise management
- set logging (reps + weight)
- history formatting

### storage.py
Responsible for:
- loading configuration
- ensuring data directories exist
- reading/writing JSON safely

---

## Data Format

Workout data is stored as structured session data:

```
{
  "sessions": [
    {
      "id": 11,
      "date": "2026-04-16",
      "exercises": [
        {
          "name": "bench press",
          "sets": [
            {"reps": 10, "weight": 185},
            {"reps": 10, "weight": 175}
          ]
        }
      ]
    }
  ]
}
```

This structure supports full workout tracking and enables future expansion.

---

## Running the Program

Navigate to the project directory and run:

```
python3 main.py
```

Python 3.9+ is recommended.

---

## Design Goals

This project focuses on demonstrating core software engineering practices:

- modular program design
- separation of concerns
- defensive programming
- structured data modeling
- CLI application design
- iterative project development

---

## Limitations

- No editing of sessions (yet)
- CLI-based (not optimized for mobile use)
- JSON storage (not optimized for large-scale data)

---

## Future Improvements

Planned upgrades include:

- SQLite database integration
- session editing capabilities
- predefined workout templates
- improved analytics and progress tracking
- web application version

---

## License

This project is provided for educational and portfolio purposes.

---

## Author

James Charron

Built as part of a structured daily software engineering practice routine focused on becoming job-ready.