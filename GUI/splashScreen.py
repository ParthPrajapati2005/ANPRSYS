from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import time
import customtkinter

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("dark-blue")

class splashScreenInstance():                                                                                             #Define splashScreen window
    splash = Tk()
                                                                                                                  #Destroy splash screen
    def __init__(self):                                                                                           #Initialise function
        splashHeight = 210                                                                                        #Define splash screen height
        splashWidth = 350                                                                                         #Define splash screen width
        screenHeight = self.splash.winfo_screenheight()                                                           #Get screen height
        screenWidth = self.splash.winfo_screenwidth()                                                             #Get screen width
        x_center = (screenWidth//2)-(splashWidth//2)                                                              #Get center x coordinate
        y_center = (screenHeight//2)-(splashHeight//2)                                                            #Get center y coordinate
        self.splash.geometry('{}x{}+{}+{}'.format(splashWidth, splashHeight, x_center, y_center))                 #Set splash screen position

        load = Image.open('C:\\Users\\parth\\Documents\\ANPR\\GUI\\splash-background.jpg')
        render = ImageTk.PhotoImage(load)                                                                         #Set splash screen background colour

        canvas = Canvas(self.splash, borderwidth=0, width=350, height=210, highlightthickness=0)
        canvas.create_image(-1,-1, image=render)
        canvas.create_text(170,100, text="ANPR", font=("Good Times Rg", 60), fill='white')
        canvas.pack()

        self.splash.overrideredirect(True) 
        self.splash.after(2000,self.destroySplash)  
        self.splash.mainloop()                                                              
                                                                                                                 

    def destroySplash(self):
        self.splash.destroy()
        self.splash.quit()
    

#https://stackoverflow.com/questions/53021603/how-to-make-a-tkinter-canvas-background-transparent