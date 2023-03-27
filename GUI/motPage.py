import tkinter as tk
from tkinter import *
from tkinter import ttk
import os
import json
from PIL import Image, ImageTk
import customtkinter
import requests
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from matplotlib.figure import Figure

class motPage(tk.Canvas):
    prevmast = ()
    workspace = ()

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
                          'mot-icon-blue':os.path.join('GUI','Icons', 'mot-icon-blue-48.png'),
                          'mot-icon':os.path.join('GUI','Icons', 'mot-icon-48.png'),
                          'settings-icon':os.path.join('GUI','Icons', 'settings-icon-48.png'),
                          'logoff-icon':os.path.join('GUI','Icons', 'logoff-icon-48.png'),
                          'empty-icon':os.path.join('GUI','Icons', 'empty-icon-48.png')}
        
        screen.icon_renders = {'dashboard-icon':ImageTk.PhotoImage(image=Image.open(screen.icon_filePaths['dashboard-icon'])),
                        'detect-icon':ImageTk.PhotoImage(master=screen, image=Image.open(screen.icon_filePaths['detect-icon'])),
                        'database-icon':ImageTk.PhotoImage(master=screen, image=Image.open(screen.icon_filePaths['database-icon'])),
                        'search-icon':ImageTk.PhotoImage(master=screen, image=Image.open(screen.icon_filePaths['search-icon'])),
                        'mot-icon':ImageTk.PhotoImage(master=screen, image=Image.open(screen.icon_filePaths['mot-icon-blue'])),
                        'settings-icon':ImageTk.PhotoImage(master=screen, image=Image.open(screen.icon_filePaths['settings-icon'])),
                        'logoff-icon':ImageTk.PhotoImage(master=screen, image=Image.open(screen.icon_filePaths['logoff-icon'])),
                        'empty-icon':ImageTk.PhotoImage(master=screen, image=Image.open(screen.icon_filePaths['empty-icon']))}

        screen.create_rectangle(0,0,100,screenheight, fill="#1F2940", outline="")

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
    
        self.workspace = Canvas(screen, height=screenheight, width=screenwidth-100, highlightthickness=False, bg="#141B2D")
        self.workspace.place(x=100, y=100)
        screen.create_text(150, 60, fill="white", text="MOT & MILEAGE", font=("Azonix", 40), anchor='w')

        self.build()
    
    def build(self):    
        self.workspace.create_text(450,100,fill="white",text="Enter the registration plate of the vehicle you wish to search below : ", font=("Modern_Mono",25),anchor="w", tag="workspaceItem")
        self.workspace.create_text(450,700,fill="green",text="Note : Private/Personalised plates also work using this function! ", font=("Modern_Mono",25), anchor="w", tag="workspaceItem")
        self.inputWorkspace = Canvas(self.workspace, height=145, width=640, bg="#f8bc04") ##f8bc04 yellow colour shade
        self.inputWorkspace.pack()
        self.workspace.create_window(300,300,window=self.inputWorkspace)
        self.inputWorkspace.place(x=615, y=228)
        self.workspace.regTemplatePath = os.path.join("GUI", "Icons", "reg-template.png")
        self.workspace.regTemplateRender = ImageTk.PhotoImage(master=self.workspace, image=Image.open(self.workspace.regTemplatePath))

        self.workspace.create_image(900, 300, image=self.workspace.regTemplateRender, tag="workspaceItem")

        def capitalise(event):
            var.set(var.get().upper())
        
        var = StringVar()
        self.inputEntry = Entry(self.inputWorkspace, font=("Charles Wright", 76), bg="#f8bc04", fg="black", width=10, highlightthickness=False, highlightcolor="#f8bc04", borderwidth=0, justify=CENTER, textvariable=var)
        self.inputEntry.pack()
        self.inputEntry.bind("<KeyRelease>", capitalise)

        def search():
            vehicleData, status = self.vehicleLookup()

            if status == 1:
                self.displayDetails(vehicleData)

            if status == 2:
                self.workspace.delete("error")
                self.workspace.create_text(700,450,text="The Number Plate is invalid!", tag="error", fill="red", font=("Modern_Mono",25), anchor="w")

        self.submitButton = customtkinter.CTkButton(self.workspace, text_font=("Modern_Mono", 25), text="Submit", width=200, height=100, command=search)
        self.submitButton.pack()
        self.submitButton.place(x=800, y=500)

    def displayDetails(self, vehicleData):
        self.workspace.delete("workspaceItem")
        for widgets in self.workspace.winfo_children():
            widgets.destroy()
        
        com = Label(self.workspace, text="LOOKUP COMPLETE!", fg="lime", bg="#141B2D", font=("Azonix", 40), anchor="center")
        com.pack()

        detailWorkspace = Canvas(self.workspace, height=100, width=self.winfo_screenwidth()-100, bg="#141B2D", highlightthickness=False)
        detailWorkspace.pack()

        detailWorkspace.create_text(900,75,text=("REGISTRATION : "+vehicleData["registration"]+"    MAKE : "+vehicleData["make"]+"    MODEL : "+vehicleData["model"]+"   COLOUR : "+vehicleData["primaryColour"]), font=("Modern_Mono", 25), fill="white")

        treeWorkspace = Canvas(self.workspace, height=750, width=self.winfo_screenwidth()-100, bg="#141B2D", highlightthickness=False)
        treeWorkspace.pack()

        def reset():
            self.prevmast.switchFrame("motPage")
        
        
        self.tree = ttk.Treeview(treeWorkspace, height=10)  #Declare tree object and set max rows to 12
        self.tree['show'] = 'headings'                         #Configure to show the headings of the table

        #Define tree styles
        style = ttk.Style(treeWorkspace)
        style.theme_use("default")
        style.configure("Treeview.Heading", font=("Modern_Mono", 20, "bold"), rowheight=80)
        style.configure(".", font=("Modern_Mono", 17,))
        style.configure("Treeview.Heading", fieldbackground="#141B2D", background="#141B2D", foreground="white", borderwidth=0)
        style.configure("Treeview", fieldbackground="#141B2D", background="#141B2D", foreground="white", rowheight=60, borderwidth=0)
        style.configure("arrowless.Horizontal.TScrollbar", background="white",  arrowcolor="#141B2D", troughcolor = "#141B2D", borderwidth=0)
        style.configure("arrowless.Vertical.TScrollbar", background="white", arrowcolor="#141B2D", troughcolor = "#141B2D", borderwidth=0)

        self.tree["columns"] = (
                    "dateOfMOT",
                    "testResult",
                    "motExpiry",
                    "mileage",
                    "motTestNumber",
                    "advisories"
                    )

        columnWidth = 280
        self.tree.column("dateOfMOT", width=columnWidth, minwidth=250, anchor=CENTER)
        self.tree.column("testResult", width=columnWidth, minwidth=250, anchor=CENTER)
        self.tree.column("motExpiry", width=columnWidth, minwidth=250, anchor=CENTER)
        self.tree.column("mileage", width=columnWidth, minwidth=250, anchor=CENTER)
        self.tree.column("motTestNumber", width=columnWidth, minwidth=250, anchor=CENTER)
        self.tree.column("advisories", width=columnWidth, minwidth=250, anchor=CENTER)

        self.tree.heading("dateOfMOT", text="Date & Time of MOT", anchor=CENTER)
        self.tree.heading("testResult", text="Test Result", anchor=CENTER)
        self.tree.heading("motExpiry", text="MOT Expiry", anchor=CENTER)
        self.tree.heading("mileage", text="Mileage", anchor=CENTER)
        self.tree.heading("motTestNumber", text="MOT Test Number", anchor=CENTER)
        self.tree.heading("advisories", text="Any Advisories?", anchor=CENTER)

        self.tree.tag_configure('pass', foreground="lime")
        self.tree.tag_configure('advisories', foreground='yellow')
        self.tree.tag_configure('fail', foreground='red')

        def OnDoubleClick(event):
            item = self.tree.selection()[0]
            selItemValues = self.tree.item(item, "values")
            selTestNumber = selItemValues[4]

            treeWorkspace.pack_forget()
            advisoryWorkspace = Canvas(self.workspace, height=750, width=750, bg="#141B2D", highlightthickness=False)
            advisoryWorkspace.pack(side="left")

            advisoryTree = ttk.Treeview(advisoryWorkspace, height=9)
            advisoryTree['show'] = 'headings'

            advisoryStyle = ttk.Style(advisoryWorkspace)
            advisoryStyle.theme_use("default")
            advisoryStyle.configure("Treeview.Heading", font=("Modern_Mono", 20, "bold"), rowheight=80)
            advisoryStyle.configure(".", font=("Modern_Mono", 17,))
            advisoryStyle.configure("Treeview.Heading", fieldbackground="#141B2D", background="#141B2D", foreground="white", borderwidth=0)
            advisoryStyle.configure("Treeview", fieldbackground="#141B2D", background="#141B2D", foreground="white", rowheight=60, borderwidth=0)
            advisoryStyle.configure("arrowless.Horizontal.TScrollbar", background="white",  arrowcolor="#141B2D", troughcolor = "#141B2D", borderwidth=0)
            advisoryStyle.configure("arrowless.Vertical.TScrollbar", background="white", arrowcolor="#141B2D", troughcolor = "#141B2D", borderwidth=0)

            advisoryTree["columns"] = ("advisoryNote", "advisoryType")

            advisoryTree.column("advisoryNote", width=550, minwidth=750, anchor=CENTER)
            advisoryTree.column("advisoryType", width=200, minwidth=200, anchor=CENTER)

            advisoryTree.heading("advisoryNote", text="Advisory Note", anchor=CENTER)
            advisoryTree.heading("advisoryType", text="Advisory Type", anchor=CENTER)

            mileages = []
            dates = []

            for x in vehicleData["motTests"]:
                if x["motTestNumber"] == selTestNumber:
                    found = x
                    advisoryDetails = found["rfrAndComments"]
                mileages.append(x["odometerValue"])
                dates.append(x["completedDate"])

            j = 0
            for y in advisoryDetails:
                advisoryTree.insert("", j, text="", values=(y["text"], y["type"]))
                j = j + 1

            advisoryTree_scrolly = ttk.Scrollbar(advisoryWorkspace, orient=tk.VERTICAL, command=advisoryTree.yview, style='arrowless.Vertical.TScrollbar')
            advisoryTree_scrolly.pack(side=tk.RIGHT, fill=tk.Y)

            advisoryTree_scrollx = ttk.Scrollbar(advisoryWorkspace, orient=tk.HORIZONTAL, command=advisoryTree.xview, style='arrowless.Horizontal.TScrollbar')
            advisoryTree_scrollx.pack(side=tk.BOTTOM, fill=tk.X)

            advisoryTree.config(yscrollcommand=advisoryTree_scrolly.set)
            advisoryTree.config(xscrollcommand=advisoryTree_scrollx.set)

            advisoryTree.pack(padx=40, pady=50, fill=BOTH, expand=1)

            graphWorkspace = Canvas(self.workspace, height=750, width=self.winfo_screenwidth()-900, bg="#141B2D", highlightthickness=False)
            graphWorkspace.pack()

            newDates = []
            for x in dates:
                newDates.append(x[0:4])

            mileages.sort()
            newDates.sort()

            x_axis = newDates
            y_axis = mileages

            fig = Figure(figsize=(10, 7), dpi=100)
            fig.set_facecolor("#141B2D")
            graph = fig.add_subplot(111)
            graph.plot(x_axis,y_axis, marker="o", color="white")
            graph.set_title("Mileage Graph", fontsize=22).set_color("white")
            graph.set_xlabel("Time", fontsize=18)
            graph.set_ylabel("Mileage", fontsize=18)
            graph.set_facecolor("#141B2D")
            graph.xaxis.label.set_color("white")
            graph.yaxis.label.set_color("white")
            graph.spines['left'].set_color("white")
            graph.spines['bottom'].set_color("white")
            graph.spines['top'].set_color("#141B2D")
            graph.spines['right'].set_color("#141B2D")
            graph.tick_params(axis='x', colors='white')
            graph.tick_params(axis='y', colors='white')

            canvas = FigureCanvasTkAgg(fig, master=graphWorkspace)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1, pady=50)
            

        i = 0
        myTag = ''

        for x in vehicleData["motTests"]:
            motDate = x["completedDate"]

            if x["testResult"] == "PASSED":
                motExpiry =  x["expiryDate"]
            else:
                motExpiry = "N/A"

            motTestNumber = x["motTestNumber"]
            mileage = x["odometerValue"]
            testResult = x["testResult"]
            
            if len(x["rfrAndComments"]) != 0:
                advisories = "YES"
            else:
                advisories = "NO"
            
            if testResult == "PASSED" and advisories == "YES":
                myTag = 'advisories'
            elif testResult == "PASSED" and advisories == "NO":
                myTag = 'pass'
            elif testResult == "FAILED":
                myTag = 'fail'

            self.tree.insert("", i, text="", values=(motDate,testResult,motExpiry,mileage,motTestNumber,advisories), tags=(myTag))
            self.tree.bind("<Double-1>", OnDoubleClick)
            i = i + 1

        tree_scrolly = ttk.Scrollbar(treeWorkspace, orient=tk.VERTICAL, command=self.tree.yview, style='arrowless.Vertical.TScrollbar')
        tree_scrolly.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.pack(padx=40, pady=50, fill=BOTH, expand=1)
        self.tree.config(yscrollcommand=tree_scrolly.set)

        buttonWorkspace = Frame(self.workspace, height=75, width=200, highlightthickness=False, bg="#141B2D")
        buttonWorkspace.pack()
        buttonWorkspace.place(x=1500,y=0)

        resetButton = customtkinter.CTkButton(buttonWorkspace, text="SEARCH AGAIN", height=75, width=200, bg="#141B2D", command=reset)
        resetButton.pack()

    def vehicleLookup(self):
        finalPlate = self.inputEntry.get()
        body = {"registrationPlate" : str(finalPlate)}
        status = 0
        vehicleData = {}

        try:
            req3 = requests.post('https://vehicle-api-parth13075.vercel.app/getMOTDetails', json=body)
            vehicleData = json.loads(req3.text)
            status = 1
        except:
            status = 2

        return vehicleData, status

    def switchDashboard(self, event):
        self.prevmast.switchFrame("homePage")

    def switchDetect(self, event):
        self.prevmast.switchFrame("detectPage")

    def switchDatabase(self, event):
        self.prevmast.switchFrame("databasePage")

    def switchSearch(self, event):
        self.prevmast.switchFrame("searchPage")

    def switchMOT(self, event):
        pass
    
    def switchSettings(self, event):
        self.prevmast.switchFrame("settingsPage")

    def switchLogoff(self, event):
        self.prevmast.switchFrame("logoffPage")

if __name__ == "__main__":
    app = motPage()
    app.mainloop()