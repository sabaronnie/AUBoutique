import socket
import threading
import time
import os
import sys
import pickle
from datetime import date, timedelta
import curses
import sqlite3
import os
from PIL import Image
import io
import queue
import select
import requests
import json  
from .BackEndSignal import signals
from . import conversion
from .MSGNotification import notif


msgHistoryDB = sqlite3.connect("db.msgHistory")
cursor = msgHistoryDB.cursor()

cursor.execute("CREATE TABLE if not exists History(source TEXT, destination TEXT, message_type TEXT, content BLOB)") 

cursor.execute("CREATE TABLE if not exists Unread(source TEXT, destination TEXT, message_type TEXT, content BLOB)") 
msgHistoryDB.commit()




try:
    dstprt = 9999
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((socket.gethostbyname(socket.gethostname()),dstprt))
except:
    print("CONNECTION FAILED ERROR")
    sys.exit(1)


clientIP = client.getsockname()[0]

P2PServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
P2PServer.bind((clientIP,0))

clientPort = P2PServer.getsockname()[1]


print("myIP: " + clientIP)
print("myPort: " + str(clientPort))


messageQueue_R = queue.Queue()
registerQueue_R = queue.Queue()
loginQueue_R = queue.Queue()
authQueue_R = queue.Queue()
addProductQueue_R = queue.Queue()
imageProductQueue_R = queue.Queue()
LogoutQueue_R = queue.Queue() # LOG_OUT
ListProductsQueue_R = queue.Queue() # SEND_PRODUCTS
getOnlineQueue_R = queue.Queue() # GET_ONLINE
sendChatQueue_R = queue.Queue() # SEND_CHAT
recvChatQueue_R = queue.Queue() # RECV_CHAT
handleMSGQueue_R = queue.Queue() # HNDLE_MSG
buyQueue_R = queue.Queue() # BUY
viewUserProductQueue_R = queue.Queue() #viewUProduct
viewBuyersQueue_R = queue.Queue() # viewBuyers
FirstQueue_R = queue.Queue() #First
constListenMSGQueue_R = queue.Queue()
sendTargetContact_R = queue.Queue() #targetDetails
getCurrentBalanceQueue_R = queue.Queue()
getUserCurrencyQueue_R = queue.Queue()
isOnlineQueue_R = queue.Queue()
#getAllUsers

socketList = []
socketList.append(client)
delimiter = b"BRK"
ending = b"<END>"
def receiveThread():
    global delimiter
    global ending
    buffer = b"" 
    remaining = b""
    count=0
    while True:
        
        remaining += client.recv(1024)
        
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
            ptype = ptype.decode()
            
            if ptype == "str":
                data=data.decode('utf-8')
            elif ptype == "json":
                data = data.decode()
                data = json.loads(data)

            
            print(header)
            if header == "MSG":
                messageQueue_R.put(data)
            elif header == "REGISTER":
                registerQueue_R.put(data)
            elif header == "LOGIN":
                loginQueue_R.put(data)
            elif header == "AUTH":
                authQueue_R.put(data)
            elif header == "ADD_PRODUCT":
                addProductQueue_R.put(data)
            elif header == "IMG_PRODUCT":
                imageProductQueue_R.put(data)
            elif header == "LOG_OUT":
                LogoutQueue_R.put(data)
            elif header == "SEND_PRODUCTS": 
                ListProductsQueue_R.put(data)
            elif header=="GET_ONLINE":
                getOnlineQueue_R.put(data)
            elif header=="SEND_CHAT":
                sendChatQueue_R.put(data)
            elif header=="RECV_CHAT":
                recvChatQueue_R.put(data)
            elif header=="HNDLE_MSG":
                handleMSGQueue_R.put(data)
            elif header=="BUY":
                buyQueue_R.put(data)
            elif header=="viewUProduct":
                viewUserProductQueue_R.put(data)
            elif header=="viewBuyers":
                viewBuyersQueue_R.put(data)
            elif header=="FIRST":
                FirstQueue_R.put(data)
            elif header == "ConstListenMSG": 
                constListenMSGQueue_R.put(data)
            elif header=="targetDetails":
                sendTargetContact_R.put(data)
            elif header=="GET_CURRENT_BALANCE":
                getCurrentBalanceQueue_R.put(data)
            elif header=="GET_USER_CURRENCY":
                getUserCurrencyQueue_R.put(data)
            elif header=="IS_ONLINE":
                isOnlineQueue_R.put(data)


