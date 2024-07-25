from PIL import Image
import random

from quests import Action, Quest


class TempleShelterAction(Action):
    def __init__(self):
        super().__init__()
        self.content = ("Sleep in the praying room at the temple.")
        self.button = "Pay 2 coins."
        self.image = Image.open("world/img/shelters/church.jpg")

    def execute(self, player, world):
        if player.personality["Faith"] < 20:
            world.message = "You are far too godless to be let into the temple."
        elif player.personality["Faith"] < 40:
            world.message = "You too godless to be let to the common sleeping area. Return during daytime to repent."
        else:
            if player.money >= 2:
                player.money -= 2
                toss = random.randint(1, 100)
                if toss < 30:
                    possible_quests = []
                    if "temple-mysteriouswhisper" not in player.tags:
                        possible_quests.append("q:temple-mysteriouswhisper")
                    if "temple-strangedreams" not in player.tags:
                        possible_quests.append("q:temple-strangedreams")
                    if len(possible_quests) > 0:
                        quest = random.choice(possible_quests)
                        player.tags.append("in-quest")
                        player.tags.append(quest)
                        world.message = "Something happened..."
                        return None
                world.message = (":blue-background[You spend the night listening to prayers.]")
                energy_boost = random.randint(25, 50)
                player.personality["Energy"] += energy_boost
                player.personality["Energy"] = min(100, player.personality["Energy"])
                world.message += f"  \r You gain back :green-background[{energy_boost} Energy]."
                toss = random.random()
                if toss < 0.5:
                    faith_bonus = random.randint(1, 4)
                    degeneracy_penalty = random.randint(0, 1)
                    player.personality["Faith"] += faith_bonus
                    player.personality["Degeneracy"] -= degeneracy_penalty
                    world.message += f"  \r You feel your faith growing (*+{faith_bonus}* Faith"
                    if degeneracy_penalty > 0:
                        world.message += f", *-{degeneracy_penalty}* Degeneracy"
                    world.message += ")."
                elif toss < 0.8:
                    if "Cold" not in player.traits:
                        world.message += "  \r You caught a cold."
                        player.traits.append("Cold")
                super().execute(player, world)
            else:
                world.message = (":red-background[*You don't have enough money.*]")

class MysteriousWhisperQuest(Quest):
    def __init__(self):
        super().__init__()
        self.title = "Temple / Mysterious Whisper."
        self.tag = "q:temple-mysteriouswhisper"
        self.content = ("As you drift off to sleep, you hear a soft whisper calling your name. You look around and see "
                        "a hooded figure standing in the shadows. The figure motions for you to come closer.")
        self.actions["shout"] = ShoutMWQAction()
        self.actions["approach"] = ApproachMWQAction()
        self.actions["ignore"] = IgnoreMWQAction()

class ShoutMWQAction(Action):
    def __init__(self):
        super().__init__()
        self.content = "You decide to shout and alert others."
        self.button = "Shout."

    def execute(self, player, world):
        world.message = "The figure vanishes, and others in the room wake up. "
        toss = random.randint(1,3)
        world.message += f"  \r :red-background[You lose {toss} Charisma.]"
        player.abilities["Charisma"] -= toss
        world.message += ("  \r :blue-background[You fall back asleep, exhausted.]")
        energy_boost = random.randint(25, 50)
        player.personality["Energy"] += energy_boost
        player.personality["Energy"] = min(100, player.personality["Energy"])
        world.message += f"  \r You gain back :green-background[{energy_boost} Energy]"
        player.tags.remove("q:temple-mysteriouswhisper")
        player.tags.append("temple-mysteriouswhisper")
        player.tags.remove("in-quest")
        super().execute(player, world)

class ApproachMWQAction(Action):
    def __init__(self):
        super().__init__()
        self.content = "You decide to approach the hooded figure."
        self.button = "Approach."

    def execute(self, player, world):
        world.message = "The figure hands you a mysterious key. "
        player.inventory.append("temple-key")
        world.message += f"  \r :green-background[Gained item: Mysterious key]"
        world.message += ("  \r :blue-background[You fall back asleep, exhausted.]")
        energy_boost = random.randint(25, 50)
        player.personality["Energy"] += energy_boost
        player.personality["Energy"] = min(100, player.personality["Energy"])
        world.message += f"  \r You gain back :green-background[{energy_boost} Energy]"
        player.tags.remove("q:temple-mysteriouswhisper")
        player.tags.append("temple-mysteriouswhisper")
        player.tags.remove("in-quest")
        super().execute(player, world)
        player.notes["Mysterious key"] = "Ask priestess in the temple about the key gifted to you by the hooded figure at night."

