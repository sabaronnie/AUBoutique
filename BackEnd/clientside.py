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

def Login(Limit):
    counter = 0
    #TODO: define blockLOGIN up here somewhere
    #Ensure you can't login if you got blocked for 3 minutes
    blockLOGIN = False
    client.sendall("LOGIN".encode('utf-8'))
    while True: 
        # Get username and password, send it to server, and get response depending on validity
        if counter == Limit:
            if seconds > 0:
                print(f"There are {seconds} seconds left till you can attempt a login again.")
                return "LOGIN_BLOCKED"
            else: counter=0 #Reset the login Block
            
        username = input("Username: ")
        # if Exit(username) == "GO_BACK":
        #     return "GO_BACK"
        client.send(username.encode('utf-8'))
        password = input("Password: ")
        client.sendall(password.encode('utf-8'))
        response = client.recv(1024).decode('utf-8')
        
        
        if response == "CORRECT":
            print("Success! Welcome " + username)
            # Send this client's IP and Port
            client.sendall(f"{clientIP} {clientPort}".encode('utf-8'))
            return "SIGNED_IN"
        elif response == "INVALID_PASSWORD":
            #TODO:  specify invalid what
            print("Invalid Password")
            counter+=1
        elif response == "INVALID_INFO":
            #TODO:  specify invalid what
            print("Invalid Username or Password")
            counter+=1
        if counter == Limit:
            print("You have failed to login way too many times!") 
            print("Please wait 3 minutes to try again.")
            timerThread = threading.Thread(target='Timer', args=(180))
            timerThread.start()


# If successfully login, return out of the function
#Otherwise, stay stuck in it unless u exit
def Exit(text):
    choice = input("Do you want to go back go the main menu? Y/N")
    if choice.lower() == 'y':
        return 0
    elif choice.lower()=='n':
        return 1
    
# def authentication():
#     print("Welcome to AUBoutique")
    
#     exit = False
#     while True: 
#         print("Select action (Pick Number): ")
#         print("1. LOGIN")
#         print("2. REGISTER")
#         print("3. EXIT")
        
#         print("Any time you want to go back to previous menu, type -1")
#         #input validation in gui later
#         choice = int(input(""))
        
#         # MAX Login Attempts   
#         #Technically 3 tries, on the 3th if wrong, says EXCEEDED 
#         LIMIT = 2
#         counter = 0
#         #LOGIN
#         if choice == 1:  
#             if Exit() == 1:
#                 break              
#             response = Login(LIMIT, counter)
            
#             #Ask to back a menu
                    
#             if response == "SIGNED_IN":
#                 print("")
#             elif response == "INVALID_INFO" or response == "LOGIN_BLOCKED":
#                 print("tutu")
            
#         elif choice == 2:
#             if Exit() == 1:
#                 break  
#             if Register() == "ACCOUNT_CREATED":
#                 #exit authentication. now you're logged in, mabrouk
#                 return
                
#         elif choice == 3:
#             break
#             #terminate completely
      
# TODO: do exit type, -1 to extit, or ask to ask after u enter
def authentication():
    print("Welcome to AUBoutique")
    
    exit = False
    while True:
        print("Select action (Pick Number): ")
        print("1. LOGIN")
        print("2. REGISTER")
        print("3. EXIT")
        #input validation in gui later
        choice = int(input(""))
        Limit = 3
        # MAX Login Attempts   
        #Technically 3 tries, on the 3th if wrong, says EXCEEDED 
        
        #LOGIN
        if choice == 1:                
            response = Login(Limit)
            if response == "SIGNED_IN":
                break
            elif response == "INVALID_INFO" or response == "LOGIN_BLOCKED":
                continue
            
        elif choice == 2:
            if Register() == "ACCOUNT_CREATED":
                #exit authentication. now you're logged in, mabrouk
                print("acc created")
                break
                
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
    
    
#kind of recursion, do i keep?
def LogOut():
    handle_client()
    
def handle_client():
    authentication() 
    
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