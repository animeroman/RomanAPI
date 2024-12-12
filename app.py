from flask import Flask, jsonify, request

app = Flask(__name__)

# Load your JSON data
import json
with open('export.json', 'r') as f:
    data = json.load(f)

@app.route('/api/anime', methods=['GET'])
def get_anime():
    return jsonify(data)

@app.route('/api/anime', methods=['POST'])
def add_anime():
    new_entry = request.json  # Expecting JSON input
    data.append(new_entry)   # Add new entry to data
    
    # Save back to file
    with open('export.json', 'w') as f:
        json.dump(data, f, indent=4)
    
    return jsonify({"message": "Anime added successfully!"}), 201

if __name__ == '__main__':
    app.run(debug=True)
