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
prtnm = 9999
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((socket.gethostbyname(socket.gethostname()), prtnm))

db = sqlite3.connect('db.AUBoutique')
db.execute("PRAGMA foreign_keys=on")
cursor = db.cursor()







cursor.execute("CREATE TABLE if not exists Users (name TEXT, mail TEXT UNIQUE, username TEXT PRIMARY KEY UNIQUE, password TEXT, balance REAL, currency TEXT)") #name, email address, username, and password.
db.commit()

cursor.execute("CREATE TABLE if not exists Products(username TEXT, product_name TEXT, quantity INT, avgRating REAL DEFAULT 0, numberofRatings INT DEFAULT 0, price REAL DEFAULT 1, currency TEXT, desc TEXT, filename TEXT, status INT, FOREIGN KEY(username) REFERENCES Users(username))") 
db.commit()

cursor.execute("CREATE TABLE if not exists Messages(source TEXT, destination TEXT, message TEXT, FOREIGN KEY(source) REFERENCES Users(username))") 
db.commit()


cursor.execute("CREATE TABLE if not exists Purchases(owner TEXT, buyer TEXT, product TEXT, price INT, FOREIGN KEY(owner) REFERENCES Users(username),  FOREIGN KEY(buyer) REFERENCES Users(username))") 
db.commit()
Purchases = []

db.commit()


cursor.execute("SELECT username, password FROM USERS")
all_users = cursor.fetchall()
print(all_users)

def computeAvgRating(owner, product, userRating, cursor, db):
    cursor.execute("SELECT avgRating, numberofRatings FROM Products WHERE product_name=? AND username=?", (product, owner))
    oldAvgRating, oldN = cursor.fetchone()
    newAvg = (oldAvgRating*oldN + userRating)/(oldN+1)
    cursor.execute("UPDATE Products SET avgRating=?, numberOfRatings=? WHERE product_name=? AND username=?", (newAvg, oldN+1, product, owner))
    
    db.commit()
    
def showRating(owner, product, cursor):
    cursor.execute("SELECT avgRating FROM Products WHERE product_name=? AND username=?", (product, owner))
    rating = cursor.fetchone()
    return rating


userQueues = {}

def receiveThread(connection):
    ending = b"<END>"
    delimiter = b"BRK"
    remaining = b""
    try:
        count = 0
        while True:
                        
            remaining += connection.recv(1024)
                    
            while remaining:

                # Using split and handling cases where the result has one element or two
                split_result = remaining.split(ending, 1)
                
                if len(split_result) == 1: #if there was no ending
                    break
                # If split_result has more than one part, unpack it
                elif len(split_result) == 2:
                    receive, remaining = split_result
            
                header, ptype, data = receive.split(delimiter, 2)
                header = header.decode('utf-8')
                ptype = ptype.decode('utf-8')

                if ptype == "str":
                    data=data.decode('utf-8')
                elif ptype == "json":
                    data = data.decode()
                    data = json.loads(data)
                
                if header == "MSG":
                    userQueues[connection]['messageQueue_R'].put(data)
                elif header == "REGISTER":
                    userQueues[connection]['registerQueue_R'].put(data)
                elif header == "LOGIN":
                    userQueues[connection]['loginQueue_R'].put(data)
                elif header == "AUTH":
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
                elif header== "SET_NEW_BALANCE":
                    userQueues[connection]['setNewProductQueue_R'].put(data)
                elif header == "GET_USER_CURRENCY":
                    userQueues[connection]['getUserCurrencyQueue_R'].put(data)
                elif header=="IS_ONLINE":
                    userQueues[connection]['isOnlineQueue_R'].put(data)
    except Exception as e:
        print(e)
        print("Connection was closed.")
      
#sendingQueue = queue()
def sendThread(connection):
    while True:
        header, data = userQueues[connection]["sendingQueue"].get()
        ptype = ""
        if isinstance(data, str):
            ptype = "str" 
            data = data.encode()
        elif isinstance(data, dict):
            ptype = "json"
            data = json.dumps(data)
            data = data.encode()
        else:
            ptype = "other"
            
        
        delimiter = b"BRK"
        ending = b"<END>"
        message = header.encode() + delimiter + ptype.encode() + delimiter + data + ending
        
        connection.sendall(message)

    

