from flask import Flask, request, jsonify

import numpy as np
import cv2

app = Flask(__name__)


@app.route('/post', methods=['POST'])
def post():
    # data = request.get_data()
    # print(data)
    # 이제 여기서 반대로 나와지는거는 opencv 에서 고치자 제발.............;;
    file = request.files['camera.pixels']
    byte_data = file.read()

    # 문자열로 왔기때문에, eval을 씌어줌
    camera_size = eval(request.form.get('camera.size'))
    camera_colorfmt = request.form.get('camera.colorfmt')
    
    # print(camera_colorfmt)
    texture_to_image(byte_data, camera_size, camera_colorfmt)

    return byte_data
 

    # return jsonify({'response': 'Hello, {}!'.format(data)})

def texture_to_image(pixels, size, mode):

    buf = np.frombuffer(pixels, dtype=np.uint8)
    buf.shape = (size[1], size[0], len(mode))
    buf = cv2.cvtColor(buf, cv2.COLOR_RGB2BGR)
    cv2.imwrite('./imageFolder/kaka.jpg', buf)
    
    

    return buf

if __name__ == '__main__':
    app.run(port=8000)


