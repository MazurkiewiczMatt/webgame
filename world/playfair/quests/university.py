from PIL import Image
import random

from quests import Quest, Action
from .square import ExitSquareBuilding


class UniversityQuest(Quest):
    def __init__(self, player):
        super().__init__()
        self.title = "Playfair Square / Playfair University"
        self.content = "Playfair University's innovative approach prepares graduates for diverse careers, merging the future's technology with the enchantment of the mystical. PU is where the extraordinary meets the practical, fostering a dynamic learning environment for all."
        self.content += "  \r"
        if "PU_charisma_class" not in player.tags:
            self.actions["charisma"] = EtiquetteCourse()
        else:
            self.content += "  \r :blue-background[You are enrolled in an etiquette class.]"
        if "PU_intelligence_class" not in player.tags:
            self.actions["intelligence"] = LogicCourse()
        else:
            self.content += "  \r  :blue-background[You are enrolled in a logic class.]"
        self.actions["exit"] = ExitSquareBuilding()

class EtiquetteCourse(Action):
    def __init__(self):
        super().__init__()
        self.content = ("A **one-week** course with classes every **morning**. Teaches basics of etiquette and diplomacy,"
                        " increasing Charisma of the participant by anywhere between 7 and 21. "
                        "  \r :moneybag: :blue-background[Cost 50 for Playfair Citizens, 100 for non-citizens]")
        self.button = "Enroll."
        self.image = Image.open("world/img/actions/charisma_class.jpg")
        self.image_size = 0.4

    def execute(self, player, world):
        if "Playfair Citizen" in player.traits:
            fee = 50
        else:
            fee = 100
        if player.money > fee:
            player.money -= fee
            player.tags.append("PU_charisma_class")
            player.tags.append("PU_charisma_class_0")
            world.message = f":green-background[You paid {fee} to enroll in etiquette class at Playfair University.]"

class LogicCourse(Action):
    def __init__(self):
        super().__init__()
        self.content = ("A **two-weeks** course with classes every **afternoon**. Develops Wisdom of the participant, "
                        " with increases in range 14-28."
                        "  \r :moneybag: :blue-background[Cost 100 for Playfair Citizens, 200 for non-citizens]")
        self.button = "Enroll."
        self.image = Image.open("world/img/actions/intelligence_course.png")
        self.image_size = 0.4

    def execute(self, player, world):
        if "Playfair Citizen" in player.traits:
            fee = 100
        else:
            fee = 200
        if player.money > fee:
            player.money -= fee
            player.tags.append("PU_intelligence_class")
            player.tags.append("PU_intelligence_class_0")
            world.message = f":green-background[You paid {fee} to enroll in logic class at Playfair University.]"


class StudentQuest(Quest):
    def __init__(self, player, time_of_day):
        super().__init__()
        self.title = "Studies at Playfair University."
        if "PU_charisma_class" in player.tags:
            self.content += "  \r :blue-background[You are enrolled in an etiquette class.]"
            if time_of_day == "Morning":
                self.actions["charisma"] = EtiquetteClass(player)
            else:
                self.content += " Come back in the morning to participate."

        if "PU_intelligence_class" in player.tags:
            self.content += "  \r  :blue-background[You are enrolled in a logic class.]"
            if time_of_day == "Afternoon":
                self.actions["intelligence"] = LogicClass(player)
            else:
                self.content += " Come back in the afternoon to participate."


class EtiquetteClass(Action):
    def __init__(self, player):
        super().__init__()
        self.current_day = 0
        for tag in player.tags:
            if "PU_charisma_class_" == tag[:18]:
                self.tag = tag
                self.current_day = int(tag[18:]) + 1
        self.content = f"Etiquette class. Day {self.current_day} out of 7."
        self.button = "Study."

    def execute(self, player, world):
        charisma_gain = random.randint(2, 4)
        player.abilities["Charisma"] += charisma_gain
        world.message = f"You studied at Playfair University and :green-background[gained {charisma_gain} Charisma points]."

        player.tags.remove(self.tag)
        if self.current_day < 7:
            player.tags.append(self.tag[:18] + str(self.current_day))
        else:
            player.tags.remove("PU_charisma_class")
            world.message += "  \r This was the final day of the course."

        exhaustion_gain = random.randint(10, 25)
        player.personality["Energy"] -= exhaustion_gain
        world.message += f"  \r  Your energy decreased by {exhaustion_gain}."

        super().execute(player, world)


class LogicClass(Action):
    def __init__(self, player):
        super().__init__()
        self.current_day = 0
        for tag in player.tags:
            if "PU_intelligence_class_" == tag[:22]:
                self.tag = tag
                self.current_day = int(tag[22:]) + 1
        self.content = f"Logic class. Day {self.current_day} out of 14."
        self.button = "Study."

    def execute(self, player, world):
        wisdom_gain = random.randint(1, 2)
        player.abilities["Wisdom"] += wisdom_gain
        world.message = f"You studied at Playfair University and :green-background[gained {wisdom_gain} Wisdom points]."

        player.tags.remove(self.tag)
        if self.current_day < 14:
            player.tags.append(self.tag[:22] + str(self.current_day))
        else:
            player.tags.remove("PU_intelligence_class")
            world.message += "  \r This was the final day of the course."
        exhaustion_gain = random.randint(10, 25)
        player.personality["Energy"] -= exhaustion_gain
        world.message += f"  \r  Your energy decreased by {exhaustion_gain}."
        super().execute(player, world)
