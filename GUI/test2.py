import requests
data = {"email":"johnboston@yopmail.com"}
x = requests.post("http://127.0.0.1:5000/clearDatabase",json=data)

parse = x.text

print(parse)
