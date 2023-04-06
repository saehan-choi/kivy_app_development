from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
import requests
import time

url = 'http://127.0.0.1:8000/post'

Builder.load_string('''
<CameraClick>:
    FloatLayout:
        Camera:
            id: camera
            resolution: (1280, 720)
            allow_stretch: True
            keep_ratio: True
            pos: 0, 0
            # size: root.width, root.height        
            size: root.height, root.width
            play: False
            canvas.before:
                PushMatrix
                Rotate:
                    # angle: -90
                    angle: 0
                    origin: self.center
            canvas.after:
                PopMatrix
        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, None
            height: '48dp'
            ToggleButton:
                text: 'Play'
                on_press: camera.play = not camera.play
                size_hint_x: None
                width: '80dp'
                opacity: 0.5
            Button:
                text: 'Capture'
                size_hint_x: None
                width: '80dp'
                on_press: root.capture()
                opacity: 0.5
''')

class CameraClick(FloatLayout):
    def capture(self):
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")

        camera.export_to_png("IMG_{}.png".format(timestr))
        print("Captured")

    def on_success(self, req, result):
        print('Image sent successfully')
        
    def on_failure(self, req, result):
        print('Failed to send image')


class TestCamera(App):

    def build(self):
        try:
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.CAMERA,
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.READ_EXTERNAL_STORAGE
            ])
        except:
            pass

        return CameraClick()


if __name__ == '__main__':
    # Window.fullscreen = True
    TestCamera().run()
