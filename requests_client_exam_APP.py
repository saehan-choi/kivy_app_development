from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.uix.camera import Camera
from kivy.uix.image import Image

import requests

url = 'http://127.0.0.1:8000/post'

Builder.load_string('''
<CameraClick>:
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



class CameraClick(FloatLayout):
    def __init__(self, **kwargs):
        super(CameraClick, self).__init__(**kwargs)
        Clock.schedule_interval(self.update, 1.0 / 30.0)  # 30 fps

    def update(self, dt):
        texture = self.ids['camera'].texture

        response = requests.post(url,
                                json={
                                    'imageInfo': f'{texture}',
                                    },
                                timeout=1)
        if response.status_code == 200:
            print(response.text)
        else:
            print('breaked')

        self.ids['image'].texture = texture


class TestCamera(App):
    def build(self):
        return CameraClick()

TestCamera().run()
