import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QListWidget, QLabel, QScrollArea, QFrame
from PyQt5.QtCore import Qt

class WhatsAppSim(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the main layout
        self.setWindowTitle("WhatsApp Web Simulator")
        self.setGeometry(100, 100, 800, 600)

        # Create layout for the entire window
        main_layout = QHBoxLayout()

        # Left: User list
        self.user_list_widget = QListWidget()
        self.user_list_widget.setStyleSheet("""
            QListWidget {
                background-color: #f1f1f1;
                border: none;
                width: 200px;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #ddd;
            }
            QListWidget::item:selected {
                background-color: #0078d4;
                color: white;
            }
        """)
        self.user_list_widget.addItem("John Doe")
        self.user_list_widget.addItem("Jane Smith")
        self.user_list_widget.addItem("Sarah Lee")
        self.user_list_widget.setSelectionMode(QListWidget.SingleSelection)

        # Create right part for the chat box
        self.chat_area = QVBoxLayout()
        self.chat_area.setAlignment(Qt.AlignTop)

        # Chat display (scrollable area)
        self.chat_scroll_area = QScrollArea()
        self.chat_scroll_area.setWidgetResizable(True)
        self.chat_scroll_widget = QWidget()
        self.chat_scroll_area.setWidget(self.chat_scroll_widget)

        self.chat_layout = QVBoxLayout(self.chat_scroll_widget)

        # Input message box
        self.message_input = QTextEdit()
        self.message_input.setPlaceholderText("Type a message...")
        self.message_input.setStyleSheet("""
            QTextEdit {
                background-color: #eaeaea;
                border: 1px solid #ccc;
                border-radius: 15px;
                padding: 10px;
                min-height: 50px;
            }
        """)

        # Send button
        self.send_button = QPushButton("Send")
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #25d366;
                color: white;
                border-radius: 15px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #128c7e;
            }
        """)
        self.send_button.clicked.connect(self.send_message)

        # Adding widgets to right layout
        self.chat_area.addWidget(self.chat_scroll_area)
        self.chat_area.addWidget(self.message_input)
        self.chat_area.addWidget(self.send_button)

        # Add widgets to main layout
        main_layout.addWidget(self.user_list_widget)
        main_layout.addLayout(self.chat_area)

        self.setLayout(main_layout)

    def send_message(self):
        # Get the message text from the input
        message = self.message_input.toPlainText().strip()
        if message:
            # Create the message bubble (sent message on the right)
            message_widget = QLabel(f"<div style='background-color:#DCF8C6; border-radius:15px; padding:10px;'>You: {message}</div>")
            message_widget.setAlignment(Qt.AlignRight)
            self.chat_layout.addWidget(message_widget)

            # Clear input field
            self.message_input.clear()

            # Auto-scroll to the bottom after sending the message
            self.chat_scroll_area.verticalScrollBar().setValue(self.chat_scroll_area.verticalScrollBar().maximum())

    def receive_message(self, message):
        # Create the message bubble (received message on the left)
        message_widget = QLabel(f"<div style='background-color:#f1f1f1; border-radius:15px; padding:10px;'>Friend: {message}</div>")
        message_widget.setAlignment(Qt.AlignLeft)
        self.chat_layout.addWidget(message_widget)

        # Auto-scroll to the bottom after receiving the message
        self.chat_scroll_area.verticalScrollBar().setValue(self.chat_scroll_area.verticalScrollBar().maximum())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WhatsAppSim()
    window.show()
    sys.exit(app.exec_())