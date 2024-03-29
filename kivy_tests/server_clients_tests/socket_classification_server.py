
import socket
import numpy as np
import cv2
import time

import torchvision.transforms as transforms
import torch

import torch.nn.functional as F

import timm

import threading


# bad reaction good reaction 넣어도 괜찮을듯 하네요


HOST = ''
PORT = 8000

resolution = (640, 480, 4)

# 나중에 cv2로 바꾸면 256*256*3 이렇게 변할수도 있겠군

# 전송하는데 0.02s
# 아, 근데 이미지 사이즈를 256,256으로 돌려도 문제없을텐데, timm이 어느 이미지사이즈에서 학습했는지 알아야한다.


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


    # img = np.rot90(img) -> 이건 나중에 앱에서 사용허가 후 진행
    # img = cv2.resize(img, (256, 256))

    cv2.imwrite('kaka.jpg', img)

    return img

def imagenet_classes_arr():
    with open('imagenet_classes.txt', 'r') as f:
        lines = f.readlines()

    class_names = []
    for line in lines:
        line = line.split(',')
        line = line[0].strip()  # 줄바꿈 문자 제거
        class_names.append(line)

    return class_names

def img_to_tensor(img):

    img = cv2.resize(img, (256,256))
    # h, w, c -> c, h, w 로 변경! imagenet에서 학습될 때 이런 색상으로 학습된다네용
    img = img.transpose(2, 0, 1)
    # ed1 = time.time()

    # cv2 to normalized tensor
    tensor_img = torch.from_numpy(img / 255.0).float()
    normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    normalized_img = normalize(tensor_img).unsqueeze(0)
    normalized_img = normalized_img.to(device)
    # ed2 = time.time()

    return normalized_img

def tensor_to_results(model, img, classes):
    # inference
    classification_results = ""
    model.eval()
    with torch.no_grad():
        results = model(img)
        max_values, max_indices = torch.topk(results, k=5, dim=1)
        softmax_results = F.softmax(max_values, dim=1)

        # max_indices -> tensor([[508, 878, 398, 810, 681]])
        for i in range(max_indices.shape[0]):
            for j in range(max_indices.shape[1]):
                prob = softmax_results[i][j]*100
                print(f"{j+1}. {classes[int(max_indices[i][j])]}: {prob:.1f}%")
                
                if i == max_indices.shape[0] - 1 and j == max_indices.shape[1] - 1:
                    classification_results += f"   {classes[int(max_indices[i][j])]}: {prob:.1f}%"
                else:
                    classification_results+=f"   {classes[int(max_indices[i][j])]}: {prob:.1f}%\n"


        # socket으로 전송하기 위해서는 bytes로 결과를 보내야하기 때문에 이렇게 전송
        serialized_results = classification_results.encode('utf-8')
        return serialized_results

def handle_client(client_socket):
    st = time.time()
    bytes = recvall(client_socket)
    img = bytes_to_image(bytes)
    tensor = img_to_tensor(img)
    results = tensor_to_results(model, tensor, classes)

    client_socket.sendall(results)

    ed = time.time()
    print(f'{ed-st}s passed')
    print('\n\n')

    client_socket.close()

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        while True:
            client_socket, addr = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            client_thread.start()
            # print(f"Connection from {addr} has been established.")

if __name__ == "__main__":
    classes = imagenet_classes_arr()
    device = torch.device("cuda:2")
    model = timm.create_model('efficientnet_b0', pretrained=True)
    model.to(device)

    start_server()

# 나중에 배치로 처리하고 일정시간이상 안들어오면 


# if __name__ == "__main__":
#     classes = imagenet_classes_arr()
#     device = torch.device("cuda:2")
#     model = timm.create_model('efficientnet_b0', pretrained=True)
#     model.to(device)
#     # 집 네트워크 200mb 환경에서 0.12s 나옵니다. 네트워크 더 좋은환경에서 더 빨리됨.
#     # 근데 회사 wifi 5g로 하면 0.2~0.3s 나옵니다.  일반wifi로 하면 0.5~0.6s 소요됩니다.
#     # 로컬로 보내면 0.02s 나옵니다..!
#     # 3g로 보내면 9s 나옴.
    
#     while True:

#         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
#             server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#             server_socket.bind((HOST, PORT))
#             server_socket.listen()
    
#             client_socket, addr = server_socket.accept()
#             st = time.time()
            
#             bytes = recvall(client_socket)
#             img = bytes_to_image(bytes)
#             tensor = img_to_tensor(img)
#             results = tensor_to_results(model, tensor, classes)
            
#             client_socket.sendall(results)

#             ed = time.time()
#             print(f'{ed-st}s passed')
            
#         client_socket.close()
#         server_socket.close()

