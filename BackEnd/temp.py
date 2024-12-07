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
#yalla btjarib l 2 clients?

#TODO: viewing ur own buyers
#TODO: fixing errors and making sure they dont crash 
#TODO: fixing the msging issue


sys.path.append("modules") 

from prettytable import PrettyTable

#dstprt = int(input("Enter the port number of the server you want to connect to: "))]
dstprt = 9999
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((socket.gethostbyname(socket.gethostname()),dstprt))

clientIP = client.getsockname()[0]

P2PServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
P2PServer.bind((clientIP,0))

clientPort = P2PServer.getsockname()[1]


print("myIP: " + clientIP)
print("myPort: " + str(clientPort))
# def emptyTerminal():
#     for i in range(50):
#         print("")


# aam jarb its loading
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

socketList = []
socketList.append(client)
delimiter = b"BRK"
ending = b"<END>"
def receiveThread():
    global delimiter
    global ending
    global socketList
    buffer = b"" 
    remaining = b""
    while True:
        readable, _, _ = select.select(socketList, [], [])
            #remaining = client.recv(1024)
        
        for sock in readable:
            print("RARARA")
            if not remaining:
                remaining += sock.recv(1024)
            
            while remaining:
                print("while remaining")
                #receive, remaining = remaining.split(ending, 1)
                # Using split and handling cases where the result has one element or two
                split_result = remaining.split(ending, 1)
                if len(split_result) == 1: #if there was no ending
                    break
                # If split_result has more than one part, unpack it
                elif len(split_result) == 2:
                    receive, remaining = split_result
                # else:
                #     # Handle the case where there is only one part
                #     receive = split_result[0]
                #     remaining = b""
            
                # print(receive)
                print("BABABAABBA")
                header, ptype, data = receive.split(delimiter, 2)
                header = header.decode('utf-8')
                ptype = ptype.decode()
                #print(header)
                if ptype == "str":
                    data=data.decode('utf-8')
                    print("Data: " + data)
                
                print(header)
                if header == "MSG":
                    messageQueue_R.put(data)
                elif header == "REGISTER":
                    registerQueue_R.put(data)
                elif header == "LOGIN":
                    #loginQueue_R.put(data)
                    loginQueue_R.put(data)
                elif header == "AUTH":
                    #authQueue_R.put(data)
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


sendingQueue = queue.Queue()
def sendThread():
    global delimiter
    global ending
    print("yi")
    while True:
        #get the prefix
        header, data = sendingQueue.get()
        print(header)
        print(data)
        #tt = f"{header},{data.decode()}"
        ptype = ""
        if isinstance(data, str):
            ptype = "str" 
            data = data.encode()
        else:
            ptype = "other"
        
        message = header.encode() + delimiter + ptype.encode() + delimiter + data + ending
        
        client.sendall(message)
        #client.send(header.encode('utf-8'))  # Send the header first
        #client.recv(1024)  # Wait for the server to acknowledge the header
        #client.sendall(data) 

receivingThread = threading.Thread(target=receiveThread, args=())
receivingThread.start()
sendingThread = threading.Thread(target=sendThread, args=())
sendingThread.start()


def Sign_In_Animation():
    
    counter = 3
    #  emptyTerminal()
    #  while counter > 0:
    #      print("Signing in", end= "", flush=True)    
    #      time.sleep(0.4)
    #      print(".", end="", flush=True)
    #      time.sleep(0.4)
    #      print(".", end="", flush=True)
    #      time.sleep(0.4)
    #      print(".", end="", flush=True)
    #      time.sleep(0.4)
    #      emptyTerminal()
    #      counter -= 1
    
    # emptyTerminal()

def emptyTerminal():
    print(" ")
    # if os.name == 'nt':  # For Windows
    #     os.system('cls')
    # else:  # For Linux and macOS
    #     os.system('clear')

