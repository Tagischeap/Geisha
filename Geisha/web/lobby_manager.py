import uuid
import logging
from flask import jsonify, render_template
from flask_socketio import emit, join_room

# Store active lobbies
active_lobbies = {}

# Lobby management functions
def create_lobby(public_ip):
    lobby_id = str(uuid.uuid4())
    lobby_url = f"http://{public_ip}:5000/lobby/{lobby_id}"
    active_lobbies[lobby_id] = {"players": []}
    logging.info(f"Lobby created with ID: {lobby_id}")
    return {"lobby_url": lobby_url, "lobby_id": lobby_id}

def list_lobbies():
    logging.info(f"Active lobbies: {list(active_lobbies.keys())}")
    return list(active_lobbies.keys())

def get_lobby(lobby_id):
    return active_lobbies.get(lobby_id)

def render_lobby_page(lobby_id):
    lobby = get_lobby(lobby_id)
    if lobby:
        return render_template('lobby.html', lobby_id=lobby_id)
    logging.warning(f"Attempted to access non-existent lobby: {lobby_id}")
    return "Lobby not found.", 404

# Flask API route handlers
def api_create_lobby(public_ip):
    lobby_info = create_lobby(public_ip)
    return jsonify(lobby_info)

def api_list_lobbies():
    return jsonify(list_lobbies())

# Socket.IO event handlers
def on_join_lobby(data):
    lobby_id = data['lobby_id']
    username = data['username']
    lobby = get_lobby(lobby_id)
    
    if lobby:
        if username not in lobby["players"]:
            lobby["players"].append(username)
        join_room(lobby_id)
        emit('user_joined', {'username': username, 'players': lobby["players"]}, room=lobby_id)
    else:
        emit('error', {'message': 'Lobby not found'})
        logging.warning(f"Lobby '{lobby_id}' not found for user '{username}'")

def handle_draw_event(data):
    lobby_id = data['lobby_id']
    emit('draw', data, room=lobby_id)
