import socket
def receiveImageFile(connection):
    f = open("Image", "wb")
    fileData = b""
    while True:
        if fileData[-5:] == b"<END>":
            break
        data = connection.recv(1024)
        fileData+=data
    f.write(fileData[:-5])