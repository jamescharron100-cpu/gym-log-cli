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


def parse_positive_int(raw):
    """Parse user input into a positive integer.
    Returns int if valid, otherwise None."""
    try:
        value = int(raw)
    except (TypeError, ValueError):
        return None
    if value <= 0:
        return None
    return value


def next_session_id(data: dict) -> int:
    """Return the next available session id based on existing sessions."""
    if not data["sessions"]:
        return 1

    max_id = 0
    for session in data["sessions"]:
        if session["id"] > max_id:
            max_id = session["id"]
    return max_id + 1


def create_session(data: dict) -> dict:
    next_id = next_session_id(data)
    today = date.today().isoformat()

    session = {
        "id": next_id,
        "date": today,
        "exercises": []
    }

    data["sessions"].append(session)

    return session


def delete_session(data: dict, session_id: int) -> bool:
    """Remove a session by its id.
    Returns True if a session was removed, False otherwise."""
    sessions = data.get("sessions", [])
    for i, session in enumerate(sessions):
        if session.get("id") == session_id:
            sessions.pop(i)
            return True
    return False


def add_exercise_to_session(session: dict, exercise_name: str) -> bool:
    name = normalize_exercise(exercise_name)
    if not name:
        return False

    for exercise in session["exercises"]:
        if exercise["name"] == name:
            return False

    session["exercises"].append({
        "name": name,
        "sets": []
    })

    return True


def current_session_lines(session: dict) -> list[str]:
    """Build readable lines for displaying the current workout session."""
    lines = []
    header = f"Session {session['id']} - {session['date']}"
    divider = "----------------------"

    lines.append(header)
    lines.append(divider)

    if not session["exercises"]:
        lines.append("No exercises logged in this session yet.")
        return lines

    for exercise in session["exercises"]:
        lines.append(exercise["name"])

        for i, set_entry in enumerate(exercise["sets"], start=1):
            reps = set_entry["reps"]
            weight = normalize_weight(set_entry["weight"])
            lines.append(f"  Set {i}: {reps} reps @ {weight} lbs")

    return lines


def session_history_lines(data: dict) -> list[str]:
    """Build readable lines for displaying all past workout sessions."""
    lines = []

    sessions = data.get("sessions", [])
    if not sessions:
        lines.append("No sessions found.")
        return lines

    for session in reversed(sessions):
        session_id = session.get("id")
        session_date = session.get("date", "unknown")
        exercises = session.get("exercises", [])
        exercise_count = len(exercises)

        label = "exercise" if exercise_count == 1 else "exercises"
        lines.append(f"Session {session_id} - {session_date} ({exercise_count} {label})")
    
    return lines


def exercise_history_lines(data: dict) -> list[str]:
    """Build readable lines for displaying exercise history across all sessions."""
    lines = []
    sessions = data.get("sessions", [])

    exercise_counts = {}
    for session in sessions:
        exercises = session.get("exercises", [])
        for exercise in exercises:
            name = exercise.get("name")
            if not isinstance(name, str) or not name:
                continue
            exercise_counts[name] = exercise_counts.get(name, 0) + 1

    if not exercise_counts:
        lines.append("No exercise history found.")
        return lines

    for name in sorted(exercise_counts.keys()):
        count = exercise_counts[name]
        label = "session" if count == 1 else "sessions"
        lines.append(f"{name}: logged in {count} {label}")

    return lines