import socket
import threading
import os

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
        log=msg[4:]
        f = open("log.txt","a")
        f.write(log)

def write():
    print("Sending message")
    msg="FILE"
    client.send(msg.encode(FORMAT))
    while True:
        
        res = client.recv(HEADER).decode(FORMAT)
        
        tokens=res.split(",")
        src=tokens[1][tokens[1].find(":")+1:]
        dst=tokens[2][tokens[2].find(":")+1:]
        msg=tokens[3][tokens[3].find(":")+1:]
        print(msg)
        if msg.startswith("LOG:"):
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




#iniciamos los hilos
#este primer hilo es para que este pendiente del metodo receive
#receive_thread = threading.Thread(target=receive)
#receive_thread.start()

#Este hilo solo se preocupa de el metodo write
write_thread = threading.Thread(target=write)
write_thread.start()
