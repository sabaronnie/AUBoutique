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


sys.path.append("modules") 

from prettytable import PrettyTable


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
            if count<15:
                #print(remaining)
                print("while remaining")
            count+=1

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
        print('inside login, fi meshkle hon')
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

  
def add_product(product_name, quantity, price, description, file_path):
    header = "ADD_PRODUCT"
    sendingQueue.put(("FIRST", "ADD_PRODUCT"))
    try: 
        currency = "USD"
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
    
def convert(changeThisCurrency,toThisCurrency,amount):
    url = "https://api.currencybeacon.com/v1/convert"
    params = {"from": changeThisCurrency,"to": toThisCurrency,"amount": amount}
    api_key = "p9WCI0sOzsOma0mHAN3S0EGyH2LByTJY"
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        return data["response"]["value"]
    else:
        print("Error:", response.status_code, response.text)

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
                price = convert(product_currency, selected_currency, price)
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
        
#kelshi u purchased
def purchasedProductsArray(username):
    try:
        returnedArray = []
        header = "SEND_PRODUCTS"
        sendingQueue.put(("FIRST", "SEND_PURCHASED_PRODUCTS"))
        sendingQueue.put((header, username))
        n = int(ListProductsQueue_R.get())
        print("n = ", n)
        for i in range(n):
            temporary = ListProductsQueue_R.get()
            
            print("TEMPORARY: " )
            print(temporary)
            temporary = json.loads(temporary)
            print("JSON")
            print(temporary)
              # Assuming currency is at index 
            returnedArray.append(
                {
                    "owner": temporary[1],
                    "name": temporary[0],
                }
            )
            print("done with appending at the array, now gonna print ")
        print(returnedArray)
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
    # try:
    #     returnedArray = []
    #     header = "SEND_PRODUCTS"
    #     sendingQueue.put(("FIRST", "SEND_MY_PRODUCTS"))
    #     sendingQueue.put((header, username))
    #     n = int(ListProductsQueue_R.get())
    #     for i in range(n):
    #         temporary = ListProductsQueue_R.get()
    #         print("TEMPORARY: " )
    #         print(temporary)
    #         temporary = json.loads(temporary)
    #         print("JSON")
    #         print(temporary)
    #         product_currency = temporary[6]  # Assuming currency is at index 9
    #         price = float(temporary[5])
    #         if product_currency != selected_currency:
    #             price = convert(product_currency, selected_currency, price)
    #         returnedArray.append(
    #             {
    #                 "owner": temporary[0],
    #                 "name": temporary[1],
    #                 "quantity": temporary[2],
    #                 "rating": temporary[3],
    #                 "numberOfRatings": temporary[4],
    #                 "price": price,
    #                 "description": temporary[7],
    #                 "filename": temporary[8],
    #                 "status": temporary[9],
    #                 "currency": selected_currency
    #             }
    #         )
    #     print(returnedArray)
    #     return returnedArray
    # except Exception as e:
    #     # Catch all types of exceptions and print the error name and message
    #     print(f"An error occurred: {type(e).__name__}")
    #     print(f"Error message: {e}")


# def list_products():
#     header = "SEND_PRODUCTS"
#     sendingQueue.put(("FIRST", "SEND_PRODUCTS"))
#     #client.sendall("SEND_PRODUCTS".encode('utf-8'))
#     n = int(ListProductsQueue_R.get())
#     #n = int(client.recv(1024).decode('utf-8'))
#     sendingQueue.put((header, "Received"))
#     #client.sendall("Received number of products".encode('utf-8'))
    
#     table = PrettyTable()
#     table.field_names = ["Username", "Product Name", "Price (in $)", "Description"]
#     for i in range(n):
#         temporary = ListProductsQueue_R.get()
#         #temporary = client.recv(1024)
#         sendingQueue.put((header, "OK"))
#         #client.sendall("OK".encode('utf-8'))
#         temporary = pickle.loads(temporary)
#         table.add_row([temporary[0], temporary[1], temporary[2], temporary[3]])
#     # Print the table
#     print(table)

def getCurrentBalance():
    sendingQueue.put(("FIRST", "GET_CURRENT_BALANCE"))
    current_balance = getCurrentBalanceQueue_R.get()
    return float(current_balance)

def setNewBalance(new_balance):
    sendingQueue.put(("FIRST", "SET_NEW_BALANCE"))
    sendingQueue.put(("SET_NEW_BALANCE", str(new_balance)))
    status = getCurrentBalanceQueue_R.get()
    return status
    

    
def getOnlineUsers():
    onlineUsers = getOnlineQueue_R.get()
    #onlineUsers = client.recv(1024)
    onlineUsers = pickle.loads(onlineUsers)
    for i in range(1, len(onlineUsers)+1):
        print(str(i) + "- " + onlineUsers[i-1])
        