def passwordValidate(password):
    character_MinLength = 8
    character_MaxLength = 64
    size = len(password)
    specialChars = "!@#$%^&*()-_=+[];:<>?~"
    containsLetter = any(char.isalpha() for char in password)
    containsNumber = any(char.isdigit() for char in password) 
    firstTime = True
    while  True:
        
        if firstTime == True:
            firstTime = False
            if size <= character_MaxLength and size >= character_MinLength and containsLetter and containsNumber and password[0] not in specialChars:
                # what other condtions do i add
                print('Password meets the requirements.')
                return password
            elif size >= character_MaxLength and size <= character_MinLength : 
                print("Your password has to be ATLEAST 8 characters and LESS than 64 characters.")
            elif  not containsLetter:
                print("Your password does not contain a letter.")
            elif not containsNumber:
                print("Your password does not contain a number.")
            else:
                print("Your password starts with a special character.")
        newpass = input("Enter another password: ")
        containsLetter = any(char.isalpha() for char in newpass)
        containsNumber = any(char.isdigit() for char in newpass) 
        size = len(newpass)
        if size <= character_MaxLength and size >= character_MinLength and containsLetter and containsNumber and newpass[0] not in specialChars:
                    # what other condtions do i add
            break
        elif size > character_MaxLength or size < character_MinLength : 
           print("Your password has to be ATLEAST 8 characters and LESS than 64 characters.")
        elif  not containsLetter:
             print("Your password does not contain a letter.")
        elif not containsNumber:
            print("Your password does not contain a number.")
        elif newpass[0] in specialChars:
            print("Your password starts with a special character.")

        
    return newpass
def sendImageFile(filename):
    while True:
        file1 = open(filename, "rb")
        for line in file1:
            client.sendall(line)
        client.sendall(b"END")


        
def validateEmail(email):
    firstTime = True
    while True:
        if firstTime == True:
            firstTime = False
            if email[-12:] == "mail.aub.edu":
                return email
            else:
                print("Your email should be an AUB email.")

        mail = input("Enter your mail again: ")
        if mail[-12:] == "mail.aub.edu":
                return mail
        print("Your email should be an AUB email.")
        

    
def Register():
    header = "REGISTER"
    firstTime = True
    emptyTerminal()
    while True:
        try: 
            # if firstTime:
            #     sendingQueue.put((header, "REGISTER"))
            name = input("Enter your full name: ")
            email = input("Enter your email: ")
            email = validateEmail(email)
            username = input("Enter your username: ")
            password = input("\nPassword should be at least 8 characters.\nPassword should be alphanumeric (Contains numbers and letters and not one type only).\nPassword should not start with a special character (!@#$%^&*()-_=+[];:<>?~)\nEnter your password: ")
            firstTime = False
            password = passwordValidate(password)
            
            message = f"{name},{email},{username},{password}"
            sendingQueue.put((header, message))
            #client.sendall(message.encode('utf-8'))
            response = registerQueue_R.get()
            #response = client.recv(1024).decode('utf-8')
            if response == "ACCOUNT_CREATED":
                #print("RIGHT HERE")
                sendingQueue.put((header, f"{clientIP} {clientPort}"))
                #client.sendall(f"{clientIP} {clientPort}".encode('utf-8'))

                return response
            elif response == "ACCOUNT_ALREADY_EXISTS":
                
                print("\nAccount already exists. Either login or use a different email or username.")
                time.sleep(2)
                return ""
            break
        except ValueError:
            counter = 5
            emptyTerminal()
            while counter>0:
                print("Password does not meet the necessary requirements.")
                print("- Atleast 8 characters, Less than 64 characters")
                print("")
                print("You will have the chance to retry again in " + str(counter) + " seconds.")
                time.sleep(1)
                counter -= 1
                emptyTerminal()
      
seconds = 0
def Timer (countDown):
    seconds = countDown
    while seconds > 0:
        time.sleep(1)
        seconds-=1


def Login(LIMIT): #username, password
    header = "LOGIN"
    counter = 0

    # sendingQueue.put((header, "LOGIN"))
    #client.sendall("LOGIN".encode('utf-8'))
    invalidUserPassword = False
    counter = 0
    while counter < 3: 
        # Get username and password, send it to server, and get response depending on validity
        emptyTerminal()

        # if counter == LIMIT:
        #     if seconds > 0:
        #         print(f"There are {seconds} seconds left till you can attempt a login again.")
        #         return "LOGIN_BLOCKED"
        #     else: counter=0 #Reset the login Block
        
        if invalidUserPassword:
            print("Invalid Username or Password. Please try again.")
            numOfTries = 3-counter
            numOfTries1 = str(numOfTries)
            print("You have " + numOfTries1 + " tries left")
            print("\n")
            invalidUserPassword = False
            
            
        username = input("Username: ")
        password = input("Password: ")
 
        sendingQueue.put((header, f"{username} {password}"))
        print("send username and pass")
        #client.sendall(f"{username} {password}".encode('utf-8'))  
        response = loginQueue_R.get()
        #response = client.recv(1024).decode('utf-8')   
        if response == "CORRECT":
            print("Success! Welcome " + username)
            # Send this client's IP and Port
            sendingQueue.put((header, f"{clientIP} {clientPort}"))
            
            
            offlinesize = int(loginQueue_R.get())
            if offlinesize > 0:
                for i in range(offlinesize):
                    source, msg = loginQueue_R.get().split(",")
                    cursor.execute("INSERT INTO Unread values(?, ?, ?)", (source, username, msg))
                    msgHistoryDB.commit()
            
                
            return f"SIGNED_IN {username}"
        elif response == "INVALID_INFO":
            counter +=1 
            invalidUserPassword = True
    return f"NO {username}"  
            
            
            #return "INVALID_INFO"
        



      
