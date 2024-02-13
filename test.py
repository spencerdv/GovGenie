import requests

BASE = "http://127.0.0.1:8000/"

response = requests.put(BASE + "results/test", {"street": "348"})
print(response.json())