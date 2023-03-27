from tkinter import*
import tkinter as tk
import customtkinter
import requests
import time

class register(tk.Canvas):
    prevmast = ()
    entryWorkspace = ()
    buttonWorkspace = ()
    error = ()

    firstName = ""
    lastName = ""
    email = ""
    phoneNumber = ""
    password = ""

    def __init__(self, master):
        tk.Canvas.__init__(self, master)
        self.prevmast = master
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        width = 1000
        height = 800
        x = (screenwidth/2)-(width/2)
        y = (screenheight/2)-(height/2)
        master.geometry('%dx%d+%d+%d' % (width, height, x, y))
        self.prevmast.title("ANPR - Automatic Number Plate Recognition System - Register") 

        screen = Canvas(self, highlightthickness=False, width=screenwidth, height=screenheight, bg="#141B2D")
        screen.pack()
        #Add text and placeholders
        screen.create_text(50,50,text="REGISTER", font=("Azonix", 40), fill="white", anchor="nw")
        screen.create_text(50,150, text="FIRST NAME : ", font=("Modern_Mono", 25), fill="white", anchor="nw")
        screen.create_text(50,210, text="LAST NAME : ", font=("Modern_Mono", 25), fill="white", anchor="nw")
        screen.create_text(50,270, text="EMAIL : ", font=("Modern_Mono", 25), fill="white", anchor="nw")
        screen.create_text(50,330, text="PHONE NUMBER : ", font=("Modern_Mono", 25), fill="white", anchor="nw")
        screen.create_text(50,390, text="PASSWORD : ", font=("Modern_Mono", 25), fill="white", anchor="nw")
        screen.create_text(50,450, text="RE-ENTER PASSWORD : ", font=("Modern_Mono", 25), fill="white", anchor="nw")

        self.entryWorkspace = Frame(screen, width=550, height=400, bg="#141B2D")
        self.entryWorkspace.pack()
        screen.create_window(0,0,window=self.entryWorkspace)
        self.entryWorkspace.place(x=400, y=120)
        
        firstName = customtkinter.CTkEntry(self.entryWorkspace, width=550, height=50, border=0, bg_color="#141B2D", text_font=("Modern Sans", 20))
        firstName.pack()
        firstName.place(x=0, y=20)

        lastName = customtkinter.CTkEntry(self.entryWorkspace, width=550, height=50, border=0, bg_color="#141B2D", text_font=("Modern Sans", 20))
        lastName.pack()
        lastName.place(x=0, y=80)
        
        email = customtkinter.CTkEntry(self.entryWorkspace, width=550, height=50, border=0, bg_color="#141B2D", text_font=("Modern Sans", 20))
        email.pack()
        email.place(x=0, y=140)

        phoneNumber = customtkinter.CTkEntry(self.entryWorkspace, width=550, height=50, border=0, bg_color="#141B2D", text_font=("Modern Sans", 20))
        phoneNumber.pack()
        phoneNumber.place(x=0, y=200)

        password = customtkinter.CTkEntry(self.entryWorkspace, width=550, height=50, border=0, bg_color="#141B2D", text_font=("Modern Sans", 20), show="*")
        password.pack()
        password.place(x=0, y=260)

        rePassword = customtkinter.CTkEntry(self.entryWorkspace, width=550, height=50, border=0, bg_color="#141B2D", text_font=("Modern Sans", 20), show="*")
        rePassword.pack()
        rePassword.place(x=0, y=320)

        self.buttonWorkspace = Canvas(screen, width=1000, height=200, bg="#141B2D", highlightthickness=False)
        self.buttonWorkspace.pack()
        screen.create_window(0,0,window=self.buttonWorkspace)
        self.buttonWorkspace.place(x=0, y=600)
        #If button clicked, call createReg function
        def go():
            self.buttonWorkspace.create_text(500,20, text="", font=("Modern Sans", 20), fill="red", tag="error")
            self.createReg(firstName.get(), lastName.get(), email.get(), phoneNumber.get(), password.get(), rePassword.get())

        submitButton = customtkinter.CTkButton(self.buttonWorkspace, width=200, height=100, text="Submit", text_font=("Modern_Mono", 25), bg_color="#141B2D", command=go)
        submitButton.pack()
        submitButton.place(x=400, y = 80)     

    def createReg(self, firstName, lastName, email, phoneNumber, password, rePassword):
        self.buttonWorkspace.delete("error")    #Delete any error messages onscreen 
        check = False   #Set flag to false

        #If any of the fields are empty, show error
        if firstName == "" or lastName == "" or email == "" or phoneNumber == "" or password == "" or rePassword == "":
            self.buttonWorkspace.create_text(500,20, text="All entries are mantatory!", font=("Modern Sans", 20), fill="red", tag="error")
            check = True
        #If the two passwords do not match, show error
        elif password != rePassword:
            self.buttonWorkspace.create_text(500,20, text="Passwords must match!", font=("Modern Sans", 20), fill="red", tag="error")
            check = True
        #If the phone number is not 10 digits long, show error
        elif len(phoneNumber) != 10:
            if (len(phoneNumber) != 11):
                self.buttonWorkspace.create_text(500,20, text="Phone Number is Invalid", font=("Modern Sans",20), fill="red", tag="error")
                check = True
        #If the phone number is not integer input, show error
        if check == False:
            count = 0
            while count != len(phoneNumber):
                if ord(phoneNumber[count]) not in range(48,58):
                    self.buttonWorkspace.create_text(500,20, text="Phone Number is Invalid", font=("Modern Sans",20), fill="red", tag="error")
                    check = True
                
                count = count + 1 
        #If email does not contail @
        if check == False:
            count = 0
            found = False
            while count != len(email):
                if email[count] == "@":
                    found = True
                count = count + 1

            if found == False:
                self.buttonWorkspace.create_text(500,20, text="Email must contain @ !", font=("Modern Sans",20), fill="red", tag="error")
                check = True
        #Check if password has 8 characters
        #Check if password has uppercase letter
        #Check if passowrd has lowercase letter
        #Check if password has special character
        if check == False:
            count = 0
            checker = 0
            check1 = False
            check2 = False
            check3 = False
            check4 = False
            check5 = False

            while count != len(password):
                if ord(password[count]) in range(65, 91):       #Using ASCII values to check
                    checker = checker + 1
                    check1 = True
                if ord(password[count]) in range(97,123):
                    checker = checker + 1
                    check2 = True
                if ord(password[count]) in range(48,58):
                    checker = checker + 1
                    check3 = True
                if ord(password[count]) in range(33,44):
                    checker = checker + 1
                    check4 = True
                if ord(password[count]) in range(63,65):
                    checker = checker + 1
                    check5 = True
                
                count = count + 1

            if count >= 8:  #If all checks passed, then flag is still false
                if (check1 == True) and (check2 == True) and (check3 == True) and (check4 == True) and (check5 == True):
                    check = False
            else:
                self.buttonWorkspace.create_text(500,25, text="Password must be 8 characters long and contain at least 1 Uppercase, 1 Lowercase\n character, and at least 1 special character from the following: ! # $ % & () * + @ ?", font=("Modern Sans",18), fill="red", tag="error")    
                check = True

        if check == False:              #If all checks passed, set variables to information provided
            self.firstName = firstName
            self.lastName = lastName
            self.email = email
            self.phoneNumber = phoneNumber
            self.password = password
            self.verifyEmail()              #Continue to email verification

    def verifyEmail(self):
        for widgets in self.buttonWorkspace.winfo_children():   #Destroy buttons on previous page
            widgets.destroy()
        
        url = "https://email-verification-api.vercel.app/verifyEmail/"  #Send POST Request with user email to verification API
        body = {"email":self.email}
        req = requests.post(url, json=body)
        keyToCheck = req.text                           #Correct code from API

        def checkCode():                            #Function to check verification code
            self.buttonWorkspace.delete("error")    #Delete all error messages onscreen
            entry = codeEntry.get()                 #Get user entered value
            if str(entry) == str(keyToCheck):       #If the value matches, verification successful
                for widgets in self.buttonWorkspace.winfo_children():
                    widgets.destroy()
                #Success message
                self.buttonWorkspace.create_text(500,50, text="Verification Success! Please wait while your account is created.", font=("Modern_Mono",20), fill="green", tag="error")
                self.createDatabaseAccount()    #Create accound in database
            else:
                self.buttonWorkspace.create_text(500,20, text="Verification was Unsuccessful. Try Again.", font=("Modern_Mono",20), fill="red", tag="error")

        #Text and placeholders
        self.buttonWorkspace.create_text(500,20, text="An email has been sent with a verification code. Please enter it below.", font=("Modern Sans",20), fill="green", tag="error")
        self.buttonWorkspace.create_text(200,125, text="Enter code: ", font=("Modern Sans",25), fill="white", tag="code")
        codeEntry = customtkinter.CTkEntry(self.buttonWorkspace, width=400, height=50, border=0, bg_color="#141B2D", text_font=("Modern Sans", 20), show="*")
        codeEntry.pack()
        codeEntry.place(x=350, y=100)
        checkButton = customtkinter.CTkButton(self.buttonWorkspace, width=150, height=80, text="Submit", text_font=("Modern_Mono", 25), bg_color="#141B2D", command=checkCode)
        checkButton.pack()
        checkButton.place(x=800, y = 80) 
    
    def createDatabaseAccount(self):
        url = "https://register-api.vercel.app/registerUser/"
        body = {"email":self.email,
                "firstName":self.firstName,
                "lastName":self.lastName,
                "phoneNumber":self.phoneNumber,
                "password":self.password}

        req = requests.post(url, json=body)

        if req.text == "Account created sucessfully! You can now login.":
            self.buttonWorkspace.delete("error")
            self.buttonWorkspace.delete("code")
            self.buttonWorkspace.create_text(500,50, text="Account Created Successfully! You can now login.", font=("Modern_Mono",20), fill="green", tag="error")
        
        if req.text == "An account with the same email already exists!":
            self.buttonWorkspace.delete("error")
            self.buttonWorkspace.delete("code")
            self.buttonWorkspace.create_text(500,50, text="An account with the same email already exists! Please Login", font=("Modern_Mono",20), fill="red", tag="error")
        
        def proceedToLogin():
            self.prevmast.switchFrame("loginPage")

        loginButton = customtkinter.CTkButton(self.buttonWorkspace, width=150, height=80, text="Login", text_font=("Modern_Mono", 25), bg_color="#141B2D", command=proceedToLogin)
        loginButton.pack()
        loginButton.place(x=425, y=80)

if __name__ == "__main__":
    app = register()
    app.mainloop()