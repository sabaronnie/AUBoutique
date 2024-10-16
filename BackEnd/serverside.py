import socket
import threading
import sqlite3
import time
from prettytable import PrettyTable
import pickle
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((socket.gethostbyname(socket.gethostname()), 9999))

db = sqlite3.connect('db.AUBoutique')
db.execute("PRAGMA foreign_keys=on")
cursor = db.cursor()
#hayda l part mafroud ykoun bi while loop in order to take many clients.
#check tahet



#mail lezem tkoun l primary key ahsan

#TABLE INFO:
# - Username always stored in lower case
cursor.execute("CREATE TABLE if not exists Users (name TEXT, mail TEXT UNIQUE, username TEXT PRIMARY KEY UNIQUE, password TEXT)") #name, email address, username, and password.

# ONLINE LIST OF USERS
# contains IP and Port
cursor.execute("CREATE TABLE if not exists Online(username TEXT, ip_address TEXT, port INT, FOREIGN KEY(username) REFERENCES Users(username))") 

# PRODUCT LIST
#ADD IMAGES
cursor.execute("CREATE TABLE if not exists Products(username TEXT, product_name TEXT, price INT, desc TEXT, FOREIGN KEY(username) REFERENCES Users(username))") 
db.commit()
    
def setOnline(username, ip, port, cursor, db):
    cursor.execute("INSERT INTO Online values(?, ?, ?)", (username, ip, port))
    db.commit()
    
# TODO: When you terminate client, or decide to log out, use this
def removeOnline(username):
    cursor.execute("DELETE FROM Online WHERE username=?", (username))
    db.commit()
    
def authentication(connection, address, cursor, db):
    #Get username and password
    while True:
        #Get LOGIN/REGISTER input
        option = connection.recv(1024).decode('utf-8')
        
        if option == "LOGIN":
            username, password = connection.recv(1024).decode('utf-8').split()
                
            #Get user data from the database
            try:      
                #Already checks for username
                cursor.execute("SELECT password FROM Users WHERE username=? ", (username.lower(),))
                print("NOT PASSED YET")
                targetPassword = cursor.fetchall()[0][0] #check that this is not rendered between parentheses.
                print("PASSED HERE")
                
                if  password == targetPassword:
                    connection.sendall("CORRECT".encode('utf-8'))
                    clientIP, clientPort = connection.recv(1024).decode('utf-8').split()
                    # Set signed in user as online
                    setOnline(username, clientIP, clientPort, cursor, db)
                    return username
                else: #Invalid Password
                    connection.sendall("INVALID_PASSWORD".encode('utf-8'))                        
                    counter+=1
            except:
                #if no such account even exists, also say invalid username or password
                # badkon naamela t2oul no suck account exists mnel ekher?
                print("No user with that username exists")
                connection.sendall("INVALID_INFO".encode('utf-8'))
                return -1
                    
                    
        elif option =="REGISTER":
            try:
            # Register then logs you in
            
                name, email, username, password = connection.recv(1024).decode('utf-8').split()
                print(name)
                print(email)
                print(username)
                print(password)
                cursor.execute("INSERT INTO Users values(?, ?, ?, ?)", (name.lower(), email.lower(), username.lower(), password))
                db.commit()
                connection.send("ACCOUNT_CREATED".encode('utf-8'))
                
                
                
                clientIP, clientPort = connection.recv(1024).decode('utf-8').split()
                setOnline(username, clientIP, clientPort, cursor, db)
                
                return username
            except sqlite3.IntegrityError:
                print("Account already exists. Duplicate detected.")
                connection.send("ACCOUNT_ALREADY_EXISTS".encode('utf-8'))
                return -1
        
        
# def addSpaces(file1):
    
def sendProducts(connection):
    #file1 = open("ServerFiles/toBePrinted", 'a')
    #cursor.execute("SELECT * FROM Products")
    #10 spaces
    #file1.write("Username")
    #addSpaces()
    #file1.write("Product Name")        
    #addSpaces()
    #file1.write("Price (in $)")       
    #addSpaces()
    #file1.write("Description")
    # Create a PrettyTable object
    #eemol save now
    #ehh
    #saveeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
    #save now
    #bye
    
    #3melet dw
    #yalla gna test the code hdar
    table = PrettyTable()

    # Define the column names
    connection.send("Alice 25 New_York tete".encode('utf-8'))

    # t1 = cursor.fetchall()
    # file1.write(t1)
    # file1.close()
    # file2 = open("ServerFiles/toBePrinted", 'rb')
    # for lines in file2:
    #     connection.send(lines)
    

                
            
#Handle add product
def add_product(connection, username,cursor,  db):
    try:
        product_name, price, description = connection.recv(1024).decode('utf-8').split()
        print (product_name)
        print(price)
        print(description)
        print(username)
        cursor.execute("INSERT INTO Products VALUES(?, ?, ?, ?)", (username, product_name, float(price), description))
        db.commit()
        connection.send("PRODUCT_ADDED".encode('utf-8'))
    except Exception as e:
        connection.send("ERROR: Cannot ADD product".encode('utf-8'))

def handle_client(connection, address):
    
    db = sqlite3.connect('db.AUBoutique')
    cursor = db.cursor()
    #why did we use this here, and why was it mandatory

    #Acts like assert, doesnt prcoeed until we exit from authentication
    myUsername = authentication(connection, address, cursor, db) 
    if myUsername == -1:
        connection.close()
        return
    
    while True:
        option = connection.recv(1024).decode('utf-8')
        username = myUsername
        
        if option == "ADD_PRODUCT":
            add_product(connection, username, cursor, db)
        elif option == "SEND_PRODUCTS":
            sendProducts(connection)
        #zet l shi la be2e l options (LIST_PRODUCTS, ...)
   
        
        
    

server.listen()
while True:
    connection,address= server.accept()
    server_thread = threading.Thread(target=handle_client, args=(connection, address))
    server_thread.start()
    








