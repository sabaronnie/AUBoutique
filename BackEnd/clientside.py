import socket
import threading
import time

#Port = 9999
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((socket.gethostbyname(socket.gethostname()),9999))

clientIP = client.getsockname()[0]
clientPort = client.getsockname()[1]

def Register():
    client.sendall("REGISTER".encode('utf-8'))
    name = input("Enter you name: ")
    email = input("Enter your email: ")
    username = input("Enter your username: ")
    password = input("Enter your password: ")
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
def add_product():
    product_name = input("Product name: ")
    price = input("Price: ")
    description = input("Description: ")
    client.send("ADD_PRODUCT".encode('utf-8'))
    client.send(f"{product_name} {price} {description}".encode('utf-8'))
    
    
#kind of recursion, do i keep?
def LogOut():
    handle_client()
    
def handle_client():
    
    if authentication() == -1:
        client.close()
    else:
        #Now get list of products
        #Display list of options to client 
        while True:
            print("1. Add a Product")
            print("2. List Products")
            print("3. View Someone's Products")
            print("4. Send Message")
            print("5. Log Out")
            
            choice = input("Enter you choice: ")
            
            if choice == '1':
                add_product()
            elif choice == '4':
                LogOut()
            
        
handle_client()