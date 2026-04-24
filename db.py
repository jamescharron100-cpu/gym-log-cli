from datetime import date


def init_db(conn):
    """Create required database tables if they do not already exist."""
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS exercises (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        FOREIGN KEY (session_id) REFERENCES sessions(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        exercise_id INTEGER NOT NULL,
        reps INTEGER NOT NULL,
        weight REAL NOT NULL,
        FOREIGN KEY (exercise_id) REFERENCES exercises(id)
    )
    """)

    conn.commit()


def start_session(conn):
    cursor = conn.cursor()

    today = str(date.today())

    cursor.execute(
        "INSERT INTO sessions (date) VALUES (?)",
        (today,)
    )

    conn.commit()

    return cursor.lastrowid


def add_exercise(conn, session_id, name):
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO exercises (session_id, name) VALUES (?, ?)",
        (session_id, name)
    )

    conn.commit()

    return cursor.lastrowid


def add_set(conn, exercise_id, reps, weight):
    """Add a completed set to an exercise and return the new set id."""
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO sets (exercise_id, reps, weight) VALUES (?, ?, ?)",
        (exercise_id, reps, weight)
    )

    conn.commit()

    return cursor.lastrowid


def get_sessions(conn):
    cursor = conn.cursor()

    cursor.execute("SELECT id, date FROM sessions ORDER BY id DESC")
    sessions = cursor.fetchall()

    return sessions


def get_exercises_for_session(conn, session_id):
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, name FROM exercises WHERE session_id = ? ORDER BY id",
        (session_id,)
    )

    return cursor.fetchall()


def get_sets_for_exercise(conn, exercise_id):
    """Return all sets for a specific exercise."""
    cursor = conn.cursor()

    cursor.execute(
        "SELECT reps, weight FROM sets WHERE exercise_id = ? ORDER BY id",
        (exercise_id,)
    )

    return cursor.fetchall()


def delete_session(conn, session_id):
    """Delete a session and all related exercises and sets."""
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM exercises WHERE session_id = ?",
        (session_id,)
    )
    exercises = cursor.fetchall()

    for exercise in exercises:
        exercise_id = exercise[0]
        cursor.execute(
            "DELETE FROM sets WHERE exercise_id = ?",
            (exercise_id,)
        )

    cursor.execute(
        "DELETE FROM exercises WHERE session_id = ?",
        (session_id,)
    )

    cursor.execute(
        "DELETE FROM sessions WHERE id = ?",
        (session_id,)
    )
    
    conn.commit()

    return cursor.rowcount > 0


def get_exercise_history(conn):
    """Return exercise history grouped by exercise names."""
    cursor = conn.cursor()

    cursor.execute("""
    SELECT name, COUNT(DISTINCT session_id)
    FROM exercises
    GROUP BY name
    ORDER BY name
    """)

    return cursor.fetchall()