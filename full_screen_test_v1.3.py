from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.uix.camera import Camera
from kivy.uix.image import Image
from kivy.graphics.texture import Texture

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

    def update(self, dt):
        texture = self.ids['camera'].texture

        response = requests.post(url,
                                files={
                                        'camera.pixels': texture.pixels
                                        },
                                
                                timeout=10)

        new_texture = Texture.create(size=texture.size, colorfmt=texture.colorfmt)
        new_texture.blit_buffer(response.content, bufferfmt='ubyte', colorfmt=texture.colorfmt)

        # if response.status_code == 200:
        #     print(f'success code:{response.text}')
        # else:
        #     print(f'error code:{response.status_code}')
        #     print('')

        # 서버에서 전달받는 response로 작업을 진행!
        # self.ids['image'].texture = new_texture
        self.ids['image'].texture = texture

def texture_to_image(texture):
    # 서버에서쓰기; ㅋ
    buf = texture.pixels
    size = texture.size
    mode = texture.colorfmt


class TestCamera(App):
    def build(self):
        return CameraClick()

TestCamera().run()


