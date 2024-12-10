import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLabel, QScrollArea, QFrame, QDialog, QMessageBox, QHBoxLayout, QLineEdit
)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from . import notifications
from ..BackEnd import client
from . import chat
from ..BackEnd import conversion

wallet1 = 100

def filter_products(query):
    filtered = []
    for product in products:
        if query.lower() in product["name"].lower() or query.lower() in product["description"].lower():
            filtered.append(product)
    return filtered

db = sqlite3.connect('db.AUBoutique')
db.execute("PRAGMA foreign_keys=on")
cursor = db.cursor()


def rate(star_butts, rating_label, updatedrating, rating, product):
    rating1 = rating
    rating_label.setText(f"Your Rating: {rating1}/5")

    for i in range(5):
        if i < rating:
            star_butts[i].setIcon(QIcon("AUBoutique/resources/IMAGES/filled.png"))  # Filled star icon
        else:
            star_butts[i].setIcon(QIcon("AUBoutique/resources/IMAGES/empty.png"))  # Empty star icon

    newRating = ((product["numberOfRatings"] * product["rating"]) + rating1) / (product["numberOfRatings"] + 1)
    product["rating"] = newRating
    product["numberOfRatings"] += 1
    cursor.execute("UPDATE Products SET avgRating=?, numberOfRatings=? WHERE product_name=?", (newRating, product["numberOfRatings"], product["name"]))
    db.commit()
    updatedrating.setText(f"Updated Rating: {newRating}")

def confirmrating(star_butts, rating_label, updatedrating, i, product):
    message = QMessageBox()
    message.setIcon(QMessageBox.Question)
    message.setWindowTitle("Confirm Rating")
    message.setText("Are you sure you want to confirm your rating?")
    message.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    message.setDefaultButton(QMessageBox.No)

    result = message.exec_()
    if result == QMessageBox.Yes:
        rate(star_butts, rating_label, updatedrating, i, product)

def show_product_details(self, product, username):
    dialog = QDialog()
    dialog.setWindowTitle(f"Details of {product['name']}")
    dialog.setGeometry(200, 200, 500, 400)
    
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
    # cursor.execute("SELECT currency from Users WHERE username=?", (username,))
    # curr = cursor.fetchall()[0]
    currency = client.getUserCurrency(username)
    newprice = conversion.convert("USD", currency, product['price'])
    details = [
        f"Name: {product['name']}",
        f"Price: {newprice} (in {currency})" ,
        f"Description: {product['description']}",
        f"Quantity: {product['quantity']}",
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


    def buy_action(dialog):
        print("buying ")
        response = client.buyProducts(product['name'], product['owner'])
        print("buying productss")
        if response == "SUCCESS":
            successfulBuy(dialog)
        elif response == "INSUFFICIENT_FUNDS":
            notEnoughMon(dialog)
        elif response == "OWN_PRODUCT":
            ownProduct(dialog)
        elif response == "notOntheMarketAnymore":
            notifications.getErrorNotification("Error", "Cannot buy this product", self)

            
    def successfulBuy(dialog):
        notifications.getSuccessNotification("Success!", "", self)
        dialog.accept() 
    def notEnoughMon(dialog):
        notifications.getErrorNotification("Error", "Not enough money", self)
        dialog.accept() 
    def ownProduct(dialog):
        notifications.getErrorNotification("Error", "Cannot buy your own product", self)
        dialog.accept()  
     

    buy_button.clicked.connect(lambda: buy_action(dialog))
    layout.addWidget(buy_button)

    back_button = QPushButton("Chat", dialog)
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
    back_button.clicked.connect(lambda: openChat(dialog, product['owner'], username))
    layout.addWidget(back_button)

    dialog.setLayout(layout)
    dialog.exec_()
def openChat(dialog, user, myusername):
    dialog.accept()
    chat_window = chat.MessagingWindow(user, myusername)
    chat_window.show()
def create_product_grid(query=""):
    container = QWidget()
    smallcontainer = QWidget()
    container_market_layout = QVBoxLayout()
    grid_layout = QGridLayout()
    grid_layout.setSpacing(20)

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

def create_banner_image():
    banner_label = QLabel()
    banner_label.set