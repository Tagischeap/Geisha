# web/server.py
import requests
from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO, emit
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a secure key
socketio = SocketIO(app)

def get_public_ip():
    try:
        # Check if we're on AWS or a remote server by trying to access the AWS metadata service
        # This will fail if not on AWS, so we use localhost in that case
        response = requests.get("http://169.254.169.254/latest/meta-data/public-ipv4", timeout=1)
        response.raise_for_status()
        return response.text
    except requests.RequestException:
        return "localhost"  # Use localhost for local testing

# Get the server's public IP at startup
public_ip = get_public_ip()

# Store active lobbies in memory (for a persistent setup, use a database)
active_lobbies = {}

@app.route('/api/create-lobby', methods=['POST'])
def create_lobby():
    # Generate a unique lobby ID and URL
    lobby_id = str(uuid.uuid4())
    lobby_url = f"http://{public_ip}:5000/lobby/{lobby_id}"  # Use the dynamic IP
    
    # Register the lobby
    active_lobbies[lobby_id] = {"players": []}

    # Return the lobby URL as JSON for the bot to share
    return jsonify({"lobby_url": lobby_url})

@app.route('/api/get-lobby-url', methods=['GET'])
def get_lobby_url():
    # Provide the base URL for lobby creation
    return jsonify({"lobby_base_url": f"http://{public_ip}:5000/api/create-lobby"})

@app.route('/lobby/<lobby_id>')
def lobby(lobby_id):
    # Check if the lobby exists
    if lobby_id in active_lobbies:
        return render_template('lobby.html', lobby_id=lobby_id)
    return "Lobby not found.", 404

@socketio.on('draw')
def handle_draw_event(data):
    # Broadcast the drawing event to all clients in the same lobby
    emit('draw', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
