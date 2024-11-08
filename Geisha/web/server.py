# web/server.py
import requests
import logging
import socket
from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, emit, join_room
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a secure key
socketio = SocketIO(app)

logging.basicConfig(level=logging.INFO)

def is_aws_environment():
    try:
        socket.create_connection(("169.254.169.254", 80), timeout=1)
        return True
    except OSError:
        return False

def get_public_ip():
    if is_aws_environment():
        try:
            token_response = requests.put(
                "http://169.254.169.254/latest/api/token",
                headers={"X-aws-ec2-metadata-token-ttl-seconds": "21600"},
                timeout=1
            )
            token = token_response.text
            ip_response = requests.get(
                "http://169.254.169.254/latest/meta-data/public-ipv4",
                headers={"X-aws-ec2-metadata-token": token},
                timeout=1
            )
            ip_response.raise_for_status()
            return ip_response.text
        except requests.exceptions.RequestException as e:
            logging.error("Failed to retrieve public IP from AWS metadata service", exc_info=e)
    
    try:
        fallback_response = requests.get("https://api.ipify.org?format=json", timeout=1)
        fallback_response.raise_for_status()
        return fallback_response.json()["ip"]
    except requests.exceptions.RequestException as fallback_e:
        logging.error("Failed to retrieve public IP from fallback service", exc_info=fallback_e)
        return "IP retrieval failed"

public_ip = get_public_ip()
logging.info(f"Public IP: {public_ip}")

active_lobbies = {}

# Serve the main page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/diagnostic', methods=['GET'])
def diagnostic():
    # This will display the current state of all active lobbies
    return jsonify(active_lobbies)

@app.route('/api/create-lobby', methods=['POST'])
def create_lobby():
    lobby_id = str(uuid.uuid4())
    lobby_url = f"http://{public_ip}:5000/lobby/{lobby_id}"
    active_lobbies[lobby_id] = {"players": []}
    logging.info(f"Lobby created with ID: {lobby_id}")
    return jsonify({"lobby_url": lobby_url, "lobby_id": lobby_id})

@app.route('/api/active-lobbies', methods=['GET'])
def active_lobbies_list():
    logging.info(f"Active lobbies: {list(active_lobbies.keys())}")
    return jsonify(list(active_lobbies.keys()))

@app.route('/lobby/<lobby_id>')
def lobby(lobby_id):
    if lobby_id in active_lobbies:
        return render_template('lobby.html', lobby_id=lobby_id)
    logging.warning(f"Attempted to access non-existent lobby: {lobby_id}")
    return "Lobby not found.", 404

@app.route('/api/view-lobby/<lobby_id>', methods=['GET'])
def view_lobby(lobby_id):
    if lobby_id in active_lobbies:
        logging.info(f"Viewing players in lobby '{lobby_id}': {active_lobbies[lobby_id]['players']}")
        return jsonify({"players": active_lobbies[lobby_id]["players"]})
    else:
        logging.warning(f"Lobby '{lobby_id}' not found for viewing")
        return jsonify({"error": "Lobby not found"}), 404

@socketio.on('join_lobby')
def on_join_lobby(data):
    lobby_id = data['lobby_id']
    username = data['username']
    logging.info(f"User '{username}' attempting to join lobby '{lobby_id}'")
    
    if lobby_id in active_lobbies:
        # Check if the user is already in the lobby to avoid duplicates
        if username not in active_lobbies[lobby_id]["players"]:
            active_lobbies[lobby_id]["players"].append(username)
            logging.info(f"User '{username}' added to lobby '{lobby_id}'")
        else:
            logging.info(f"User '{username}' is already in lobby '{lobby_id}'")

        # Join the lobby room and notify other users
        join_room(lobby_id)
        emit('user_joined', {'username': username, 'players': active_lobbies[lobby_id]["players"]}, room=lobby_id)
    else:
        emit('error', {'message': 'Lobby not found'})
        logging.warning(f"Lobby '{lobby_id}' not found for user '{username}'")

@socketio.on('draw')
def handle_draw_event(data):
    lobby_id = data['lobby_id']
    emit('draw', data, room=lobby_id)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
