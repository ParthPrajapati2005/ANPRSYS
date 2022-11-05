from tkinter import *
import os

class HomeGUI:
    def __init__(self):
        root = Tk()
        thisWidth = 1800 # Define Width
        thisHeight = 900 # Define Height
        menuBar = Menu(root) # Define Menu Template
        fileMenu = Menu(menuBar, tearoff=0) # Define 'File' menu

        root.geometry(str(thisWidth)+"x"+str(thisHeight)) # Set Window dimensions
        self.setWindowIcon
        root.mainloop()

    def createDropdown():
        pass

myWindow = HomeGUI()