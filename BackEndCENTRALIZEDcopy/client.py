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
clientPort = client.getsockname()[1]

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

def receiveThread():
    buffer = b"" 
    delimiter = b"BRK"
    remaining = b""
    ending = b"<END>"
    while True:
        #chunk = client.recv(1024)
        # if not chunk:
        #     break  # Connection closed
        # buffer += chunk  # Add received data to the buffer
        if not remaining:
            remaining = client.recv(1024)
        
        receive, remaining = remaining.split(ending, 1)
        
        
        print(receive)
        header, ptype, data = receive.split(delimiter, 2)
        header = header.decode('utf-8')
        ptype = ptype.decode()
        print(header)
        if ptype == "str":
            data=data.decode('utf-8')
            
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


sendingQueue = queue.Queue()
def sendThread():
    print("yi")
    while True:
        #get the prefix
        print("lakk")
        header, data = sendingQueue.get()
        print("got thru sending queue")
        print(header)
        print(data)
        #tt = f"{header},{data.decode()}"
        ptype = ""
        if isinstance(data, str):
            ptype = "str" 
            data = data.encode()
        else:
            ptype = "other"
        
        delimiter = b"BRK"#b"\0\0"
        ending = b"<END>"
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

def Login(LIMIT):
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
            #client.sendall(f"{clientIP} {clientPort}".encode('utf-8'))
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


def sendChat(messages_list, size, unread_messages, username, target, db):
    header = "RECV_CHAT"
    db = sqlite3.connect("db.msgHistory")
    cursor = db.cursor()
    global i
    
    
    print("FETIT AA SEND CHAT")
    stdscr = curses.initscr()
    #curses.noecho()
    #curses.cbreak()
    stdscr.keypad(True)
    
    stdscr.clear()
    
    stdscr.addstr(0, 0, f">>> {target.upper()}")
    stdscr.refresh()
    stdscr.addstr(1, 0, "Chat opened. Type 'exit' to close the chat.")
    stdscr.refresh()

    #WRITE HISTORY
    for j in range(len(messages_list)):
        if messages_list[j][0] == target:
            stdscr.addstr(i, 0, f"{target}: {messages_list[j][1]}")
        else:
            stdscr.addstr(i, 0, f"You: {messages_list[j][1]}")
        i+=1 #possible extra line here
        stdscr.refresh()
        
    #NOW WRITE UNREAD    
    if size > 0:
    
        i+=3
        stdscr.addstr(i, 0, f">> You have some unread messages!")

        i+=2
        q = 0
        for q in range(size):
            stdscr.addstr(i, 0, f"{target}: {unread_messages[q]}")
            i+=1   
            cursor.execute("INSERT INTO History values(?,?,?)", (target, username, unread_messages[q]))   
            db.commit()   

    
    print("HAHHAHAHAAHAHAHAHAH")
    while True:
        stdscr.addstr(curses.LINES - 1, 0, "Enter: ")
        stdscr.refresh()
        message = stdscr.getstr(curses.LINES-1, 8).decode('utf-8')
        lastLine = curses.LINES-1
        stdscr.move(lastLine, 0)     # Move the cursor to the beginning of line y
        stdscr.clrtoeol()     # Clear to the end of line
        stdscr.refresh()      # Refresh the screen to apply changes
        # Starts reading after "Enter something: "
        if message.lower() == "exit": 
            sendingQueue.put((header, "EXIT_CHAT"))
            #client.sendall("EXIT_CHAT".encode('utf-8'))
            i=0
            break
        else:
            stdscr.addstr(i, 0, f"You: {message}")
            stdscr.refresh()  
            i+=1
            #print("You: ", message)
            sendingQueue.put((header, message))
            #client.sendall(message.encode('utf-8'))
            if target and username and message:
                cursor.execute("INSERT INTO History values(?,?,?)", (username, target, message))   
                db.commit()
        
    #curses.nocbreak()
    stdscr.keypad(False)
    #curses.echo()
    curses.endwin()


#this runs in the background when you open the chat
#so bas teftah l chat, 
# 0history shows up
# unread show up
# and at the same time, if someone sends u a msg rn, it should show up to
def receiveChat(username, target):
    header = "SEND_CHAT"
    global i
    db = sqlite3.connect("db.msgHistory")
    cursor = db.cursor()
    stdscr = curses.initscr()
    while True:
        #y, x = stdscr.getyx()
        response = recvChatQueue_R.get()
        #response = client.recv(1024).decode('utf-8')
       # stdscr.addstr(i, 0, "Enter: ")
        if response == "EXIT_CHAT":
            print("User has left the chat.")
            break
        if username and target and response:
            cursor.execute("INSERT INTO History values(?,?,?)", (username, target, response))   
            db.commit()
        stdscr.addstr(i, 0, f"{target}: {response}")
        stdscr.refresh()  
        lastLine = curses.LINES-1
          # Get current cursor coordinates
        # if y != lastLine:
        stdscr.move(lastLine, 8)   # Read the character at position (y, x)
        stdscr.refresh()  
        #print(target + ": " + response)
        i+=1


    
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
    
    
    
