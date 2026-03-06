from pathlib import Path
import sys
from storage import load_config, set_environment, load_data, save_data
from logic import add_exercise, log_entry, delete_exercise, summary_lines


def run_menu(data: dict, file_path: Path) -> None:
    """Run the interactive CLI menu for the gym log.
    Allows the user to add exercises, log weights, view summaries,
    delete exercises, and save progress to disk.
    """
    while True:
        print("\nGym Log")
        print("-------")
        print("1) Add Exercise")
        print("2) Log Exercise Weight")
        print("3) View Summary")
        print("4) Delete Exercise")
        print("5) Exit & Save")

        choice = input("Choice: ").strip()

        if choice == '1':
            exercise = input("Exercise name: ").strip().lower()
            if not exercise:
                print("Exercise name cannot be empty.")
                continue
            
            result = add_exercise(data, exercise)
            if result:
                save_data(file_path, data)
                print(f"{exercise} added.")
            else:
                print(f"{exercise} already exists.")
            
        elif choice == '2':
            exercise = input("Exercise name: ").strip().lower()
            if not exercise:
                print("Exercise name cannot be empty.")
                continue
            if exercise not in data:
                print(f"{exercise} hasn't been added yet.")
                continue

            try:
                weight = float(input("Log weight: ").strip())
            except ValueError:
                print("Weight value must be a valid number.")
                continue

            if weight <= 0:
                print("Weight value must be greater than 0.")
                continue

            result = log_entry(data, exercise, weight)
            if result:
                save_data(file_path, data)
                print("Good job! New weight logged.")

        elif choice == '3':

            print("\nGym Log Summary")
            print("---------------")
            lines = summary_lines(data)
            if not lines:
                print("No exercises have been added yet.")
                continue
            for line in lines:
                print(line)
                print()

        elif choice == '4':
            exercise = input("Exercise name: ").strip().lower()
            if not exercise:
                print("Exercise name cannot be empty.")
                continue

            confirmation = input("Are you sure? (y/n): ").strip().lower()
            if confirmation == 'y':
                result = delete_exercise(data, exercise)
            elif confirmation == 'n':
                print("Canceled.")
                continue
            else:
                print("Invalid response.")
                continue

            if result:
                save_data(file_path, data)
                print(f"Deleted: {exercise}")
            else:
                print(f"{exercise} not found.")

        elif choice == '5':
            save_data(file_path, data)
            print("Saved. Goodbye!")
            break

        else:
            print("Invalid choice. Menu options are 1, 2, 3, 4, or 5.")


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