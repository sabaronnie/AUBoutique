import socket
import threading
import time
#Port = 9999
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((socket.gethostbyname(socket.gethostname()),9999))


def Login(LIMIT, counter):
        
    client.sendall("LOGIN".encode('utf-8'))
    
    # Get username and password, send it to server, and ger response depending on validity
    username = input("Username: ")
    password = input("Password: ")
    client.sendall(f"{username} {password}".encode('utf-8'))
    response = client.recv(1024).decode('utf-8')
    
    if response == "0":
        print("Success! Welcome " + username)
        return 0
    elif counter == "LIMIT":
        print("You have failed to login too many times!") 
        print("Please wait 3 minutes to try again.")
        blockLOGIN = True
        timerThread = threading.Thread(target="Timer", args=(180))
        timerThread.start()
        counter = 0
        break -1
    elif response == "1":
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
        
        if choice == 1:
            
        #Ensure you can't login if you got blocked for 3 minutes
        if blockLOGIN == True:
            if seconds > 0:
                print(f"There are {seconds} seconds left till you can attempt a login again.")
                continue
            else: blockLOGIN = False #Reset the login Block
        Login(LIMIT, counter)
            
            
            
            
            
        elif choice == 'n':
            client.sendall("REGISTER".encode('utf-8'))
            name = input("Enter you name: ")
            email = input("Enter your email: ")
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            message = f"{name} {email} {username} {password}"
            client.send(message.encode('utf-8'))
        
        

                           
         
    
    