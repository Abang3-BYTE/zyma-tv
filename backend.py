from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS 
import os

app = Flask(__name__)
CORS(app)  # This allow website to talk to backend for internet

UPLOAD_FOLDER = 'videos'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/')
def home():
    return "ZYMA TV backend is Live Go to index.html"


@app.route('/upload', methods=['POST'])
def upload():
    if 'video' not in request.files:
        return jsonify({"error": "No video file"}), 400
    file = request.files['video']
    if file.filename == '':
        return jsonify({"error": "No name"}), 400
    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)
    return jsonify({
        "Message": "Upload Success!",
        "Url": f"/videos/{file.filename}"
    })


@app.route('/videos')
def list_videos():
    files = os.listdir(UPLOAD_FOLDER)
    videos = [{"name": f, "url": f"/videos/{f}"}
              for f in files if f.endswith(('.mp4', '.mov', '.mkv'))]
    return jsonify(videos)


@app.route('/videos/<filename>')
def serve_video(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


if __name__ == '__main__':
    # host 0.0.0.0 make e work for internet
    app.run(host='0.0.0.0', port=5000, debug=True)