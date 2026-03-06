from datetime import date

def normalize_weight(weight):
    """Format whole-number floats as ints for cleaner output/display."""
    if isinstance(weight, float) and weight.is_integer():
        return int(weight)
    return weight 


def normalize_exercise(exercise: str) -> str:
    """Normalize exercise names by stripping whitespace and lowercasing text."""
    if not isinstance(exercise, str):
        return ""
    return exercise.strip().lower()


def parse_weight(raw):
    """Parse user input into a positive numeric weight.
    Returns int/float if valid, otherwise None."""
    try:
        weight = float(raw)
    except (TypeError, ValueError):
        return None
    if weight <= 0:
        return None
    return int(weight) if weight.is_integer() else weight


def add_exercise(data: dict, exercise: str) -> bool:
    """Add a new exercise with an empty entry history.
    Returns False if the name is invalid or already exists."""
    exercise = normalize_exercise(exercise)
    if not exercise:
        return False
    if exercise in data:
        return False
    data[exercise] = []
    return True


def log_entry(data: dict, exercise: str, weight) -> bool:
    """Append a new dated weight entry to an existing exercise.
    Returns False if the exercise is missing or the weight is invalid."""
    exercise = normalize_exercise(exercise)
    if exercise not in data:
        return False
    
    weight = parse_weight(weight)
    if weight is None:
        return False

    data[exercise].append({"date": date.today().isoformat(), "weight": weight})
    return True


def delete_exercise(data: dict, exercise: str) -> bool:
    """Delete an exercise and all of its logged history.
    Returns False if the exercise does not exist."""
    exercise = normalize_exercise(exercise)
    if exercise not in data:
        return False
    del data[exercise]
    return True

def summary_lines(data: dict) -> list[str]:
    """Build a user-facing summary showing the latest weight and progress.
    Each exercise is summarized using its most recent entry and previous entry if available."""
    lines = []
    for exercise in sorted(data.keys()):
        entries = data.get(exercise)
        if not isinstance(entries, list) or not entries:
            continue
        
        last_entry = entries[-1]
        last_weight = last_entry.get("weight")
        last_date = last_entry.get("date")
        if not isinstance(last_date, str):
            last_date = "unknown"

        if not isinstance(last_weight, (int, float)):
            continue

        weight_display = normalize_weight(last_weight)
        base_line = f"{exercise}: {weight_display} lbs ({last_date})"

        if len(entries) >= 2:
            prev_entry = entries[-2]
            prev_weight = prev_entry.get("weight")
            if isinstance(prev_weight, (int, float)):
                progress = last_weight - prev_weight

                if progress > 0:
                    progress_text = f"+{normalize_weight(progress)}"
                elif progress < 0:
                    progress_text = f"{normalize_weight(progress)}"
                else:
                    progress_text = "No change"

                lines.append(f"{base_line}\nProgress: {progress_text} lbs")
                continue

        if len(entries) == 1:
            lines.append(f"{base_line}\nProgress: First Entry")
        else:
            lines.append(base_line)
            
    return lines
