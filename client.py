import tkinter as tk
from tkinter import ttk
import json
import socket
import threading

#USE 136 for running on Odin, 192 for running from Home
playerName = "default"
PORT = 5000
#SERVER = "136.168.201.110"
SERVER = "192.168.1.209"
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"
CONNECTED = False

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#client.connect(ADDRESS)



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

        self.plsLogin = tk.Label(self, text = "Please Enter a Username", justify = tk.CENTER, font = "Helvetica 14 bold")
        self.plsLogin.pack(side="top")

        self.usrname = tk.Label(self, text = "Username: ", font = "Helvetica 12")
        self.usrname.pack(side="top")

        self.entryName = tk.Entry(self, font = "Helvetica 14")
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

        #Grid options
        self.grid_columnconfigure(0, weight = 3)
        self.grid_columnconfigure(1, weight = 1)
        self.grid_columnconfigure(2, weight = 1)
        self.grid_rowconfigure(0, minsize = 490)

        #Frame for server connect widget
        self.connectF = tk.Frame(self)
        self.connectF.grid(row = 0, column = 2, sticky = 'n')
        loginLabel = tk.Label(self.connectF, text = "Please Connect to Server")
        loginLabel.grid(row = 0, column = 0, columnspan = 2)
        ipLabel = tk.Label(self.connectF, text="Server IP:")
        ipLabel.grid(row = 1, column = 0)
        entIp = tk.Entry(self.connectF, font = "Helvetica 13")
        entIp.grid(row = 1, column = 1)
        self.connectBtn = tk.Button(self.connectF, text = "Connect", font = "Helvetica 10 bold", command = lambda: self.connect(entIp.get()))
        self.connectBtn.grid(row = 1, column = 2)

        #Frame for information display
        self.connectedF = tk.Frame(self, height = self.connectF.winfo_height(), width = self.connectF.winfo_width())
        self.connectLabel = tk.Label(self.connectedF, text = "CONNECTED", font = "Helvetica 12 bold")
        self.connectLabel.grid(row = 0, column = 0, columnspan = 2)
        quitBtn = tk.Button(self.connectedF, text="Disconnect", font = "Helvetica 10 bold", command = lambda: self.quit())
        quitBtn.grid(row = 0, column = 2)
        self.playerCount = tk.Label(self.connectedF, text = "Connected Players: None", font = "Helvetica 12 bold")
        self.playerCount.grid(row = 1, column = 0, columnspan = 2)
        self.playerBalance = tk.Label(self.connectedF, text = "Your Balance: ", font = "Helvetica 12 bold")
        self.playerBalance.grid(row = 2, column = 0, columnspan = 2)

        #Chat Frame
        self.chatFrame = tk.Frame(self)
        self.chatFrame.grid(row = 3, column = 2)
        self.textBox = tk.Text(self.chatFrame, width = 60, height = 10, font = "Helvetica 12", padx = 5, pady = 5, wrap = tk.WORD)
        self.textBox.grid(row = 0, column = 0, rowspan = 100, columnspan = 5, sticky = 'ne')
        self.textBox.config(state = tk.DISABLED)
        scrollbar = tk.Scrollbar(self.textBox)
        scrollbar.place(relheight = 1.0, relx = 0.990)
        scrollbar.config(command = self.textBox.yview)
        self.entryMsg = tk.Entry(self.chatFrame, bg = "#ABB2B9", font = "Helvetica 13", width = 55)
        self.entryMsg.grid(row = 111, column = 0, columnspan = 4)
        self.entryMsg.focus()
        self.sendBtn = tk.Button(self.chatFrame, text = "Send", font = "helvetica 10 bold", command = lambda: self.sendButton(self.entryMsg.get()))
        self.sendBtn.grid(row = 111, column = 4)

    def connect(self, ip):
        global SERVER
        global CONNECTED
        global client
        SERVER = ip
        port = 5000
        address = (SERVER, port)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(address)
        CONNECTED = True
        rcv = threading.Thread(target = self.receiveMsg)
        rcv.start()
        self.connectF.grid_forget()
        #self.grid_rowconfigure(1, minsize = 420)
        self.connectedF.grid(row = 0, column = 2, sticky = 'n')
        self.connectBtn.config(state = tk.DISABLED)
        connectLab = "Connected to: " + ip
        self.connectLabel.configure(text = connectLab)


    def sendButton(self, msg):
        self.textBox.config(state = tk.DISABLED)
        self.msg = msg
        self.entryMsg.delete(0, tk.END)
        send = threading.Thread(target = self.sendMessage)
        send.start()
        self.sendMessage

    def receiveMsg(self):
        while CONNECTED:
            try:
                incoming = client.recv(1024).decode(FORMAT)
                data = json.loads(incoming)
                if ('m' in data):
                    message = data.get('m')
                    if message == 'NAME':
                        client.send(playerName.encode(FORMAT))
                    else:
                        self.textBox.config(state = tk.NORMAL)
                        self.textBox.insert(tk.END, message+"\n\n")
                        self.textBox.config(state = tk.DISABLED)
                        self.textBox.see(tk.END)
                if ('pCount' in data):
                    count = data.get('pCount')
                    string = "Connected Players: " + str(count)
                    self.playerCount.configure(text = string)
                    print(string)
                del data
                del incoming
            except Exception as e:
                print("Error from receiveMsg")
                print(e)
                client.close()
                break

    def sendMessage(self):
        self.textBox.config(state=tk.DISABLED)
        while CONNECTED:
            message = (f'{playerName}: {self.msg}')
            data = json.dumps({'m':message})
            #client.send(message.encode(FORMAT))
            client.send(data.encode(FORMAT))
            break

    def quit(self):
        global CONNECTED
        if CONNECTED:
            client.shutdown(socket.SHUT_RDWR)
            client.close()
            CONNECTED = False
            self.connectBtn.config(state = tk.NORMAL)
            self.connectF.grid(row = 0, column = 2, sticky = 'n')
            self.connectedF.grid_forget()
            #self.grid_rowconfigure(1, minsize = 450)



test = gui()
test.geometry("1280x720")
test.mainloop()