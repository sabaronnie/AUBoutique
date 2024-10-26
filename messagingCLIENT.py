import socket
import threading
import time
import os
import sys
import pickle
from datetime import date, timedelta
#yalla btjarib l 2 clients?



sys.path.append("modules") 

from prettytable import PrettyTable

#Port = 9999
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((socket.gethostbyname(socket.gethostname()),8888))

clientIP = client.getsockname()[0]
clientPort = client.getsockname()[1]

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

seconds = 0
def Timer (countDown):
    seconds = countDown
    while seconds > 0:
        time.sleep(1)
        seconds-=1
        
def Login(LIMIT):
    counter = 0

    # client.sendall("LOGIN".encode('utf-8'))
    invalidPassword = False
    while True: 
        # Get username and password, send it to server, and get response depending on validity
        #emptyTerminal()

        # if counter == LIMIT:
            # if seconds > 0:
            #     print(f"There are {seconds} seconds left till you can attempt a login again.")
            #     return "LOGIN_BLOCKED"
            # else: counter=0 #Reset the login Block
            
        # username = input("Username: ")
        # password = input("Password: ")
        
        #AUTO SIGN IN
        username = "ron"
        password = "12345678"
        
        # client.sendall(f"{username} {password}".encode('utf-8'))
    
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
            timerThread = threading.Thread(target=Timer, args=(180))
            timerThread.start()


def getOnlineUsers():
    print("uh")
    onlineUsers = client.recv(1024)
    print("bruv")
    onlineUsers = pickle.loads(onlineUsers)
    print("WHYYYY")
    for i in range(1, len(onlineUsers)+1):
        print(i + "- " + onlineUsers[i-1])
    
def msgGUI(USER_UNAVAILABLE):
    print(">>")
    print("Pick the user to message (or type 'exit' to cancel):")
    getOnlineUsers()
    
    print()
    if USER_UNAVAILABLE:
        print("The user you previously selected is no longer available")
        return -1
    return 0
    
def sendChat(target):
    print(">>> ", target.upper())
    print("Chat opened. Type 'exit' to close the chat.")
    print("sendCHATTT")
    while True:
        message = input("Enter: ")
        if message.lower() == "exit": 
            client.sendall("EXIT_CHAT".encode('utf-8'))
            break
        else:
            print("You: ", message)
            client.sendall(message.encode('utf-8'))
        
                
        
    
    print("")
    
def receiveChat(target):
    print("receiveCHATTT")
    while True:
        response = client.recv(1024).decode('utf-8')
        if response == "EXIT_CHAT":
            print("User has left the chat.")
            break
        print(target + ": " + response)
    
    
    
def listenForIncomingChatRequest():
    while True:
        while True:
            try:
                senderUser = client.recv(1024).decode('utf-8') #do timeout later TODO
                break
            except Exception as e:
                print(type(e).__name__)
                
        
        print("INCOMING..")
        print(senderUser + " would like to open a chat with you.")
        print("Would you like to accept? Y/N")
        choice = input("")
        #do input validation here
        if choice.lower() == "y":
            client.sendall("REQUEST_ACCEPTED".encode('utf-8'))
            #sending_thread = threading.Thread(target=sendChat, args=(senderUser,))
            receiving_thread = threading.Thread(target=receiveChat, args=(senderUser,))
            #sending_thread.start()
            receiving_thread.start()

            
        #get signal from server that ronnie wants to open chat
        #get ronnies name
        
        #now open the chat
        #if ronnie sends msg, see it
        # if i send msg, send it to ronnie

def handle_messaging():
    #client.sendall("MSG".encode('utf-8'))
    USER_UNAVAILABLE = False
    while True:
        print(">> MESSAGING")
        print("1. Open a chat with someone")
        print("2. Accept an incoming chat request")
        option = input("")

        #do input validation here later
        if option == "1":
            client.sendall("INITIATE_CHAT".encode('utf-8'))
            if msgGUI(USER_UNAVAILABLE) == -1:
                USER_UNAVAILABLE = False
            
            print("kkkkkkkk")
            target = input("")
            if target.lower() == "exit": #Exit if user cancels
                return
            client.sendall(target.encode('utf-8')) #Send target username to server
            response = client.recv(1024).decode('utf-8')
            
            if response == "NOT_ONLINE":
                print("The selected user is not currently online. Please choose another user.")
            elif response =="FOUND":
                # response = client.recv(1024).decode('utf-8')
                #if the user went unavailable since u last printed the table
                # if response == "USER_UNAVAILABLE":
                #     USER_UNAVAILABLE = True
                #     continue
                
                #Send a chat request
                sending_thread = threading.Thread(target=sendChat, args=(target,))
                #receiving_thread = threading.Thread(target=receiveChat, args=(target,))
                sending_thread.start()
                #receiving_thread.start()
        elif option == "2":
            print("ok chosen 2")
            client.sendall("LISTEN_FOR_CHAT".encode('utf-8'))
            print("send the signal")
            listenForIncomingChatRequest()
            
            
def handle_client():
    
    if authentication() == -1:
        client.close()
    else:
        
        while True:
            print("listproducts bro")
            #list_products()
            print("<<")
            print("1. Add a Product")
            print("2. View Someone's Products")
            print("3. Send Message")
            print("4. Buy a Product")
            print("5. Log Out")
            
            choice = input("Enter you choice: ")

            if choice == '3':
                handle_messaging()
        
handle_client()