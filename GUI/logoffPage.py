import tkinter as tk
from tkinter import *
import os
from PIL import Image, ImageTk
import customtkinter

class logoffPage(tk.Canvas):
    prevmast = ()

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
                          'mot-icon':os.path.join('GUI','Icons', 'mot-icon-48.png'),
                          'settings-icon':os.path.join('GUI','Icons', 'settings-icon-48.png'),
                          'logoff-icon':os.path.join('GUI','Icons', 'logoff-icon-48.png'),
                          'logoff-icon-blue':os.path.join('GUI','Icons', 'logoff-icon-blue-48.png'),
                          'empty-icon':os.path.join('GUI','Icons', 'empty-icon-48.png')}
        
        screen.icon_renders = {'dashboard-icon':ImageTk.PhotoImage(image=Image.open(screen.icon_filePaths['dashboard-icon'])),
                        'detect-icon':ImageTk.PhotoImage(master=screen, image=Image.open(screen.icon_filePaths['detect-icon'])),
                        'database-icon':ImageTk.PhotoImage(master=screen, image=Image.open(screen.icon_filePaths['database-icon'])),
                        'search-icon':ImageTk.PhotoImage(master=screen, image=Image.open(screen.icon_filePaths['search-icon'])),
                        'mot-icon':ImageTk.PhotoImage(master=screen, image=Image.open(screen.icon_filePaths['mot-icon'])),
                        'settings-icon':ImageTk.PhotoImage(master=screen, image=Image.open(screen.icon_filePaths['settings-icon'])),
                        'logoff-icon':ImageTk.PhotoImage(master=screen, image=Image.open(screen.icon_filePaths['logoff-icon-blue'])),
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

        workspace = Canvas(screen, height=screenheight, width=screenwidth-100, highlightthickness=False, bg="#141B2D")
        screen.create_window(-500,-500,window=workspace)
        workspace.place(x=100, y=0)

        self.build(screen, workspace)
    
    def build(self, screen, workspace):
        workspace.create_text(50, 60, fill="white", text="LOG OFF", font=("Azonix", 40), anchor='w')

        workspace.create_text(250,300, fill="white", text="Are you sure you wish to log off?", font=("Modern_Mono", 70), anchor="w")


        def logoff():
            self.prevmast.switchFrame("loginPage")

        logoffButton = customtkinter.CTkButton(workspace, width=300, height=100, bg_color="#141B2D",fg_color="red", text="LOG OFF",text_font=("Modern_Mono",30), command=logoff)
        logoffButton.pack()
        logoffButton.place(x=700, y=600)

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
        self.prevmast.switchFrame("settingsPage")

    def switchLogoff(self, event):
        pass

if __name__ == "__main__":
    app = logoffPage()
    app.mainloop()