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
# resolution: (720, 480) -> 이렇게하면 나중에 size가 자동적으로 바뀔 수 있음
# resolution: (640, 480) -> 파일전송후 읽어들이는데에 시간이 오래걸림..! 더 좋게 못바꾸나.. 흠..
# resolution: (480, 320) -> 에러남

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
        # Clock.schedule_interval(self.update, 1.0 / 30.0)  # 30 fps
        # 지금 이것 때문에 느려진다!!!!!!!!!!!!!!!! 알아냈다!!!!!!!!!!
        # 적당량 조절하고 이걸 threading으로 변환하면 될 것 같다.
        # Clock.schedule_interval(self.update, 1.0 / 10.0)

        Clock.schedule_interval(self.update, 1.0 / 5.0)


    def update(self, dt):

        texture = self.ids['camera'].texture
        # shape 확인하고 해상도 낮춰서 해보기 !!
        response = requests.post(url,
                                files={
                                        'camera.pixels': texture.pixels
                                        },
                                data = {
                                        'camera.size': str(texture.size),
                                        'camera.colorfmt': texture.colorfmt
                                        },
                                timeout=10)

        # new_texture = Texture.create(size=(texture.size[1], texture.size[0]), colorfmt=texture.colorfmt)
        # new_texture.blit_buffer(response.content, bufferfmt='ubyte', colorfmt=texture.colorfmt)
        
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
                Permission.INTERNET,
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.READ_EXTERNAL_STORAGE
            ])
            
        except:
            pass
                
                
        return yoloDetection()

TestCamera().run()


