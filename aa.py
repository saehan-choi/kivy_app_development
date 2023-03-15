from flask import Flask, request, jsonify

import numpy as np
import cv2

app = Flask(__name__)


@app.route('/post', methods=['POST'])
def post():
    data = request.get_data()

    print(data)

    # print(eval(data['camera.pixels']))
    
    # print('')
    # print('')
    # print(type(eval(data['camera.pixels'])))
    # print('')
    # print('')
    
    # print(data['camera.size'])
    # print(data['camera.colorfmt'])
    
    return data