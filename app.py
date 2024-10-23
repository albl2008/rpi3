import os
import time
from flask import Flask, request
from PIL import Image
import subprocess

app = Flask(__name__)


@app.route('/last', methods=['GET'])
def last():
    filepath = 'images/image.png'
    try:
        # Using subprocess to call the external Python script
        subprocess.run(['python3', 'display.py', filepath], check=True)
    except subprocess.CalledProcessError as e:
        return f'Error displaying image: {e}', 500

    return 'Image saved and displayed successfully'


@app.route('/random', methods=['GET'])
def random():
    # here i want ot display a random image saved in the images/saved folder
    # get a list of all the files in the images/saved folder
    files = []
    for filename in os.listdir('images/saved'):
        if filename.endswith('.png'):
            files.append(filename)

    # get a random file from the list
    random_file = random.choice(files)
    filepath = 'images/saved/' + random_file
    try:
        # Using subprocess to call the external Python script
        subprocess.run(['python3', 'display.py', filepath], check=True)
    except subprocess.CalledProcessError as e:
        return f'Error displaying image: {e}', 500

    return 'Image saved and displayed successfully'



@app.route('/image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return 'No image part in the request', 400

    image_file = request.files['image']

    if image_file.filename == '':
        return 'No image file selected', 400

    # Save the uploaded image to a file
    filepath = 'images/image.png'
    image_file.save(filepath)

    randomNum = int(time.time() * 1000)
    randomFilePath = 'images/saved/' + str(randomNum) + '.png'
    image_file.save(randomFilePath)


    # Call the display.py script with the path to the uploaded image
    try:
        # Using subprocess to call the external Python script
        subprocess.run(['python3', 'display.py', filepath], check=True)
    except subprocess.CalledProcessError as e:
        return f'Error displaying image: {e}', 500

    return 'Image saved and displayed successfully'

@app.route('/weather', methods=['POST'])
def upload_weather():
    if 'image' not in request.files:
        return 'No image part in the request', 400

    image_file = request.files['image']

    if image_file.filename == '':
        return 'No image file selected', 400

    # Save the uploaded image to a file
    filepath = 'images/weather.png'
    image_file.save(filepath)

    # Call the display.py script with the path to the uploaded weather image
    try:
        subprocess.run(['python3', 'display.py', filepath], check=True)
    except subprocess.CalledProcessError as e:
        return f'Error displaying weather image: {e}', 500

    return 'Weather image saved and displayed successfully'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5005, debug=True)

