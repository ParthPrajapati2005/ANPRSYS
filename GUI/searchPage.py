import tkinter as tk
from tkinter import *
import os
import json
from PIL import Image, ImageTk
import customtkinter
import requests

class searchPage(tk.Canvas):
    prevmast = ()
    workspace = ()

    def __init__(self, master):
        tk.Canvas.__init__(self, master)
        self.prevmast = master
        screenwidth = master.winfo_screenwidth()
        screenheight = master.winfo_screenheight()
        master.geometry("{}x{}+{}+{}".format(screenwidth, screenheight,-1,1))
        self.prevmast.title("ANPR - Automatic Number Plate Recognition System") 

        screen = Canvas(self, highlightthickness=False, width=screenwidth, height=screenheight, bg="#141B2D") ##141B2D
        
        screen.icon_filePaths = {'dashboard-icon':os.path.join('GUI','Icons', 'dashboard-icon-48.png'),
                          'detect-icon':os.path.join('GUI','Icons', 'detect-icon-48.png'),
                          'database-icon':os.path.join('GUI','Icons', 'database-icon-48.png'),
                          'search-icon':os.path.join('GUI','Icons', 'search-icon-48.png'),
                          'search-icon-blue':os.path.join('GUI','Icons', 'search-icon-blue-48.png'),
                          'mot-icon':os.path.join('GUI','Icons', 'mot-icon-48.png'),
                          'settings-icon':os.path.join('GUI','Icons', 'settings-icon-48.png'),
                          'logoff-icon':os.path.join('GUI','Icons', 'logoff-icon-48.png'),
                          'empty-icon':os.path.join('GUI','Icons', 'empty-icon-48.png')}
        
        screen.icon_renders = {'dashboard-icon':ImageTk.PhotoImage(image=Image.open(screen.icon_filePaths['dashboard-icon'])),
                        'detect-icon':ImageTk.PhotoImage(master=screen, image=Image.open(screen.icon_filePaths['detect-icon'])),
                        'database-icon':ImageTk.PhotoImage(master=screen, image=Image.open(screen.icon_filePaths['database-icon'])),
                        'search-icon':ImageTk.PhotoImage(master=screen, image=Image.open(screen.icon_filePaths['search-icon-blue'])),
                        'mot-icon':ImageTk.PhotoImage(master=screen, image=Image.open(screen.icon_filePaths['mot-icon'])),
                        'settings-icon':ImageTk.PhotoImage(master=screen, image=Image.open(screen.icon_filePaths['settings-icon'])),
                        'logoff-icon':ImageTk.PhotoImage(master=screen, image=Image.open(screen.icon_filePaths['logoff-icon'])),
                        'empty-icon':ImageTk.PhotoImage(master=screen, image=Image.open(screen.icon_filePaths['empty-icon']))}

        screen.create_rectangle(0,0,100,screenheight, fill="#1F2940", outline="")   #212325

        dashboardButton = screen.create_image(50,50,image=screen.icon_renders['dashboard-icon'])
        screen.tag_bind(dashboardButton, "<Button-1>", self.switchDashboard)
        screen.create_text(50, 100, text="Dashboard", font=("Modern_Mono",15), fill='white')
        
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
    
        self.workspace = Canvas(screen, height=screenheight, width=screenwidth-100, highlightthickness=False, bg="#141B2D")
        self.workspace.place(x=100, y=100)
        screen.create_text(150, 60, fill="white", text="SEARCH", font=("Azonix", 40), anchor='w')

        self.build()
    
    def build(self):    
        self.workspace.create_text(450,100,fill="white",text="Enter the registration plate of the vehicle you wish to search below : ", font=("Modern_Mono",25),anchor="w", tag="workspaceItem")
        self.workspace.create_text(450,700,fill="green",text="Note : Private/Personalised plates also work using this function! ", font=("Modern_Mono",25), anchor="w", tag="workspaceItem")
        self.inputWorkspace = Canvas(self.workspace, height=145, width=640, bg="#f8bc04") ##f8bc04 yellow colour shade
        self.inputWorkspace.pack()
        self.workspace.create_window(300,300,window=self.inputWorkspace)
        self.inputWorkspace.place(x=615, y=228)
        self.workspace.regTemplatePath = os.path.join("GUI", "Icons", "reg-template.png")
        self.workspace.regTemplateRender = ImageTk.PhotoImage(master=self.workspace, image=Image.open(self.workspace.regTemplatePath))

        self.workspace.create_image(900, 300, image=self.workspace.regTemplateRender, tag="workspaceItem")

        def capitalise(event):
            var.set(var.get().upper())
        
        var = StringVar()
        self.inputEntry = Entry(self.inputWorkspace, font=("Charles Wright", 76), bg="#f8bc04", fg="black", width=10, highlightthickness=False, highlightcolor="#f8bc04", borderwidth=0, justify=CENTER, textvariable=var)
        self.inputEntry.pack()
        self.inputEntry.bind("<KeyRelease>", capitalise)

        def search():
            vehicleImageURL, vehicleLogoURL, vehicleDetails, vehicleMileages, status = self.vehicleLookup()

            if status == 1 or status == 2:
                self.displayDetails(vehicleImageURL, vehicleLogoURL, vehicleDetails, vehicleMileages, status)

            if status == 3:
                self.workspace.delete("error")
                self.workspace.create_text(700,450,text="The Number Plate is invalid!", tag="error", fill="red", font=("Modern_Mono",25), anchor="w")

        self.submitButton = customtkinter.CTkButton(self.workspace, text_font=("Modern_Mono", 25), text="Submit", width=200, height=100, command=search)
        self.submitButton.pack()
        self.submitButton.place(x=800, y=500)

    def displayDetails(self,vehicleImageURL, vehicleLogoURL, vehicleDetails, vehicleMileages, status):
        self.workspace.delete("workspaceItem")
        for widgets in self.workspace.winfo_children():
            widgets.destroy()
        
        com = Label(self.workspace, text="LOOKUP COMPLETE!", fg="lime", bg="#141B2D", font=("Azonix", 40), anchor="center")
        com.pack()

        displayWorkspace = ()
        displayWorkspace = Canvas(self.workspace, height=self.winfo_screenheight()-50, width=self.winfo_screenwidth()-100, bg="#141B2D", highlightthickness=False)
        displayWorkspace.pack(side="left")

        def reset():
            self.prevmast.switchFrame("searchPage")

        if status == 1:
            displayWorkspace.create_text(100,50,text=("REGISTRATION PLATE : "+vehicleDetails["Registration Plate"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,80,text=("MAKE : "+vehicleDetails["Make"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,110,text=("MODEL : "+vehicleDetails["Model"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,140,text=("COLOUR : "+vehicleDetails["Colour"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,170,text=("FUEL : "+vehicleDetails["Fuel"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,200,text=("VEHICLE TYPE : "+vehicleDetails["Vehicle Type"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,230,text=("BODY TYPE : "+vehicleDetails["Body Type"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,260,text=("EXPORTED VEHICLE : "+vehicleDetails["Exported Vehicle"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,290,text=("TOP SPEED : "+vehicleDetails["Top Speed"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,320,text=("0 - 60MPH TIME : "+vehicleDetails["0-60mph Time"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,350,text=("ENGINE CAPACITY : "+vehicleDetails["Engine Capacity"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,380,text=("HORSEPOWER : "+vehicleDetails["Horsepower"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,410,text=("ESTIMATED CURRENT MILEAGE : "+vehicleDetails["Estimated Current Mileage"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,440,text=("INSURANCE GROUP : "+vehicleDetails["Insurance Group"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,470,text=("VEHICLE AGE : "+(vehicleDetails["Vehicle Age"])[1:]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,500,text=("YEAR OF MANUFACTURE : "+vehicleDetails["Year of Manufacture"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,530,text=("SALVAGE HISTORY : "+vehicleDetails["Salvage History"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,560,text=("MOT DUE ON : "+vehicleDetails["MOT Due"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,590,text=("TAX DUE ON : "+vehicleDetails["TAX Due"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,620,text=("CARBON EMMISIONS : "+vehicleDetails["Carbon Emissions"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,650,text=("FUEL ECONOMY : "+vehicleDetails["Combined Fuel Economy"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,680,text=("AVERAGE TAX COST (12 MONTHS) : "+vehicleDetails["Average Tax Cost (12 Months)"]), font=("Modern_Mono",20), fill="white", anchor="nw")

        elif status == 2:
            displayWorkspace.create_text(100,50,text=("REGISTRATION PLATE : "+vehicleDetails["Registration Plate"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,80,text=("MAKE : "+vehicleDetails["make"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,110,text=("MODEL : "+vehicleDetails["model"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,140,text=("COLOUR : "+vehicleDetails["colour"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,170,text=("FUEL : "+vehicleDetails["fuelType"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,200,text=("VEHICLE TYPE : "+vehicleDetails["vehicleType"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,230,text=("BODY TYPE : "+vehicleDetails["bodyType"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,260,text=("EXPORTED VEHICLE : "+vehicleDetails["Exported"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,290,text=("TOP SPEED : "+vehicleDetails["topSpeed"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,320,text=("0 - 60MPH TIME : "+vehicleDetails["0-60mph"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,350,text=("ENGINE CAPACITY : "+str(vehicleDetails["engineCapacity"])), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,380,text=("HORSEPOWER : "+vehicleDetails["horsepower"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,410,text=("INSURANCE GROUP : "+vehicleDetails["insuranceGroup"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,440,text=("YEAR OF MANUFACTURE : "+str(vehicleDetails["yearOfManufacture"])), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,470,text=("REGISTERED IN : "+str(vehicleDetails["registeredNear"])), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,500,text=("MOT : "+vehicleDetails["motExpiry"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,530,text=("TAX : "+vehicleDetails["taxExpiry"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,560,text=("AVERAGE TAX COST (12 MONTHS) : "+vehicleDetails["taxCost12Months"]), font=("Modern_Mono",20), fill="white", anchor="nw")
        
        
        carImage = Image.open(requests.get(vehicleImageURL, stream = True).raw)
        resizedCarImage = carImage.resize((600,400),Image.ANTIALIAS)
        self.carImage = ImageTk.PhotoImage(resizedCarImage)

        logoImage = Image.open(requests.get(vehicleLogoURL, stream=True).raw)
        resizedLogoImage = logoImage.resize((300, 200), Image.ANTIALIAS)
        self.logoImage = ImageTk.PhotoImage(resizedLogoImage)

        displayWorkspace.create_image(1000, 250, image=self.carImage)
        displayWorkspace.create_image(1600, 250, image=self.logoImage)

        buttonWorkspace = Frame(displayWorkspace, height=300, width=550, highlightthickness=False, bg="#141B2D")
        buttonWorkspace.pack()
        displayWorkspace.create_window(1500,550, window=buttonWorkspace)

        resetButton = customtkinter.CTkButton(buttonWorkspace, text="SEARCH AGAIN", height=80, width=200, bg="#141B2D", command=reset)
        resetButton.pack()

    def vehicleLookup(self):
        finalPlate = self.inputEntry.get()
        body = {"registrationPlate" : str(finalPlate)}
        status = 0

        vehicleDetails = {}
        vehicleImages = {}
        vehicleImageURL = {}
        vehicleLogoURL = {}
        vehicleMileages = {}

        try:
            req1 = requests.post('https://vehicle-api-parth13075.vercel.app/getImages', json=body)
            req1a = requests.post('https://vehicle-api-parth13075.vercel.app/getImages2', json=body)
            if req1.status_code == 200:
                vehicleImages = json.loads(req1.text)
            else:
                vehicleImages = json.loads(req1a.text)
                
            vehicleImageURL = vehicleImages["carImageURL"]
            vehicleLogoURL = vehicleImages["logoImageURL"]

            req2 = requests.post('https://vehicle-api-parth13075.vercel.app/depthCheckAPI', json=body)
            req2a = requests.post('https://vehicle-api-parth13075.vercel.app/depthCheckAPI2', json=body)


            if req2.status_code == 200:
                vehicleDetails = json.loads(req2.text)
                status = 1
            else:
                vehicleDetails = json.loads(req2a.text)
                status = 2

            req3 = requests.post('https://vehicle-api-parth13075.vercel.app/getMileageHistory', json=body)
            vehicleMileages = json.loads(req3.text)
        except:
            status = 3

        return vehicleImageURL, vehicleLogoURL, vehicleDetails, vehicleMileages, status

    def switchDashboard(self, event):
        self.prevmast.switchFrame("homePage")

    def switchDetect(self, event):
        self.prevmast.switchFrame("detectPage")

    def switchDatabase(self, event):
        self.prevmast.switchFrame("databasePage")

    def switchSearch(self, event):
        pass

    def switchMOT(self, event):
        self.prevmast.switchFrame("motPage")
    
    def switchSettings(self, event):
        self.prevmast.switchFrame("settingsPage")

    def switchLogoff(self, event):
        self.prevmast.switchFrame("logoffPage")

if __name__ == "__main__":
    app = searchPage()
    app.mainloop()