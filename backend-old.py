from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Data storage (simple)
live_data = {"title": "Morning Show from Abuja", "streamUrl": "https://www.youtube.com/embed/jfKfPfyJRdk?autoplay=1&mute=1"}
programs = [
    {"time": "08:00 AM", "title": "Morning Show", "status": "live"},
    {"time": "10:00 AM", "title": "News at 10", "status": "scheduled"}
]
chat_messages = [{"user": "Admin", "text": "Welcome to ZYMA TV LIVE!"}]
ADMIN_PASSWORD = "12345678"


@app.route('/api/live')
def get_live(): return jsonify(live_data)


@app.route('/api/programs')
def get_programs(): return jsonify(programs)


@app.route('/api/chat')
def get_chat(): return jsonify(chat_messages)


@app.route('/api/chat', methods=['POST'])
def post_chat():
    data = request.json
    chat_messages.append({"user": data.get('user','Viewer'), "text": data.get('text','')})
    if len(chat_messages) > 50: chat_messages.pop(0)
    return jsonify({"ok": True})


@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    if request.json.get('password') == ADMIN_PASSWORD:
        return jsonify({"ok": True})
    return jsonify({"ok": False}), 401


@app.route('/api/admin/update_live', methods=['POST'])
def update_live():
    global live_data
    live_data = request.json
    return jsonify(live_data)


@app.route('/api/admin/add_program', methods=['POST'])
def add_program():
    programs.append(request.json)
    return jsonify(programs)


@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files: return jsonify({"error": "No file"}), 400
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return jsonify({"url": f"/uploads/{filename}", "filename": filename})


if __name__ == '__main__':
    app.run(port=5000, debug=True)