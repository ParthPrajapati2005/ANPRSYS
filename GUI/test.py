import customtkinter                                        #Import customtkinter library
root = customtkinter.CTk()                                  #Define root variable
customtkinter.set_default_color_theme("dark-blue")          #Define customtkinter theme
screenheight = root.winfo_screenheight()                    #Fetch screenheight
screenwidth = root.winfo_screenwidth()                      #Fetch screenwidth
root.title("ANPR")                                          #Set Window title
root.geometry(str(screenwidth)+"x"+str(screenheight))       #Set screen dimensions
root.configure(bg="#141B2D")                                #Set screen background colour
root.mainloop()                                             #Launch GUI

######################################################################################################

import customtkinter                                        #Import customtkinter library
from homePage import homePage                               #Import pages...
from detectPage import detectPage
from databasePage import databasePage
from searchPage import searchPage
from motPage import motPage
from settingsPage import settingsPage
from logoffPage import logoffPage


pages = {                                                   #Define dictionary of page instances
    "homePage": homePage, 
    "detectPage": detectPage,
    "databasePage":databasePage,
    "motPage":motPage,
    "searchPage":searchPage,
    "settingsPage":settingsPage,
    "logoffPage":logoffPage,
}

class ANPR(customtkinter.CTk):                              #Create class

    def __init__(self):                                     #Default procedure init
        customtkinter.CTk.__init__(self)                    #Define the instance to be a customtkinter instance
        self._frame = None                                  #Define variable which stores current page
        self.switchFrame("homePage")                        #Call switchPage fucntion to launch homePage by default

    def switchFrame(self, pageToTransition):                #Define switchFrame procedure, page to change as parameter
        page = pages[pageToTransition]                      #Load page from dictionary
        new_frame = page(master = self)                     #Launch page and pass the parameter of the master root from TkMain 
        if self._frame is not None:                         #If there is a page currently open, destroy it
            self._frame.destroy()
        self._frame = new_frame                             #Define current page variable to new page
        self._frame.pack()                                  #Launch new page

if __name__ == "__main__":
    app = ANPR()                            
    app.mainloop()                                          #Launch app



#####################################################################################################################
import tkinter as tk                                                            #Import Tkinter library
from tkinter import *                                                           

class Page(tk.Canvas):                                                          #Define page to be of canvas type
    prevmast = ()                                                               #Define global variable for master root
                                                                                #passed as a parameter from TkMain
    def __init__(self, master):                                                 #Pass master root and self root in init
        tk.Canvas.__init__(self, master)                                        #Display page as canvas on master root
        self.prevmast = master                                                  #Define global variable as master root
        screenwidth = master.winfo_screenwidth()                                #Fetch screenwidth
        screenheight = master.winfo_screenheight()                              #Fetch screenheight
        master.geometry("{}x{}+{}+{}".format(screenwidth, screenheight,-1,1))   #Set Dimensions
        self.prevmast.title("ANPR - Automatic Number Plate Recognition System") #Set title
        
    def switchDashboard(self, event):                                           #Procedure to switch to dashboard
        self.prevmast.switchFrame("homePage")                                   #Use switchpage procedure from 
                                                                                #TkMain using master root
                                                                                
    def switchDetect(self, event):                                              #Procedure to switch to detect page
        self.prevmast.switchFrame("detectPage")

    def switchDatabase(self, event):                                            #Procedure to switch to database page
        self.prevmast.switchFrame("databasePage")

    def switchSearch(self, event):                                              #Procedure to switch to search page
        self.prevmast.switchFrame("searchPage")                                 

    def switchMOT(self, event):                                                 #Procedure to switch to mot page
        self.prevmast.switchFrame("motPage")                                    
    
    def switchSettings(self, event):                                            #Procedure to switch to settings page
        self.prevmast.switchFrame("settingsPage")                               

    def switchLogoff(self, event):                                              #Procedure to switch to logoff page
        self.prevmast.switchFrame("logoffPage")

if __name__ == "__main__":
    app = settingsPage()
    app.mainloop()

###################################################################################################################################