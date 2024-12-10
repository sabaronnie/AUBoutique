import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QScrollArea, QWidget, QGridLayout
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class HomePage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(985, 820)
        self.setWindowTitle("Home Page")
        self.initUI()

    def initUI(self):
        # Main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)  # Remove any margin

        # Scrollable area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setContentsMargins(0, 0, 0, 0)
        scroll_area.setStyleSheet("border: none;")  # Remove border around scroll area

        scrollable_content = QWidget()
        scrollable_layout = QVBoxLayout(scrollable_content)
        scrollable_layout.setSpacing(10)
        scrollable_layout.setContentsMargins(0, 0, 0, 0)  # Remove inner margins

        scroll_area.setStyleSheet("""
            QScrollArea {
                border:none;
            }
            QScrollBar:vertical {
                border: none;  /* Remove border around scrollbar */
                background: transparent;  /* Transparent track */
                width: 6px;  /* Thin scrollbar */
            }
            QScrollBar::handle:vertical {
                background: gray;  /* Thumb color */
                min-height: 10px;  /* Minimum thumb size */
                border-radius: 3px;  /* Half of the width ensures full rounding */
            }
            QScrollBar::handle:vertical:hover {
                background: gray;  /* Thumb color when hovered */
            }
            QScrollBar::handle:vertical:pressed {
                background: gray;  /* Thumb color when pressed */
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;  /* Remove up/down arrow buttons */
                background: none;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;  /* Space above/below the thumb */
            }
        """)

        # Banner and buttons overlay container
        banner_widget = QWidget()
        banner_layout = QVBoxLayout(banner_widget)

        # Banner
        banner = QLabel()
        pixmap = QPixmap("IMAGES/AUB_Banner.png")  # Replace with your banner image path
        pixmap = pixmap.scaled(
            800, 500,  # Set the desired width and height for the banner
            Qt.IgnoreAspectRatio,
            Qt.SmoothTransformation
        )
        banner.setPixmap(pixmap)
        banner.setScaledContents(True)
        banner.setStyleSheet("background-color: #cccccc;")  # Fallback in case image doesn't load
        banner.setAlignment(Qt.AlignCenter)
        banner.setFixedHeight(500)

        # Add the banner to the layout
        banner_layout.addWidget(banner)

        # Create a widget for the buttons and set its layout
        banner_buttons_widget = QWidget(banner_widget)
        banner_buttons_layout = QHBoxLayout(banner_buttons_widget)
        banner_buttons_layout.setContentsMargins(0, 0, 0, 0)
        banner_buttons_layout.setSpacing(0)
        banner_buttons_widget.setStyleSheet("background: transparent;")

        # Create buttons and add them to the layout
        for i, page in enumerate(["Page 1", "Page 2", "Page 3", "Page 4"]):
            btn = QPushButton(page)
            btn.setFixedSize(100, 80)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #45a049; 
                    color: white; 
                    border: none; 
                    font-size: 14px;
                    margin: 0;
                    padding: 0;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
                QPushButton:pressed {
                    background-color: #388E3C;
                }
            """)
            banner_buttons_layout.addWidget(btn)

        # banner_buttons_layout.setContentsMargins(0, 0, 0, 0)
        # #banner_buttons_layout.setSpacing(0)
        banner_buttons_widget.setGeometry(0, banner.height() - 40, self.width(), 40) 
        # Set the buttons' widget's position over the banner using absolute positioning
       # banner_buttons_widget.setGeometry(0, 0, 800, 50)  # Position the buttons above the banner
        banner_buttons_widget.raise_()  # Ensure the buttons are on top of the banner

        # Add the banner and buttons widget to the scrollable layout
        scrollable_layout.addWidget(banner_widget)

        # Product section
        product_container = QWidget()
        product_layout = QGridLayout(product_container)
        product_layout.setSpacing(20)
        product_layout.setContentsMargins(10, 10, 10, 10)

        # Add dynamic products
        for i in range(20):  # Simulate a dynamic number of products
            product_widget = self.create_product_widget(f"Product {i+1}")
            row, col = divmod(i, 5)  # Arrange products in a grid (3 per row)
            product_layout.addWidget(product_widget, row, col)

        scrollable_layout.addWidget(product_container)

        scroll_area.setWidget(scrollable_content)

        # Set the main layout
        main_layout.addWidget(scroll_area)
        self.setCentralWidget(main_widget)

    def create_product_widget(self, product_name):
        """Creates a widget for a single product."""
        product_widget = QWidget()
        product_layout = QVBoxLayout(product_widget)
        product_layout.setSpacing(10)

        # Product image
        product_image = QLabel()
        pixmap = QPixmap("IMAGES/best-homemade-baked-potato-chip-recipe-1.jpg")  # Replace with your product image path
        pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        product_image.setPixmap(pixmap)
        product_image.setAlignment(Qt.AlignCenter)

        # Product name
        product_label = QLabel(product_name)
        product_label.setAlignment(Qt.AlignCenter)
        product_label.setStyleSheet("font-size: 14px; font-weight: bold;")

        # Button under product
        product_button = QPushButton("Buy Now")
        product_button.setFixedSize(100, 30)
        product_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3; 
                color: white; 
                border: none; 
                border-radius: 5px; 
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """)

        product_layout.addWidget(product_image)
        product_layout.addWidget(product_label)
        product_layout.addWidget(product_button, alignment=Qt.AlignCenter)
        return product_widget


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HomePage()
    window.show()
    sys.exit(app.exec_())