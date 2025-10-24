import sqlite3
from pathlib import Path
from typing import List, Mapping, Sequence

DB_PATH = Path(__file__).with_name("projects.db")


def _get_connection() -> sqlite3.Connection:
    """Return a SQLite connection configured to yield rows as mappings."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database() -> None:
    """Create the projects table if it does not exist and seed starter rows."""
    with _get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                image_filename TEXT NOT NULL
            )
            """
        )
    _seed_initial_projects()


def _seed_initial_projects() -> None:
    """Populate the database with starter records when it is empty."""
    starter_projects: Sequence[Sequence[str]] = (
        (
            "Dual Approach to Melakarta Raga Classification",
            (
                "Documented a database of 72 Melakarta ragas; extracted FFT spectrograms and "
                "compared spectral feature extraction vs neural networks to enhance raga "
                "recognition and musicological research."
            ),
            "icon_music.svg",
        ),
        (
            "AI-Powered Medical Document Verification",
            (
                "Built ML to vectorize medical documents for accurate preliminary diagnosis "
                "retrieval; matched universal medical codes with hospital claim codes to "
                "improve transparency and reduce administrative errors."
            ),
            "icon_stethoscope.svg",
        ),
        (
            "FitTrack - Smart Personal Fitness Tracker",
            (
                "Developed a fitness app with Google Fit API to surface workouts by muscle "
                "group, integrate health metrics, provide form-correction flashcards, log "
                "activity, track calories, and export progress reports."
            ),
            "icon_dumbbell.svg",
        ),
    )

    with _get_connection() as conn:
        count = conn.execute("SELECT COUNT(*) FROM projects").fetchone()[0]
        if count == 0:
            conn.executemany(
                """
                INSERT INTO projects (title, description, image_filename)
                VALUES (?, ?, ?)
                """,
                starter_projects,
            )

def list_projects() -> List[Mapping[str, str]]:
    """Return every project row ordered by creation."""
    with _get_connection() as conn:
        rows = conn.execute(
            """
            SELECT id, title, description, image_filename
            FROM projects
            ORDER BY id DESC
            """
        ).fetchall()
    return [dict(row) for row in rows]


def add_project(title: str, description: str, image_filename: str) -> None:
    """Insert a new project."""
    with _get_connection() as conn:
        conn.execute(
            """
            INSERT INTO projects (title, description, image_filename)
            VALUES (?, ?, ?)
            """,
            (title.strip(), description.strip(), image_filename.strip()),
        )

def delete_project(project_id: int) -> None:
    """Remove a project by its identifier."""
    with _get_connection() as conn:
        conn.execute("DELETE FROM projects WHERE id = ?", (project_id,))



# Ensure schema exists on import so the app can query immediately.
initialize_database()
