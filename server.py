import socket 
import select 
import sys 
import thread 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
 
if len(sys.argv) != 3: 
    print ("Correct usage: script, IP address, port number")
    exit() 
 
IP_address = str(sys.argv[1]) 
Port = int(sys.argv[2]) 
server.bind((IP_address, Port)) 
server.listen(100) 
  
list_of_clients = [] 

def getFile(conn):
    with open('received_file', 'wb') as f:
        print ('file opened')
        while True:
            print('receiving data...')
            data = conn.recv(1024)
            if data[0:12]=="done sending":
                break
            print(data[0:6])
            print('data=%s', (data))
            
            # write data to a file
            f.write(data)

    f.close()
    print('Successfully get the file')


def sendFile(conn):
    filename='mytext.txt'
    f = open(filename,'rb')
    l = f.read(1024)
    while (l):
       conn.send(l)
       print('Sent ',repr(l))
       l = f.read(1024)
    f.close()

    print('Done sending')


def clientthread(conn, addr): 
    conn.send("Welcome to this chatroom!") 
    
    while True: 
            try: 
                message = conn.recv(2048) 
                if message[0:9] == "send file": 
                    broadcastFile("received_file",conn)
                    getFile(conn)
                elif message:
                    print ("<" + addr[0] + "> " + message)
                    message_to_send = "<" + addr[0] + "> " + message 
                    broadcast(message_to_send, conn) 
                else: 
                    remove(conn) 
  
            except: 
                continue
  
def broadcast(message, connection): 
    for clients in list_of_clients: 
        if clients!=connection: 
            try: 
                clients.send(message) 
            except: 
                clients.close() 
                remove(clients) 

def broadcastFile(filename,conn):
    for clients in list_of_clients: 
        if clients!=conn: 
            try: 
                clients.send(filename)
            except: 
                clients.close() 
                remove(clients) 

def remove(connection): 
    if connection in list_of_clients: 
        list_of_clients.remove(connection) 
  
while True: 
    conn, addr = server.accept() 
    list_of_clients.append(conn) 
    print (addr[0] + " connected")
    thread.start_new_thread(clientthread,(conn,addr))     
  
conn.close() 
server.close() 