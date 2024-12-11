import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, 
    QLineEdit, QPushButton, QLabel, QFrame, QListWidget, QListWidgetItem, QSizePolicy
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

class MainPage(QWidget):
    def __init__(self, myusername, password):
        super().__init__()
        #myusername = client.getTheUsername()
        self.users = client.getExistingChats(myusername)
        self.setWindowTitle("Users")
        self.setGeometry(100, 100, 400, 600)
        self.setStyleSheet("background-color: #e5ddd5;") 
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
        
        self.users_list = QListWidget(self)
        #self.users_list.setStyleSheet("background-color: #e5ddd5;") 
        self.users_list.setStyleSheet("""
            QListWidget {
                background-color: #e5ddd5;
                border: none;
            }
            QListWidget::item {
                background-color: #ffffff;
                border: 1px solid #ddd;
                border-radius: 8px;
                margin: 5px;
                padding: 10px;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
                color: #333;
            }
            QListWidget::item:hover {
                background-color: #f0f0f0;
                border: 1px solid #bbb;
            }
            QListWidget::item:selected {
                background-color: #d4eaf7;
                border: 1px solid #7eb0d5;
            }
        """)
        
        for i, user in enumerate(self.users):
            user_item = QListWidgetItem(f"{user}")  
            self.users_list.addItem(user_item)

        self.users_list.clicked.connect(lambda index: self.onUserClick(index, myusername))
        main_layout.addWidget(self.users_list)

        self.setLayout(main_layout)

    def onUserClick(self, index, myusername):
        # Get the clicked user
        user = self.users_list.itemFromIndex(index).text().split(' - ')[0]
        last_message = self.users_list.itemFromIndex(index).data(Qt.UserRole)

        # Open the chat window with the selected user
        client.addToInChat(user)
        self.chat_window = MessagingWindow(user, myusername)
        self.chat_window.show() 
        
        

class MessagingWindow(QWidget):
    def __init__(self, user, myusername):
        super().__init__()

        self.user = user
        self.setWindowTitle(f"Chat with {self.user}")
        self.setGeometry(100, 100, 400, 600)
        self.setStyleSheet("background-color: #e5ddd5;")  

        signals.new_message.connect(self.receivetextMessage)
        
        self.initUI(myusername)
        self.showHistory(self.user, myusername)
        self.showUnread(self.user, myusername)
        
    def closeEvent(self, event):
        client.removeFromInChat(self.user)

    def showContent(self, message, ownUsername):
        print("SHOWING CONTENT")
        print(message)
        print(ownUsername)
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
        #Add an image message to the chat
        # Create a frame for the image message
        
        message_box = QFrame()
        message_box.setStyleSheet("""
            background-color: #DCF8C6;
            border-radius: 10px;
            padding: 13px;
            margin: 8px;
        """)
        message_box.setContentsMargins(0, 0, 0, 0)
        message_box.setFrameShape(QFrame.NoFrame)

        # the image
        image_label = QLabel(message_box)
        pixmap = QPixmap()
        byte_array = QByteArray(msg)
        buffer = QBuffer(byte_array)
        buffer.open(QBuffer.ReadOnly)
        pixmap.loadFromData(buffer.data())
        
        pixmap = pixmap.scaled(200, 200, aspectRatioMode=1)  # Scale to fit nicely
        image_label.setPixmap(pixmap)


        message_box.setMaximumWidth(350)  


        box_layout = QVBoxLayout(message_box)
        box_layout.setContentsMargins(5, 5, 5, 5)  
        box_layout.addWidget(image_label)

        # Adjust the size of the message box based on its content
        message_box.adjustSize()
        
        if (alignment == "right"):
            alignment = Qt.AlignRight
        else:
            alignment = Qt.AlignLeft
        self.messages_layout.addWidget(message_box, alignment=alignment)

 
            
            
    def showHistory(self, user, myusername):
         # [source, destination, message_type, message ]
        history = client.getHistory(myusername, user)
        prev = ""
        for message in history:
            if message[3] != prev:
                self.showContent(message, myusername)
                prev = message[3]

        
    def showUnread(self, user, myusername):
         # [source, destination, message_type, message ]
        unread = client.getUnread(myusername, user)
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

        

        self.messages_container = QWidget()
        self.messages_layout = QVBoxLayout(self.messages_container)
        self.messages_layout.setAlignment(Qt.AlignTop)  
        self.scroll_area.setWidget(self.messages_container)
        
        main_layout.addWidget(self.scroll_area)

        input_layout = QHBoxLayout()
        
        self.input_field = QLineEdit(self)
        self.input_field.setStyleSheet("""
            background-color: #36393e;
            border-radius: 10px;
            padding: 8px;
            font-size: 14px;
        """)
        self.input_field.setPlaceholderText("Type your message here...")
       # msgSocket = client.handle_messaging(myusername, self.user)
        self.input_field.returnPressed.connect(lambda: self.sendtextMessage(myusername))
        #self.input_field.returnPressed.connect(self.sendtextMessage)  
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
        client.sendChatClient(username, target, msgtype, message)
        self.textMessageHist(message, "right")
        self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())
            
              
    def receivetextMessage(self, message):
        self.textMessageHist(message, "left")
        print(message)

   
    def textMessageHist(self, message, align):

        if message:  # Only proceed if the message is not empty
            # Create a message box
            
            if isinstance(message, bytes):
                message = message.decode('utf-8')

            message_box = QFrame(self.messages_container)
            message_box.setStyleSheet("""
                background-color: #DCF8C6;
                border-radius: 10px;
                padding: 14px;
                margin: 1px;
            """)
            #message_box.setContentsMargins(0, 0, 0, 0)
            message_box.setFrameShape(QFrame.NoFrame)

            # Add the message text
            message_label = QLabel(message, message_box)
            message_label.setWordWrap(True)  
            message_label.setStyleSheet("""
                font-size: 10px;  
                margin: 0; 
                color: black;
                padding: 14px;
            """)
            
            message_label.setMaximumWidth(250) 
            message_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
            message_box.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
            #message_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            #message_label.adjustSize() 

            box_layout = QVBoxLayout(message_box)
            #box_layout.setContentsMargins(5, 5, 5, 5)  
            box_layout.addWidget(message_label)
            
            box_layout.addStretch(1) 
            #box_layout.setContentsMargins(5, 5, 5, 5)
            box_layout.setContentsMargins(0, 0, 0, 0)
            self.messages_layout.setSpacing(5)
            #box_layout.addWidget(message_label)
            #message_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            message_box.adjustSize()

            # Adjust the size of the message box based on its content
           # message_box.adjustSize()

            # Align the message box (right for sent messages)
            if (align == "right"):
                alignment = Qt.AlignRight
            else:
                alignment = Qt.AlignLeft
            self.messages_layout.addWidget(message_box, alignment=alignment)


            # self.messages_layout.update()
            # self.messages_container.updateGeometry()
            self.scroll_area.setWidgetResizable(True) 
            self.scroll_area.verticalScrollBar().setValue(
                self.scroll_area.verticalScrollBar().maximum()
            )
    
            # Clear the input field
            self.input_field.clear()

if __name__ == "__main__":
    myusername = client.getTheUsername()
    app = QApplication(sys.argv)
    window = MainPage()
    window.show()
    sys.exit(app.exec_())