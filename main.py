from pathlib import Path
import sys
from storage import load_config, set_environment, load_data, save_data
from logic import create_session, delete_session, add_exercise_to_session, parse_weight, parse_positive_int, current_session_lines


def run_menu(data: dict, file_path: Path) -> None:
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
            session = create_session(data)
            save_data(file_path, data)
            print(f"New session created. (ID: {session['id']}, Date: {session['date']})")
            run_session_menu(data, file_path, session)
            
        elif choice == '2':
            print("View history coming soon.")

        elif choice == '3':
            save_data(file_path, data)
            print("Saved. Goodbye!")
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
            raw_reps = input(f"Set {i} reps: ").strip()
            reps = parse_positive_int(raw_reps)
            if reps is None:
                print("Reps must be a whole number greater than 0.")
                continue
            break

        while True:
            raw_weight = input(f"Set {i} weight: ").strip()
            weight = parse_weight(raw_weight)
            if weight is None:
                print("Weight must be a number greater than 0.")
                continue
            break

        sets.append({"reps": reps, "weight": weight})

    return sets


def run_session_menu(data: dict, file_path: Path, session: dict) -> None:
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
            exercise_name = input("Enter exercise name: ").strip()
            if add_exercise_to_session(session, exercise_name):
                sets = prompt_for_sets()
                session["exercises"][-1]["sets"] = sets
                save_data(file_path, data)
                print("Exercise added.")

            else:
                print("Invalid or duplicate exercise.")

        elif choice == '2':
            for line in current_session_lines(session):
                print(line)
        
        elif choice == '3':
            delete_choice = input("Are you sure? (y/n): ").strip().lower()
            if delete_choice == 'y':
                delete_session(data, session["id"])
                save_data(file_path, data)
                print("Session deleted.")
                return
            
            elif delete_choice == 'n':
                continue
            
            else:
                 print("Invalid response.")
                 continue

        elif choice == '4':
            if not session["exercises"]:
                delete_session(data, session["id"])
                save_data(file_path, data)
                print("Empty session discarded.")
                return

            save_data(file_path, data)
            return

        else:
            print("Invalid choice. Menu options are 1, 2, 3, or 4.")


def main() -> None:
    """Program entry point.
    Loads configuration, prepares the data environment,
    loads existing gym data, and initiates the CLI menu.
    """
    base_dir = Path(__file__).resolve().parent
    config_path = base_dir / "config.json"

    config = load_config(config_path)
    if config is None:
        sys.exit("Config failed to load.")
    data_folder = config.get("data_folder")
    data_file = config.get("data_file")

    if not data_folder or not data_file:
        print("Error: config.json must contain 'data_folder' and 'data_file'.")
        sys.exit(1)
    if not isinstance(data_folder, str) or not isinstance(data_file, str):
        print("Error: 'data_folder' and 'data_file' must both be strings")
        sys.exit(1)

    file_path = set_environment(data_folder, data_file)
    data = load_data(file_path)
    run_menu(data, file_path)


if __name__ == "__main__":
    main()