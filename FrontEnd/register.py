import sys
import subprocess
import queue
from . import notifications
import time
from PyQt5.QtCore import QTimer
subprocess.run([sys.executable, "-m", "pip", "install", "pyqt5"])

from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, 
    QPushButton, QFormLayout, QHBoxLayout, QTextEdit, QMessageBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, pyqtSignal
import re
from .homepage import General1
from ..BackEnd import client
from . import notifications
#import tempclient
class RegisterWindow(QMainWindow):
    #dataReady = pyqtSignal(dict)
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 700, 500)
        self.setMinimumSize(800, 522)
        self.initUI()
        self.userInformation  = {}
        
        #self.theQueues = {'fullname' : queue.Queue(), 'email': queue.Queue(), 'username' : queue.Queue(), 'password': queue.Queue()}
    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Error info box
        errorText = """
        Passwords must contain at least 8 characters and 
        a maximum of 64 characters
        
        Passwords must meet all of the following conditions:
        - English Letters (A, B, C, ... Z or a, b, c, ... z)
        - Westernized Arabic Numerals (0, 1, 2, ... 9)
        - Non-alphanumeric (~!@#$%^&*_-+=`|(){}[]:;”‘<>,.?/)
        """
        actualText = QTextEdit()
        actualText.setStyleSheet("""
            background-color: red;
            color: white;
            font-size: 16px;
            border-radius: 5px;            
        """)
        actualText.setReadOnly(True)
        actualText.setFixedSize(450, 270)
        actualText.setText(errorText)
        actualText.setAlignment(Qt.AlignCenter)

        # Background image
        piclabel = QLabel(central_widget)
        pixmap = QPixmap("IMAGES/plain-dark-green-wallpaper-4py2q8q4fvne42p7.jpg")
        scaled_pixmap = pixmap.scaled(500, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        piclabel.setPixmap(scaled_pixmap)
        piclabel.setScaledContents(True)

        # Register Form Area
        rectangle = QLabel()
        rectangle.setFixedSize(300, 480)
        #            box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.9);
        rectangle.setStyleSheet("""
            background-color: #36393e;
            border-radius: 5px;
        """)

        form_layout = QVBoxLayout()
        TopPart = QHBoxLayout()
        auboutique = QLabel("Register")
        TopPart.addWidget(auboutique, alignment=Qt.AlignCenter)
        TopPart.setContentsMargins(0, 0, 0, 15) 
        auboutique.setStyleSheet("""
            font-weight: bold;
            font-size: 20px;
        """) 

        # Full Name Field
        fullname_layout = QFormLayout()
        fullnameText = QLabel("Full Name")
        fullnameText.setStyleSheet("color: #99aab5; font-weight: bold;")
        fullname = QLineEdit()
        fullname.setFixedSize(250, 30)
        fullname.setStyleSheet("""
            background-color: #23272a; 
            color: white; 
            padding-left: 10px; 
            border-radius: 5px;
            border: none;
        """)
        fullname_layout.addWidget(fullnameText)
        fullname_layout.addWidget(fullname)

        # Email Field
        email_layout = QFormLayout()
        emailText = QLabel("Email")
        emailText.setStyleSheet("color: #99aab5; font-weight: bold;")
        email = QLineEdit()
        email.setFixedSize(250, 30)
        email.setStyleSheet("""
            background-color: #23272a; 
            color: white; 
            padding-left: 10px; 
            border-radius: 5px;
            border: none;
        """)
        email_layout.addWidget(emailText)
        email_layout.addWidget(email)

        # Username Field
        username_layout = QFormLayout()
        userText = QLabel("Username")
        userText.setStyleSheet("color: #99aab5; font-weight: bold;")
        username = QLineEdit()
        username.setFixedSize(250, 30)
        username.setStyleSheet("""
            background-color: #23272a; 
            color: white; 
            padding-left: 10px; 
            border-radius: 5px;
            border: none;
        """)
        username_layout.addWidget(userText)
        username_layout.addWidget(username)

        # Password Field
        password_layout = QFormLayout()
        passText = QLabel("Password")
        passText.setStyleSheet("color: #99aab5; font-weight: bold;")
        password = QLineEdit()
        password.setFixedSize(250, 30)
        password.setEchoMode(QLineEdit.Password)  # Hide password characters
        password.setStyleSheet("""
            background-color: #23272a; 
            color: white; 
            padding-left: 10px; 
            border-radius: 5px;
            border: none;
        """)
        password_layout.addWidget(passText)
        password_layout.addWidget(password)

        # Confirm Password Field
        confirmpass_layout = QFormLayout()
        cpassText = QLabel("Confirm Password")
        cpassText.setStyleSheet("color: #99aab5; font-weight: bold;")
        confirmPassword = QLineEdit()
        confirmPassword.setFixedSize(250, 30)
        confirmPassword.setEchoMode(QLineEdit.Password)  # Hide password characters
        confirmPassword.setStyleSheet("""
            background-color: #23272a; 
            color: white; 
            padding-left: 10px; 
            border-radius: 5px;
            border: none;
        """)
        confirmpass_layout.addWidget(cpassText)
        confirmpass_layout.addWidget(confirmPassword)

        # Add all fields to form layout
        form_layout.addLayout(TopPart)
        form_layout.addLayout(fullname_layout)
        form_layout.addLayout(email_layout)
        form_layout.addLayout(username_layout)
        form_layout.addLayout(password_layout)
        form_layout.addLayout(confirmpass_layout)

        # Submit Button
        submit_layout = QFormLayout()
        Empty = QLabel()
        Submit = QPushButton("Register")
        Submit.setFixedSize(250, 30)
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
        submit_layout.addWidget(Empty)
        submit_layout.addWidget(Submit)
        form_layout.addLayout(submit_layout)

        # Add layout to rectangle
        rectangle_layout = QVBoxLayout(rectangle)
        rectangle_layout.addLayout(form_layout)
        rectangle_layout.setAlignment(Qt.AlignCenter)
        rectangle_layout.setContentsMargins(0, 0, 15, 0)

        # Main layout
        problem_layout = QHBoxLayout()
        problem_layout.addWidget(rectangle, alignment=Qt.AlignCenter)
        problem_layout.addWidget(actualText, alignment=Qt.AlignCenter)
        problem_layout.setSpacing(15)

        mainlayout = QVBoxLayout(central_widget)
        mainlayout.addWidget(piclabel)
        mainlayout.addLayout(problem_layout)
        central_widget.setLayout(mainlayout)

        # Connect button click to validate inputs
        Submit.clicked.connect(lambda: self.validate_inputs(fullname, email, username, password, confirmPassword))
        
        
    def openMainMenu(self):
        self.mainmenu = General1()   
        self.mainmenu.show()
        
    
    def validate_inputs(self, fullname, email, username, password, confirmPassword):
        """Validate the inputs for all fields.""" 
        # Check if any of the fields are empty
        if not fullname.text() or not email.text() or not username.text() or not password.text() or not confirmPassword.text():
            notifications.getErrorNotification("Register", "Please fill in all the fields.", self)
            return

        # Check if the email ends with "@mail.aub.edu"
        if not email.text().endswith("@mail.aub.edu"):
            notifications.getErrorNotification("Register", "The email you just entered is not an AUB email.", self)
            
            return

        # Check if the username starts with a special character
        if re.match(r'^[~!@#$%^&*_\-+=`|(){}[\]:;"\'<>,.?/]', username.text()):
            notifications.getErrorNotification("Register", "Username cannot start with a special character.", self)
            return

        # Check if passwords match
        if password.text() != confirmPassword.text():
            notifications.getErrorNotification("Register", "Passwords do not match", self)
            return
        if password.text().isalpha():
            notifications.getErrorNotification("Register", "Password cannot be alphabetical only", self)
            return
        if password.text().isdigit():
            notifications.getErrorNotification("Register", "Password cannot be numerical only", self)
            return
        # user_data = {
        #     'fullname': fullname.text(),
        #     'email': email.text(),
        #     'username': username.text(),
        #     'password': password.text()
        # }
       # self.dataReady.emit(user_data)
        
        
        self.userInformation['fullname'] = fullname
        self.userInformation['email'] = email
        self.userInformation['username'] = username
        self.userInformation['password'] = password
        print("cr")
        Answer = client.Register(fullname.text(), email.text(), username.text(), password.text())
        print("flyer")
        if Answer != "ACCOUNT_CREATED":
           print("flyer1")
           self.show_error("There is already an account with this username or email. Please Try again")
           return
        elif Answer == "ACCOUNT_CREATED":
            print("flyer2")
            
            notifications.getInfoNotification("Creating Your Account...", "", self)
            QTimer.singleShot(2000, lambda: self.finalize_account_creation())

    def finalize_account_creation(self):
        notifications.getInfoNotification("Finalizing Details...", "", self)

        # Use QTimer for the second delay
        QTimer.singleShot(5000, lambda: self.openMainMenu())
            # QMessageBox.information(self, "Success", "Registration successful!")
                #need to open a new page here.

    def show_error(self, message):
        """Show an error message box.""" 
        QMessageBox.critical(self, "Error", message)
