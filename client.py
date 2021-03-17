import tkinter as tk
from tkinter import ttk
import socket
import threading


playerName = "default"


class gui(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.iconbitmap(self, default="clientIcon.ico")
        tk.Tk.wm_title(self, "Work In Progress")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        pageList = (loginPage, mainPage)
        for F in (pageList):
            frame = F(container, self)

            self.frames[F] =frame

            frame.grid(row=0, column=0, stick="nsew")

        self.show_frame(loginPage)

    def show_frame(self, pageName):
        frame = self.frames[pageName]
        frame.tkraise()

class loginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        #self.login = ttk.Frame()
        #self.login.pack()
        #self.login.title("Login")
        #self.login.resizable(width = False, height = False)
        #self.login.configure(width = 400, height = 400)

        self.plsLogin = tk.Label(self, text = "Please Enter a Username", justify = tk.CENTER, font = "Helvetica 14 bold")
        #self.plsLogin.place(relheight = 0.15, relx = 0.2, rely = 0.07)
        self.plsLogin.pack(side="top")

        self.usrname = tk.Label(self, text = "Username: ", font = "Helvetica 12")
        #self.usrname.place(relheight = 0.2, relx = 0.1, rely = 0.2)
        self.usrname.pack(side="top")

        self.entryName = tk.Entry(self, font = "Helvetica 14")
        #self.entryName.place(relwidth = 0.4, relheight = 0.12, relx = 0.35, rely = 0.2)
        self.entryName.pack(side="top")
        self.entryName.focus()

        self.go = ttk.Button(self, text = "CONTINUE", command = lambda: self.goAhead(self.entryName.get()))

        #self.go.place(relx = 0.4, rely = 0.55)
        self.go.pack(side="top")

    def goAhead(self, name):
        playerName = name
        self.controller.show_frame(mainPage)

class mainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.label1 = tk.Label(self, text = "Main Page!")
        self.label1.pack()


test = gui()
test.mainloop()