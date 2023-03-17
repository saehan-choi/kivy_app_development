from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.uix.camera import Camera
from kivy.uix.image import Image

import requests

url = 'http://127.0.0.1:8000/post'

# 이미지 화질을 줄여서 할수있다.

Builder.load_string('''
<CameraClick>:
    Camera:
        id: camera
        resolution: (720, 480)
        play: True
        opacity: 0
    Image:
        id: image
        allow_stretch: True
        keep_ratio: True
        # 투명도 조절
        opacity: 1

        # ToggleButton:
        #     # id: 
        #     text:'detection'
        #     on_press: texture
        #     size_hint_x: None
        #     width: '80dp'
        #     opacity: 0.5
''')

class CameraClick(FloatLayout):
    def __init__(self, **kwargs):
        super(CameraClick, self).__init__(**kwargs)
        Clock.schedule_interval(self.update, 1.0 / 30.0)  # 30 fps

    # 여기서 update가 detection 클릭하면, self.ids['camera'].texture 가져오게하고,
    # detection toggle시 response response값 가져오게하기

    def update(self, dt):
        texture = self.ids['camera'].texture

        response = requests.post(url,
                                files={
                                # 'camera.texture': b'texture.texture',
                                # 'camera.pixels': f'{texture.pixels}',
                                'camera.pixels': texture.pixels,
                                # 'camera.size': f'{texture.size}',
                                # 'camera.colorfmt': texture.colorfmt
                                    },
                                timeout=10)
        
        # response = requests.post(url,
        #                         json={
        #                         # 'camera.texture': b'texture.texture',
        #                         # 'camera.pixels': f'{texture.pixels}',
        #                         'camera.pixels': texture.pixels,
        #                         'camera.size': texture.size,
        #                         'camera.colorfmt': texture.colorfmt
        #                             },
        #                         timeout=1)
        
        if response.status_code == 200:
            print(f'success code:{response.text}')
        else:
            print(f'error code:{response.status_code}')
            print('')

        # 서버에서 전달받는 response로 작업을 진행!

        self.ids['image'].texture = response

def texture_to_image(texture):
    # 서버에서쓰기; ㅋ
    buf = texture.pixels
    size = texture.size
    mode = texture.colorfmt


class TestCamera(App):
    def build(self):
        return CameraClick()

TestCamera().run()


