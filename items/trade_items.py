from .item import Item, register_item


@register_item("steel-ingot")
class SteelIngot(Item):
    def __init__(self):
        super().__init__()
        self.name = "Steel ingot"
        self.image_path = "items/img/steel-ingot.jpg"

@register_item("silver-ingot")
class SilverIngot(Item):
    def __init__(self):
        super().__init__()
        self.name = "Silver ingot"
        self.image_path = "items/img/silver-ingot.jpg"

@register_item("sxotic-fish")
class ExoticFish(Item):
    def __init__(self):
        super().__init__()
        self.name = "Exotic fish"
        self.image_path = "items/img/exotic-fish.jpg"