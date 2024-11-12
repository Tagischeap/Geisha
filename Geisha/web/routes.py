# web/routes.py
from flask import jsonify, request
from app import app
import lobby_manager

# Route to set the game type for a lobby
@app.route('/api/lobby/<lobby_id>/set-game', methods=['POST'])
def set_game(lobby_id):
    game_type = request.json.get("game_type")
    if lobby_manager.set_game_type(lobby_id, game_type):
        return jsonify({"message": f"Game type set to '{game_type}' in lobby '{lobby_id}'"})
    return jsonify({"error": "Failed to set game type"}), 400

# Route to update game settings for a lobby
@app.route('/api/lobby/<lobby_id>/update-settings', methods=['POST'])
def update_game_settings(lobby_id):
    settings = request.json.get("settings", {})
    if lobby_manager.update_game_settings(lobby_id, settings):
        return jsonify({"message": "Game settings updated", "settings": settings})
    return jsonify({"error": "Failed to update settings"}), 400

# Route to start the game in a lobby
@app.route('/api/lobby/<lobby_id>/start-game', methods=['POST'])
def start_game(lobby_id):
    if lobby_manager.start_game(lobby_id):
        return jsonify({"message": "Game started"})
    return jsonify({"error": "Failed to start game"}), 400
