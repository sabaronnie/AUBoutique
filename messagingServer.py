import socket
import threading
import sqlite3
import time
from queue import Queue
from datetime import date, timedelta
import pickle
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((socket.gethostbyname(socket.gethostname()), 8888))

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
cursor.execute("CREATE TABLE if not exists Online(username TEXT, ip_address TEXT, port INT, in_chat TEXT, FOREIGN KEY(username) REFERENCES Users(username))") 

# PRODUCT LIST
#ADD IMAGES
cursor.execute("CREATE TABLE if not exists Products(username TEXT, product_name TEXT, price INT, desc TEXT, FOREIGN KEY(username) REFERENCES Users(username))") 
db.commit()

def setOnline(username, ip, port, cursor, db):
    cursor.execute("INSERT INTO Online values(?, ?, ?, ?)", (username, ip, port, "false"))
    db.commit()
    
def enableChat(username, db):
    cursor = db.cursor()
    cursor.execute("UPDATE Online SET in_chat=true WHERE username=?", (username))
    
def disableChat(username, db):
    cursor = db.cursor()
    cursor.execute("UPDATE Online SET in_chat=false WHERE username=?", (username))
# TODO: When you terminate client, or decide to log out, use this
def removeOnline(username, db):
    cursor = db.cursor()
    cursor.execute("DELETE FROM Online WHERE username=?", (username))
    db.commit()
    
def authentication(connection, address, cursor, db):
    #Get username and password
    while True:
        #Get LOGIN/REGISTER input
        #option = connection.recv(1024).decode('utf-8')
        option = "LOGIN"
        if option == "LOGIN":
            username, password = ("ron", "12345678")
            #connection.recv(1024).decode('utf-8').split()
                
            #Get user data from the database
            try:      
                #Already checks for username
                cursor.execute("SELECT password FROM Users WHERE username=? ", (username.lower(),))
                print("NOT PASSED YET")
                targetPassword = cursor.fetchall()[0][0] #check that this is not rendered between parentheses.
                print("PASSED HERE")
                
                if  password == targetPassword:
                    connection.sendall("CORRECT".encode('utf-8'))
                    clientIP, clientPort = connection.recv(1024).decode('utf-8').split()
                    # Set signed in user as online
                    setOnline(username, clientIP, clientPort, cursor, db)
                    return username
                else: #Invalid Password
                    connection.sendall("INVALID_PASSWORD".encode('utf-8'))                        
                    counter+=1
            except:
                #if no such account even exists, also say invalid username or password
                # badkon naamela t2oul no suck account exists mnel ekher?
                print("No user with that username exists")
                connection.sendall("INVALID_INFO".encode('utf-8'))
                return -1
                    
                    
        elif option =="REGISTER":
            try:
            # Register then logs you in
                
                name, email, username, password = connection.recv(1024).decode('utf-8').split(",")
                print(name)
                print(email)
                print(username)
                print(password)
                cursor.execute("INSERT INTO Users values(?, ?, ?, ?)", (name.lower(), email.lower(), username.lower(), password))
                db.commit()
                connection.sendall("ACCOUNT_CREATED".encode('utf-8'))
                
                
                
                clientIP, clientPort = connection.recv(1024).decode('utf-8').split()
                setOnline(username, clientIP, clientPort, cursor, db)
                
                return username
            except sqlite3.IntegrityError:
                print("Account already exists. Duplicate detected.")
                connection.sendall("ACCOUNT_ALREADY_EXISTS".encode('utf-8'))
                return -1
        
        
OnlineUserConnections = {}
threadLocks = {}
threadEvents = {}


def sendOnlineUsers(connection, cursor):
    cursor.execute("SELECT username FROM Online WHERE in_chat=true")
    onlineUsers = cursor.fetchall()
    print("BEFORE LOL")
    connection.sendall(pickle.dumps(onlineUsers))
    print("LOLLL")
