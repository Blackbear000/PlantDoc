from flask import Flask, render_template, request, send_file, jsonify
import os
from PIL import Image
from detection.yolov8_objectDetection import ObjectDetection
from ultralytics import YOLO

app = Flask(__name__)

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
    model = YOLO("detection/train13/weights/best.pt")
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

@app.route('/handle_direction', methods=['POST'])
def handle_direction():
    data = request.get_json()
    direction = data.get('direction')

    if direction == 0:
        result = "0"
    elif direction == 1:
        result = "Up"
    elif direction == 2:
        result = "Down"
    elif direction == 3:
        result = "Left"
    elif direction == 4:
        result = "Right"
    else:
        result = "Invalid direction"

    return jsonify({'result': result})


detect_results = []

@app.route('/detect', methods=['POST'])
def detect():

    position = "Some position"
    disease = "Some disease"

    # 将结果存储到 detect_results 中
    detect_results.append({"position": position, "disease": disease})

    # 返回最新的 detect 结果
    return jsonify({"position": position, "disease": disease})

if __name__ == '__main__':
    app.run(debug=False)
