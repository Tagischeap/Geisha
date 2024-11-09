# web/server.py
from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, emit, join_room
import logging
from config import SECRET_KEY
from ip_utils import get_public_ip
import lobby_manager

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
socketio = SocketIO(app)

logging.basicConfig(level=logging.INFO)
public_ip = get_public_ip()
logging.info(f"Public IP: {public_ip}")

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

# Socket.IO Events
@socketio.on('join_lobby')
def on_join_lobby(data):
    lobby_id = data['lobby_id']
    username = data['username']
    success = lobby_manager.add_player_to_lobby(lobby_id, username)
    
    if success:
        join_room(lobby_id)
        emit('user_joined', {'username': username, 'players': lobby_manager.get_lobby(lobby_id)["players"]}, room=lobby_id)
    else:
        emit('error', {'message': 'Lobby not found or user already in lobby'})
        logging.warning(f"Failed join attempt for lobby '{lobby_id}' by user '{username}'")

@socketio.on('draw')
def handle_draw_event(data):
    lobby_id = data['lobby_id']
    emit('draw', data, room=lobby_id)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