def getAllUsers(cursor):
    cursor.execute("SELECT username FROM Users")
    userslist = cursor.fetchall()
    userQueues[connection]['getOnlineQueue_R'].put(json.dumps(userslist))
    

# accountTries = {}
# def resetTries(username):
#     del accountTries[username]
    
# def incrementTries(username):
#     accountTries[username]+=1

# LOGIN_COOLDOWN = 15

# STOP_TIMER_AND_RESET = False
# seconds = 0
# def Timer (username):
#     global seconds, STOP_TIMER_AND_RESET, LOGIN_COOLDOWN
#     print("STARTED TIME FOR ", username)
#     seconds = LOGIN_COOLDOWN
#     while seconds > 0:
#         if STOP_TIMER_AND_RESET:
#             STOP_TIMER_AND_RESET = False
#             break
#         time.sleep(1)
#         seconds-=1
#     resetTries(username)
    
def getUnsentMSGs(username, connection, header, cursor):
    db2 = sqlite3.connect('db.AUBoutique')
    cursor = db2.cursor()
    cursor.execute("SELECT source, message FROM Messages WHERE destination=?", (username,))
    messages = cursor.fetchall() 
    userQueues[connection]['sendingQueue'].put((header, str(len(messages))))
    if len(messages)>0:
        for msg in messages:
            info = f"{msg[0]},{msg[1]}"
            print(info)
            userQueues[connection]['sendingQueue'].put((header, info))
            cursor.execute("DELETE FROM Messages WHERE destination=?", (username,))
            db2.commit()
        
    
def authentication(connection, address, cursor, db):
    header = "AUTH"
    global STOP_TIMER_AND_RESET, seconds, LOGIN_COOLDOWN
    option = userQueues[connection]['authQueue_R'].get()

    if option == "LOGIN":
        header = "LOGIN"
        counter = 0
        while counter < 3:
            username, password = userQueues[connection]['loginQueue_R'].get().split()

            
            try:      
                cursor.execute("SELECT password FROM Users WHERE username=? ", (username.lower(),))
                targetPassword = cursor.fetchall() #check that this is not rendered between parentheses.
                if not targetPassword:
                    raise sqlite3.IntegrityError
                else:
                    targetPassword = targetPassword[0][0]        
                
                
                if  password == targetPassword:
                    userQueues[connection]['sendingQueue'].put((header, "CORRECT"))
                    clientIP, clientPort = userQueues[connection]['loginQueue_R'].get().split() #connection.recv(1024).decode('utf-8').split()

                    OnlineUserConnections[username] = (connection, clientIP, clientPort)
                    
                    getUnsentMSGs(username, connection, header, cursor)
                    STOP_TIMER_AND_RESET = True
                    return username
                else: #Invalid Password
                    counter += 1
                    userQueues[connection]['sendingQueue'].put((header, "INVALID_INFO"))
                    return -1
            except sqlite3.IntegrityError:
                counter += 1
                userQueues[connection]['sendingQueue'].put((header, "INVALID_INFO"))
                print("No user with that username exists")
                return -1
                
    elif option =="REGISTER":
        header = "REGISTER"
        try:
        # Register then logs you in
            name, email, username, password = userQueues[connection]['registerQueue_R'].get().split(",")                
            print(name)
            print(email)
            print(username)
            print(password)
            
            cursor.execute("INSERT INTO Users values(?, ?, ?, ?, ?, ?)", (name.lower(), email.lower(), username.lower(), password, 20, "USD"))
            db.commit()
            
            userQueues[connection]['sendingQueue'].put((header, "ACCOUNT_CREATED"))
            clientIP, clientPort = userQueues[connection]['registerQueue_R'].get().split() 
            OnlineUserConnections[username] = (connection, clientIP, clientPort)
            
            return username
        except sqlite3.IntegrityError:
           
            print("Account already exists. Duplicate detected.")
            userQueues[connection]['sendingQueue'].put((header, "ACCOUNT_ALREADY_EXISTS"))
    elif option == "EXIT":
        return -1
        

        
    
import json
def sendMYProducts(username, connection, db):
    selected_currency = "USD"
    header= "SEND_PRODUCTS"
    db2 = sqlite3.connect('db.AUBoutique')
    cursor = db2.cursor()
    
    cursor.execute("SELECT * FROM Products WHERE username=?", (username,))
    productsByUser = cursor.fetchall()
    userQueues[connection]['sendingQueue'].put((header, str(len(productsByUser))))
    
    for i in range(len(productsByUser)):
        print(productsByUser[i])
        test = json.dumps(productsByUser[i])
        userQueues[connection]['sendingQueue'].put((header, test))
        
