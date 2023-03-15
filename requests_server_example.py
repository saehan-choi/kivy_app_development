from flask import Flask, request, jsonify

import numpy as np
import cv2

app = Flask(__name__)


@app.route('/post', methods=['POST'])
def post():
    # data = request.get_data()
    # print(data)
    
    
    if 'camera.pixels' in request.files:
        file = request.files['camera.pixels']
        byte_data = file.read()  # 바이트 데이터를 읽어옵니다.

        return byte_data
    
    else:
        return 'No file found in request.', 400
    

    # return jsonify({'response': 'Hello, {}!'.format(data)})

def texture_to_image(pixels, size, mode):
    # 서버에서쓰기; ㅋ
    # buf = texture.pixels
    # size = texture.size
    # mode = texture.colorfmt
    buf = np.frombuffer(buf, dtype=np.uint8)
    buf.shape = (size[1], size[0], len(mode))
    buf = cv2.cvtColor(buf, cv2.COLOR_RGB2BGR)
    cv2.imwrite('./imageFolder/kaka.jpg', buf)
    return buf

if __name__ == '__main__':
    app.run(port=8000)


