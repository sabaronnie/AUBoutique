import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, 
    QLineEdit, QPushButton, QLabel, QFrame, QListWidget, QListWidgetItem
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from ..BackEnd import client
from PyQt5.QtCore import QBuffer, QByteArray
#from . import login
from PyQt5.QtCore import QObject, Qt, pyqtSignal, QTimer
import threading
import sqlite3
from ..BackEnd.BackEndSignal import signals
from . import notifications
# users = client.getAllUsers()

# myusername = client.getTheUsername()
# users = client.getExistingChats(myusername)
# print("pRINTING USERS:")
# print(users)
# print("userss")
#last_messages = ["Hello!", "Hey, how's it going?", "Where are you?", "Call me later.", "Let's meet soon!", "How are you?", "What's up?"]  # Example last messages

class MainPage(QWidget):
    def __init__(self, myusername, password):
        super().__init__()
        #myusername = client.getTheUsername()
        self.users = client.getExistingChats(myusername)
        self.setWindowTitle("Users")
        self.setGeometry(100, 100, 400, 600)
        self.setStyleSheet("background-color: #e5ddd5;")  # WhatsApp-style background
        #self.users = client.getExistingChats(self.myusername)
        self.initUI(myusername)

    def initUI(self, myusername):
        # Main layout
        main_layout = QVBoxLayout(self)

        # Scrollable area for users
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("border: none;")
        
        # Container for users
        self.users_container = QWidget()
        self.users_layout = QVBoxLayout(self.users_container)
        self.users_layout.setAlignment(Qt.AlignTop)
        self.scroll_area.setWidget(self.users_container)
        
        # Create a QListWidget to display the users
        self.users_list = QListWidget(self)
        self.users_list.setStyleSheet("background-color: #e5ddd5;") 
        
        for i, user in enumerate(self.users):
            user_item = QListWidgetItem(f"{user}")  # Display name and last message
            # Pass the user name as an argument to the slot
            self.users_list.addItem(user_item)

        self.users_list.clicked.connect(lambda index: self.onUserClick(index, myusername))
        # Add the QListWidget to the layout
        main_layout.addWidget(self.users_list)

        # Set the layout for the widget
        self.setLayout(main_layout)

    def onUserClick(self, index, myusername):
        # Get the clicked user
        user = self.users_list.itemFromIndex(index).text().split(' - ')[0]
        last_message = self.users_list.itemFromIndex(index).data(Qt.UserRole)

        # Open the chat window with the selected user
        client.addToInChat(user)
        self.chat_window = MessagingWindow(user, myusername)
        self.chat_window.show()  # Show the window properly, make sure this is not closed immediately
        
        