sendingQueue = queue.Queue()
def sendThread():
    global delimiter
    global ending

    while True:
        #get the prefix
        header, data = sendingQueue.get()
        print(header)
        print(data)
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
        
        message = header.encode() + delimiter + ptype.encode() + delimiter + data + ending
        client.sendall(message)


receivingThread = threading.Thread(target=receiveThread, args=())
receivingThread.start()
sendingThread = threading.Thread(target=sendThread, args=())
sendingThread.start()

def sendImageFile(filename):
    while True:
        file1 = open(filename, "rb")
        
        for line in file1:
            client.sendall(line)
        client.sendall(b"END")



invalidUserPassword = False
           
           
globalUsername = ""      
def getTheUsername():
    return globalUsername     
           
counter = 0
def Login(username, password): #username, password
    global globalUsername
    header = "LOGIN"
    global counter

    sendingQueue.put(("AUTH", "LOGIN"))
    sendingQueue.put((header, f"{username} {password}"))

    response = loginQueue_R.get()

    if response == "CORRECT":
        globalUsername = username
        msgListening = threading.Thread(target=constantlylistenforMessages, args=(username,))
        msgListening.start()    
        sendingQueue.put((header, f"{clientIP} {clientPort}"))
        
        offlinesize = int(loginQueue_R.get())
        if offlinesize > 0:
            for i in range(offlinesize):
                source, msg = loginQueue_R.get().split(",")
                cursor.execute("INSERT INTO Unread values(?, ?, ?, ?)", (source, username, "TEXT", msg))
                msgHistoryDB.commit()
        return (response,counter)
    elif response == "INVALID_INFO":
        counter +=1 
        return (response, 2-counter)
               
def Register(name, email, username, password):
    global globalUsername
    header = "REGISTER"
    sendingQueue.put(("AUTH", "REGISTER"))
    message = f"{name},{email},{username},{password}"
    sendingQueue.put((header, message))
    response = registerQueue_R.get()
    if response == "ACCOUNT_CREATED":
        globalUsername = username
        msgListening = threading.Thread(target=constantlylistenforMessages, args=(username,))
        msgListening.start()  
        sendingQueue.put((header, f"{clientIP} {clientPort}"))
        return "ACCOUNT_CREATED"
    elif response == "ACCOUNT_ALREADY_EXISTS":
        return "ACCOUNT_ALREADY_EXISTS"     
        

def authentication():
    header = "AUTH"
    print("Welcome to AUBoutique")
    LIMIT = 3
    while True:
        
        choice = 1
        if choice == 1:     
            sendingQueue.put((header, "LOGIN"))           
            response, username = Login(LIMIT).split()
            if response == "SIGNED_IN":
                return username
            else:
                continue
        elif choice == 2:
            sendingQueue.put((header, "REGISTER"))
            if Register() == "ACCOUNT_CREATED":
                return 0 
        elif choice == 3:
            sendingQueue.put((header, "EXIT"))
            return -1

  
def add_product(product_name, quantity, price, description, file_path, currency):
    header = "ADD_PRODUCT"
    sendingQueue.put(("FIRST", "ADD_PRODUCT"))
    try: 
        sendingQueue.put((header, f"{product_name},{quantity},{price},{description},{file_path},{currency}"))
        response = addProductQueue_R.get()
        if response == "PRODUCT_ADDED":
            sendProductImage(file_path)
            return product_name
        else: 
            print("There was an error in adding your product. Please try again.")
    except ValueError:
        print("ERROR: Please only enter a value greater than or equal to 1$.")
    

