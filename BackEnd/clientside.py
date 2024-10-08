import socket
import threading
import sqlite3

#Port = 9999
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((socket.gethostbyname(socket.gethostname()),9999))




def authentication():
    print("Welcome to AUBoutique")
    
    choice = input("Do you already have an account?")
    if choice == 'y':
        exit = False
        while True:
            client.sendall("LOGIN".encode('utf-8'))
            username = input("Username: ")
            password = input("Password: ")
            client.sendall(f"{username} {password}".encode('utf-8'))
            response = client.recv(1024).decode('utf-8')
            if response == "0":
                print("Success! Welcome " + username)
            elif response == "1":
                print("Invalid Username or Password")
            elif response == "-1":
                print("You have failed to login too many times!")
                print("Please wait 3 minutes to try again.")
                #TODO Figure out how to make a 3 minute timer until you can choose LOGIN again
                break
            
            
            
            
            
    elif choice == 'n':
        client.sendall("REGISTER".encode('utf-8'))
        name = input("Enter you name: ")
        email = input("Enter your email: ")
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        message = f"{name} {email} {username} {password}"
        client.send(message.encode('utf-8'))
    
        

                           
         
    
    