from flask import Flask
from flask import request
import requests
from bs4 import BeautifulSoup


app = Flask(__name__)

@app.route('/')
def displayWebPage():
    return "<h1>Welcome to the UK Vehicle API</h1>"

@app.route('/DVLA-API/', methods=['POST'])
def recieve():
    if request.method == 'POST':
        dvla_url = 'https://driver-vehicle-licensing.api.gov.uk/vehicle-enquiry/v1/vehicles'
        head = {'x-api-key':'U8eDaSElCE5V5doIvCQmP95TVOzNEXiM1pZ5jh47', 'Content-Type':'application/json'}
        regPlate = request.json['registrationPlate']
        body = {'registrationNumber': regPlate}
        x = requests.post(dvla_url, json = body, headers=head)

    return x.json()

@app.route('/depthCheckAPI/', methods=['POST'])  

def depthCheckAPI():
    if request.method=='POST':
        data = {}

        def extract(regPlate):
            base_url = "https://www.rapidcarcheck.co.uk/results/?RegPlate="
            url = base_url + regPlate
            r = requests.get(url)
            if r.status_code != 200:
                r.raise_for_status()
            return r.text

        def parse(html):
            soup = BeautifulSoup(html, 'html.parser')
            selectSoup1 = soup.select('div.wpb_wrapper p')
            selectSoup2 = soup.select('strong')

            headers = ["Registration Plate", "Make", "Model", "Colour", "Vehicle Type", "Body Type", "Fuel", 
                    "Engine Capacity", "Horsepower", "Top Speed", "0-60mph Time", "Average Yearly Mileage",
                    "Insurance Group", "V5C Issue Date", "Vehicle Age", "Year of Manufacture", "NA1", "NA2",
                    "Mileage", "Salvage History", "Exported Vehicle", "NA3", "MOT Due", "MOT Due in",
                    "Previous MOT Records", "Last Mileage Record", "TAX Due", "Tax Due in", "Carbon Emissions", 
                    "Average Tax Cost (12 Months)", "Average Tax Cost (6 Months)", "NA4", "Total Mileage Records",
                    "Estimated Current Mileage", "Average Yearly Mileage", "Estimated Current Mileage", 
                    "Urban Fuel Economy", "Extra-Urban Fuel Economy", "Combined Fuel Economy", "Cost per mile", 
                    "Cost per 100 miles", "Cost per 12000 miles"]

            for x in range(2,7):
                header = headers[x-2]
                key = (selectSoup2[x].text)
                data.update({header : key})
            
            for y in range(7,18):
                header = headers[y-2]
                key = (selectSoup2[y].text)
                data.update({header : key})
            
            for y in range(18,44):
                header = headers[y-2]
                key = (selectSoup2[y].text)
                data.update({header : key})
            
            return data
        regPlate = request.json['registrationPlate']
        extraction = extract(regPlate)
        result = parse(extraction)
    return result

@app.route('/getImages/', methods=['POST'])

def getImages():
    if request.method == 'POST':
        def extract(regPlate):
            base_url = "https://www.rapidcarcheck.co.uk/results/?RegPlate="
            url = base_url + regPlate
            r = requests.get(url)
            if r.status_code != 200:
                r.raise_for_status()
            return r.text

        def getCarImageURL(html):
            soup = BeautifulSoup(html, 'html.parser')
            refinedSoup = soup.select("img.image1")
            refinedSoup1 = soup.select("img.image2")
            carImageOutput = (refinedSoup[0])['src']
            logoImageOutput = (refinedSoup1[0])['src']

            URLS = {"carImageURL":carImageOutput, "logoImageURL":logoImageOutput}
            return URLS

        regPlate = request.json['registrationPlate']
        extraction = extract(regPlate)
        URLS = getCarImageURL(extraction)
        return URLS

@app.route('/getImages2/', methods=['POST'])