class IgnoreMWQAction(Action):
    def __init__(self):
        super().__init__()
        self.content = "You ignore the figure and go back to sleep."
        self.button = "Ignore."

    def execute(self, player, world):
        world.message = "You go back to sleep and have a restful night. "
        energy_boost = random.randint(25, 50)
        player.personality["Energy"] += energy_boost
        player.personality["Energy"] = min(100, player.personality["Energy"])
        world.message += f"  \r You gain back :green-background[{energy_boost} Energy]"
        player.tags.remove("q:temple-mysteriouswhisper")
        player.tags.append("temple-mysteriouswhisper")
        player.tags.remove("in-quest")
        super().execute(player, world)

class StrangeDreamsQuest(Quest):
    def __init__(self):
        super().__init__()
        self.title = "Temple / Strange Dreams."
        self.tag = "q:temple-strangedreams"
        self.content = ("You have a strange and vivid dream about an ancient ritual. When you wake up, in middle of the night, you feel like you learned something important.")
        self.actions["record"] = RecordSDQAction()
        self.actions["ignore"] = IgnoreSDQAction()
        self.actions["discuss"] = DiscussSDQAction()

class RecordSDQAction(Action):
    def __init__(self):
        super().__init__()
        self.content = "You decide to record the details of the dream."
        self.button = "Record."

    def execute(self, player, world):
        world.message = "You write down the details and later realize they contain valuable knowledge. "
        player.abilities["Wisdom"] += 1
        world.message += f"  \r :green-background[You gain 1 Wisdom.]"
        world.message += ("  \r :blue-background[You fall back asleep, after some time.]")
        energy_boost = random.randint(15, 30)
        player.personality["Energy"] += energy_boost
        player.personality["Energy"] = min(100, player.personality["Energy"])
        world.message += f"  \r You gain back :green-background[{energy_boost} Energy]"
        player.tags.remove("q:temple-strangedreams")
        player.tags.append("temple-strangedreams")
        player.tags.remove("in-quest")
        super().execute(player, world)

class IgnoreSDQAction(Action):
    def __init__(self):
        super().__init__()
        self.content = "You ignore the dream and go back to sleep."
        self.button = "Ignore."

    def execute(self, player, world):
        world.message = "You feel a bit unsettled but go back to sleep. "
        player.abilities["Wisdom"] -= 1
        world.message += f"  \r :red-background[You lose 1 Wisdom.]"
        world.message += ("  \r :blue-background[You fall back asleep, exhausted.]")
        energy_boost = random.randint(25, 50)
        player.personality["Energy"] += energy_boost
        player.personality["Energy"] = min(100, player.personality["Energy"])
        world.message += f"  \r You gain back :green-background[{energy_boost} Energy]"
        player.tags.remove("q:temple-strangedreams")
        player.tags.append("temple-strangedreams")
        player.tags.remove("in-quest")
        super().execute(player, world)

class DiscussSDQAction(Action):
    def __init__(self):
        super().__init__()
        self.content = "You discuss the dream with others in the room."
        self.button = "Discuss."

    def execute(self, player, world):
        world.message = "Others find the dream fascinating and offer their insights. "
        player.abilities["Wisdom"] += 1
        player.abilities["Charisma"] += 1
        world.message += f"  \r :green-background[You gain 1 Wisdom.]"
        world.message += f"  \r :green-background[You gain 1 Charisma.]"
        energy_boost = random.randint(25, 50)
        player.personality["Energy"] += energy_boost
        player.personality["Energy"] = min(100, player.personality["Energy"])
        world.message += f"  \r You gain back :green-background[{energy_boost} Energy]"
        player.tags.remove("q:temple-strangedreams")
        player.tags.append("temple-strangedreams")
        player.tags.remove("in-quest")
        super().execute(player, world)

