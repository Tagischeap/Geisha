# web/server.py
from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, emit, join_room
import logging
from config import SECRET_KEY
from ip_utils import get_public_ip
import lobby_manager
from db_utils import load_drawing_history, save_draw_event 


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
socketio = SocketIO(app)

# Set up logging
logging.basicConfig(level=logging.INFO)
public_ip = get_public_ip()
logging.info(f"Public IP: {public_ip}")

@socketio.on('join_lobby')
def on_join_lobby(data):
    lobby_id = data['lobby_id']
    username = data['username']
    join_room(lobby_id)
    
    # Load drawing history and log the output
    history = load_drawing_history(lobby_id)
    logging.info(f"Loaded drawing history for lobby {lobby_id}: {history}")
    
    # Emit the full drawing history as a single event to the joining client
    emit('drawing_history', {'history': history}, room=request.sid)
    logging.info(f"Emitted drawing history to {request.sid}")


@socketio.on('draw_start')
def handle_draw_start(data):
    logging.info(f"draw_start event with data: {data}")
    lobby_id = data.get('lobby_id')
    pos = data.get('pos')
    if lobby_id and pos:
        save_draw_event(lobby_id, 'draw_start', pos)
        emit('draw_start', {'lobby_id': lobby_id, 'pos': pos}, room=lobby_id)

@socketio.on('draw')
def handle_draw_event(data):
    logging.info(f"draw event with data: {data}")
    lobby_id = data.get('lobby_id')
    pos = data.get('pos')
    if lobby_id and pos:
        save_draw_event(lobby_id, 'draw', pos)
        emit('draw', {'lobby_id': lobby_id, 'pos': pos}, room=lobby_id)

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

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