def listenForIncomingChatRequest():
    while True:
        print("")
        global stopLoop
        waiting_animation = threading.Thread(target=Waiting_Animation, args=())
        waiting_animation.start()
        senderUser = client.recv(1024).decode('utf-8', errors='replace') #do timeout later TODO
        stopLoop = True
        waiting_animation.join()
        emptyTerminal()
        print("INCOMING..")
        print(senderUser + " would like to open a chat with you.")
        print("Would you like to accept? Y/N")
        choice = input("")
        #do input validation here
        if choice.lower() == "y":
            client.sendall("REQUEST_ACCEPTED".encode('utf-8'))
            receiving_thread = threading.Thread(target=receiveChat, args=(senderUser,))
            #sending_thread.start()
            receiving_thread.start()
            sendChat(senderUser)

#threadsQueue = {}
# IDK HOW TO IMPLEMENT YET
def passivelyListenForChatRequest():
    while True:
        received = client.recv(1024).decode('utf-8')
        status, username = received.split()
        if status == "INCOMING_CHAT_REQUEST":
            print(f"!!!\nYou have received some messages from {username}.\nMake sure to check them out later.")
            

    # Messages
    # 1. Open a chat with someone new
    
    # Existing Chats:
    # 1. Farid
    # 2. Anthony

    #1 open a chat with someone specific
    # choose who this person is
    # if the person is not in chat, send w sayyev bel database implement old1 with receiver not in chat.
    
    #if the person is in the chat, do the chatting el usual li kena 3am naamelo through dictionaries. 

 

db = sqlite3.connect("db.msgHistory")
cursor = db.cursor()
cursor.execute("CREATE TABLE if not exists History(source TEXT, destination TEXT, message TEXT)") 

