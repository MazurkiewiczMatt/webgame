import random
from PIL import Image

from quests import Quest, Action


class RaceSelectionQuest(Quest):
    def __init__(self):
        super().__init__()
        self.title = "Create new character / Select ancestry"

        self.actions["eaglefolk"] = EaglefolkSelection()
        self.actions["bearfolk"] = BoarfolkSelection()
        self.actions["lionfolk"] = LionfolkSelection()
        self.actions["oxfolk"] = OxfolkSelection()
        self.actions["foreigner"] = ForeignerSelection()


class EaglefolkSelection(Action):
    def __init__(self):
        super().__init__()
        self.content = (
            "**Eaglefolk**. Citizens of Playfair. Industrious and intelligent, they form the middle "
            "class.  \r  \r :bar_chart: **Abilities**:  \r Strength: 20+2d10  \r Wisdom: 20+2d10  \r "
            "Charisma: 20+2d10  \r  \r :chart_with_upwards_trend: **Advantages**:  \r "
            "Playfair citizenship  \r  2d10 coins")
        self.image = Image.open("character/quests/img/eaglefolk.jpg")
        self.button = "Select."

    def execute(self, player, world):
        player.race = "Eaglefolk"
        world.message = ":green-background[You selected eaglefolk as your ethnicity.]"
        player.abilities["Strength"] = 20 + random.randint(1, 10) + random.randint(1, 10)
        player.abilities["Wisdom"] = 20 + random.randint(1, 10) + random.randint(1, 10)
        player.abilities["Charisma"] = 20 + random.randint(1, 10) + random.randint(1, 10)
        world.message += f'  \r Strength: 20+2d10 = {player.abilities["Strength"]}.'
        world.message += f'  \r Wisdom: 20+2d10 = {player.abilities["Wisdom"]}.'
        world.message += f'  \r Charisma: 20+2d10 = {player.abilities["Charisma"]}.'
        player.traits.append("Playfair Citizen")
        player.money += random.randint(1, 10) + random.randint(1, 10)


class BoarfolkSelection(Action):
    def __init__(self):
        super().__init__()
        self.content = (
            "**Boarfolk**. Merchants and craftsmen of Playfair. Eager to earn wages or comission. Impervious to exhaustion "
            "and diesease.  \r  \r :bar_chart: **Abilities**:  \r Strength: 25+2d10  \r Wisdom: 25+2d10  \r "
            "Charisma: 15+2d10  \r  \r :chart_with_upwards_trend: **Advantages**:  \r "
            "Resilient  \r  1d10 coins")
        self.image = Image.open("character/quests/img/boarfolk.jpg")
        self.button = "Select."

    def execute(self, player, world):
        player.race = "Boarfolk"
        world.message = ":green-background[You selected boarfolk as your ethnicity.]"
        player.abilities["Strength"] = 25 + random.randint(1, 10) + random.randint(1, 10)
        player.abilities["Wisdom"] = 25 + random.randint(1, 10) + random.randint(1, 10)
        player.abilities["Charisma"] = 15 + random.randint(1, 10) + random.randint(1, 10)
        world.message += f'  \r Strength: 25+2d10 = {player.abilities["Strength"]}.'
        world.message += f'  \r Wisdom: 25+2d10 = {player.abilities["Wisdom"]}.'
        world.message += f'  \r Charisma: 15+2d10 = {player.abilities["Charisma"]}.'
        player.money += random.randint(1, 10)
        player.traits.append("Resilient")


class LionfolkSelection(Action):
    def __init__(self):
        super().__init__()
        self.content = (
            "**Lionfolk**. Citizens of Playfair. Highly estemeed race of statesmen and philosophers. "
            "It made some of greatest warriors of the realm.  \r  \r :bar_chart: **Abilities**:  \r Strength: 25+2d10  \r Wisdom: 20+2d10  \r "
            "Charisma: 25+2d10  \r  \r :chart_with_upwards_trend: **Advantages**:  \r "
            "Playfair citizenship  \r  1d10 coins")
        self.image = Image.open("character/quests/img/lionfolk.jpg")
        self.button = "Select."

    def execute(self, player, world):
        player.race = "Lionfolk"
        world.message = ":green-background[You selected lionfolk as your ethnicity.]"
        player.abilities["Strength"] = 25 + random.randint(1, 10) + random.randint(1, 10)
        player.abilities["Wisdom"] = 20 + random.randint(1, 10) + random.randint(1, 10)
        player.abilities["Charisma"] = 25 + random.randint(1, 10) + random.randint(1, 10)
        world.message += f'  \r Strength: 25+2d10 = {player.abilities["Strength"]}.'
        world.message += f'  \r Wisdom: 20+2d10 = {player.abilities["Wisdom"]}.'
        world.message += f'  \r Charisma: 25+2d10 = {player.abilities["Charisma"]}.'
        player.traits.append("Playfair Citizen")
        player.money += random.randint(1, 10)


class OxfolkSelection(Action):
    def __init__(self):
        super().__init__()
        self.content = (
            "**Oxfolk**. Workers of Playfair. They struggle, dependent for employment on higher casts."
            "  \r  \r :bar_chart: **Abilities**:  \r Strength: 40+2d10  \r Wisdom: 20+2d10  \r "
            "Charisma: 15+2d10")
        self.image = Image.open("character/quests/img/oxfolk.jpg")
        self.button = "Select."

    def execute(self, player, world):
        player.race = "Oxfolk"
        world.message = ":green-background[You selected oxfolk as your ethnicity.]"
        player.abilities["Strength"] = 40 + random.randint(1, 10) + random.randint(1, 10)
        player.abilities["Wisdom"] = 20 + random.randint(1, 10) + random.randint(1, 10)
        player.abilities["Charisma"] = 15 + random.randint(1, 10) + random.randint(1, 10)
        world.message += f'  \r Strength: 40+2d10 = {player.abilities["Strength"]}.'
        world.message += f'  \r Wisdom: 20+2d10 = {player.abilities["Wisdom"]}.'
        world.message += f'  \r Charisma: 15+2d10 = {player.abilities["Charisma"]}.'


class ForeignerSelection(Action):
    def __init__(self):
        super().__init__()
        self.content = (
            "**Foreigner**. You come from a faraway land, of which no denizen of Playfair ever heard. "
            "\r  \r :bar_chart: **Abilities**:  \r Strength: 20+2d10  \r Wisdom: 25+2d10  \r "
            "Charisma: 20+2d10  \r  \r :chart_with_upwards_trend: **Advantages**:  \r "
            " 20 + 2d10 coins")
        self.image = Image.open("character/quests/img/foreigner.jpg")
        self.button = "Select."

    def execute(self, player, world):
        player.race = "Foreigner"
        world.message = ":green-background[You selected foreign origins.]"
        player.abilities["Strength"] = 20 + random.randint(1, 10) + random.randint(1, 10)
        player.abilities["Wisdom"] = 25 + random.randint(1, 10) + random.randint(1, 10)
        player.abilities["Charisma"] = 20 + random.randint(1, 10) + random.randint(1, 10)
        world.message += f"  \r Strength: 20+2d10 = {player.abilities['Strength']}."
        world.message += f"  \r Wisdom: 25+2d10 = {player.abilities['Wisdom']}."
        world.message += f"  \r Charisma: 20+2d10 = {player.abilities['Charisma']}."
        player.traits.append("Foreigner")
        player.money += 20 + random.randint(1, 10) + random.randint(1, 10)
