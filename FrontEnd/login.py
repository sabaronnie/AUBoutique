import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, pyqtSignal
from . import notifications
from ..BackEnd import client
from . import homepage
import threading


class LoginWindow(QMainWindow):
    dataReady1 = pyqtSignal(dict)
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 700, 500)
        self.setMinimumSize(700, 500)
        self.initUI()
        self.personsCredentials = {}

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Define the background image
        piclabel = QLabel(central_widget)
        pixmap = QPixmap("IMAGES/plain-dark-green-wallpaper-4py2q8q4fvne42p7.jpg")  # Update image path
        scaled_pixmap = pixmap.scaled(500, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        piclabel.setPixmap(scaled_pixmap)
        piclabel.setScaledContents(True)

        # Rectangle for login form
        box_width = 350
        rectangle = QWidget()
        rectangle.setFixedSize(box_width, 300)
        #            box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.9);
        rectangle.setStyleSheet("""
            background-color: #36393e;
            border-radius: 5px;
        """)

        # Form layout inside the rectangle
        form_layout = QVBoxLayout()
        form_layout.setAlignment(Qt.AlignCenter)

        # Username field
        userText = QLabel("Username")
        userText.setStyleSheet("color: #99aab5; font-weight: bold;")
        username = QLineEdit()
        username.setFixedSize(box_width - 50, 40)
        username.setStyleSheet("""
            background-color: #23272a;
            color: white;
            padding-left: 10px;
            border-radius: 5px;
            border: none;
        """)
        

        # Password field
        passText = QLabel("Password")
        passText.setStyleSheet("color: #99aab5; font-weight: bold;")
        password = QLineEdit()
        password.setFixedSize(box_width - 50, 40)
        password.setStyleSheet("""
            background-color: #23272a;
            color: white;
            padding-left: 10px;
            border-radius: 5px;
            border: none;
        """)
        
        password.setEchoMode(QLineEdit.Password)

        # Submit button
        Submit = QPushButton("Login")
        
        
        Submit.setFixedSize(box_width - 50, 40)
        Submit.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 5px 20px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #388E3C;
            }
        """)

        # Add widgets to form layout
        form_layout.addWidget(userText)
        form_layout.addWidget(username)
        form_layout.addWidget(passText)
        form_layout.addWidget(password)
        form_layout.addWidget(Submit)

        # Add form to the rectangle
        rectangle_layout = QVBoxLayout(rectangle)
        rectangle_layout.addLayout(form_layout)
        rectangle_layout.setAlignment(Qt.AlignCenter)
        rectangle_layout.setContentsMargins(0, 10, 0, 10)

        # Main layout
        mainlayout = QVBoxLayout(central_widget)
        mainlayout.addStretch()
        mainlayout.addWidget(piclabel)
        mainlayout.addWidget(rectangle)
        mainlayout.addStretch()
        mainlayout.setAlignment(Qt.AlignCenter)

        central_widget.setStyleSheet("padding: 0px; margin: 0px;")
        central_widget.setLayout(mainlayout)

        Submit.clicked.connect(lambda: self.loginButton(username, password))
    def openMainMenu(self, username, password):
        self.mainmenu = homepage.General1(username.text(), password.text())   
        self.mainmenu.show()    
        
    def loginButton(self, username1, password1):
        global myusername
        credentials = {
        'username' : username1.text(),
          'password' : password1.text()
           }
        self.dataReady1.emit(credentials)

        received = client.Login(username1.text(), password1.text())
        response = received[0]
        triesLeft = received[1]
        if response == "INVALID_INFO":
            notifications.getErrorNotification("Login", "Invalid Username or Password", self)
            return
        elif response == "CORRECT":
            self.openMainMenu(username1, password1)

            
    


            