def sendProducts(connection, db):
    selected_currency = "USD"
    header= "SEND_PRODUCTS"
    db2 = sqlite3.connect('db.AUBoutique')
    cursor = db2.cursor()
    
    cursor.execute("SELECT * FROM Products WHERE status=1")
    productsByUser = cursor.fetchall()
    userQueues[connection]['sendingQueue'].put((header, str(len(productsByUser))))
    
    for i in range(len(productsByUser)):
        print(productsByUser[i])
        test = json.dumps(productsByUser[i])
        userQueues[connection]['sendingQueue'].put((header, test))


def sendPurchasedProducts(connection):
    selected_currency = "USD"
    header= "SEND_PRODUCTS"
    db2 = sqlite3.connect('db.AUBoutique')
    cursor = db2.cursor()
    
    username = userQueues[connection]['ListProductsQueue_R'].get()
    cursor.execute("SELECT product, owner FROM Purchases WHERE buyer=?", (username,))
    myPurchases = cursor.fetchall()
    

    userQueues[connection]['sendingQueue'].put((header, str(len(myPurchases))))
    for i in range(len(myPurchases)):
        userQueues[connection]['sendingQueue'].put((header, json.dumps(myPurchases[i])))

        

        
def sendBuyers(connection):
    selected_currency = "USD"
    header= "SEND_PRODUCTS"
    db2 = sqlite3.connect('db.AUBoutique')
    cursor = db2.cursor()
    

    username = userQueues[connection]['ListProductsQueue_R'].get()
    product_name = userQueues[connection]['ListProductsQueue_R'].get()
    cursor.execute("SELECT buyer FROM Purchases WHERE owner=? AND product=?", (username,product_name))
    buyers = cursor.fetchall()
    buyer_list = [row[0] for row in buyers]
    userQueues[connection]['sendingQueue'].put((header, json.dumps(buyer_list)))

def sendUsersProducts(connection, db):
    header = "viewUProduct"
    cursor = db.cursor()
    userQueues[connection]['sendingQueue'].put((header, "Start"))
    username = userQueues[connection]['viewUserProductQueue_R'].get()
    cursor.execute("SELECT product_name, price, desc FROM Products WHERE username = ?", (username,))
    usersProducts = cursor.fetchall()
    
    userQueues[connection]['sendingQueue'].put((header, str(len(usersProducts))))
    if(len(usersProducts) == 0):
        return
    for i in range(len(usersProducts)):
        userQueues[connection]['sendingQueue'].put((header, pickle.dumps(usersProducts)))
        userQueues[connection]['viewUserProductQueue_R'].get()
    
OnlineUserConnections = {}
incomingQueues = {}


def sendOnlineUsers(connection, cursor):
    onlineUsers= []
    for users in OnlineUserConnections:
        onlineUsers.append(users)
    userQueues[connection]['sendingQueue'].put(("GET_ONLINE", pickle.dumps(onlineUsers)))


def buyProducts(username, connection, db):
    header = "BUY"
    db = sqlite3.connect('db.AUBoutique')
    cursor = db.cursor()
    product = userQueues[connection]['buyQueue_R'].get()
    product_owner = userQueues[connection]['buyQueue_R'].get()
    cursor.execute("SELECT username, price, quantity FROM Products WHERE product_name = ? AND status=1 AND username=?", (product,product_owner))
    data = cursor.fetchone()
    if not data:  
        userQueues[connection]['sendingQueue'].put((header, "ERROR"))  
    else: 
        seller, price, quantity = data
        if (seller == username):
            userQueues[connection]['sendingQueue'].put((header, "OWN_PRODUCT"))
        else:
            userQueues[connection]['sendingQueue'].put((header, "CONT"))
            print(username)
            print("purchasing")
            cursor.execute("SELECT balance FROM Users WHERE username=?", (username,))
            balance = cursor.fetchone()
            if not balance:
                balance = 0
            else:
                balance = balance[0]
            if(balance < price):
                userQueues[connection]['sendingQueue'].put((header, "INSUFFICIENT_FUNDS"))
            else:
                if (quantity <= 0):
                    userQueues[connection]['sendingQueue'].put((header, "notOntheMarketAnymore"))
                else:
                    userQueues[connection]['sendingQueue'].put((header, "SUCCESS"))
                    quantity -=1
                    cursor.execute("UPDATE Products SET quantity=? WHERE product_name=? AND username=?", (quantity, product, seller))
                    db.commit()
                    cursor.execute("UPDATE Users SET balance=? WHERE username=?", (balance - price, username))
                    db.commit()
                    cursor.execute("INSERT INTO Purchases values(?,?,?,?)", (seller, username, product, price ))
                    db.commit()
                
            if (quantity <= 0):
                cursor.execute("UPDATE Products SET status=0 WHERE product_name=? AND username=?", (product, seller))
                db.commit()
            


        
