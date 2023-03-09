import requests
import json

url = 'http://127.0.0.1:8000/post'

response = requests.post(url, 
                         json={
                                'camera.texture': b'camera.texture',
                                'camera.size': (255,255),
                                'camera.colorfmt':'rgba'
                                }, 
                         timeout=1)

print(response.text)