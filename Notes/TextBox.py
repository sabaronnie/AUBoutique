import sys
from PyQt5.QtWidgets import QApplication, QFormLayout, QSpinBox, QTextEdit, QScrollArea, QTableWidgetItem, QFileDialog, QTableWidget, QMessageBox, QComboBox, QWidget, QVBoxLayout, QTabWidget, QHBoxLayout, QFrame, QLabel, QLineEdit, QPushButton
import PyQt5.QtGui as qtg

#Define your application hek
app = QApplication(sys.argv)
#Define one window
window = QWidget()

#Set title
window.setWindowTitle("PyQt5 Tabs Example")
#Set size
window.setGeometry(0, 0, 640, 460)
#We can set background, image, and many otehr things

# QH means layout is horizontaol, QV means vertical
layout = QHBoxLayout()



#plainText here is the default text
text = QTextEdit(placeholderText="Enter your tst here", plainText="My text box")
layout.addWidget(text)


window.setLayout(layout)

window.show()

sys.exit(app.exec_())