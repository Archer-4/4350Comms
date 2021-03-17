import tkinter as tk
from tkinter import ttk
import socket
import threading

#USE 136 for running on Odin, 192 for running from Home
playerName = "default"
PORT = 5000
#SERVER = "136.168.201.110"
SERVER = "192.168.1.209"
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)



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
        global playerName 
        playerName = name
        self.controller.show_frame(mainPage)

class mainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.label1 = tk.Label(self, text = "Main Page!")
        self.label1.pack()
        self.textBox = tk.Text(self, width = 20, height = 2, font = "Helvetica 14", padx = 5, pady = 5)
        self.textBox.place(relheight = 0.45, relwidth = 0.5, relx = 0.5, rely = 0.5, y = -10)
        self.textBox.config(state = tk.DISABLED)
        scrollbar = tk.Scrollbar(self.textBox)
        scrollbar.place(relheight = 1, relx = 0.974)
        scrollbar.config(command = self.textBox.yview)

        self.entryMsg = tk.Entry(self, bg = "#ABB2B9", font = "Helvetica 13")
        self.entryMsg.place(relheight = 0.05, relwidth = 0.42, relx = 0.5, rely = 0.95)
        self.entryMsg.focus()

        self.sendBtn = tk.Button(self, text = "Send", font = "helvetica 10 bold", command = lambda: self.sendButton(self.entryMsg.get()))
        self.sendBtn.place(relheight = 0.05, relwidth = 0.08, relx = 0.92,rely = 0.95)
        rcv = threading.Thread(target=self.receiveMsg)
        rcv.start()

    def sendButton(self, msg):
        self.textBox.config(state = tk.DISABLED)
        self.msg = msg
        self.entryMsg.delete(0, tk.END)
        send = threading.Thread(target = self.sendMessage)
        send.start()

    def receiveMsg(self):
        while True:
            try:
                message = client.recv(1024).decode(FORMAT)

                if message == 'NAME':
                    client.send(playerName.encode(FORMAT))
                else:
                    self.textBox.config(state = tk.NORMAL)
                    self.textBox.insert(tk.END, message+"\n\n")
                    self.textBox.config(state = tk.DISABLED)
                    self.textBox.see(tk.END)
            except:
                print("Error")
                client.close()
                break

    def sendMessage(self):
        self.textBox.config(state=tk.DISABLED)
        while True:
            message = (f'{playerName}: {self.msg}')
            client.send(message.encode(FORMAT))
            break


test = gui()
test.geometry("1280x720")
test.mainloop()