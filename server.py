import socket
import threading
import json
PORT = 5000

SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"
clients, names = [], []
nameReq = json.dumps({'m':"NAME"})
success = json.dumps({'m':"Connection successful!"})

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)

def start():
    print("Server is working on " + SERVER)

    server.listen(5)

    while True:
        conn, addr = server.accept()
        #conn.send("NAME".encode(FORMAT))
        conn.send(nameReq.encode(FORMAT))
        name = conn.recv(1024).decode(FORMAT)
        names.append(name)
        clients.append(conn)

        print(f'Name is :{name}')

        #broadcastMessage(f'{name} has joined the chat!'.encode(FORMAT))
        broadcastMessage(f'{name} has joined the chat!')
        #conn.send('Connection successful!'.encode(FORMAT))
        conn.send(success.encode(FORMAT))

        thread = threading.Thread(target = handle, args = (conn, addr))
        thread.start()

        print(f'active connections {threading.activeCount()-1}')

def handle(conn, addr):
    print(f'new connection {addr}')

    while True:
        incoming = conn.recv(1024)
        if not incoming:
            print(f'{addr} disconnected')
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

start()
