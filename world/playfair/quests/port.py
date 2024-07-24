from quests import Quest, Action
from items import ITEMS_DATABASE
from PIL import Image
from .square import ExitSquareBuilding

class PortQuest(Quest):
    def __init__(self):
        super().__init__()
        self.title = "Playfair Port."
        self.content = "Playfair Port processes wares of ships sailing to and from ports all around the region."
        self.actions["aie"] = AIEAction()


class AIEAction(Action):
    def __init__(self):
        super().__init__()
        self.content = "Trading floor of the Aero Import-Export company."
        self.button = "Enter."
        self.image = Image.open("world/img/places/tradingfloor.jpg")

    def execute(self, player, world):
        player.tags.append("in-quest")
        player.tags.append("q:aietrade")

class AIEQuest(Quest):
    def __init__(self, prices, player):
        super().__init__()
        self.title = "Playfair Port / Aero Import-Export."
        self.content = ("Here you can invest in resources with hope of selling them at a higher price later.")
        for res in prices:
            self.actions[f"buy_{res}"] = BuyResource(player, res, prices[res])
            self.actions[f"sell_{res}"] = SellResource(player, res, prices[res])
        self.actions["exit"] = ExitSquareBuilding()


class BuyResource(Action):
    def __init__(self, player, resource_name, resource_value):
        super().__init__()
        self.item = ITEMS_DATABASE[resource_name]()
        if self.item.image_path is not None:
            self.image = Image.open(self.item.image_path)
            self.image_size = 0.3
        count = player.inventory.count(resource_name)
        self.content = f"Buy {self.item.name} for {resource_value} a piece. You currently have {count}."
        self.button = "Buy one."
        self.resource_name = resource_name
        self.resource_value = resource_value
    def execute(self, player, world):
        if player.money > self.resource_value:
            player.money -= self.resource_value
            player.inventory.append(self.resource_name)
            world.message = f":green-background[You bought {self.item.name} for {self.resource_value} coins.]"
        else:
            world.message = f":red-background[You can't afford to buy {self.item.name} for {self.resource_value} coins.]"

class SellResource(Action):
    def __init__(self, player, resource_name, resource_value):
        super().__init__()
        self.item = ITEMS_DATABASE[resource_name]()
        if self.item.image_path is not None:
            self.image = Image.open(self.item.image_path)
            self.image_size = 0.3
        count = player.inventory.count(resource_name)
        self.content = f"Sell {self.item.name} for {resource_value} a piece. You currently have {count}."
        self.button = "Sell one."
        self.resource_name = resource_name
        self.resource_value = resource_value
    def execute(self, player, world):
        if self.resource_name in player.inventory:
            player.money += self.resource_value
            player.inventory.remove(self.resource_name)
            world.message = f":green-background[You sold {self.item.name} for {self.resource_value} coins.]"
        else:
            world.message = f":red-background[You don't have {self.item.name} to sell.]"
