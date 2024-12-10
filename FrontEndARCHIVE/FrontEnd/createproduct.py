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
        central_widget.setStyleSheet("background-color: #e5ddd5;") 
    
        problemlayout = QVBoxLayout()
        
        red = QWidget()
        red.setStyleSheet("""
            background-color: red;
            color: white;
            font-size: 16px;
            padding: 0px;
            margin: 0px;
            border-radius: 5px;
        """)
        red.setFixedSize(300, 50)


        red.setVisible(False)

        bannerLayout = QHBoxLayout()
        
        incorrectText = QLabel("Incorrect Username or Password")
        incorrectText.setStyleSheet("""
            color: white;
            font-size: 14px;
            padding: 0px;
        """)
        
        removeBanner = QPushButton("X")
        removeBanner.setStyleSheet("""
            color: #c4251a;
            background-color: transparent;
            align-self: flex-start;  /* Align it to the top-left */
            padding: 0px;  /* Remove extra padding */
            margin: 0px;   /* Remove extra margin */
            font-size: 16px;
        """)
        
        removeBanner.clicked.connect(lambda: red.setVisible(False))
        
        bannerLayout.addWidget(removeBanner, alignment=Qt.AlignLeft)
        bannerLayout.addWidget(incorrectText, alignment=Qt.AlignLeft)
        bannerLayout.setSpacing(0)
        
        red.setLayout(bannerLayout)
        problemlayout.addWidget(red)
        # problemlayout.addLayout(bannerLayout)
        problemlayout.setSpacing(5)

        
    
    
        # piclabel = QLabel(central_widget)
        # pixmap = QPixmap("IMAGES/plain-dark-green-wallpaper-4py2q8q4fvne42p7.jpg")
        # scaled_pixmap = pixmap.scaled(500, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        # piclabel.setPixmap(scaled_pixmap)
        # piclabel.setScaledContents(True)  # Allow the image to scale with the label


        rectangle = QLabel()
        #label.setFont(QFont("Arial",50))
        rectangle.setFixedSize(300, 420)
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
        auboutique = QLabel("Create a Product")
        TopPart.addWidget(auboutique, alignment=Qt.AlignCenter)
        TopPart.setContentsMargins(0, 0, 0, 15) 
        auboutique.setStyleSheet("""
            font-weight: bold;
            font-size: 20px;
        """) 
        
        name_layout = QFormLayout()
        nameText = QLabel("Product Name")
        nameText.setStyleSheet("color: #99aab5; font-weight: bold;")  # Set label color

        name = QLineEdit()
        name.setFixedSize(250, 30)  # Thinner and longer text box
        name.setStyleSheet("""
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
        name_layout.addWidget(nameText)
        name_layout.addWidget(name)
                
        
        price_layout = QFormLayout()
        priceText = QLabel("Price")
        priceText.setStyleSheet("color: #99aab5; font-weight: bold;")  # Set label color
        
        price = QLineEdit()
        price.setFixedSize(250, 30)
        price.setStyleSheet("""
            background-color: #23272a; 
            color: white; 
            padding-left: 10px; 
            border-radius: 5px;
            border: none;  /* Remove the default border */
            outline: none;  /* Remove the focus outline */
        """)
        price_layout.addWidget(priceText)
        price_layout.addWidget(price)
        

        desc_layout = QFormLayout()
        descText = QLabel("Description")
        descText.setStyleSheet("color: #99aab5; font-weight: bold;")  # Set label color
        
        desc = QLineEdit()
        desc.setFixedSize(250, 30)
        desc.setStyleSheet("""
            background-color: #23272a; 
            color: white; 
            padding-left: 10px; 
            border-radius: 5px;
            border: none;  /* Remove the default border */
            outline: none;  /* Remove the focus outline */
        """)
        desc_layout.addWidget(descText)
        desc_layout.addWidget(desc)
        


        img_layout = QVBoxLayout()
        imgText = QLabel("Upload Image")
        imgText.setStyleSheet("color: #99aab5; font-weight: bold; margin: 0px 18px;")  # Set label color

        img_upload = QPushButton("Upload")
        img_upload.clicked.connect(self.upload_image)
        img_upload.setFixedSize(70, 25)
        img_upload.setStyleSheet("""
            QPushButton {
                background-color: #006400;  /* Dark green */
                color: white;  /* White text */
                border: none;  /* Remove border */
                border-radius: 5px;  /* Rounded corners */
                padding: 0px 0px;  /* Add padding */
                margin: 0px 0px 0px 24px;
                font-size: 10px;  /* Font size */
            }
            QPushButton:hover {
                background-color: #004d00;  /* Slightly darker green when hovered */
            }
            QPushButton:pressed {
                background-color: #003300;  /* Even darker green when pressed */
            }
        """)

        name_layout.setSpacing(3)
        price_layout.setSpacing(3)
        desc_layout.setSpacing(3)
        img_layout.setSpacing(3)
        # piclabel = QLabel(central_widget)
        # pixmap = QPixmap("")
        # scaled_pixmap = pixmap.scaled(500, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        # piclabel.setPixmap(scaled_pixmap)
        # piclabel.setScaledContents(True)  # Allow the image to scale with the label
        imgText.setAlignment(Qt.AlignLeft)
        
        
        img_layout.addWidget(imgText)
        img_layout.addWidget(img_upload)
        # img_layout.addWidget(piclabel)
        # img_layout.addWidget(img_upload)
        
        
        # form_layout.addWidget(username)
        # form_layout.addWidget(password)
        form_layout.addLayout(TopPart)
        form_layout.addLayout(name_layout)
        form_layout.addLayout(price_layout)
        form_layout.addLayout(desc_layout)
        form_layout.addLayout(img_layout)
        
        
        submit_layout = QFormLayout()
        Empty = QLabel()
        Submit = QPushButton("Create")
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

        problemlayout.addWidget(rectangle)
        
        mainlayout = QGridLayout(central_widget)
        # mainlayout.addWidget(piclabel, 0, 0)
        mainlayout.addLayout(problemlayout, 0, 0, alignment=Qt.AlignCenter)
        # mainlayout.addWidget(rectangle, 0, 0, alignment=Qt.AlignCenter)

        mainlayout.setAlignment(rectangle, Qt.AlignCenter)
        # Remove layout margins
        mainlayout.setContentsMargins(0, 0, 0, 0)  # Top, left, bottom, right margins set to 0
        mainlayout.setSpacing(0)  # No spa cing between widgets
        
    
        
        central_widget.setStyleSheet("padding: 0px; margin: 0px;")
        central_widget.setLayout(mainlayout)
        
    def upload_image(self):
        # Open file dialog to choose an image file
        options = QFileDialog.Options()
        file, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.bmp *.gif)", options=options)

        if file:
            # Display the selected image
            pixmap = QPixmap(file)
            self.image_label.setPixmap(pixmap)
            self.image_label.setScaledContents(True)  # Scale the image to fit in the label

            # Optional: Resize the window to fit the image
            self.resize(pixmap.width(), pixmap.height())
        
        
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())