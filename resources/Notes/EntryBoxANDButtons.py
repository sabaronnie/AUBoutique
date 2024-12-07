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

#we can add wigits to the layout
#layout.addWidget()

#we can add labels, its a WIDGET
my_label = QLabel("Hello world")

#creates a input text field, and optionally add the placeholder thing
#if you want a placeholder to show, itsp ossible, but look uit up
entry_box = QLineEdit()

#add a text that you want to be there by default
#NOT A PLACEHOLDER
entry_box.setText("Hello everyone")

layout.addWidget(entry_box)

#You can play around with shape, size, look, color, and everyting of
#entry box just like you can with the window

def button_pressed():
    print("LOLLL")

#Create a button, and when pressed, make it call the function
my_button = QPushButton("Click me!", clicked=lambda:button_pressed())
layout.addWidget(my_button)

window.setLayout(layout)

window.show()

sys.exit(app.exec_())