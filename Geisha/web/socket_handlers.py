# web/socket_handlers.py
from server import socketio
from flask import request
from flask_socketio import emit, join_room
from db_utils import save_draw_event, load_drawing_history
import lobby_manager
import logging

@socketio.on("connect")
def on_connect():
    logging.info("Client connected directly through socket_handlers.")

@socketio.on('set_game')
def handle_set_game(data):
    lobby_id = data['lobby_id']
    game_type = data['game_type']
    if lobby_manager.set_game_type(lobby_id, game_type):
        emit('game_type_set', {"lobby_id": lobby_id, "game_type": game_type}, room=lobby_id)

@socketio.on('update_settings')
def handle_update_settings(data):
    lobby_id = data['lobby_id']
    settings = data['settings']
    if lobby_manager.update_game_settings(lobby_id, settings):
        emit('settings_updated', {"lobby_id": lobby_id, "settings": settings}, room=lobby_id)

@socketio.on('start_game')
def handle_start_game(data):
    lobby_id = data['lobby_id']
    if lobby_manager.start_game(lobby_id):
        emit('game_started', {"lobby_id": lobby_id}, room=lobby_id)
