from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# Load your JSON data
import json
with open('export.json', 'r') as f:
    data = json.load(f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/anime', methods=['GET'])
def get_anime():
    return jsonify(data)

@app.route('/api/anime', methods=['POST'])
def add_anime():
    new_entry = request.json
    
    # Validate fields (optional)
    if not new_entry or 'id' not in new_entry or 'animeEnglish' not in new_entry:
        return jsonify({"error": "Invalid data"}), 400

    data.append(new_entry)
    
    # Save the updated data to the JSON file
    with open('export.json', 'w') as f:
        json.dump(data, f, indent=4)
    
    return jsonify({"message": "Anime added successfully!"}), 201

if __name__ == '__main__':
    app.run(debug=True)
