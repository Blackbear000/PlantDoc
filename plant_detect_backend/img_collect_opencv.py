
import cv2
import time
import base64
import requests
import numpy as np
from io import BytesIO
from utils import compress_image_to_base64


def collect_img(shared_img_str, img_url, lantency=3):
    """
    lantency: the second used by sleep after each iteration
    """
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        image_array = np.array(frame)
        if not ret:
            continue

        compressed_img = compress_image_to_base64(image_array)
        shared_img_str.value = compressed_img.encode()

        try:
            requests.post(img_url, json={"img": compressed_img})
            
        except:
            continue
        cv2.waitKey(lantency*1000)  


