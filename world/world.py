import random

from PIL import Image

from utils import dict_to_display_string
from quests import PlaceholderQuest
from .playfair.quests import NightPlayfairQuest, PlayfairSquare, ShopQuest, TempleQuest
from .playfair.playfair_jobs import JobBoard, generate_corpo_job, InterviewQuest, EmploymentQuest
from .playfair.quests.villainry import CounterfeitDocumentsQuest, FistfightQuest


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
            "quarry": ("Playfair Quarry", "Manual worker", 6, None, "Ask for a job."),
            "corpo1": (generate_corpo_job()),
            "corpo2": (generate_corpo_job()),
            "corpo3": (generate_corpo_job()),
            "corpo4": (generate_corpo_job()),
        }

        self.playfair_store = []
        self.replenish_store()

        self.missions = []

    def replenish_store(self):
        self.playfair_store = [random.choices(["beer", "energy_drink", "nootropic"], weights=[0.5, 0.25, 0.25])[0] for _ in range(6)]


    def update(self, character):
        self.replenish_store()
        self.generate_missions(character)
        if self.state["Time of day"] == "Night":
            self.state["Time of day"] = "Morning"
            self.state["Day"] += 1
        elif self.state["Time of day"] == "Morning":
            self.state["Time of day"] = "Afternoon"
        elif self.state["Time of day"] == "Afternoon":
            self.state["Time of day"] = "Night"

        for c in ["corpo1", "corpo2", "corpo3", "corpo4"]:
            toss = random.random()
            if toss < 0.1:
                self.playfair_jobs[c] = generate_corpo_job()

    def display(self):
        return dict_to_display_string(self.state)

    def generate_missions(self, character):
        missions = []
        if self.state["Location"] == "The City of Playfair":
            toss = random.randint(1, 100)
            if toss < character.personality["Degeneracy"]//2 - 15:
                possible_villain_missions = []

                if "Playfair Citizen" not in character.traits:
                    possible_villain_missions.append(CounterfeitDocumentsQuest())

                possible_villain_missions.append(FistfightQuest())

                if len(possible_villain_missions)>0:
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
            return []

        quests = [] + self.missions

        if self.state["Location"] == "The City of Playfair":
            if self.state["Time of day"] == "Night":
                quests.append(NightPlayfairQuest())
            else:
                if "employed" in character.tags and character.job is not None:
                    quests.append(EmploymentQuest(character, self.state["Day"]))
                quests.append(PlayfairSquare(self.state))
                quests.append(JobBoard(self.playfair_jobs))
                quests.append(PlaceholderQuest())



        if len(quests) == 0 and "no-quests" in character.tags:
            quests.append(PlaceholderQuest())

        return quests

    def to_dict(self):
        return {
            "state": self.state,
            "tags": self.tags,
            "message": self.message,
            "image_path": self.image_path,
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
        if world.image_path is not None:
            world.image = Image.open(world.image_path)
        else:
            world.image = None
        return world


