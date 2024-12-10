import os
import socket
import threading
import sqlite3
import time
from queue import Queue
from datetime import date, timedelta
import pickle
import os
from PIL import Image
import io
prtnm = int(input("Please enter the port number you want the server to use: "))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((socket.gethostbyname(socket.gethostname()), prtnm))

print("\nMessage to correctors: A picture with name BeirutRaouche.jpg is inserted in the file to try the function of seeing a products picture")
print("\n                       Please have the file temp.txt in the repository")
print("\n                       Note: A registered username cannot be used twice")



db = sqlite3.connect('db.AUBoutique')
db.execute("PRAGMA foreign_keys=on")
cursor = db.cursor()
#hayda l part mafroud ykoun bi while loop in order to take many clients.
#check tahet

#TODO: 1- When you login, if you have incoming msgs, let it tell u, and then you have to open a msg by going to 2
    #       If multiple people have msged u, you can check any of ur choice until you check them all
    #2- When you go to 1 and msg someone, if user isnt in 2
                # - If user is online, but not in 2, store it in database but send them a msg that someone texted them. view later
                #- If user is not online, just store it in database



#TABLE INFO:
  #Username always stored in lower case
#cursor.execute("DROP TABLE IF EXISTS Purchases") 
#db.commit()
#cursor.execute("DROP TABLE IF EXISTS Products")
#db.commit()
#cursor.execute("DROP TABLE IF EXISTS Messages")
#db.commit()
#cursor.execute("DROP TABLE IF EXISTS Users")
#db.commit()



cursor.execute("CREATE TABLE if not exists Users (name TEXT, mail TEXT UNIQUE, username TEXT PRIMARY KEY UNIQUE, password TEXT)") #name, email address, username, and password.
db.commit()
# ONLINE LIST OF USERS
# contains IP and Port
#cursor.execute("CREATE TABLE if not exists Online(username TEXT, ip_address TEXT, port INT, in_chat TEXT, FOREIGN KEY(username) REFERENCES Users(username))") 



cursor.execute("CREATE TABLE if not exists Products(username TEXT, product_name TEXT, price INT, desc TEXT, filename TEXT, FOREIGN KEY(username) REFERENCES Users(username))") 
db.commit()

cursor.execute("CREATE TABLE if not exists Messages(source TEXT, destination TEXT, message TEXT, FOREIGN KEY(source) REFERENCES Users(username))") 
db.commit()


cursor.execute("CREATE TABLE if not exists Purchases(owner TEXT, buyer TEXT, product TEXT, price INT, FOREIGN KEY(owner) REFERENCES Users(username),  FOREIGN KEY(buyer) REFERENCES Users(username))") 
db.commit()
Purchases = []




# def setOnline(username, ip, port, cursor, db):
#     cursor.execute("INSERT INTO Online values(?, ?, ?, ?)", (username, ip, port, "false"))
#     db.commit()
    
# def enableChat(username, db):
#     cursor = db.cursor()
#     cursor.execute("UPDATE Online SET in_chat=true WHERE username=?", (username))
    
# def disableChat(username, db):
#     cursor = db.cursor()
#     cursor.execute("UPDATE Online SET in_chat=false WHERE username=?", (username))
# TODO: When you terminate client, or decide to log out, use this

#gna run
# deal

def receiveImageFile(connection):
    f = open("Image", "wb")
    fileData = b""
    while True:
        if fileData[-5:] == b"<END>":
            break
        data = connection.recv(1024)
        fileData+=data
    f.write(fileData[:-5])


accountTries = {}
def resetTries(username):
    del accountTries[username]
    
def incrementTries(username):
    accountTries[username]+=1

LOGIN_COOLDOWN = 15

STOP_TIMER_AND_RESET = False
seconds = 0
def Timer (username):
    global seconds, STOP_TIMER_AND_RESET, LOGIN_COOLDOWN
    print("STARTED TIME FOR ", username)
    seconds = LOGIN_COOLDOWN
    while seconds > 0:
        if STOP_TIMER_AND_RESET:
            STOP_TIMER_AND_RESET = False
            break
        time.sleep(1)
        seconds-=1
    resetTries(username)
    
        
