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
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
import threading

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
        self.users = client.getExistingChats(myusername)[0]
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

        # self.users_list.clicked.connect(self.onUserClick)

        # # Add each user to the list
        # for i, user in enumerate(self.users):
        #     user_item = QListWidgetItem(f"{user}")  # Display name and last message
        #     #user_item.setData(Qt.UserRole, last_messages[i])  # Store the last message for each user
        #     self.users_list.addItem(user_item)
        
        
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
        self.chat_window = MessagingWindow(user, last_message, myusername)
        self.chat_window.show()  # Show the window properly, make sure this is not closed immediately
        
        

class MessagingWindow(QWidget):
    def __init__(self, user, last_message, myusername):
        super().__init__()


        self.user = user
        self.last_message = last_message
        self.setWindowTitle(f"Chat with {self.user}")
        self.setGeometry(100, 100, 400, 600)
        self.setStyleSheet("background-color: #e5ddd5;")  # WhatsApp-style background
        
        # receivingGUI = threading.Thread(target=self.receivetextMessage, args=(self))
        # receivingGUI.start()

        # receivingGUI = threading.Thread(target=self.receivetextMessage)
        # receivingGUI.start()
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.receivetextMessage)
        self.timer.start(100)  

        self.initUI(myusername)
        self.showHistory(self.user, myusername)

    def showContent(self, message, ownUsername):
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
            border-radius: 8px;
            padding: 5px;
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
        
    def initUI(self, myusername):
        # Main layout
        main_layout = QVBoxLayout(self)

        # Scrollable area for messages
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("border: none;")
        
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

    def sendtextMessage(self, myusername):
        # Get the typed message
        message = self.input_field.text().strip()
        
        target = self.user
        username = myusername
        msgtype = "TEXT"
        msgSocket = client.handle_messaging(username, target)
        client.sendChatClient(msgSocket, username, target, msgtype, message)

        if message:  # Only proceed if the message is not empty
            # Create a message box
            message_box = QFrame(self.messages_container)
            message_box.setStyleSheet("""
                background-color: #DCF8C6;
                color: black;
                border-radius: 8px;  /* Smaller corner radius for a tighter look */
                padding: 5px 8px;  /* Reduced padding for a smaller box */
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
            alignment = Qt.AlignRight
                #alignment = Qt.AlignLeft
            self.messages_layout.addWidget(message_box, alignment=alignment)

            # Clear the input field
            self.input_field.clear()

            # Ensure the latest message is visible
            self.scroll_area.verticalScrollBar().setValue(
                self.scroll_area.verticalScrollBar().maximum()
            )
    def display_message(self, message):
            # This method will update the GUI safely in the main thread
            print(f"Displaying message: {message}")

            # Create a message box
            message_box = QFrame(self.messages_container)
            message_box.setStyleSheet("""
                background-color: #DCF8C6;
                color: black;
                border-radius: 8px;
                padding: 5px 8px;
                margin: 2px;
            """)
            message_box.setContentsMargins(0, 0, 0, 0)
            message_box.setFrameShape(QFrame.NoFrame)

            # Add the message text
            message_label = QLabel(message, message_box)
            message_label.setWordWrap(True)
            message_label.setStyleSheet("font-size: 12px; margin: 0;")
            message_label.setMaximumWidth(350)

            # Layout for the message box
            box_layout = QVBoxLayout(message_box)
            box_layout.setContentsMargins(5, 5, 5, 5)
            box_layout.addWidget(message_label)

            # Adjust the size of the message box
            message_box.adjustSize()

            # Add the message box to the layout
            self.messages_layout.addWidget(message_box, alignment=Qt.AlignLeft)

            # Scroll to the latest message
            self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())
            
              
    def receivetextMessage(self):
        # Get the typed message
        # while True:
        message = client.popFromTheMSGQueue() #client.receivedMSG.get()
        self.display_message(message)
        
        #print("CHAT, RECEIVED MSG: " + message)
        #message = message.decode()
        print("BRAVOO SAR MAAK L MSG")
            # if message:  # Only proceed if the message is not empty
            #     print("RICHHHHH")
            #     print("le message "+message)
            #     # Create a message box
            #     message_box = QFrame(self.messages_container)
            #     message_box.setStyleSheet("""
            #         background-color: #DCF8C6;
            #         color: black;
            #         border-radius: 8px;  /* Smaller corner radius for a tighter look */
            #         padding: 5px 8px;  /* Reduced padding for a smaller box */
            #         margin: 2px;  /* Slightly reduced margin */
            #     """)
            #     message_box.setContentsMargins(0, 0, 0, 0)
            #     message_box.setFrameShape(QFrame.NoFrame)

            #     # Add the message text
            #     message_label = QLabel(message, message_box)
            #     message_label.setWordWrap(True)  # Allow wrapping of long text
            #     message_label.setStyleSheet("""
            #         font-size: 12px;  /* Slightly smaller font size */
            #         margin: 0;  /* No margin to tightly fit the text */
            #     """)
                
            #     # Set the maximum width of the message box so the message wraps if it exceeds that width
            #     message_label.setMaximumWidth(350)  # Set a reasonable max width for the message box

            #     # Layout for the message box
            #     box_layout = QVBoxLayout(message_box)
            #     box_layout.setContentsMargins(5, 5, 5, 5)  # Tighten margins for a compact layout
            #     box_layout.addWidget(message_label)

            #     # Adjust the size of the message box based on its content
            #     message_box.adjustSize()

            #     # Align the message box (right alignment for sent messages)
            #     #if (align == "right"):
            #     #alignment = Qt.AlignRight
            #     #else:
            #     alignment = Qt.AlignLeft
            #     self.messages_layout.addWidget(message_box, alignment=alignment)

            #     # Clear the input field
            #     self.input_field.clear()

            #     # Ensure the latest message is visible
            #     self.scroll_area.verticalScrollBar().setValue(
            #         self.scroll_area.verticalScrollBar().maximum()
            #     )
   
    def textMessageHist(self, message, align):


        if message:  # Only proceed if the message is not empty
            # Create a message box
            
            if isinstance(message, bytes):
                message = message.decode('utf-8')

            message_box = QFrame(self.messages_container)
            message_box.setStyleSheet("""
                background-color: #DCF8C6;
                color: black;
                border-radius: 8px;  /* Smaller corner radius for a tighter look */
                padding: 5px 8px;  /* Reduced padding for a smaller box */
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