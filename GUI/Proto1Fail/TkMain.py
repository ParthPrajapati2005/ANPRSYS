import tkinter as tk
from customtkinter import *
from splashScreen import *
from homeScreen import homeScreenInstance
from detectPage import detectPage
from databasePage import databasePage

pages = {
    "homePage": homeScreenInstance,
    "detectPage": detectPage,
    "databasePage":databasePage
}

splashScreenInstance()
class ANPR():
    _frame = False
    def __init__(self):
        self.switchFrame("homePage")
    
    def switchFrame(self, transition):
        frameInit = pages[transition]
        run = frameInit(master=self)
        run.destroy()
        self._frame = True
    """
    def switchFrame(self, frameToTransition):
        (self._frame).destroy()
        frameInit = pages[frameToTransition]
        self._frame = frameInit(master=self)
    """

app = ANPR()
#https://stackoverflow.com/questions/67992255/switch-between-two-frames-in-tkinter-in-separates-files