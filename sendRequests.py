import requests
import json

#url = 'https://vehicle-api-parth13075.vercel.app/DVLA-API'
url = 'https://vehicle-api-parth13075.vercel.app/depthCheckAPI2'
body = {'registrationPlate':'VA64LNM'}

r = requests.post(url, json=body)

if r.status_code == 200:
    print("YESS")
    print(r.text)

else:
    print("NO")