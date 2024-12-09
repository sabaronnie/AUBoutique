import sys
import sqlite3
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QGridLayout, QApplication, QMainWindow, QScrollArea, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QStackedWidget, QDialog, QDialogButtonBox, QLineEdit, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon, QPainter, QColor
from PyQt5.QtCore import Qt, QSize
from .market import show_product_details
from . import market
from .chat import MainPage
from .profile import profileInfo
from .createproduct import MainWindow
from ..BackEnd import client

# products = [
#     {"name": "Green Apple from Batroun, Lebanon.", "price": "$10", "description": "A great product from the lush orchards of Lebanon.","rating": 0, "owner": "Owner 1", "numberOfRatings" : 0},
#     {"name": "Premium Red Grapes", "price": "$15", "description": "Sweet and fresh red grapes.","rating": 0, "owner": "Owner 2", "numberOfRatings" : 0},
#     {"name": "Golden Pears", "price": "$12", "description": "Crisp and juicy golden pears.","rating": 0, "owner": "Owner 3", "numberOfRatings" : 0},
#     {"name": "Exotic Mango", "price": "$20", "description": "Fresh tropical mangoes.", "rating": 0,"owner": "Owner 4", "numberOfRatings" : 0},
#     {"name": "Fresh Blueberries", "price": "$18", "description": "Organic blueberries.","rating": 0, "owner": "Owner 5", "numberOfRatings" : 0},
#     {"name": "Ripe Strawberries", "price": "$22", "description": "Sweet and delicious strawberries.","rating": 0, "owner": "Owner 6", "numberOfRatings" : 0},
# ]
db = sqlite3.connect('db.AUBoutique')
db.execute("PRAGMA foreign_keys=on")
cursor = db.cursor()