def printFirstMenu():
    while True:
        try:
            emptyTerminal()
            print("Select action (Pick Number): ")
            print("1. LOGIN")
            print("2. REGISTER")
            print("3. EXIT")
            #input validation in gui later
            n = int(input(""))
            return n
        except Exception as e:
            
            print("Please only submit a number.")
          
            
# TODO: do exit type, -1 to extit, or ask to ask after u enter
def authentication():
    header = "AUTH"
    print("Welcome to AUBoutique")
    LIMIT = 3
    while True:
        
        choice = printFirstMenu()
        #LOGIN
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
                #exit authentication. now you're logged in, mabrouk
                return 0 
        elif choice == 3:
            sendingQueue.put((header, "EXIT"))
            #client.send("EXIT".encode('utf-8'))
            return -1

#mnaamel handling functions la kel choice w mnerjaa mnaamella call bel main function tahet
def priceValidate(price):
    MIN_PRICE = 1 #cant sell for smth less than 1$
    #if price isnt actually a float, itll raise an error
    # if its less than 1, itll also send an error
    if float(price) < MIN_PRICE:
        raise ValueError("Less than 1") 
    
def add_product():
    header = "ADD_PRODUCT"
    sendingQueue.put(("FIRST", "ADD_PRODUCT"))
    #client.sendall("ADD_PRODUCT".encode('utf-8'))
    print(addProductQueue_R.get())
    #print(client.recv(1024).decode('utf-8'))
    while True:
        try: 
            product_name = input("Product name: ")
            price = input("Price: ")
            priceValidate(price)
            description = input("Description: ")
            #filename = input("Enter the path of the picture you want to send.")
            filename = input("Enter the filename of the picture: ")

            sendingQueue.put((header, f"{product_name},{price},{description},{filename}"))
            #client.sendall(f"{product_name},{price},{description},{filename}".encode('utf-8'))
            
            #list_products1()
            response = addProductQueue_R.get()
            #response = client.recv(1024).decode('utf-8')
            if response == "PRODUCT_ADDED":
                
                return product_name
            else: 
                print(response)
                print("There was an error in adding your product. Please try again.")
        except ValueError:
            print("ERROR: Please only enter a value greather than or equal to 1$.")
    return product_name  



def image_of_product(client):
    header = "IMG_PRODUCT"
    x = sendingQueue.put((header, "VIEW_PICTURE"))
    #x = client.send("VIEW_PICTURE".encode('utf-8'))
    ans = imageProductQueue_R.get().decode('utf-8')
    #ans = client.recv(1024).decode('utf-8')
    
    if(ans == "No products"):
        print("\nThere are no products are on the market\n")
        return
    try:
        product=input("Enter the name of the product you would like to view: ")
        sendingQueue.put((header, product))
        #client.send(product.encode('utf-8')) 
        x = imageProductQueue_R.get().decode('utf-8')
        #x=client.recv(1024).decode('utf-8')
        
        while(x=="Invalid product"):
            product=input("Error: enter the product name again: ")
            sendingQueue.put((header, product))
            #client.send(product.encode('utf-8')) 
            x = imageProductQueue_R.get()
            # client.send(product.encode())
            # x=client.recv(1024).decode('utf-8')

        size = int(imageProductQueue_R.get().decode('utf-8'))
        #size=int(client.recv(1024).decode())
        data = imageProductQueue_R.get()
        # COME BACK HERE AND DEFINE THE SIZE SOMEHOW
        #data=client.recv(size)
        image = Image.open(io.BytesIO(data))
        image.show()
    except Exception as e:
       print("An error has occured")

