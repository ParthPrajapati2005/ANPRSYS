from flask import Flask
from flask import request
import mysql.connector

app = Flask(__name__)

@app.route('/')
def displayWebPage():
    return "<h1>Welcome</h1>"

@app.route('/registerUser/', methods=['POST'])
def registerUser():
    mydb = mysql.connector.connect(         #Login into ANPR Database
    host="132.145.65.198",
    user="anprAdministrator",               #Login as anprAdmin
    password="anpr!Admin2022",
    auth_plugin='mysql_native_password',
    database= "anprDATABASE")                #Specify which database
    email = request.json['email']               #Get user email from response
    firstName = request.json["firstName"]       #Get user first name from response
    lastName = request.json["lastName"]         #Get user last name from response
    phoneNumber = request.json["phoneNumber"]   #Get user phone number from reponse
    password = request.json["password"]         #Get user password from resoponse
    mycursor = mydb.cursor()                    #Open Database
    check = False                               #Flag variable

    try:
        userCreation = "CREATE USER '"+email+"'@'%' IDENTIFIED WITH mysql_native_password BY '"+password+"';"       #Create USER account
        mycursor.execute(userCreation)                                                                              #Execute command
        check = True                                                                                                #Set flag variable to true
    except:
        return "An account with the same email already exists!"                                                     #If failed, it means it already exists!

    if check == True:   #If account was created successfully
            addToUserTable = "INSERT INTO users (user_email, user_firstName, user_lastName, user_phoneNumber) VALUES (%s, %s, %s, %s)"  #Add user table record
            userTableValues = (email, firstName,lastName, phoneNumber)
            mycursor.execute(addToUserTable,userTableValues)            #Execute command
            mydb.commit()                                               #Commit to Database
            getUserRow = "SELECT * FROM users"                          #Use detection_id PRIMARY key in user table as identfier for detection table
            mycursor.execute(getUserRow)
            rows = mycursor.fetchall()
            newDBName = str(rows[len(rows)-1][0]) + "_" + str(rows[len(rows)-1][2]) + "_" + str(rows[len(rows)-1][3]) + "_detections"   #Create detection table name 

            #Create detection table for user with all columns
            createDetectionTable = "CREATE TABLE "+newDBName+""" ( `detectionID` INT NOT NULL AUTO_INCREMENT ,  
                                                                    `registrationPlate` VARCHAR(50) NULL , 
                                                                    `dateOfDetection` VARCHAR(50) NULL , 
                                                                    `timeOfDetection` VARCHAR(50) NULL , 
                                                                    `vehicleMake` VARCHAR(50) NULL , 
                                                                    `vehicleModel` VARCHAR(100) NULL , 
                                                                    `vehicleColour` VARCHAR(50) NULL , 
                                                                    `vehicleFuelType` VARCHAR(50) NULL , 
                                                                    `vehicleType` VARCHAR(50) NULL , 
                                                                    `vehicleBodyType` VARCHAR(50) NULL , 
                                                                    `vehicleExported` VARCHAR(50) NULL , 
                                                                    `vehicleTopSpeed` VARCHAR(50) NULL , 
                                                                    `vehicle60Time` VARCHAR(50) NULL , 
                                                                    `vehicleEngineCapacity` VARCHAR(50) NULL , 
                                                                    `vehicleHorsepower` VARCHAR(50) NULL , 
                                                                    `vehicleEstimatedMileage` VARCHAR(50) NULL , 
                                                                    `vehicleInsuranceGroup` VARCHAR(50) NULL , 
                                                                    `vehicleAge` VARCHAR(50) NULL , 
                                                                    `vehicleYOM` VARCHAR(50) NULL , 
                                                                    `vehicleSalvage` VARCHAR(50) NULL , 
                                                                    `vehicleMOTDue` VARCHAR(50) NULL , 
                                                                    `vehicleTAXDue` VARCHAR(50) NULL , 
                                                                    `vehicleCarbonEmissions` VARCHAR(50) NULL , 
                                                                    `vehicleFuelEconomy` VARCHAR(50) NULL , 
                                                                    `vehicleTaxCost` VARCHAR(50) NULL , 
                                                                    PRIMARY KEY (`detectionID`))"""
            mycursor.execute(createDetectionTable)
            grantUserPermissions = "GRANT DROP, INSERT, UPDATE, DELETE, SELECT on "+newDBName+" TO '"+email+"'@'%';"    #Grant user limited permissions only for that table
            mycursor.execute(grantUserPermissions)  #execute
            
            return "Account created sucessfully! You can now login."  #Return success message

@app.route('/clearDatabase', methods=['POST'])
def clearDatabase():

    mydb = mysql.connector.connect(         #Login into ANPR Database
    host="132.145.65.198",
    user="anprAdministrator",               #Login as anprAdmin
    password="anpr!Admin2022",
    auth_plugin='mysql_native_password',
    database= "anprDATABASE")
    email = request.json['email']

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM users WHERE user_email = '"+email+"';")
    row = (mycursor.fetchone())
    tableName = str(row[0])+"_"+str(row[2])+"_"+str(row[3])+"_detections"
    mycursor.execute("TRUNCATE "+tableName+";")

    return ""

@app.route('/getUserDetails', methods=['POST'])
def getUserDetails():

    mydb = mysql.connector.connect(         #Login into ANPR Database
    host="132.145.65.198",
    user="anprAdministrator",               #Login as anprAdmin
    password="anpr!Admin2022",
    auth_plugin='mysql_native_password',
    database= "anprDATABASE")
    email = request.json['email']

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM users WHERE user_email = '"+email+"';")
    row = (mycursor.fetchone())

    return list(row)

if __name__ == "__main__":
    app.run(debug=True)