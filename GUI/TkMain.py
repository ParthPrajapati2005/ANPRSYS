import tkinter as tk
import customtkinter
from splashScreen import splashScreenInstance
from homePage import homePage
from detectPage import detectPage
from databasePage import databasePage
from searchPage import searchPage
from motPage import motPage
from settingsPage import settingsPage
from logoffPage import logoffPage
from loginPage import loginPage
from login import login
from register import register

pages = {
    "homePage": homePage, 
    "detectPage": detectPage,
    "databasePage":databasePage,
    "motPage":motPage,
    "searchPage":searchPage,
    "settingsPage":settingsPage,
    "logoffPage":logoffPage,
    "loginPage":loginPage,
    "login":login,
    "register":register
}

class ANPR(customtkinter.CTk):
    detection_id = ""
    detectionUser = ""
    detectionPassword = ""
    userFirstName = ""
    userLastName = ""
    userPhoneNumber = ""

    def __init__(self):
        customtkinter.CTk.__init__(self)
        self._frame = None
        self.switchFrame("loginPage")

    def switchFrame(self, pageToTransition):
        cls = pages[pageToTransition]
        new_frame = cls(master = self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

if __name__ == "__main__":
    splashScreenInstance()
    app = ANPR()
    app.mainloop()