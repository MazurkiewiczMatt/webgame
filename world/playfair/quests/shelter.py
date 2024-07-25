import random
from PIL import Image

from quests import Quest, Action
from .shelters import TempleShelterAction


class NightPlayfairQuest(Quest):
    def __init__(self):
        super().__init__()
        self.title = "It's getting dark."

        self.actions["a"] = A()
        self.actions["b"] = B()
        self.actions["c"] = TempleShelterAction()
        self.actions["d"] = D()


class A(Action):
    def __init__(self):
        super().__init__()
        self.content = ("Starlight hotel offers luxury units for the most affluent of Playfair citizens.")
        self.button = "Pay 60 coins."
        self.image = Image.open("world/img/shelters/hotel.jpg")

    def execute(self, player, world):
        if "Playfair Citizen" in player.traits:
            if player.money >= 60:
                player.money -= 60
                world.message = ("You had an excquisite meal at the restaurant and socialized"
                                 " with other rich of the city.  \r :green-background[You wake up very well rested.]")
                charisma_gain = random.randint(0, 2)
                player.abilities["Charisma"] += charisma_gain
                if charisma_gain > 0:
                    world.message += f"  \r You gain *+{charisma_gain} Charisma*"
                energy_boost = random.randint(60, 70)
                player.personality["Energy"] += energy_boost
                player.personality["Energy"] = min(100, player.personality["Energy"])
                world.message += f"  \r You gain back :green-background[{energy_boost} Energy]."
                super().execute(player, world)
            else:
                world.message = (":red-background[*You don't have enough money.*]")
        else:
            world.message = (":red-background[*You aren't a Playfair Citizen.*]")


class B(Action):
    def __init__(self):
        super().__init__()
        self.content = ("Get a cheap room in the Adventurers' Inn.")
        self.button = "Pay 8 coins."
        self.image = Image.open("world/img/shelters/inn.jpg")

    def execute(self, player, world):
        if player.money >= 8:
            player.money -= 8
            world.message = (":green-background[You slept well.]")
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
