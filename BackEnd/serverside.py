import socket
import threading
import sqlite3
import time
from queue import Queue
from datetime import date, timedelta
import pickle
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
        option = connection.recv(1024).decode('utf-8')
        
        if option == "LOGIN":
            username, password = connection.recv(1024).decode('utf-8').split()
                
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
        

        
# def addSpaces(file1):
    
def sendProducts(connection, db):

    cursor = db.cursor()
    ##SEND AS JSONN 
    # cuz when we mae gui, we cant use pretty tables sl we need to be 
    # ready to read the file
  
    
    cursor.execute("SELECT * FROM Products")
    productsByUser = cursor.fetchall()
    connection.sendall(str(len(productsByUser)).encode('utf-8'))
    response = connection.recv(1024).decode('utf-8')
    print(response)
    for i in range(len(productsByUser)):
        connection.sendall(pickle.dumps(productsByUser[i]))
        connection.recv(1024)
    # t1 = cursor.fetchall()
    # file1.write(t1)
    # file1.close()
    # file2 = open("ServerFiles/toBePrinted", 'rb')
    # for lines in file2:
    #     connection.sendall(lines)

#"CREATE TABLE if not exists Online(username TEXT, ip_address TEXT, port INT, FOREIGN KEY(username) REFERENCES Users(username))") 

def sendUsersProducts(connection, db):
    cursor = db.cursor()
    connection.sendall("Function of sending users products now open".encode('utf-8'))
    username = connection.recv(1024).decode('utf-8')
    cursor.execute("SELECT product_name, price, desc FROM Products WHERE username = ?", (username,))
    usersProducts = cursor.fetchall()
    connection.sendall(str(len(usersProducts)).encode('utf-8'))
    
    for i in range(len(usersProducts)):
        connection.sendall(pickle.dumps(usersProducts[i]))
        connection.recv(1024)
    
def sendOnlineUsers(connection, cursor):
    cursor.execute("SELECT username FROM Online WHERE in_chat=true")
    onlineUsers = cursor.fetchall()
    print("BEFORE LOL")
    connection.sendall(pickle.dumps(onlineUsers))
    print("LOLLL")
    # for i in range(len(onlineUsers)):
    #     connection.sendall(pickle.dumps(onlineUsers[i]))
    #connection.sendall("<END>".encode('uf-8'))

def buyProducts(connection, cursor):
    connection.sendall("".encode('utf-8'))
    product = connection.recv(1024).decode('utf-8')
    connection.sendall("Product name received".encode('utf-8'))
    cursor.execute("DELETE FROM Products WHERE product_name = ?", (product,))
    connection.recv(1024)
    connection.sendall("toni".encode('utf-8'))
    #iza badak make a random number generator
    #to decide how much time till u get the item
    
    
OnlineUserConnections = {}
threadLocks = {}
threadEvents = {}

#make it a queue 
def sendChatSENDER(username,target, connection):
    #targetUser, targetIP, targetPort, in_chat = targetDetails
    try:
        targetConnection = OnlineUserConnections[target]

        targetConnection.sendall(username.encode('utf-8'))
        response = targetConnection.recv(1024).decode('utf-8')
        connection.send(response.encode('utf-8'))
        if response == "REQUEST_ACCEPTED":
            while True:
                messageToSend = connection.recv(1024).decode('utf-8')
                if messageToSend.lower() == "exit": 
                    connection.sendall("EXIT_CHAT".encode('utf-8'))
                    break
                targetConnection.sendall(messageToSend.encode('utf-8'))
                print(messageToSend)
        threadEvents[target].set(True)
    except Exception as e:
        print(type(e).__name__)
        print("THE ERROR IS IN SEND CHAT SENDER")
# def receiveChatRECEIVER(connection):
#     while True:
#         global SenderToReceiver
#         sendMsg = SenderToReceiver.get()
#         connection.sendall(sendMsg.encode('utf-8'))
        
# 

 
    
    
def handle_messaging(username, connection, db):
    cursor = db.cursor()
    try:
        option = connection.recv(1024).decode('utf-8')
        if option == "INITIATE_CHAT": #sends chat request for somekne waiting
            sendOnlineUsers(connection, cursor)
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
        elif option == "LISTEN_FOR_CHAT":
            if username not in OnlineUserConnections:
                OnlineUserConnections[username] = connection
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
            
    except Exception as e:
        print(type(e).__name__)
        print("BRO LEH FETIT ERROR YA ZABREEEEEEEEEEEEEEE")
        connection.sendall("NOT_ONLINE".encode('utf-8'))
        
def logOutUser(connection, username, cursor, db):
     removeOnline(username, db)
     connection.sendall("LOGOUT_SUCCESS".encode('utf-8'))
    
        
            
#Handle add product
def add_product(connection, username,cursor,  db):
    connection.sendall("Opened add products now.".encode('utf-8'))
    try:
        product_name, price, description = connection.recv(1024).decode('utf-8').split(",")
        print (product_name)
        print(price)
        print(description)
        print(username)
        cursor.execute("INSERT INTO Products VALUES(?, ?, ?, ?)", (username, product_name, float(price), description))
        db.commit()

        #sendProducts(connection, db)
        connection.sendall("PRODUCT_ADDED".encode('utf-8'))


    except Exception as e:
        connection.sendall("ERROR: Cannot ADD product".encode('utf-8'))

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
        #TODO for some reason aweatwhen i close the clients, it spams this print
        print("SOMEHOW WE BACK HERE")
        option = connection.recv(1024).decode('utf-8')
        username = myUsername
        
        if option == "ADD_PRODUCT":
            add_product(connection, username, cursor, db)
        elif option == "SEND_PRODUCTS":
            sendProducts(connection, db)
        elif option ==  "VIEW_USERS_PRODUCTS":
            sendUsersProducts(connection, db)
        elif option =="MSG":
            handle_messaging(myUsername, connection, db)
        elif option =="LOG_OUT":
            logOutUser(connection, username, cursor, db)
        elif option == "BUY_PRODUCTS":
            buyProducts(connection, cursor)
        #zet l shi la be2e l options (LIST_PRODUCTS, ...)
   
        
        
    

server.listen()
while True:
    connection,address= server.accept()
    server_thread = threading.Thread(target=handle_client, args=(connection, address))
    server_thread.start()
    








