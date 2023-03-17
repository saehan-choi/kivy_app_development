from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.floatlayout import FloatLayout

from kivy.core.window import Window
# from kivy.network.urlrequest import UrlRequest

import requests
import time

# 밑으로 전송함.
url = 'http://127.0.0.1:8000/post'

Builder.load_string('''
<CameraClick>:
    orientation: 'vertical'
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
    # ToggleButton:
    #     text: 'Play'
    #     on_press: camera.play = not camera.play
    #     size_hint_y: None
    #     height: '48dp'
    #     opacity: 0.5
    # Button:
    #     text: 'Capture'
    #     size_hint_y: None
    #     height: '48dp'
    #     on_press: root.capture()
    #     opacity: 0.5
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







        
        # img = texture_to_image(camera.texture)  -> 나중에 저 함수를 서버측에서 처리하도록 설정하기.
        # req = UrlRequest(url, req_body={'image': camera.texture}, on_success=self.on_success, on_failure=self.on_failure)

        # req = UrlRequest(url, req_body={'pixels': camera.texture.pixels,
        #                                 'size' : camera.texture.size,
        #                                 'mode' : camera.texture.colorfmt}, 
        # 나중에 이거 추가하고 테스트 해보기

        # requests에 타임아웃 지정해놓으면 그 시간대로 안들어오면 앱이 꺼집니다.
        # 또한, 서버를 열어놔야 post신호를 받을수있어서 앱이 안꺼집니다.. 이건 WIFI 연결되면 할것
        # response = requests.post(url, 
        #                         json={
        #                             'camera.texture': f'{camera.texture}',
        #                             'camera.size': camera.size,
        #                             'camera.colorfmt':camera.size
        #                             }, 
        #                         timeout=1)
