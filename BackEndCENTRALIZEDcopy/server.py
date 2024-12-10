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
import queue
#prtnm = int(input("Please enter the port number you want the server to use: "))
prtnm = 9999
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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

userQueues = {}

def receiveThread(connection):
    buffer = b"" 
    ending = b"<END>"
    delimiter = b"BRK"
    remaining = b""
    while True:
        # chunk = connection.recv(1024)
        # if not chunk:
        #     break  # Connection closed
        # buffer += chunk  # Add received data to the buffer
        # #delimiter = b"\0\0"
        # if delimiter in buffer:
        #     header, data = buffer.split(delimiter, 1)
        #     header = header.decode('utf-8')
        #     buffer = b"" 
        # data = connection.recv(1024)
        # #if delimiter in buffer:
        # header, payload = data.split(delimiter, 1)
        # header = header.decode('utf-8')
        
        if not remaining:
            remaining = connection.recv(1024)
        print(remaining)
        receive, remaining = remaining.split(ending, 1)
        
        print("part 1:")
        print(receive)
        print("part 2:")
        print(remaining)
        
        header, ptype, data = receive.split(delimiter, 2)
        header = header.decode('utf-8')
        ptype = ptype.decode('utf-8')
        print("header: ")
        print(header)
        print("ptype: ")
        print(ptype)
        if ptype == "str":
            data=data.decode('utf-8')
            print(data)
        
        # if isinstance(data, str):
        #     payload=payload.decode('utf-8')
        print(header)
        
        if header == "MSG":
            userQueues[connection]['messageQueue_R'].put(data)
        # elif header == "REGISTER" or header == "LOGIN" or header=="AUTH":
        #     authQueue_R.put(data.decode('utf-8'))
        elif header == "REGISTER":
            userQueues[connection]['registerQueue_R'].put(data)
        elif header == "LOGIN":
            #userQueues[connection]['loginQueue_R'].put(data)
            userQueues[connection]['loginQueue_R'].put(data)
        elif header == "AUTH":
            #userQueues[connection]['authQueue_R'].put(data)
            userQueues[connection]['authQueue_R'].put(data)
        elif header == "ADD_PRODUCT":
            userQueues[connection]['addProductQueue_R'].put(data)
        elif header == "IMG_PRODUCT":
            userQueues[connection]['imageProductQueue_R'].put(data)
        elif header == "LOG_OUT":
            userQueues[connection]['LogoutQueue_R'].put(data)
        elif header == "SEND_PRODUCTS":
            userQueues[connection]['ListProductsQueue_R'].put(data)
        elif header=="GET_ONLINE":
            userQueues[connection]['getOnlineQueue_R'].put(data)
        elif header=="SEND_CHAT":
            userQueues[connection]['sendChatQueue_R'].put(data)
        elif header=="RECV_CHAT":
            userQueues[connection]['recvChatQueue_R'].put(data)
        elif header=="HNDLE_MSG":
            userQueues[connection]['handleMSGQueue_R'].put(data)
        elif header=="BUY":
            userQueues[connection]['buyQueue_R'].put(data)
        elif header=="viewUProduct":
            userQueues[connection]['viewUserProductQueue_R'].put(data)
        elif header=="viewBuyers":
            userQueues[connection]['viewBuyersQueue_R'].put(data)
        elif header== "FIRST":
            userQueues[connection]["FirstQueue_R"].put(data)
            
#sendingQueue = queue()
def sendThread(connection):
    while True:
        #get the prefix
        header, data = userQueues[connection]["sendingQueue"].get()
        #tt = f"{header},{data.decode()}"
        print(header)
        print(data)
        #tt = f"{header},{data.decode()}"
        ptype = ""
        if isinstance(data, str):
            ptype = "str" 
            data = data.encode()
        else:
            ptype = "other"
            
        # if not isinstance(data, bytes):
        #     data = data.encode()
        #     print("encoded")
        
        delimiter = b"BRK"
        ending = b"<END>"
        message = header.encode() + delimiter + ptype.encode() + delimiter + data + ending
        
        connection.sendall(message)
        print("sent")
        # header, data = userqu
        # header = userQueues[connection]['sendingQueue'].get()[0]
        # connection.send(header.encode('utf-8'))  # Send the header first
        # #connection.recv(1024)  # Wait for the server to acknowledge the header
        # data = userQueues[connection]['sendingQueue'].get()[1]
        # connection.sendall(data) 

