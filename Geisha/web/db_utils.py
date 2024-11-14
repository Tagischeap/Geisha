# web/db_utils.py
import os
import sqlite3
import logging

DB_PATH = os.path.join(os.path.dirname(__file__), 'drawings.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

with get_db_connection() as conn:
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='drawings';").fetchall()
    if not tables:
        print("Table 'drawings' does not exist.")
    else:
        print("Table 'drawings' is present.")

# Create a table if it doesn’t exist
with get_db_connection() as conn:
    conn.execute('''
        CREATE TABLE IF NOT EXISTS drawings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lobby_id TEXT,
            event_type TEXT,
            pos_x INTEGER,
            pos_y INTEGER
        )
    ''')
    conn.commit()

# Functions to save and load drawing events in SQLite
def save_draw_event(lobby_id, event_type, pos):
    logging.debug(f"Attempting to save event to drawings: {lobby_id}, {event_type}, {pos}")
    try:
        with get_db_connection() as conn:
            conn.execute('''
                INSERT INTO drawings (lobby_id, event_type, pos_x, pos_y)
                VALUES (?, ?, ?, ?)
            ''', (lobby_id, event_type, pos['x'], pos['y']))
            conn.commit()
        logging.debug("Save operation successful.")
    except Exception as e:
        logging.error(f"Error saving draw event: {e}")

def load_drawing_history(lobby_id):
    logging.debug(f"Attempting to load drawing history for lobby {lobby_id}")
    try:
        with get_db_connection() as conn:
            events = conn.execute('''
                SELECT event_type, pos_x, pos_y FROM drawings
                WHERE lobby_id = ?
            ''', (lobby_id,)).fetchall()
        logging.debug("Load operation successful.")
        return [{'type': row['event_type'], 'data': {'pos': {'x': row['pos_x'], 'y': row['pos_y']}}} for row in events]
    except Exception as e:
        logging.error(f"Error loading drawing history: {e}")
        return []
