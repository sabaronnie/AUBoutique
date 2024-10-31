import socket
import threading
import time
import os
import sys
import pickle
from datetime import date, timedelta
import curses
import sqlite3
#yalla btjarib l 2 clients?

#TODO: password and mail validation
#TODO: viewing ur own buyers
#TODO: fixing errors and making sure they dont crash 
#TODO: fixing the msging issue


sys.path.append("modules") 

from prettytable import PrettyTable

#Port = 9999
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((socket.gethostbyname(socket.gethostname()),9999))


clientIP = client.getsockname()[0]
clientPort = client.getsockname()[1]

# def emptyTerminal():
#     for i in range(50):
#         print("")

# aam jarb its loading
def Sign_In_Animation():
    print("SINGING IN NO ANIMATION FOR NOW")
    # counter = 2
    # emptyTerminal()
    # while counter > 0:
    #     print("Signing in", end= "", flush=True)    
    #     time.sleep(0.4)
    #     print(".", end="", flush=True)
    #     time.sleep(0.4)
    #     print(".", end="", flush=True)
    #     time.sleep(0.4)
    #     print(".", end="", flush=True)
    #     time.sleep(0.4)
    #     emptyTerminal()
    #     counter -= 1
    
    # emptyTerminal()

def emptyTerminal():
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Linux and macOS
        os.system('clear')

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
        if size <= character_MaxLength and size >= character_MinLength and containsLetter and containsNumber and password[0] not in specialChars:
                    # what other condtions do i add
            print('Password meets the requirements.')
            break
        elif size >= character_MaxLength and size <= character_MinLength : 
           print("Your password has to be ATLEAST 8 characters and LESS than 64 characters.")
        elif  not containsLetter:
             print("Your password does not contain a letter.")
        elif not containsNumber:
            print("Your password does not contain a number.")
        else:
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
        

    

        
seconds = 0
def Timer (countDown):
    seconds = countDown
    while seconds > 0:
        time.sleep(1)
        seconds-=1

def Login(LIMIT):
    counter = 0

    client.sendall("LOGIN".encode('utf-8'))
    invalidUserPassword = False
    TIMER_BLOCK = False
    TIMER_NOTIFY = False
    seconds = 0
    while True: 
        # Get username and password, send it to server, and get response depending on validity
        emptyTerminal()

        # if counter == LIMIT:
        #     if seconds > 0:
        #         print(f"There are {seconds} seconds left till you can attempt a login again.")
        #         return "LOGIN_BLOCKED"
        #     else: counter=0 #Reset the login Block
        if TIMER_BLOCK:
            print(f"There are {seconds} seconds left till you can attempt a login again.")
            print("\n")
            TIMER_BLOCK = False   
        elif TIMER_NOTIFY:
            print("You have failed to login way too many times!") 
            print("Please wait 3 minutes to try again.")   
            print("\n")
            TIMER_NOTIFY = False
        if invalidUserPassword:
            print("Invalid Username or Password. Please try again.")
            print("\n")
            invalidUserPassword = False
            
            
        username = input("Username: ")
        password = input("Password: ")
        
        #password = "12345678"
        #AUTO SIGN IN
        # username = "ron"
        # password = "12345678"
        
        client.sendall(f"{username} {password}".encode('utf-8'))
        
    
        response = client.recv(1024).decode('utf-8')
        
        if response == "TIMER_NOT_FINISHED":
            TIMER_BLOCK = True
            client.send("OK".encode('utf-8'))
            seconds = client.recv(1024).decode('utf-8')
            continue   
            
        if response == "CORRECT":
            print("Success! Welcome " + username)
            # Send this client's IP and Port
            #client.sendall(f"{clientIP} {clientPort}".encode('utf-8'))
            return f"SIGNED_IN {username}"
        elif response == "INVALID_INFO":
            invalidUserPassword = True
            response = client.recv(1024).decode('utf-8')
            if response == "TIMER_NOTIFY":
                TIMER_NOTIFY = True
            #return "INVALID_INFO"
        



      
def printFirstMenu():
    while True:
        try:
            #emptyTerminal()
            print("Select action (Pick Number): ")
            print("1. LOGIN")
            print("2. REGISTER")
            print("3. EXIT")
            #input validation in gui later
            n = int(input(""))
            return n
        except Exception as e:
            print(type(e).__name__)
            print("Please only submit a number. ")
            
# TODO: do exit type, -1 to extit, or ask to ask after u enter
def authentication():
    print("Welcome to AUBoutique")
    LIMIT = 3
    while True:
        
        choice = printFirstMenu()
        
        #LOGIN
        if choice == 1:                
            response, username = Login(LIMIT).split()
            if response == "SIGNED_IN":
                return username
            elif response == "INVALID_INFO" or response == "LOGIN_BLOCKED":
                continue
        elif choice == 2:
            if Register() == "ACCOUNT_CREATED":
                #exit authentication. now you're logged in, mabrouk
                return 0 
        elif choice == 3:
            client.send("EXIT".encode('utf-8'))
            return -1