def authentication(connection, address, cursor, db):
    global STOP_TIMER_AND_RESET, seconds, LOGIN_COOLDOWN
    #Get username and password
    while True:
        #Get LOGIN/REGISTER input
        option = connection.recv(1024).decode('utf-8')
        
        if option == "LOGIN":
            counter = 0
            while counter < 3:
                username, password = connection.recv(1024).decode('utf-8').split()
                
                #Get user data from the database
                try:      
                    #Already checks for username
                    cursor.execute("SELECT password FROM Users WHERE username=? ", (username.lower(),))
                    targetPassword = cursor.fetchall() #check that this is not rendered between parentheses.
                    if not targetPassword:
                        raise sqlite3.IntegrityError
                    else:
                        targetPassword = targetPassword[0][0]        
                    
                    
                    if  password == targetPassword:
                        connection.sendall("CORRECT".encode('utf-8'))
                        STOP_TIMER_AND_RESET = True
                        return username
                    else: #Invalid Password
                        counter += 1
                        connection.send("INVALID_INFO".encode('utf-8'))
                        #raise sqlite3.IntegrityError
                except sqlite3.IntegrityError:
                    counter += 1
                    connection.send("INVALID_INFO".encode('utf-8'))
                    print("No user with that username exists")
                    

                    
                    
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
                # setOnline(username, clientIP, clientPort, cursor, db)
                
                return username
            except sqlite3.IntegrityError:
                print("Account already exists. Duplicate detected.")
                connection.sendall("ACCOUNT_ALREADY_EXISTS".encode('utf-8'))
        elif option == "EXIT":
            return -1
        

def picture(connection, db):
    db=sqlite3.connect('db.AUBoutique')
    cursor=db.cursor()
    cursor.execute("SELECT * FROM Products")
    answer = cursor.fetchall()
    if (not answer):
        connection.send("No products".encode('utf-8'))
        return
    else:
        connection.send("Hey".encode("utf-8"))
    product=connection.recv(1024).decode('utf-8')
    
    cursor.execute(f"SELECT * FROM Products WHERE product_name = \"{product}\"")
    image=cursor.fetchall()
    print(image)
    if(not image):
        connection.send("Invalid product".encode('utf-8'))
        while(not image):
            product=connection.recv(1024).decode()
            cursor.execute(f"SELECT * FROM Products WHERE product_name = \"{product}\"")
            image=cursor.fetchall()
            if(image==None):
                connection.send("Invalid product".encode('utf-8'))
            else:
                connection.send("Good".encode('utf-8'))
                break
    else:
        connection.send("Good".encode('utf-8'))
    try:
        print(image)
        file=open(image[0][4],"rb")
        data=file.read()
        size=os.stat(image[0][4]).st_size
        connection.send(str(size).encode('utf-8'))
        connection.send(data)
        file.close()
    except Exception as e:
        connection.send("No file available".encode('utf-8'))
        
        
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
    if(len(usersProducts) == 0):
        return
    for i in range(len(usersProducts)):
        connection.sendall(pickle.dumps(usersProducts[i]))
        connection.recv(1024)
    
OnlineUserConnections = {}
incomingQueues = {}

def sendOnlineUsers(connection, cursor):
    #cursor.execute("SELECT username FROM Online WHERE in_chat=true")
    #onlineUsers = cursor.fetchall()
    #print("BEFORE LOL")
    onlineUsers= []
    for users in OnlineUserConnections:
        onlineUsers.append(users)
    connection.sendall(pickle.dumps(onlineUsers))
    #print("LOLLL")
    # for i in range(len(onlineUsers)):
    #     connection.sendall(pickle.dumps(onlineUsers[i]))
    #connection.sendall("<END>".encode('uf-8'))


#client 1 sends to server
#server stores data in database
#client 2 receives the data and prints it from the database

def buyProducts(username, connection, db):
    db = sqlite3.connect('db.AUBoutique')
    cursor = db.cursor()
    while True:
        cursor.execute("SELECT * FROM Products")
        prods = cursor.fetchall()
        good = False
        if not prods:
            connection.send("There are no products on the market.".encode('utf-8'))
            break
        for i in range(len(prods)):
            if prods[i][0] != username:
                  good = True
        if good == False:
            connection.send("All the products on the market are your own. You cannot buy at this time.".encode('utf-8'))
            break
        connection.sendall("22".encode('utf-8'))
        product = connection.recv(1024).decode('utf-8')
        
        cursor.execute("SELECT username, price FROM Products WHERE product_name = ?", (product, ))
        data = cursor.fetchall()
        if not data:
            connection.send("The entered product is not up for sale. Please try again.".encode('utf-8'))
            continue
        print(data)
        if (data[0][0] != username):
            connection.sendall("Product name received".encode('utf-8'))
        else:
            connection.send("You cannot purchase your own products. Please choose another product to buy.".encode('utf-8'))
            continue
        cursor.execute("DELETE FROM Products WHERE product_name = ?", (product,))
        db.commit()
        cursor.execute("INSERT INTO Purchases values(?,?,?,?)", (data[0][0], username, product, data[0][1]))
        db.commit()
        connection.recv(1024)
        connection.sendall("t".encode('utf-8'))
        break
        
