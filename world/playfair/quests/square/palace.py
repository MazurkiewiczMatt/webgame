from PIL import Image

from quests import Quest, Action
from .exit import ExitSquareBuilding


class PalaceAction(Action):
    def __init__(self):
        super().__init__()
        self.content = ("At Patrician's Palace, denizens of Playfair may apply for citizenship "
                        "and professional licenses.")
        self.button = "Ask for admission."
        self.image = Image.open("world/img/companies/palace.jpg")

    def execute(self, player, world):
        player.tags.append("in-quest")
        player.tags.append("q:playfair_palace")


class PatriciansPalace(Quest):
    def __init__(self, player):
        super().__init__()
        self.title = "Playfair Square / Patrician's Palace"
        self.content = ("At the entrance, a pair of massive wooden doors, embellished with golden accents and "
                        "intricate designs, open into a spacious foyer. The walls of the foyer are lined with "
                        "portraits of past Patricians, each framed in gold and showcasing their regal bearing. "
                        "  \r   \r The "
                        "main hall is vast and opulent, with a high vaulted ceiling supported by marble pillars. "
                        "Crystal chandeliers hang from above, their lights reflecting off the gold-leafed decorations "
                        "that adorn the ceiling. Rich tapestries depicting historical scenes of Playfair's "
                        "illustrious past cover the walls, adding a sense of grandeur and history to the space.  \r  \r")
        if "Playfair Citizen" not in player.traits:
            self.actions["citizenship"] = BuyCitizenship()
        else:
            self.content += "  \r :green-background[You are a citizen of Playfair.]"
        if "Licensed Physician" not in player.traits:
            self.actions["license"] = MedicalLicense()
        else:
            self.content += "  \r :green-background[You are a licensed physician.]"
        self.actions["exit"] = ExitSquareBuilding()


class BuyCitizenship(Action):
    def __init__(self):
        super().__init__()
        self.content = ("Buy Playfair Citizenship.")
        self.button = "Pay 1000 coins."

    def execute(self, player, world):
        if player.money < 1000:
            world.message = ":red-background[You can't afford to buy a Playfair Citizenship.]"
        else:
            player.money -= 1000
            world.message = ":red-background[You paid :moneybag: 1000 coins.]"
            world.message += "  \r :green-background[You are now a Playfair Citizen!]"
            player.traits.append("Playfair Citizen")

class MedicalLicense(Action):
    def __init__(self):
        super().__init__()
        self.content = ("Apply for :blue-background[a physician's license] (requires Medicine Associate, possible to acquire at Playfair University).")
        self.button = "Pay 200 coins."

    def execute(self, player, world):
        if "Medicine Associate" not in player.traits:
            world.message = (":red-background[You have no formal education in medicine.] "
                             "  \r You must complete an Associate degree in Medicine before applying for a license.")
        else:
            if player.money < 200:
                world.message = ":red-background[You can't afford to apply for the license.]"
            else:
                player.money -= 200
                world.message = ":red-background[You paid :moneybag: 200 coins.]"
                world.message += "  \r :green-background[You obtained the physician's license and can now practice as a doctor!]"
                player.traits.append("Licensed Physician")

