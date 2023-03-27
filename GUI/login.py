from tkinter import*
import tkinter as tk
import customtkinter
import mysql.connector
import requests

class login(tk.Canvas):
    prevmast = ()
    emailToCheck = ""

    def __init__(self, master):
        tk.Canvas.__init__(self, master)
        self.prevmast = master
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        width = 1000
        height = 500
        x = (screenwidth/2)-(width/2)
        y = (screenheight/2)-(height/2)
        master.geometry('%dx%d+%d+%d' % (width, height, x, y))
        self.prevmast.title("ANPR - Automatic Number Plate Recognition System - Login") 


        self.screen = Canvas(self, highlightthickness=False, width=screenwidth, height=screenheight, bg="#141B2D")
        self.screen.pack()
        self.screen.delete("screen")
        self.screen.create_text(50,50,text="LOGIN", font=("Azonix", 40), fill="white", anchor="nw", tag="screen")
        self.screen.create_text(50,150, text="EMAIL : ", font=("Modern_Mono", 25), fill="white", anchor="nw", tag="screen")
        self.screen.create_text(50,210, text="PASSWORD : ", font=("Modern_Mono", 25), fill="white", anchor="nw", tag="screen")

        self.entryWorkspace = Frame(self.screen, width=550, height=150, bg="#141B2D")
        self.entryWorkspace.pack()
        self.screen.create_window(0,0,window=self.entryWorkspace)
        self.entryWorkspace.place(x=400, y=120)

        self.loginEmail = customtkinter.CTkEntry(self.entryWorkspace, width=550, height=50, border=0, bg_color="#141B2D", text_font=("Modern Sans", 20))
        self.loginEmail.pack()
        self.loginEmail.place(x=0, y=20)

        self.loginPassword = customtkinter.CTkEntry(self.entryWorkspace, width=550, height=50, border=0, bg_color="#141B2D", text_font=("Modern Sans", 20), show="*")
        self.loginPassword.pack()
        self.loginPassword.place(x=0, y=80)

        self.buttonWorkspace = Canvas(self.screen, width=1000, height=200,bg="#141B2D", highlightthickness=False)
        self.buttonWorkspace.pack()
        self.screen.create_window(0,0,window=self.buttonWorkspace)
        self.buttonWorkspace.place(x=0, y=250)

        submitButton = customtkinter.CTkButton(self.buttonWorkspace, width=200, height=60, text="Submit", text_font=("Modern_Mono", 25), bg_color="#141B2D", command=self.login)
        submitButton.pack()
        submitButton.place(x=100, y = 120)

        forgotButton = customtkinter.CTkButton(self.buttonWorkspace, width=500, height=60, text="Forgot Your Password?", text_font=("Modern_Mono", 25), bg_color="#141B2D", command=self.forgotPass)
        forgotButton.pack()
        forgotButton.place(x=450, y = 120)

    def login(self):
            self.buttonWorkspace.create_text(500,20, text="", font=("Modern Sans", 20), fill="red", tag="error")
            
            try:
                mydb = mysql.connector.connect(         #Try to connect to the databse with the details provided
                    host="132.145.65.198",
                    user=self.loginEmail.get(),
                    password=self.loginPassword.get(),
                    auth_plugin='mysql_native_password',
                    database= "anprDATABASE"
                    )
                
                mycursor = mydb.cursor()                #DB Object
                mycursor.execute("SHOW TABLES;")        #Execute SHOW Tables command
                table = (mycursor.fetchone()[0]).decode("utf-8")  #Convert bytearray object to string
                
                detectionPos = table.find("_")                          #The detection_id is the first number before the first _
                data = {'email':(self.loginEmail.get())}
                req = requests.post("https://register-api.vercel.app/getUserDetails", json=data)
                details = req.json()

                self.prevmast.detection_id = str(table[0:detectionPos])
                self.prevmast.detectionUser = self.loginEmail.get()             #Store in global variables which can be accessed from any page
                self.prevmast.detectionPassword = self.loginPassword.get()
                self.prevmast.userFirstName = details[2]
                self.prevmast.userLastName = details[3]
                self.prevmast.userPhoneNumber = details[4]
                self.buttonWorkspace.delete("error")      #Delete any error messages
                self.prevmast.switchFrame("homePage")     #Open to Dashboard page
                
            except:
                self.buttonWorkspace.delete("error")    #Display error message if login unseccessful
                self.buttonWorkspace.create_text(500,50, text="Login Unsuccessful. Check your email and password.", font=("Modern Sans", 20), fill="red", tag="error")

    def forgotPass(self):                                       #If user has forgotten password
        for widgets in self.buttonWorkspace.winfo_children():
            widgets.destroy()
        for widgets1 in self.entryWorkspace.winfo_children():
            widgets1.destroy()

        self.forgotWorkspace = Canvas(self.screen, width=1000, height=350,bg="#141B2D", highlightthickness=False)
        self.forgotWorkspace.pack()                 #Create workspace
        self.forgotWorkspace.place(x=0, y=150)
        #If user verification complete and password meets requirements then alter user password in database using API
        def checkAndUpdateDatabase():
            self.forgotWorkspace.delete("error")
            check = False
            pass1 = self.newPassword.get()
            pass2 = self.reNewPassword.get()
            if pass1 != pass2:
                self.forgotWorkspace.create_text(500,25, text="Passwords must match!", font=("Modern Sans", 20), fill="red", tag="error")
                check = True
            if check == False:
                count = 0
                checker = 0
                check1 = False
                check2 = False
                check3 = False
                check4 = False
                check5 = False
                while count != len(pass1):
                    if ord(pass1[count]) in range(65, 91):
                        checker = checker + 1
                        check1 = True
                    if ord(pass1[count]) in range(97,123):
                        checker = checker + 1
                        check2 = True
                    if ord(pass1[count]) in range(48,58):
                        checker = checker + 1
                        check3 = True
                    if ord(pass1[count]) in range(33,44):
                        checker = checker + 1
                        check4 = True
                    if ord(pass1[count]) in range(63,65):
                        checker = checker + 1
                        check5 = True
                    count = count + 1
                if count >= 8:
                    if (check1 == True) and (check2 == True) and (check3 == True) and (check4 == True) and (check5 == True):
                        check = False
                else:
                    self.forgotWorkspace.create_text(500,25, text="Password must be 8 characters long and contain at least 1 Uppercase, 1 Lowercase\n character, and at least 1 special character from the following: ! # $ % & () * + @ ?", font=("Modern Sans",18), fill="red", tag="error")    
                    check = True
            if check == False:
                #Update database here
                url = "https://email-verification-api.vercel.app/changePassword"
                body = {"email":self.emailToCheck, "password":pass1}
                req = requests.post(url, json=body)

                self.forgotWorkspace.create_text(500,25, text="Passwords changed Successfully! You may now login.", font=("Modern Sans", 20), fill="green", tag="error")

                def proceedToLogin():
                    self.prevmast.switchFrame("loginPage")

                loginButton = customtkinter.CTkButton(self.forgotWorkspace, width=150, height=80, text="Login", text_font=("Modern_Mono", 25), bg_color="#141B2D", command=proceedToLogin)
                loginButton.pack()
                loginButton.place(x=600, y=250)
        #Display screen with entry boxes to change password
        def resetPassword():
            self.forgotWorkspace.delete("code")
            self.forgotWorkspace.create_text(50,120, text="PASSWORD : ", font=("Modern_Mono", 25), fill="white", anchor="nw", tag="screen")
            self.forgotWorkspace.create_text(50,180, text="RE-ENTER PASSWORD : ", font=("Modern_Mono", 25), fill="white", anchor="nw", tag="screen")

            self.newPassword = customtkinter.CTkEntry(self.forgotWorkspace, width=400, height=50, border=0, bg_color="#141B2D", text_font=("Modern Sans", 20), show="*")
            self.newPassword.pack()
            self.newPassword.place(x=500, y=105)

            self.reNewPassword = customtkinter.CTkEntry(self.forgotWorkspace, width=400, height=50, border=0, bg_color="#141B2D", text_font=("Modern Sans", 20), show="*")
            self.reNewPassword.pack()
            self.reNewPassword.place(x=500, y=175)

            passButton = customtkinter.CTkButton(self.forgotWorkspace, width=150, height=80, text="Submit", text_font=("Modern_Mono", 25), bg_color="#141B2D", command=checkAndUpdateDatabase)
            passButton.pack()
            passButton.place(x=420, y = 250) 
        #Verify user email again as before using API
        def emailVerification():

            url = "https://email-verification-api.vercel.app/verifyEmail/"
            body = {"email":self.emailToCheck}
            req = requests.post(url, json=body)
            keyToCheck = req.text

            def checkCode():
                self.forgotWorkspace.delete("error")
                entry = codeEntry.get()
                if str(entry) == str(keyToCheck):
                    for widgets in self.forgotWorkspace.winfo_children():
                        widgets.destroy()

                    self.forgotWorkspace.create_text(500,30, text="Verification Success! Please choose your new password.", font=("Modern_Mono",20), fill="green", tag="error")
                    resetPassword()
                else:
                    self.forgotWorkspace.create_text(500,25, text="Verification was Unsuccessful. Try Again.", font=("Modern_Mono",20), fill="red", tag="error")


            self.forgotWorkspace.create_text(500,50, text="A verification code has been sent to the registered email. Please enter it below.", font=("Modern_Mono", 20), fill="green", tag="error")
            self.forgotWorkspace.create_text(150,200, text="Enter code: ", font=("Modern_Mono",25), fill="white", tag="code")
            codeEntry = customtkinter.CTkEntry(self.forgotWorkspace, width=400, height=50, border=0, bg_color="#141B2D", text_font=("Modern Sans", 20), show="*")
            codeEntry.pack()
            codeEntry.place(x=300, y=175)

            checkButton = customtkinter.CTkButton(self.forgotWorkspace, width=150, height=80, text="Submit", text_font=("Modern_Mono", 25), bg_color="#141B2D", command=checkCode)
            checkButton.pack()
            checkButton.place(x=750, y = 155)
        #Verify there is a user in the database with the given email
        def verifyEmail():
            self.forgotWorkspace.delete("msg")
            emailToCheck = str(forgotEmail.get())
            count = 0
            check = False
            #Check if email is valid and contains @
            while count != len(emailToCheck):
                if emailToCheck[count] == "@":
                    check == True
                count = count + 1

            if check == False:
                self.forgotWorkspace.create_text(500,100, text="The email you have entered is invalid. Please check again.", font=("Modern_Mono", 20), fill="red", tag="msg")

            getEmails = requests.post("https://email-verification-api.vercel.app/returnEmails") #returns all emails in databse
            allEmails = getEmails.json()

            found = False
            count = 0
            while count != len(allEmails):
                if emailToCheck == allEmails[count][1]:     #Check if email in database
                    found = True
                count = count + 1
            
            if found == False:
                self.forgotWorkspace.delete("msg")
                self.forgotWorkspace.create_text(500,100, text="There is no account in our database with the email you provided. Please register.", font=("Modern_Mono", 20), fill="red", tag="msg")

            if found == True:
                self.forgotWorkspace.delete("msg")
                self.forgotWorkspace.delete("error")

                for widgets in self.forgotWorkspace.winfo_children():
                    widgets.destroy()
                
                self.emailToCheck = emailToCheck
                emailVerification()
                    
        self.screen.delete("screen")
        self.screen.create_text(50,50,text="FORGOTTEN PASSWORD", font=("Azonix", 40), fill="white", anchor="nw", tag="screen")
        
        self.forgotWorkspace.create_text(500,50, text="Please enter your email below.", font=("Modern_Mono", 25), fill="white", tag="error")

        forgotEmail = customtkinter.CTkEntry(self.forgotWorkspace, width=550, height=50, border=0, bg_color="#141B2D", text_font=("Modern Sans", 20))
        forgotEmail.pack()
        forgotEmail.place(x=230, y=150)

        forgotButton = customtkinter.CTkButton(self.forgotWorkspace, width=200, height=60, text="Submit", text_font=("Modern_Mono", 25), bg_color="#141B2D", command=verifyEmail)
        forgotButton.pack()
        forgotButton.place(x=400, y = 250)

if __name__ == "__main__":
    app = login()
    app.mainloop()