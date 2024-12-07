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
        self.setMinimumSize(1128, 750) 
        self.initUI()
        
    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setGeometry(700,300,500,500)
    
        piclabel = QLabel(central_widget)
        pixmap = QPixmap("IMAGES/AUB_Oxy.png")
        scaled_pixmap = pixmap.scaled(500, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        piclabel.setPixmap(scaled_pixmap)
        piclabel.setScaledContents(True)  # Allow the image to scale with the label


        rectangle = QLabel()
        #label.setFont(QFont("Arial",50))
        rectangle.setFixedSize(300, 300)
        ##36393e
        rectangle.setStyleSheet("""
            background-color: transparent; 
            box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.9);
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
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 16px;
                border-radius: 5px;
            }
            
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);  /* Slightly translucent white when hovered */
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
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 16px;
                border-radius: 5px;
            }
            
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);  /* Slightly translucent white when hovered */
                border: 1px solid rgba(255, 255, 255, 0.5);  /* Add a translucent white border on hover */
            }
            
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.2);  /* Slightly more opaque when pressed */
                padding: 12px 22px;  /* Optional: add some effect on click, like a padding change */
            }
        """)
        
        rectangle_layout = QVBoxLayout(rectangle)
        rectangle_layout.addWidget(Login, alignment=Qt.AlignHCenter)
        rectangle_layout.addWidget(Register, alignment=Qt.AlignHCenter)
        rectangle_layout.setSpacing(0)
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
        
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("AUBoutique")
#         # self.setGeometry(700, 300, 500, 500)
        
#         piclabel=QLabel(self)
#         piclabel.setGeometry(0,0, self.width(),self.height())
        
#         pixmap = QPixmap("IMAGES/1325116.png")
#         piclabel.setPixmap(pixmap)
#         piclabel.setScaledContents(True)
#         piclabel.setGeometry((self.width()-piclabel.width()),
#                              (self.height()-piclabel.height()), 
#                              piclabel.width(), 
#                              piclabel.height())
#         piclabel.setStyleSheet("background-size: cover;")
        
#         label = QLabel("AUBoutique", self)
#         label.setFont(QFont("Arial",50))
#         #label.setGeometry(0,0,100,100)
#         label.setGeometry((self.width()-label.width())//2,
#                              (self.height()-label.height())//2, 
#                              label.width(), 
#                              label.height())
#         label.setStyleSheet("color: red;"
#                             "background-color: #6fdcf7;"
#                             "font-style: italic;")
#         label.setAlignment(Qt.AlignCenter)

app = QApplication(sys.argv)
app.setWindowIcon(QIcon("IMAGES/FirstBackground.webp")) 
window = MainWindow()
window.show()
sys.exit(app.exec_())