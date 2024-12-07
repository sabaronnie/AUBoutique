import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLabel, QScrollArea, QFrame, QDialog, QMessageBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
 
# Sample product data
products = [
    {"name": "Green Apple from Batroun, Lebanon.", "price": "$10", "description": "A great product from the lush orchards of Lebanon.", "owner": "Owner 1"},
    {"name": "Premium Red Grapes", "price": "$15", "description": "Sweet and fresh red grapes.", "owner": "Owner 2"},
    {"name": "Golden Pears", "price": "$12", "description": "Crisp and juicy golden pears.", "owner": "Owner 3"},
    {"name": "Exotic Mango", "price": "$20", "description": "Fresh tropical mangoes.", "owner": "Owner 4"},
    {"name": "Fresh Blueberries", "price": "$18", "description": "Organic blueberries.", "owner": "Owner 5"},
    {"name": "Ripe Strawberries", "price": "$22", "description": "Sweet and delicious strawberries.", "owner": "Owner 6"},
]
 
def show_product_details(product):
    dialog = QDialog()
    dialog.setWindowTitle(f"Details of {product['name']}")
    dialog.setGeometry(200, 200, 400, 300)
 
    layout = QVBoxLayout()
 
    # Add product details
    layout.addWidget(QLabel(f"Name: {product['name']}"))
    layout.addWidget(QLabel(f"Price: {product['price']}"))
    layout.addWidget(QLabel(f"Description: {product['description']}"))
    layout.addWidget(QLabel(f"Owner: {product['owner']}"))
 
    # Add a "Buy" button
    buy_button = QPushButton("Buy")
    def buy_action():
        QMessageBox.information(dialog, "Purchase", "Thank you for your purchase!")
        dialog.accept()  # Close the dialog
    buy_button.clicked.connect(buy_action)
    layout.addWidget(buy_button)
    back_button = QPushButton("Back", dialog)
    back_button.clicked.connect(dialog.accept)
    layout.addWidget(back_button)
   
    dialog.setLayout(layout)
    dialog.exec_()  # Open the dialog as a modal window
 
# Function to create the main product grid frame
def create_product_grid():
    container = QWidget()
    smallcontainer = QWidget()
    container_market_layout = QVBoxLayout()
    grid_layout = QGridLayout()
    grid_layout.setSpacing(20)  # Uniform spacing between products
 
    # Add products to the grid layout
    for index, product in enumerate(products):
        row = index // 3  # 3 products per row
        col = index % 3
 
        product_card = QFrame()
        card_layout = QVBoxLayout()
 
        # Add product image
        piclabel = QLabel()
        piclabel.setFixedSize(200, 200)
        piclabel.setStyleSheet("border: 1px solid black;")
        FILE_PATH = "IMAGES/greenapple.jpg"  # Replace with the actual path to your images
        try:
            pixmap = QPixmap(FILE_PATH)
            if pixmap.isNull():
                raise FileNotFoundError
        except FileNotFoundError:
            pixmap = QPixmap("IMAGES/default.jpg")  # Fallback image
 
        scaled_pixmap = pixmap.scaled(
            piclabel.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        piclabel.setPixmap(scaled_pixmap)
        card_layout.addWidget(piclabel)
 
        # Create a QLabel for the name that wraps text
        name_label = QLabel(product["name"])
        name_label.setWordWrap(True)
        name_label.setFixedWidth(200)  # Fixed width for wrapping
        name_label.setStyleSheet("""
            QLabel {
                color: darkgreen;
                font-size: 14px;
                font-weight: bold;
                text-align: left;
            }
        """)
        name_label.setFixedHeight(50)  # Fixed height for 2 lines
        name_label.setAlignment(Qt.AlignCenter)
 
        # Add the name QLabel to the card
        card_layout.addWidget(name_label)
 
        # Add button to show product details
        more_info_button = QPushButton("More Info")
        more_info_button.setStyleSheet("""
            QPushButton {
                color: darkgreen;
                font-size: 14px;
                font-weight: bold;
                background-color: transparent;
            }
            QPushButton:hover {
                color: lightgreen;
            }
        """)
        more_info_button.clicked.connect(lambda checked, p=product: show_product_details(p))
        card_layout.addWidget(more_info_button)
 
        product_card.setLayout(card_layout)
        product_card.setFixedSize(220, 320)  # Uniform size for cards
        grid_layout.addWidget(product_card, row, col)
       
    smallcontainer.setLayout(grid_layout)
    banner_image = create_banner_image()
    container_market_layout.addWidget(banner_image)
    container_market_layout.addWidget(smallcontainer)
    container.setLayout(container_market_layout)
 
    # Wrap the grid in a scroll area
    scroll_area = QScrollArea()
    scroll_area.setWidget(container)
    scroll_area.setWidgetResizable(True)
    return scroll_area
 

# Function to create the banner image at the top of the window
def create_banner_image():
    banner_label = QLabel()
    banner_label.setFixedHeight(400)  # Height of the banner image
    FILE_PATH = "IMAGES/FirstBackground.webp"  # Replace with your banner image path
    try:
        pixmap = QPixmap(FILE_PATH)
        if pixmap.isNull():
            raise FileNotFoundError
    except FileNotFoundError:
        pixmap = QPixmap("IMAGES/default_banner.jpg")  # Fallback image for banner
 
    scaled_pixmap = pixmap.scaled(
        banner_label.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
    )
    banner_label.setPixmap(scaled_pixmap)
    banner_label.setAlignment(Qt.AlignCenter)
    return banner_label
 
# Main application entry point
def running ():
    #app = QApplication(sys.argv)
    main_market_window = QWidget()
    #main_market_window.setWindowTitle("Product Grid")
    main_layout = QVBoxLayout()
 
   
 
    # Add the product grid below the banner
    product_grid = create_product_grid()
    main_layout.addWidget(product_grid)
 
    main_market_window.setLayout(main_layout)
    main_market_window.resize(800, 600)  # Set the window size
    #main_market_window.show()
    #sys.exit(app.exec_())
    return main_market_window


