import requests

class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


response = requests.get("https://api.cesium.com/v1/assets", auth=BearerAuth('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI0Y2Y5Yjg4NC1hMzUyLTQxZjMtYjUwYS02NTMwOGVmNTEzM2MiLCJpZCI6MzY1ODEsImlhdCI6MTYwMzc2NTgyOX0.fuK3A1uXh9FNFBWZA2FYaKRJyXzMcfUiN4l6PiXEVp0'))

print(response, response.text)