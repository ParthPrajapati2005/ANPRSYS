import requests

url = "https://email-verification-api.vercel.app/returnEmails"

req = requests.post(url)

out = req.json()

count = 0
while count != len(out):
    print(out[count][1])
    count = count + 1