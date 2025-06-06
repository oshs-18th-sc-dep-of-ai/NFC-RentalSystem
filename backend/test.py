import requests

url = "http://127.0.0.1:5000/login"
data = {"student_id": "2420913", "password": "123456"}

response = requests.post(url, json=data)

print("응답 상태 코드:", response.status_code)  # HTTP 상태 코드 확인
print("응답 내용:", response.text)  # 원본 응답 확인

try:
    print("JSON 응답:", response.json())  # JSON 변환 시도
except requests.exceptions.JSONDecodeError:
    print("서버 응답이 JSON 형식이 아닙니다!")
