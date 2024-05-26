from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
from model import model_trainer

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('output', exist_ok=True)
os.makedirs('images', exist_ok=True)


@app.route('/upload', methods=['POST'])
def upload():
    if 'video' not in request.files:
        return jsonify({'message': 'No video part in the request'}), 400

    file = request.files['video']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    try:
        file.save(os.path.join(UPLOAD_FOLDER,
                  'vehicle-counting.mp4'))
        model_trainer(file.filename)
        return jsonify({'message': 'File uploaded successfully'}), 200
    except Exception as e:
        return jsonify({'message': f'File upload failed: {str(e)}'}), 500


@app.route('/download', methods=['GET'])
def download():

    return 'Download'


@app.route('/image', methods=['GET'])
def image():
    image = os.path.join('images', 'annotated_frame.jpg')
    return send_file(image, mimetype='image/jpg')


if __name__ == '__main__':
    app.run(port=5000)
