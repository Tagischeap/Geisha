# web/db_utils.py
import os
import sqlite3
import logging
from contextlib import contextmanager

# Path to database
DB_PATH = os.path.join(os.path.dirname(__file__), 'drawings.db')

# Context manager for database connection
@contextmanager
def connect_db():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    try:
        yield cursor
        connection.commit()
    except sqlite3.Error as e:
        connection.rollback()
        logging.error(f"Database error: {e}")
    finally:
        connection.close()

# Database initialization function
def initialize_db():
    """Initialize the database with the drawings table if it does not exist."""
    with connect_db() as conn:
        tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='drawings';").fetchall()
        if not tables:
            logging.info("Table 'drawings' does not exist. Creating table.")
        else:
            logging.info("Table 'drawings' is present.")
        conn.execute('''
            CREATE TABLE IF NOT EXISTS drawings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lobby_id TEXT,
                event_type TEXT,
                pos_x INTEGER,
                pos_y INTEGER
            )
        ''')

# Save drawing event function using CRUD pattern
def save_draw_event(lobby_id, event_type, pos):
    logging.debug(f"Attempting to save event to drawings: {lobby_id}, {event_type}, {pos}")
    data = {
        'lobby_id': lobby_id,
        'event_type': event_type,
        'pos_x': pos['x'],
        'pos_y': pos['y']
    }
    try:
        with connect_db() as conn:
            conn.execute('''
                INSERT INTO drawings (lobby_id, event_type, pos_x, pos_y)
                VALUES (:lobby_id, :event_type, :pos_x, :pos_y)
            ''', data)
        logging.debug("Save operation successful.")
    except Exception as e:
        logging.error(f"Error saving draw event: {e}")

# Load drawing history function using CRUD pattern
def load_drawing_history(lobby_id):
    logging.debug(f"Attempting to load drawing history for lobby {lobby_id}")
    try:
        with connect_db() as conn:
            events = conn.execute('''
                SELECT event_type, pos_x, pos_y FROM drawings
                WHERE lobby_id = ?
            ''', (lobby_id,)).fetchall()
        
        logging.debug(f"Loaded events: {events}")  # Log the raw query result
        return [{'type': row['event_type'], 'data': {'pos': {'x': row['pos_x'], 'y': row['pos_y']}}} for row in events]
    except Exception as e:
        logging.error(f"Error loading drawing history: {e}")
        return []

# Run initialize_db once at startup
initialize_db()