products = []
class General1(QMainWindow):
    def __init__(self, username, password):
        global products
        super().__init__()
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(985, 820)
        self.setWindowTitle("AUBoutique")
        #TODO:
        cursor.execute("SELECT balance FROM Users WHERE username = ?", (username,))
        wallet1 = cursor.fetchone()[0]
        currency = client.getUserCurrency(username)
        products = client.populateProductsArray(currency)
        self.initUI(username, password, wallet1, products)
        


    def initUI(self, username, password, wallet1, products):
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
        self.tab_buttons_widget = self.create_tab_buttons(wallet1, username)

        # Add banner and tab buttons to the layout
        main_layout.addWidget(self.banner_widget)
        main_layout.addWidget(self.tab_buttons_widget)

        # Add the stacked widget to hold the content for each tab
        main_layout.addWidget(self.stacked_widget)

        
        # Create the content for each tab
        self.create_tab_content(username, password)

        # Create a QScrollArea to make the layout scrollable
        scroll_area = QScrollArea()
        scroll_area.setWidget(main_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet(""" 
            QScrollArea {
                border:none;
            }
            QScrollBar:vertical {
                border: none;  
                background: transparent;  
                width: 6px;  
            }
            QScrollBar::handle:vertical {
                background: gray;  
                min-height: 10px;  
                border-radius: 3px;  
            }
            QScrollBar::handle:vertical:hover {
                background: gray;  
            }
            QScrollBar::handle:vertical:pressed {
                background: gray;  
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;  
                background: none;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;  
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
        pixmap = QPixmap("AUBoutique/resources/IMAGES/AUB_Banner.png")  # Replace with your banner image path
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

    def create_tab_buttons(self, wallet1, username):
        """Creates tab buttons widget."""
        tab_buttons_widget = QWidget()
        tab_buttons_layout = QHBoxLayout(tab_buttons_widget)
        tab_buttons_layout.setContentsMargins(0, 0, 0, 0)
        tab_buttons_layout.setSpacing(0)

        #use cursor hon
        # 
        # Tab buttons
        for i, page in enumerate(["Home", "Sell a Product", "Chat", "Profile", "Wallet", "Log Out"]):  # Added "Chat" tab
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
                    background-color: #34495e;
                }
            """)
            
            btn.clicked.connect(lambda checked, wallet = wallet1: self.on_tab_button_click(wallet, username))
            tab_buttons_layout.addWidget(btn)

        tab_buttons_widget.setStyleSheet("background-color: #34495e;")  # Tab buttons background
        return tab_buttons_widget


    def on_tab_button_click(self, wallet1, username):
       
        """Handles the tab button click event."""
        global products
        sender = self.sender()
        if sender.text() == "Home":
            self.stacked_widget.setCurrentIndex(0)
            print("ENTERING HOME")
            currency = client.getUserCurrency(username)
            #hon we created it, men hota hon as global>
            products = client.populateProductsArray(currency)
            print("THIS SHOULD APPEAR")
            print(products)
            self.banner_widget.show()
            self.update()
        elif sender.text() == "Sell a Product":
            self.stacked_widget.setCurrentIndex(1)
            self.banner_widget.hide()
        elif sender.text() == "Chat":
            self.stacked_widget.setCurrentIndex(2)
            self.banner_widget.hide()  # Hide the banner when switching to Chat
        elif sender.text() == "Profile":
            #self.purchasedProducts = client.purchasedProductsArray(username)
            # self.my_products = client.populateProductsArray()
            #self.productList = []
            #for prod in self.my_products:
            # if prod["owner"] == username:
            #     self.productList.append(prod["name"])
            self.stacked_widget.setCurrentIndex(3)
            self.banner_widget.hide()  # Hide the banner when switching to Profile
        elif sender.text() == "Wallet":
            self.stacked_widget.setCurrentIndex(4)
            self.show_wallet_dialog(wallet1, username)
        elif sender.text() == "Log Out":
            self.stacked_widget.setCurrentIndex(5)
            self.show_logout_confirmation(username)
    def create_tab_content(self, username, password):
        """Creates the content for each tab."""
        global products
        # Home tab content
        home_container = QWidget()
        home_layout = QGridLayout(home_container)
        home_layout.setSpacing(20)
        counter = 0
        #for product in products:
        #   product_widget = self.create_product_widget(product)
        #   row, col = divmod(counter, 4)  # Arrange products in a grid (3 per row)
        #    counter += 1
        #   home_layout.addWidget(product_widget, row, col)

        search_bar = QLineEdit()
        search_bar.setPlaceholderText("Search products...")
        search_bar.textChanged.connect(lambda: self.filter_products(username))
        
        search_bar.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border-radius: 15px;
                background-color: #f0f0f0;
                border: 2px solid #ccc;
                font-size: 16px;
                color: #333;
            }
            
            QLineEdit:focus {
                border: 2px solid #4CAF50; /* Green border on focus */
                background-color: #fff;
            }
            
            QLineEdit::placeholder {
                color: #888;
                font-style: italic;
            }
            
            QLineEdit::clear-button {
                background-color: transparent;
                border: none;
                width: 16px;
                height: 16px;
            }
            
            QLineEdit::clear-button:hover {
                background-color: #ddd;
            }
        """)
        
        home_layout.addWidget(search_bar, 0, 0, 1, 4)  # Span the search bar across all columns

        self.home_layout = home_layout
        self.counter = 0  # Counter to keep track of product placement
        
        self.product_widgets = []  # List to store product widgets
        self.product_display(username)  # Initially display all products

        self.stacked_widget.addWidget(home_container)
        
        productCreator_widget = MainWindow(username)
        self.stacked_widget.addWidget(productCreator_widget)
        # Chat tab content
        chat_widget = MainPage(username, password)  # Use the MainPage class from chat.py
        self.stacked_widget.addWidget(chat_widget)
        
        profile1_widget1 = profileInfo(username)
        self.stacked_widget.addWidget(profile1_widget1)

        # Profile tab content
        profile_widget = QWidget()
        profile_layout = QVBoxLayout(profile_widget)
        profile_layout.addWidget(QLabel("Your Profile"))
        self.stacked_widget.addWidget(profile_widget)

        # Wallet tab content
        wallet_widget = QWidget()
        wallet_layout = QVBoxLayout(wallet_widget)
        wallet_layout.addWidget(QLabel("Your Wallet"))
        wallet_layout.addWidget(QPushButton("Balance: $25 USD"))  # Example wallet balance
        self.stacked_widget.addWidget(wallet_widget)
    def filter_products(self, username):
        global products
        """Filters products based on the search query."""
        search_text = self.home_layout.itemAtPosition(0, 0).widget().text().lower()  # Get text from search bar
        filtered_products = [product for product in products if search_text in product['name'].lower()]

        self.update_product_display(username, filtered_products)
    def product_display(self, username):
        global products
        """Updates the product display based on filtered products."""
        # Remove existing product widgets
        for widget in self.product_widgets:
            widget.setParent(None)

        self.product_widgets = []

    # Set the number of products per row (4 per row in this case)
        products_per_row = 4

        for i, product in enumerate(products):
            product_widget = self.create_product_widget(username, product)
            # Calculate the row and column based on the number of products per row
            row, col = divmod(i, products_per_row)
            # Add the product widget to the grid layout
            self.home_layout.addWidget(product_widget, row + 1, col)
            # Keep track of the product widget for removal later
            self.product_widgets.append(product_widget)
    def update_product_display(self, username, filtered_products):
        
        """Updates the product display based on filtered products."""
        # Remove existing product widgets
        for widget in self.product_widgets:
            widget.setParent(None)

        self.product_widgets = []

    # Set the number of products per row (4 per row in this case)
        products_per_row = 4

        for i, product in enumerate(filtered_products):
            product_widget = self.create_product_widget(username, product)
            # Calculate the row and column based on the number of products per row
            row, col = divmod(i, products_per_row)
            # Add the product widget to the grid layout
            self.home_layout.addWidget(product_widget, row + 1, col)
            # Keep track of the product widget for removal later
            self.product_widgets.append(product_widget)
    def show_logout_confirmation(self,username):
        """Displays a confirmation dialog for logging out."""
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setWindowTitle("Log Out")
        msg_box.setText("Are you sure you want to log out?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)
        
        response = msg_box.exec_()
        if response == QMessageBox.Yes:
            print("User confirmed log out")
            response = client.LogOut(username)
            if response == "LOGOUT_SUCCESS":
                self.close()  # Close the MainWindow
        else:
            print("User canceled log out")        
    def show_wallet_dialog(self, wallet1, username):
        """Show a dialog with the wallet details and allow adding money."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Wallet Details")
        dialog.setGeometry(100, 100, 300, 200)  # Increase height for new content
        layout = QVBoxLayout()
        
        # Display the current wallet balance
        # cursor.execute("SELECT balance FROM Users WHERE username = ?", (username,))
        # wallet1 = cursor.fetchone()[0]
        wallet1 = client.getCurrentBalance()
        wallet_label = QLabel(f"Your balance: {wallet1} USD", dialog)
        layout.addWidget(wallet_label)

        # Add input field for adding money
        add_money_label = QLabel("Enter amount to add:", dialog)
        layout.addWidget(add_money_label)

        # Create a QLineEdit to input the amount
        add_money_input = QLineEdit(dialog)
        add_money_input.setPlaceholderText("Amount in USD")
        layout.addWidget(add_money_input)

        # Button to add money to the wallet
        add_money_button = QPushButton("Add Money", dialog)
        layout.addWidget(add_money_button)

        # Button to confirm and close the dialog
        button_box = QDialogButtonBox(QDialogButtonBox.Ok, dialog)
        button_box.accepted.connect(dialog.accept)
        layout.addWidget(button_box)

        # Connect the Add Money button to a method that updates the wallet
        def on_add_money(wallet1, username):
            try:
                amount = float(add_money_input.text())  # Get the input amount
                if amount > 0:
                    wallet1 += amount  # Add the money to the wallet          db.commit()
                    # cursor.execute("UPDATE Users SET balance = ? WHERE username = ?", (wallet1, username))
                    # db.commit()
                    client.setNewBalance(wallet1)
                    wallet_label.setText(f"Your balance: {wallet1} USD")  # Update the wallet balance display
                    add_money_input.clear()  # Clear the input field
                else:
                    wallet_label.setText("Please enter a positive amount.")  # Error message
            except ValueError:
                wallet_label.setText("Invalid amount. Please enter a number.")  # Handle invalid input

        add_money_button.clicked.connect(lambda checked, wallet = wallet1: on_add_money(wallet1, username))
        

        dialog.setLayout(layout)
        dialog.exec_()

    def create_product_widget(self, username, product):
        """Creates a widget for a single product."""
        product_widget = QWidget()
        product_layout = QVBoxLayout(product_widget)
        product_layout.setSpacing(10)
        
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(15)  # Adjust for more/less blur
        shadow_effect.setXOffset(0)  # No horizontal offset
        shadow_effect.setYOffset(0)  # No vertical offset
        shadow_effect.setColor(QColor(0, 0, 0, 160))  # Semi-transparent black shadow
        product_widget.setGraphicsEffect(shadow_effect)
        
        product_image = QPushButton()
        #ik
        image_data = client.getProductImage(product["owner"], product["name"])  # Replace 'image' with your key for image bytes
        if image_data:
            pixmap = QPixmap()
            pixmap.loadFromData(image_data)  # Load image from bytes
        else:
            pixmap = QPixmap(150, 150)  # Placeholder pixmap if image data is missing
            pixmap.fill(Qt.gray)  # Fill with a placeholder color
        # Create the product image button
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
        product_button = QPushButton(product['name'])
        product_button.setFixedSize(100, 30)
        product_button.setStyleSheet("""
        QPushButton {
            background-color: #FF5722;
            color: white;
            font-family: 'Segoe UI', sans-serif;
            font-size: 14px;
            border: none;
            border-radius: 8px;
            padding: 8px 12px;
        }
        QPushButton:hover {
            background-color: #E64A19;
        }
        QPushButton:pressed {
            background-color: #D84315;
        }
        """)

        #eh eh thats not wrong its blue
        # laeanno u imported specifically show_product_details enta 
        # Add the product name button to the layout, also centered
        product_layout.addWidget(product_button, alignment=Qt.AlignCenter)
        
        product_image.clicked.connect(lambda checked, p=product: show_product_details(self, p, username))
        product_button.clicked.connect(lambda checked, p=product: show_product_details(self, p, username))

        return product_widget


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = General1()
    window.show()
    sys.exit(app.exec_())