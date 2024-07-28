import random

from PIL import Image

from utils import dict_to_display_string
from quests import PlaceholderQuest
from .playfair.quests import ShelterPlayfairQuest, PlayfairSquare, ShopQuest, TempleQuest, UniversityQuest, \
    StudentQuest, PortQuest, AIEQuest
from .playfair.playfair_jobs import JobBoard, generate_corpo_job, InterviewQuest, EmploymentQuest
from .playfair.quests.shelters.hotel import HotelOfferQuest
from .playfair.quests.shelters.temple import MysteriousWhisperQuest, StrangeDreamsQuest
from .playfair.quests.villainry import CounterfeitDocumentsQuest, FistfightQuest, PickpocketQuest


class World:
    def __init__(self):
        self.state = {
            "Day": 0,
            "Time of day": "Morning",
            "Location": "The City of Playfair",
        }

        self.tags = []

        self.message = ""
        self.image_path = r"world/img/playfair.png"
        self.image = Image.open(self.image_path)

        self.playfair_jobs = {
            "servant": {'Employer': "Patrician's Palace",
                        'Title': "Servant",
                        'Salary': 4,
                        'Wisdom': None,
                        'Strength': None,
                        'Action': "Plead for a job.",
                        'Days_since_raise': 0,
                        'Raise_possible': False},
            "quarry": {'Employer': "Playfair Quarry",
                       'Title': "Manual worker",
                       'Salary': 6,
                       'Wisdom': None,
                       'Strength': 30,
                       'Action': "Ask for a job.",
                       'Days_since_raise': 0,
                       'Raise_possible': True},
            "corpo1": generate_corpo_job(),
            "corpo2": generate_corpo_job(),
        }

        self.playfair_store = []
        self.replenish_store()

        self.missions = []

        self.resource_prices = {
            "steel-ingot": 11,
            "silver-ingot": 60,
            "exotic-fish": 300,
        }

    def replenish_store(self):
        self.playfair_store = [random.choices(["beer", "energy_drink", "nootropic", "hypertrophy-potion"], weights=[0.4, 0.2, 0.2, 0.2])[0] for _
                               in range(8)]

    def update_resource_prices(self):
        for resource in self.resource_prices:
            toss = random.random()
            if toss < 0.5:
                price = self.resource_prices[resource]
                self.resource_prices[resource] += random.randint(0, price // 15) - price // 30
            elif toss < 0.65:
                self.resource_prices[resource] = int(self.resource_prices[resource] * 1.2)
            elif toss < 0.72:
                self.resource_prices[resource] = int(self.resource_prices[resource] * 0.7)
            self.resource_prices[resource] = max(10, self.resource_prices[resource])

    def update(self, character):
        self.update_resource_prices()
        self.replenish_store()
        self.generate_missions(character)
        if self.state["Time of day"] == "Night":
            self.state["Time of day"] = "Morning"
            self.state["Day"] += 1
        elif self.state["Time of day"] == "Morning":
            self.state["Time of day"] = "Afternoon"
        elif self.state["Time of day"] == "Afternoon":
            self.state["Time of day"] = "Night"

        for c in ["corpo1", "corpo2"]:
            toss = random.random()
            if toss < 0.2:
                self.playfair_jobs[c] = generate_corpo_job()

    def display(self):
        return dict_to_display_string(self.state)

    def generate_missions(self, character):
        missions = []
        if self.state["Location"] == "The City of Playfair":
            toss = random.randint(1, 100)
            if toss < character.personality["Degeneracy"] // 2 - 15:
                possible_villain_missions = []

                if "Playfair Citizen" not in character.traits:
                    possible_villain_missions.append(CounterfeitDocumentsQuest())

                possible_villain_missions.append(FistfightQuest())
                possible_villain_missions.append(PickpocketQuest())

                if len(possible_villain_missions) > 0:
                    missions.append(random.choice(possible_villain_missions))
        self.missions = missions

    def generate_quests(self, character):

        if "in-quest" in character.tags:
            for tag in character.tags:
                if tag[:2] == "a:":
                    return [InterviewQuest(self.playfair_jobs[tag[2:]], tag[2:], character)]
            if "q:playfair_shop" in character.tags:
                return [ShopQuest(self.playfair_store)]
            elif "q:playfair_temple" in character.tags:
                return [TempleQuest(character)]
            elif "q:playfair_university" in character.tags:
                return [UniversityQuest(character)]
            elif "q:aietrade" in character.tags:
                return [AIEQuest(self.resource_prices, character)]
            elif "q:temple-mysteriouswhisper" in character.tags:
                return [MysteriousWhisperQuest()]
            elif "q:temple-strangedreams" in character.tags:
                return [StrangeDreamsQuest()]
            elif "q:hotel_offer" in character.tags:
                return [HotelOfferQuest(self.resource_prices)]
            return []

        quests = []

        if self.state["Location"] == "The City of Playfair":
            if self.state["Time of day"] == "Night":
                quests.append(ShelterPlayfairQuest())
            else:
                quests += self.missions
                if "PU_charisma_class" in character.tags or "PU_intelligence_class" in character.tags or (
                        character.degree is not None and character.degree["place"] == "The City of Playfair"):
                    quests.append(StudentQuest(character, self.state["Time of day"]))
                if "employed" in character.tags and character.job is not None:
                    quests.append(EmploymentQuest(character, self.state["Day"]))
                quests.append(PlayfairSquare(self.state))
                quests.append(PortQuest())
                quests.append(JobBoard(self.playfair_jobs))
                quests.append(PlaceholderQuest())

        return quests

    def to_dict(self):
        return {
            "state": self.state,
            "tags": self.tags,
            "message": self.message,
            "image_path": self.image_path,
            "resource_prices": self.resource_prices,
        }

    @classmethod
    def from_dict(cls, data):
        world = cls()
        world.state = data.get("state", {
            "Day": 0,
            "Time of day": "Night",
        })
        world.tags = data.get("tags", [])
        world.message = data.get("message", "")
        world.image_path = data.get("image_path", None)
        world.resource_prices = data.get("resource_prices", {
            "steel-ingot": 11,
            "silver-ingot": 60,
            "exotic-fish": 300,
        })
        if world.image_path is not None:
            world.image = Image.open(world.image_path)
        else:
            world.image = None
        return world
