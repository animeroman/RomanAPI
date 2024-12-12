from flask import Flask, jsonify, request, render_template
import os
import json

app = Flask(__name__)

# Set the path for the data file on the persistent volume
data_file_path = "/data/export.json"

# Ensure the file exists, and load data
if os.path.exists(data_file_path):
    with open(data_file_path, 'r') as f:
        data = json.load(f)
else:
    # If the file doesn't exist, create an empty JSON structure
    data = []
    with open(data_file_path, 'w') as f:
        json.dump(data, f, indent=4)

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
        print("Received data:", new_entry)  # Debugging log

        if not new_entry or 'id' not in new_entry or 'animeEnglish' not in new_entry:
            return jsonify({"error": "Invalid data"}), 400  # Proper JSON response

        data.append(new_entry)

        # Save the updated data to the JSON file
        with open(data_file_path, 'w') as f:
            json.dump(data, f, indent=4)

        return jsonify({"message": "Anime added successfully!"}), 201  # Proper JSON response
    except Exception as e:
        print("Error:", e)  # Debugging log
        return jsonify({"error": str(e)}), 500  # Proper JSON response


if __name__ == '__main__':
    app.run(debug=True)
