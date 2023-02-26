import requests

BASE = "http://127.0.0.1:5000/"

response = requests.put(BASE + "signup/1",data = {"likes":1000})

print(response.json())