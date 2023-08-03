import socket
import threading

serverPort = 55555

def connectClient(server):
    server.listen()
    client, clientIP = server.accept()
    print(f"Client Connected with IP {clientIP}")
    return client



def main():
    hostname = socket.gethostname()
    ipaddr = socket.gethostbyname(hostname)
    
    print(f"hostname: {hostname}    ip: {ipaddr}")
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ipaddr, serverPort))
    
    client = connectClient(server)

    while True:
        try:
            client.send(f"server".encode("utf-8"))
            print(client.recv(1024).decode("utf-8"))
        except Exception as e:
            print(e)
            client = connectClient(server)



if __name__=="__main__":
    main()