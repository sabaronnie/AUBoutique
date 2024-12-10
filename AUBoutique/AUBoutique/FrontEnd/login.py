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
    def __init__(self, firstpage):
        super().__init__()
        self.setGeometry(0, 0, 700, 500)
        self.setMinimumSize(700, 500)
        self.initUI(firstpage)
        self.personsCredentials = {}

    def initUI(self, firstpage):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        piclabel = QLabel(central_widget)
        pixmap = QPixmap("IMAGES/plain-dark-green-wallpaper-4py2q8q4fvne42p7.jpg")  # Update image path
        scaled_pixmap = pixmap.scaled(500, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        piclabel.setPixmap(scaled_pixmap)
        piclabel.setScaledContents(True)

        box_width = 350
        rectangle = QWidget()
        rectangle.setFixedSize(box_width, 300)
        rectangle.setStyleSheet("""
            background-color: #36393e;
            border-radius: 5px;
        """)

        form_layout = QVBoxLayout()
        form_layout.setAlignment(Qt.AlignCenter)

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

        Submit = QPushButton("Login")
        
        
        Submit.setFixedSize(box_width - 50, 40)
        Submit.setStyleSheet("""
            QPushButton {
                background-color: #34495e;
                color: white;
                border: none;
                padding: 5px 20px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #4c79a6;
            }
            QPushButton:pressed {
                background-color: ##639fdb;
            }
        """)

        form_layout.addWidget(userText)
        form_layout.addWidget(username)
        form_layout.addWidget(passText)
        form_layout.addWidget(password)
        form_layout.addWidget(Submit)

        rectangle_layout = QVBoxLayout(rectangle)
        rectangle_layout.addLayout(form_layout)
        rectangle_layout.setAlignment(Qt.AlignCenter)
        rectangle_layout.setContentsMargins(0, 10, 0, 10)

        mainlayout = QVBoxLayout(central_widget)
        mainlayout.addStretch()
        mainlayout.addWidget(piclabel)
        mainlayout.addWidget(rectangle)
        mainlayout.addStretch()
        mainlayout.setAlignment(Qt.AlignCenter)

        central_widget.setStyleSheet("padding: 0px; margin: 0px;")
        central_widget.setLayout(mainlayout)

        Submit.clicked.connect(lambda: self.loginButton(username, password, firstpage))
    def openMainMenu(self, username, password):
        self.mainmenu = homepage.General1(username.text(), password.text())   
        self.mainmenu.show()    
        
    def loginButton(self, username1, password1, firstpage):
        global myusername
        
        if not username1.text() or not password1.text():
            notifications.getErrorNotification("Login", "Please fill in all the fields.", self)
            return
        
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
            self.close()
            firstpage.close()

            
    


            
