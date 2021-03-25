import socket
import threading
import subprocess
import time
import random

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

clients = {} #KEY:NOMBRE, VALUE:SOCKET

    
    # utilidades del kernel---------------------------------------
 
def cliente(msg):
    print("destino es el cliente")
    client=clients["CLIENT"]
    print(msg)
    client.send(msg.encode(FORMAT))

def log():
    print("aqui deberia ir el contenido del mensaje a guardar")

def archivo(msg):
    client=clients["FILE"]
    print(msg)
    client.send(msg.encode(FORMAT))

def app(msg):
    client=clients["APP"]
    client.send(msg.encode(FORMAT))
    #---------------------------------------------------------------

 
conn=0 #0b001
def kernel(client, addr):
    global conn
    print("--------------")
    while True: 
        time.sleep(random.randint(2, 3))
        #time.sleep(100)

        msg = None
        try:
            msg=client.recv(HEADER).decode(FORMAT)
        except: 
            print("error recieving from client")
            return 1

        if  conn !=0b111:
            
            if  msg.startswith("APP") and not ((conn&0b001)==0b001):
                conn= conn|0b001
                print("app connected")
                clients["APP"]=client

            elif msg.startswith("FILE") and not ((conn&0b010)==0b010):
                conn= conn|0b010
                clients["FILE"]=client
            elif msg.startswith("CLIENT")  and not ((conn&0b010)==0b100):
                conn= conn|0b100                
                clients["CLIENT"]=client
        else:
            tokens=msg.split(",")
            cmd=tokens[0][4:]
            src=tokens[1][4:]
            dst=tokens[2][4:]
            msgg=tokens[3][4:]
            
            log=f"cmd:LOG,src:CLIENT,dst:{dst},{msgg}"
            #
            if src=="CLIENT":
                clients["FILE"].send(log.encode(FORMAT))
                if dst=="CLIENT":
                    cliente(msg)
                elif dst=="FILE":
                    print("esta mierda deberia estar llegando aqui")
                    archivo(msg)
                elif dst=="APP":
                    app(msg)
                elif dst=="KERNEL":
                    print("aqui se llamara un metodo que guarda algo en el log y le notifica al usuario")
            else:
                if cmd=="info":
                    cliente(msg)
                elif cmd=="wait":
                    print("luis no tiene paciencia")
                    cliente(msg)
                else:
                    print("luis la cago")
                    cliente(msg)
 
                


            
        
        
        
        

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
