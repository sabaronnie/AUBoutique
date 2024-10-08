import socket
import threading
import sqlite3
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((socket.gethostbyname(socket.gethostname()), 9999))

db = sqlite3.connect('db.AUBoutique')
cursor = db.cursor()
#hayda l part mafroud ykoun bi while loop in order to take many clients.
#check tahet



#mail lezem tkoun l primary key ahsan

#TABLE INFO:
# - Username always stored in lower case
cursor.execute("CREATE TABLE if not exists Users (name TEXT, mail TEXT PRIMARY KEY, username TEXT, password TEXT)") #name, email address, username, and password.



    
    
def authentication(connection, address):
    #Get username and password
    while True:
        option = connection.recv(1024).decode('utf-8')
        if option == "LOGIN":
            LIMIT = 3
            counter = 0
            #Technically 4 tries, on the 4th if wrong, says EXCEEDED
            while True:
                username, password = connection.recv(1024).decode('utf-8').split()
                
                #aywa shab el TODOOOO HAHAHAAHAHAHAHAHA
                #ossa kb
                # eh wer walaw
                #TODO: GET SQL DATA FOR USERNAME and PASSWORD
                
                cursor.execute("SELECT username, password FROM Users WHERE username=? ", (username.lower(),))

                
                targetUsername, targetPassword = cursor.fetchall()
                if username == targetUsername and password == targetPassword:
                    connection.sendall("0".encode('utf-8'))
                    return
                elif counter == LIMIT:
                    connection.sendall("-1".encode('utf-8'))
                    break
                else: #Invalid Username or Password
                    connection.sendall("1".encode('utf-8'))
                    counter+=1
                    
                    
        elif option =="REGISTER":
            name, email, username, password = connection.recv(1024).decode('utf-8').split()`
    
    
def handle_client(connection, address):
    
    #First authenticate 
    authentication(connection, address)  

server.listen()
while True:
    connection,address= server.accept()
    server_thread = threading.Thread(target="handle_client", args=("connection", "address"))
    server_thread.start()
    