def getAllUsers():
    sendingQueue.put(("FIRST", "GETALLUSERS"))
    #sendTargetContact_R
    print("test")
    allUsers = getOnlineQueue_R.get()
    print("test")
    print("GOT ALL USERS")
    #onlineUsers = client.recv(1024)
    onlineUsers = json.loads(allUsers)
    return onlineUsers
    
def msgGUI(USER_UNAVAILABLE):
    print(">>")
    #getOnlineUsers()
    print("Pick the user to message (or type 'exit' to cancel):")

    
    print()
    if USER_UNAVAILABLE:
        print("The user you previously selected is no longer available")
        return -1
    return 0

#LOCK IT
i = 3

#TODO; if other client crashed or closed, show on both sides

    

    # 1. Open a chat with someone new
    
    # Existing Chats:
    # 1. Farid
    # 2. Anthony

    #1 open a chat with someone specific
    # choose who this person is
    # if the person is not in chat, send w sayyev bel database implement old1 with receiver not in chat.
    
    #if the person is in the chat, do the chatting el usual li kena 3am naamelo through dictionaries. 
# def theserver():
#     P2PServer.listen()
#     while True:
#         connection, address = P2PServer.accept()
#         socketList.append(connection)

# def getAllUsers():
#     cursor.execute("SELECT username FROM Users")
#     userslist = cursor.fetchall()
#     return userslist
        
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
    
   # header = "ConstListenMSG"
    header = "IS_ONLINE"
    msgHistoryDB = sqlite3.connect("db.msgHistory")
    cursor = msgHistoryDB.cursor()

    sendingQueue.put(("FIRST","IS_ONLINE"))
    sendingQueue.put(("IS_ONLINE", target))
    print("khara 2")
    status = isOnlineQueue_R.get()
    print("khara 1")
    print(status)
    if status == "ONLINE":
        print("OK OK OK OK OK OKOK ")
        msgSocket = ""
        if not target in active_sockets:
                msgSocket = handle_messaging(username, target)
                active_sockets[target] = msgSocket
        else:
            msgSocket = active_sockets[target]
            
        if msgtype == "TEXT":
            print("ANA AAM BHAWEL EBAAT THIS NOW: ")
            info = msgtype.encode() + delimiter + username.encode() + delimiter + f"{message}".encode() + ending
        # elif msgtype =="IMG":
        #     info = formatImage(username, message)
            msgSocket.send(info)
            
        if target and username and message:
            cursor.execute("INSERT INTO History values(?,?,?,?)", (username, target, msgtype, message))   
            msgHistoryDB.commit()
    elif status == "NOT_ONLINE":
        #maa msgtype
        sendingQueue.put((header, message))


receivedMSG = queue.Queue()

def popFromTheMSGQueue():
    global receivedMSG
    message = receivedMSG.get()
        
    return message

# def addToMSGQueue():
#     global receivedMSG


def receiveChatAVAILABLE(username, target, message, signals):
    global receivedMSG
    header = "SEND_CHAT"
    print("OK FA RECEIVE CHAT WAS CALLED SHAWARMA")
    msgHistoryDB = sqlite3.connect("db.msgHistory")
    cursor = msgHistoryDB.cursor()
    #while True:
        #y, x = stdscr.getyx()
        #response = recvChatQueue_R.get()
    response = message
    #response = client.recv(1024).decode('utf-8')
    # stdscr.addstr(i, 0, "Enter: ")
    # if response == "EXIT_CHAT":
    #     print("User has left the chat.")
    #     return
    print("feeefoooofeeeeeeeefooooooo")
    if username and target and response:
        # print("AAM BHOT " + response + "IN MESSAGES apple")
        cursor.execute("INSERT INTO History values(?,?,?, ?)", (username, target, "TEXT", response))   
        msgHistoryDB.commit()
        
    signals.new_message.emit(message)
    #receivedMSG.put(message)
    print("THIS IS THE MESSAGE WE'RE MEANT TO RECEIVED")
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
    ##GUI BASED
    print(username + " SENT YOU A MSG")

# def setInChat(target):
#     inChat[target]=True
    

from PyQt5.QtCore import QObject, pyqtSignal

