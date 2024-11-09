import uuid
import logging

# Dictionary to store active lobbies
active_lobbies = {}

def create_lobby(public_ip):
    lobby_id = str(uuid.uuid4())
    lobby_url = f"http://{public_ip}:5000/lobby/{lobby_id}"
    active_lobbies[lobby_id] = {
        "players": [],
        "game": {
            "type": None,            # Game type (e.g., drawing game)
            "status": "waiting",     # Game status: waiting, active, or finished
            "settings": {}           # Game-specific settings (e.g., number of rounds)
        }
    }
    logging.info(f"Lobby created with ID: {lobby_id}")
    return {"lobby_url": lobby_url, "lobby_id": lobby_id}

def list_lobbies():
    return list(active_lobbies.keys())

def get_lobby(lobby_id):
    return active_lobbies.get(lobby_id)

def add_player_to_lobby(lobby_id, username):
    lobby = get_lobby(lobby_id)
    if lobby and username not in lobby["players"]:
        lobby["players"].append(username)
        return True
    return False

# Game management functions
def set_game_type(lobby_id, game_type):
    lobby = get_lobby(lobby_id)
    if lobby:
        lobby["game"]["type"] = game_type
        lobby["game"]["status"] = "waiting"
        return True
    return False

def update_game_settings(lobby_id, settings):
    lobby = get_lobby(lobby_id)
    if lobby:
        lobby["game"]["settings"].update(settings)
        return True
    return False

def start_game(lobby_id):
    lobby = get_lobby(lobby_id)
    if lobby and lobby["game"]["type"]:
        lobby["game"]["status"] = "active"
        logging.info(f"Game started in lobby '{lobby_id}' with settings: {lobby['game']}")
        return True
    return False
