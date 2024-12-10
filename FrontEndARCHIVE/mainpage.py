import sys
from PyQt5.QtWidgets import QApplication, QTextEdit, QFrame, QScrollArea, QTableWidgetItem, QFileDialog, QTableWidget, QFormLayout, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QSpinBox, QTabWidget, QMenu, QMainWindow, QAction
import PyQt5.QtGui as qtg

app = QApplication(sys.argv)

window = QMainWindow()

window.setWindowTitle("Main page")
window.setGeometry(0, 0, 1000, 840)

menu_bar = window.menuBar()

market = menu_bar.addMenu("Market")
new_action = QAction("New", window)
#new_action.triggered.connect(file)
market.addAction(new_action)

chat = menu_bar.addMenu("Chat")
newAction = QAction("New", window)


layout = QHBoxLayout()

frame1 = QFrame()
frame2 = QFrame()
frame3 = QFrame()

frame_layout1 = QVBoxLayout()
frame_layout2 = QVBoxLayout()
frame_layout3 = QVBoxLayout()

search = QTextEdit(placeholderText = "Enter the product name here")
frame_layout1.addWidget(search)

app = QApplication(sys.argv)


layout.addWidget(frame1)
layout.addWidget(frame2)
layout.addWidget(frame3)

window.setLayout(layout)
window.show()
sys.exit(app.exec_())
