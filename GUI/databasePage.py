import tkinter as tk
from tkinter import *
from tkinter import ttk
import os
import mysql.connector
import customtkinter
from PIL import Image, ImageTk

class databasePage(tk.Canvas):
    prevmast = ()

    def __init__(self, master):
        tk.Canvas.__init__(self, master)
        self.prevmast = master
        screenwidth = master.winfo_screenwidth()
        screenheight = master.winfo_screenheight()
        master.geometry("{}x{}+{}+{}".format(screenwidth, screenheight,-1,1))
        self.prevmast.title("ANPR - Automatic Number Plate Recognition System") 

        #workspace = ()
        #tree = ()

        screen = Canvas(self, highlightthickness=False, width=screenwidth, height=screenheight, bg="#141B2D") ##141B2D
        
        screen.icon_filePaths = {'dashboard-icon':os.path.join('GUI','Icons', 'dashboard-icon-48.png'),
                          'detect-icon':os.path.join('GUI','Icons', 'detect-icon-48.png'),
                          'database-icon':os.path.join('GUI','Icons', 'database-icon-48.png'),
                          'database-icon-blue':os.path.join('GUI','Icons', 'database-icon-blue-48.png'),
                          'search-icon':os.path.join('GUI','Icons', 'search-icon-48.png'),
                          'mot-icon':os.path.join('GUI','Icons', 'mot-icon-48.png'),
                          'settings-icon':os.path.join('GUI','Icons', 'settings-icon-48.png'),
                          'logoff-icon':os.path.join('GUI','Icons', 'logoff-icon-48.png'),
                          'empty-icon':os.path.join('GUI','Icons', 'empty-icon-48.png')}
        
        screen.icon_renders = {'dashboard-icon':ImageTk.PhotoImage(image=Image.open(screen.icon_filePaths['dashboard-icon'])),
                        'detect-icon':ImageTk.PhotoImage(master=screen, image=Image.open(screen.icon_filePaths['detect-icon'])),
                        'database-icon':ImageTk.PhotoImage(master=screen, image=Image.open(screen.icon_filePaths['database-icon-blue'])),
                        'search-icon':ImageTk.PhotoImage(master=screen, image=Image.open(screen.icon_filePaths['search-icon'])),
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
        screen.create_window(-500,-500,window=self.workspace)
        self.workspace.place(x=100, y=0)

        self.build()
    
    def build(self):
        self.workspace.create_text(50, 60, fill="white", text="DATABASE", font=("Azonix", 40), anchor='w') # Page Title

        self.searchVar = StringVar()    #Create stringVar to search database as user types into box
        self.workspace.create_text(50, 180, fill="white", text="Search Database : ", font=("Modern_Mono", 25), anchor="w")  #Caption
        
        entryBox = customtkinter.CTkEntry(self.workspace, height=50, width=300, text_font=("Modern_Mono", 25), textvariable=self.searchVar) #Create entry box
        entryBox.bind("<Key>", self.search)
        entryBox.pack()
        entryBox.place(x=320, y=160)

        self.dataBaseWorkspace = Frame(self.workspace)  #Database frame
        self.dataBaseWorkspace.pack(padx=50, pady=300)

        user_email = self.prevmast.detectionUser        #Get user details from global variable
        user_password = self.prevmast.detectionPassword

        mydb = mysql.connector.connect(                 #Connect to database
        host="132.145.65.198",
        user=user_email,
        password=user_password,
        auth_plugin='mysql_native_password',
        database= "anprDATABASE"
        )

        mycursor = mydb.cursor()                    #DB Object
        mycursor.execute("SHOW TABLES;")            #Get Table
        self.table = (mycursor.fetchone()[0]).decode("utf-8")

        getRows = "SELECT * FROM "+self.table   #Get all rows in database
        mycursor.execute(getRows)

        self.tree = ttk.Treeview(self.dataBaseWorkspace)   #Create Table object
        self.tree['show'] = 'headings'                     #Show headings in table

        style = ttk.Style(self.dataBaseWorkspace)          #Style Table 
        style.theme_use("default")
        style.configure("Treeview.Heading", font=("Modern_Mono", 20, "bold"), rowheight=80)
        style.configure(".", font=("Modern_Mono", 17,))
        style.configure("Treeview.Heading", fieldbackground="#141B2D", background="#141B2D", foreground="white", borderwidth=0)
        style.configure("Treeview", fieldbackground="#141B2D", background="#141B2D", foreground="white", rowheight=60, borderwidth=0)
        style.configure("arrowless.Horizontal.TScrollbar", background="white",  arrowcolor="#141B2D", troughcolor = "#141B2D", borderwidth=0)
        style.configure("arrowless.Vertical.TScrollbar", background="white", arrowcolor="#141B2D", troughcolor = "#141B2D", borderwidth=0)

        self.tree["columns"] = ("detection_id",     #Confingure columns
                    "registrationPlate",
                    "dateOfDetection",
                    "timeOfDetection",
                    "vehicleMake",
                    "vehicleModel",
                    "vehicleColour",
                    "vehicleFuelType",
                    "vehicleType",
                    "vehicleBodyType",
                    "vehicleExported",
                    "vehicleTopSpeed",
                    "vehicle60Time",
                    "vehicleEngineCapacity",
                    "vehicleHorsepower",
                    "vehicleEstimatedMileage",
                    "vehicleInsuranceGroup",
                    "vehicleAge",
                    "vehicleYOM",
                    "vehicleSalvage",
                    "vehicleMOTDue",
                    "vehicleTAXDue",
                    "vehicleCarbonEmissions",
                    "vehicleFuelEconomy",
                    "vehicleTaxCost")

        columnWidth = round((self.winfo_screenwidth()-300)/24)      #Set column width  
        self.tree.column("detection_id", width=columnWidth, minwidth=200, anchor=CENTER)        #Configure column positioning
        self.tree.column("registrationPlate", width=columnWidth, minwidth=200, anchor=CENTER)
        self.tree.column("dateOfDetection", width=columnWidth, minwidth=220, anchor=CENTER)
        self.tree.column("timeOfDetection", width=columnWidth, minwidth=200, anchor=CENTER)
        self.tree.column("vehicleMake", width=columnWidth, minwidth=200, anchor=CENTER)
        self.tree.column("vehicleModel", width=columnWidth, minwidth=300, anchor=CENTER)
        self.tree.column("vehicleColour", width=columnWidth, minwidth=200, anchor=CENTER)
        self.tree.column("vehicleFuelType", width=columnWidth, minwidth=200, anchor=CENTER)
        self.tree.column("vehicleType", width=columnWidth, minwidth=200, anchor=CENTER)
        self.tree.column("vehicleBodyType", width=columnWidth, minwidth=200, anchor=CENTER)
        self.tree.column("vehicleExported", width=columnWidth, minwidth=200, anchor=CENTER)
        self.tree.column("vehicleTopSpeed", width=columnWidth, minwidth=200, anchor=CENTER)
        self.tree.column("vehicle60Time", width=columnWidth, minwidth=200, anchor=CENTER)
        self.tree.column("vehicleEngineCapacity", width=columnWidth, minwidth=200, anchor=CENTER)
        self.tree.column("vehicleHorsepower", width=columnWidth, minwidth=200, anchor=CENTER)
        self.tree.column("vehicleEstimatedMileage", width=columnWidth, minwidth=230, anchor=CENTER)
        self.tree.column("vehicleInsuranceGroup", width=columnWidth, minwidth=220, anchor=CENTER)
        self.tree.column("vehicleAge", width=columnWidth, minwidth=200, anchor=CENTER)
        self.tree.column("vehicleYOM", width=columnWidth, minwidth=250, anchor=CENTER)
        self.tree.column("vehicleSalvage", width=columnWidth, minwidth=200, anchor=CENTER)
        self.tree.column("vehicleMOTDue", width=columnWidth, minwidth=250, anchor=CENTER)
        self.tree.column("vehicleTAXDue", width=columnWidth, minwidth=250, anchor=CENTER)
        self.tree.column("vehicleCarbonEmissions", width=columnWidth, minwidth=220, anchor=CENTER)
        self.tree.column("vehicleFuelEconomy", width=columnWidth, minwidth=200, anchor=CENTER)
        self.tree.column("vehicleTaxCost", width=columnWidth, minwidth=200, anchor=CENTER)

        self.tree.heading("detection_id", text="Detection ID", anchor=CENTER)       #Configure headings
        self.tree.heading("registrationPlate", text="Registration", anchor=CENTER)
        self.tree.heading("dateOfDetection", text="Date of Detection", anchor=CENTER)
        self.tree.heading("timeOfDetection", text="Time", anchor=CENTER)
        self.tree.heading("vehicleMake", text="Make", anchor=CENTER)
        self.tree.heading("vehicleModel", text="Model", anchor=CENTER)
        self.tree.heading("vehicleColour", text="Colour", anchor=CENTER)
        self.tree.heading("vehicleFuelType", text="Fuel", anchor=CENTER)
        self.tree.heading("vehicleType", text="Vehicle Type", anchor=CENTER)
        self.tree.heading("vehicleBodyType", text="Body Type", anchor=CENTER)
        self.tree.heading("vehicleExported", text="Exported", anchor=CENTER)
        self.tree.heading("vehicleTopSpeed", text="Top Speed", anchor=CENTER)
        self.tree.heading("vehicle60Time", text="0-60mph", anchor=CENTER)
        self.tree.heading("vehicleEngineCapacity", text="Engine Capacity", anchor=CENTER)
        self.tree.heading("vehicleHorsepower", text="Horsepower", anchor=CENTER)
        self.tree.heading("vehicleEstimatedMileage", text="Estimated Mileage", anchor=CENTER)
        self.tree.heading("vehicleInsuranceGroup", text="Insurance Group", anchor=CENTER)
        self.tree.heading("vehicleAge", text="Vehicle Age", anchor=CENTER)
        self.tree.heading("vehicleYOM", text="Year of Manufacture", anchor=CENTER)
        self.tree.heading("vehicleSalvage", text="Salvaged", anchor=CENTER)
        self.tree.heading("vehicleMOTDue", text="MOT Due", anchor=CENTER)
        self.tree.heading("vehicleTAXDue", text="TAX Due", anchor=CENTER)
        self.tree.heading("vehicleCarbonEmissions", text="Carbon Emissions", anchor=CENTER)
        self.tree.heading("vehicleFuelEconomy", text="Fuel Economy", anchor=CENTER)
        self.tree.heading("vehicleTaxCost", text="TAX Cost", anchor=CENTER)

        i = 0
        for row in mycursor:                                    #Insert values into table 
            self.tree.insert("", i, text="", values=(row[0], 
                                                row[1], 
                                                row[2], 
                                                row[3], 
                                                row[4], 
                                                row[5], 
                                                row[6],
                                                row[7], 
                                                row[8], 
                                                row[9], 
                                                row[10], 
                                                row[11], 
                                                row[12], 
                                                row[13], 
                                                row[14], 
                                                row[15], 
                                                row[16], 
                                                row[17], 
                                                row[18], 
                                                row[19],
                                                row[20], 
                                                row[21], 
                                                row[22], 
                                                row[23],
                                                row[24]))
            i = i + 1
        tree_scrollx = ttk.Scrollbar(self.dataBaseWorkspace, orient=tk.HORIZONTAL, command=self.tree.xview, style='arrowless.Horizontal.TScrollbar')
        tree_scrollx.pack(side=tk.BOTTOM, fill=tk.X)        #Configure and place horizontal scrollbar
        
        tree_scrolly = ttk.Scrollbar(self.dataBaseWorkspace, orient=tk.VERTICAL, command=self.tree.yview, style='arrowless.Vertical.TScrollbar')
        tree_scrolly.pack(side=tk.RIGHT, fill=tk.Y)         #Configure and place vertical scrollbar

        self.tree.pack()                                    #Pack table object
        self.tree.config(xscrollcommand=tree_scrollx.set)
      
    def search(self, event):                    #Database search function

        user_email = self.prevmast.detectionUser                #Get user details
        user_password = self.prevmast.detectionPassword

        mydb = mysql.connector.connect(     #Connect to database
            host="132.145.65.198",
            user=user_email,
            password=user_password,
            auth_plugin='mysql_native_password',
            database= "anprDATABASE"
            )
        mycursor = mydb.cursor()            #DB Object

        try:                    #Try to search the database where search term is similar
            command = "SELECT * FROM "+self.table+" where registrationPlate LIKE '%"+self.searchVar.get()+"%'"
            mycursor.execute(command)
            row = mycursor.fetchall()

            if len(row) > 0:
                self.tree.delete(*self.tree.get_children())         #Delete irrevelavnt values
                for i in row:
                    self.tree.insert('',END,values=i)               
            else:
                self.tree.delete(*self.tree.get_children())
            
        except Exception as ex:
            print(ex)
 
    def switchDashboard(self, event):
        self.prevmast.switchFrame("homePage")

    def switchDetect(self, event):
        self.prevmast.switchFrame("detectPage")

    def switchDatabase(self, event):
        pass

    def switchSearch(self, event):
        self.prevmast.switchFrame("searchPage")

    def switchMOT(self, event):
        self.prevmast.switchFrame("motPage")
    
    def switchSettings(self, event):
        self.prevmast.switchFrame("settingsPage")

    def switchLogoff(self, event):
        self.prevmast.switchFrame("logoffPage")

if __name__ == "__main__":
    app = databasePage()
    app.mainloop()