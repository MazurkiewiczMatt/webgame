from .item import Item, register_item


@register_item("temple-key")
class TempleKey(Item):
    def __init__(self):
        super().__init__()
        self.name = "Mysterious key"
