import tkinter as tk
from tkinter import *
import os
from PIL import Image, ImageTk
from tkinter import font as tkFont


class loginPage(tk.Canvas):
    prevmast = ()

    def __init__(self, master):
        tk.Canvas.__init__(self, master)
        self.prevmast = master
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        width = 500
        height = 300
        x = (screenwidth/2)-(width/2)
        y = (screenheight/2)-(height/2)
        master.geometry('%dx%d+%d+%d' % (width, height, x, y))
        self.prevmast.title("ANPR - Automatic Number Plate Recognition System") 

        screen = Canvas(self, highlightthickness=False, width=screenwidth, height=screenheight, bg="#141B2D")
        screen.pack()

        screen.create_text(30,30, text="Welcome to ANPR System", font=("Azonix", 20), fill="white", anchor="nw")

        screen.loginButtonFilePath = os.path.join('GUI','Icons', 'login-icon-100.png')
        screen.registerButtonFilePath = os.path.join('GUI','Icons', 'register-icon-100.png')

        screen.loginButtonRender = ImageTk.PhotoImage(master=screen,image=Image.open(screen.loginButtonFilePath))
        screen.registerButtonRender = ImageTk.PhotoImage(master = screen, image=Image.open(screen.registerButtonFilePath))

        loginButton = screen.create_image(150,150,image=screen.loginButtonRender)
        registerButton = screen.create_image(350,150, image=screen.registerButtonRender)
        screen.tag_bind(loginButton, "<Button-1>", self.switchLogin)
        screen.tag_bind(registerButton, "<Button-1>", self.switchRegister)

        screen.create_text(147,230, text="Login", font=("Modern_Mono", 18), fill="white", anchor="center")
        screen.create_text(347,230, text="Register", font=("Modern_Mono", 18), fill="white", anchor="center")

    def switchLogin(self, event):
        self.prevmast.switchFrame("login")

    def switchRegister(self, event):
        self.prevmast.switchFrame("register")

if __name__ == "__main__":
    app = loginPage()
    app.mainloop()