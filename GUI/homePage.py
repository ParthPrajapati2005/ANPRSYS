import tkinter as tk
from tkinter import *
import os
import mysql.connector
from PIL import Image, ImageTk

class homePage(tk.Canvas):
    prevmast = ()

    def __init__(self, master):
        screenwidth = master.winfo_screenwidth()
        screenheight = master.winfo_screenheight()
        master.geometry("{}x{}+{}+{}".format(screenwidth, screenheight,-1,1))
        tk.Canvas.__init__(self, master, height=screenheight, width=screenwidth)
        self.prevmast = master
        self.prevmast.title("ANPR - Automatic Number Plate Recognition System") 

        screen = Canvas(self, highlightthickness=False, width=screenwidth, height=screenheight, bg="#141B2D") ##141B2D
        

        screen.icon_filePaths = {'dashboard-icon':os.path.join('GUI','Icons', 'dashboard-icon-48.png'),
                          'dashboard-icon-blue':os.path.join('GUI','Icons', 'dashboard-icon-blue-48.png'),
                          'detect-icon':os.path.join('GUI','Icons', 'detect-icon-48.png'),
                          'database-icon':os.path.join('GUI','Icons', 'database-icon-48.png'),
                          'search-icon':os.path.join('GUI','Icons', 'search-icon-48.png'),
                          'mot-icon':os.path.join('GUI','Icons', 'mot-icon-48.png'),
                          'settings-icon':os.path.join('GUI','Icons', 'settings-icon-48.png'),
                          'logoff-icon':os.path.join('GUI','Icons', 'logoff-icon-48.png'),
                          'empty-icon':os.path.join('GUI','Icons', 'empty-icon-48.png')}
        
        screen.icon_renders = {'dashboard-icon':ImageTk.PhotoImage(image=Image.open(screen.icon_filePaths['dashboard-icon-blue'])),
                        'detect-icon':ImageTk.PhotoImage(master=screen, image=Image.open(screen.icon_filePaths['detect-icon'])),
                        'database-icon':ImageTk.PhotoImage(master=screen, image=Image.open(screen.icon_filePaths['database-icon'])),
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
        
        screen.pack(side=tk.LEFT,expand=Y,fill=BOTH)

        workspace = Canvas(screen, height=screenheight, width=screenwidth-100, highlightthickness=False, bg="#141B2D")
        screen.create_window(-500,-500,window=workspace)
        workspace.place(x=100, y=0)

        self.build(screen, workspace)
    
    def build(self, screen, workspace):
        workspace.create_text(50, 60, fill="white", text="DASHBOARD", font=("Azonix", 40), anchor='w')
        self.dashWorkspace = Canvas(workspace, height=self.winfo_screenheight()-100, width=self.winfo_screenwidth(), bg="#141B2D", highlightthickness=False)
        self.dashWorkspace.pack(pady=100)
        user_FirstName = self.prevmast.userFirstName
        user_LastName = self.prevmast.userLastName

        self.dashWorkspace.create_text((self.winfo_screenwidth()-100)/2,100, text=("Welcome, "+user_FirstName+" "+user_LastName), font=("Modern Sans", 40), fill="white", anchor="center")

        mydb = mysql.connector.connect(       #Try to connect to the databse with the details provided
                    host="132.145.65.198",
                    user=self.prevmast.detectionUser,
                    password=self.prevmast.detectionPassword,
                    auth_plugin='mysql_native_password',
                    database= "anprDATABASE"
                    )
        mycursor = mydb.cursor()                #DB Object
        mycursor.execute("SHOW TABLES;")        #Execute SHOW Tables command
        table = (mycursor.fetchone()[0]).decode("utf-8")  #Convert bytearray object to string
        mycursor.execute("SELECT * FROM "+table+";")
        try:
            lastDetection = mycursor.fetchall()[-1]
            print(lastDetection)
            self.dashWorkspace.create_text(200,300, text=("TOTAL DETECTIONS"), font=("Modern Sans", 40), fill="white", anchor="w")
            self.dashWorkspace.create_text(410,385, text=(lastDetection[0]), font=("Modern Sans", 60), fill="white", anchor="center")

            self.dashWorkspace.create_text(200,550, text=("LAST DETECTION"), font=("Modern Sans", 40), fill="white", anchor="w")
            self.dashWorkspace.create_text(410,685, text=(lastDetection[1]), font=("Modern Sans", 60), fill="white", anchor="center")

            self.dashWorkspace.create_text(900,280, text=("VEHICLE MAKE \t\t:"+lastDetection[4]), font=("Modern Sans", 25), fill="white", anchor="w")
            self.dashWorkspace.create_text(900,320, text=("VEHICLE MODEL \t\t:"+lastDetection[5]), font=("Modern Sans", 25), fill="white", anchor="w")
            self.dashWorkspace.create_text(900,360, text=("COLOUR \t\t:"+lastDetection[6]), font=("Modern Sans", 25), fill="white", anchor="w")
            self.dashWorkspace.create_text(900,400, text=("FUEL TYPE \t\t:"+lastDetection[7]), font=("Modern Sans", 25), fill="white", anchor="w")
            self.dashWorkspace.create_text(900,440, text=("BODY TYPE \t\t:"+lastDetection[9]), font=("Modern Sans", 25), fill="white", anchor="w")
            self.dashWorkspace.create_text(900,480, text=("EXPORTED? \t\t:"+lastDetection[10]), font=("Modern Sans", 25), fill="white", anchor="w")
            self.dashWorkspace.create_text(900,520, text=("TOP SPEED \t\t:"+lastDetection[11]), font=("Modern Sans", 25), fill="white", anchor="w")
            self.dashWorkspace.create_text(900,560, text=("0 - 60MPH \t\t:"+lastDetection[12]), font=("Modern Sans", 25), fill="white", anchor="w")
            self.dashWorkspace.create_text(900,600, text=("ENGINE CAPACITY \t:"+lastDetection[13]), font=("Modern Sans", 25), fill="white", anchor="w")
            self.dashWorkspace.create_text(900,640, text=("HORSEPOWER \t\t:"+lastDetection[14]), font=("Modern Sans", 25), fill="white", anchor="w")
            self.dashWorkspace.create_text(900,680, text=("ESTIMATED MILEAGE \t:"+lastDetection[15]), font=("Modern Sans", 25), fill="white", anchor="w")
            self.dashWorkspace.create_text(900,720, text=("INSURANCE GROUP \t:"+lastDetection[16]), font=("Modern Sans", 25), fill="white", anchor="w")


        except:
            self.dashWorkspace.create_text(200,300, text=("TOTAL DETECTIONS"), font=("Modern Sans", 40), fill="white", anchor="w")
            self.dashWorkspace.create_text(410,385, text=("0"), font=("Modern Sans", 60), fill="white", anchor="center")

            self.dashWorkspace.create_text(200,550, text=("LAST DETECTION"), font=("Modern Sans", 40), fill="white", anchor="w")
            self.dashWorkspace.create_text(410,685, text=("--"), font=("Modern Sans", 60), fill="white", anchor="center")

        

        
    def switchDashboard(self, event):
        pass

    def switchDetect(self, event):
        self.prevmast.switchFrame("detectPage")

    def switchDatabase(self, event):
        self.prevmast.switchFrame("databasePage")

    def switchSearch(self, event):
        self.prevmast.switchFrame("searchPage")

    def switchMOT(self, event):
        self.prevmast.switchFrame("motPage")
    
    def switchSettings(self, event):
        self.prevmast.switchFrame("settingsPage")

    def switchLogoff(self, event):
        self.prevmast.switchFrame("logoffPage")

if __name__ == "__main__":
    app = homePage()
    app.mainloop()