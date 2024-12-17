from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import json
import os

app = Flask(__name__)

# Enable CORS for all routes, allowing any origin
CORS(app, resources={r"/*": {"origins": "*"}})

# Load JSON data
try:
    with open('export.json', 'r') as f:
        data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    data = []  # Initialize with an empty list if file not found or invalid

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/anime', methods=['GET'])
def get_anime():
    return jsonify(data)

@app.route('/api/anime', methods=['POST'])
def add_anime():
    try:
        new_entry = request.json
        if not new_entry or 'id' not in new_entry or 'animeEnglish' not in new_entry:
            return jsonify({"error": "Invalid data"}), 400

        # Validate episodes
        if 'episodes' in new_entry:
            for episode in new_entry['episodes']:
                if 'episodeNumber' not in episode:
                    return jsonify({"error": "Episode data is incomplete"}), 400

        # Check for duplicate IDs
        if any(anime['id'] == new_entry['id'] for anime in data):
            return jsonify({"error": "Anime with this ID already exists"}), 409

        # Append and save
        data.append(new_entry)
        with open('export.json', 'w') as f:
            json.dump(data, f, indent=4)

        return jsonify({"message": "Anime added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/anime/update', methods=['PUT'])
def update_anime():
    try:
        update_data = request.json
        if not update_data or 'id' not in update_data or 'episodes' not in update_data:
            return jsonify({"error": "Invalid data"}), 400

        anime_id = update_data['id']
        episodes = update_data['episodes']

        # Find the anime by ID and update episodes
        anime_found = False
        for anime in data:
            if anime['id'] == anime_id:
                anime['episodes'] = episodes
                anime_found = True
                break

        if not anime_found:
            return jsonify({"error": "Anime ID not found"}), 404

        # Save updated data back to JSON
        with open('export.json', 'w') as f:
            json.dump(data, f, indent=4)

        return jsonify({"message": "Episodes updated successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
