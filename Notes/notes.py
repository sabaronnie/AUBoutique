import sys
from PyQt5.QtWidgets import QApplication, QTextEdit, QFrame, QScrollArea, QTableWidgetItem, QFileDialog, QTableWidget, QFormLayout, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QSpinBox, QTabWidget
import PyQt5.QtGui as qtg

def button_pressed():
    print(entry_box.text())
    print(my_dropbox.currentText())
app = QApplication(sys.argv)
window  = QWidget()
window.setWindowTitle("PyQt5 Tabs")
window.setGeometry(0, 0, 640, 460)

layout = QHBoxLayout() 


frame1 = QFrame()
frame2 = QFrame()

frame_layout1 = QVBoxLayout()
frame_layout2 = QVBoxLayout()

my_dropbox = QComboBox(editable = False) #can only select from available options

my_dropbox.addItem("Mercedes", "12345")
my_dropbox.addItem("BMW", "54321")
my_dropbox.addItems(["Toyota", "Nissan", "Mitsubishi"])
frame_layout1.addWidget(my_dropbox)

my_spinbox = QSpinBox(value = 10, maximum = 100, minimum =  0, singleStep = 1,prefix =  "Temperature ", suffix = " Celsius")
frame_layout1.addWidget(my_spinbox)


my_label = QLabel("Hey")
my_label.setFont(qtg.QFont("Comic Sans MS", 16))

text = QTextEdit(placeholderText = "Enter your text here", plainText = "My text box")
frame_layout2.addWidget(text)

entry_box = QLineEdit()
entry_box.setText("Hello everyone.")
frame_layout2.addWidget(entry_box)

frame_layout1.addWidget(my_label)
my_button = QPushButton("Click", clicked=lambda:button_pressed())
frame_layout2.addWidget(my_button)

form_layout = QFormLayout()
form_layout.addRow("Username ", QLineEdit())
form_layout.addRow("Spinbox", QSpinBox(value = 10, maximum = 100, minimum = 0))

window.setLayout(form_layout)


frame1.setLayout(frame_layout1)
frame2.setLayout(frame_layout2)

layout.addWidget(frame1)
layout.addWidget(frame2)

window.setLayout(layout)

window.show()

sys.exit(app.exec_())
