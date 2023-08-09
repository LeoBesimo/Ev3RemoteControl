#!/usr/bin/env python3

import socket
import threading
from time import sleep
import os

from ev3dev2.motor import MoveTank, OUTPUT_B, OUTPUT_C

serverPort = 55555
lSpeed = 0
rSpeed = 0

motor = MoveTank(OUTPUT_C, OUTPUT_B)

def connectClient(server):
    server.listen()
    client, clientIP = server.accept()
    print("Client Connected")
    print("Client Connected with IP: ")
    print(str(clientIP))
    return client

def parseMessage(message):
    global rSpeed, lSpeed
    splitMessage = message.split(":")
    rSpeed = int(splitMessage[1])
    lSpeed = int(splitMessage[0])
    #print("RSpeed: " + str(rSpeed) + "   LSpeed: " + str(lSpeed))

def driveRobot():
    global lSpeed, rSpeed, motor
    while True:
        #print(str(lSpeed) + " " + str(rSpeed))
        if(lSpeed == 0 and rSpeed == 0):
            motor.off()
        else:
            motor.on(left_speed=lSpeed, right_speed=rSpeed)

def main():

    os.system('setfont Lat15-TerminusBold14')

    hostname = socket.gethostname()
    ipaddr = socket.gethostbyname(hostname)
    
    #print(f"hostname: {hostname}    ip: {ipaddr}")
    print("Hostname: " + hostname + "   ip: " + ipaddr)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ipaddr, serverPort))
    
    client = connectClient(server)

    moveThread = threading.Thread(target=driveRobot)
    moveThread.start()

    while True:
        try:
            #sleep(0.01)
            client.send("Confirmed".encode("utf-8"))
            message = client.recv(1024).decode("utf-8")
            parseMessage(message)
            #print(message)
        except Exception as e:
            #print("Client Disconnected due to: ")
            #print(e)
            print("Client Disconnected")
            print("Hostname: " + hostname + "   ip: " + ipaddr)
            client = connectClient(server)



if __name__=="__main__":
    main()