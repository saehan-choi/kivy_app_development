from kivy.app import App
from kivy.clock import Clock
from kivy.uix.camera import Camera
from kivy.uix.floatlayout import FloatLayout

class CameraApp(App):
    def build(self):
        layout = FloatLayout()
        self.camera = Camera(resolution=(640, 480), play=True)
        layout.add_widget(self.camera)
        Clock.schedule_interval(self.update, 1.0 / 30.0)  # 30fps로 업데이트
        return layout

    def update(self, dt):
        # 캡처된 이미지를 화면에 업데이트
        self.camera.texture = self.camera.texture

if __name__ == '__main__':
    CameraApp().run()
