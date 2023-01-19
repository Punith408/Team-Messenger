import socket,os,threading

HOST = '127.0.0.1'
PORT = 50055

try:
    os.chdir("c:\\chatbox")
except:
    os.mkdir("c:\\chatbox")
    os.chdir("c:\\chatbox")



name = input("enter your name : ")
clientslist=[]
print("""Commands :
%list - to show all people on line
%private - to chat privately with a person
%public - to switch to public
%history - to only your messages
%clear - to clear screen
%help - to display commands""")
    
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'name':
                client.send(name.encode('ascii'))
                clients_num=int(client.recv(1024).decode('ascii'))
                for i in range(0,clients_num):
                    temp=client.recv(1024).decode('ascii')
                    clientslist.append(temp)
                if(len(clientslist)!=0):
                    print(f"Clients connected are {clientslist}")
            else:
                print(message)
                k=message.split()[0]
                l=message.split()[1]
                if k not in clientslist and k !='connected':
                    clientslist.append(k)
                if l =='left' and k in clientslist:
                    clientslist.remove(k)  
                with open("%s.txt"%(name),"a+") as f:
                    f.write(message)
                
        except:
            print("Error Occured")
            client.close()
            break
to='all'

def mod(n):
    global to
    if(n=='private'):
        to=input(f"Choose a name {clientslist}: ")
    elif(n=='public'):
        to='all'
    elif(n=='history'):
        with open("%s.txt"%(name)) as f:
            l=f.readlines()
            print("Only Your last 30 messages :")
            for i in l[-30:]:
                print(i)
    elif(n=='clear'):
        os.system("CLS")

def write():
    while True:
        msg=input(">>>")
        if(msg=='%list'):
            print("people on line",clientslist)
        elif(msg=='%private'):
            mod('private')
        elif(msg=='%public'):
            mod('public')
        elif(msg=='%history'):
            mod('history')
        elif(msg=='%clean'):
            mod('clear')
        else:
            message = '{} to {} : {}'.format(name,to,msg)
            client.send(message.encode('ascii'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
