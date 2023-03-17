

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
        # self.my_camera = KivyCamera(fps=5)
        self.my_camera = KivyCamera(fps=30)

        self.camera = BoxLayout(orientation='vertical', size_hint=(1, 0.9))
        self.camera.add_widget(self.my_camera)


        self.btn = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        btn1 = Button(text="original")
        self.btn.add_widget(btn1)
        btn2 = Button(text="detect")
        self.btn.add_widget(btn2)


        self.all_box = BoxLayout(orientation='vertical')
        self.all_box.add_widget(self.camera)
        self.all_box.add_widget(self.btn)

        # l = Label(text=cv2.__version__, font_size=150)
        # self.box.add_widget(l)
        return self.all_box

    def on_stop(self):
        # without this, app will not exit even if the window is closed
        # self.capture.release()
        pass

    def on_pause(self):
        return True


if __name__ == '__main__':
    CamApp().run()

