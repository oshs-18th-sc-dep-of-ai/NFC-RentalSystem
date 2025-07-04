import requests

url = "http://127.0.0.1:5000/api/auth/login"
data = {
    "id": "2420913",
    "pw": "123456"
}

response = requests.post(url, json=data)
print(response.json())  