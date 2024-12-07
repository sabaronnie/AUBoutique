import sys

#sys.path.append("modules") 
import subprocess

subprocess.run([sys.executable, "-m", "pip", "install", "pyqt5"])

import sys
from PyQt5.QtWidgets import QGridLayout, QStackedLayout, QMainWindow, QApplication, QTextEdit, QFrame, QScrollArea, QTableWidgetItem, QFileDialog, QTableWidget, QFormLayout, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QSpinBox, QTabWidget, QMessageBox
import PyQt5.QtGui as qtg
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt 

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 700, 500)
        self.setMinimumSize(700, 500)
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setGeometry(700, 245, 500, 500)
        central_widget.setStyleSheet("background-color: #e5ddd5;")

        problemlayout = QVBoxLayout()

        # Red banner for error message
        red = QWidget()
        red.setStyleSheet("""
            background-color: red;
            color: white;
            font-size: 16px;
            padding: 0px;
            margin: 0px;
            border-radius: 5px;
        """)
        red.setFixedSize(245, 50)
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
            padding: 0px;
            margin: 0px;
            font-size: 16px;
        """)

        removeBanner.clicked.connect(lambda: red.setVisible(False))

        bannerLayout.addWidget(removeBanner, alignment=Qt.AlignLeft)
        bannerLayout.addWidget(incorrectText, alignment=Qt.AlignLeft)
        bannerLayout.setSpacing(0)

        red.setLayout(bannerLayout)
        problemlayout.addWidget(red)
        problemlayout.setSpacing(5)

        rectangle = QLabel()
        rectangle.setFixedSize(260, 420)
        rectangle.setStyleSheet("""
            background-color: #36393e;
            box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.9);
            border-radius: 5px;
        """)

        form_layout = QVBoxLayout()
        TopPart = QHBoxLayout()
        auboutique = QLabel("Create a Product")
        TopPart.addWidget(auboutique, alignment=Qt.AlignCenter)
        TopPart.setContentsMargins(0, 0, 0, 15)
        auboutique.setStyleSheet("""
            font-weight: bold;
            font-size: 20px;
        """)

        name_layout = QFormLayout()
        nameText = QLabel("Product Name")
        nameText.setStyleSheet("color: #99aab5; font-weight: bold;")
        name = QLineEdit()
        name.setFixedSize(245, 30)
        name.setStyleSheet("""
            QLineEdit {
                background-color: #23272a;
                color: white;
                padding-left: 10px;
                border-radius: 5px;
                border: none;
                outline: none;
                border: 1px solid transparent;
            }
            QLineEdit:focus {
                border: 0 none #FFF;
                outline:none;
            }
        """)
        name_layout.addWidget(nameText)
        name_layout.addWidget(name)

        # Make sure all fields have the same width
        price_layout = QFormLayout()
        priceText = QLabel("Price")
        priceText.setStyleSheet("color: #99aab5; font-weight: bold;")
        price = QLineEdit()
        price.setFixedSize(245, 30)
        price.setStyleSheet("""
            background-color: #23272a;
            color: white;
            padding-left: 10px;
            border-radius: 5px;
            border: none;
            outline: none;
        """)
        price_layout.addWidget(priceText)
        price_layout.addWidget(price)

        desc_layout = QFormLayout()
        descText = QLabel("Description")
        descText.setStyleSheet("color: #99aab5; font-weight: bold;")
        desc = QLineEdit()
        desc.setFixedSize(245, 30)
        desc.setStyleSheet("""
            background-color: #23272a;
            color: white;
            padding-left: 10px;
            border-radius: 5px;
            border: none;
            outline: none;
        """)
        desc_layout.addWidget(descText)
        desc_layout.addWidget(desc)

        # Upload Image
        img_layout = QVBoxLayout()
        imgText = QLabel("Upload Image")
        imgText.setStyleSheet("color: #99aab5; font-weight: bold; margin: 0px 18px;")
        img_upload = QPushButton("Upload")
        img_upload.clicked.connect(self.upload_image)
        img_upload.setFixedSize(70, 25)
        img_upload.setStyleSheet("""
            QPushButton {
                background-color: #006400;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 0px 0px;
                margin: 0px 0px 0px 24px;
                font-size: 10px;
            }
            QPushButton:hover {
                background-color: #004d00;
            }
            QPushButton:pressed {
                background-color: #003245;
            }
        """)
        img_layout.addWidget(imgText)
        img_layout.addWidget(img_upload)

        # Submit button
        submit_layout = QFormLayout()
        Empty = QLabel()
        Submit = QPushButton("Create")
        
        Submit.setFixedSize(245, 30)
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

        form_layout.addLayout(TopPart)
        form_layout.addLayout(name_layout)
        form_layout.addLayout(price_layout)
        form_layout.addLayout(desc_layout)
        form_layout.addLayout(img_layout)
        form_layout.addLayout(submit_layout)

        rectangle_layout = QVBoxLayout(rectangle)
        rectangle_layout.addLayout(form_layout)
        rectangle_layout.setAlignment(Qt.AlignCenter)
        rectangle_layout.setContentsMargins(0, 0, 15, 0)

        problemlayout.addWidget(rectangle)

        mainlayout = QGridLayout(central_widget)
        mainlayout.addLayout(problemlayout, 0, 0, alignment=Qt.AlignCenter)
        mainlayout.setAlignment(rectangle, Qt.AlignCenter)
        mainlayout.setContentsMargins(0, 0, 0, 0)
        mainlayout.setSpacing(0)

        central_widget.setStyleSheet("padding: 0px; margin: 0px;")
        central_widget.setLayout(mainlayout)
        Submit.clicked.connect(lambda: self.validate_inputs(name, price, desc))
    def validate_inputs(self, name, price, description):
        """Validate the inputs for all fields.""" 
        # Check if any of the fields are empty
        if not name.text() or not price.text() or not description.text():
            self.show_error("Please fill in all the fields.")
            return
        price_value = float(price.text())  # Use float() to allow decimal values as well
        if price_value < 0:
            self.show_error("Price cannot be negative.")
            return
        
    def upload_image(self):
        options = QFileDialog.Options()
        file, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.bmp *.gif)", options=options)

        if file:
            pixmap = QPixmap(file)
            self.image_label.setPixmap(pixmap)
            self.image_label.setScaledContents(True)
            self.resize(pixmap.width(), pixmap.height())
    def show_error(self, message):
        """Show an error message box.""" 
        QMessageBox.critical(self, "Error", message)
