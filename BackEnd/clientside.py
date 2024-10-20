import socket
import threading
import time
import os
import sys
import pickle

sys.path.append("BackEnd/modules") 

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
    counter = 2
    emptyTerminal()
    while counter > 0:
        print("Signing in", end= "", flush=True)    
        time.sleep(0.4)
        print(".", end="", flush=True)
        time.sleep(0.4)
        print(".", end="", flush=True)
        time.sleep(0.4)
        print(".", end="", flush=True)
        time.sleep(0.4)
        emptyTerminal()
        counter -= 1
    
    # emptyTerminal()

def emptyTerminal():
    print("")
    # if os.name == 'nt':  # For Windows
    #     os.system('cls')
    # else:  # For Linux and macOS
    #     os.system('clear')

def passwordValidate(password):
    character_MinLength = 8
    character_MaxLength = 64
    size = len(password)
    if size <= character_MaxLength and size >= character_MinLength :
        # what other condtions do i add
        print('Password meets the requirements.')

    else: raise ValueError("Your password has to be ATLEAST 8 characters and LESS than 64 characters.")
    
def Register():
    firstTime = True
    emptyTerminal()
    while True:
        try: 
            if firstTime:
                client.sendall("REGISTER".encode('utf-8'))
            name = input("Enter your full name: ")
            email = input("Enter your email: ")
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            firstTime = False
            
            passwordValidate(password)
            
            
            message = f"{name} {email} {username} {password}"
            client.send(message.encode('utf-8'))
            response = client.recv(1024).decode('utf-8')
            if response == "ACCOUNT_CREATED":
                print("RIGHT HERE")
                client.sendall(f"{clientIP} {clientPort}".encode('utf-8'))
                return response
            elif response == "ACCOUNT_ALREADY_EXISTS":
                print("Account already exists. Either login or use a different email or username.")
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
    counter = 0

    client.sendall("LOGIN".encode('utf-8'))
    invalidPassword = False
    while True: 
        # Get username and password, send it to server, and get response depending on validity
        #emptyTerminal()

        if counter == LIMIT:
            if seconds > 0:
                print(f"There are {seconds} seconds left till you can attempt a login again.")
                return "LOGIN_BLOCKED"
            else: counter=0 #Reset the login Block
            
        if invalidPassword:
            print("Invalid Password, Please try again.")
            
        username = input("Username: ")
        password = input("Password: ")
        
        client.send(f"{username} {password}".encode('utf-8'))
        response = client.recv(1024).decode('utf-8')
        
        
        if response == "CORRECT":
            print("Success! Welcome " + username)
            # Send this client's IP and Port
            client.sendall(f"{clientIP} {clientPort}".encode('utf-8'))
            return "SIGNED_IN"
        elif response == "INVALID_PASSWORD":
            invalidPassword = True
            print("Invalid Password")
            counter+=1
        elif response == "INVALID_INFO":
            invalidPassword = True
            print("Invalid Username or Password")
            counter+=1
        if counter == LIMIT:
            print("You have failed to login way too many times!") 
            print("Please wait 3 minutes to try again.")
            timerThread = threading.Thread(target='Timer', args=(180))
            timerThread.start()

      
def printFirstMenu():
    while True:
        try:
            emptyTerminal()
            print("Select action (Pick Number): ")
            print("1. LOGIN")
            print("2. REGISTER")
            print("3. EXIT")
            #input validation in gui later
            return int(input(""))
        except:
            print("Please only submit a number. ")
            
# TODO: do exit type, -1 to extit, or ask to ask after u enter
def authentication():
    print("Welcome to AUBoutique")
    LIMIT = 3
    while True:
        
        choice = printFirstMenu()
        
        #LOGIN
        if choice == 1:                
            response = Login(LIMIT)
            if response == "SIGNED_IN":
                return 0
            elif response == "INVALID_INFO" or response == "LOGIN_BLOCKED":
                continue
        elif choice == 2:
            if Register() == "ACCOUNT_CREATED":
                #exit authentication. now you're logged in, mabrouk
                return 0
                
        elif choice == 3:
            return -1

