import socket
import threading
import random

HEADER = 1024
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
app=0

def startApp(msg):
    global app
    if msg.startswith("AP1"):
        if  app&0b0010==0b0010:
            return "App1 already in use"
        else:
            app=app|0b0010
            return "...App1 started"
    
    if msg.startswith("AP2"):
        if  app&0b0100==0b0100:
            return "App2 already in use"
        else:
            app=app|0b0100
            return "...App2 started"

    if msg.startswith("AP3"):
        if  app&0b1000==0b1000:
            return "App3 already in use"
        else:
            app=app|0b1000
            return "...App3 started"
    

def stopApp(msg):
    global app
    if msg.startswith("ST1"):
        if  app&0b0010==0b0010:
            app=app&0b1101
            return "...App1 stopped"
        else:
            return "App1 hasn't been started"
           
    if msg.startswith("ST2"):
        if  app&0b0100==0b0100:
            app=app&0b1011
            return "...App2 stopped"
        else:
            return "App2 hasn't been started" 

    if msg.startswith("ST3"):
        if  app&0b1000==0b1000:
            
            app=app&0b0111
            return "...App3 stopped"
        else:
            return "App3 hasn't been started"  


def write():
    global app
    while True:
        res = client.recv(HEADER).decode(FORMAT)
        typ="info"
        tokens=res.split(",")
        cmd=tokens[0][4:]
        src=tokens[1][tokens[1].find(":")+1:]
        dst=tokens[2][tokens[2].find(":")+1:]
        msg=tokens[3][tokens[3].find(":")+1:]
        rand=random.randint(0, 9)#
        if cmd =="erro":
            break
        
        elif rand==1:
            print("mensaje error")
            typ="erro"
            MSG="ERROR"

        elif rand==2:
            print("Esta ocupado, intenta mas tarde")
            typ="wait"
            MSG="WAIT"       


        elif msg.startswith("INI"):
            if app&0b0001==0b0001:
                MSG="app module already active"
            else:
                #poner un delay aqui luego
                app= 0b0001
                MSG="APP MODULE STARTED"
        elif msg.startswith("BRK"):
            if app==0b0000:
                MSG="app module hasn't been initiated"
            else:
                MSG= "stopping app module..."
                #delay mas adelante
                app=0
                MSG="...Stopped app module"
                MSG="APP MODULE STOPED"
        elif app&0b0001==0b0001:    
            if msg.startswith("AP"):
                MSG = startApp(msg)
            elif msg.startswith("ST"):
                MSG = stopApp(msg)
        

        else:
        
            MSG="App module hasn't been started"
        print(MSG)
        client.send(f"cmd:{typ},src:APP,dst:CLIENT,msg:{MSG}".encode(FORMAT))




#iniciamos los hilos
#este primer hilo es para que este pendiente del metodo receive
#receive_thread = threading.Thread(target=receive)
#receive_thread.start()

#Este hilo solo se preocupa de el metodo write
write_thread = threading.Thread(target=write)
write_thread.start()
print("Sending message")
msg="APP"
client.send(msg.encode(FORMAT))