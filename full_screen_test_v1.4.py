from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.uix.camera import Camera
from kivy.uix.image import Image
from kivy.graphics.texture import Texture

import requests

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

class TestCamera(App):
    def build(self):
        try:
            # permission을 해줘야하네 ㄷㄷ; 무조건 있어야합니다..!
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.CAMERA,
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.READ_EXTERNAL_STORAGE
            ])
        except:
            pass
        
        return CameraClick()

TestCamera().run()


