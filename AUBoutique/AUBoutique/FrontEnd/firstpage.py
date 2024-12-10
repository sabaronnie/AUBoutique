import sys

#sys.path.append("modules") 
import subprocess


import sys
from PyQt5.QtWidgets import (QGridLayout, QStackedLayout, QMainWindow, QApplication, QTextEdit, QFrame, QScrollArea, QTableWidgetItem, QFileDialog, QTableWidget, 
QFormLayout, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QSpinBox, QTabWidget, QMessageBox)
import PyQt5.QtGui as qtg
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt 
from .login import LoginWindow 
from .register import RegisterWindow
from .homepage import General1




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(0,0,700,500)
        self.setMinimumSize(1128, 750) 
        self.initUI()
        
    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setGeometry(700,300,500,500)
    
        piclabel = QLabel(central_widget)


        pixmap = QPixmap("AUBoutique/resources/IMAGES/AUB_Oxy.png")


        original_width = pixmap.width()
        original_height = pixmap.height()

        self.setMaximumSize(original_width, original_height)
       
        max_width = 1128
        max_height = 750


        if original_width > max_width or original_height > max_height:
            scaled_pixmap = pixmap.scaled(max_width, max_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        else:
            scaled_pixmap = pixmap  


        piclabel.setPixmap(scaled_pixmap)


        piclabel.setAlignment(Qt.AlignCenter) 


        rectangle = QLabel()
        #label.setFont(QFont("Arial",50))
        rectangle.setFixedSize(300, 300)
        ##36393e
        #box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.9);
        rectangle.setStyleSheet("""
            background-color: transparent; 
            border-radius: 5px;
        """)
        #label.setAlignment(Qt.AlignCenter)
        
        Login = QPushButton("Login")
        Login.setFixedSize(150, 50)

        Login.setStyleSheet("""
            QPushButton {
                background-color: transparent;  
                color: black;
                border: none;
                padding: 10px 20px;
                font-size: 18px;
                border-radius: 5px;
                background-color: rgba(255, 255, 255, 0.6);
            }
            
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.8);  
                border: 1px solid rgba(255, 255, 255, 0.5);
            }
            
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.2);  
                padding: 12px 22px; 
            }
        """)
        
        Register = QPushButton("Register")
        Register.setFixedSize(150, 50)
        Register.setStyleSheet("""
            QPushButton {
                background-color: transparent; 
                color: black;
                border: none;
                padding: 10px 20px;
                font-family: Arial;
                font-size: 18px;
                border-radius: 5px;
                background-color: rgba(255, 255, 255, 0.6);  
            }
            
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.8);  
                border: 1px solid rgba(255, 255, 255, 1); 
            }
            
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.2); 
                padding: 12px 22px;  
            }
        """)
        
        rectangle_layout = QVBoxLayout(rectangle)
        rectangle_layout.addWidget(Login, alignment=Qt.AlignHCenter)
        rectangle_layout.addWidget(Register, alignment=Qt.AlignHCenter)
        
        rectangle_layout.setSpacing(0)  
       

        mainlayout = QGridLayout(central_widget)
        mainlayout.addWidget(piclabel, 0, 0)
        mainlayout.addWidget(rectangle, 0, 0, alignment=Qt.AlignCenter)

        mainlayout.setAlignment(rectangle, Qt.AlignCenter)
        # Remove layout margins
        mainlayout.setContentsMargins(0, 0, 0, 0)  
        mainlayout.setSpacing(0) 
        
        central_widget.setStyleSheet("padding: 0px; margin: 0px;")
        central_widget.setLayout(mainlayout)
        # Connect the Login button to show LoginWindow
        
            
        Login.clicked.connect(self.showLoginWindow)
        Register.clicked.connect(self.showRegisterWindow)
    def showLoginWindow(self):
            """Show the LoginWindow when login button is clicked"""
            self.login_window = LoginWindow(self)  
            self.login_window.show()  
            self.login_window.dataReady1.connect(self.handleLoginData)
    def GeneralPage(self):
        self.GeneralPage = General1()
        self.GeneralPage.show()
        
    def handleLoginData(self, credentials):
        username = credentials['username']
        password = credentials['password']

        
    def handleRegistrationData(self, user_data):
        # This method will be called once the data is ready
        fullname = user_data['fullname']
        email = user_data['email']
        username = user_data['username']
        password = user_data['password']
        # Now you can use the user data
        print("Full Name:", fullname)
        print("Email:", email)
        print("Username:", username)
        print("Password:", password)

        
        #Answer = Register(fullname, email, username, password)
        #if Answer != "ACCOUNT_CREATED":
        #    self.show_error("There is already an account with this username or email. Please Try again")
        #    return
        #elif Answer == "ACCOUNT_CREATED":
        #    QMessageBox.information(self, "Success", "Registration successful!")
        #    self.GeneralPage() 
    
            
    def showRegisterWindow(self):
        self.registerWindow1 = RegisterWindow(self)
        self.registerWindow1.show() 
        #self.registerWindow1.dataReady.connect(self.handleRegistrationData)
        
        #Answer = Register(fullname, email, username, password)
        #if Answer != "ACCOUNT_CREATED":
        #    self.show_error("There is already an account with this username or email. Please Try again")
        #    return
        #elif Answer == "ACCOUNT_CREATED":
        #   QMessageBox.information(self, "Success", "Registration successful!")
        #   self.GeneralPage()


app = QApplication(sys.argv)
app.setWindowIcon(QIcon("AUBoutique/resources/IMAGES/AppIcon.jpeg")) 
window = MainWindow()
window.show()
sys.exit(app.exec_())