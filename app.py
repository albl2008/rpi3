from PIL import Image
import os
import time
from flask import Flask, request
from threading import Lock
import random
import subprocess

app = Flask(__name__)
save_lock = Lock()  # Lock to prevent concurrent access to file-saving operations


def save_image(image_file, base_filename):
    with save_lock:
        # Save temporarily and reopen to verify/convert the image
        temp_filepath = os.path.join('images', 'temp_upload.png')
        image_file.save(temp_filepath)

        # Verify and re-save in a clean format
        final_filepath = os.path.join('images', base_filename)
        with Image.open(temp_filepath) as img:
            img = img.convert('RGB')  # Ensure compatibility
            img.save(final_filepath, 'PNG')

        os.remove(temp_filepath)  # Clean up temporary file
        return final_filepath


@app.route('/image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return 'No image part in the request', 400

    image_file = request.files['image']

    if image_file.filename == '':
        return 'No image file selected', 400

    # Save with standard filename and then with a unique timestamped filename
    filepath = save_image(image_file, 'image.png')
    timestamped_filepath = save_image(image_file, f'img_{int(time.time() * 1000)}.png')

    # Call display with the standard filepath
    try:
        subprocess.run(['python3', 'display.py', filepath], check=True)
    except subprocess.CalledProcessError as e:
        return f'Error displaying image: {e}', 500

    return 'Image saved and displayed successfully'


@app.route('/random', methods=['GET'])
def random_image():
    files = [filename for filename in os.listdir('images') if filename.endswith('.png') and filename not in ('weather.png', 'image.png')]

    if not files:
        return 'No images found in the folder', 404

    random_file = random.choice(files)
    filepath = os.path.join('images', random_file)

    try:
        subprocess.run(['python3', 'display.py', filepath], check=True)
    except subprocess.CalledProcessError as e:
        return f'Error displaying image: {e}', 500

    return 'Image displayed successfully', 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5005, debug=True)