def getUserCurrency(username):
    sendingQueue.put(("FIRST", "GET_USER_CURRENCY"))
    sendingQueue.put(("GET_USER_CURRENCY", username))
    user_currency = getUserCurrencyQueue_R.get()
    return user_currency

def setUserCurrency(username, currency):
    sendingQueue.put(("FIRST", "SET_USER_CURRENCY"))
    sendingQueue.put(("GET_USER_CURRENCY", username))
    sendingQueue.put(("GET_USER_CURRENCY", currency))
    
def getProductImage(username, product_name):
    header = "IMG_PRODUCT"
    sendingQueue.put(("FIRST", "SEND_PRODUCT_IMAGE"))
    sendingQueue.put((header, product_name))
    sendingQueue.put((header, username))
    
    return imageProductQueue_R.get()


def sendProductImage(filepath):
    header = "IMG_PRODUCT"
    file_name = os.path.basename(filepath)
    sendingQueue.put((header,file_name))
    f = open(filepath, "rb")
    file_content = f.read()
    sendingQueue.put((header, file_content))
    f.close()
    
def LogOut(username):
    if username in active_sockets:
        del active_sockets[username]
    header = "LOG_OUT"
    sendingQueue.put(("FIRST", "LOG_OUT"))
    print("Logging out...")
    response = LogoutQueue_R.get()
    if response == "LOGOUT_SUCCESS":
        print("You have been successfully logged out.")
        return response
    else:
        print("Error logging out, please try again.")
        return "FAILED"
    
# def convert(changeThisCurrency,toThisCurrency,amount):
#     url = "https://api.currencybeacon.com/v1/convert"
#     params = {"from": changeThisCurrency,"to": toThisCurrency,"amount": amount}
#     api_key = "p9WCI0sOzsOma0mHAN3S0EGyH2LByTJY"
#     headers = {"Authorization": f"Bearer {api_key}"}
#     response = requests.get(url, headers=headers, params=params)
#     if response.status_code == 200:
#         data = response.json()
#         return data["response"]["value"]
#     else:
#         print("Error:", response.status_code, response.text)

def populateProductsArray(selected_currency="USD"):
    try:
        returnedArray = []
        header = "SEND_PRODUCTS"
        sendingQueue.put(("FIRST", "SEND_PRODUCTS"))
        n = int(ListProductsQueue_R.get())

        for i in range(n):
            temporary = ListProductsQueue_R.get()
            temporary = json.loads(temporary)
            product_currency = temporary[6]
            price = float(temporary[5])
            if product_currency != selected_currency:
                price = conversion.convert(product_currency, selected_currency, price)
            returnedArray.append(
                {
                    "owner": temporary[0],
                    "name": temporary[1],
                    "quantity": temporary[2],
                    "rating": temporary[3],
                    "numberOfRatings": temporary[4],
                    "price": price,
                    "description": temporary[7],
                    "filename": temporary[8],
                    "status": temporary[9],
                    "currency": selected_currency
                }
            )
        print(returnedArray)
        return returnedArray
    except Exception as e:
        # Catch all types of exceptions and print the error name and message
        print(f"An error occurred: {type(e).__name__}")
        print(f"Error message: {e}")
        
def purchasedProductsArray(username):
    try:
        returnedArray = []
        header = "SEND_PRODUCTS"
        sendingQueue.put(("FIRST", "SEND_PURCHASED_PRODUCTS"))
        sendingQueue.put((header, username))
        n = int(ListProductsQueue_R.get())
        for i in range(n):
            temporary = ListProductsQueue_R.get()
            temporary = json.loads(temporary)
            returnedArray.append(
                {
                    "owner": temporary[1],
                    "name": temporary[0],
                }
            )
        return returnedArray
    except Exception as e:
        # Catch all types of exceptions and print the error name and message
        print(f"An error occurred: {type(e).__name__}")
        print(f"Error message: {e}")
    
    
