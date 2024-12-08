import sys

#sys.path.append("modules") 
import subprocess

# subprocess.run([sys.executable, "-m", "pip", "install", "pyqt5"])
import sys
from PyQt5.QtWidgets import (QGridLayout, QStackedLayout, QMainWindow, QApplication, QTextEdit, QFrame, QScrollArea, QTableWidgetItem, QFileDialog, QTableWidget, 
QFormLayout, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QSpinBox, QTabWidget, QMessageBox)
import PyQt5.QtGui as qtg
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt 
from .login import LoginWindow 
from .register import RegisterWindow
from .homepage import General1
#import tempclient
#from tempclient import Register
#from tempclient import Login

#TODO:
#make it os you can only open 1 login

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

        # Load the image
        pixmap = QPixmap("AUBoutique/resources/IMAGES/AUB_Oxy.png")

        # Get the original size of the pixmap
        original_width = pixmap.width()
        original_height = pixmap.height()

        # Set maximum size to scale to, but only if the original image is larger than the desired size
        max_width = 1128
        max_height = 750

        # Scale image only if needed (if the original size is larger than max size)
        if original_width > max_width or original_height > max_height:
            scaled_pixmap = pixmap.scaled(max_width, max_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        else:
            scaled_pixmap = pixmap  # Use the original size if the image is already smaller

        # Set the pixmap to the label
        piclabel.setPixmap(scaled_pixmap)

        # No need for setScaledContents(True), let the pixmap handle the scaling
        piclabel.setAlignment(Qt.AlignCenter)  # This centers the image in the label`


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
        # Login.setStyleSheet("""
        #     background-color: #2c914c; 
        #     box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.9);
        # """)
        ##4CAF50
        # #45a049
        
        Login.setStyleSheet("""
            QPushButton {
                background-color: transparent;  /* Normal state background */
                color: black;
                border: none;
                padding: 10px 20px;
                font-size: 18px;
                border-radius: 5px;
                background-color: rgba(255, 255, 255, 0.6);
            }
            
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.8);  /* Slightly translucent white when hovered */
                border: 1px solid rgba(255, 255, 255, 0.5);  /* Add a translucent white border on hover */
            }
            
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.2);  /* Slightly more opaque when pressed */
                padding: 12px 22px;  /* Optional: add some effect on click, like a padding change */
            }
        """)
        
        Register = QPushButton("Register")
        Register.setFixedSize(150, 50)
        Register.setStyleSheet("""
            QPushButton {
                background-color: transparent;  /* Normal state background */
                color: black;
                border: none;
                padding: 10px 20px;
                font-family: Arial;
                font-size: 18px;
                border-radius: 5px;
                background-color: rgba(255, 255, 255, 0.6);  /* Slightly translucent white when hovered */
            }
            
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.8);  /* Slightly translucent white when hovered */
                border: 1px solid rgba(255, 255, 255, 1);  /* Add a translucent white border on hover */
            }
            
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.2);  /* Slightly more opaque when pressed */
                padding: 12px 22px;  /* Optional: add some effect on click, like a padding change */
            }
        """)
        
        rectangle_layout = QVBoxLayout(rectangle)
        rectangle_layout.addWidget(Login, alignment=Qt.AlignHCenter)
        rectangle_layout.addWidget(Register, alignment=Qt.AlignHCenter)
        
        rectangle_layout.setSpacing(0)  # Adjust the spacing between the widgets
       

        mainlayout = QGridLayout(central_widget)
        mainlayout.addWidget(piclabel, 0, 0)
        mainlayout.addWidget(rectangle, 0, 0, alignment=Qt.AlignCenter)

        mainlayout.setAlignment(rectangle, Qt.AlignCenter)
        # Remove layout margins
        mainlayout.setContentsMargins(0, 0, 0, 0)  # Top, left, bottom, right margins set to 0
        mainlayout.setSpacing(0)  # No spa cing between widgets
        
        central_widget.setStyleSheet("padding: 0px; margin: 0px;")
        central_widget.setLayout(mainlayout)
        # Connect the Login button to show LoginWindow
        
            
        Login.clicked.connect(self.showLoginWindow)
        Register.clicked.connect(self.showRegisterWindow)
    def showLoginWindow(self):
            """Show the LoginWindow when login button is clicked"""
            self.login_window = LoginWindow()  # Create an instance of LoginWindow
            self.login_window.show()  
            self.login_window.dataReady1.connect(self.handleLoginData)
    def GeneralPage(self):
        self.GeneralPage = General1()
        self.GeneralPage.show()
        
    def handleLoginData(self, credentials):
        username = credentials['username']
        password = credentials['password']
        print("kifak")
        print("username", username)
        print("password", password)
        
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

        # You can now proceed with the registration logic
        #Answer = Register(fullname, email, username, password)
        #if Answer != "ACCOUNT_CREATED":
        #    self.show_error("There is already an account with this username or email. Please Try again")
        #    return
        #elif Answer == "ACCOUNT_CREATED":
        #    QMessageBox.information(self, "Success", "Registration successful!")
        #    self.GeneralPage() 
    
            
    def showRegisterWindow(self):
        self.registerWindow1 = RegisterWindow()
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
app.setWindowIcon(QIcon("IMAGES/FirstBackground.webp")) 
window = MainWindow()
window.show()
sys.exit(app.exec_())