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

#dropdown box
# the editable makes it let users add their own to the dropdown if true
comboBox = QComboBox(editable=True)

#adds to the dropwdown, with an associated, backend data
# so publicText, data
comboBox.addItem("Mercedes", "12345")
comboBox.addItem("BMW", "54321")
#we can also add an item at a specific index in the dropdown
#can add an array without data
comboBox.addItems(["Toyota", "Nissan", "Ferrari"])

layout.addWidget(comboBox)

#SPIN BOX
#value would be the number we start at
# max and min the range of numbers
# by how much the arrows can increase/decrease
#preffix is just if we want a text before the scrollable number
#and suffix if we want after

my_box = QSpinBox(value=10, maximum=100, minimum=0, singleStep=1, prefix="Temperature", suffix="C")
layout.addWidget(my_box)


def button_pressed():
    print("LOLLL")
    #print the text select, and the data selected
    print(comboBox.currentText())
    print(comboBox.currentData())
    
    #PRINT THE VALUE IN THE SPIN BOX
    print(my_box.value())

#Create a button, and when pressed, make it call the function
my_button = QPushButton("Click me!", clicked=lambda:button_pressed())
layout.addWidget(my_button)


window.setLayout(layout)

window.show()

sys.exit(app.exec_())