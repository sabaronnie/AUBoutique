import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLabel, QMessageBox, QDialog, QHBoxLayout
)
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt 
# Sample product data
products = [
    {"name": "Green Apple from Batroun, Lebanon. ", "price": "$10", "description": "A great product!", "owner": "Owner 1"},
    {"name": "Product 2", "price": "$20", "description": "Another awesome product!", "owner": "Owner 2"},
    {"name": "Product 3", "price": "$30", "description": "The best product ever!", "owner": "Owner 3"},
    {"name": "Product 4", "price": "$40", "description": "A premium product!", "owner": "Owner 4"},
    {"name": "Product 5", "price": "$50", "description": "Top-quality product!", "owner": "Owner 5"},
    {"name": "Product 6", "price": "$60", "description": "A luxurious product!", "owner": "Owner 6"},
]
 
# Function to create and display the product details dialog
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
 
    dialog.setLayout(layout)
    dialog.exec_()  # Open the dialog as a modal window
 
# Function to create the main product grid frame
def create_product_grid():
    frame = QWidget()
    frame.setWindowTitle("Product Grid")
    frame.setGeometry(100, 100, 1000, 1000)
 
    grid_layout = QGridLayout()
 
    grid_layout.setSpacing(1)
    grid_layout.setContentsMargins(0, 0, 0, 0)  # Remove outer margins
    grid_layout.setRowStretch(0, 0)
    grid_layout.setColumnStretch(0, 0)
    # Add products to the grid layout
    for index, product in enumerate(products):
        row = index // 5  # 3 products per row
        col = index % 5
 
        # Create a product card with name and "More Info" button
        product_card = QWidget()
        card_layout = QVBoxLayout()
       
        piclabel = QLabel(product_card)
        piclabel.setFixedSize(200, 200)  # Set the size of the QLabel
        piclabel.setStyleSheet("border: 1px solid black;")  # Optional border to visualize the label's boundary

        # Load and scale the pixmap to fit inside the label
        FILE_PATH = "IMAGES/greenapple.jpg"
        pixmap = QPixmap(FILE_PATH)
        scaled_pixmap = pixmap.scaled(
            piclabel.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        piclabel.setPixmap(scaled_pixmap)

        card_layout.addWidget(piclabel)
        
        name_layout = QHBoxLayout()

        productname = product["name"]
        if len(productname) >35:
            productname = productname[:22] + "..."
        # name = QLabel(productname)
        # name.setFixedSize(300, 100)
        # name_layout.addWidget(name)
        # name.setWordWrap(True)
        # # name.setContentsMargins(0,0,0,0)
        # name_layout.setAlignment(Qt.AlignCenter)
        # card_layout.addLayout(name_layout)
        # name.setStyleSheet("""
        #     QLabel {
        #         color: darkgreen;  /* Dark green text */
        #         font-weight: bold; /* Bold text */
        #         font-size: 20px;
        #     }
            
        #     QLabel:hover{
        #         color: lightgreen;
                
        #     }
        # """)
        
        

        more_info_button = QPushButton(productname)
        more_info_button.clicked.connect(lambda checked, p=product: show_product_details(p))
        card_layout.addWidget(more_info_button)
        more_info_button.setStyleSheet("""
            QPushButton {
                color: darkgreen;  /* Dark green text */
                font-weight: bold; /* Bold text */
                font-size: 20px;
                background-color: transparent;
            }
            
            QPushButton:hover{
                color: lightgreen;
                
            }                                       
                                       
                                       
        """)
       
        name_layout.setContentsMargins(0, 0, 0, 0)
        piclabel.setContentsMargins(0, 0, 0, 0)
        #more_info_button.setContentsMargins(0, 0, 0, 0)
        product_card.setLayout(card_layout)
 
        # Add the product card to the grid
        grid_layout.addWidget(product_card, row, col)
 
    frame.setLayout(grid_layout)
    return frame
 
# Main application entry point
app = QApplication(sys.argv)
product_grid = create_product_grid()
product_grid.show()
sys.exit(app.exec_())