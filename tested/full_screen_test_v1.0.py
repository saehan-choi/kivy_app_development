# from kivy.app import App
# from kivy.lang import Builder
# from kivy.uix.boxlayout import BoxLayout
# from kivy.core.window import Window
# from kivy.clock import Clock
# from kivy.uix.image import Image
# import time

# Builder.load_string('''
# <CameraClick>:
#     orientation: 'vertical'
#     BoxLayout:
#         size_hint: 1, 1
#         padding: 0
#         Camera:
#             id: camera
#             # resolution: (1280, 720)
#             resolution: (1080, 1920)
#             allow_stretch: True
#             keep_ratio: True
#             play: False
#             angle: -90
#     BoxLayout:
#         orientation: 'horizontal'
#         size_hint: 1, None
#         height: '48dp'
#         ToggleButton:
#             text: 'Play'
#             on_press: camera.play = not camera.play
#             size_hint_x: None
#             width: '80dp'
#             opacity: 0.5
#         Button:
#             text: 'Capture'
#             size_hint_x: None
#             width: '80dp'
#             on_press: root.capture()
#             opacity: 0.5
# ''')

# class CameraClick(BoxLayout):
#     def __init__(self, **kwargs):
#         super(CameraClick, self).__init__(**kwargs)
#         Clock.schedule_interval(self.update, 1.0 / 30.0)  # 30 fps

#     def update(self, dt):
#         self.ids['image'].texture = self.ids['camera'].texture
        
#     def capture(self):
#         '''
#         Function to capture the images and give them the names
#         according to their captured time and date.
#         '''
#         camera = self.ids['camera']
#         timestr = time.strftime("%Y%m%d_%H%M%S")


#         camera.export_to_png("IMG_{}.png".format(timestr))
#         print("Captured")

# class TestCamera(App):
#     def build(self):
#         return CameraClick()

# TestCamera().run()



from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.image import Image
import time

Builder.load_string('''
<CameraClick>:
    orientation: 'vertical'
    BoxLayout:
        size_hint: 1, 1
        padding: 0
        Camera:
            id: camera
            # resolution: (1280, 720)
            resolution: (1080, 1920)
            allow_stretch: True
            keep_ratio: True
            play: False
            angle: -90
    Image:
        id: image
        allow_stretch: True
        keep_ratio: True
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

class CameraClick(BoxLayout):
    def __init__(self, **kwargs):
        super(CameraClick, self).__init__(**kwargs)
        self.image = self.ids['image']
        Clock.schedule_interval(self.update, 1.0 / 30.0)  # 30 fps

    def update(self, dt):
        self.image.texture = self.ids['camera'].texture
        
    def capture(self):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")

        camera.export_to_png("IMG_{}.png".format(timestr))
        print("Captured")

class TestCamera(App):
    def build(self):
        return CameraClick()

TestCamera().run()
