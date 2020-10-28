import requests

class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


response = requests.get("https://api.cesium.com/v1/assets", auth=BearerAuth('<ION_ACCESS_TOKEN>'))

print(response, response.text)