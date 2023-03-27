
import requests

url = "https://vehicle-api-parth13075.vercel.app/getMOTDetails"
body = {"registrationPlate":"GP56YPH"}

r = requests.post(url, json=body)

print(r.text)




#a = text.find("*")

#print(text[a:])