inChatOf = {}


def handle_messaging(username, connection, db):
    header = "HNDLE_MSG"
    cursor = db.cursor()
    target = userQueues[connection]['handleMSGQueue_R'].get()
    info = f"{OnlineUserConnections[target][1]},{OnlineUserConnections[target][2]}"
    userQueues[connection]['sendingQueue'].put((header, info))


def logOutUser(connection, username, cursor, db):
     del OnlineUserConnections[username]
     userQueues[connection]['sendingQueue'].put(("LOG_OUT", "LOGOUT_SUCCESS"))
      

           
           
def receiveImageFile(connection):
    db=sqlite3.connect('db.AUBoutique')
    cursor=db.cursor()
    image_name = userQueues[connection]['imageProductQueue_R'].get()
    image_data = userQueues[connection]['imageProductQueue_R'].get()

    f = open("AUBoutique/BackEnd/ServerFiles/"+image_name, "wb")
    f.write(image_data)
    
    f.close()
    
def sendImageFile(connection):
    header = "IMG_PRODUCT"
    db=sqlite3.connect('db.AUBoutique')
    cursor = db.cursor()
    product_name = userQueues[connection]['imageProductQueue_R'].get()
    username = userQueues[connection]['imageProductQueue_R'].get()
    
    cursor.execute("SELECT filename FROM Products WHERE username=? AND product_name=?", (username, product_name))
    filepath = cursor.fetchone()[0]
    
    
    f = open(filepath, "rb")
    file_content = f.read()
    userQueues[connection]["sendingQueue"].put((header, file_content))

