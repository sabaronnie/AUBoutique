import sys

#sys.path.append("modules") 
import subprocess

subprocess.run([sys.executable, "-m", "pip", "install", "pyqt5"])

import sys
from PyQt5.QtWidgets import QGridLayout, QStackedLayout, QMainWindow, QApplication, QTextEdit, QFrame, QScrollArea, QTableWidgetItem, QFileDialog, QTableWidget, QFormLayout, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QSpinBox, QTabWidget
import PyQt5.QtGui as qtg
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt 

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(0,0,700,500)
        self.setMinimumSize(700, 500) 
        self.initUI()
        
    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setGeometry(700,300,500,500)
    
        piclabel = QLabel(central_widget)
        pixmap = QPixmap("IMAGES/plain-dark-green-wallpaper-4py2q8q4fvne42p7.jpg")
        scaled_pixmap = pixmap.scaled(500, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        piclabel.setPixmap(scaled_pixmap)
        piclabel.setScaledContents(True)  # Allow the image to scale with the label


        rectangle = QLabel()
        #label.setFont(QFont("Arial",50))
        rectangle.setFixedSize(300, 480)
        rectangle.setStyleSheet("""
            background-color: #36393e; 
            box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.9);
            border-radius: 5px;
        """)
        #label.setAlignment(Qt.AlignCenter)
        
        form_layout = QVBoxLayout()
        # form_layout.addRow("Username ", QLineEdit())
        # form_layout.addRow("Password", QLineEdit())
        TopPart = QHBoxLayout()
        # goback = QPushButton("<")
        auboutique = QLabel("Register")
        TopPart.addWidget(auboutique, alignment=Qt.AlignCenter)
        TopPart.setContentsMargins(0, 0, 0, 15) 
        auboutique.setStyleSheet("""
            font-weight: bold;
            font-size: 20px;
        """) 
        
        fullname_layout = QFormLayout()
        fullnameText = QLabel("Full Name")
        fullnameText.setStyleSheet("color: #99aab5; font-weight: bold;")  # Set label color
        fullname = QLineEdit()
        fullname.setFixedSize(250, 30)  # Thinner and longer text box
        fullname.setStyleSheet("""
            QLineEdit {
                background-color: #23272a; 
                color: white; 
                padding-left: 10px; 
                border-radius: 5px;
                border: none;  /* Remove the default border */
                outline: none;  /* Remove the focus outline */
                border: 1px solid transparent;
            }
            
            QLineEdit:focus {
                border: 0 none #FFF;
                overflow: hidden;
                outline:none;
            }

            /* Remove any unwanted focus effect on the widget itself */
            QWidget:focus {
                outline: none;  /* Removes unwanted focus outline on macOS */
            }
        """)
        fullname_layout.addWidget(fullnameText)
        fullname_layout.addWidget(fullname)
        
        
        email_layout = QFormLayout()
        emailText = QLabel("Email")
        emailText.setStyleSheet("color: #99aab5; font-weight: bold;")  # Set label color
        email = QLineEdit()
        email.setFixedSize(250, 30)  # Thinner and longer text box
        email.setStyleSheet("""
            QLineEdit {
                background-color: #23272a; 
                color: white; 
                padding-left: 10px; 
                border-radius: 5px;
                border: none;  /* Remove the default border */
                outline: none;  /* Remove the focus outline */
                border: 1px solid transparent;
            }
            
            QLineEdit:focus {
                border: 0 none #FFF;
                overflow: hidden;
                outline:none;
            }

            /* Remove any unwanted focus effect on the widget itself */
            QWidget:focus {
                outline: none;  /* Removes unwanted focus outline on macOS */
            }
        """)
        email_layout.addWidget(emailText)
        email_layout.addWidget(email)
        
        username_layout = QFormLayout()
        userText = QLabel("Username")
        userText.setStyleSheet("color: #99aab5; font-weight: bold;")  # Set label color
        username = QLineEdit()
        username.setFixedSize(250, 30)  # Thinner and longer text box
        username.setStyleSheet("""
            QLineEdit {
                background-color: #23272a; 
                color: white; 
                padding-left: 10px; 
                border-radius: 5px;
                border: none;  /* Remove the default border */
                outline: none;  /* Remove the focus outline */
                border: 1px solid transparent;
            }
            
            QLineEdit:focus {
                border: 0 none #FFF;
                overflow: hidden;
                outline:none;
            }

            /* Remove any unwanted focus effect on the widget itself */
            QWidget:focus {
                outline: none;  /* Removes unwanted focus outline on macOS */
            }
        """)
        username_layout.addWidget(userText)
        username_layout.addWidget(username)
                
        
        password_layout = QFormLayout()
        passText = QLabel("Password")
        passText.setStyleSheet("color: #99aab5; font-weight: bold;")  # Set label color
        password = QLineEdit()
        password.setFixedSize(250, 30)
        password.setStyleSheet("""
            background-color: #23272a; 
            color: white; 
            padding-left: 10px; 
            border-radius: 5px;
            border: none;  /* Remove the default border */
            outline: none;  /* Remove the focus outline */
        """)
        password_layout.addWidget(passText)
        password_layout.addWidget(password)
        
        
        confirmpass_layout = QFormLayout()
        cpassText = QLabel("Confirm Password")
        cpassText.setStyleSheet("color: #99aab5; font-weight: bold;")  # Set label color
        confirmPassword = QLineEdit()
        confirmPassword.setFixedSize(250, 30)
        confirmPassword.setStyleSheet("""
            background-color: #23272a; 
            color: white; 
            padding-left: 10px; 
            border-radius: 5px;
            border: none;  /* Remove the default border */
            outline: none;  /* Remove the focus outline */
        """)
        confirmpass_layout.addWidget(cpassText)
        confirmpass_layout.addWidget(confirmPassword)
        
        # form_layout.addWidget(username)
        # form_layout.addWidget(password)
        form_layout.addLayout(TopPart)
        form_layout.addLayout(fullname_layout)
        form_layout.addLayout(email_layout)
        form_layout.addLayout(username_layout)
        form_layout.addLayout(password_layout)
        form_layout.addLayout(confirmpass_layout)
        
        
        submit_layout = QFormLayout()
        Empty = QLabel()
        Submit = QPushButton("Register")
        Submit.setFixedSize(250, 30)
        # Login.setStyleSheet("""
        #     background-color: #2c914c; 
        #     box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.9);
        # """)
        Submit.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;  /* Normal state background */
                color: white;
                border: none;
                padding: 5px 20px;
                font-size: 14px;
                border-radius: 5px;
            }
            
            QPushButton:hover {
                background-color: #45a049;  /* Hover state background */
            }
            
            QPushButton:pressed {
                background-color: #388E3C;  /* Pressed state background */
                padding: 12px 22px;  /* Optional: add some effect on click, like a padding change */
            }
        """)
        submit_layout.addWidget(Empty)
        submit_layout.addWidget(Submit)
        form_layout.addLayout(submit_layout)
        
        
        rectangle_layout = QVBoxLayout(rectangle)
        rectangle_layout.addLayout(form_layout)
        # rectangle_layout.addWidget(Submit)
        rectangle_layout.setAlignment(Qt.AlignCenter)
        rectangle_layout.setContentsMargins(0, 0, 15, 0) 
        # rectangle_layout.addWidget(Login)
        # rectangle_layout.addWidget(Register)

        # rectangle.raise_()

        mainlayout = QGridLayout(central_widget)
        mainlayout.addWidget(piclabel, 0, 0)
        mainlayout.addWidget(rectangle, 0, 0, alignment=Qt.AlignCenter)

        mainlayout.setAlignment(rectangle, Qt.AlignCenter)
        # Remove layout margins
        mainlayout.setContentsMargins(0, 0, 0, 0)  # Top, left, bottom, right margins set to 0
        mainlayout.setSpacing(0)  # No spa cing between widgets
        
        central_widget.setStyleSheet("padding: 0px; margin: 0px;")
        central_widget.setLayout(mainlayout)
        
        
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())