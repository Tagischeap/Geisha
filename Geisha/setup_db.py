import sqlite3

def setup_database():
    conn = sqlite3.connect('drawings.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS drawings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lobby_id TEXT,
            event_type TEXT,
            position_x REAL,
            position_y REAL
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_database()
