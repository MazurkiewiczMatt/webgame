ITEMS_DATABASE = {}

def register_item(key):
    def register(item):
        item.key = key
        ITEMS_DATABASE[key] = item
        return item
    return register

class Item:
    def __init__(self):
        self.image_path = None
        self.price = 0
        self.name = "Generic item"
        self.type = "Generic"
        self.description = ""
        self.stackable = True