def getImages2():
    if request.method == 'POST':
        def extract(regPlate):
            base_url = "https://totalcarcheck.co.uk/FreeCheck?regno="
            url = base_url + regPlate
            r = requests.get(url)
            if r.status_code != 200:
                r.raise_for_status()
            return r.text

        def getCarImageURL(html):
            soup = BeautifulSoup(html, 'html.parser')
            refinedSoup = soup.select("img#vehicleImage")
            refinedSoup1 = soup.select("img#vehicleMakeImage")
            carImageOutput = (refinedSoup[0])['src']
            print(carImageOutput)
            logoImageOutput = "https://totalcarcheck.co.uk"+((refinedSoup1[0])['src'])
            print(logoImageOutput)

            URLS = {"carImageURL":carImageOutput, "logoImageURL":logoImageOutput}
            return URLS

        regPlate = request.json['registrationPlate']
        extraction = extract(regPlate)
        URLS = getCarImageURL(extraction)
        return URLS


@app.route('/getMileageHistory/', methods=['POST'])

def getMileageHistory():
    if request.method == 'POST':
        def extract(regPlate):
            base_url = "https://cardotcheck.co.uk/report/free/"
            url = base_url + regPlate
            r = requests.get(url)
            if r.status_code != 200:
                r.raise_for_status()
            return r.text

        regPlate = request.json['registrationPlate']
        html = extract(regPlate)

        mileageHistory = {}
        soup = BeautifulSoup(html,'html.parser')
        refinedSoup1 = soup.select('table.responsive-table td')
        check1 = False
        check2 = False
        for x in refinedSoup1:
            if x['data-title'] == "Date":
                date = x.text
                check1 = True
            
            if x['data-title'] == "Mileage recorded (MOT)":
                mileage = x.text
                check2 = True
        
            if check1 == True & check2 == True:
                mileageHistory.update({date:mileage})
                check1 = False
                check2 = False
        return mileageHistory

@app.route('/depthCheckAPI2/', methods=['POST'])

def depthCheckAPI2():
    if request.method == 'POST':
        data = {}

        def extract(regPlate):
            base_url = "https://totalcarcheck.co.uk/FreeCheck?regno="
            url = base_url + regPlate
            r = requests.get(url)
            if r.status_code != 200:
                r.raise_for_status()
            return r.text

        def parse(html):
            soup = BeautifulSoup(html, 'html.parser')
            selectSoup1 = soup.select('div.col-sm-5 table td span')

            headers = ["Registration Plate", "Exported", "motExpiry","motDaysLeft", "taxExpiry", "taxDaysLeft", "make", "model", 
                    "modelDetail","colour","vehicleType","bodyType", "fuelType", "engineCapacity", "euroStatus", "NA1",
                    "horsepower","vehicleAge", "registeredDate", "v5cRegistered", "registeredNear", "yearOfManufacture", "NA2", 
                    "insuranceGroup", "topSpeed", "0-60mph", "taxCost12Months", "taxCost6Months", "co2Emissions"]

            for a in range(0,29):
                header = headers[a]
                key = (selectSoup1[a].text)
                data.update({header : key})
                print(selectSoup1[a].text)
            
            for x in range(0,29):
                if selectSoup1[x] != "":
                    print(selectSoup1[x].text)
            
            return data
        regPlate = request.json['registrationPlate']
        extraction = extract(regPlate)
        result = parse(extraction)
    return result

@app.route('/getMOTDetails/', methods=['POST'])
def getMOT():
    if request.method == 'POST':
        regPlate = request.json['registrationPlate']
        base_url = "https://beta.check-mot.service.gov.uk/trade/vehicles/mot-tests?registration="+regPlate
        head = {'x-api-key':"WqHaXRA9s75QoGm3NFkoH2dzHNc5jTaf4IooEtcP",'Content-Type':"application/json"}
        x = requests.get(base_url, headers=head)
        parse = (x.json())[0]
        return parse
    return parse

if __name__ == "__main__":
    app.run(debug=True)
