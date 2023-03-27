from flask import Flask
from flask import request
import smtplib
from email.message import EmailMessage
import mysql.connector
import ssl
import random

app = Flask(__name__)

@app.route('/')
def displayWebPage():
    return "<h1>Welcome</h1>"

@app.route('/verifyEmail/', methods=['POST'])

def verifyEmail():
    if request.method == 'POST':
        hostEmail = "anprdetectionsystem@gmail.com"     #EMail sender details
        hostPass = "xbhbduydivmdohhy"
        reciever = request.json['email']       #Email recieved in request body

        msg = EmailMessage()    #Define Email object
        msg['Subject'] = "Your Verification Code from ANPR System"  #Email Subject
        msg['From'] = hostEmail     #Email sender
        msg['To'] = reciever        #Email reciever

        key = str(random.randint(111111,999999))     #Generate random 6 digit key

        #Simple HTML body of email
        msg.add_alternative(f"""\n\n      

        <div class="c-email">
            <div class="c-email__header">
            <h1 class="c-email__header__title">Your Verification Code</h1>
            </div>
            <div class="c-email__content">
            <p class="c-email__content__text text-title">
                Enter this verification code in field:
            </p>
            <div class="c-email__code">
                <span class="c-email__code__text">"""+key+"""</span>
            </div>
            <p class="c-email__content__text text-italic opacity-30 text-title mb-0">Return to the ANPR System and enter the code.</p>
            </div>
            <div class="c-email__footer"></div>
        </div>

        """, subtype="html")

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:  #Use gmail smtp servers
            smtp.login(hostEmail, hostPass)                                     #Try to login with sender details
            try:
                smtp.sendmail(hostEmail, reciever, msg.as_string())             #Try to send the mail to the reciever address
                return key                                                      #Return the key
            except:
                return None

@app.route('/returnEmails/', methods=['POST'])

def checkEmail():

    mydb = mysql.connector.connect(
    host="132.145.65.198",
    user="anprAdministrator",
    password="anpr!Admin2022",
    auth_plugin='mysql_native_password',
    database= "anprDATABASE"
    )

    mycursor = mydb.cursor()
    getAllUsers = "SELECT * FROM users"
    mycursor.execute(getAllUsers)

    ret = mycursor.fetchall()
    
    return ret

@app.route('/changePassword/', methods=['POST'])

def changePassword():
    mydb = mysql.connector.connect(
    host="132.145.65.198",                      #Connect as admin to database
    user="anprAdministrator",
    password="anpr!Admin2022",
    auth_plugin='mysql_native_password',
    database= "anprDATABASE"
    )
    
    email = request.json['email']                   #Get email from request body
    passwordToChange = request.json['password']     #Get new password from request body
    mycursor = mydb.cursor()

    updatePass = "ALTER USER '"+email+"'@'%' IDENTIFIED BY '"+passwordToChange+"';" #Build SQL query
    mycursor.execute(updatePass)        #Execute command
    mycursor.execute("FLUSH PRIVILEGES")    #Refresh privileges

if __name__ == "__main__":
    app.run(debug=True)

