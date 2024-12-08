import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QScrollArea
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
from ..BackEnd import client

purchasedProducts = [("Cleaner", 4.5, "tony","empty.png"),("Dish", 3, "tony", "empty.png"),("Cleaner", 3.4, "tony","empty.png"),("Cleaner", 4.8, "tony", "empty.png")]
my_products = [("Ball", "4.5", "/path/to/macbook.jpg"),("Fork", "4.7", "/path/to/iphone.jpg"), ("Water bottle", 3.2, "star.png")]

#purchasedProducts = client.purchasedProductsArray(username, currency)

class UserInfoPanel(QWidget):
    def __init__(self):
        super().__init__()

        # Set up font
        self.font = QFont("Arial", 13)

        # Create layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(15, 15, 15, 15)

        # Title
        self.title_label = QLabel("User Information")
        self.title_label.setFont(QFont("Helvetica", 16, QFont.Bold))
        self.title_label.setStyleSheet("color: white;")
        self.layout.addWidget(self.title_label)

        # User info fields
        self.add_user_info("Name: Anthony Kanaan")
        self.add_user_info("Email: anthonyjohn@gmail.com")
        self.add_user_info("Username: ")

        # Panel container
        self.panel = QWidget()
        self.panel.setStyleSheet("background-color: rgba(44, 47, 51, 0.9); border-radius: 10px; padding: 20px;")
        self.panel.setLayout(self.layout)

        # Scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.panel)

    def add_user_info(self, text):
        label = QLabel(text)
        label.setFont(self.font)
        label.setStyleSheet("color: white;")
        self.layout.addWidget(label)


class ProductItem(QFrame):
    def __init__(self, name, rating, image_path):
        super().__init__()

        # Set up layout
        self.setStyleSheet("border: 1px solid #ddd; border-radius: 10px; padding: 10px; margin-bottom: 2px;")
        item_layout = QHBoxLayout()

        # Product image
        self.product_image = QLabel()
        pixmap = QPixmap(image_path).scaled(100, 100, Qt.KeepAspectRatio)
        self.product_image.setPixmap(pixmap)
        item_layout.addWidget(self.product_image)

        # Product details
        details_layout = QVBoxLayout()
        self.product_name = QLabel(name)
        self.product_name.setFont(QFont("Sans-serif", 13))
        self.product_name.setStyleSheet("color: black;")
        details_layout.addWidget(self.product_name)

        self.product_rating = QLabel(f"Rating: {rating} ★")
        
        self.product_rating.setFont(QFont("Sans-serif", 13))
        self.product_rating.setStyleSheet("color: black;")
        details_layout.addWidget(self.product_rating)

        item_layout.addLayout(details_layout)
        self.setLayout(item_layout)
class PurchasedProductItem(QFrame):
    def __init__(self, name, rating, owner, image_path):
        super().__init__()

        # Set up layout
        self.setStyleSheet("border: 1px solid #ddd; border-radius: 10px; padding: 10px; margin-bottom: 2px;")
        item_layout = QHBoxLayout()

        # Product image
        self.product_image = QLabel()
        pixmap = QPixmap(image_path).scaled(100, 100, Qt.KeepAspectRatio)
        self.product_image.setPixmap(pixmap)
        item_layout.addWidget(self.product_image)

        # Product details
        details_layout = QVBoxLayout()
        self.product_name = QLabel(name)
        self.product_name.setFont(QFont("Sans-serif", 13))
        self.product_name.setStyleSheet("color: black;")
        details_layout.addWidget(self.product_name)

        self.product_rating = QLabel(f"Rating: {rating} ★")
        self.product_owner = QLabel(f"Owner: {owner} ")
        self.product_owner.setFont(QFont("Sans-serif", 13))
        self.product_rating.setFont(QFont("Sans-serif", 13))
        self.product_rating.setStyleSheet("color: black;")
        details_layout.addWidget(self.product_rating)
        details_layout.addWidget(self.product_owner)

        item_layout.addLayout(details_layout)
        self.setLayout(item_layout)


class ProductsPanel(QWidget):
    def __init__(self, title, products):
        super().__init__()

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(8, 8, 8, 8)

        # Set the title label
        self.products_label = QLabel(title)
        self.products_label.setFont(QFont("Helvetica", 13, QFont.Bold))
        self.products_label.setStyleSheet("color: black;")
        self.layout.addWidget(self.products_label)

        # Add product items
        for product in products:
            product_item = ProductItem(product[0], product[1], product[2])
            self.layout.addWidget(product_item)

        # Create a panel for the product items
        self.panel = QWidget()
        self.panel.setStyleSheet("background-color: rgba(255, 255, 255, 0.7); border-radius: 10px; padding: 20px;")
        self.panel.setLayout(self.layout)

        # Wrap the panel in a scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.panel)
class PurchasedProductsPanel(QWidget):
    def __init__(self, title, products):
        super().__init__()

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(8, 8, 8, 8)

        # Set the title label
        self.products_label = QLabel(title)
        self.products_label.setFont(QFont("Helvetica", 13, QFont.Bold))
        self.products_label.setStyleSheet("color: black;")
        self.layout.addWidget(self.products_label)

        # Add product items
        for product in products:
            product_item = PurchasedProductItem(product[0], product[1], product[2], product[3])
            self.layout.addWidget(product_item)

        # Create a panel for the product items
        self.panel = QWidget()
        self.panel.setStyleSheet("background-color: rgba(255, 255, 255, 0.7); border-radius: 10px; padding: 20px;")
        self.panel.setLayout(self.layout)

        # Wrap the panel in a scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.panel)



class profileInfo(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("User Profile")

        # Main layout (horizontal)
        self.main_layout = QHBoxLayout()

        # Set the overall background color
        self.setStyleSheet("background-color: #F5F5DC;")

        # Left side: User info
        self.user_info_panel = UserInfoPanel()
        self.main_layout.addWidget(self.user_info_panel.scroll_area)

        # Right side: Products (My Products and Purchased Products)
        self.my_products = [
            ("Apple MacBook Pro M4", "4.5", "/path/to/macbook.jpg"),
            ("Apple iPhone 15 Pro", "4.7", "/path/to/iphone.jpg"),
        ]
        self.purchased_products = [
            ("Apple Pencil 2nd Generation", "3.7", "/path/to/pencil.jpg"),
            ("Airpods Pro 2", "4.5", "/path/to/airpods.jpg"),
        ]

        self.my_products_panel = ProductsPanel("My Products", self.my_products)
        self.main_layout.addWidget(self.my_products_panel.scroll_area)

        self.purchased_products_panel = PurchasedProductsPanel("Purchased Products", purchasedProducts)
        self.main_layout.addWidget(self.purchased_products_panel.scroll_area)

        # Set the layout for the main window
        self.setLayout(self.main_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create and show the main window
    window = profileInfo()
    window.show()

    sys.exit(app.exec_())