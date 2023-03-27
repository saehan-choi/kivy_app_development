from yolov5.models.experimental import attempt_load
from yolov5.utils.general import check_img_size, non_max_suppression, scale_boxes
from yolov5.utils.torch_utils import select_device

from flask import Flask, request, jsonify

import numpy as np
import cv2, time, torch

app = Flask(__name__)


@app.route('/', methods=['POST'])
def post():
    
    file = request.files['camera.pixels']
    byte_data = file.read()
    # 여기서 0.1s 소요됨.. 이걸 해결해야한다. -> 직접 byte파일을 보내고, 읽어올수있는 방법없는지 찾기
    
    img = bytes_to_img(byte_data)
    
    # classification으로 시작할때 어떤사이즈가 최적의 사이즈인지 알아내고, app에서 전송할때 그사이즈로 resize해서 전송할것.
    # 그래야 더 빨라짐.
    results = classification(img)
    
    return results

def bytes_to_img(byte_data):
    img = cv2.cvtColor(byte_data, cv2.COLOR_RGBA2BGR)
    return img


# def img_rotate(img):
#     img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
#     return img

def classification(img):
    
    resized_frame = cv2.resize(img)
    return None

if __name__ == '__main__':
    # Configuration
    app.run(host="0.0.0.0", port=8000)