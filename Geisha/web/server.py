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
        # Request a token for IMDSv2
        token_response = requests.put(
            "http://169.254.169.254/latest/api/token",
            headers={"X-aws-ec2-metadata-token-ttl-seconds": "21600"},
            timeout=2
        )
        token_response.raise_for_status()
        token = token_response.text
        
        # Use the token to retrieve the public IP
        ip_response = requests.get(
            "http://169.254.169.254/latest/meta-data/public-ipv4",
            headers={"X-aws-ec2-metadata-token": token},
            timeout=2
        )
        ip_response.raise_for_status()
        return ip_response.text
    except requests.RequestException as e:
        logging.error("Failed to retrieve public IP from AWS metadata service", exc_info=e)
        return "localhost"

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
