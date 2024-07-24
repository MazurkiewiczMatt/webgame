from .item import Item


class Weapon(Item):
    def __init__(self):
        super().__init__()
        self.type = "weapon"
        self.damage = 0