class MessagingWindow(QWidget):
    def __init__(self, user, myusername):
        super().__init__()

        self.user = user
        
        self.setWindowTitle(f"Chat with {self.user}")
        self.setGeometry(100, 100, 400, 600)
        self.setStyleSheet("background-color: #e5ddd5;")  # WhatsApp-style background

        signals.new_message.connect(self.receivetextMessage)
        
        self.initUI(myusername)
        self.showHistory(self.user, myusername)
        self.showUnread(self.user, myusername)
        
    

    def showContent(self, message, ownUsername):
        print("SHOWING CONTENT")
        print(message)
        if message[2]=="TEXT":
            if message[0] == ownUsername: #if im the source
                self.textMessageHist(message[3],"right")
            else:
                self.textMessageHist(message[3],"left")
        elif message[2]=="IMG":
            if message[0] == ownUsername: #if im the source
                self.imgMessageHist(message[3],"right")
            else:
                self.imgMessageHist(message[3],"left")
                


            
    def imgMessageHIST(self, msg, alignment):
        """Add an image message to the chat."""
        # Create a frame for the image message
        
        message_box = QFrame()
        message_box.setStyleSheet("""
            background-color: #DCF8C6;
            border-radius: 10px;
            padding: 8px;
            margin: 2px;
        """)
        message_box.setContentsMargins(0, 0, 0, 0)
        message_box.setFrameShape(QFrame.NoFrame)

        # Add the image
        image_label = QLabel(message_box)
        pixmap = QPixmap()
        byte_array = QByteArray(msg)
        buffer = QBuffer(byte_array)
        buffer.open(QBuffer.ReadOnly)
        pixmap.loadFromData(buffer.data())
        
        pixmap = pixmap.scaled(200, 200, aspectRatioMode=1)  # Scale to fit nicely
        image_label.setPixmap(pixmap)


        # Set the maximum width of the message box so the message wraps if it exceeds that width
        message_box.setMaximumWidth(350)  # Set a reasonable max width for the message box

            # Layout for the message box
        box_layout = QVBoxLayout(message_box)
        box_layout.setContentsMargins(5, 5, 5, 5)  # Tighten margins for a compact layout
        box_layout.addWidget(image_label)

        # Adjust the size of the message box based on its content
        message_box.adjustSize()
        
        if (alignment == "right"):
            alignment = Qt.AlignRight
        else:
            alignment = Qt.AlignLeft
        self.messages_layout.addWidget(message_box, alignment=alignment)

 
            
            
    def showHistory(self, myusername, user):
         # [source, destination, message_type, message ]
        history = client.getHistory(user, myusername)
        for message in history:
            self.showContent(message, myusername)
        #self.send_button.clicked.connect(self.sendMessage)
        
    def showUnread(self, myusername, user):
         # [source, destination, message_type, message ]
        unread = client.getUnread(user, myusername)
        if len(unread)==0:
            return
        else:
            unread_separator = QLabel("Unread Chats", self.messages_container)
            unread_separator.setAlignment(Qt.AlignCenter)
            unread_separator.setStyleSheet("""
            color: gray;
            font-style: italic;
            margin: 10px 0;
        """)
            self.messages_layout.addWidget(unread_separator)
            for message in unread:
                notifications.getInfoNotification("Faird", "Incoming Message", self)
                self.textMessageHist(message,"left")
        
    def initUI(self, myusername):
        # Main layout
        main_layout = QVBoxLayout(self)

        # Scrollable area for messages
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet(""" 
            QScrollArea {
                border:none;
            }
            QScrollBar:vertical {
                border: none;  
                background: transparent;  
                width: 6px;  
            }
            QScrollBar::handle:vertical {
                background: gray;  
                min-height: 10px;  
                border-radius: 3px;  
            }
            QScrollBar::handle:vertical:hover {
                background: gray;  
            }
            QScrollBar::handle:vertical:pressed {
                background: gray;  
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;  
                background: none;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;  
            }
        """)
        
        # Container for messages
        self.messages_container = QWidget()
        self.messages_layout = QVBoxLayout(self.messages_container)
        self.messages_layout.setAlignment(Qt.AlignTop)  # Align messages to the top
        self.scroll_area.setWidget(self.messages_container)
        
        main_layout.addWidget(self.scroll_area)
        #self.showHistory(self.user)
        # Display the last message exchanged
        #last_message_label = QLabel(f"Last message: {self.last_message}", self)
        #last_message_label.setStyleSheet("font-size: 14px; color: #555;")
        #main_layout.addWidget(last_message_label)

        # Input field and send button
        input_layout = QHBoxLayout()
        
        self.input_field = QLineEdit(self)
        self.input_field.setStyleSheet("""
            background-color: #36393e;
            border-radius: 10px;
            padding: 10px;
            font-size: 14px;
        """)
        self.input_field.setPlaceholderText("Type your message here...")
       # msgSocket = client.handle_messaging(myusername, self.user)
        self.input_field.returnPressed.connect(lambda: self.sendtextMessage(myusername))
        #self.input_field.returnPressed.connect(self.sendtextMessage)  # Send message on Enter key
        input_layout.addWidget(self.input_field)

        self.send_button = QPushButton("Send", self)
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #075E54;
                color: white;
                font-size: 14px;
                border-radius: 10px;
                padding: 10px 15px;
            }
            QPushButton:hover {
                background-color: #128C7E;
            }
        """)


        input_layout.addWidget(self.send_button)
        self.send_button.clicked.connect(lambda: self.sendtextMessage(myusername))
        main_layout.addLayout(input_layout)


    #do u see this
    def sendtextMessage(self, myusername):
        # Get the typed message
        message = self.input_field.text().strip()
        
        target = self.user
        username = myusername
        msgtype = "TEXT"
        #msgSocket = client.handle_messaging(username, target)
        client.sendChatClient(username, target, msgtype, message)
        print("msg sent to chat client")
        
        self.textMessageHist(message, "right")

        #self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())
            
    
    # def constantlylistenforMessages(username):
    #     ending = b"<END>"
    #     delimiter = b"BRK"
    #     msgHistoryDB = sqlite3.connect('db.msgHistory')
    #     cursor = msgHistoryDB.cursor()

    #     client.P2PServer.listen()
    #     while True:
    #         connection, address = client.P2PServer.accept()
    #         print("ana officially hon ya zabreyete")
    #         #socketList.append(connection)
    #         receive = b""
    #         remaining = b""
    #         #header.encode() + delimiter + f"{username}".encode() + delimiter + f"{message}".encode()
    #         count = 0
    #         while True:
    #             if count < 15:
    #                 print(count)
    #                 print("fetit aal while loop k?")
    #                 print("REMAINING, BEFORE: ")
    #                 print(remaining)
    #             if not remaining:
    #                 remaining += connection.recv(1024)
    #                 if count < 15:
    #                     print("successly received shi farrouj")
    #             else:
    #                 if count< 15:
    #                     print("The REMAINING")
    #                     print(remaining)
                
    #             count+=1

    #             while remaining:
    #                 split_result = remaining.split(ending, 1)
    #                 if count < 15:
    #                     print(split_result)
    #                     print("LENGTH: " + str(len(split_result)))
    #                 if len(split_result) == 1: #if there was no ending
    #                     break
    #                 # If split_result has more than one part, unpack it
    #                 elif len(split_result) == 2:
    #                     receive, remaining = split_result
                        
    #                 #Either TEXT or 
    #                 print("lah ebke")
    #                 msgtype, target, message = receive.split(delimiter, 2)
    #                 msgtype = msgtype.decode('utf-8')
    #                 target = target.decode()
    #                 if count < 15:
    #                     print(msgtype)
    #                     print(target)
    #                     print(message)
    #                     print("BACKEND TARGET:  " + target)
                        
    #                 #temp
    #                 message=message.decode()
    #             # else: 
    #             #target,msgToHandle = connection.recv(1024).decode().split(",") #constListenMSGQueue_R.get().split(",")
    #                 # if message == "EXIT_CHAT":
    #                 #     break
    #                 if target in inChat:
    #                     print("IBNEEE, ANA IN CHAT OF TARGET")
    #                     #call send and receive
    #                     client.receiveChatAVAILABLE(username, target, message) #fix input
    #                 else: #if not in chat
    #                     print(username)
    #                     print(target)
    #                     print(message)
    #                     cursor.execute("INSERT INTO Unread values(?, ?, ?, ?)", (username, target, msgtype, message))
    #                     msgHistoryDB.commit()
              
    def receivetextMessage(self, message):
        # Get the typed message
        # while True:
        # message = client.popFromTheMSGQueue() #client.receivedMSG.get()
        self.textMessageHist(message, "left")
        # self.display_message(message)
        
        #print("CHAT, RECEIVED MSG: " + message)
        #message = message.decode()
        print("BRAVOO SAR MAAK L MSG")
        print(message)

   
    def textMessageHist(self, message, align):
        #print("TEXT MESSAGE HIST")

        if message:  # Only proceed if the message is not empty
            # Create a message box
            
            if isinstance(message, bytes):
                message = message.decode('utf-8')

            print("aam bebaat htis: ")
            print(message)
            message_box = QFrame(self.messages_container)
            message_box.setStyleSheet("""
                background-color: #DCF8C6;
                color: black;
                border-radius: 10px;  /* Smaller corner radius for a tighter look */
                padding: 8px;  /* Reduced padding for a smaller box */
                margin: 2px;  /* Slightly reduced margin */
            """)
            message_box.setContentsMargins(0, 0, 0, 0)
            message_box.setFrameShape(QFrame.NoFrame)

            # Add the message text
            message_label = QLabel(message, message_box)
            message_label.setWordWrap(True)  # Allow wrapping of long text
            message_label.setStyleSheet("""
                font-size: 12px;  /* Slightly smaller font size */
                margin: 0;  /* No margin to tightly fit the text */
            """)
            
            # Set the maximum width of the message box so the message wraps if it exceeds that width
            message_label.setMaximumWidth(350)  # Set a reasonable max width for the message box

            # Layout for the message box
            box_layout = QVBoxLayout(message_box)
            box_layout.setContentsMargins(5, 5, 5, 5)  # Tighten margins for a compact layout
            box_layout.addWidget(message_label)

            # Adjust the size of the message box based on its content
            message_box.adjustSize()

            # Align the message box (right alignment for sent messages)
            if (align == "right"):
                alignment = Qt.AlignRight
            else:
                alignment = Qt.AlignLeft
            self.messages_layout.addWidget(message_box, alignment=alignment)

            # Clear the input field
            self.input_field.clear()

            # Ensure the latest message is visible
            self.scroll_area.verticalScrollBar().setValue(
                self.scroll_area.verticalScrollBar().maximum()
            )
    

if __name__ == "__main__":
    myusername = client.getTheUsername()
    print("pRINTING USERS:")
    #print(users)
    print("userss")
    app = QApplication(sys.argv)
    window = MainPage()
    window.show()
    sys.exit(app.exec_())