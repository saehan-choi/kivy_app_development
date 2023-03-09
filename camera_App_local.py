from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
# from kivy.network.urlrequest import UrlRequest

import requests
import time

# 밑으로 전송함.

url = 'http://127.0.0.1:8000/post'

# window. 안먹히네 흠
# Window.maximize()


# 이거때문인가?
# allow_stretch: True
# keep_ratio: True       


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

# 이게 매번 빌드한번할때마다 새로 clean 해주고 해야하나봅니다.

# 그냥 opencv로 처리하는것을 저거로해놓자.!!!!!!!!!!!!!!!!!!!!!!!
# 해상도 늘리기..!
# 앱 꾸미기..!

# 나중에 필요한것들은 주석으로 달아놓았습니다.

# def texture_to_image(texture):
#     buf = texture.pixels
#     size = texture.size
#     mode = texture.colorfmt
#     buf = np.frombuffer(buf, dtype=np.uint8)
#     buf.shape = (size[1], size[0], len(mode))
#     buf = cv2.cvtColor(buf, cv2.COLOR_RGB2BGR)
#     return buf


class CameraClick(BoxLayout):
    def capture(self):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        
        # req = UrlRequest(url, req_body={'image': camera.texture}, on_success=self.on_success, on_failure=self.on_failure)
        # 타임아웃 지정해놓음
        response = requests.post(url, 
                                json={
                                    'camera.texture': f'{camera.texture}',
                                    'camera.size': camera.size,
                                    'camera.colorfmt':camera.size
                                    }, 
                                timeout=1)

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
