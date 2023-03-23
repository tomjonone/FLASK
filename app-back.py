#!/home/jack/Desktop/FLASK/flask_venv/bin/python
import subprocess
import logging
from flask import Flask, render_template, send_file, request, redirect, url_for, flash
from flask import jsonify, send_from_directory
import os
from logging.handlers import RotatingFileHandler
import datetime
from werkzeug.utils import secure_filename
import os
import pygame
import random
from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip

app = Flask(__name__)

@app.route('/')
def index():
    image_dir = 'static/images'
    image_files = [f for f in os.listdir(image_dir) if f.endswith('.jpg')]
    random_image_file = random.choice(image_files)
    return render_template('index.html', random_image_file=random_image_file)


app.secret_key = os.urandom(24)

app.config['UPLOAD_FOLDER'] = 'static/images/uploads'
app.config['RESULTS_FOLDER'] = 'static/videos/results'
app.config['THUMBNAILS_FOLDER'] = 'static/images/thumbnails'
#app.config['CHECKPOINT_PATH'] = '/home/jack/Desktop/FlaskApp/Wav2Lip/checkpoints/wav2lip_gan.pth'
#app.config['AUDIO_PATH'] = '/home/jack/Desktop/FlaskApp/Wav2Lip/content/sample_data/input_audio.wav'

# Set the maximum file size to 16MB
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Configure the logger
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
app.logger.addHandler(handler)

# Define route to display upload form
@app.route('/upload_file', methods=['POST', 'GET'])
def upload_file():
    if request.method == 'POST':
        # Check if file was uploaded
        if 'file' not in request.files:
            app.logger.error('No file was uploaded')
            flash('Error: No file was uploaded')
            return redirect(request.url)
        app.logger.error('request.files[\'file\']')
        file = request.files['file']

        # Check if file was selected
        if file.filename == '':
            app.logger.error('No file was selected')
            flash('Error: No file was selected')
            return redirect(request.url)

        # Define allowed file extensions
        ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

        # Define function to check file extension
        def allowed_file(filename):
            return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

        # Check if file is allowed
        if not allowed_file(file.filename):
            app.logger.error(f'File {file.filename} is not allowed')
            flash(f'Error: File {file.filename} is not allowed')
            return redirect(request.url)

        # Save the file
        try:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            app.logger.info(f'File {filename} saved')
        except Exception as e:
            app.logger.error(f'Error saving file: {e}')
            flash('Error: Unable to save file')
            return redirect(request.url)

        # Redirect to the result page
        return redirect(url_for('result', filename=filename))

    # Return the upload form for GET requests
    return render_template('upload_file.html')

@app.route('/result/<filename>')
def result(filename):
    return render_template('result.html', filename=filename)

@app.route('/get_gallery')
def get_gallery():
    image_dir = '/home/jack/Desktop/FLASK/static/images/uploads'
    image_names = os.listdir(image_dir)
    return render_template('get_gallery.html', image_names=image_names)

@app.route('/uploads/<filename>')
def send_image(filename):
    return send_from_directory('static/images/uploads', filename)

@app.route('/uploads/thumbnails/<filename>')
def send_image_thumb(filename):
    return send_from_directory('static/images/uploads/thumbnails', filename)
@app.route('/flask_info')
def flask_info():
    return render_template('flask_info.html')

if __name__ == '__main__':
    app.run(debug=True)


