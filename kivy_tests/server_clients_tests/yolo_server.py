from yolov5.models.experimental import attempt_load
from yolov5.utils.general import check_img_size, non_max_suppression, scale_boxes
from yolov5.utils.torch_utils import select_device

from flask import Flask, request, jsonify

import numpy as np
import cv2, time, torch

app = Flask(__name__)


@app.route('/', methods=['POST'])
def post():
    
    st = time.time()

    file = request.files['camera.pixels']
    byte_data = file.read()
    # 여기서 0.1s 소요됨.. 이걸 해결해야한다. -> 직접 byte파일을 보내고, 읽어올수있는 방법없는지 찾기

    # 문자열로 왔기때문에, eval을 씌어줌
    camera_size = eval(request.form.get('camera.size'))
    camera_colorfmt = request.form.get('camera.colorfmt')
    # 여기선 0.0002s 가량 소요

    result = img_processing(byte_data, camera_size, camera_colorfmt)
    ed = time.time()
    print(f'{ed-st}s passed')
    
    # print("processed")

    return result

def img_processing(byte_data, size, mode):
    img = bytes_to_img(byte_data, size, mode)
    
    img = yolo_detection(img, size)
    
    img = img_rotate(img)
    # here is detection code.
    # detection_code(img)
    byte_img = img_to_bytes(img)
    return byte_img

def bytes_to_img(byte_data, size, mode):
    buf = np.frombuffer(byte_data, dtype=np.uint8)
    # 이미지 rotate 안할때 사용할 것
    # buf.shape = (size[0], size[1], len(mode))
    buf.shape = (size[1], size[0], len(mode))

    img = cv2.cvtColor(buf, cv2.COLOR_RGBA2BGR)
    
    return img

def img_to_bytes(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
    byte_image = img.tobytes()

    return byte_image

def img_rotate(img):
    img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    return img

def yolo_detection(frame, size):

    # Calculate the new height while maintaining the aspect ratio
    height, width, _ = frame.shape
    new_height = int(height * (imgsz / width))
    
    # Make sure new_height is divisible by the stride
    new_height = new_height - (new_height % stride)

    # Resize the frame while maintaining the aspect ratio
    img = cv2.resize(frame, (imgsz, new_height))
    img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
    img = np.ascontiguousarray(img)
    img = torch.from_numpy(img).to(device)
    img = img.float()  # uint8 to fp16/32
    img /= 255.0  # 0 - 255 to 0.0 - 1.0

    if img.ndimension() == 3:
        img = img.unsqueeze(0)

    # Inference
    pred = model(img, augment=False)[0]

    # Apply NMS
    pred = non_max_suppression(pred, conf_thres, iou_thres, agnostic=True)
    detected_objects = []

    # Process detections
    for i, det in enumerate(pred):
        if len(det):
            # Rescale boxes from img_size to frame size
            det[:, :4] = scale_boxes(img.shape[2:], det[:, :4], frame.shape).round()
    
            # Draw bounding boxes and labels
            for *xyxy, conf, cls in reversed(det):
                label = f'{model.names[int(cls)]} {conf:.2f}'
                detected_objects.append(label)
                xyxy = [int(x) for x in xyxy]
                x1, y1, x2, y2 = xyxy
    
                # Get class color
                color = colors[int(cls)]
    
                # Draw bounding box
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
    
                # Draw label
                (text_width, text_height) = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)[0]
                cv2.rectangle(frame, (x1, y1 - text_height - 4), (x1 + text_width, y1), color, -1)
                cv2.putText(frame, label, (x1, y1 - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)

    # Display frame
    resized_frame = cv2.resize(frame, (size[0], size[1]))

    return resized_frame

if __name__ == '__main__':
    # Configuration
    weights = './yolov5/yolov5x.pt'  # 모델 가중치 파일 경로
    source = '0'  # 웹캠 인덱스 (0 또는 1)
    imgsz = 640  # 이미지 크기
    conf_thres = 0.5  # 신뢰도 임계값
    iou_thres = 0.45  # IoU 임계값
    device = select_device('')  # GPU 사용 설정

    # Load model
    model = attempt_load(weights, device=device)  # FP32 모델 불러오기
    stride = int(model.stride.max())  # 모델 스트라이드
    imgsz = check_img_size(imgsz, s=stride)  # 이미지 크기 확인
    num_classes = len(model.names)
    colors = [(np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255)) for _ in range(num_classes)]


    app.run(host="0.0.0.0", port=8000)