def receiveImageFile(connection):
    f = open("Image", "wb")
    fileData = b""
    while True:
        if fileData[-5:] == b"<END>":
            break
        data=userQueues[connection]['imageProductQueue_R'].get()
        #data = connection.recv(1024)
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
    header = "AUTH"
    global STOP_TIMER_AND_RESET, seconds, LOGIN_COOLDOWN
    #Get username and password
    while True:
        #Get LOGIN/REGISTER input
        print("wait bro")
        option = userQueues[connection]['authQueue_R'].get()
        #option = connection.recv(1024).decode('utf-8')
        print("Option: ", option)
        print("i got option")
        if option == "LOGIN":
            header = "LOGIN"
            counter = 0
            print("i went inside login")
            while counter < 3:
                print("shuuuuuuuu")
                username, password = userQueues[connection]['loginQueue_R'].get().split()
                print("")
                print("bahabhjasahjsajahk")
                #username, password = connection.recv(1024).decode('utf-8').split()
                
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
                        userQueues[connection]['sendingQueue'].put((header, "CORRECT"))
                        #connection.sendall("CORRECT".encode('utf-8'))
                        STOP_TIMER_AND_RESET = True
                        return username
                    else: #Invalid Password
                        counter += 1
                        userQueues[connection]['sendingQueue'].put((header, "INVALID_INFO"))
                        #connection.send("INVALID_INFO".encode('utf-8'))
                        #raise sqlite3.IntegrityError
                except sqlite3.IntegrityError:
                    counter += 1
                    userQueues[connection]['sendingQueue'].put((header, "INVALID_INFO"))
                    #connection.send("INVALID_INFO".encode('utf-8'))
                    print("No user with that username exists")
                    

                    
                    
        elif option =="REGISTER":
            header = "REGISTER"
            try:
            # Register then logs you in
                name, email, username, password = userQueues[connection]['registerQueue_R'].get().split(",")                
                #name, email, username, password = connection.recv(1024).decode('utf-8').split(",")
                print(name)
                print(email)
                print(username)
                print(password)
                cursor.execute("INSERT INTO Users values(?, ?, ?, ?)", (name.lower(), email.lower(), username.lower(), password))
                db.commit()
                userQueues[connection]['sendingQueue'].put((header, "ACCOUNT_CREATED"))
                #connection.sendall("ACCOUNT_CREATED".encode('utf-8'))
                
                
                
                clientIP, clientPort = userQueues[connection]['registerQueue_R'].get().split() #connection.recv(1024).decode('utf-8').split()
                # setOnline(username, clientIP, clientPort, cursor, db)
                
                return username
            except sqlite3.IntegrityError:
                print("Account already exists. Duplicate detected.")
                userQueues[connection]['sendingQueue'].put((header, "ACCOUNT_ALREADY_EXISTS"))
                #connection.sendall("ACCOUNT_ALREADY_EXISTS".encode('utf-8'))
        elif option == "EXIT":
            return -1
        
    
