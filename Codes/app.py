# app.py
from flask import Flask, render_template, jsonify
import subprocess
import threading

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/record', methods=['POST'])
def record_audio():
    subprocess.run(["python", "asr-1.py", "record", "myvoice.wav", "30"])
    return jsonify({"status": "recorded"})

# @app.route('/play', methods=['GET'])
# def play_audio():
#     subprocess.run(["python", "asr-1.py", "play", "myvoice.wav", "30"])
#     return jsonify({"status": "played"})

is_playing = False
playback_thread = None

def play_audio_background():
    global is_playing
    is_playing = True
    subprocess.run(["python", "asr-1.py", "play", "myvoice.wav", "30"])
    is_playing = False

@app.route('/play', methods=['GET'])
def play_audio():
    global is_playing, playback_thread
    if not is_playing:
        playback_thread = threading.Thread(target=play_audio_background)
        playback_thread.start()
        return jsonify({"status": "playing"})
    else:
        # Optional: handle stopping the playback if required
        return jsonify({"status": "already playing"})

@app.route('/transcribe', methods=['GET'])
def transcribe_audio():
    subprocess.run(["python", "asr-1.py", "transcribe", "myvoice.wav"])
    
    try:
        with open("myvoice_transcription.txt", "r", encoding='utf-8') as file:
            transcription = file.read()
        return jsonify({"transcription": transcription})
    except FileNotFoundError:
        return jsonify({"error": "Transcription file not found"}), 404

@app.route('/correct_text', methods=['GET'])
def correct_text():
    subprocess.run(["python", "corrected.py"])
    try:
        with open('../Data/myvoice_transcription_corrected.txt', 'r', encoding='utf-8') as file:
            corrected_text = file.read().strip()
        return jsonify({"corrected_text": corrected_text})
    except FileNotFoundError:
        return jsonify({"error": "Corrected text file not found"}), 404

# ... [rest of your Flask app] ...

if __name__ == "__main__":
    app.run(debug=True)
