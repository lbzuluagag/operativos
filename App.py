import socket
import threading


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
            print("App1 already in use")
        else:
            print("Starting app1...")
            app=app|0b0010
            print("...App1 started")
    
    if msg.startswith("AP2"):
        if  app&0b0100==0b0100:
            print("App2 already in use")
        else:
            print("Starting app2...")
            app=app|0b0100
            print("...App2 started")

    if msg.startswith("AP3"):
        if  app&0b1000==0b1000:
            print("App3 already in use")
        else:
            print("Starting app3...")
            app=app|0b1000
            print("...App3 started")
    

def stopApp(msg):
    global app
    if msg.startswith("ST1"):
        if  app&0b0010==0b0010:
            print("Stopping app1...")
            app=app&0b1101
            print("...App1 stopped")
        else:
            print("App1 hasn't been started")
           
    if msg.startswith("ST2"):
        if  app&0b0100==0b0100:
            print("Stopping app2...")
            app=app&0b1011
            print("...App2 stopped")
        else:
            print("App2 hasn't been started")  

    if msg.startswith("ST3"):
        if  app&0b1000==0b1000:
            print("Stopping app3...")
            app=app&0b0111
            print("...App3 stopped")
        else:
            print("App3 hasn't been started")  


def write():
    global app
    while True:
        res = client.recv(HEADER).decode(FORMAT)
        
        tokens=res.split(",")
        src=tokens[1][tokens[1].find(":")+1:]
        dst=tokens[2][tokens[2].find(":")+1:]
        msg=tokens[3][tokens[3].find(":")+1:]
        print(msg)
        if msg.startswith("INI"):
            if app&0b0001==0b0001:
                print("app module already active")
            else:
                #poner un delay aqui luego
                print("Starting app module...")
                app= 0b0001
                print("...App module started")
        elif msg.startswith("BRK"):
            if app==0b0000:
                print("app module hasn't been initiated")
            else:
                print("stoping app module...")
                #delay mas adelante
                app=0
                print("...Stoped app module")
        if app&0b0001==0b0001:    
            if msg.startswith("AP"):
                startApp(msg)
            elif msg.startswith("ST"):
                stopApp(msg)
        

        else:
            print("App module hasn't been started")




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