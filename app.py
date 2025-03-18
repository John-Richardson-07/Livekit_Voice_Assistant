from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route("/process_audio", methods=["POST"])
def process_audio():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file uploaded"}), 400

    audio_file = request.files["audio"]
    file_path = os.path.join("uploads", audio_file.filename)
    audio_file.save(file_path)

    # Forward the audio to LiveKit Agent
    # You need to integrate this with your LiveKit setup

    return jsonify({"message": "Audio received successfully"})

if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    app.run(debug=True, port=5000)
