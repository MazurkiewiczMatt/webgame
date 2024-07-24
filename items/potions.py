from .item import Item, register_item


class Potion(Item):
    def __init__(self):
        super().__init__()
        self.type = "potion"

    def use(self, player):
        return self

@register_item("beer")
class Beer(Potion):
    def __init__(self):
        super().__init__()
        self.type = "potion"
        self.name = "Beer"
        self.price = 1
        self.image_path = "items/img/beer.jpg"

    def use(self, player):
        player.traits.add("Drunk")
        return None
