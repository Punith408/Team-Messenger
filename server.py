import socket,threading,os

HOST = '127.0.0.1'
PORT = 50055

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
clientslist = []
nameslist = []
l=[]
ls=[]
j=0


try:
    os.chdir("c:\\chatbox")
    os.chdir("c:\\chatbox\\admin")
except:
    try:
        os.mkdir("c:\\chatbox")
    except:
        pass
    os.mkdir("c:\\chatbox\\admin")
    os.chdir("c:\\chatbox")
    os.chdir("c:\\chatbox\\admin")
    
def broadcast(message):
    to = message.decode('ascii').split()[2]

    if (to == 'all' or to == 'the' or to == '!'):
        for client in clientslist:
            client.send(message)
        with open("Serverchat.txt", "a+") as f:
            f.write(str(message.decode('ascii') + "\n"))
        f.close()
    else:
        index = nameslist.index(to)
        clientslist[index].send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clientslist.index(client)
            clientslist.remove(client)
            client.close()
            name = nameslist[index]
            broadcast('{} left !'.format(name).encode('ascii'))
            print(name, "left !")
            nameslist.remove(name)
            break

def search():
    try:
        with open("Userlist.txt","r") as n:
            global l
            l=n.readlines()
            print(f"ALL NAMES :{l}")
    except:
        print("File doesn't exist")


def receive():
    while True:
        client, address = server.accept()
        print(f"connected with {address}")
        client.send('name'.encode('ascii'))
        name = client.recv(1024).decode('ascii')
        client.send(str(len(nameslist)).encode('ascii'))
        for i in nameslist:
            client.send(i.encode('ascii'))
        nameslist.append(name)
        clientslist.append(client)
        search()
        with open("Userlist.txt","a+") as n:
            if (name+'\n') not in l:
                n.write(name+'\n')
        print(f"name of the client is {name}")
        broadcast(f"{name} joined the chat".encode('ascii'))

        with open("Serverchat.txt","r+") as f1:
            ls=f1.readlines()
            j=0
            f1.seek(0)
            for i in ls[0:]:
                if (name+" joined the chat\n") == i:
                    break
                j+=1
            for i in ls[j:]:
                if (name+'\n') in l:
                    client.send(i.encode('ascii'))
        f1.close()
        client.send(f"connected to the server\n".encode('ascii'))

        print(f"All Connections {nameslist}")

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("server is listening...")
receive()
