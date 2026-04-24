# Gym Log CLI (V3)

## Overview

**Gym Log CLI** is a command-line application for tracking full workout sessions using a SQLite database. It allows users to log exercises and sets (weight × reps), review current sessions, and explore past training history directly from the terminal.

This version replaces JSON storage with SQLite, providing a more scalable and structured data model.

SQLite was chosen to introduce relational data modeling and improve scalability compared to flat JSON storage.

---

## Example Usage

```
Gym Log
-------
1) Start New Session
2) View History
3) Exit & Save
```

Session flow:

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
Session 1 - 2026-04-24
bench press
  Set 1: 185 lbs x 10 reps
  Set 2: 225 lbs x 6 reps
  Set 3: 205 lbs x 8 reps
tricep pushdown
  Set 1: 62.5 lbs x 10 reps
  Set 2: 67.5 lbs x 8 reps
```

---
## Key Features

- Start and manage workout sessions
- Add exercises to a session (duplicate prevention)
- Log multiple sets per exercise (weight × reps)
- View the current session with full set breakdown
- View session history (with exercise counts)
- View exercise history across all sessions
- Delete sessions (with full cleanup of related data)
- Automatic cleanup of empty sessions
- Defensive input validation for all user inputs
- Persistent storage via SQLite
- Clean modular architecture (main / logic / db)

---

## Project Architecture

```
gym_log/
│
├── main.py   # CLI interface and menu flow
├── db.py     # SQLite database layer (queries, inserts, deletes)
├── logic.py  # Input validation and formatting helpers
└── gym.db    # SQLite database file (created at runtime, not tracked in repo)
```

### main.py
Handles user interaction, menu navigation, and overall program flow.

### db.py
Responsible for all database operations, including:
- creating tables
- inserting sessions, exercises, and sets
- querying session and exercise history
- deleting sessions and related data

### logic.py
Contains helper functions for:
- input validation
- parsing numbers
- formatting weight output

---

## Technologies Used

- Python 3
- SQLite

---

## Database Schema

The application uses three related tables:

### sessions
| id | date |

### exercises
| id | session_id | name |

### sets
| id | exercise_id | reps | weight |

Relationships:

```
session → exercises → sets
```

---

## Running the Program

From the project directory:

```
python3 main.py
```

Python 3.9+ recommended.

---

## Design Goals

This project demonstrates:

- modular program design
- separation of concerns
- relational data modeling with SQLite
- CLI application architecture
- iterative software development

---

## Project Evolution

- V1 → basic CLI
- V2 → JSON-based persistence
- V3 → SQLite relational model

---

## Limitations

- No editing of sessions or sets
- CLI-based interface
- No user authentication or multi-user support

---

## Future Improvements

- Edit existing sessions and sets
- Add exercise presets / templates
- Progress tracking and analytics
- Export data (CSV / JSON)
- Web or GUI version

---

## License

This project was created for educational and portfolio purposes.

---

## Author

James Charron

Built as part of a structured daily software engineering practice routine focused on becoming job-ready.