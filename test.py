from flask import Flask, render_template, request, send_file, jsonify
import os
from PIL import Image
from detection.yolov8_objectDetection import ObjectDetection
from ultralytics import YOLO
from plant_detect_backend.utils import decompress_base64_to_image
import multiprocessing
import cv2
from flask import Response
from flask_cors import CORS
import numpy as np
import logging
import sys
import requests
import base64
from io import BytesIO

img_url = "http://localhost:930/test/img"
vo_url = "http://localhost:930/test/vo"

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
fh = logging.FileHandler("test.log")
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)  # 把formater绑定到fh上
logger.addHandler(fh)

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
fh = logging.FileHandler("flask.log")
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)  # 把formater绑定到fh上
logger.addHandler(fh)
logger.warning("test")

shared_data = type('', (), {})()
shared_data.value = b""

def decompress_base64_to_image(base64_string):
    image_data = base64.b64decode(base64_string)
    image = Image.open(BytesIO(image_data))
    return image

def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()


def run_flask(shared_data):
    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/process', methods=['POST'])
    def process():
        if 'picture' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        picture = request.files['picture']
        if picture.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # Save the uploaded image to the project root directory
        picture_path = os.path.join(app.root_path, picture.filename)
        picture.save(picture_path)

        # Process the uploaded image using your ObjectDetection class
        # model = YOLO("detection/train13/weights/best.pt")
        model = YOLO("detection/train16/weights/best.pt")
        results = model(picture_path)
        for result in results:
            boxes = result.boxes
            name = result.names

            confidence_scores = boxes.conf.tolist()  # Convert to list
            class_names = [name[int(cls.item())] for cls in boxes.cls]  # Convert to list

        # Remove the temporary image file
        os.remove(picture_path)

        # Return the results
        return jsonify({'class_names': class_names, 'confidence_scores': confidence_scores}), 200


    detect_results = []

    @app.route('/test/vo', methods=['POST'])
    def detect():

        camera_stream_src = request.form['camera_stream_src']
        if not camera_stream_src:
            return jsonify({"error": "No camera stream source provided"}), 400
        
        picture_response = requests.get(camera_stream_src)
        if picture_response.status_code != 200:
            return jsonify({"error": "Failed to fetch image from URL"}), 500
        
        filename = 'camera_image.jpg'
        picture_path = os.path.join(app.root_path, filename)
        with open(picture_path, 'wb') as f:
            f.write(picture_response.content)

        # model = YOLO("detection/train13/weights/best.pt")
        model = YOLO("detection/train16/weights/best.pt")
        results = model(picture_path)

        class_names = []
        for result in results:
            boxes = result.boxes
            name = result.names

            confidence_scores = boxes.conf.tolist()  # Convert to list
            class_names = [name[int(cls.item())] for cls in boxes.cls]  # Convert to list

        if not class_names:
            return jsonify({"position": None, "disease": None})
        


        # Remove the temporary image file
        os.remove(picture_path)

        position = request.json["vo"]

        detect_results.append({"position": position, "disease": class_names})

        return jsonify({"position": position, "disease": class_names})
    
    @app.route("/test/img", methods=["GET", "POST"])
    def get_img():
        if request.method == "GET":
            img_data = shared_data.value.decode()
            if not img_data:
                return jsonify({"status": "error", "message": "No image data available"}), 404

            img = decompress_base64_to_image(img_data)
            img = np.array(img)
            opencv_image = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            pil_image = Image.fromarray(cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB))
            img_base64 = image_to_base64(pil_image)
            return jsonify({"status": "ok", "img": img_base64})

        elif request.method == "POST":
            logger.info("Updating shared data with new image")
            img = request.json.get("img")
            if img:
                shared_data.value = img.encode()
                return jsonify({"status": "ok"})
            else:
                return jsonify({"status": "error", "message": "No image data provided"}), 400

    
    app.run(host="0.0.0.0", port=930)
    
    
    



if __name__ == '__main__':
    img_str = multiprocessing.Array("c", 10*1024*1024, lock=False)
    app_process = multiprocessing.Process(target=run_flask, args=(img_str, ))
    # check_img_process = multiprocessing.Process(target=check_img, args=(img_str, ))

    # check_img_process.start()
    app_process.start()
    
    app_process.join()
    # check_img_process.join()
