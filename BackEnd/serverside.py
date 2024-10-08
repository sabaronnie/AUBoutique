import socket
import threading
import sqlite3
import time
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((socket.gethostbyname(socket.gethostname()), 9999))

db = sqlite3.connect('db.AUBoutique')
db.execute("PRAGMA foreign_keys=on")
cursor = db.cursor()
#hayda l part mafroud ykoun bi while loop in order to take many clients.
#check tahet



#mail lezem tkoun l primary key ahsan

#TABLE INFO:
# - Username always stored in lower case
cursor.execute("CREATE TABLE if not exists Users (name TEXT, mail TEXT UNIQUE, username TEXT PRIMARY KEY UNIQUE, password TEXT)") #name, email address, username, and password.

# ONLINE LIST OF USERS
# contains IP and Port
cursor.execute("CREATE TABLE if not exists Online(username TEXT, ip_address TEXT, port INT, FOREIGN_KEY(username) REFERENCES Users(username))") 

# PRODUCT LIST
cursor.execute("CREATE TABLE if not exists Products(username TEXT, product_name TEXT, FOREIGN_KEY(username) REFERENCES Users(username))") 


def setOnline(username, ip, port):
    cursor.execute("INSERT INTO Online values(?, ?, )", (username, ip, port))

# TODO: When you terminate client, or decide to log out, use this
def removeOnline(username):
    cursor.execute("DELETE FROM Online WHERE username=?", (username))
    
def authentication(connection, address):
    #Get username and password
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
                    clientIP, clientPort = connection.recv(1024).decode('utf-8').split()
                    # Set signed in user as online
                    setOnline(username, clientIP, clientPort)
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
            try:
            # Register then logs you in
                name, email, username, password = connection.recv(1024).decode('utf-8').split()
                cursor.execute("INSERT INTO Users values(?, ?, ?, ?)", (name.lower(), email.lower(), username.lower(), password))
                connection.send("ACCOUNT_CREATED".encode('utf-8'))
                
                clientIP, clientPort = connection.recv(1024).decode('utf-8').split()
                setOnline(username, clientIP, clientPort)
            except:
                print("Account already exists. Duplicate detected.")
                connection.send("ACCOUNT_CREATED".encode('utf-8'))
                
            
    
    
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
    



