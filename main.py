from pathlib import Path
import sqlite3
from logic import parse_weight, parse_positive_int, normalize_weight
from db import init_db, start_session, add_exercise, add_set, get_sessions, get_exercises_for_session, get_sets_for_exercise, delete_session, get_exercise_history


def run_menu(conn) -> None:
    """Run the main CLI menu for the gym log application.

    Allows the user to:
    - start a new workout session
    - view workout history (sessions or exercises)
    - exit and save data

    This function serves as the primary navigation loop for the application.
    """
    while True:
        print("\nGym Log")
        print("-------")
        print("1) Start New Session")
        print("2) View History")
        print("3) Exit & Save")

        choice = input("Choice: ").strip()

        if choice == '1':
            session_id = start_session(conn)
            print(f"New session created. (ID: {session_id})")
            run_session_menu(conn, session_id)
            
        elif choice == '2':
            run_history_menu(conn)

        elif choice == '3':
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Menu options are 1, 2, or 3.")


def prompt_for_sets() -> list[dict]:
    """Prompt the user for completed sets and return them as a list.
    Each set contains validated reps and weight values.
    """
    while True:
        raw_count = input("How many sets did you complete? ").strip()
        set_count = parse_positive_int(raw_count)
        if set_count is None:
            print("Set count must be a whole number greater than 0.")
            continue
        break

    sets = []
    for i in range(1, set_count + 1):
        while True:
            raw_weight = input(f"Set {i} weight: ").strip()
            weight = parse_weight(raw_weight)
            if weight is None:
                print("Weight must be a number greater than 0.")
                continue
            break

        while True:
            raw_reps = input(f"Set {i} reps: ").strip()
            reps = parse_positive_int(raw_reps)
            if reps is None:
                print("Reps must be a whole number greater than 0.")
                continue
            break

        sets.append({"reps": reps, "weight": weight})

    return sets


def run_session_menu(conn, session_id: int) -> None:
    """Run the active session submenu for logging and reviewing a workout."""
    while True:
        print("\nCurrent Session")
        print("---------------")
        print("1) Add Exercise")
        print("2) View Current Session")
        print("3) Delete Session")
        print("4) Finish Session")

        choice = input("Choice: ").strip()

        if choice == '1':
            name = input("Enter exercise name: ").strip().lower()
            if not name:
                print("Exercise name cannot be empty.")
            else:
                existing_exercises = get_exercises_for_session(conn, session_id)
                duplicate = False
                for exercise in existing_exercises:
                    if exercise[1] == name:
                        duplicate = True
                        break

                if duplicate:
                    print("Invalid or duplicate exercise.")
                    continue

                exercise_id = add_exercise(conn, session_id, name)

                sets = prompt_for_sets()
                for s in sets:
                    add_set(conn, exercise_id, s["reps"], s["weight"])

                print("Exercise added.")

        elif choice == '2':
            sessions = get_sessions(conn)
            session_row = None
            for row in sessions:
                if row[0] == session_id:
                    session_row = row
                    break
            
            if session_row is None:
                print("Session not found.")
                continue
            
            print(f"Session {session_row[0]} - {session_row[1]}")
            exercises = get_exercises_for_session(conn, session_id)
            if not exercises:
                print("No exercises logged in this session yet.")
            else:
                for exercise in exercises:
                    exercise_id = exercise[0]
                    exercise_name = exercise[1]
                    print(exercise_name)

                    sets = get_sets_for_exercise(conn, exercise_id)
                    for i, set_entry in enumerate(sets, start=1):
                        reps = set_entry[0]
                        weight = normalize_weight(set_entry[1])
                        print(f"  Set {i}: {weight} lbs x {reps} reps")
        
        elif choice == '3':
            delete_choice = input("Are you sure? (y/n): ").strip().lower()
            if delete_choice == 'y':
                if delete_session(conn, session_id):
                    print("Session deleted.")
                else:
                    print("Session not found.")
                return
            elif delete_choice == 'n':
                continue
            else:
                print("Invalid response.")
                continue

        elif choice == '4':
            exercises = get_exercises_for_session(conn, session_id)
            if not exercises:
                delete_session(conn, session_id)
                print("Empty session discarded.")
            return

        else:
            print("Invalid choice. Menu options are 1, 2, 3, or 4.")


def run_history_menu(conn) -> None:
    """Run the history submenu for viewing past workout data."""
    while True:
        print("\nHistory")
        print("-------")
        print("1) View Session History")
        print("2) View Exercise History")
        print("3) Back")

        choice = input("Choice: ").strip()

        if choice == '1':
            sessions = get_sessions(conn)
            if not sessions:
                print("No sessions found.")
            else:
                for row in reversed(sessions):
                    session_id = row[0]
                    session_date = row[1]
                    exercises = get_exercises_for_session(conn, session_id)
                    exercise_count = len(exercises)
                    label = "exercise" if exercise_count == 1 else "exercises"
                    print(f"Session {session_id} - {session_date} ({exercise_count} {label})")

        elif choice == '2':
            history = get_exercise_history(conn)
            if not history:
                print("No exercise history found.")
            else:
                for row in history:
                    name = row[0]
                    count = row[1]
                    label = "session" if count == 1 else "sessions"
                    print(f"{name}: logged in {count} {label}")

        elif choice == '3':
            return
        
        else:
            print("Invalid choice. Menu options are 1, 2, or 3.")


def main() -> None:
    """Program entry point.
    Opens the SQLite database connection and starts the CLI menu.
    """
    base_dir = Path(__file__).resolve().parent
    db_path = base_dir / "gym.db"
    conn = sqlite3.connect(db_path)
    init_db(conn)
    try:
        run_menu(conn)
    finally:
        conn.close()


if __name__ == "__main__":
    main()