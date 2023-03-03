import requests

BASE = "http://127.0.0.1:5000/"

#response = requests.post(BASE + "video/1", {"likes": 10, "name": "Tim"})
#print(response.json())
response = requests.get(BASE + "video/6")
print(response.json())                                        