import requests

BASE = "http://127.0.0.1:5000/" # define the base url 

response = requests.delete(BASE + "video/2")
input()
response = requests.put(BASE + "video/2", {'name': 'Gustavo', 'views':10000, 'likes' : 10})
print(response.json())
input()
response = requests.get(BASE + "video/2")
print(response.json())