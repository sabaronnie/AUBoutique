import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, 
    QLineEdit, QPushButton, QLabel, QFrame
)
from PyQt5.QtCore import Qt

class MessagingWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Messaging Window")
        self.setGeometry(100, 100, 400, 600)
        self.setStyleSheet("background-color: #e5ddd5;")  # WhatsApp-style background

        self.initUI()

    def initUI(self):
        # Main layout
        main_layout = QVBoxLayout(self)

        # Scrollable area for messages
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("border: none;")
        
        # Container for messages
        self.messages_container = QWidget()
        self.messages_layout = QVBoxLayout(self.messages_container)
        self.messages_layout.setAlignment(Qt.AlignTop)  # Align messages to the top
        self.scroll_area.setWidget(self.messages_container)
        
        main_layout.addWidget(self.scroll_area)

        # Input field and send button
        input_layout = QHBoxLayout()

        self.input_field = QLineEdit(self)
        self.input_field.setStyleSheet("""
            background-color: #36393e;
            border-radius: 10px;
            padding: 10px;
            font-size: 14px;
        """)
        self.input_field.setPlaceholderText("Type your message here...")
        self.input_field.returnPressed.connect(self.sendMessage)  # Send message on Enter key
        input_layout.addWidget(self.input_field)

        self.send_button = QPushButton("Send", self)
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #075E54;
                color: white;
                font-size: 14px;
                border-radius: 10px;
                padding: 10px 15px;
            }
            QPushButton:hover {
                background-color: #128C7E;
            }
        """)
        self.send_button.clicked.connect(self.sendMessage)
        input_layout.addWidget(self.send_button)

        main_layout.addLayout(input_layout)

    def sendMessage(self):
        # Get the typed message
        message = self.input_field.text().strip()

        if message:  # Only proceed if the message is not empty
            # Create a message box
            message_box = QFrame(self.messages_container)
            message_box.setStyleSheet("""
                background-color: #DCF8C6;
                color: black;
                border-radius: 10px;
                padding: 10px;
                margin: 3px;
            """)
            message_box.setContentsMargins(0,0,0,0)
            message_box.setFrameShape(QFrame.NoFrame)
            #message_box.setFixedWidth(150)  # Adjust box width

            # Add the message text
            message_label = QLabel(message, message_box)
            message_label.setWordWrap(True)  # Allow wrapping of long text
            message_label.setStyleSheet("font-size: 14px;")
            
            
            # Layout for the message box
            box_layout = QVBoxLayout(message_box)
            box_layout.addWidget(message_label)
            
            message_box.adjustSize()

            # Align the message box (right alignment for sent messages)
            alignment = Qt.AlignRight 
            if message:
                message_label.setStyleSheet("border-bottom-right-radius: 50px;")
            else:
                message_label.setStyleSheet("border-bottom-left-radius: 0px;")
                alignment = Qt.AlignLeft
            self.messages_layout.addWidget(message_box, alignment=alignment)

            # Clear the input field
            self.input_field.clear()

            # Ensure the latest message is visible
            self.scroll_area.verticalScrollBar().setValue(
                self.scroll_area.verticalScrollBar().maximum()
            )
            
    def adjustSizeToText(self):
        # Get the width of the text
        text = self.line_edit.text() or self.line_edit.placeholderText()
        font_metrics = self.line_edit.fontMetrics()
        text_width = font_metrics.horizontalAdvance(text) + 10  # Add some padding

        # Set the minimum and maximum width
        self.line_edit.setFixedWidth(max(100, min(text_width, 600)))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MessagingWindow()
    window.show()
    sys.exit(app.exec_())