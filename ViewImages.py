#!/home/jack/Desktop/YOUTUBE_video/flask_env/bin/python
from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

# Define the image directory
Image_Directory = "static/images/Current_Project/"

@app.route('/')
def show_images():
    image_list = os.listdir(Image_Directory)
    image_list = [filename for filename in image_list if filename.endswith(".jpg")]
    return render_template('image.html', image_list=image_list)

@app.route('/display_image/<filename>')
def display_image(filename):
    image_path = os.path.join(Image_Directory, filename)
    return send_from_directory(Image_Directory, filename)

if __name__ == '__main__':
    app.run(debug=True, port=5300)
