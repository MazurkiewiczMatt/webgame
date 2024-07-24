import random

from PIL import Image

from quests import Quest, Action
from items import ITEMS_DATABASE



class PlayfairSquare(Quest):
    def __init__(self, city_state):
        super().__init__()
        self.title = "Playfair Square."
        if city_state["Time of day"] == "Morning":
            self.content = ("As the sun rises, Playfair Square awakens with the gentle glow of morning light "
                            "filtering through the leaves of ancient oak trees. The sound of commerce blends with the "
                            "hum of early risers chatting over steaming cups of coffee at outdoor cafés.")
        elif city_state["Time of day"] == "Afternoon":
            self.content = ("By afternoon, Playfair Square is alive with energy and color, bathed in the warm, "
                            "golden hues of the sun. A gentle breeze rustles the leaves, and the fountain at the "
                            "center of the square sparkles in the sunlight.")
        self.content += ("\r  \r The Playfair Square boasts a :blue-background[shop (open only in the mornings)] and "
                         "a :blue-background[temple (open through day, and offering"
                         " cheap shelter at night)].")
        if city_state["Time of day"] == "Morning":
            self.actions["shop"] = ShopAction()
        else:
            self.content += "  \r The shop is now :red-background[closed]."
        self.actions["temple"] = TempleAction()



class ShopAction(Action):
    def __init__(self):
        super().__init__()
        self.content = ("The General Emporium is a charming, rustic shop offering a curated selection of any item "
                        "either a passing adventurer or Playfair denizen may need.")
        self.button = "Shop."
        self.image = Image.open("world/img/places/shop.jpg")
    def execute(self, player, world):
        player.tags.append("in-quest")
        player.tags.append("q:playfair_shop")


class TempleAction(Action):
    def __init__(self):
        super().__init__()
        self.content = "A temple dedicated to a goddess of vitality."
        self.button = "Enter."
        self.image = Image.open("world/img/places/temple.jpg")
    def execute(self, player, world):
        if player.personality["Faith"] < 20:
            world.message = ":red-background[You are too faithless to be let into the temple.]"
        else:
            player.tags.append("in-quest")
            player.tags.append("q:playfair_temple")


class ShopQuest(Quest):
    def __init__(self, items):
        super().__init__()
        self.title = "Playfair Square / The General Emporium"
        for i in range(len(items)):
            self.actions[i] = ItemAction(items[i])
        self.actions["exit"] = ExitSquareBuilding()

class TempleQuest(Quest):
    def __init__(self, player):
        super().__init__()
        self.title = "Playfair Square / Temple"
        self.content = ("Constructed from sun-kissed stones, the temple's structure is adorned with intricate carvings "
                        "of intertwining vines and blossoms, symbolizing life and growth. At its heart lies a "
                        "tranquil courtyard, where a crystal-clear spring feeds into a small, sacred pool, "
                        "believed to be blessed by the goddess herself..")
        self.actions["pray"] = PrayAction()
        self.actions["donate"] = DonateAction()
        self.actions["preach"] = PreachAction(player)
        self.actions["renounce"] = RenounceAction()
        self.actions["exit"] = ExitSquareBuilding()

class PrayAction(Action):
    def __init__(self):
        super().__init__()
        self.content = "Join a three-hours-long mass. (Increases Faith)"
        self.button = "Pray."
    def execute(self, player, world):
        faith_bonus = random.randint(1,6)
        player.personality["Faith"] += faith_bonus
        world.message = f":green-background[Your Faith increases by {faith_bonus}.]"
        player.tags.remove("q:playfair_temple")
        player.tags.remove("in-quest")
        super().execute(player, world)

class DonateAction(Action):
    def __init__(self):
        super().__init__()
        self.content = "Be generous towards renovation of a praying area. (Increases Faith)"
        self.button = "Donate 10 coins."
    def execute(self, player, world):
        if player.money > 10:
            player.money -= 10
            faith_bonus = random.randint(1,6)
            player.personality["Faith"] += faith_bonus
            world.message = f"You donate 10 coins and :green-background[your Faith increases by {faith_bonus}.]"
        else:
            world.message = f":red-background[You don't have enough to donate.]"

class PreachAction(Action):
    def __init__(self, player):
        super().__init__()
        odds = (player.personality["Faith"] + player.abilities["Charisma"])//2 - 30
        self.content = f'Start preaching to the crowd.  \r Odds of success: {odds}% ([{player.personality["Faith"]} Faith + {player.abilities["Charisma"]} Charisma]/2 - 30)'
        self.button = "Preach."
        self.odds = odds

    def execute(self, player, world):
        energy_loss = random.randint(2, 10)
        player.personality["Energy"] -= energy_loss
        world.message = f"You spend {energy_loss} Energy preaching in the temple."

        toss = random.randint(1, 100)

        if toss < self.odds:
            faith_gain = random.randint(4, 10)
            player.personality["Faith"] += faith_gain
            money_gain = random.randint(0, 5)
            player.money += money_gain
            world.message += '  \r :green-background[The crowd listens attentively and thanks you for your teaching.]'
            world.message += f'  \r Your faith grows by {faith_gain}.'
            if money_gain > 0:
                world.message += f'  \r You collect :moneybag: {money_gain} coins in donations.'
        else:
            world.message += '  \r :red-background[No one pays much attention to your rambling.]'
        super().execute(player, world)

class RenounceAction(Action):
    def __init__(self):
        super().__init__()
        self.content = "Publicly renounce the goddess. (Decreases Faith)"
        self.button = "Renounce."
    def execute(self, player, world):
        faith_bonus = random.randint(6,14)
        player.personality["Faith"] -= faith_bonus
        world.message = f":red-background[Your Faith decreases by {faith_bonus}.]"
        player.tags.remove("q:playfair_temple")
        player.tags.remove("in-quest")
        super().execute(player, world)

class ExitSquareBuilding(Action):
    def __init__(self):
        super().__init__()
        self.button = "Exit."

    def execute(self, player, world):
        player.tags.remove("in-quest")
        if "q:playfair_shop" in player.tags:
            player.tags.remove("q:playfair_shop")
        if "q:playfair_temple" in player.tags:
            player.tags.remove("q:playfair_temple")


class ItemAction(Action):
    def __init__(self, item_key):
        super().__init__()
        item = ITEMS_DATABASE[item_key]()
        if item.image_path is not None:
            self.image = Image.open(item.image_path)
            self.image_size = 0.3
        self.content = f"**{item.name}**"
        if item.description != "":
            self.content += f": {item.description}"
        self.button = f"Buy for {item.price} coins."
        self.item = item

    def execute(self, player, world):
        if player.money > self.item.price:
            player.money -= self.item.price
            player.inventory.append(self.item.key)
            world.playfair_store.remove(self.item.key)
            world.message = f"You bought {self.item.name} for {self.item.price} coins."
        else:
            world.message = f":red-background[You can't afford to buy {self.item.name} for {self.item.price} coins.]"