#TODO CONVERT THIS 

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
    header= "SEND_PRODUCTS"
    cursor = db.cursor()
    ##SEND AS JSONN 
    # cuz when we mae gui, we cant use pretty tables sl we need to be 
    # ready to read the file
  
    
    cursor.execute("SELECT * FROM Products")
    productsByUser = cursor.fetchall()
    userQueues[connection]['sendingQueue'].put((header, str(len(productsByUser))))
    #connection.sendall(str(len(productsByUser)).encode('utf-8'))
    response = userQueues[connection]['ListProductsQueue_R'].get()
    #response = connection.recv(1024).decode('utf-8')
    print(response)
    for i in range(len(productsByUser)):
        userQueues[connection]['sendingQueue'].put((header, pickle.dumps(productsByUser[i])))
        #connection.sendall(pickle.dumps(productsByUser[i]))
        userQueues[connection]['ListProductsQueue_R'].get()
        #connection.recv(1024)
    # t1 = cursor.fetchall()
    # file1.write(t1)
    # file1.close()
    # file2 = open("ServerFiles/toBePrinted", 'rb')
    # for lines in file2:
    #     connection.sendall(lines)

#"CREATE TABLE if not exists Online(username TEXT, ip_address TEXT, port INT, FOREIGN KEY(username) REFERENCES Users(username))") 

def sendUsersProducts(connection, db):
    header = "viewUProduct"
    cursor = db.cursor()
    userQueues[connection]['sendingQueue'].put((header, "Start"))
    #connection.sendall("Function of sending users products now open".encode('utf-8'))
    username = userQueues[connection]['viewUserProductQueue_R'].get()
    #username = connection.recv(1024).decode('utf-8')
    cursor.execute("SELECT product_name, price, desc FROM Products WHERE username = ?", (username,))
    usersProducts = cursor.fetchall()
    
    userQueues[connection]['sendingQueue'].put((header, str(len(usersProducts))))
    #connection.sendall(str(len(usersProducts)).encode('utf-8'))
    if(len(usersProducts) == 0):
        return
    for i in range(len(usersProducts)):
        userQueues[connection]['sendingQueue'].put((header, pickle.dumps(usersProducts)))
        #connection.sendall(pickle.dumps(usersProducts[i]))
        userQueues[connection]['viewUserProductQueue_R'].get()
        #connection.recv(1024)
    
OnlineUserConnections = {}
incomingQueues = {}


def sendOnlineUsers(connection, cursor):
    #cursor.execute("SELECT username FROM Online WHERE in_chat=true")
    #onlineUsers = cursor.fetchall()
    #print("BEFORE LOL")
    onlineUsers= []
    for users in OnlineUserConnections:
        onlineUsers.append(users)
    userQueues[connection]['sendingQueue'].put(("GET_ONLINE", pickle.dumps(onlineUsers)))
    #connection.sendall(pickle.dumps(onlineUsers))
    #print("LOLLL")
    # for i in range(len(onlineUsers)):
    #     connection.sendall(pickle.dumps(onlineUsers[i]))
    #connection.sendall("<END>".encode('uf-8'))


#client 1 sends to server
#server stores data in database
#client 2 receives the data and prints it from the database


def buyProducts(username, connection, db):
    header = "BUY"
    db = sqlite3.connect('db.AUBoutique')
    cursor = db.cursor()
    while True:
        cursor.execute("SELECT * FROM Products")
        prods = cursor.fetchall()
        good = False
        if not prods:
            userQueues[connection]['sendingQueue'].put((header, "No Products"))
            #connection.send("There are no products on the market.".encode('utf-8'))
            break
        for i in range(len(prods)):
            if prods[i][0] != username:
                  good = True
        if good == False:
            userQueues[connection]['sendingQueue'].put((header, "No products for sale."))
            #connection.send("All the products on the market are your own. You cannot buy at this time.".encode('utf-8'))
            break
        userQueues[connection]['sendingQueue'].put((header, "22"))
        #connection.sendall("22".encode('utf-8'))
        product = userQueues[connection]['buyQueue_R'].get()
        #product = connection.recv(1024).decode('utf-8')
        
        cursor.execute("SELECT username, price FROM Products WHERE product_name = ?", (product, ))
        data = cursor.fetchall()
        if not data:
            userQueues[connection]['sendingQueue'].put((header, "Not for Sale"))
            #connection.send("The entered product is not up for sale. Please try again.".encode('utf-8'))
            continue
        print(data)
        if (data[0][0] != username):
            userQueues[connection]['sendingQueue'].put((header, "Received"))
            #connection.sendall("Product name received".encode('utf-8'))
        else:
            userQueues[connection]['sendingQueue'].put((header, "You cannot purchase your own products."))
            #connection.send("You cannot purchase your own products. Please choose another product to buy.".encode('utf-8'))
            continue
        cursor.execute("DELETE FROM Products WHERE product_name = ?", (product,))
        db.commit()
        cursor.execute("INSERT INTO Purchases values(?,?,?,?)", (data[0][0], username, product, data[0][1]))
        db.commit()
        userQueues[connection]['buyQueue_R'].get()
        #connection.recv(1024)
        userQueues[connection]['sendingQueue'].put((header, "t"))
        #connection.sendall("t".encode('utf-8'))
        break
        
