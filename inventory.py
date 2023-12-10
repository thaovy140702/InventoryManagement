from datetime import datetime

class Inventory:

    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.created_at = datetime.now().strftime('%Y-%m-%d %H:%M')
        self.updated_at = datetime.now().strftime('%Y-%m-%d %H:%M')
