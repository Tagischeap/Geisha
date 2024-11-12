# web/server.py
import sqlite3
from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, emit, join_room
import logging
from config import SECRET_KEY
from ip_utils import get_public_ip
import lobby_manager

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
socketio = SocketIO(app)

# Set up logging
logging.basicConfig(level=logging.INFO)
public_ip = get_public_ip()
logging.info(f"Public IP: {public_ip}")

# Initialize SQLite connection
def get_db_connection():
    conn = sqlite3.connect('drawings.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

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
    with get_db_connection() as conn:
        conn.execute('''
            INSERT INTO drawings (lobby_id, event_type, pos_x, pos_y)
            VALUES (?, ?, ?, ?)
        ''', (lobby_id, event_type, pos['x'], pos['y']))
        conn.commit()
        logging.info(f"Saved draw event in lobby {lobby_id} with type {event_type} and pos {pos}")

def load_drawing_history(lobby_id):
    with get_db_connection() as conn:
        events = conn.execute('''
            SELECT event_type, pos_x, pos_y FROM drawings
            WHERE lobby_id = ?
        ''', (lobby_id,)).fetchall()
        logging.info(f"Loaded drawing history for lobby {lobby_id}")
        return [{'type': row['event_type'], 'data': {'pos': {'x': row['pos_x'], 'y': row['pos_y']}}} for row in events]

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/create-lobby', methods=['POST'])
def api_create_lobby():
    lobby_info = lobby_manager.create_lobby(public_ip)
    return jsonify(lobby_info)

@app.route('/api/active-lobbies', methods=['GET'])
def api_active_lobbies():
    return jsonify(lobby_manager.list_lobbies())

@app.route('/api/view-lobby/<lobby_id>', methods=['GET'])
def view_lobby(lobby_id):
    lobby = lobby_manager.get_lobby(lobby_id)
    if lobby:
        logging.info(f"Viewing players in lobby '{lobby_id}': {lobby['players']}")
        return jsonify({"players": lobby["players"]})
    else:
        logging.warning(f"Lobby '{lobby_id}' not found for viewing")
        return jsonify({"error": "Lobby not found"}), 404

@app.route('/lobby/<lobby_id>')
def lobby_page(lobby_id):
    lobby = lobby_manager.get_lobby(lobby_id)
    if lobby:
        return render_template('lobby.html', lobby_id=lobby_id)
    logging.warning(f"Attempted to access non-existent lobby: {lobby_id}")
    return "Lobby not found.", 404

@socketio.on('join_lobby')
def on_join_lobby(data):
    lobby_id = data['lobby_id']
    username = data['username']
    join_room(lobby_id)

    # Load drawing history
    history = load_drawing_history(lobby_id)
    logging.info(f"Loaded drawing history for lobby {lobby_id}: {history}")
    
    # Send existing drawing history to the user who just joined
    for event in history:
        logging.info(f"Emitting event {event['type']} with data {event['data']} to room {request.sid}")
        emit(event['type'], event['data'], room=request.sid)


@socketio.on('draw_start')
def handle_draw_start(data):
    lobby_id = data.get('lobby_id')
    pos = data.get('pos')
    if lobby_id and pos:
        save_draw_event(lobby_id, 'draw_start', pos)
        emit('draw_start', {'pos': pos}, room=lobby_id)

@socketio.on('draw')
def handle_draw_event(data):
    lobby_id = data.get('lobby_id')
    pos = data.get('pos')
    if lobby_id and pos:
        save_draw_event(lobby_id, 'draw', pos)
        emit('draw', {'pos': pos}, room=lobby_id)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
