from datetime import datetime

class Product:
    def __init__(self, product_name, unit_price, quantity, category, inventory):
        self.name = product_name
        self.price = unit_price
        self.category = category
        self.quantity = quantity
        self.inventory = inventory
        self.created_at = datetime.now().strftime('%Y-%m-%d %H:%M')
        self.updated_at = datetime.now().strftime('%Y-%m-%d %H:%M')