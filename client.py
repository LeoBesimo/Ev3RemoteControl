import socket
import threading
from Controller import ControllerHandler, InputMethods

inputValues = {}

handler = ControllerHandler()
serverPort = 55555

def getControls():
    while True:
        inputs = handler.getInputs()
        for input in inputs:
            inputValues[input[0].name] = input[1]
        

def main():
    #serverIP = input("Input Server IP: ")
    serverIP = "192.168.1.38"
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((serverIP, serverPort))
    print(client.recv(1024).decode("utf-8"))

    print(f"Connected to Server")


    thread = threading.Thread(target=getControls)
    thread.start()

    while True:
        try:
            client.send(f"{inputValues}".encode("utf-8"))
            print(client.recv(1024).decode("utf-8"))
        except Exception as e:
            print(e)
            break
            

if __name__=="__main__":
    main()