#kind of recursion, do i keep?
def LogOut():
    header = "LOG_OUT"
    # TODO remove user from online database from here too
    sendingQueue.put(("FIRST", "LOG_OUT"))
    #client.sendall("LOG_OUT".encode('utf-8'))
    print("Logging out...")
   # client.sendall("LOGOUT".encode('utf-8'))
    response = LogoutQueue_R.get()
    #response = client.recv(1024).decode('utf-8') #Wait for confirmation from server
    if response == "LOGOUT_SUCCESS":
        print("You have been successfully logged out.")
        time.sleep(1.2)
    else:
        print("Error logging out, please try again.")
    # handle_client()
    

def list_products():
    header = "SEND_PRODUCTS"
    sendingQueue.put(("FIRST", "SEND_PRODUCTS"))
    #client.sendall("SEND_PRODUCTS".encode('utf-8'))
    n = int(ListProductsQueue_R.get())
    #n = int(client.recv(1024).decode('utf-8'))
    sendingQueue.put((header, "Received"))
    #client.sendall("Received number of products".encode('utf-8'))
    
    table = PrettyTable()
    table.field_names = ["Username", "Product Name", "Price (in $)", "Description"]
    for i in range(n):
        temporary = ListProductsQueue_R.get()
        #temporary = client.recv(1024)
        sendingQueue.put((header, "OK"))
        #client.sendall("OK".encode('utf-8'))
        temporary = pickle.loads(temporary)
        table.add_row([temporary[0], temporary[1], temporary[2], temporary[3]])
    # Print the table
    print(table)


    
def getOnlineUsers():
    onlineUsers = getOnlineQueue_R.get()
    #onlineUsers = client.recv(1024)
    onlineUsers = pickle.loads(onlineUsers)
    for i in range(1, len(onlineUsers)+1):
        print(str(i) + "- " + onlineUsers[i-1])
    
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

stopLoop = False
def Waiting_Animation():
    emptyTerminal()
    while not stopLoop:
        print("Waiting for chat request", end= "", flush=True)    
        time.sleep(0.4)
        print(".", end="", flush=True)
        time.sleep(0.4)
        print(".", end="", flush=True)
        time.sleep(0.4)
        print(".", end="", flush=True)
        time.sleep(0.4)
        emptyTerminal()
    
    
    

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
        
def sendChatClient(targetIP, targetPort, messages_list, size, unread_messages, username, target):
    global ending
    global delimiter
    global socketList
    global inChat
    header = "ConstListenMSG"
    msgHistoryDB = sqlite3.connect("db.msgHistory")
    cursor = msgHistoryDB.cursor()

    print(target.upper())
    print("Chat opened. Type 'exit' to close the chat.")

    #WRITE HISTORY
    for j in range(len(messages_list)):
        if messages_list[j][0] == target:
            print(f"{target}: {messages_list[j][1]}")
        else:
            print(f"You: {messages_list[j][1]}")

        
    #NOW WRITE UNREAD    
    if size > 0:
        print(f">> You have some unread messages!")
        q=0
        for q in range(size):
            print(f"{target}: {unread_messages[q][0]}") 
            cursor.execute("DELETE FROM Unread WHERE message=?", (unread_messages[q][0],))   
            cursor.execute("INSERT INTO History values(?,?,?)", (target, username, unread_messages[q][0]))   
            msgHistoryDB.commit()   

    msgSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # print("targetIP: " + targetIP)
    # print("targetPort: " + str(targetPort))
    msgSocket.connect((targetIP,targetPort))
   # socketList.append(msgSocket)
    
    #print("HAHHAHAHAAHAHAHAHAH")
    while True:
        message = input("Enter: ")
        if message.lower() == "exit": 
            msgSocket.send("EXIT_CHAT".encode())
            del inChat[target]
            #client.sendall("EXIT_CHAT".encode('utf-8'))
            break
        else:
            print(f"You: {message}")
            #print("You: ", message)
            print("part one")
            info = header.encode() + delimiter + "str".encode() + delimiter + f"{username},{message}".encode() + ending
            #msgSocket.send(f"{username},{message}".encode())
            msgSocket.send(info)
            print("part two")
            
            #sendingQueue.put((header, message))
            #client.sendall(message.encode('utf-8'))
            if target and username and message:
                cursor.execute("INSERT INTO History values(?,?,?)", (username, target, message))   
                msgHistoryDB.commit()

