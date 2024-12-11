import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QScrollArea, QComboBox
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
from ..BackEnd import client



class UserInfoPanel(QWidget):
    def __init__(self, username):
        super().__init__()

        self.font = QFont("Arial", 13)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(15, 15, 15, 15)

        self.title_label = QLabel("User Information")
        self.title_label.setFont(QFont("Helvetica", 16, QFont.Bold))
        self.title_label.setStyleSheet("color: white;")
        self.layout.addWidget(self.title_label)

        

        self.add_user_info(f"Username: {username}")

       
        self.add_currency_dropdown(username)

       
        self.panel = QWidget()
        self.panel.setStyleSheet("background-color: rgba(44, 47, 51, 0.9); border-radius: 10px; padding: 20px;")
        self.panel.setLayout(self.layout)

        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.panel)

    def add_user_info(self, text):
        label = QLabel(text)
        label.setFont(self.font)
        label.setStyleSheet("color: white;")
        self.layout.addWidget(label)

    def add_currency_dropdown(self, username):
        
        currency_label = QLabel("Select Currency:")
        currency_label.setFont(self.font)
        currency_label.setStyleSheet("color: white;")
        self.layout.addWidget(currency_label)

        
        self.currency_dropdown = QComboBox()
        self.currency_dropdown.addItems(["USD", "EUR", "GBP", "LBP"])  # Add more currencies as needed
        self.currency_dropdown.setStyleSheet("""
            QComboBox {
                background-color: white;
                color: black;
                font-size: 14px;
                padding: 5px;
                border-radius: 5px;
            }
        """)

        
        self.currency_dropdown.currentTextChanged.connect(lambda currency: self.on_currency_change(username, currency))
        self.layout.addWidget(self.currency_dropdown)

    def on_currency_change(self, username, currency):
        print(f"Selected currency: {currency}")  
        client.setUserCurrency(username, currency)

class ProductItem(QFrame):
    def __init__(self, name, buyers):
        super().__init__()

       
        self.setStyleSheet("border: 1px solid #ddd; border-radius: 10px; padding: 10px; margin-bottom: 2px;")
        item_layout = QHBoxLayout()

       

        
        details_layout = QVBoxLayout()
        self.product_name = QLabel(name)
        self.product_name.setFont(QFont("Sans-serif", 13))
        self.product_name.setStyleSheet("color: black;")
        details_layout.addWidget(self.product_name)

        

        
        buyers_label = QLabel(f"Buyers: {', '.join(buyers) if buyers else 'No buyers yet'}")
        buyers_label.setFont(QFont("Sans-serif", 13))
        buyers_label.setStyleSheet("color: black;")
        details_layout.addWidget(buyers_label)

        item_layout.addLayout(details_layout)
        self.setLayout(item_layout)


class PurchasedProductItem(QFrame):
    def __init__(self, name, owner):
        super().__init__()

       
        self.setStyleSheet("border: 1px solid #ddd; border-radius: 10px; padding: 10px; margin-bottom: 2px;")
        item_layout = QHBoxLayout()

        

        details_layout = QVBoxLayout()
        self.product_name = QLabel(f"Product name: {name}")
        self.product_name.setFont(QFont("Sans-serif", 13))
        self.product_name.setStyleSheet("color: black;")
        details_layout.addWidget(self.product_name)
        print("This is the product name", name)
        #self.product_rating = QLabel(f"Rating: {rating} ★")
        print("This is the owner's name", owner)
        self.product_owner = QLabel(f"Owner: {owner}")
        self.product_owner.setFont(QFont("Sans-serif", 13))
        self.product_owner.setStyleSheet("color: black;")
        details_layout.addWidget(self.product_owner)

        item_layout.addLayout(details_layout)
        self.setLayout(item_layout)


class ProductsPanel(QWidget):
    def __init__(self, username, title, products):
        super().__init__()

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(8, 8, 8, 8)

        self.products_label = QLabel(title)
        self.products_label.setFont(QFont("Helvetica", 13, QFont.Bold))
        self.products_label.setStyleSheet("color: black;")
        self.layout.addWidget(self.products_label)
        for product in products:
            buyers = client.getBuyers(username, product)
            product_item = ProductItem(product, buyers)  # Include buyers
            self.layout.addWidget(product_item)

        self.panel = QWidget()
        self.panel.setStyleSheet("background-color: rgba(255, 255, 255, 0.7); border-radius: 10px; padding: 20px;")
        self.panel.setLayout(self.layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.panel)


class PurchasedProductsPanel(QWidget):
    def __init__(self, title, products):
        super().__init__()

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(8, 8, 8, 8)

        self.products_label = QLabel(title)
        self.products_label.setFont(QFont("Helvetica", 13, QFont.Bold))
        self.products_label.setStyleSheet("color: black;")
        self.layout.addWidget(self.products_label)

        print("Printing products")
        print(products)
        print("purchased products array of dictionaries is empty")
             
        for product in products:
            product_item = PurchasedProductItem(product['name'], product['owner'])
            self.layout.addWidget(product_item)

        self.panel = QWidget()
        self.panel.setStyleSheet("background-color: rgba(255, 255, 255, 0.7); border-radius: 10px; padding: 20px;")
        self.panel.setLayout(self.layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.panel)


class profileInfo(QWidget):
    def __init__(self, username):
        super().__init__()

        self.setWindowTitle("User Profile")

        self.main_layout = QHBoxLayout()

        self.setStyleSheet("background-color: #F5F5DC;")

        self.user_info_panel = UserInfoPanel(username)
        self.main_layout.addWidget(self.user_info_panel.scroll_area)

        

        my_products = client.myProductsArray()
        productList = []
        for prod in my_products:
            if prod["owner"] == username:
                productList.append(prod["name"])
        self.my_products_panel = ProductsPanel(username, "My Products", productList)
        self.main_layout.addWidget(self.my_products_panel.scroll_area)
        purchasedProducts = client.purchasedProductsArray(username)
        self.purchased_products_panel = PurchasedProductsPanel("Purchased Products", purchasedProducts)
        self.main_layout.addWidget(self.purchased_products_panel.scroll_area)

        self.setLayout(self.main_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = profileInfo("trial")
    window.show()

    sys.exit(app.exec_())