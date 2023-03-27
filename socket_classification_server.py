
import socket
import numpy as np
import cv2
import time

import torchvision.transforms as transforms
import torch

import torch.nn.functional as F

import timm

HOST = ''
PORT = 8000

resolution = (640, 480, 4)

# 전송하는데 0.02s ㅋㅋㅋㅋㅋㅋ
# 미쳤군.
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
                classification_results+=f"{classes[int(max_indices[i][j])]}: {prob:.1f}%\n"

            print('\n\n')

        # socket으로 전송하기 위해서는 bytes로 결과를 보내야하기 때문에 이렇게 전송
        serialized_results = classification_results.encode('utf-8')
        return serialized_results

if __name__ == "__main__":
    classes = imagenet_classes_arr()
    device = torch.device("cuda:2")
    model = timm.create_model('efficientnet_b0', pretrained=True)
    model.to(device)

    while True:

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((HOST, PORT))
            server_socket.listen()
            client_socket, addr = server_socket.accept()
            bytes = recvall(client_socket)
            img = bytes_to_image(bytes)
            tensor = img_to_tensor(img)
            results = tensor_to_results(model, tensor, classes)
            
            client_socket.sendall(results)

        client_socket.close()
        server_socket.close()

