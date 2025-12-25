# server.py
from flask import Flask, request, jsonify
from pipeline import run_pipeline
import os

app = Flask(__name__)

UPLOAD_DIR = "data/input"
OUTPUT_DIR = "data/output_user"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route('/process', methods=['POST'])
def process():
    # 1️⃣ Save uploaded song
    song_file = request.files.get('song')
    if not song_file:
        return jsonify({"error": "No song uploaded"}), 400
    song_path = os.path.join(UPLOAD_DIR, "user_song.wav")
    song_file.save(song_path)
    
    # 2️⃣ Save uploaded lyrics (optional)
    lyrics_file = request.files.get('lyrics')
    lyrics_path = None
    if lyrics_file:
        lyrics_path = os.path.join(UPLOAD_DIR, "user_lyrics.txt")
        lyrics_file.save(lyrics_path)

    # 3️⃣ Run the existing pipeline
    results = run_pipeline(song_path, lyrics_path, out_dir=OUTPUT_DIR)

    # 4️⃣ Return paths for frontend
    # We'll just return relative paths for JS to load
    return jsonify({
        "vocals": f"{OUTPUT_DIR}/stems/vocals.wav",
        "kick": f"{OUTPUT_DIR}/drums/kick.wav",
        "snare": f"{OUTPUT_DIR}/drums/snare.wav",
        "hihat": f"{OUTPUT_DIR}/drums/hihat.wav",
        "midi": f"{OUTPUT_DIR}/vocals.mid",
        "lyrics": f"{OUTPUT_DIR}/lyrics.json" if lyrics_path else None
    })

if __name__ == "__main__":
    app.run(debug=True)