#mnaamel handling functions la kel choice w mnerjaa mnaamella call bel main function tahet
def priceValidate(price):
    MIN_PRICE = 1 #cant sell for smth less than 1$
    #if price isnt actually a float, itll raise an error
    # if its less than 1, itll also send an error
    if float(price) < MIN_PRICE:
        raise ValueError("Less than 1") 
    
def add_product():
    client.send("ADD_PRODUCT".encode('utf-8'))
    print(client.recv(1024).decode('utf-8'))
    while True:
        try: 
            product_name = input("Product name: ")
            price = input("Price: ")
            priceValidate(price)
            description = input("Description: ")

            client.send(f"{product_name} {price} {description}".encode('utf-8'))
            
            response = client.recv(1024).decode('utf-8')
            if response == "PRODUCT_ADDED":
                print("Product was successfully added.")
            else: print("There was an error in adding your product. Please try again.")
            break
        except ValueError:
            print("ERROR: Please only enter a value greather than or equal to 1$.")
        
    
    
#kind of recursion, do i keep?
def LogOut():
    # TODO remove user from online database from here too
    print("Logging out...)
    client.send("LOGOUT".encode('utf-8'))
    response = client.recv(1024).decode('utf-8')
    if response == "LOGOUT_SUCCESS":
        print("You have been successfully logged out.")
    else:
        print("Error logging out, please try again.")
    handle_client()

def list_products():
    client.send("SEND_PRODUCTS".encode('utf-8'))
    n = int(client.recv(1024).decode('utf-8'))
    client.send("Received number of products".encode('utf-8'))
    
    table = PrettyTable()
    table.field_names = ["Username", "Product Name", "Price (in $)", "Description"]
    for i in range(n):
        temporary = client.recv(1024)
        temporary = pickle.loads(temporary)
        table.add_row([temporary[0], temporary[1], temporary[2], temporary[3]])
    # Print the table
    print(table)
    
    
def getOnlineUsers():
    onlineUsers = client.recv(1024)
    onlineUsers = pickle.loads(onlineUsers)
    
    for i in range(1, len(onlineUsers)+1):
        print(i + "- " + onlineUsers[i-1])
    
def msgGUI():
    print(">>")
    print("Please pick the user you want to message: ")
    getOnlineUsers()
    
def openChat():
    #jds
    print("")
# TODO: receive list of online users
def sendMessage():
    client.send("MSG".encode('utf-8'))
    while True:
        msgGUI()
        
        target = input("")
        client.send(target.encode('utf-8'))
        response = client.recv(1024).decode('utf-8')
        if response == "NOT_ONLINE":
            print("No such user exists")
        elif response =="FOUND":
            openChat()
            
def viewUsersProducts():
    client.send("VIEW_USERS_PRODUCTS".encode('utf-8'))
    client.recv(1024)
    username = input("Enter the username of the user whose products you want to see.")
    client.send(username.encode('utf-8'))
    n1 = (int) (client.recv(1024).decode('utf-8'))
    table = prettyTable()
    table.add_fields("Product Name", "Price (in $)", "Description")
    for i in range(n1):
     temporary = client.recv(1024)
     temporary = pickle.loads(temporary)
     table.add_row(temporary[0], temporary[1], temporary[2])
     
    


        
    
    
def handle_client():
    
    if authentication() == -1:
        client.close()
    else:
        Sign_In_Animation()
        #Now get list of products
        #Display list of options to client 
        f = open("BackEnd/temp.txt")
        lol = f.read()
        print(lol)
        
        while True:
            emptyTerminal()
            list_products()
            print("<<")
            print("1. Add a Product")
            print("2. View Someone's Products")
            print("3. Send Message")
            print("4. Log Out")
            
            choice = input("Enter you choice: ")
            
            if choice == '1':
                add_product()
            elif choice == '2':
                viewUsersProducts()
            elif choice == '3':
                sendMessage()
            elif choice == '4':
                LogOut()
        
handle_client()
