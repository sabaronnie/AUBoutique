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
#you can customize the label too
#  font name, font size
my_label.setFont(qtg.QFont("Comic Sans MS", 16))

#now, add the widget to the layout called layout
layout.addWidget(my_label)

#Alternatively instead of making another variable, i can add a label 
# do it this way if u dont want to change aynthing
layout.addWidget(QLabel("EECE351 hayen"))

#you have to set the window wto the layout so it runs
window.setLayout(layout)

window.show()

sys.exit(app.exec_())