import socket
import threading
import json
from support import player
from urllib.request import urlopen
import urllib
PORT = 5000
def get_public_ip():
    print("Getting public IP")
    import re
    data = str(urlopen('http://checkip.dyndns.com/').read())
    print(data)
    return re.compile(r'Address: (\d+.\d+.\d+.\d+)').search(data).group(1)

SERVER = socket.gethostbyname(socket.gethostname())
publicIp = get_public_ip()
#ADDRESS = (SERVER, PORT)
ADDRESS = ('', PORT)
FORMAT = "utf-8"
clients, players = [], []
nameReq = json.dumps({'m':"NAME"})
success = json.dumps({'m':"Connection successful!"})
commsLock = threading.Lock()

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
        incoming = incoming.decode(FORMAT)
        print("Incoming is:")
        print(incoming)
        try: 
            data = json.loads(incoming)
        except:
            continue
        if ('m' in data):
            message = data.get('m')
            with commsLock:
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
                with commsLock:
                    client.send(outgo.encode(FORMAT))
        for player in players:
            if player.updateFlag:
                with commsLock:
                    player.update()

def blackJack():
    curPlayers = []



start()