def receiveChatAVAILABLE(username, target, message):
    header = "SEND_CHAT"
    msgHistoryDB = sqlite3.connect("db.msgHistory")
    cursor = msgHistoryDB.cursor()
    #while True:
        #y, x = stdscr.getyx()
        #response = recvChatQueue_R.get()
    response = message
    #response = client.recv(1024).decode('utf-8')
    # stdscr.addstr(i, 0, "Enter: ")
    if response == "EXIT_CHAT":
        print("User has left the chat.")
        return
    if username and target and response:
        cursor.execute("INSERT INTO History values(?,?,?)", (username, target, response))   
        msgHistoryDB.commit()
    print(f"{target}: {response}")

inChat = {}

def notification(username):
    ##GUI BASED
    print(username + " SENT YOU A MSG")


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
        socketList.append(connection)
        while True:
            # target = ""
            # msgToHandle = ""
            # if not offlineQueue.empty():
            #     print("now this should be added to unread")
            #     target, msgToHandle = offlineQueue.get().split(",")
                
            # else: 
            target,msgToHandle = constListenMSGQueue_R.get().split(",") #connection.recv(1024).decode().split(",") #constListenMSGQueue_R.get().split(",")
                
            if msgToHandle == "EXIT_CHAT":
                break
            if target in inChat:
                #call send and receive
                receiveChatAVAILABLE(username, target, msgToHandle) #fix input
            else: #if not in chat
                print(username)
                print(target)
                print(msgToHandle)
                cursor.execute("INSERT INTO Unread values(?, ?, ?)", (username, target, msgToHandle))
                msgHistoryDB.commit()
            #notification(target)
        

msgHistoryDB = sqlite3.connect("db.msgHistory")
cursor = msgHistoryDB.cursor()
cursor.execute("CREATE TABLE if not exists History(source TEXT, destination TEXT, message TEXT)") 

cursor.execute("CREATE TABLE if not exists Unread(source TEXT, destination TEXT, message TEXT)") 
msgHistoryDB.commit()

def handle_messaging(username):
    global inChat
    header = "HNDLE_MSG"
    sendingQueue.put(("FIRST", "MSG"))
    msgHistoryDB = sqlite3.connect('db.msgHistory')
    cursor = msgHistoryDB.cursor()
    USER_UNAVAILABLE = False
    while True:
        print(">> MESSAGING")
        #print("2. Accept an incoming chat request")
        #anychats = False
        newChat = False
        cursor.execute("SELECT message FROM History")
        existing_chats = cursor.fetchall()
        if not existing_chats:
            print("You have no past chats! Want to create a new chat? (y/n)")
            print("'exit' to Exit.")
            newChat = True

        else:
        # anychats = True
            print("1. Open a chat with someone new")
            print("\n\nExisting Chats: ")
            cursor.execute("SELECT DISTINCT source, destination FROM History WHERE destination = ? OR source = ?", (username, username))
            toPrint = cursor.fetchall()
            for i in range (len(toPrint)):
                if toPrint[i][0] == username: #if source is username, print destination
                    print("- " + toPrint[i][1])
                else: #if source not username, print source
                    print("- " + toPrint[i][0])
                

            print("\n\n\n")

        #IF YOU EXIT AND TRY TO MSG SOMEONE AGAIN, -> error
        target = input("min badak tehke: ")
        if target =="exit": 
            sendingQueue.put((header, "EXIT"))
           # client.sendall("EXIT".encode('utf-8'))
            break
        
        sendingQueue.put((header, target))
        
        unread_messages = []
        cursor.execute("SELECT message FROM Unread WHERE source=? AND destination=?", (target, username))
        unread_messages = cursor.fetchall()
        size = len(unread_messages)

        cursor.execute("SELECT source, message FROM History WHERE destination = ? OR source = ?", (username, username))
        history = cursor.fetchall()

        print("How many unread messages: " + str(size))
        status = handleMSGQueue_R.get()
        print("STATUS: " + status)
        if status == "ONLINE": #do p2p directly even if not in chat
            targetIP, targetPort = handleMSGQueue_R.get().split(",") 
            targetPort = int(targetPort)
            inChat[target] = True
            sendChat = threading.Thread(target=sendChatClient, args=(targetIP, targetPort, history, size, unread_messages, username, target))
            sendChat.start()
            sendChat.join()
            #sendChatClient(targetIP, targetPort, history, size, unread_messages, username, target)
        elif status=="NOT_ONLINE": #if not online, send msg to server until he gets online ok
            while True:
                msg = input("Enter your message: ")
                sendingQueue.put((header, msg))
    
