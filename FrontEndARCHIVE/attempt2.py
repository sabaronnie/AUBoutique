import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QTextEdit, QFrame, QScrollArea, QTableWidgetItem, QFileDialog, QTableWidget, QFormLayout, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QSpinBox, QTabWidget
import PyQt5.QtGui as qtg
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt 

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(700,300,500,500)
        self.initUI()
        
    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        label1=QLabel("#1", self)
        label2 = QLabel("#2", self)
        label3 = QLabel("#3", self)
        label4 = QLabel("#4", self)
        label5 = QLabel("#5", self)
        label1.setStyleSheet("background-color: red;")
        label2.setStyleSheet("background-color: yellow;")
        label3.setStyleSheet("background-color: green;")
        label4.setStyleSheet("background-color: blue;")
        label5.setStyleSheet("background-color: purple;")
        
        vbox=QHBoxLayout()
        vbox.addWidget(label1)
        vbox.addWidget(label2)
        vbox.addWidget(label3)
        vbox.addWidget(label4)
        vbox.addWidget(label5)
        
        central_widget.setLayout(vbox)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())