import socket
import threading
import time

#Port = 9999
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((socket.gethostbyname(socket.gethostname()),9999))

clientIP = socket.getsockname()[0]
clientPort = socket.getsockname()[1]

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
        client.sendall(f"{clientIP} {clientPort}".encode('utf-8'))
        return response
    elif response == "ALREADY_EXISTS":
        print("Account already exists. Either login or use a different email or username.")
        return ""
        
def Login(LIMIT, counter):
    #Ensure you can't login if you got blocked for 3 minutes
    if blockLOGIN == True:
        if seconds > 0:
            print(f"There are {seconds} seconds left till you can attempt a login again.")
            return "LOGIN_BLOCKED"
        else: blockLOGIN = False #Reset the login Block
        
    client.sendall("LOGIN".encode('utf-8'))
    
    # Get username and password, send it to server, and get response depending on validity
    username = input("Username: ")
    password = input("Password: ")
    client.sendall(f"{username} {password}".encode('utf-8'))
    response = client.recv(1024).decode('utf-8')
    
    if response == "0":
        print("Success! Welcome " + username)
        # Send this client's IP and Port
        client.sendall(f"{clientIP} {clientPort}".encode('utf-8'))
        return "SIGNED_IN"
    elif counter == LIMIT:
        print("You have failed to login too many times!") 
        print("Please wait 3 minutes to try again.")
        blockLOGIN = True
        timerThread = threading.Thread(target="Timer", args=(180))
        timerThread.start()
        counter = 0
        return -1
    elif response == "INVALID_INFO":
        print("Invalid Username or Password")
        counter+=1

# If successfully login, return out of the function
#Otherwise, stay stuck in it unless u exit
seconds = 0
def Timer (countDown):
    seconds = countDown
    while seconds > 0:
        time.sleep(1)
        seconds=-1

def authentication():
    print("Welcome to AUBoutique")
    
    exit = False
    while True:
        print("Select action (Pick Number): ")
        print("1. LOGIN")
        print("2. REGISTER")
        print("3. EXIT")
        choice = input("")
        
        # MAX Login Attempts   
        #Technically 3 tries, on the 3th if wrong, says EXCEEDED 
        LIMIT = 2
        counter = 0
        #LOGIN
        if choice == 1:                
            response = Login(LIMIT, counter)
            if response == "SIGNED_IN":
                break
            elif response == "INVALID_INFO" or response == "LOGIN_BLOCKED":
                continue
            
        elif choice == 2:
            if Register() == "ACCOUNT_CREATED":
                #exit authentication. now you're logged in, mabrouk
                return
                
        elif choice == 3:
            #terminate completely
            break

#mnaamel handling functions la kel choice w mnerjaa mnaamella call bel main function tahet
def add_product():
    product_name = input("Product name: ")
    price = input("Price: ")
    description = input("Description: ")
    client.send("ADD_PRODUCT".encode('utf-8'))
    client.send(f"{product_name} {price} {description}".encode('utf-8'))
    
def handle_client():
    authentication() 
    
    #Now get list of products
    #Display list of options to client 
    while True:
        print("1. Add a Product")
        print("2. List Products")
        print("3. List products")
        print("4. Send Message")
        print("5. Log Out")
        
        choice = input("Enter you choice: ")
        
        if choice == '1':
            add_product()
        

                           
         
    
    