inChatOf = {}

#make it a queue 
def sendChat(username,target, connection):
    while True:
        messageToSend = incomingQueues[username].get()
        if messageToSend.lower() == "exit": 
            connection.sendall("EXIT_CHAT".encode('utf-8'))
            #inChatOf[target] = ""  
            inChatOf[username] = ""  
            break
        connection.sendall(messageToSend.encode('utf-8'))
        


def receiveChat(username,target, connection, db):
    db = sqlite3.connect('db.AUBoutique')
    cursor = db.cursor()
    #connection.send("0".encode('utf-8'))
    while True:
        messageToSend = connection.recv(1024).decode('utf-8')

        if messageToSend == "EXIT_CHAT":
            #inChatOf[target] = ""  
            inChatOf[username] = ""  
            incomingQueues[target].put(messageToSend)
            break
        
        if username in inChatOf and target in inChatOf and inChatOf[username] ==target and inChatOf[target]==username:
            incomingQueues[target].put(messageToSend)
        else: 
            if username and target and messageToSend:
                cursor.execute("INSERT INTO Messages values(?, ?, ?)", (username, target, messageToSend,))
                db.commit()
            else: print("BUGG")





def receiveChatUNAVAILABLE(source, target , connection, db):
    db = sqlite3.connect('db.AUBoutique') #this creates a connection from this thread to the database since every thread has to have its own connection
    cursor = db.cursor()
    
            
    while True:
        messageToSendLater = connection.recv(1024).decode('utf-8')
        print(messageToSendLater)
        print("kifak")
        if messageToSendLater == "EXIT_CHAT":
            cursor.close()
            break

        if source and target and messageToSendLater:
            cursor.execute("INSERT INTO Messages VALUES (?, ?, ?)", (source, target, messageToSendLater))
        else: print("BUGGGGG")

        db.commit()
        
        

                # exit = connection.recv(1024).decode('utf-8')
                # if exit == "EXIT_CHAT":
                #     continue
      
WaitingForConnection = {}
def handle_messaging(username, connection, db):
    cursor = db.cursor()
    # try:
    while True:
        # cursor.execute("SELECT message from Messages WHERE destination=?", (username,))
        # unread_messages = cursor.fetchall()
        # if not unread_messages:
        #     print("There are no unread messages.")
        #     connection.send("NO_UNREAD".encode('utf-8'))
        # else:
        #     connection.send("UNREAD".encode('utf-8'))
            
        option = connection.recv(1024).decode('utf-8')
        
        
        #connection.send("OK".encode('utf-8'))
        #response = connection.recv(1024).decode('utf-8')
        if option == "EXIT":
            break
        elif option == "INITIATE_NEW_CHAT":
            #start a new chat with a user and thats it
            connection.send("OK".encode('utf-8'))
            target = connection.recv(1024).decode('utf-8')
            
            print(target)
            
            inChatOf[username]=target
            #connection.send("OK".encode('utf-8'))
            receivingUNAVAILABLE_thread = threading.Thread(target=receiveChatUNAVAILABLE, args=(username,target, connection, db))
            receivingUNAVAILABLE_thread.start()
        
            #username opens chat with target
            inChatOf[target]= username
            receivingUNAVAILABLE_thread.join()
        
        elif option == "OPEN_EXISTING_CHAT":
            
            # beje bade eftah a chat maa x
            # if x is in the chat, do it live, if not, send
            connection.send("OK".encode('utf-8'))
            # if u open a chat,
            target = connection.recv(1024).decode('utf-8')
            #target hon is the username you want to open chat with
            inChatOf[target] = username    

            cursor.execute("SELECT message FROM Messages WHERE source=? AND destination=?", (target, username))
            messages = cursor.fetchall()
            # if not messages:
            #     connection.send("NO_SUCH_USER".encode('utf-8'))
            # else:
            #connection.send("SUCCESS".encode('utf-8'))
            #connection.recv(1024)
            connection.send(f"{len(messages)}".encode('utf-8'))
            connection.recv(1024)
            print("AMOUNT OF MSGS: " + str(len(messages)))
            print(messages)
            for i in range(len(messages)):
                connection.send(messages[i][0].encode('utf-8'))
                connection.recv(1024)
            
            cursor.execute("DELETE FROM Messages WHERE source=? AND destination=?", (target,username))
            db.commit()
                # exit = connection.recv(1024).decode('utf-8')
                # if exit == "EXIT_CHAT":
                #     continue
            
            sending_thread = threading.Thread(target=sendChat, args=(username, target, connection,))
            receiving_thread = threading.Thread(target=receiveChat, args=(username, target, connection, db))
            sending_thread.start()
            receiving_thread.start()
            
            sending_thread.join()
            receiving_thread.join()
                
            #  3 cases
            # - user opens chat with x while x is on the chat   
                #sendchat w receivechat both client and server
                
            # - user opens chat with x when x isnt Online 
                # receiveChatUNAVAILABLE and sendchat (clientside)
                
            # - user opens chat when x isnt online, but then x joins the chat while user is in chat
             
