# web/lobby_manager.py
import uuid
import logging

active_lobbies = {}

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

def add_player_to_lobby(lobby_id, username):
    lobby = get_lobby(lobby_id)
    if lobby and username not in lobby["players"]:
        lobby["players"].append(username)
        return True
    return False