#if offlinec but then becomes online TODO
#operating in its own thread
def constantlylistenforMessages(username):
    global socketList
    global inChat
    
    
    msgHistoryDB = sqlite3.connect('db.msgHistory')
    cursor = msgHistoryDB.cursor()

    P2PServer.listen()
    while True:
        connection, address = P2PServer.accept()
        print("ana officially hon ya zabreyete")
        #socketList.append(connection)
        receive = b""
        remaining = b""
        #header.encode() + delimiter + f"{username}".encode() + delimiter + f"{message}".encode()
        count = 0
        while True:
            if count < 15:
                print(count)
                print("fetit aal while loop k?")
                print("REMAINING, BEFORE: ")
                print(remaining)
            if not remaining:
                remaining += connection.recv(1024)
                if count < 15:
                    print("REMAINING, NOW: ")
                    print(remaining)
            else:
                if count< 15:
                    print("The REMAINING")
                    print(remaining)
            
            count+=1

            while remaining:
                split_result = remaining.split(ending, 1)
                if count < 15:
                    print(split_result)
                    print("LENGTH: " + str(len(split_result)))
                if len(split_result) == 1: #if there was no ending
                    break
                # If split_result has more than one part, unpack it
                elif len(split_result) == 2:
                    receive, remaining = split_result
                    
                #Either TEXT or 
                print("lah ebke")
                msgtype, target, message = receive.split(delimiter, 2)
                msgtype = msgtype.decode('utf-8')
                target = target.decode()
                if count < 15:
                    print(msgtype)
                    print(target)
                    print(message)
                    print("BACKEND TARGET:  " + target)
                    
                #temp
                message=message.decode()
                if count < 15:
                    print("L MSG AAM BEBAAT: " + message)
            # else: 
            #target,msgToHandle = connection.recv(1024).decode().split(",") #constListenMSGQueue_R.get().split(",")
                # if message == "EXIT_CHAT":
                #     break
                if target in inChat:
                    print("IBNEEE, ANA IN CHAT OF TARGET")
                    #call send and receive
                    receiveChatAVAILABLE(username, target, message, signals) #fix input
                else: #if not in chat
                    print(username)
                    print(target)
                    print(message)
                    cursor.execute("INSERT INTO Unread values(?, ?, ?, ?)", (username, target, msgtype, message))
                    msgHistoryDB.commit()

                #notification(target)
        

msgHistoryDB = sqlite3.connect("db.msgHistory")
cursor = msgHistoryDB.cursor()

cursor.execute("CREATE TABLE if not exists History(source TEXT, destination TEXT, message_type TEXT, content BLOB)") 

cursor.execute("CREATE TABLE if not exists Unread(source TEXT, destination TEXT, message_type TEXT, content BLOB)") 
msgHistoryDB.commit()

cursor.execute("INSERT INTO History values(?,?,?,?)", ("ron", "farid", "TEXT", "zabzabrennnre"))
msgHistoryDB.commit()


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
    #print("CHECK THIS OUTG")
    print(targetIP)
    print(targetPort)
    msgSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    msgSocket.connect((targetIP,targetPort))
    return msgSocket
    #     inChat[target] = True
    #     sendChat = threading.Thread(target=sendChatClient, args=(targetIP, targetPort, history, size, unread_messages, username, target))
    #     sendChat.start()
    #     sendChat.join()
    #     #sendChatClient(targetIP, targetPort, history, size, unread_messages, username, target)
    # elif status=="NOT_ONLINE": #if not online, send msg to server until he gets online ok
    #     while True:
    #         msg = input("Enter your message: ")
    #         sendingQueue.put((header, msg))
    
def buyProducts(product_name, username):
    header = "BUY"
    sendingQueue.put(("FIRST", "BUY_PRODUCTS"))
    #client.send("BUY_PRODUCTS".encode('utf-8'))

    sendingQueue.put((header, product_name))
    sendingQueue.put((header, username))
    answer = buyQueue_R.get()
    #answer1 = client.recv(1024).decode('utf-8')

    if answer == "OWN_PRODUCT":
        return answer
    elif answer == "ERROR":
        return answer
    else:
        response = buyQueue_R.get()
        if response == "INSUFFICIENT_FUNDS":
            return response
        else:
            #notification, buy was succesful
            return "SUCCESS"

 
    # if NoProds:
    #     return "No product bought."
    # return product_name


def viewUsersProducts():
    header = "viewUProduct"
    sendingQueue.put(("FIRST", "VIEW_USERS_PRODUCTS"))
    #client.sendall("VIEW_USERS_PRODUCTS".encode('utf-8'))
    viewUserProductQueue_R.get()
    #client.recv(1024)
    username = input("Enter the username of the user whose products you want to see: ")
    sendingQueue.put((header, username))
    #client.sendall(username.encode('utf-8'))
    t = viewUserProductQueue_R.get()
    print(t)
    n1 = int(t)
    #n1 = (int) (client.recv(1024).decode('utf-8'))
    table = PrettyTable()
    table.field_names = ["Product Name", "Price (in $)", "Description"]
    for i in range(n1):
        temporary = viewUserProductQueue_R.get()
        #temporary = client.recv(1024)
        temporary = pickle.loads(temporary)
        sendingQueue.put((header, "OK"))
        #client.sendall("OK".encode('utf-8'))
        table.add_row([temporary[0], temporary[1], temporary[2]])
    
    print(f"Viewing {username}'s products: ")   
    print(table)

     
