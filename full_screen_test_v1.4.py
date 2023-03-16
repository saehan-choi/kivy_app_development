from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.uix.camera import Camera
from kivy.uix.image import Image
from kivy.graphics.texture import Texture

import requests

import numpy as np
import cv2

url = "http://27.112.246.62:8000"

# 이미지 화질을 줄여서 할수있다.
Builder.load_string('''
<CameraClick>:
    Camera:
        id: camera
        # resolution: (720, 480)
        resolution: (640, 480)
        play: True
        opacity: 0
    Image:
        id: image
        allow_stretch: True
        keep_ratio: True
        # 투명도 조절
        opacity: 1
''')


class CameraClick(FloatLayout):
    def __init__(self, **kwargs):
        super(CameraClick, self).__init__(**kwargs)
        Clock.schedule_interval(self.update, 1.0 / 30.0)  # 30 fps

    def update(self, dt):
        
        texture = self.ids['camera'].texture

        response = requests.post(url,
                                files={
                                        'camera.pixels': texture.pixels
                                        },
                                data = {
                                        'camera.size': str(texture.size),
                                        'camera.colorfmt': texture.colorfmt
                                        },
                                timeout=10)

        new_texture = Texture.create(size=(texture.size[1], texture.size[0]), colorfmt=texture.colorfmt)
        new_texture.blit_buffer(response.content, bufferfmt='ubyte', colorfmt=texture.colorfmt)

        self.ids['image'].texture = new_texture





# def texture_to_image(pixels, size, mode):
#     # 최종적으로 opencv 말고 PIL 사용도 검토할것, byte전환속도가 5배빠름..ㄷ;
#     buf = np.frombuffer(pixels, dtype=np.uint8)
#     buf.shape = (size[1], size[0], len(mode))
#     img = cv2.cvtColor(buf, cv2.COLOR_RGB2BGR)
#     img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)

#     # here is detection code.
#     detection_code(img)

# def detection_code(img):
#     # yolo algorithm
#     return None

class TestCamera(App):
    def build(self):
        return CameraClick()

TestCamera().run()


