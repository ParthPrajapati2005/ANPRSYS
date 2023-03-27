from tkinter import *
import tkinter as tk
import customtkinter
from PIL import Image, ImageTk
import os

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

class homeScreenInstance():
    homeRoot = customtkinter.CTk()
    screenheight = homeRoot.winfo_screenheight()
    screenwidth = homeRoot.winfo_screenwidth()
    homeRoot.geometry("{}x{}+{}+{}".format(screenwidth, screenheight,-1,1))
    homeRoot.title("ANPR - Automatic Number Plate Recognition System") 
    prevmast = ()

    def __init__(self, master):
        #CONSTANTS & INITIALISATION
        self.prevmast = master
        screen = Canvas(self.homeRoot, bg="#141B2D", highlightthickness=False, width=100, height=self.screenheight)
        
        icon_filePaths = {'dashboard-icon':os.path.join('GUI','Icons', 'dashboard-icon-48.png'),
                          'dashboard-icon-blue':os.path.join('GUI','Icons', 'dashboard-icon-blue-48.png'),
                          'detect-icon':os.path.join('GUI','Icons', 'detect-icon-48.png'),
                          'database-icon':os.path.join('GUI','Icons', 'database-icon-48.png'),
                          'search-icon':os.path.join('GUI','Icons', 'search-icon-48.png'),
                          'mot-icon':os.path.join('GUI','Icons', 'mot-icon-48.png'),
                          'settings-icon':os.path.join('GUI','Icons', 'settings-icon-48.png'),
                          'logoff-icon':os.path.join('GUI','Icons', 'logoff-icon-48.png'),
                          'empty-icon':os.path.join('GUI','Icons', 'empty-icon-48.png')}
        
        icon_renders = {'dashboard-icon':ImageTk.PhotoImage(master=screen, image=Image.open(icon_filePaths['dashboard-icon-blue'])),
                        'detect-icon':ImageTk.PhotoImage(master=screen, image=Image.open(icon_filePaths['detect-icon'])),
                        'database-icon':ImageTk.PhotoImage(master=screen, image=Image.open(icon_filePaths['database-icon'])),
                        'search-icon':ImageTk.PhotoImage(master=screen, image=Image.open(icon_filePaths['search-icon'])),
                        'mot-icon':ImageTk.PhotoImage(master=screen, image=Image.open(icon_filePaths['mot-icon'])),
                        'settings-icon':ImageTk.PhotoImage(master=screen, image=Image.open(icon_filePaths['settings-icon'])),
                        'logoff-icon':ImageTk.PhotoImage(master=screen, image=Image.open(icon_filePaths['logoff-icon'])),
                        'empty-icon':ImageTk.PhotoImage(master=screen, image=Image.open(icon_filePaths['empty-icon']))}

        screen.create_rectangle(0,0,100,self.screenheight, fill="#1F2940", outline="")   #212325

        dashboardButton = screen.create_image(50,50,image=icon_renders['dashboard-icon'])
        screen.tag_bind(dashboardButton, "<Button-1>", self.switchDashboard)
        screen.create_text(50, 100, text="Dashboard", font=("Modern_Mono",15), fill='white')
        
        detectButton = screen.create_image(50, 200, image=icon_renders['detect-icon'])
        screen.tag_bind(detectButton, "<Button-1>", self.switchDetect)
        screen.create_text(50, 250, text="Detect", font=("Modern_Mono",15), fill='white')

        databaseButton = screen.create_image(50,350, image=icon_renders['database-icon'])
        screen.tag_bind(databaseButton, "<Button-1>", self.switchDatabase)
        screen.create_text(50, 400, text="Database", font=("Modern_Mono",15), fill='white')

        searchButton = screen.create_image(50,500, image=icon_renders['search-icon'])
        screen.tag_bind(searchButton, "<Button-1>", self.switchSearch)
        screen.create_text(50, 550, text="Search", font=("Modern_Mono",15), fill='white')

        motButton = screen.create_image(50,650, image=icon_renders['mot-icon'])
        screen.tag_bind(motButton, "<Button-1>", self.switchMOT)
        screen.create_text(50, 700, text="MOT", font=("Modern_Mono",15), fill='white')

        settingsButton = screen.create_image(50,800, image=icon_renders['settings-icon'])
        screen.tag_bind(settingsButton, "<Button-1>", self.switchSettings)
        screen.create_text(50, 850, text="Settings", font=("Modern_Mono",15), fill='white')

        logoffButton = screen.create_image(50,950, image=icon_renders['logoff-icon'])
        screen.tag_bind(logoffButton, "<Button-1>", self.switchLogoff)
        screen.create_text(50, 1000, text="Log Off", font=("Modern_Mono",15), fill='white')

        screen.pack(side=LEFT)

        self.homeRoot.mainloop()
    
    def switchDashboard(self, event):
        self.prevmast.switchFrame("homePage")

    def switchDetect(self, event):
        #self.homeRoot.destroy()
        self.prevmast.switchFrame("detectPage")

    def switchDatabase(self, event):
        #self.homeRoot.destroy()
        self.prevmast.switchFrame("databasePage")

    def switchSearch(self, event):
        self.homeRoot.destroy()
        self.prevmast.switchFrame("searchPage")

    def switchMOT(self, event):
        self.homeRoot.destroy()
        self.prevmast.switchFrame("motPage")
    
    def switchSettings(self, event):
        self.homeRoot.destroy()
        self.prevmast.switchFrame("settingsPage")

    def switchLogoff(self, event):
        self.homeRoot.destroy()
        self.prevmast.switchFrame("logoffPage")
        