def getBuyers(username, product_name):
    header = "SEND_PRODUCTS"
    sendingQueue.put(("FIRST", "GET_BUYERS"))
        
    sendingQueue.put((header, username))
    sendingQueue.put((header, product_name))
    
    buyers = ListProductsQueue_R.get()
    buyers = json.loads(buyers)
    
    return buyers
   
def getCurrentBalance():
    sendingQueue.put(("FIRST", "GET_CURRENT_BALANCE"))
    current_balance = getCurrentBalanceQueue_R.get()
    return float(current_balance)

def setNewBalance(new_balance):
    sendingQueue.put(("FIRST", "SET_NEW_BALANCE"))
    sendingQueue.put(("SET_NEW_BALANCE", str(new_balance)))
    status = getCurrentBalanceQueue_R.get()
    return status
    
# def getOnlineUsers():
#     onlineUsers = getOnlineQueue_R.get()
#     #onlineUsers = client.recv(1024)
#     onlineUsers = pickle.loads(onlineUsers)
#     for i in range(1, len(onlineUsers)+1):
#         print(str(i) + "- " + onlineUsers[i-1])
        
# def getAllUsers():
#     sendingQueue.put(("FIRST", "GETALLUSERS"))
#     allUsers = getOnlineQueue_R.get()
#     print("test")
#     print("GOT ALL USERS")
#     #onlineUsers = client.recv(1024)
#     onlineUsers = json.loads(allUsers)
#     return onlineUsers
    
def getHistory(username, target):
    cursor.execute("SELECT source, destination, message_type, content FROM History WHERE destination = ? OR source = ?", (username, username))
    messages_list = cursor.fetchall()
    return messages_list
            
def getUnread(username, target):
    unread_messages = []
    cursor.execute("SELECT content FROM Unread WHERE source=? AND destination=?", (target, username))
    unread_messages = cursor.fetchall()
    size = len(unread_messages)
    unread_list = []
    if size > 0:
        for q in range(size):
            unread_list.append(unread_messages[q][0])
            print(f"{target}: {unread_messages[q][0]}") 
            cursor.execute("DELETE FROM Unread WHERE content=?", (unread_messages[q][0],))   
            cursor.execute("INSERT INTO History values(?,?,?, ?)", (target, username, "TEXT",unread_messages[q][0]))   
            msgHistoryDB.commit()   
            
    return unread_list


def formatImage(username, filename):
    header = "IMG"
    f = open(filename, "rb")
    payload = b""
    for line in f:
        paylod += line
        
    info = header.encode() + delimiter + username.encode() + delimiter + payload + ending
    return info


active_sockets = {}
def sendChatClient(username, target, msgtype, message):
    global ending
    global delimiter
    global socketList
    global inChat
    global msging
    
    header = "IS_ONLINE"
    msgHistoryDB = sqlite3.connect("db.msgHistory")
    cursor = msgHistoryDB.cursor()

    sendingQueue.put(("FIRST","IS_ONLINE"))
    sendingQueue.put(("IS_ONLINE", target))
    status = isOnlineQueue_R.get()
    print(status)
    if status == "ONLINE":
        msgSocket = ""
        if not target in active_sockets:
                msgSocket = handle_messaging(username, target)
                active_sockets[target] = msgSocket
        else:
            msgSocket = active_sockets[target]
            
        if msgtype == "TEXT":
            info = msgtype.encode() + delimiter + username.encode() + delimiter + f"{message}".encode() + ending
            msgSocket.send(info)
            
        if target and username and message:
            cursor.execute("INSERT INTO History values(?,?,?,?)", (username, target, msgtype, message))   
            msgHistoryDB.commit()
    elif status == "NOT_ONLINE":
        sendingQueue.put((header, message))
        cursor.execute("INSERT INTO History values(?,?,?,?)", (username, target, msgtype, message))   
        msgHistoryDB.commit()


