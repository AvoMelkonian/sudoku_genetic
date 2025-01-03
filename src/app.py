from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/data')
def data():
    return jsonify({"message": "Hello from Flask API!"})

if __name__ == '__main__':
    app.run(debug=True)
