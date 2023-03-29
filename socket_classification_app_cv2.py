from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.camera import Camera
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.uix.button import Button
from kivy.clock import Clock

import socket
import numpy as np
import io

import cv2
# import cv2 -> cv2를 같이 넣어주면 전송속도 시간감소에 도움될듯


# IP, PORT = '27.112.246.62', 8000

IP, PORT = '27.112.246.62', 8000

# resolution: (640, 480) -> 디텍션 가능함.
# resolution: (320, 240) -> 디텍션 가능함.

# 1280x720
# 1920x1080
# -> 이부분은 테스트 아직 안해보았음

Builder.load_string('''
<classificationApp>:
    Camera:
        id: camera
        resolution: (640, 480)
        play: True
        opacity: 0
    Image:
        id: image
        allow_stretch: True
        keep_ratio: True
        # 투명도 조절
        opacity: 1
    Label:
        id: response_label
        size_hint: 0.5, 0.4
        valign: 'top'
        halign: 'left'
        text_size: self.width, None
        pos_hint: {'x': 0, 'y': 0}
        font_size: '10sp'

        # sizehint는 상대크기 size는 절대크기입니다. height도 절대크기이므로 사용하지 않는게 좋다.
        # size:w, h 입니다.
        # size: 300, 180
        # height: 120
        # valign은 수직정렬 halign은 수평정렬
        # kivy앱에서 상대적인 위치를 지정 x:0 y:0 은 왼쪽하단 x:1 y:1은 우측상단        
''')

# 왜 실시간으로 되다가 버튼한번누르면 (뚞뚞끊낌) 안되는거지?

class classificationApp(FloatLayout):
    def __init__(self, **kwargs):
        super(classificationApp, self).__init__(**kwargs)

        Clock.schedule_interval(self.update, 1.0 / 30.0)
        # 나중에 1.0/30.0으로 바꾸고 해상도도변경해야함.

        # 버튼 추가 size=(200, 150) 로 되어있는데, 지금 버튼 크기 width 더 늘려야해서 400, 150 으로 해볼것. height는 딱맞음.
        # 이거 흠... 길면 짤리는데 어케하지 .......!
        btn_capture = Button(text='Classficiation', size_hint=(None, None), size=(300, 150), pos_hint={'center_x': 0.5, 'y': 0})
        # 버튼도 나중에 이미지 넣기 가능 background_normal='path/to/your/image.png' 이런식으로!
        
        # 이거 size 조절해야함.......!  
        btn_capture.texture_size = btn_capture.size
        btn_capture.padding = [20, 20]

        btn_capture.bind(on_press=self.capture)
        self.add_widget(btn_capture)
        self.capture_timeout = 5

    def capture(self, instance):
        # 현재 화면에 보이는 프레임을 캡처하고 처리하는 함수 호출
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((IP, PORT))

        # 이것도 일단됨
        # self.sock.sendall(self.rotated_numpy.tobytes())
        self.sock.sendall(self.rotated_bytes)

        texts = self.sock.recv(1024).decode('utf-8')
        
        self.ids['response_label'].text = texts

        Clock.unschedule(self.update)
        # dt가 있는 이유는 schedule_once에서 dt인자를 받아야하기 때문입니다.
        Clock.schedule_once(lambda dt: Clock.schedule_interval(self.update, 1.0 / 30.0), self.capture_timeout)
        # Clock.schedule_once(self.clear_label_text, self.capture_timeout)

    def update(self, dt):
        texture = self.ids['camera'].texture

        # rotate를 위해 numpy로 변환 및 회전후 bytes로 변경
        self.rotated_numpy = self.bytes_to_numpy(texture)
        self.rotated_bytes = self.numpy_to_bytes(self.rotated_numpy)

        self.new_texture = Texture.create(size=(texture.size[1], texture.size[0]), colorfmt=texture.colorfmt)
        self.new_texture.blit_buffer(self.rotated_bytes, bufferfmt='ubyte', colorfmt=texture.colorfmt)

        # self.new_texture.flip_vertical() -> 이렇게 하면 상하반전입니다 ㅎㅎ
        # self.new_texture.flip_horizontal() -> 이렇게 하면 좌우반전

        self.ids['image'].texture = self.new_texture
        self.ids['response_label'].text = ''

    def img_to_bytes(self, array):
        bytes_array = bytearray(array)
        bytes = io.BytesIO(bytes_array)
        return bytes.getvalue()

    # for rotation
    def bytes_to_img(self, texture):
        pixels = np.frombuffer(texture.pixels, dtype=np.uint8)
        # print(pixels.shape)
        pixels = pixels.reshape(texture.size[1], texture.size[0], -1)
        # (480, 640)
        rotated_pixels = np.rot90(pixels)

        img = cv2.cvtColor(rotated_pixels, cv2.COLOR_RGBA2BGR)
        img = cv2.resize(img, (256,256))
        # print(img)

        # (640, 480)
        # 여기서 나중에 넘겨줄때 이미지 사이즈를 작게해서 넘겨주면 더 빠르게 수행가능합니다. 지금 서버코드에서 cv2 를 이용해 resize를 진행하는데
        # 이렇게 할 필요 없습니다!!!!!!

        # bytes만 반환
        return rotated_pixels


class TestCamera(App):
    def build(self):
        try:
            # permission을 해줘야하네 ㄷㄷ; 무조건 있어야합니다..!
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.CAMERA,
                Permission.INTERNET,
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.READ_EXTERNAL_STORAGE
            ])
            
        except:
            pass
            
                
        return classificationApp()

TestCamera().run()