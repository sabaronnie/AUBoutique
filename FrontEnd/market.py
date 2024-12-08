import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLabel, QScrollArea, QFrame, QDialog, QMessageBox, QHBoxLayout, QLineEdit
)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt

from ..BackEnd import client
wallet1 = 100

# Sample product data
# def getAllProducts():
    
# products = [
#     {"name": "Green Apple from Batroun, Lebanon.", "price": "$10", "description": "A great product from the lush orchards of Lebanon.","rating": 0, "owner": "Owner 1", "numberOfRatings" : 0},
#     {"name": "Premium Red Grapes", "price": "$15", "description": "Sweet and fresh red grapes.","rating": 0, "owner": "Owner 2", "numberOfRatings" : 0},
#     {"name": "Golden Pears", "price": "$12", "description": "Crisp and juicy golden pears.","rating": 0, "owner": "Owner 3", "numberOfRatings" : 0},
#     {"name": "Exotic Mango", "price": "$20", "description": "Fresh tropical mangoes.", "rating": 0,"owner": "Owner 4", "numberOfRatings" : 0},
#     {"name": "Fresh Blueberries", "price": "$18", "description": "Organic blueberries.","rating": 0, "owner": "Owner 5", "numberOfRatings" : 0},
#     {"name": "Ripe Strawberries", "price": "$22", "description": "Sweet and delicious strawberries.","rating": 0, "owner": "Owner 6", "numberOfRatings" : 0},
# ]

# products = client.populateProductsArray()
# products = []
# Function to filter products based on search query
def filter_products(query):
    filtered = []
    for product in products:
        if query.lower() in product["name"].lower() or query.lower() in product["description"].lower():
            filtered.append(product)
    return filtered



# Function to rate a product
def rate(star_butts, rating_label, updatedrating, rating, product):
    rating1 = rating
    rating_label.setText(f"Your Rating: {rating1}/5")

    # Update the star icons based on the rating
    for i in range(5):
        if i < rating:
            star_butts[i].setIcon(QIcon("AUBoutique/resources/IMAGES/filled.png"))  # Filled star icon
        else:
            star_butts[i].setIcon(QIcon("AUBoutique/resources/IMAGES/empty.png"))  # Empty star icon

    newRating = ((product["numberOfRatings"] * product["rating"]) + rating1) / (product["numberOfRatings"] + 1)
    product["rating"] = newRating
    product["numberOfRatings"] += 1
    updatedrating.setText(f"Updated Rating: {newRating}")

# Function to confirm the rating action
def confirmrating(star_butts, rating_label, updatedrating, i, product):
    message = QMessageBox()
    message.setIcon(QMessageBox.Question)
    message.setWindowTitle("Confirm Rating")
    message.setText("Are you sure you want to confirm your rating?")
    message.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    message.setDefaultButton(QMessageBox.No)

    # Show the dialog and wait for the user's response
    result = message.exec_()
    if result == QMessageBox.Yes:
        rate(star_butts, rating_label, updatedrating, i, product)

