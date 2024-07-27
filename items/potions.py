import random

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
            player.personality["Degeneracy"] += 6
            world.message += "   \r You lose control of yourself (*+6* Degeneracy)."
            world.update(player)
            player.update(world)
        elif "Drunk" in player.traits:
            player.traits.remove("Drunk")
            world.message = "You drank another beer and became Very drunk."
            degeneracy_bonus = random.randint(1, 4)
            player.personality["Degeneracy"] += degeneracy_bonus
            world.message += f"   \r You lose control of yourself (*+{degeneracy_bonus}* Degeneracy)."
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
        self.price = 20
        self.image_path = "items/img/nootropic.png"
        self.description = "Increases Wisdom by 1-5."

    def use(self, player, world):
        wisdom_bonus = min(random.randint(1, 5), random.randint(1, 10))
        player.abilities["Wisdom"] += wisdom_bonus
        world.message = f"After drinking the nootropic potion, :green-background[your wisdom increased by {wisdom_bonus}.]"

@register_item("energy_drink")
class EnergyDrink(Potion):
    def __init__(self):
        super().__init__()
        self.type = "potion"
        self.name = "Energy Drink"
        self.price = 5
        self.image_path = "items/img/energy_drink.jpg"
        self.description = "Increases Energy by 3-10."

    def use(self, player, world):
        bonus = random.randint(3, 10)
        player.personality["Energy"] += bonus
        world.message = f"After drinking the energy drink, :green-background[your Energy increased by {bonus}.]"
