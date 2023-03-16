import cv2

img = cv2.imread('./img_to_byte_test.png')

bts = cv2.imencode('.png',img)
bts = bts.tostring()
print(bts)

import cv2

# 이미지 로드
image = cv2.imread('img_to_byte_test.png')

# 이미지를 바이트로 변환
retval, buffer = cv2.imencode('.jpg', image)
print(retval)
byte_image = buffer.tobytes()


# print(byte_image)