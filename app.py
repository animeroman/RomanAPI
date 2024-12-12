from flask import Flask, jsonify

app = Flask(__name__)

# Load your JSON data
import json
with open('export.json') as f:
    data = json.load(f)

@app.route('/api/anime', methods=['GET'])
def get_anime():
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
