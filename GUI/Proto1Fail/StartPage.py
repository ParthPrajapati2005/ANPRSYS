import tkinter as tk

class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="This is the start page").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Open page one", command=lambda: master.switch_frame("PageOne")).pack()
        tk.Button(self, text="Open page two", command=lambda: master.switch_frame("PageTwo")).pack()