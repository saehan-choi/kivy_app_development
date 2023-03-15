
import requests


response = requests.post(url,
                        files={
                                'camera.pixels': texture.pixels
                                },
                        timeout=10)
