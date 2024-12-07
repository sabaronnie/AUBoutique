import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QTextEdit, QFrame, QScrollArea, QTableWidgetItem, QFileDialog, QTableWidget, QFormLayout, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QSpinBox, QTabWidget
import PyQt5.QtGui as qtg
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt 

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AUBoutique")
        self.setGeometry(700, 300, 500, 500)
        
        piclabel=QLabel(self)
        piclabel.setGeometry(0,0, 200,200)
        
        pixmap = QPixmap("IMAGES/1325116.png")
        piclabel.setPixmap(pixmap)
        piclabel.setScaledContents(True)
        piclabel.setGeometry((self.width()-piclabel.width()) //2,
                             (self.height()-piclabel.height()) //2, 
                             piclabel.width(), 
                             piclabel.height())
        
        label = QLabel("AUBoutique", self)
        label.setFont(QFont("Arial",50))
        label.setGeometry(0,0,100,100)
        label.setStyleSheet("color: red;"
                            "background-color: #6fdcf7;"
                            "font-style: italic;")
        label.setAlignment(Qt.AlignCenter)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())