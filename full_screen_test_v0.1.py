
# from kivy.app import App
# from kivy.lang import Builder
# from kivy.uix.boxlayout import BoxLayout
# from kivy.core.window import Window

# 이거 kivy 모듈 카메라가 개쓰레기라서 테스트할때 개오래걸렸네;

# import requests
# import time

# # 밑으로 전송함.

# url = 'http://127.0.0.1:8000/post'


# Builder.load_string('''
# <CameraClick>:
#     orientation: 'vertical'
#     BoxLayout:
#         orientation: 'vertical'

#         Camera:
#             id: camera
#             resolution: (1280, 720)
#             allow_stretch: True
#             keep_ratio: True        
#             play: False
#             size_hint_y: 0.8
#             canvas.before:
#                 PushMatrix
#                 # rotate 0도 했을떄도 그렇게되는지 보기
#                 Rotate:
#                     angle: -90
#                     origin: self.center
#             canvas.after:
#                 PopMatrix
#         ToggleButton:
#             text: 'Play'
#             on_press: camera.play = not camera.play
#             size_hint_y: 0.1
#             height: '48dp'
#         Button:
#             text: 'Capture'
#             size_hint_y: 0.1
#             height: '48dp'
#             on_press: root.capture()
# ''')



# class CameraClick(BoxLayout):
#     def capture(self):
#         '''
#         Function to capture the images and give them the names
#         according to their captured time and date.
#         '''
#         camera = self.ids['camera']
#         timestr = time.strftime("%Y%m%d_%H%M%S")
        
#         # req = UrlRequest(url, req_body={'image': camera.texture}, on_success=self.on_success, on_failure=self.on_failure)
#         # 타임아웃 지정해놓음 -> 타임아웃하면 
#         response = requests.post(url, 
#                                 json={
#                                     'camera.texture': f'{camera.texture}',
#                                     'camera.size': camera.size,
#                                     'camera.colorfmt':camera.size
#                                     }, 
#                                 )

#         camera.export_to_png("IMG_{}.png".format(timestr))
#         print("Captured")



#     def on_success(self, req, result):
#         '''
#         Function to handle successful response from the server.
#         '''
#         print('Image sent successfully')
        
#     def on_failure(self, req, result):
#         '''
#         Function to handle failed response from the server.
#         '''
#         print('Failed to send image')



# class TestCamera(App):

#     def build(self):

#         # 이거 나중에 없애기 (휴대폰 용)

        
#         try:
#             # permission을 해줘야하네 ㄷㄷ; 무조건 있어야합니다..!
#             from android.permissions import request_permissions, Permission
#             request_permissions([
#                 Permission.CAMERA,
#                 Permission.WRITE_EXTERNAL_STORAGE,
#                 Permission.READ_EXTERNAL_STORAGE
#             ])
#         except:
#             pass
        
#         # Window.size = (720, 1280)
        
#         return CameraClick()


# TestCamera().run()



import os

import cv2
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image


class KivyCamera(Image):
    def __init__(self, capture=None, fps=0, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        # self.capture = cv2.VideoCapture("/sdcard2/python-apk/2.mp4")
        # print "file path exist :" + str(os.path.exists("/sdcard2/python-apk/1.mkv"))
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update, 1.0 / fps)

    def update(self, dt):
        ret, frame = self.capture.read()
        # print str(os.listdir('/sdcard2/'))
        if ret:
            # convert it to texture
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.texture = image_texture


class CamApp(App):
    def build(self):
        self.my_camera = KivyCamera(fps=12)
        self.box = BoxLayout(orientation='vertical')
        btn1 = Button(text="Hello")
        self.box.add_widget(btn1)
        # l = Label(text=cv2.__version__, font_size=150)
        # self.box.add_widget(l)
        self.box.add_widget(self.my_camera)
        return self.box

    def on_stop(self):
        # without this, app will not exit even if the window is closed
        # self.capture.release()
        pass

    def on_pause(self):
        return True


if __name__ == '__main__':
    CamApp().run()