receivedMSG = queue.Queue()

def popFromTheMSGQueue():
    global receivedMSG
    message = receivedMSG.get()
        
    return message

def receiveChatAVAILABLE(username, target, message, signals):
    global receivedMSG
    header = "SEND_CHAT"
    msgHistoryDB = sqlite3.connect("db.msgHistory")
    cursor = msgHistoryDB.cursor()

    response = message

    if username and target and response:
        cursor.execute("INSERT INTO History values(?,?,?, ?)", (username, target, "TEXT", response))   
        msgHistoryDB.commit()
        
    signals.new_message.emit(message)
    print(f"{target}: {response}")

inChat = {}

def addToInChat(target):
    inChat[target] = True
    
def checkIfIMinChatOF(target):
    if target in inChat:
        return True
    else:
        return False

def notification(username):
    print(username + " SENT YOU A MSG")

    
from PyQt5.QtCore import QObject, pyqtSignal

def constantlylistenforMessages(username):
    global socketList
    global inChat
    
    
    msgHistoryDB = sqlite3.connect('db.msgHistory')
    cursor = msgHistoryDB.cursor()

    P2PServer.listen()
    while True:
        connection, address = P2PServer.accept()
        receive = b""
        remaining = b""
        while True:

            if not remaining:
                remaining += connection.recv(1024)

            while remaining:
                split_result = remaining.split(ending, 1)

                if len(split_result) == 1: #if there was no ending
                    break
                # If split_result has more than one part, unpack it
                elif len(split_result) == 2:
                    receive, remaining = split_result

                msgtype, target, message = receive.split(delimiter, 2)
                msgtype = msgtype.decode('utf-8')
                target = target.decode()

                message=message.decode()

                if target in inChat:
                    receiveChatAVAILABLE(username, target, message, signals) #fix input
                else: #if not in chat
                    notif.new_message.emit(target)
                    cursor.execute("INSERT INTO Unread values(?, ?, ?, ?)", (username, target, msgtype, message))
                    msgHistoryDB.commit()

                #notification(target)
        



def getExistingChats(username):
    print("USERNAME: ", str(username))
    cursor.execute("SELECT DISTINCT destination FROM History WHERE source=?", (username,))
    listofUsers1 = [user[0] for user in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT source FROM History WHERE destination=? ", (username, ))
    listofUsers2 = [user[0] for user in cursor.fetchall()]
    
    merged_list = list(set(listofUsers1 + listofUsers2))
    return merged_list

# def getTargetIP(target):
#     targetIP, targetPort = sendTargetContact_R.get().split(",") 
#     targetPort = int(targetPort)
#     msgSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     msgSocket.connect((targetIP,targetPort))
#     return msgSocket

def handle_messaging(username, target):
    global inChat
    header = "HNDLE_MSG"
    sendingQueue.put(("FIRST", "MSG"))
    sendingQueue.put((header, target))
    targetIP, targetPort = handleMSGQueue_R.get().split(",")
    
    targetPort = int(targetPort)
    print(targetIP)
    print(targetPort)
    msgSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    msgSocket.connect((targetIP,targetPort))
    return msgSocket

    
def buyProducts(product_name, username):
    header = "BUY"
    sendingQueue.put(("FIRST", "BUY_PRODUCTS"))

    sendingQueue.put((header, product_name))
    sendingQueue.put((header, username))
    answer = buyQueue_R.get()

    if answer == "OWN_PRODUCT":
        return answer
    elif answer == "ERROR":
        return answer
    else:
        response = buyQueue_R.get()
        if response == "INSUFFICIENT_FUNDS":
            return response
        else:
            return "SUCCESS"

 


