# import cv2

# img = cv2.imread('./img_to_byte_test.png')

# bts = cv2.imencode('.png',img)
# bts = bts.tostring()
# print(bts)

# import cv2

# # 이미지 로드
# image = cv2.imread('img_to_byte_test.png')

# # 이미지를 바이트로 변환
# retval, buffer = cv2.imencode('.jpg', image)
# print(retval)
# byte_image = buffer.tobytes()


# # print(byte_image)


import numpy as np
import cv2

def img_processing(byte_data, size, mode):

    img = bytes_to_img(byte_data, size, mode)

    # img = img_rotate(img)
    # here is detection code.
    # detection_code(img)
    # here is byte transform code.

    byte_img = img_to_bytes(img)
    
    return byte_img


def bytes_to_img(byte_data, size, mode):
    buf = np.frombuffer(byte_data, dtype=np.uint8)
    buf.shape = (size[1], size[0], len(mode))
    img = cv2.cvtColor(buf, cv2.COLOR_RGB2BGR)
    return img

def img_to_bytes(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    retval, buffer = cv2.imencode('.jpg', img)
    byte_image = buffer.tobytes()
    return byte_image

def img_rotate(img):
    img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
