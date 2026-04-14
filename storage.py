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
    """
    Load workout data from disk and validate structure.

    Expected format:
    {
        "sessions": [
            {
                "id": int,
                "date": "YYYY-MM-DD",
                "exercises": [
                    {
                        "name": str,
                        "sets": [{"reps": int, "weight": number}]
                    }
                ]
            }
        ]
    }

    Returns:
    - valid data if structure is correct
    - {"sessions": []} if file is missing, corrupted, or invalid
    """
    try:
        with file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

            if not isinstance(data, dict):
                print(f"Warning: format of {file_path.name} is invalid - Starting fresh...")
                return {"sessions" : []}
            
            if "sessions" not in data or not isinstance(data["sessions"], list):
                print(f"Warning: format of {file_path.name} is invalid - Starting fresh...")
                return {"sessions" : []}
            
            for session in data["sessions"]:
                if not isinstance(session, dict):
                    return {"sessions" : []}
                if "id" not in session or "date" not in session or "exercises" not in session:
                    return {"sessions" : []}
                if not isinstance(session["exercises"], list):
                    return {"sessions" : []}
                
    except FileNotFoundError:
        print(f"File: {file_path.name} not found. Starting fresh...")
        data = {"sessions" : []}
    except json.JSONDecodeError:
        print(f"Warning: contents of {file_path.name} are corrupted. Starting fresh...")
        data = {"sessions" : []}

    return data


def save_data(file_path: Path, data):
    """Safely save data to disk using a temporary file then atomic replace.
    Prevents data corruption if the program crashes during writing."""
    temp_path = file_path.with_suffix(file_path.suffix + ".tmp")

    with temp_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    temp_path.replace(file_path)

