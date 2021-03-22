import socket
import threading
import json
from support import player
PORT = 5000

SERVER = socket.gethostbyname(socket.gethostname())
#ADDRESS = (SERVER, PORT)
ADDRESS = ('', PORT)
FORMAT = "utf-8"
clients, players = [], []
nameReq = json.dumps({'m':"NAME"})
success = json.dumps({'m':"Connection successful!"})

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)

def start():
    print("Server is working on " + SERVER)

    server.listen(5)
    updateThread = threading.Thread(target = updatePlayers, args = ())
    updateThread.start()

    while True:
        conn, addr = server.accept()
        #conn.send("NAME".encode(FORMAT))
        conn.send(nameReq.encode(FORMAT))
        name = conn.recv(1024).decode(FORMAT)
        players.append(player(name, conn))
        clients.append(conn)

        print(f'Name is :{name}')

        #broadcastMessage(f'{name} has joined the chat!'.encode(FORMAT))
        broadcastMessage(f'{name} has joined the chat!')
        #conn.send('Connection successful!'.encode(FORMAT))
        conn.send(success.encode(FORMAT))

        thread = threading.Thread(target = handle, args = (conn, addr))
        thread.start()


        print(f'active connections {threading.activeCount()-2}')

def handle(conn, addr):
    print(f'new connection {addr}')

    while True:
        incoming = conn.recv(1024)
        if not incoming:
            print(f'{addr} disconnected')
            lostPos = clients.index(conn)
            players.pop(lostPos)
            clients.remove(conn)
            break;
        data = json.loads(incoming)
        if ('m' in data):
            message = data.get('m')
            broadcastMessage(message)

    conn.close()

def broadcastMessage(message):
    data = json.dumps({'m': message})
    for client in clients:
        #client.send(message)
        client.send(data.encode(FORMAT))

def updatePlayers():
    playerCount = 0
    while True:
        if (playerCount != len(players)):
            playerCount = len(players)
            outgo = json.dumps({'pCount':playerCount})
            for client in clients:
                client.send(outgo.encode(FORMAT))

start()
