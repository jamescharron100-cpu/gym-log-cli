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