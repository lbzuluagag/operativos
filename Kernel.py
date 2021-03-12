import socket
import threading
import subprocess


# metodo para enviar mensaje a todos los usuarios conectados
# pendiente mas adelante poner que reciba a que sala debe hacer el broadcast
def broadcast(msg):
    for client in CLIENTS:
        client.send(msg)



def handle(client,addr):
    while True:
        #luego voy a probar poner aqui
        #un if donde dependiendo de que llegue se hace un menu
        try:
            msg=client.recv(HEADER)
            broadcast(msg.encode(FORMAT))
        except:
            index = CLIENTS.index(client)
            CLIENTS.remove(client)
            client.close()
            nickname = NICKNAMES[index]
            broadcast("{} left the chat!".format(nickname).encode(FORMAT))
            NICKNAMES.remove(nickname)
            break



        # NETWORKING SETUP-------------------------------------------
        #msg length in bytes
HEADER = 1024
PORT = 5050
#get IP
SERVER = socket.gethostbyname(socket.gethostname()) 
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
# ----------------------------------------------------------
VERBS = {"ER", "OK"}

clients = {}

    
    # utilidades del servidor---------------------------------------
 

    #---------------------------------------------------------------

 
conn=0
def kernel(client, addr):
    global conn
    print("--------------")
    while True: 
        msg = None
        try:
            msg=client.recv(HEADER).decode(FORMAT)
        except: 
            print("error recieving from client")
            return 1

        if  conn !=0b111:
            
            if  msg.startswith("APP") and not ((conn&0b001)==0b001):
                conn= conn|0b001
                print("client connected")
                clients["app"]=client

            elif msg.startswith("FILE") and not ((conn&0b010)==0b010):
                conn= conn|0b010
                clients["file"]=client
            elif msg.startswith("CLIENT")  and not ((conn&0b010)==0b100):
                conn= conn|0b100                
                clients["client"]=client

            print(conn)
        
        
        
        

def start_kernel():
    server.listen()
    subprocess.call("start.bat")
    print(f"[LISTENING] Server is listening on {SERVER}")

    while True:
        conn, addr = server.accept()
        print(f"Connected with {str(addr)}")
        thread = threading.Thread(target=kernel, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count }")


#inicia el servidor
print("Starting server...")

start_kernel()