def logOutUser(connection, username, cursor, db):
     del OnlineUserConnections[username]
     connection.sendall("LOGOUT_SUCCESS".encode('utf-8'))
           
#Handle add product
def add_product(connection, username,cursor,  db):
    connection.sendall("Opened add products now.".encode('utf-8'))
    while True:
        
            product_name, price, description, filename = connection.recv(1024).decode('utf-8').split(",")
            print(product_name, price, description)
            print("testing0")
            cursor.execute("INSERT INTO Products VALUES(?, ?, ?, ?, ?)", (username, product_name, float(price), description, filename))
            print("testing1")
            db.commit()
            print("testing2")
            cursor.execute("SELECT * FROM Products WHERE product_name = ?", (product_name,))
            print(cursor.fetchall())
            print("testing3")
            # Fetch all results
            #sendProducts(connection, db)
            connection.sendall("PRODUCT_ADDED".encode('utf-8'))
            break

        #except Exception as e:
            #connection.sendall("ERROR: Cannot ADD product".encode('utf-8'))
        

def view_buyers(connection, username, db):
    db = sqlite3.connect('db.AUBoutique')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Purchases WHERE owner=?", (username,))
    list = cursor.fetchall()
    

    n = (str) (len(list))
    connection.send(n.encode('utf-8'))
    connection.recv(1024)
    for i in range (len(list)):
        connection.sendall(pickle.dumps(list[i]))
        connection.recv(1024)
        
     


def handle_client(connection, address):
    
    db = sqlite3.connect('db.AUBoutique')
    cursor = db.cursor()
    #why did we use this here, and why was it mandatory

    #Acts like assert, doesnt prcoeed until we exit from authentication
    while True: 
        myUsername = authentication(connection, address, cursor, db) 
        if myUsername == -1:
            connection.close()

            return
        
        OnlineUserConnections[myUsername] = connection
        incomingQueues[myUsername]= Queue()
        
        
        while True:
            # threadLocks[myUsername].acquire()
            # threadLocks[myUsername].release()
            
           
            option = connection.recv(1024).decode('utf-8')
            username = myUsername
            
            if option == "ADD_PRODUCT":
                add_product(connection, username, cursor, db)
            elif option ==  "VIEW_USERS_PRODUCTS":
                sendUsersProducts(connection, db)
            elif option == "SEND_PRODUCTS":
                sendProducts(connection, db)
            elif option =="MSG":
                handle_messaging(myUsername, connection, db)
            elif option == "BUY_PRODUCTS":
                buyProducts(username, connection, db)
            elif option == "VIEW_BUYERS":
                view_buyers(connection, username, db)
            elif option == "VIEW_PICTURE":
                picture(connection, db)
            elif option =="LOG_OUT":
                logOutUser(connection, username, cursor, db)
                break
            #zet l shi la be2e l options (LIST_PRODUCTS, ...)
   
        
        

server.listen()
while True:
    connection,address= server.accept()
    server_thread = threading.Thread(target=handle_client, args=(connection, address))
    server_thread.start()


#def start_server():
    #server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #
    #server.listen()
    #while True:
    #    connection,address= server.accept()
    #    server_thread = threading.Thread(target=handle_client, args=(connection, address))
    #    server_thread.start()
    