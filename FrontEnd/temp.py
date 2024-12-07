import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox
import notifications

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle("Simple Button App")
        self.setGeometry(200, 200, 400, 300)

        # Create a button
        self.button = QPushButton("Click Me!", self)
        self.button.setGeometry(150, 130, 100, 50)  # x, y, width, height

        # Connect the button's click signal to a method
        self.button.clicked.connect(self.on_button_click)

    def on_button_click(self):
        # Display a message box on button click
        notifications.getErrorNotification("Purchase", "Insufficient Funds", self)
        #QMessageBox.information(self, "Hello!", "You clicked the button!")

# Main entry point
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())