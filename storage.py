from pathlib import Path
import json


def load_config(config_path: Path):
    """Load and parse the JSON configuration file.
    Returns the config dictionary or None if the file is not found or invalid."""
    try:
        with config_path.open("r", encoding="utf-8") as file:
            config = json.load(file)
    except FileNotFoundError:
        print(f"Error: {config_path} not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: {config_path} file is corrupted.")
        return None

    return config


def set_environment(data_folder: str, data_file: str) -> Path:
    """Ensure the data directory exists and return the full path to the data file."""
    base_dir = Path(__file__).resolve().parent
    data_dir = base_dir / data_folder
    data_dir.mkdir(parents=True, exist_ok=True)
    file_path = data_dir / data_file
    return file_path


def load_data(file_path: Path):
    """Load workout data from disk and validate its structure.
    Returns a dictionary shaped like:
    {exercise: [{"date": "YYYY-MM-DD", "weight": number}, ...]}
    If the file is not found or malformed, an empty dict is returned instead."""
    try:
        with file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

            if not isinstance(data, dict):
                print(f"Warning: format of {file_path.name} is invalid - Starting fresh...")
                return {}
            
            for exercise, entries in data.items():
                if not isinstance(exercise, str) or not isinstance(entries, list):
                    print(f"Warning: format of {file_path.name} is invalid - Starting fresh...")
                    return {}
                
                for entry in entries:
                    if not isinstance(entry, dict) or "date" not in entry or "weight" not in entry:
                        print(f"Warning: format of {file_path.name} is invalid - Starting fresh...")
                        return {}

    except FileNotFoundError:
        print(f"File: {file_path.name} not found. Starting fresh...")
        data = {}
    except json.JSONDecodeError:
        print(f"Warning: contents of {file_path.name} are corrupted. Starting fresh...")
        data = {}

    return data


def save_data(file_path: Path, data):
    """Safely save data to disk using a temporary file then atomic replace.
    Prevents data corruption if the program crashes during writing."""
    temp_path = file_path.with_suffix(file_path.suffix + ".tmp")

    with temp_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    temp_path.replace(file_path)

