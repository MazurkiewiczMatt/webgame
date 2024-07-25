import random
from PIL import Image

from quests import Quest, Action
from .shelters import TempleShelterAction, HotelShelterAction


class ShelterPlayfairQuest(Quest):
    def __init__(self):
        super().__init__()
        self.title = "It's getting dark."

        self.actions["a"] = HotelShelterAction()
        self.actions["b"] = B()
        self.actions["c"] = TempleShelterAction()
        self.actions["d"] = D()



class B(Action):
    def __init__(self):
        super().__init__()
        self.content = ("Get a cheap room in the Adventurers' Inn.")
        self.button = "Pay 8 coins."
        self.image = Image.open("world/img/shelters/inn.jpg")

    def execute(self, player, world):
        if player.money >= 8:
            player.money -= 8
            world.message = f"You paid 8 coins."
            world.message = ("  \r :green-background[You slept well.]")
            energy_boost = random.randint(45, 60)
            player.personality["Energy"] += energy_boost
            player.personality["Energy"] = min(100, player.personality["Energy"])
            world.message += f"  \r You gain back :green-background[{energy_boost} Energy]."
            super().execute(player, world)
        else:
            world.message = (":red-background[*You don't have enough money.*]")




class D(Action):
    def __init__(self):
        super().__init__()
        self.content = ("Sleep on the streets.")
        self.button = "Select."
        self.image = Image.open("world/img/shelters/homeless.jpg")

    def execute(self, player, world):
        degeneracy_bonus = random.randint(2, 6)
        world.message = (f":red-background[You had a rough night (*+{degeneracy_bonus}* Degeneracy).]")
        energy_boost = random.randint(10, 30)
        player.personality["Energy"] += energy_boost
        player.personality["Energy"] = min(100, player.personality["Energy"])
        world.message += f"  \r You gain back :green-background[{energy_boost} Energy]."
        player.personality["Degeneracy"] += degeneracy_bonus
        toss = random.random()
        if "Resilient" in player.traits:
            toss *= 1.8
        if toss < 0.6:
            if "Cold" not in player.traits:
                world.message += "  \r You caught a cold."
                player.traits.append("Cold")
        super().execute(player, world)
