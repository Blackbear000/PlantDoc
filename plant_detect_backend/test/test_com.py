import cv2
import os
import sys
import time
import logging
import numpy as np
from PIL import Image
import multiprocessing
from flask_cors import CORS
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify

img_url = "http://localhost:930/test/img"
vo_url = "http://localhost:930/test/vo"

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from utils import decompress_base64_to_image

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


def run_flask(shared_data):
    @app.route("/test/img", methods=["POST"])
    def get_img():
        logger.info("get img")
        img = request.json["img"]
        shared_data.value = img.encode()
        return {"status": "ok"}


    @app.route("/test/vo", methods=["POST"])
    def get_vo():
        logger.info("get vo")
        vo = request.json["vo"]
        logger.info(f"vo {vo}")
        return {"status": "ok"}
    
    app.run(host="0.0.0.0", port=930)


def check_img(shared_data):
    while True:
        if len(shared_data.value) > 0:
            img = shared_data.value.decode()
            img = decompress_base64_to_image(img)
            
            img = np.array(img)
            opencv_image = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            logger.info("frontend get image")
        
            cv2.imshow("Image", opencv_image)
            cv2.waitKey(200)
            



if __name__ == "__main__":
    img_str = multiprocessing.Array("c", 10*1024*1024, lock=False)
    app_process = multiprocessing.Process(target=run_flask, args=(img_str, ))
    check_img_process = multiprocessing.Process(target=check_img, args=(img_str, ))

    check_img_process.start()
    app_process.start()
    
    app_process.join()
    check_img_process.join()