# notifyMSG = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# notifyMSG.connect((socket.gethostbyname(socket.gethostname()),9999))
   
   
def view_buyers():
    header = "viewBuyers"
    sendingQueue.put(("FIRST", "VIEW_BUYERS"))
    #client.sendall("VIEW_BUYERS".encode('utf-8'))
    n = int(viewBuyersQueue_R.get())
    #n = int(client.recv(1024).decode('utf-8'))
    sendingQueue.put((header, "received"))
    #client.send("n succesfully received.".encode('utf-8'))
    if n == 0:
        return True
    i = 0
    table = PrettyTable()
    
    table.field_names = ["Product Name", "Buyer", "Price (in $)"]
    for i in range (n):
        viewBuyersQueue_R.get()
        #temporary = client.recv(1024)
        sendingQueue.put((header, "OK"))
        #client.sendall("OK".encode('utf-8'))
        temporary = pickle.loads(temporary)
        table.add_row([temporary[2], temporary[1], temporary[3]])
    print("Those are the buyers of your products: \n")
    print(table)
    return False
    



#TODO:
#This should be executed bl gui as soon as you login
    

# def handle_client():
#     #notLoggedOut = True
#     while True:
#         username = authentication()
#         if username == -1:
#             counter = 3
#             
#             while counter > 0:
#                 print("Exiting AUBoutique", end= "", flush=True)    
#                 time.sleep(0.4)
#                 print(".", end="", flush=True)
#                 time.sleep(0.4)
#                 print(".", end="", flush=True)
#                 time.sleep(0.4)
#                 print(".", end="", flush=True)
#                 time.sleep(0.4)
#                 
#                 counter -= 1
#             print("Hope you enjoyed!")
#             time.sleep(1)
#             break
#         else:
#             msgListening = threading.Thread(target=constantlylistenforMessages, args=(username,))
#             msgListening.start()
            
#             # thesrver = threading.Thread(target=theserver, args=())
#             # thesrver.start()
#             Sign_In_Animation()
#             #Now get list of products
#             #Display list of options to client 
#             f = open("BackEnd/temp.txt")
#             lol = f.read()
#             print(lol)
#             boughtProduct = False
#             addedProduct = False
#             viewAllUsers = False
#             noBuyers = False
#             viewBuyers = False
#             product = ""
#             while True:
#                 if viewAllUsers == False and not viewBuyers:
#                     print("calling to list all products")
#                     list_products()
#                 viewAllUsers = False
#                 if viewBuyers:
#                     viewBuyers = False
#                 if addedProduct:
#                     print(f"{product} successfully added")
#                     addedProduct=False
#                 if boughtProduct:
#                     
#                     counter11 = 3
#                     while counter11 > 0:
#                         print("Waiting for confirmation", end= "", flush=True)    
#                         time.sleep(0.3)
#                         print(".", end="", flush=True)
#                         time.sleep(0.3)
#                         print(".", end="", flush=True)
#                         time.sleep(0.3)
#                         print(".", end="", flush=True)
#                         time.sleep(0.3)
#                         
#                         counter11 -= 1
#                     currentdate = date.today()
#                     currentdate = currentdate + timedelta(days = 7)
#                     currentdate = (str) (currentdate) 
#                     year, month, day = currentdate.split("-")
#                     flipped_date = f"{day}-{month}-{year}"
#                     currentdate = flipped_date
#                     message = "\n\nYour " +  product +  " will be available at the AUB Post Office in one week on " + str(currentdate)
#                     message += "\nAUB Post Office Working Hours: 8:00 a.m. till 4:00 p.m.\n\n" 
#                     print(message)
#                     boughtProduct=False
#                 if noBuyers == True:
#                     print("\nThere are no buyers for your products yet.\n")
#                     noBuyers = False
#                 print("<<")
#                 print("1. Add a Product")
#                 print("2. View Someone's Products")
#                 print("3. Send Message")
#                 print("4. Buy a Product")
#                 print("5. View buyers of your products")
#                 print("6. View the picture of a specific product")
#                 print("7. Log Out")
                
#                 choice = input("Enter your choice: ")
                
#                 if choice == '1':
#                     product = add_product()
#                     addedProduct = True
#                 elif choice == '2':
#                     viewUsersProducts()
#                     viewAllUsers = True
#                 elif choice == '3':
#                     handle_messaging(username)
#                 elif choice == '4':
#                     product = buyProducts()
#                     if product == "No product bought." or product == "No products":
#                         boughtProduct = False
#                     else:
#                         boughtProduct = True
#                 elif choice == '5':
#                     noBuyers = view_buyers()
#                     viewBuyers = True
#                 elif choice == '6':
#                     image_of_product(client)
#                 elif choice == '7':                    
#                     LogOut()
#                     break

#    client.close()          

#handle_client()