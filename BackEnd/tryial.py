import socket

def sendImageFile(filename):
    while True:
        file1 = open("BackEnd/ClientStorage/" + filename, "rb")
        for line in file1:
            client.sendall(line)
        client.sendall(b"END")
    


