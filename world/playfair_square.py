from PIL import Image

from quests import Quest, Action


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
        self.image = Image.open("world/img/places/temple.jpg")
    def execute(self, player, world):
        player.tags.append("in-quest")
        player.tags.append("q:playfair_temple")


class ShopQuest(Quest):
    def __init__(self):
        super().__init__()
        self.title = "Shop"

        class PassTimeAction(Action):
            def __init__(self):
                super().__init__()
                self.content = "Work in progress."
                self.button = "Pass time."

            def execute(self, player, world):
                player.tags.remove("in-quest")
                player.tags.remove("q:playfair_shop")

        self.actions["pass-time"] = PassTimeAction()

class TempleQuest(Quest):
    def __init__(self):
        super().__init__()
        self.title = "Temple"

        class PassTimeAction(Action):
            def __init__(self):
                super().__init__()
                self.content = "Work in progress."
                self.button = "Pass time."

            def execute(self, player, world):
                player.tags.remove("in-quest")
                player.tags.remove("q:playfair_temple")

        self.actions["pass-time"] = PassTimeAction()
