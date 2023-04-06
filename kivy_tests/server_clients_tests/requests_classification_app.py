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

import time

# 이건 나중에 server 할때 바꾸자
# url = "http://27.112.246.62:8000"

url = "https://192.168.7.102:8000"
# 나중에 이것만 바꾸면됨.
# 아 근데 이러면 외부로 포트를 안열어서 앱에서 안들어가짐


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
    Label:
        id: response_label
        size_hint: None, None
        size: 200, 60
        height: 60
        valign: 'bottom'
        halign: 'left'
        pos_hint: {'x': 0, 'y': 0}
        font_size: '20sp'
''')

        # id: response_label
        # # size_hint_y: None
        # text_size: 20, 20
        # height: 60
        # valign: 'bottom'
        # halign: 'left'
        # pos_hint: {'x': 0, 'y': 0}
        # font_size: '20sp'
        # -> 이건 중앙에 뜨게함. 흰색갈로

        
        # id: response_label
        # size_hint: None, None
        # size: 200, 60
        # valign: 'bottom'
        # halign: 'left'
        # pos_hint: {'x': 0, 'y': 0}
        # font_size: '20sp'
        
        

class classificationApp(FloatLayout):
    def __init__(self, **kwargs):
        super(classificationApp, self).__init__(**kwargs)
        self.aa = 0

        Clock.schedule_interval(self.update, 1.0 / 5.0)
        # 나중에 1.0/30.0으로 바꾸고 해상도도변경해야함.

        # 버튼 추가
        btn_capture = Button(text='Classficiation', size_hint=(None, None), size=(150, 100), pos_hint={'center_x': 0.5, 'y': 0})
        btn_capture.texture_size = btn_capture.size
        btn_capture.padding = [20, 20]

        btn_capture.bind(on_press=self.capture)
        self.add_widget(btn_capture)

        self.capture_timeout = 5

    def capture(self, instance):
        # 현재 화면에 보이는 프레임을 캡처하고 처리하는 함수 호출

        response = requests.post(url,
                                files={
                                        'camera.pixels': self.new_texture.pixels
                                        },
                                data = {
                                        'camera.size': str(self.new_texture.size),
                                        'camera.colorfmt': self.new_texture.colorfmt
                                        },
                                timeout=10)
        response_str = str(response.content.decode())

        
        self.aa+=1
        response_str = f'kakaka_{self.aa}'

        self.ids['response_label'].text = response_str

        # 이미지값 들어와야 하는경우 수정.
        # self.ids['image'].texture = self.new_texture

        Clock.unschedule(self.update)
        # dt가 있는 이유는 schedule_once에서 dt인자를 받아야하기 때문입니다.
        Clock.schedule_once(lambda dt: Clock.schedule_interval(self.update, 1.0 / 5.0), self.capture_timeout)
        Clock.schedule_once(self.clear_label_text, self.capture_timeout)


    def update(self, dt):
        texture = self.ids['camera'].texture

        # rotate를 위해 numpy로 변환 및 회전후 bytes로 변경
        rotated_numpy = self.bytes_to_numpy(texture)
        rotated_bytes = self.numpy_to_bytes(rotated_numpy)
        
        self.new_texture = Texture.create(size=(texture.size[1], texture.size[0]), colorfmt=texture.colorfmt)
        self.new_texture.blit_buffer(rotated_bytes, bufferfmt='ubyte', colorfmt=texture.colorfmt)

        self.ids['image'].texture = self.new_texture
        self.ids['response_label'].text = ''
        
    def numpy_to_bytes(self, array):
        bytes_array = bytearray(array)
        bytes = io.BytesIO(bytes_array)

        return bytes.getvalue()

    # for rotation
    def bytes_to_numpy(self, texture):
        pixels = np.frombuffer(texture.pixels, dtype=np.uint8)
        # print(pixels.shape)
        pixels = pixels.reshape(texture.size[1], texture.size[0], -1)
        # (480, 640)
        rotated_pixels = np.rot90(pixels)
        # (640, 480)

        # bytes만 반환
        return rotated_pixels

    def clear_label_text(self, dt):
        self.ids['response_label'].text = ''

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

