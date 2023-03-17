from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
# from kivy.network.urlrequest import UrlRequest

import requests
import time

# 밑으로 전송함.
url = 'http://127.0.0.1:8000/post'

Builder.load_string('''
<CameraClick>:
    orientation: 'vertical'
    BoxLayout:
        size_hint_y: 0.9
        orientation: 'vertical'
        canvas.before:
            PushMatrix
            Rotate:
                angle: -90
                origin: self.center
        canvas.after:
            PopMatrix
        Camera:
            id: camera
            resolution: (480, 720)
            allow_stretch: True
            keep_ratio: True        
            play: False
        Rectangle:
            id: camera_texture
            texture: camera.texture
            size: self.texture_size
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}


    ToggleButton:
        text: 'Play'
        on_press: camera.play = not camera.play
        size_hint_y: 0.1
        # height: '48dp'
    Button:
        text: 'Capture'
        size_hint_y: 0.1
        # height: '48dp'
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