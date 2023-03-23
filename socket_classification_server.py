
import socket
import numpy as np
import cv2
import time
HOST = ''
PORT = 8000

resolution = (640, 480, 4)


# 전송하는데 0.02s ㅋㅋㅋㅋㅋㅋ
# 미쳤군.

def recvall(sock):
    
    BUFF_SIZE = 4096 # 4 KiB
    data = b''
    while True:
        part = sock.recv(BUFF_SIZE)
        data += part
        
        # len(part) < BUFF_SIZE 이건왜하는거지
        # len(data)==640*680*4:랑 같음
        if len(data)== resolution[0] * resolution[1] * resolution[2]:
            # either 0 or end of data
            break

    return data


def bytes_to_image(bytes):
    pixels = np.frombuffer(bytes, dtype=np.uint8)
    # print(pixels.shape)
    pixels = pixels.reshape(resolution[0], resolution[1], -1)
    
    img = cv2.cvtColor(pixels, cv2.COLOR_RGB2BGR)
    img = cv2.rotate(img, cv2.ROTATE_180)
    img = cv2.flip(img, 1)
    
    return img


while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # client_socket, addr = server_socket.accept();
        # 나중에 여기서부터
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        client_socket, addr = server_socket.accept()
        # 여기까지 뺼수있을듯 main.py init부분에 서버랑 연결하는거 추가하면.

        bytes = recvall(client_socket)
        
        img = bytes_to_image(bytes)
        
        
        cv2.imwrite('kaka.jpg', img)

        client_socket.close()
        server_socket.close()