inChatOf = {}


#make it a queue 
def sendChat(username,target, connection):
    header = "RECV_CHAT"
    while True:
        messageToSend = incomingQueues[username].get()
        if messageToSend.lower() == "exit": 
            userQueues[connection]['sendingQueue'].put((header, "EXIT_CHAT"))
            #connection.sendall("EXIT_CHAT".encode('utf-8'))
            #inChatOf[target] = ""  
            inChatOf[username] = ""  
            break
        userQueues[connection]['sendingQueue'].put((header, messageToSend))
        #connection.sendall(messageToSend.encode('utf-8'))
        

def receiveChat(username,target, connection, db):
    #header = "SEND_CHAT"
    db = sqlite3.connect('db.AUBoutique')
    cursor = db.cursor()
    #connection.send("0".encode('utf-8'))
    while True:
        messageToSend = userQueues[connection]['recvChatQueue_R'].get()
        #messageToSend = connection.recv(1024).decode('utf-8')

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
        messageToSendLater = userQueues[connection]['recvChatQueue_R'].get()
        #messageToSendLater = connection.recv(1024).decode('utf-8')
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
    header = "HNDLE_MSG"
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
            
        option = userQueues[connection]['handleMSGQueue_R'].get()
        #option = connection.recv(1024).decode('utf-8')
        
        
        #connection.send("OK".encode('utf-8'))
        #response = connection.recv(1024).decode('utf-8')
        if option == "EXIT":
            break
        elif option == "INITIATE_NEW_CHAT":
            #start a new chat with a user and thats it
            userQueues[connection]['sendingQueue'].put((header, "OK"))
            #connection.send("OK".encode('utf-8'))
            target = userQueues[connection]['handleMSGQueue_R'].get()
            #target = connection.recv(1024).decode('utf-8')
            
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
            userQueues[connection]['sendingQueue'].put((header, "OK"))
            #connection.send("OK".encode('utf-8'))
            # if u open a chat,
            target = userQueues[connection]['handleMSGQueue_R'].get()
            #target = connection.recv(1024).decode('utf-8')
            #target hon is the username you want to open chat with
            inChatOf[target] = username    

            cursor.execute("SELECT message FROM Messages WHERE source=? AND destination=?", (target, username))
            messages = cursor.fetchall()
            # if not messages:
            #     connection.send("NO_SUCH_USER".encode('utf-8'))
            # else:
            #connection.send("SUCCESS".encode('utf-8'))
            #connection.recv(1024)
            userQueues[connection]['sendingQueue'].put((header, f"{len(messages)}"))
            #connection.send(f"{len(messages)}".encode('utf-8'))
            userQueues[connection]['handleMSGQueue_R'].get()
            #connection.recv(1024)
            print("AMOUNT OF MSGS: " + str(len(messages)))
            print(messages)
            for i in range(len(messages)):
                userQueues[connection]['sendingQueue'].put((header, messages[i][0]))
                #connection.send(messages[i][0].encode('utf-8'))
                userQueues[connection]['handleMSGQueue_R'].get()
                #connection.recv(1024)
            
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
     userQueues[connection]['sendingQueue'].put(("LOG_OUT", "LOGOUT_SUCCESS"))
     #connection.sendall("LOGOUT_SUCCESS".encode('utf-8'))
           