def handle_messaging(username, db):
    header = "HNDLE_MSG"
    sendingQueue(("FIRST", "MSG"))
    #client.sendall("MSG".encode('utf-8'))
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
            # cursor.execute('''
            #     SELECT 
            #     LEAST(source, destination) AS user1,
            #     GREATEST(source, destination) AS user2
            #     FROM 
            #     History 
            #     WHERE 
            #     destination = ? OR source = ?
            #     GROUP BY 
            #     user1, user2;
            #                ''')
            cursor.execute("SELECT DISTINCT source, destination FROM History WHERE destination = ? OR source = ?", (username, username))
            toPrint = cursor.fetchall()
            for i in range (len(toPrint)):
                if toPrint[i][0] == username: #if source is username, print destination
                    print("- " + toPrint[i][1])
                else: #if source not username, print source
                    print("- " + toPrint[i][0])
                

            print("\n\n\n")
            
        #IF YOU EXIT AND TRY TO MSG SOMEONE AGAIN, -> error
        target = input("")
        if target =="exit": 
            sendingQueue.put((header, "EXIT"))
           # client.sendall("EXIT".encode('utf-8'))
            break
        
        # else:
        #     client.sendall(target.encode('utf-8'))
        # # target c
        #     client.sendall(target.encode('utf-8'))       
         #if u put a name of someone
        #check if that account exists in history
        # open it, print the history
        # now get unread from server
        #and open chat 
        if target == "1" or newChat:
                newChat=False
            #open new chat
                            #so takes new name
                #sends new name to server
                #opens chat with send chat
                #w storesm sgs and sends them to server
                sendingQueue.put((header, "INITIATE_NEW_CHAT"))
                #client.sendall("INITIATE_NEW_CHAT".encode('utf-8'))
                handleMSGQueue_R.get()
                #client.recv(1024)
                
                if target=="1":
                    target = input("Who would you like to open a new chat with? ")
                sendingQueue.put((header, target))
                #client.sendall(target.encode('utf-8'))
                
                # if msgGUI(USER_UNAVAILABLE) == -1:
                #     USER_UNAVAILABLE = False
                # target = input("")
                # if target.lower() == "exit": #Exit if user cancels
                #     return#Send target username to server

                #response = client.recv(1024).decode('utf-8')
                #     receiving_thread = threading.Thread(target=receiveChat, args=(target,))
                # receiving_thread.start() 
                cursor.execute("SELECT source, message FROM History WHERE destination = ? OR source = ?", (username, username))
                messages_list = cursor.fetchall()
                
                unread_messages = []
                size = 0
                # size = int(client.recv(1024).decode('utf-8'))
                # client.send("OK".encode('utf-8'))
                # if size>0:
                #     q = 0
                #     for q in range(size):
                #         message = client.recv(1024).decode('utf-8')
                #         client.send("OK".encode('utf-8'))

                #         unread_messages.append(message)
 
                #         cursor.execute("INSERT INTO History values(?,?,?)", (target, username, message))   
                #         db.commit() 
                sendChat(messages_list, size, unread_messages, username, target, db)
                
        else:
            #who do you want to chat with
            cursor.execute("SELECT source, message FROM History WHERE destination = ? OR source = ?", (username, username))
            messages_list = cursor.fetchall()
            print(messages_list)
            # if len(messages_list)==0: #that means no history, so new chat, so 1
            #     #u dont have a chat with that person
            #     continue
            
            #else:
                #THE CHAT EXISTS, OPEN IT WITH HISTORY W KEL HAL ARAF
            sendingQueue.put((header, "OPEN_EXISTING_CHAT"))
            #client.sendall("OPEN_EXISTING_CHAT".encode('utf-8'))
            handleMSGQueue_R.get()
            #client.recv(1024)
            #target = input("Who would you like to open an existing chat with? ")
            sendingQueue.put((header, target))
            #client.sendall(target.encode('utf-8'))
            
            

            
            unread_messages = []
            size = int(handleMSGQueue_R.get())
            #size = int(client.recv(1024).decode('utf-8'))
            sendingQueue.put((header, "OK"))
            #client.send("OK".encode('utf-8'))
            if size>0:
                for q in range(size):
                    #message = client.recv(1024).decode('utf-8')
                    message = handleMSGQueue_R.get()
                    sendingQueue.put((header, "OK"))
                    #client.send("OK".encode('utf-8'))



                    if target and username and message:
                        unread_messages.append(message)
                        # cursor.execute("INSERT INTO History values(?,?,?)", (target, username, message))   
                        # db.commit() 
            print("THIS IS THE UNREAD MESSAGES")
            print(unread_messages)   
            receiving_thread = threading.Thread(target=receiveChat, args=(username, target))
            receiving_thread.start()
            sendChat(messages_list, size, unread_messages, username, target, db)
                
            
        # if you open chat, it shows unread
        # but before it stores it in unread, it check sif you're in the chat
        # if you are in the chat, send it live
        # if you are not in the chat, send it to unread    

        # if option=="1" and anychats==False:
        #     #ZABETA LATER
        #     #client.sendall("INITIATE_CHAT".encode('utf-8'))
        #     if msgGUI(USER_UNAVAILABLE) == -1:
        #         USER_UNAVAILABLE = False
        #     target = input("")
        #     if target.lower() == "exit": #Exit if user cancels
        #         return
        #     client.sendall(target.encode('utf-8')) #Send target username to server
        #     print("BUM BUM BUM")
        #     response = client.recv(1024).decode('utf-8')

        #     # if response == "NOT_ONLINE":
        #     #     print("The selected user is not currently online. Please choose another user.")

        #     if response =="ONLINE_AND_AVAILABLE":
        #         print("LLLLL")
        #         response = client.recv(1024).decode('utf-8')
        #         if response == "REQUEST_ACCEPTED":
        #             receiving_thread = threading.Thread(target=receiveChat, args=(target,))
        #             receiving_thread.start()
        #             sendChat(target)
        #         #DO CHAT REJECTION CODE
        #     elif response == "ONLINE_BUT_NOT_AVAILABLE":
        #         #SO OPEN MY CHAT ONLY
        #         print("TTTTTTTTT")
        #         sendChat(target)  
            
        # elif option == "2":
        #     client.sendall("LISTEN_FOR_CHAT".encode('utf-8'))
        #     listenForIncomingChatRequest()
            
        # elif option=="3" and any_unread =="UNREAD":
        #     client.sendall("READ_UNREAD".encode('utf-8'))
            
        #     print("Which unread messages would you like to read?")
        #     username_list = client.recv(1024).decode('utf-8')
        #     print(username_list)
        #     choice = input("")
        #     client.send(choice.encode('utf-8'))
        #     response = client.recv(1024).decode('utf-8')
        #     if response == "SUCCESS":
        #         #empty terminal hon
        #         client.send("OK".encode('utf-8'))
        #         size = int(client.recv(1024).decode('utf-8'))
        #         client.send("OK".encode('utf-8'))
        #         print(f">>> {choice.upper()}")
        #         print("Reading UNREAD chats ONLY. Type 'exit' to go back.")
        #         print("")
        #         print(size)
        #         for i in range(size):
        #             message = client.recv(1024).decode('utf-8')
        #             client.send("OK".encode('utf-8'))
                    
        #             print(f"{choice}: {message}")

        #         print("done") 
        #         exit = input("Type 'exit' to close. ")
        #         # if exit.lower() == "exit":
        #         #     client.send("EXIT_CHAT".encode('utf-8'))
        #         #     continue
                


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

     
notifyMSG = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
notifyMSG.connect((socket.gethostbyname(socket.gethostname()),9999))
   
   
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
        
def handle_client(db):
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
                    handle_messaging(username, db)
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

handle_client(db)