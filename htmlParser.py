import requests
from bs4 import BeautifulSoup

#base_url = "https://www.rapidcarcheck.co.uk/results/?RegPlate="
base_url = "https://cardotcheck.co.uk/report/free/"

data = {}


def extract():
    url = base_url + "WP62MVK"
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

    for x in range(2,5):
        #header = (((selectSoup1[x].text).split())[0])
        header = headers[x-2]######FIX#######################################
        key = (selectSoup2[x].text)
        data.update({header : key})
    
    for y in range(7,16):
        #header = (((selectSoup1[y].text).split())[0])
        header = headers[y-2]
        key = (selectSoup2[y].text)
        data.update({header : key})
    
    for y in range(18,44):
        #header = (((selectSoup1[y].text).split())[0])
        header = headers[y-2]
        key = (selectSoup2[y].text)
        data.update({header : key})
#part1 = extract()
#part2 = parse(part1)

#for x in data:
#    print("{:<30} {:<30}".format(x, data[x]))

def getCarImageURL(html):
    soup = BeautifulSoup(html, 'html.parser')
    refinedSoup = soup.select("img.image1")

    outputURL = (refinedSoup[0])['src']
    print(outputURL)

def getMileageHistory(html):
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
        
part3 = extract()
print(getMileageHistory(part3))
#part4 = getMileageHistory(part3)
#Create program which uploads the ROI image to database and sends a text file with all the vehicle details.
#OR crete an API which returs all the information.
