# web/app.py
from flask import Flask
from flask_socketio import SocketIO
from config import SECRET_KEY

# Initialize Flask and Socket.IO
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
socketio = SocketIO(app)
