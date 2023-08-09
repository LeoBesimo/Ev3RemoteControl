import socket
import threading
from Controller import ControllerHandler, InputMethods

inputValues = {
    InputMethods.LStickY.name: 0,
    InputMethods.RStickY.name: 0
}

handler = ControllerHandler()
serverPort = 55555

threshhold = 3000

def map(value, oldMin, oldMax, newMin, newMax):
    return newMin + (newMax - newMin) * ((value - oldMin) / (oldMax - oldMin))

def getControls():
    while True:
        inputs = handler.getInputs()
        for input in inputs:
            if input[0] == InputMethods.LStickY or input[0] == InputMethods.RStickY:
                if(input[1] > -threshhold and input[1] < threshhold):
                    inputValues[input[0].name] = 0
                else:
                    inputValues[input[0].name] = int(map(input[1],-32767, 32767,-100,100))
        

def main():
    serverIP = input("Input Server IP: ")
    #serverIP = "192.168.1.38"
    #serverIP = "192.168.1.18"
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((serverIP, serverPort))
    print(client.recv(1024).decode("utf-8"))

    print(f"Connected to Server")


    thread = threading.Thread(target=getControls)
    thread.start()

    while True:
        try:
            client.send(f"{inputValues[InputMethods.LStickY.name]}:{inputValues[InputMethods.RStickY.name]}".encode("utf-8"))
            client.recv(1024)
            #print(client.recv(1024).decode("utf-8"))
        except Exception as e:
            print(e)
            break
            

if __name__=="__main__":
    main()