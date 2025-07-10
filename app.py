from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import json

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
LIBRARY_FILE = 'library.json'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(LIBRARY_FILE):
    with open(LIBRARY_FILE, 'w') as f:
        json.dump([], f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        recognised_song = dummy_recognise_song(filepath)
        with open(LIBRARY_FILE, 'r') as f:
            library = json.load(f)
        library.append({'filename': file.filename, 'song': recognised_song})
        with open(LIBRARY_FILE, 'w') as f:
            json.dump(library, f, indent=2)
        return jsonify({'song': recognised_song})

def dummy_recognise_song(filepath):
    return "Dummy Song Title - Dummy Artist"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
