from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.camera import Camera
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.clock import Clock

import requests

import numpy as np


import io

url = "http://27.112.246.62:8000"

# resolution: (640, 480) -> 디텍션 가능함.
# resolution=(320, 240) -> 디텍션 가능함.

Builder.load_string('''
<yoloDetection>:
    Camera:
        id: camera
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

class yoloDetection(FloatLayout):
    def __init__(self, **kwargs):
        super(yoloDetection, self).__init__(**kwargs)
        Clock.schedule_interval(self.update, 1.0 / 5.0)
        

    def update(self, dt):

        texture = self.ids['camera'].texture
        # !!!!!!일케하면 회전되어서 보여진다!!!!!!!
        
        pixels = np.frombuffer(texture.pixels, dtype=np.uint8)
        pixels = pixels.reshape(texture.size[1], texture.size[0], -1)
        rotated_pixels = np.rot90(pixels)
        rotated_bytes = bytearray(rotated_pixels)
        rotated_bytes = io.BytesIO(rotated_bytes)


        # 이건 rgb로 잡아서 bgr로 넘겨줄지 rgba 계속사용할지 고민
        new_texture = Texture.create(size=(texture.size[1], texture.size[0]), colorfmt=texture.colorfmt)
        new_texture.blit_buffer(rotated_bytes.getvalue(), bufferfmt='ubyte', colorfmt=texture.colorfmt)

        self.ids['image'].texture = new_texture

class TestCamera(App):
    def build(self):
        try:
            # permission을 해줘야하네 ㄷㄷ; 무조건 있어야합니다..!
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.CAMERA,
                Permission.INTERNET,
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.READ_EXTERNAL_STORAGE
            ])
            
        except:
            pass
                
                
        return yoloDetection()

TestCamera().run()


