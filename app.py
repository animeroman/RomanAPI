from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import json
from functools import wraps  # Import wraps to preserve original function names

app = Flask(__name__)
# Enable CORS with specific origins
CORS(app, supports_credentials=True, origins=["http://127.0.0.1:5000", "http://127.0.0.1:8080", "https://apiromanlast.fly.dev"], methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

# Load your JSON data
with open('export.json', 'r') as f:
    data = json.load(f)

# Define the API key
API_KEY = "SkYCKXd3lZwgW7SDZZBcQOkHoCw4ggczeGFAmtbdUeJFTMWua3KYW9RDw36Esppx1c6Kp6wfy0fTh1YdvUTMF5faEyurPItvRwUKrkiZtT8DMO33yiHEppNcusg85dYC"

def require_api_key(f):
    """
    Decorator to require an API key for a route.
    """
    @wraps(f)  # Use wraps to preserve the original function's name
    def decorated_function(*args, **kwargs):
        # Retrieve the Authorization header
        api_key = request.headers.get("Authorization")
        print("Received API Key:", api_key)  # Debugging: Log received API key
        if not api_key or api_key != f"Bearer {API_KEY}":
            return jsonify({"error": "Unauthorized access, invalid API key"}), 403
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/anime', methods=['GET'])
def get_anime():
    print("Headers received for /api/anime:", request.headers)  # Debugging: Log headers
    return jsonify(data)

@app.route('/api/anime', methods=['POST'])
@require_api_key
def add_anime():
    try:
        new_entry = request.json
        print("Received data for POST /api/anime:", new_entry)  # Debugging log

        if not new_entry or 'id' not in new_entry or 'animeEnglish' not in new_entry:
            return jsonify({"error": "Invalid data"}), 400

        # Validate episodes
        if 'episodes' in new_entry:
            for episode in new_entry['episodes']:
                if 'episodeNumber' not in episode:
                    return jsonify({"error": "Episode data is incomplete"}), 400

        # Append and save
        data.append(new_entry)
        with open('export.json', 'w') as f:
            json.dump(data, f, indent=4)

        return jsonify({"message": "Anime added successfully!"}), 201
    except Exception as e:
        print("Error in POST /api/anime:", e)  # Debugging log
        return jsonify({"error": str(e)}), 500

@app.route('/api/anime/update', methods=['PUT'])
@require_api_key
def update_anime():
    try:
        update_data = request.json
        print("Received data for PUT /api/anime/update:", update_data)  # Debugging log

        # Validate the incoming data
        if not update_data or 'id' not in update_data or 'episodes' not in update_data:
            return jsonify({"error": "Invalid data"}), 400

        anime_id = update_data['id']
        new_episodes = update_data['episodes']

        # Find the anime by ID
        anime = next((anime for anime in data if anime['id'] == anime_id), None)
        if not anime:
            return jsonify({"error": "Anime ID not found"}), 404

        # Process new episodes
        existing_episodes = anime.get('episodes', [])
        for new_episode in new_episodes:
            episode_number = new_episode.get('episodeNumber')
            if not episode_number:
                continue

            # Check if episode exists
            existing_episode = next(
                (ep for ep in existing_episodes if ep['episodeNumber'] == episode_number),
                None
            )

            if existing_episode:
                # Update existing episode
                for key, value in new_episode.items():
                    if value is not None:
                        existing_episode[key] = value
            else:
                # Add new episode
                existing_episodes.append(new_episode)

        # Update the anime's episodes
        anime['episodes'] = existing_episodes

        # Save the updated data to the JSON file
        with open('export.json', 'w') as f:
            json.dump(data, f, indent=4)

        return jsonify({"message": "Episodes updated successfully!"}), 200

    except Exception as e:
        print("Error in PUT /api/anime/update:", e)  # Debugging log
        return jsonify({"error": str(e)}), 500


# Handle preflight OPTIONS requests for CORS
@app.route('/api/<path:path>', methods=['OPTIONS'])
def handle_options(path):
    response = jsonify({"message": "Preflight handled"})
    response.headers.add('Access-Control-Allow-Origin', request.headers.get('Origin'))
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

@app.after_request
def after_request(response):
    origin = request.headers.get('Origin')
    if origin:
        response.headers.add('Access-Control-Allow-Origin', origin)
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    return response


if __name__ == '__main__':
    app.run(debug=True)
