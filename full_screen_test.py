from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

import requests
import time

# 밑으로 전송함.

url = 'http://127.0.0.1:8000/post'

# Builder.load_string('''
# <CameraClick>:
#     orientation: 'vertical'
    
#     # 박스 레이아웃이 있으면 하나하나씩 올릴수있네 ㅋㅋ
#     BoxLayout:
#         orientation: 'vertical'
#         Camera:
#             id: camera
#             resolution: (1280, 720)
#             allow_stretch: True
#             keep_ratio: True
#             play: False
#             canvas.before:
#                 PushMatrix
#                 Rotate:
#                     angle: -90
#                     origin: self.center
#             canvas.after:
#                 PopMatrix
#         Label:
#             id: camera_label
#             size_hint_y: None
#             height: dp(48)
#             canvas.before:
#                 PushMatrix
#                 Rotate:
#                     angle: -90
#                     origin: self.center
#             canvas.after:
#                 PopMatrix
#             canvas:
#                 Rectangle:
#                     texture: camera.texture
#                     size: self.size
#                     pos: self.pos
#         Button:
#             text: 'Capture'
#             size_hint_y: None
#             height: '48dp'
#             on_press: root.capture()
# ''')


Builder.load_string('''
<CameraClick>:
    orientation: 'vertical'
    BoxLayout:
        orientation: 'vertical'
        size_hint: (None, None)
        size: (Window.width, Window.height)

        Camera:
            id: camera
            resolution: (1280, 720)
            allow_stretch: True
            keep_ratio: True        
            play: False
            canvas.before:
                PushMatrix
                Rotate:
                    angle: -90
                    origin: self.center
            canvas.after:
                PopMatrix
        ToggleButton:
            text: 'Play'
            on_press: camera.play = not camera.play
            size_hint_y: None
            height: '48dp'
        Button:
            text: 'Capture'
            size_hint_y: None
            height: '48dp'
            on_press: root.capture()
''')



class CameraClick(BoxLayout):
    def capture(self):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        
        # req = UrlRequest(url, req_body={'image': camera.texture}, on_success=self.on_success, on_failure=self.on_failure)
        # 타임아웃 지정해놓음 -> 타임아웃하면 
        response = requests.post(url, 
                                json={
                                    'camera.texture': f'{camera.texture}',
                                    'camera.size': camera.size,
                                    'camera.colorfmt':camera.size
                                    }, 
                                )

        camera.export_to_png("IMG_{}.png".format(timestr))
        print("Captured")



    def on_success(self, req, result):
        '''
        Function to handle successful response from the server.
        '''
        print('Image sent successfully')
        
    def on_failure(self, req, result):
        '''
        Function to handle failed response from the server.
        '''
        print('Failed to send image')



class TestCamera(App):

    def build(self):

        # 이거 나중에 없애기 (휴대폰 용)

        
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