#Handle add product
def add_product(connection, username, cursor,  db):
    header = "ADD_PRODUCT"

    product_name, quantity, price, description, filepath, currency = userQueues[connection]['addProductQueue_R'].get().split(",") 
    
    file_name = os.path.basename(filepath)
    server_file_path = f"AUBoutique/BackEnd/ServerFiles/{file_name}"  
    print(product_name, price, description)
    price = float(price)
    quantity = int(quantity)
    status = 1
    cursor.execute("""
        INSERT INTO Products 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (username, product_name, quantity, 0, 0, price, currency, description, server_file_path, status))
    db.commit()

    userQueues[connection]['sendingQueue'].put((header, "PRODUCT_ADDED"))
    receiveImageFile(connection)

# def view_buyers(connection, username, db):
#     header = "viewBuyers"
#     db = sqlite3.connect('db.AUBoutique')
#     cursor = db.cursor()
#     cursor.execute("SELECT * FROM Purchases WHERE owner=?", (username,))
#     list = cursor.fetchall()
    

#     n = (str) (len(list))
#     userQueues[connection]['sendingQueue'].put((header, n))
#     #connection.send(n.encode('utf-8'))
#     userQueues[connection]['viewBuyersQueue_R'].get()
#     #connection.recv(1024)
#     for i in range (len(list)):
#         userQueues[connection]['sendingQueue'].put((header, pickle.dumps(list[i])))
#         #connection.sendall(pickle.dumps(list[i]))
#         userQueues[connection]['viewBuyersQueue_R'].get()
#         #connection.recv(1024)
        
def sendCurrentBalance(connection, cursor, username):
    db = sqlite3.connect('db.AUBoutique')
    cursor = db.cursor()
    cursor.execute("SELECT balance FROM Users WHERE username = ?", (username,))
    wallet1 = cursor.fetchall()
    print("Sending Current Balance")
    print(username)
    print(wallet1)
    if not wallet1:
        wallet1 = 0
    else:
        wallet1 = wallet1[0][0]
    
    userQueues[connection]["sendingQueue"].put(("GET_CURRENT_BALANCE", str(wallet1 )))

def setNewBalance(username):
    db = sqlite3.connect('db.AUBoutique')
    cursor = db.cursor()
    new_balance = userQueues[connection]["setNewProductQueue_R"].get()
    print("NEW BALANCE: ")
    print(new_balance)
    cursor.execute("UPDATE Users SET balance = ? WHERE username = ?", (float(new_balance), username))
    db.commit()
    userQueues[connection]["sendingQueue"].put(("GET_CURRENT_BALANCE", "OK"))
    

    
def sendUserCurrency(connection):
    username = userQueues[connection]['getUserCurrencyQueue_R'].get()
    db = sqlite3.connect('db.AUBoutique')
    cursor = db.cursor()
    print(username)
    cursor.execute("SELECT currency FROM Users WHERE username =? ", (username,))
    currency = cursor.fetchone()
    if not currency:
        currency = "USD"
    else:
        currency = currency[0]
    userQueues[connection]['sendingQueue'].put(("GET_USER_CURRENCY", currency))
    
def setUserCurrency(connection):
    username = userQueues[connection]['getUserCurrencyQueue_R'].get()
    currency = userQueues[connection]['getUserCurrencyQueue_R'].get()
    db = sqlite3.connect('db.AUBoutique')
    cursor = db.cursor()
    cursor.execute("UPDATE Users SET currency=? WHERE username=?", (currency, username))
    db.commit()

def isOnline(username, connection):
    db = sqlite3.connect('db.AUBoutique')
    cursor = db.cursor()
    target= userQueues[connection]["isOnlineQueue_R"].get()
    print("TARGET:")
    print(target)
    if target in OnlineUserConnections:
        userQueues[connection]['sendingQueue'].put(("IS_ONLINE", "ONLINE"))
    else:
        userQueues[connection]['sendingQueue'].put(("IS_ONLINE", "NOT_ONLINE"))
        receivedMsg = userQueues[connection]['isOnlineQueue_R'].get()
        cursor.execute("INSERT INTO Messages VALUES (?, ?, ?)", (username, target, receivedMsg))
        db.commit()

    
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
        'FirstQueue_R': queue.Queue(),
        'sendTargetContact_R' : queue.Queue(), #targetDetails
        'setNewProductQueue_R': queue.Queue(),
        'getUserCurrencyQueue_R': queue.Queue(),
        'isOnlineQueue_R': queue.Queue()
    }
    
    userQueues[connection] = theQueues
    
    receivingThread = threading.Thread(target=receiveThread, args=(connection,))
    receivingThread.start()
    sendingThread = threading.Thread(target=sendThread, args=(connection,))
    sendingThread.start()
    
    
    db = sqlite3.connect('db.AUBoutique')
    cursor = db.cursor()

    while True: 
        myUsername = authentication(connection, address, cursor, db) 
        if myUsername == -1:
            continue
        
        incomingQueues[myUsername]= Queue()
        
        
        while True:

            option = userQueues[connection]["FirstQueue_R"].get()
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
            # elif option == "VIEW_BUYERS":
            #     view_buyers(connection, username, db)
            # elif option == "VIEW_PICTURE":
            #     picture(connection, db)
            elif option =="LOG_OUT":
                logOutUser(connection, username, cursor, db)
                break
            elif option=="GETALLUSERS":
                getAllUsers(cursor)
            elif option == "GET_CURRENT_BALANCE":
                sendCurrentBalance(connection, cursor, username)
            elif option == "SET_NEW_BALANCE":
                print(username)
                setNewBalance(username)
            elif option == "GET_USER_CURRENCY":
                sendUserCurrency(connection)
            elif option == "SET_USER_CURRENCY":
                setUserCurrency(connection)
            elif option =="SEND_PRODUCT_IMAGE":
                sendImageFile(connection)
            elif option=="SEND_PURCHASED_PRODUCTS":
                sendPurchasedProducts(connection)
            elif option =="GET_BUYERS":
                sendBuyers(connection)
            elif option =="IS_ONLINE":
                isOnline(username, connection)
            elif option == "SEND_MY_PRODUCTS":
                sendMYProducts(username, connection, db)

   
server.listen()
while True:
    connection,address= server.accept()
    server_thread = threading.Thread(target=handle_client, args=(connection, address))
    server_thread.start()


