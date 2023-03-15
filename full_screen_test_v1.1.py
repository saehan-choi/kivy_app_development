from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.image import Image
import time

Builder.load_string('''
<CameraClick>:
    orientation: 'vertical'
    Image:
        id: image
        allow_stretch: True
        keep_ratio: True
        play: False

    BoxLayout:
        orientation: 'horizontal'
        size_hint: 1, None
        height: '48dp'
        ToggleButton:
            text: 'Play'
            on_press: root.toggle_play()
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

class CameraClick(BoxLayout):
    def __init__(self, **kwargs):
        super(CameraClick, self).__init__(**kwargs)
        self.image = self.ids['image']
        self.is_playing = False
        Clock.schedule_interval(self.update, 1.0 / 30.0)  # 30 fps

    def toggle_play(self):
        self.is_playing = not self.is_playing
        if self.is_playing:
            self.ids['image'].play = True
        else:
            self.ids['image'].play = False

    def update(self, dt):
        self.image.texture = self.ids['image'].texture

    def capture(self):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.ids['image']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png("IMG_{}.png".format(timestr))
        print("Captured")

class TestCamera(App):
    def build(self):
        return CameraClick()

TestCamera().run()
