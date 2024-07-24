import random

from utils import dict_to_display_string
from .traits import get_trait_description
from .quests import RaceSelectionQuest, NameSelectionQuest

class Character:
    def __init__(self):
        self.name = None
        self.race = None
        self.tags = ["in-quest"]
        self.traits = []
        self.notes = {}
        self.abilities = {
            "Strength": 0,
            "Wisdom": 0,
            "Charisma": 0,
        }
        self.personality = {
            "Dedication": 50,
            "Faith": 50,
            "Degeneracy": 50,
        }
        self.inventory = []
        self.money = 0
        self.job = None


    def update(self, world):
        for ability in self.abilities:
            self.abilities[ability] = min(130, max(0, self.abilities[ability]))
        if "Cold" in self.traits:
            toss = random.random()
            if "Resilient" in self.traits:
                toss * 0.98
            if toss < 0.15:
                self.traits.remove("Cold")
                world.message += "  \r You are no longer suffering from cold."
            elif toss > 0.93:
                self.abilities["Strength"] -= 1
                world.message += "  \r You become weaker due to cold (*-1 Strength*)"
        if "negotiated_today" in self.tags:
            if world.state["Time of day"] == "Night":
                self.tags.remove("negotiated_today")

    def generate_quests(self, world):
        quests = []

        if self.race is None:
            quests.append(RaceSelectionQuest())
            return quests

        if self.name is None:
            quests.append(NameSelectionQuest())
            return quests

        if len(quests) == 0:
            self.tags.append("no-quests")
        elif "no-quests" in self.tags:
            self.tags.remove("no-quests")

        return quests

    def display(self):
        result = ""

        if self.name is not None:
            result += f"Name: {self.name}  \r"
        else:
            result += f"New arrival.  \r"

        if self.race is not None:
            result += f"Ethnicity: {self.race}  \r"
        result += "  \r"
        result += f"Coins: {self.money} | **Inventory**:  \r"
        if len(self.inventory) > 0:
            for item in self.inventory:
                result += f"{item}  \r"
        else:
            if self.money < 10:
                result += f"You have nothing to your name."
            else:
                result += f"You travel with no items."
        return result

    def display2(self):
        result = ""
        result += "**Abilities**:  \r"
        result += dict_to_display_string(self.abilities)
        return result

    def display3(self):
        result = ""
        result += "**Personality**:  \r"
        for trait, degree in self.personality.items():
            degree = min(100, max(degree, 0))
            result += f"{trait}: {get_trait_description(degree, trait)} ({degree})  \r"
        return result

    def display_notes(self):
        return dict_to_display_string(self.notes)

    def to_dict(self):
        return {
            "name": self.name,
            "race": self.race,
            "tags": self.tags,
            "notes": self.notes,
            "traits": self.traits,
            "abilities": self.abilities,
            "personality": self.personality,
            "inventory": self.inventory,
            "money": self.money,
            "job": self.job,
        }

    @classmethod
    def from_dict(cls, data):
        char = cls()
        char.name = data.get("name")
        char.race = data.get("race")
        char.tags = data.get("tags", [])
        char.notes = data.get("notes", {})
        char.traits = data.get("traits", [])
        char.abilities = data.get("abilities", {
            "Strength": 20,
            "Wisdom": 20,
            "Charisma": 20,
        })
        char.personality = data.get("personality", {
            "Dedication": 50,
            "Faith": 50,
            "Degeneracy": 50,
        })
        char.inventory = data.get("inventory", [])
        char.money = data.get("money", 0)
        char.job = data.get("job", None)
        return char


