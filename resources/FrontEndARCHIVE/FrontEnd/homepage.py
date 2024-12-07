import sys
from PyQt5.QtWidgets import QGridLayout, QApplication, QMainWindow, QScrollArea, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QStackedWidget
from PyQt5.QtGui import QPixmap, QIcon, QPainter, QColor
from PyQt5.QtCore import Qt, QSize

class HomePage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(985, 820)
        self.setWindowTitle("AUBoutique")
        self.initUI()

    def initUI(self):
        # Main widget to hold all content
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create a QStackedWidget to manage the tab content
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("background-color: #f0f0f0; padding: 0;")

        # Create the banner widget
        self.banner_widget = self.create_banner()

        # Create the tab buttons at the bottom of the banner
        self.tab_buttons_widget = self.create_tab_buttons()

        # Add banner and tab buttons to the layout
        main_layout.addWidget(self.banner_widget)
        main_layout.addWidget(self.tab_buttons_widget)

        # Add the stacked widget to hold the content for each tab
        main_layout.addWidget(self.stacked_widget)

        # Create the content for each tab
        self.create_tab_content()

        # Create a QScrollArea to make the layout scrollable
        scroll_area = QScrollArea()
        scroll_area.setWidget(main_widget)
        scroll_area.setWidgetResizable(True)
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

        # Set the scroll area as the central widget
        self.setCentralWidget(scroll_area)

    def create_banner(self):
        """Creates a banner widget."""
        banner_widget = QWidget()
        banner_layout = QVBoxLayout(banner_widget)
        banner_layout.setContentsMargins(0, 0, 0, 0)
        banner_layout.setSpacing(0)

        # Banner label with image
        banner = QLabel()
        pixmap = QPixmap("IMAGES/AUB_Banner.png")  # Replace with your banner image path
        pixmap = pixmap.scaled(
            800, 500,  # Set the desired width and height for the banner
            Qt.IgnoreAspectRatio,
            Qt.SmoothTransformation
        )
        banner.setPixmap(pixmap)
        banner.setScaledContents(True)
        banner.setAlignment(Qt.AlignCenter)
        banner.setStyleSheet("background-color: #cccccc;")  # Fallback in case image doesn't load
        banner.setFixedHeight(500)

        # Add banner to the layout
        banner_layout.addWidget(banner)
        return banner_widget

    def create_tab_buttons(self):
        """Creates tab buttons widget."""
        tab_buttons_widget = QWidget()
        tab_buttons_layout = QHBoxLayout(tab_buttons_widget)
        tab_buttons_layout.setContentsMargins(0, 0, 0, 0)
        tab_buttons_layout.setSpacing(0)
        # Tab buttons
        for i, page in enumerate(["Home" , "Chat", "Add Products", "Profile"]):
            btn = QPushButton(page)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: white;
                    font-family: 'Segoe UI', sans-serif;
                    font-size: 18px;
                    font-weight: bold;
                    padding: 10px;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #5DADE2;
                }
                QPushButton:pressed {
                    background-color: #3498DB;
                }
            """)
            btn.clicked.connect(self.on_tab_button_click)
            tab_buttons_layout.addWidget(btn)

        tab_buttons_widget.setStyleSheet("background-color: #34495e;")  # Tab buttons background
        return tab_buttons_widget

    def on_tab_button_click(self):
        """Handles the tab button click event."""
        sender = self.sender()
        if sender.text() == "Home":
            self.stacked_widget.setCurrentIndex(0)
            self.banner_widget.show()
            self.tab_buttons_widget.setStyleSheet("background-color: #34495e;")  # Keep tabs at the bottom
        elif sender.text() == "Add Products":
            self.stacked_widget.setCurrentIndex(1)
            self.banner_widget.hide()  # Hide the banner when switching to Products
            self.tab_buttons_widget.setStyleSheet("background-color: #1abc9c;")  # Move tabs to the top
        elif sender.text() == "Profile":
            self.stacked_widget.setCurrentIndex(2)
            self.banner_widget.hide()  # Hide the banner when switching to Contact
            self.tab_buttons_widget.setStyleSheet("background-color: #e74c3c;")  # Change tab background color
            
            
    def create_product_widget(self, product_name):
        """Creates a widget for a single product."""
        product_widget = QWidget()
        product_layout = QVBoxLayout(product_widget)
        product_layout.setSpacing(10)

        # Create the product image button
        product_image = QPushButton()
        pixmap = QPixmap("IMAGES/best-homemade-baked-potato-chip-recipe-1.jpg")
        dark_pixmap = pixmap.copy()  # Create a copy of the pixmap for hover effect

        # Darken the pixmap for hover effect
        painter = QPainter(dark_pixmap)
        painter.fillRect(dark_pixmap.rect(), QColor(0, 0, 0, 100))  # Add a semi-transparent overlay
        painter.end()

        product_image.setIcon(QIcon(pixmap))
        icon_size = QSize(150, 150)

        product_image.setStyleSheet("""
            QPushButton {
                background-color: transparent; 
                padding: 0px;
                border: none; 
            }
        """)
        product_image.setCursor(Qt.PointingHandCursor)
        product_image.setIconSize(icon_size) 
        product_image.setFixedSize(icon_size)

        # Event handlers for hover effect
        def on_hover_enter():
            product_image.setIcon(QIcon(dark_pixmap))  # Change to dark icon on hover

        def on_hover_leave():
            product_image.setIcon(QIcon(pixmap))  # Revert to original icon on leave

        product_image.enterEvent = lambda event: on_hover_enter()
        product_image.leaveEvent = lambda event: on_hover_leave()

        # Add the product image to the layout and center it
        product_layout.addWidget(product_image, alignment=Qt.AlignCenter)

        # Button under product (product name)
        product_button = QPushButton(product_name)
        product_button.setFixedSize(100, 30)
        
        product_button.setStyleSheet("""
        QPushButton {
            background-color: #32aab8;
            color: white;
            font-family: 'Segoe UI', sans-serif;
            font-size: 14px;
            border: none;
            border-radius: 8px;
            padding: 8px 12px;
        }
        QPushButton:hover {
            background-color: #2d95a1;
        }
        QPushButton:pressed {
            background-color: #227680;
        }
        """)
        # product_button.setStyleSheet("""
        # QPushButton {
        #     background-color: #FF5722;
        #     color: white;
        #     font-family: 'Segoe UI', sans-serif;
        #     font-size: 14px;
        #     border: none;
        #     border-radius: 8px;
        #     padding: 8px 12px;
        # }
        # QPushButton:hover {
        #     background-color: #E64A19;
        # }
        # QPushButton:pressed {
        #     background-color: #D84315;
        # }
        # """)

        # Add the product name button to the layout, also centered
        product_layout.addWidget(product_button, alignment=Qt.AlignCenter)

        return product_widget


    def create_tab_content(self):
        """Creates the content for each tab."""
        
        product_container = QWidget()
        product_layout = QGridLayout(product_container)
        product_layout.setSpacing(20)
        product_layout.setContentsMargins(10, 10, 10, 10)

        # Add dynamic products
        for i in range(200):  # Simulate a dynamic number of products
            product_widget = self.create_product_widget(f"Product {i+1}")
            row, col = divmod(i, 4)  # Arrange products in a grid (3 per row)
            product_layout.addWidget(product_widget, row, col)

        self.stacked_widget.addWidget(product_container)

        # Products tab content
        products_widget = QWidget()
        products_layout = QVBoxLayout(products_widget)
        products_layout.addWidget(QLabel("Browse our Products"))
        products_layout.addWidget(QPushButton("Shop Now"))
        self.stacked_widget.addWidget(products_widget)

        # Contact tab content
        contact_widget = QWidget()
        contact_layout = QVBoxLayout(contact_widget)
        contact_layout.addWidget(QLabel("Get in touch with us"))
        contact_layout.addWidget(QPushButton("Contact Us"))
        self.stacked_widget.addWidget(contact_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HomePage()
    window.show()
    sys.exit(app.exec_())