
from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO
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
    return lobby_manager.api_create_lobby(public_ip)

@app.route('/api/active-lobbies', methods=['GET'])
def api_active_lobbies():
    return lobby_manager.api_list_lobbies()

@app.route('/lobby/<lobby_id>')
def lobby_page(lobby_id):
    return lobby_manager.render_lobby_page(lobby_id)

# Socket.IO Events
@socketio.on('join_lobby')
def on_join_lobby(data):
    lobby_manager.on_join_lobby(data)

@socketio.on('draw')
def handle_draw_event(data):
    lobby_manager.handle_draw_event(data)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