#Handle add product
def add_product(connection, username,cursor,  db):
    header = "ADD_PRODUCT"
    userQueues[connection]['sendingQueue'].put((header, "opened"))
    #connection.sendall("Opened add products now.".encode('utf-8'))
    while True:
            product_name, price, description, filename = userQueues[connection]['addProductQueue_R'].get().split(",") 
            # product_name, price, description, filename = connection.recv(1024).decode('utf-8').split(",")
            print(product_name, price, description)
            print("testing0")
            # PRICE IS INTEGER, FIX IT LATER
            price = int(price)
            #cursor.execute("INSERT INTO Products VALUES(?, ?, ?, ?, ?)", (username, product_name, price, description, filename))
            cursor.execute("""
                INSERT INTO Products (username, product_name, price, desc, filename)
                VALUES (?, ?, ?, ?, ?)
            """, (username, product_name, price, description, filename))
            print("testing1")
            db.commit()
            print("testing2")
            cursor.execute("SELECT * FROM Products WHERE product_name = ?", (product_name,))
            print(cursor.fetchall())
            print("testing3")
            # Fetch all results
            #sendProducts(connection, db)
            userQueues[connection]['sendingQueue'].put((header, "PRODUCT_ADDED"))
            #connection.sendall("PRODUCT_ADDED".encode('utf-8'))
            break

        #except Exception as e:
            #connection.sendall("ERROR: Cannot ADD product".encode('utf-8'))

def view_buyers(connection, username, db):
    header = "viewBuyers"
    db = sqlite3.connect('db.AUBoutique')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Purchases WHERE owner=?", (username,))
    list = cursor.fetchall()
    

    n = (str) (len(list))
    userQueues[connection]['sendingQueue'].put((header, n))
    #connection.send(n.encode('utf-8'))
    userQueues[connection]['viewBuyersQueue_R'].get()
    #connection.recv(1024)
    for i in range (len(list)):
        userQueues[connection]['sendingQueue'].put((header, pickle.dumps(list[i])))
        #connection.sendall(pickle.dumps(list[i]))
        userQueues[connection]['viewBuyersQueue_R'].get()
        #connection.recv(1024)
        
     


def handle_client(connection, address):
    
    theQueues = {
        'registerQueue_R': queue.Queue(),
        'loginQueue_R': queue.Queue(),
        'authQueue_R' : queue.Queue(),
        'addProductQueue_R' : queue.Queue(),
        'imageProductQueue_R': queue.Queue(),
        'LogoutQueue_R':queue.Queue(), # LOG_OUT
        'ListProductsQueue_R': queue.Queue(), # SEND_PRODUCTS
        'getOnlineQueue_R': queue.Queue(), # GET_ONLINE
        'sendChatQueue_R': queue.Queue(), # SEND_CHAT
        'recvChatQueue_R':queue.Queue(), # RECV_CHAT
        'handleMSGQueue_R': queue.Queue(), # HNDLE_MSG
        'buyQueue_R' : queue.Queue(), # BUY
        'viewUserProductQueue_R': queue.Queue(), #viewUProduct
        'viewBuyersQueue_R' : queue.Queue(), # viewBuyers
        'sendingQueue':queue.Queue(),
        'FirstQueue_R': queue.Queue()
    }
    
    userQueues[connection] = theQueues
    
    receivingThread = threading.Thread(target=receiveThread, args=(connection,))
    receivingThread.start()
    sendingThread = threading.Thread(target=sendThread, args=(connection,))
    sendingThread.start()
    
    
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
            
            #option = input("shu baddak red\n")
            option = userQueues[connection]["FirstQueue_R"].get()
            #option = connection.recv(1024).decode('utf-8')
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
    