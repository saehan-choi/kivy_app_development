import timm
import torch

import cv2
import torchvision.transforms as transforms
import torch.nn.functional as F

import time

with open('imagenet_classes.txt', 'r') as f:
    lines = f.readlines()

class_names = []
for line in lines:
    line = line.split(',')
    line = line[0].strip()  # 줄바꿈 문자 제거
    class_names.append(line)

# model create
model = timm.create_model('efficientnet_b0', pretrained=True)


for i in range(100):

    # image reading part
    img = cv2.imread('./dog.jpg')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (256,256))
    # h, w, c -> c, h, w 로 변경! imagenet에서 학습될 때 이런 색상으로 학습된다네용
    img = img.transpose(2,0,1)
    # ed1 = time.time()

    # cv2 to normalized tensor
    tensor_img = torch.from_numpy(img / 255.0).float()
    normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    normalized_img = normalize(tensor_img).unsqueeze(0)
    # ed2 = time.time()

    # inference
    model.eval()
    with torch.no_grad():
        results = model(normalized_img)
        # argmax_results = torch.argmax(results, dim=1)
        
        max_values, max_indices = torch.topk(results, k=5, dim=1)
        softmax_results = F.softmax(max_values, dim=1)
        
        print(softmax_results)
        # 한번더소프트맥스먹이기
        # max_indices -> tensor([[508, 878, 398, 810, 681]])
        for i in range(max_indices.shape[0]):
            for j in range(max_indices.shape[1]):
                prob = softmax_results[i][j]*100
                print(f"{j+1}. {class_names[int(max_indices[i][j])]}: {prob:.1f}%")
            
    print('\n\n\n')