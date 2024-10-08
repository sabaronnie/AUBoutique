import socket
import threading
import sqlite3
import time
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((socket.gethostbyname(socket.gethostname()), 9999))

db = sqlite3.connect('db.AUBoutique')
cursor = db.cursor()
#hayda l part mafroud ykoun bi while loop in order to take many clients.
#check tahet



#mail lezem tkoun l primary key ahsan

#TABLE INFO:
# - Username always stored in lower case
cursor.execute("CREATE TABLE if not exists Users (name TEXT, mail TEXT PRIMARY KEY, username TEXT, password TEXT)") #name, email address, username, and password.



    
      
def authentication(connection, address):
    #Get username and password
    blockLOGIN = False
    
    while True:
        #Get LOGIN/REGISTER input
        option = connection.recv(1024).decode('utf-8')
        
        if option == "LOGIN":
            username, password = connection.recv(1024).decode('utf-8').split()
                
            #Get user data from the database
            try:
                    
                cursor.execute("SELECT username, password FROM Users WHERE username=? ", (username.lower(),))
                targetUsername, targetPassword = cursor.fetchall()
                
                if username == targetUsername and password == targetPassword:
                    connection.sendall("0".encode('utf-8'))
                    return 0
                else: #Invalid Username or Password
                    connection.sendall("1".encode('utf-8'))                        
                    counter+=1
            except:
                #if no such account even exists, also say invalid username or password
                # badkon naamela t2oul no suck account exists mnel ekher?
                print("No user with that username exists")
                connection.sendall("1".encode('utf-8'))
                    
                    
        elif option =="REGISTER":
            name, email, username, password = connection.recv(1024).decode('utf-8').split()`
    
    
def handle_client(connection, address):
    #First authenticate 
    #Acts like assert, doesnt prcoeed until we exit from authentication
    if authentication(connection, address) == -1:
        connection.close()
        return

server.listen()
while True:
    connection,address= server.accept()
    server_thread = threading.Thread(target="handle_client", args=("connection", "address"))
    server_thread.start()
    