# Function to show product details
def show_product_details(product):
    dialog = QDialog()
    dialog.setWindowTitle(f"Details of {product['name']}")
    dialog.setGeometry(200, 200, 500, 400)

    # Set up the layout
    ratinglayout = QHBoxLayout()
    ratelayout = QVBoxLayout()

    rating_label = QLabel("Rating: 0/5")
    ratinglayout.addWidget(rating_label)

    updatedrating = QLabel()
    ratelayout.addLayout(ratinglayout)
    ratelayout.addWidget(updatedrating)

    star_buttons = []
    for i in range(5):
        button = QPushButton()
        button.setIcon(QIcon("AUBoutique/resources/IMAGES/empty.png"))
        button.setFixedSize(40, 40)
        button.setIconSize(button.size())
        button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }
        """)
        button.clicked.connect(lambda _, q=i + 1: confirmrating(star_buttons, rating_label, updatedrating, q, product))

        def on_hover_enter(index):
            for j in range(index + 1):
                star_buttons[j].setIcon(QIcon("AUBoutique/resources/IMAGES/filled.png"))

        def on_hover_leave():
            for j in range(5):
                if j < product['rating']:
                    star_buttons[j].setIcon(QIcon("AUBoutique/resources/IMAGES/filled.png"))
                else:
                    star_buttons[j].setIcon(QIcon("AUBoutique/resources/IMAGES/empty.png"))

        button.enterEvent = lambda event, idx=i: on_hover_enter(idx)
        button.leaveEvent = lambda event: on_hover_leave()

        ratinglayout.addWidget(button)
        star_buttons.append(button)

    layout = QVBoxLayout()
    layout.setSpacing(15)

    details = [
        f"Name: {product['name']}",
        f"Price: {product['price']}",
        f"Description: {product['description']}",
        f"Rating: {product['rating']}",
        f"Owner: {product['owner']}"
    ]
    for detail in details:
        label = QLabel(detail)
        layout.addWidget(label)

    layout.addLayout(ratelayout)

    buy_button = QPushButton("Buy")
    buy_button.setStyleSheet("""
        QPushButton {
            background-color: #FFD700;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
        }
        QPushButton:hover {
            background-color: #1565C0;
        }
    """)


    def buy_action():
        response = client.buyProducts(product)
        if response == "SUCCESS":
            successfulBuy()
        elif response == "INSUFFICIENT_FUNDS":
            notEnoughMon()
        elif response == "OWN_PRODUCT":
            ownProduct()
            
    def successfulBuy():
        QMessageBox.information(dialog, "Purchase", "Thank you for your purchase")
        dialog.accept()
    def notEnoughMon():
        QMessageBox.information(dialog, "Balance", "Not enough money")
        dialog.accept() 
    def ownProduct():
        QMessageBox.information(dialog, "Problem", "You cannot buy your own products!")
        dialog.accept()  
     

    buy_button.clicked.connect(buy_action)
    layout.addWidget(buy_button)

    back_button = QPushButton("Back", dialog)
    back_button.setStyleSheet("""
        QPushButton {
            background-color: #FFC107;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
        }
        QPushButton:hover {
            background-color: #FFA000;
        }
    """)
    back_button.clicked.connect(dialog.accept)
    layout.addWidget(back_button)

    dialog.setLayout(layout)
    dialog.exec_()

# Function to create the main product grid frame
def create_product_grid(query=""):
    container = QWidget()
    smallcontainer = QWidget()
    container_market_layout = QVBoxLayout()
    grid_layout = QGridLayout()
    grid_layout.setSpacing(20)

    # Filter products based on search query
    filtered_products = filter_products(query)

    for index, product in enumerate(filtered_products):
        row = index // 3
        col = index % 3

        product_card = QFrame()
        card_layout = QVBoxLayout()

        piclabel = QLabel()
        piclabel.setFixedSize(200, 200)
        piclabel.setStyleSheet("border: 1px solid black;")
        FILE_PATH = "IMAGES/greenapple.jpg"
        try:
            pixmap = QPixmap(FILE_PATH)
            if pixmap.isNull():
                raise FileNotFoundError
        except FileNotFoundError:
            pixmap = QPixmap("IMAGES/default.jpg")

        scaled_pixmap = pixmap.scaled(
            piclabel.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        piclabel.setPixmap(scaled_pixmap)
        card_layout.addWidget(piclabel)

        name_label = QLabel(product["name"])
        name_label.setWordWrap(True)
        name_label.setFixedWidth(200)
        name_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(name_label)

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
        product_card.setFixedSize(220, 320)
        grid_layout.addWidget(product_card, row, col)

    smallcontainer.setLayout(grid_layout)
    banner_image = create_banner_image()
    container_market_layout.addWidget(banner_image)
    container_market_layout.addWidget(smallcontainer)
    container.setLayout(container_market_layout)

    scroll_area = QScrollArea()
    scroll_area.setWidget(container)
    scroll_area.setWidgetResizable(True)
    return scroll_area

# Function to create the banner image
def create_banner_image():
    banner_label = QLabel()
    banner_label.set