def buyProducts():
    header = "BUY"
    sendingQueue.put(("FIRST", "BUY_PRODUCTS"))
    #client.send("BUY_PRODUCTS".encode('utf-8'))
    NoProds = False
    while True:
        answer1 = buyQueue_R.get()
        #answer1 = client.recv(1024).decode('utf-8')
        if answer1 == "All the products on the market are your own. You cannot buy at this time.":
            print("\n" + answer1 + "\n")
            NoProds = True
            break
        elif answer1 == "There are no products on the market.":
            print("\n" + answer1 + "\n")
            return "No products"
        product = input("Which product would you like to buy? ")
        sendingQueue.put((header, product))
        #client.sendall(product.encode('utf-8'))
        answer = buyQueue_R.get()
        #answer = client.recv(1024).decode('utf-8')
        if answer == "Product name received":
            sendingQueue.put((header, "Thanks"))
            #client.sendall("Thanks".encode('utf-8'))
            print(buyQueue_R.get())
            #print(client.recv(1024).decode('utf-8'))
            break
        else:
            print(answer)  
    if NoProds:
        return "No product bought."
    return product


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
    emptyTerminal()
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
        
def handle_client():
    #notLoggedOut = True
    while True:
        username = authentication()
        if username == -1:
            counter = 3
            emptyTerminal()
            while counter > 0:
                print("Exiting AUBoutique", end= "", flush=True)    
                time.sleep(0.4)
                print(".", end="", flush=True)
                time.sleep(0.4)
                print(".", end="", flush=True)
                time.sleep(0.4)
                print(".", end="", flush=True)
                time.sleep(0.4)
                emptyTerminal()
                counter -= 1
            print("Hope you enjoyed!")
            time.sleep(1)
            break
        else:
            msgListening = threading.Thread(target=constantlylistenforMessages, args=(username,))
            msgListening.start()
            
            # thesrver = threading.Thread(target=theserver, args=())
            # thesrver.start()
            Sign_In_Animation()
            #Now get list of products
            #Display list of options to client 
            f = open("BackEnd/temp.txt")
            lol = f.read()
            print(lol)
            boughtProduct = False
            addedProduct = False
            viewAllUsers = False
            noBuyers = False
            viewBuyers = False
            product = ""
            while True:
                if viewAllUsers == False and not viewBuyers:
                    print("calling to list all products")
                    list_products()
                viewAllUsers = False
                if viewBuyers:
                    viewBuyers = False
                if addedProduct:
                    print(f"{product} successfully added")
                    addedProduct=False
                if boughtProduct:
                    emptyTerminal()
                    counter11 = 3
                    while counter11 > 0:
                        print("Waiting for confirmation", end= "", flush=True)    
                        time.sleep(0.3)
                        print(".", end="", flush=True)
                        time.sleep(0.3)
                        print(".", end="", flush=True)
                        time.sleep(0.3)
                        print(".", end="", flush=True)
                        time.sleep(0.3)
                        emptyTerminal()
                        counter11 -= 1
                    currentdate = date.today()
                    currentdate = currentdate + timedelta(days = 7)
                    currentdate = (str) (currentdate) 
                    year, month, day = currentdate.split("-")
                    flipped_date = f"{day}-{month}-{year}"
                    currentdate = flipped_date
                    message = "\n\nYour " +  product +  " will be available at the AUB Post Office in one week on " + str(currentdate)
                    message += "\nAUB Post Office Working Hours: 8:00 a.m. till 4:00 p.m.\n\n" 
                    print(message)
                    boughtProduct=False
                if noBuyers == True:
                    print("\nThere are no buyers for your products yet.\n")
                    noBuyers = False
                print("<<")
                print("1. Add a Product")
                print("2. View Someone's Products")
                print("3. Send Message")
                print("4. Buy a Product")
                print("5. View buyers of your products")
                print("6. View the picture of a specific product")
                print("7. Log Out")
                
                choice = input("Enter your choice: ")
                
                if choice == '1':
                    product = add_product()
                    addedProduct = True
                elif choice == '2':
                    viewUsersProducts()
                    viewAllUsers = True
                elif choice == '3':
                    handle_messaging(username)
                elif choice == '4':
                    product = buyProducts()
                    if product == "No product bought." or product == "No products":
                        boughtProduct = False
                    else:
                        boughtProduct = True
                elif choice == '5':
                    noBuyers = view_buyers()
                    viewBuyers = True
                elif choice == '6':
                    image_of_product(client)
                elif choice == '7':                    
                    LogOut()
                    break

    client.close()          

handle_client()