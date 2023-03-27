import requests

url = "http://127.0.0.1:5000/registerUser/"
body = {"email":"example@example23.com",
    "firstName":"Bob",
    "lastName":"Blacker",
    "phoneNumber":"07504567898",
    "password":"Anpr!2323"}

req = requests.post(url, json=body)

print(req.text)