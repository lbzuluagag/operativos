import socket
import threading


HEADER = 1024
PORT = 5050
FORMAT = 'utf-8'
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def write():
    print("Sending message")
    msg="CLIENT"
    client.send(msg.encode(FORMAT))
    while True:
        DST=input("Destiny: ")
        MSG=input("message: ")
        a="cmd"
        msg=f"cmd:info,src:CLIENT,dst:{DST},msg:{MSG}"
        client.send(msg.encode(FORMAT))
        res = client.recv(HEADER).decode(FORMAT)
        tokens=res.split(",")
        cmd=tokens[0][4:]
        src=tokens[1][tokens[1].find(":")+1:]
        dst=tokens[2][tokens[2].find(":")+1:]
        msg=tokens[3][tokens[3].find(":")+1:]
        if cmd =="erro":
            print(res)
            break
        else:
            print(res)




#iniciamos los hilos
#este primer hilo es para que este pendiente del metodo receive
#receive_thread = threading.Thread(target=receive)
#receive_thread.start()

#Este hilo solo se preocupa de el metodo write
write_thread = threading.Thread(target=write)
write_thread.start()
