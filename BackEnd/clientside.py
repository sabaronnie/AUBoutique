import socket
import threading
import time
import os
import pickle
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
    counter = 3
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
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Linux and macOS
        os.system('clear')

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
    while True: 
        # Get username and password, send it to server, and get response depending on validity
        emptyTerminal()
        if counter == LIMIT:
            if seconds > 0:
                print(f"There are {seconds} seconds left till you can attempt a login again.")
                return "LOGIN_BLOCKED"
            else: counter=0 #Reset the login Block
            
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
            print("Invalid Password")
            counter+=1
        elif response == "INVALID_INFO":
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
    while True:
        try: 
            product_name = input("Product name: ")
            price = input("Price: ")
            priceValidate(price)
            description = input("Description: ")
            client.send("ADD_PRODUCT".encode('utf-8'))
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
    handle_client()

def list_products():
    client.send("SEND_PRODUCTS".encode('utf-8'))
    
    #f = open("Reading.txt", 'rb')
    name, age, city, rando = client.recv(1024).decode('utf-8').split()
    # pickle.loads(the_table)
    
    # print(the_table)
    table = PrettyTable()
    table.field_names = ["Username", "Product Name", "Price (in $)", "Description"]

    # Add rows to the table
    table.add_row([name, age, city, rando])
    table.add_row(["Bob", 30, "San Francisco", "etet"])
    table.add_row(["Charlie", 35, "Chicago", "jre"])

    # Print the table
    print(table)
    
    
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
            list_products()
            print("<<")
            print("1. Add a Product")
            print("2. View Someone's Products")
            print("3. Send Message")
            print("4. Log Out")
            
            choice = input("Enter you choice: ")
            
            if choice == '1':
                add_product()
            elif choice == '4':
                LogOut()
            
        
handle_client()