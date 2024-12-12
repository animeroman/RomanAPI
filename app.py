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
    try:
        new_entry = request.json
        print("Received data:", new_entry)  # Debugging log

        if not new_entry or 'id' not in new_entry or 'animeEnglish' not in new_entry:
            return jsonify({"error": "Invalid data"}), 400  # Proper JSON response

        data.append(new_entry)

        with open('export.json', 'w') as f:
            json.dump(data, f, indent=4)

        return jsonify({"message": "Anime added successfully!"}), 201  # Proper JSON response
    except Exception as e:
        print("Error:", e)  # Debugging log
        return jsonify({"error": str(e)}), 500  # Proper JSON response


if __name__ == '__main__':
    app.run(debug=True)

## Command: curl -X POST http://127.0.0.1:5000/api/anime \ -H "Content-Type: application/json" \ -d '{"id": "12345", "animeEnglish": "Test Anime", "animeOriginal": "テストアニメ", "genres": ["Action", "Fantasy"]}'