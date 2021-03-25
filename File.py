import socket
import threading
import random
import os
from datetime import datetime
HEADER = 1024
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def exist(folder):
    if folder in os.listdir():
        return True
    else:
        return False

def log(log):
        print("this message is a log")
        log=log+f"->{datetime.now()}"
        f = open("log.txt","a")
        f.write(log+ "\n")
        f.close()

def write():
    
    while True:
        MSG="INFOO"
        res = client.recv(HEADER).decode(FORMAT)
        typ="info"
        tokens=res.split(",")
        lg=tokens[0][tokens[0].find(":")+1:]
        src=tokens[1][tokens[1].find(":")+1:]
        dst=tokens[2][tokens[2].find(":")+1:]
        msg=tokens[3][tokens[3].find(":")+1:]
        print(msg)
        rand=random.randint(0, 9)
        if rand<=1:
            print("mensaje error"+str(rand))
            typ="erro"
            MSG="ERROR"

        elif rand>2 and rand<=4:
            print("Esta ocupado, intenta mas tarde"+str(rand))
            typ="wait"
            MSG="WAIT" 

        elif (msg.startswith("LOG") or lg.startswith("LOG")):
            log(msg)
        elif msg.startswith("CRE"):
            folder=msg[4:]
            if exist(folder):
                print(f"Folder {folder} already exists")
            else:
                os.system(f'mkdir {folder}')
                print(f"Creating a folder with the name {folder}")
                
        elif msg.startswith("DEL"):
            folder=msg[4:]
            if exist(folder):
                os.system(f'rmdir {folder}')
                print(f"Deleting a folder with the name {folder}")
            else:
                print(f"Folder {folder} does not exist" )

        client.send(f"cmd:{typ},src:FILE,dst:CLIENT,msg:{MSG}".encode(FORMAT))


#iniciamos los hilos
#este primer hilo es para que este pendiente del metodo receive
#receive_thread = threading.Thread(target=receive)
#receive_thread.start()

#Este hilo solo se preocupa de el metodo write
write_thread = threading.Thread(target=write)
write_thread.start()
print("Sending message")
msg="FILE"
client.send(msg.encode(FORMAT))