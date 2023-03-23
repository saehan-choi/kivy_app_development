from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.camera import Camera
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.uix.button import Button

import requests

import numpy as np

import io

from kivy.clock import Clock

url = "http://27.112.246.62:8000"

# resolution: (640, 480) -> 디텍션 가능함.
# resolution: (320, 240) -> 디텍션 가능함.

Builder.load_string('''
<classificationApp>:
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

class classificationApp(FloatLayout):
    def __init__(self, **kwargs):
        super(classificationApp, self).__init__(**kwargs)
        Clock.schedule_interval(self.update, 1.0 / 5.0)

        # 버튼 추가
        btn_capture = Button(text='Capture', size_hint=(None, None), size=(150, 100), pos_hint={'center_x': 0.5, 'y': 0})
        btn_capture.texture_size = btn_capture.size
        btn_capture.padding = [20, 20]

        btn_capture.bind(on_press=self.capture)
        self.add_widget(btn_capture)

    def capture(self, instance):
        # 현재 화면에 보이는 프레임을 캡처하고 처리하는 함수 호출
        
        self.ids['image'].texture = self.new_texture

        Clock.unschedule(self.update)
        Clock.schedule_once(lambda dt: Clock.schedule_interval(self.update, 1.0 / 5.0), 5)

        # TODO: 캡처한 프레임을 처리하는 함수 호출

    def update(self, dt):
        texture = self.ids['camera'].texture

        # 나중에 이미지 사이즈 줄일때도 np저거 이용해서 줄이는게 낫겠다..! opencv 에러나니깐..!
        pixels = np.frombuffer(texture.pixels, dtype=np.uint8)
        pixels = pixels.reshape(texture.size[1], texture.size[0], -1)
        rotated_pixels = np.rot90(pixels)
        rotated_bytes = bytearray(rotated_pixels)
        rotated_bytes = io.BytesIO(rotated_bytes)

        new_texture = Texture.create(size=(texture.size[1], texture.size[0]), colorfmt=texture.colorfmt)
        new_texture.blit_buffer(rotated_bytes.getvalue(), bufferfmt='ubyte', colorfmt=texture.colorfmt)

        # 이거는 capture에서 사용하려고 선언함
        self.new_texture = new_texture
        self.ids['image'].texture = self.new_texture

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
                
                
        return classificationApp()

TestCamera().run()