#mnaamel handling functions la kel choice w mnerjaa mnaamella call bel main function tahet
def priceValidate(price):
    MIN_PRICE = 1 #cant sell for smth less than 1$
    #if price isnt actually a float, itll raise an error
    # if its less than 1, itll also send an error
    if float(price) < MIN_PRICE:
        raise ValueError("Less than 1") 
    

    
    
#kind of recursion, do i keep?
def LogOut():
    # TODO remove user from online database from here too
    client.sendall("LOG_OUT".encode('utf-8'))
    print("Logging out...")
   # client.sendall("LOGOUT".encode('utf-8'))
    response = client.recv(1024).decode('utf-8') #Wait for confirmation from server
    if response == "LOGOUT_SUCCESS":
        print("You have been successfully logged out.")
    else:
        print("Error logging out, please try again.")
    # handle_client()

# def list_products():
#     client.sendall("SEND_PRODUCTS".encode('utf-8'))
#     n = int(client.recv(1024).decode('utf-8'))
#     client.sendall("Received number of products".encode('utf-8'))
    
#     table = PrettyTable()
#     table.field_names = ["Username", "Product Name", "Price (in $)", "Description"]
#     for i in range(n):
#         temporary = client.recv(1024)
#         client.sendall("OK".encode('utf-8'))
#         temporary = pickle.loads(temporary)
#         table.add_row([temporary[0], temporary[1], temporary[2], temporary[3]])
#     # Print the table
#     print(table)


#LOCK IT
i = 3
def sendChat(messages_list, size, unread_messages, username, target, db):
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
        i+=1
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
            cursor.execute("INSERT INTO History values(?,?,?)", (target, username, message))   
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
            client.sendall("EXIT_CHAT".encode('utf-8'))
            i=0
            break
        else:
            stdscr.addstr(i, 0, f"You: {message}")
            stdscr.refresh()  
            i+=1
            #print("You: ", message)
            client.sendall(message.encode('utf-8'))
            cursor.execute("INSERT INTO History values(?,?,?)", (target, username, message))   
            db.commit()
        
    #curses.nocbreak()
    stdscr.keypad(False)
    #curses.echo()
    curses.endwin()
                
        
    
    print("")


#this runs in the background when you open the chat
#so bas teftah l chat, 
# 0history shows up
# unread show up
# and at the same time, if someone sends u a msg rn, it should show up to
def receiveChat(username, target):
    global i
    db = sqlite3.connect("db.msgHistory")
    cursor = db.cursor()
    stdscr = curses.initscr()
    while True:
        #y, x = stdscr.getyx()
        response = client.recv(1024).decode('utf-8')
       # stdscr.addstr(i, 0, "Enter: ")
        if response == "EXIT_CHAT":
            print("User has left the chat.")
            break
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
    client.sendall("MSG".encode('utf-8'))
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
            
        target = input("")
        if target =="exit": 
            continue
        
        # else:
        #     client.sendall(target.encode('utf-8'))
        # # target c
        #     client.sendall(target.encode('utf-8'))       
         #if u put a name of someone
        #check if that account exists in history
        # open it, print the history
        # now get unread from server
        #and open chat 
        if target == "1" or target.lower() == "y":
                
            #open new chat
                            #so takes new name
                #sends new name to server
                #opens chat with send chat
                #w storesm sgs and sends them to server
                client.sendall("INITIATE_NEW_CHAT".encode('utf-8'))
                client.recv(1024)
                
                
                target = input("Who would you like to open a new chat with? ")
                client.sendall(target.encode('utf-8'))
                
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
            client.sendall("OPEN_EXISTING_CHAT".encode('utf-8'))
            
            target = input("Who would you like to open an existing chat with? ")
            client.sendall(target.encode('utf-8'))
            
            

            
            unread_messages = []
            size = int(client.recv(1024).decode('utf-8'))
            client.send("OK".encode('utf-8'))
            if size>0:
                for q in range(size):
                    message = client.recv(1024).decode('utf-8')
                    client.send("OK".encode('utf-8'))

                    unread_messages.append(message)

                    
            receiving_thread = threading.Thread(target=receiveChat, args=(username, target))
            receiving_thread.start()
            sendChat(messages_list, size, unread_messages, username, target, db)
                
            




    

        
def handle_client(db):
    #notLoggedOut = True
    while True:
        username = authentication()
        if username == -1:
            print("broski")
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
            product = ""
            while True:
                # if viewAllUsers == False:
                #     #emptyTerminal()
                #     list_products()
                # viewAllUsers = False
                if addedProduct:
                    print(f"{product} successfully added")
                    addedProduct=False
                if boughtProduct:
                    currentdate = date.today()
                    currentdate = currentdate + timedelta(days = 7)
                    message = "!!! Your " +  product +  " will be available at the AUB Post Office from " + str(currentdate)
                    message += "\nAUB Post Office Working Hours: 8:00 a.m. till 4:00 p.m." 
                    print(message)
                    boughtProduct=False
                
                print("<<")
                print("1. Add a Product")
                print("2. View Someone's Products")
                print("3. Send Message")
                print("4. Buy a Product")
                print("5. View buyers of your products")
                print("6. Log Out")
                
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
                    boughtProduct = True
                elif choice == '5':
                    view_buyers()
                elif choice == '6':                    
                    LogOut()
                    break

    client.close()          
        
handle_client(db)
