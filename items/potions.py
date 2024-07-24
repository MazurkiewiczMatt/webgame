from .item import Item, register_item


class Potion(Item):
    def __init__(self):
        super().__init__()
        self.type = "potion"

    def use(self, player, world):
        pass

@register_item("beer")
class Beer(Potion):
    def __init__(self):
        super().__init__()
        self.type = "potion"
        self.name = "Beer"
        self.price = 1
        self.image_path = "items/img/beer.jpg"

    def use(self, player, world):
        if "Very drunk" in player.traits:
            player.traits.remove("Very drunk")
            world.message = ":red-background[You became blackout drunk.]"
            player.traits.append("Blackout drunk")
            world.update()
            player.update(world)
        elif "Drunk" in player.traits:
            player.traits.remove("Drunk")
            world.message = "You drank another beer and became Very drunk."
            player.traits.append("Very drunk")
        else:
            world.message = "You drank a beer and became Drunk."
            player.traits.append("Drunk")


@register_item("nootropic")
class Nootropic(Potion):
    def __init__(self):
        super().__init__()
        self.type = "potion"
        self.name = "Nootropic Potion"
        self.price = 5
        self.image_path = "items/img/nootropic.png"

    def use(self, player, world):
        player.abilities["Wisdom"] += 5
        world.message = ":green-background[After drinking the nootropic potion, your wisdom increased by 5!]"
