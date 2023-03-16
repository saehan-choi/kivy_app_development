# print(type("(255,255)"))

# print(type(eval("(255,255)")))

import requests
import json

url = "http://27.112.246.62:8000"

data = {"a": 100, "b": 200}
headers = {"Content-Type": "application/json"}

response = requests.post(url, data=json.dumps(data), headers=headers)

print(response.status_code)
print(response.text)