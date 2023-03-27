import tkinter as tk
from tkinter import *
import os
import requests
import customtkinter
from PIL import Image, ImageTk

class settingsPage(tk.Canvas):
    prevmast = ()

    def __init__(self, master):
        tk.Canvas.__init__(self, master)
        self.prevmast = master
        screenwidth = master.winfo_screenwidth()
        screenheight = master.winfo_screenheight()
        master.geometry("{}x{}+{}+{}".format(screenwidth, screenheight,-1,1))
        self.prevmast.title("ANPR - Automatic Number Plate Recognition System") 

        #Create Tkinter canvas, Disable borders, Set background colour to navy blue, Set dimensions to fill screen
        screen = Canvas(self, highlightthickness=False, width=screenwidth, height=screenheight, bg="#141B2D") 
        
        #Create a rectangle shape at coordinate (0,0) with width 100 and height= screenheight. 
        screen.create_rectangle(0,0,100,screenheight, fill="#1F2940", outline="")   #Colour is a lighter shade of navy blue, no border

        #Define File paths
        screen.icon_filePaths = {'dashboard-icon':os.path.join('GUI','Icons', 'dashboard-icon-48.png'),
                          'detect-icon':os.path.join('GUI','Icons', 'detect-icon-48.png'),
                          'database-icon':os.path.join('GUI','Icons', 'database-icon-48.png'),
                          'search-icon':os.path.join('GUI','Icons', 'search-icon-48.png'),
                          'mot-icon':os.path.join('GUI','Icons', 'mot-icon-48.png'),
                          'settings-icon':os.path.join('GUI','Icons', 'settings-icon-48.png'),
                          'settings-icon-blue':os.path.join('GUI','Icons', 'settings-icon-blue-48.png'),
                          'logoff-icon':os.path.join('GUI','Icons', 'logoff-icon-48.png')}
                          
        #Create PhotoImage object for Tkinter
        screen.icon_renders = {'dashboard-icon':ImageTk.PhotoImage(image=Image.open(screen.icon_filePaths['dashboard-icon'])),
                        'detect-icon':ImageTk.PhotoImage(master=screen, image=Image.open(screen.icon_filePaths['detect-icon'])),
                        'database-icon':ImageTk.PhotoImage(master=screen, image=Image.open(screen.icon_filePaths['database-icon'])),
                        'search-icon':ImageTk.PhotoImage(master=screen, image=Image.open(screen.icon_filePaths['search-icon'])),
                        'mot-icon':ImageTk.PhotoImage(master=screen, image=Image.open(screen.icon_filePaths['mot-icon'])),
                        'settings-icon':ImageTk.PhotoImage(master=screen, image=Image.open(screen.icon_filePaths['settings-icon-blue'])),
                        'logoff-icon':ImageTk.PhotoImage(master=screen, image=Image.open(screen.icon_filePaths['logoff-icon']))}

        
        #Display icons on main UI with position x value 50 and y difference of 150 px
        dashboardButton = screen.create_image(50,50,image=screen.icon_renders['dashboard-icon'])    #Image object referenced from dictionary
        screen.tag_bind(dashboardButton, "<Button-1>", self.switchDashboard)                        #Bind button and reference function
        screen.create_text(50, 100, text="Dashboard", font=("Modern_Mono",15), fill='white')        #Create caption under Icon
        
        detectButton = screen.create_image(50, 200, image=screen.icon_renders['detect-icon'])
        screen.tag_bind(detectButton, "<Button-1>", self.switchDetect)
        screen.create_text(50, 250, text="Detect", font=("Modern_Mono",15), fill='white')

        databaseButton = screen.create_image(50,350, image=screen.icon_renders['database-icon'])
        screen.tag_bind(databaseButton, "<Button-1>", self.switchDatabase)
        screen.create_text(50, 400, text="Database", font=("Modern_Mono",15), fill='white')

        searchButton = screen.create_image(50,500, image=screen.icon_renders['search-icon'])
        screen.tag_bind(searchButton, "<Button-1>", self.switchSearch)
        screen.create_text(50, 550, text="Search", font=("Modern_Mono",15), fill='white')

        motButton = screen.create_image(50,650, image=screen.icon_renders['mot-icon'])
        screen.tag_bind(motButton, "<Button-1>", self.switchMOT)
        screen.create_text(50, 700, text="MOT", font=("Modern_Mono",15), fill='white')

        settingsButton = screen.create_image(50,800, image=screen.icon_renders['settings-icon'])
        screen.tag_bind(settingsButton, "<Button-1>", self.switchSettings)
        screen.create_text(50, 850, text="Settings", font=("Modern_Mono",15), fill='white')

        logoffButton = screen.create_image(50,950, image=screen.icon_renders['logoff-icon'])
        screen.tag_bind(logoffButton, "<Button-1>", self.switchLogoff)
        screen.create_text(50, 1000, text="Log Off", font=("Modern_Mono",15), fill='white')

        screen.pack(side=LEFT)

        workspace = Canvas(screen, height=screenheight, width=screenwidth-100, highlightthickness=False, bg="#141B2D")
        screen.create_window(-500,-500,window=workspace)
        workspace.place(x=100, y=0)

        self.build(screen, workspace)
    
    def build(self, screen, workspace):

        user_email = self.prevmast.detectionUser        #Get user details from global variable
        user_FirstName = self.prevmast.userFirstName
        user_LastName = self.prevmast.userLastName
        user_PhoneNumber = self.prevmast.userPhoneNumber

        workspace.create_text(50, 60, fill="white", text="SETTINGS", font=("Azonix", 40), anchor='w') # Title header

        self.settingsWorkspace = Canvas(workspace, height=self.winfo_screenheight()-100, width=self.winfo_screenwidth(), bg="#141B2D", highlightthickness=False)
        self.settingsWorkspace.pack(pady=100)
        
        self.settingsWorkspace.create_text(100, 100, fill="white", text=("Registered Email\t : "+user_email), font=("Modern Sans",25), anchor="w")
        self.settingsWorkspace.create_text(100, 150, fill="white", text=("First Name\t : "+user_FirstName), font=("Modern Sans",25), anchor="w")
        self.settingsWorkspace.create_text(100, 200, fill="white", text=("Last Name\t : "+user_LastName), font=("Modern Sans",25), anchor="w")
        self.settingsWorkspace.create_text(100, 250, fill="white", text=("Phone Number\t : "+user_PhoneNumber), font=("Modern Sans",25), anchor="w")

        self.settingsWorkspace.create_text(100, 350, fill="red", text=("WARNING : This function will permenantly erase all detection database records for this account!!"), font=("Modern Sans",25), anchor="w")
        self.settingsWorkspace.create_text(100, 450, fill="white", text=("Reset Database\t :"), font=("Modern Sans",25), anchor="w")

        def resetDatabase():
            data = {"email":user_email}
            x = requests.post("https://register-api.vercel.app/clearDatabase", json=data)
            if x.status_code == 200:
                self.settingsWorkspace.create_text(1000, 450, fill="green", text=("The database has been cleared successfully!"), font=("Modern Sans",20), anchor="w")
            else:
                self.settingsWorkspace.create_text(1000, 450, fill="red", text=("There was an error."), font=("Modern Sans",20), anchor="w")

        buttonWorkspace = Canvas(self.settingsWorkspace, height=100, width=420, bg="red", highlightthickness=False)
        buttonWorkspace.pack()
        self.settingsWorkspace.create_window(0,0,window=buttonWorkspace)
        buttonWorkspace.place(x=450,y=420)
        resetDatabaseBtn = customtkinter.CTkButton(buttonWorkspace, width=400, height=60, text="Delete all database records?", text_font=("Modern_Mono",25), bg_color="#141B2D",fg_color="red", command=resetDatabase)
        resetDatabaseBtn.pack()


    def switchDashboard(self, event):
        self.prevmast.switchFrame("homePage")

    def switchDetect(self, event):
        self.prevmast.switchFrame("detectPage")

    def switchDatabase(self, event):
        self.prevmast.switchFrame("databasePage")

    def switchSearch(self, event):
        self.prevmast.switchFrame("searchPage")

    def switchMOT(self, event):
        self.prevmast.switchFrame("motPage")
    
    def switchSettings(self, event):
        pass

    def switchLogoff(self, event):
        self.prevmast.switchFrame("logoffPage")

if __name__ == "__main__":
    app = settingsPage()
    app.mainloop()