#make it a queue 
def sendChatSENDER(username,target, connection):
    #targetUser, targetIP, targetPort, in_chat = targetDetails
    targetConnection = OnlineUserConnections[target]

    targetConnection.sendall(username.encode('utf-8'))
    response = targetConnection.recv(1024).decode('utf-8')
    if response == "REQUEST_ACCEPTED":
        while True:
            messageToSend = connection.recv(1024).decode('utf-8')
            if messageToSend.lower() == "exit": 
                connection.sendall("EXIT_CHAT".encode('utf-8'))
                break
            targetConnection.sendall(messageToSend)
            print(messageToSend)
    threadEvents[target].set(True)
# def receiveChatRECEIVER(connection):
#     while True:
#         global SenderToReceiver
#         sendMsg = SenderToReceiver.get()
#         connection.sendall(sendMsg.encode('utf-8'))
        
# 

 
    
    
def handle_messaging(username, connection, db):
    cursor = db.cursor()
    #sendOnlineUsers(connection, cursor)
    try:
        option = connection.recv(1024).decode('utf-8')
        if option == "INITIATE_CHAT": #sends chat request for somekne waiting

            print("GOT TARGET")
            target = connection.recv(1024).decode('utf-8')
            #cursor.execute("SELECT username, ip_address, port, in_chat FROM Online WHERE username=?", (target,))
            #targetDetails = cursor.fetchall()
            if target in OnlineUserConnections:
                print("OK FOUND")
                connection.sendall("FOUND".encode('utf-8'))
                
                targetConnection = OnlineUserConnections[target]
                #Make them online 
                print("SAVING USER IN ONLINE AVAILABLE")
                if username not in OnlineUserConnections:
                    OnlineUserConnections[username] = connection
                
                # targetTHREADLOCK = threadLocks[target]
                # targetTHREADLOCK.acquire()
                #send a msg request to user
                print("MY NAME IS: " + username)
                print("opened chat for receiver")
                sendChatSENDER(username,target, connection)
                
                # targetTHREADLOCK.release()
            else:
                connection.sendall("NOT_ONLINE".encode('utf-8'))

            #add later a check that the user is still available at this point
            
            
            
                # sending_thread = threading.Thread(target=sendChatSENDER, args=(connection,))
                # receiving_thread = threading.Thread(target=receiveChatSENDER, args=(connection,))
                # sending_thread.start()
                # receiving_thread.start()
        elif option == "LISTEN_FOR_CHAT":
            print("woslit")
            if username not in OnlineUserConnections:
                OnlineUserConnections[username] = connection
            print('woslit2')
            threadEvents[username].wait()
            threadEvents[username].clear()
            print("WOOP WOOP")
            # targetTHREADLOCK[username].acquire()
            # targetTHREADLOCK[username].release()
            #connection.sendall("OPEN")
            # sending_thread = threading.Thread(target=sendChatRECEIVER, args=(connection,))
            # receiving_thread = threading.Thread(target=receiveChatRECEIVER, args=(connection,))
            # sending_thread.start()
            # receiving_thread.start()
            
    except:
        connection.sendall("NOT_ONLINE".encode('utf-8'))
        
        
def handle_client(connection, address):
    
    db = sqlite3.connect('db.AUBoutique')
    cursor = db.cursor()
    #why did we use this here, and why was it mandatory

    #Acts like assert, doesnt prcoeed until we exit from authentication
    myUsername = authentication(connection, address, cursor, db) 
    if myUsername == -1:
        connection.close()
        return
    
    #threadLocks[myUsername] = threading.Lock()
    threadEvents[myUsername] = threading.Event()
    
    
    while True:
        # threadLocks[myUsername].acquire()
        # threadLocks[myUsername].release()
        print("SOMEHOW WE BACK HERE")
        #option = connection.recv(1024).decode('utf-8')
        option = "MSG"
        if option =="MSG":
            handle_messaging(myUsername, connection, db)

        #zet l shi la be2e l options (LIST_PRODUCTS, ...)
   
        
        
    

server.listen()
while True:
    connection,address= server.accept()
    server_thread = threading.Thread(target=handle_client, args=(connection, address))
    server_thread.start()
    





