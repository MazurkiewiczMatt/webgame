import random
from PIL import Image

from quests import Quest, Action


class CounterfeitDocumentsQuest(Quest):
    def __init__(self):
        super().__init__()
        self.title = "You are approached by a shady salesman."
        self.content = " :smiling_imp: 'I will sell you a set of Playfair documents,' he promises. 'For just 20 coins you can become a full citizen.'"
        self.actions["agree"] = BuyDocumentsAction()
        self.actions["report"] = ReportAction("CounterfeitDocumentsQuest")
        self.actions["avoid"] = RefuseAction("CounterfeitDocumentsQuest")


class BuyDocumentsAction(Action):
    def __init__(self):
        super().__init__()
        self.content = "Agree to buy the documents."
        self.button = "Pay 20 coins."
        self.image = Image.open("world/img/actions/shady_agreement.jpg")
        self.image_size = 0.4

    def execute(self, player, world):
        if player.money >= 20:
            player.money -= 20
            toss = random.random()
            if toss < 0.5:
                player.traits.append("Playfair Citizen")
                player.tags.append("illegal-documents")
                world.message = ":green-background[You obtained legitimate-looking documents, and hence **Playfair Citizen** trait.]"
            else:
                world.message = ":red-background[These are obvious forgeries. You were swindled and bought nothing of value.]"
            degeneracy_gain = random.randint(5, 10)
            player.personality["Degeneracy"] += degeneracy_gain
            world.message += f'  \r  Your Degeneracy increased by {degeneracy_gain}.'
            for mission in world.missions:
                if mission.__class__.__name__ == "CounterfeitDocumentsQuest":
                    world.missions.remove(mission)
        else:
            world.message = ":red-background[You can't afford to buy the documents.]"


class RefuseAction(Action):
    def __init__(self, quest_name):
        super().__init__()
        self.content = "Do not pay any attention."
        self.button = "Walk away."
        self.image_size = 0.4
        self.quest_name = quest_name

    def execute(self, player, world):
        for mission in world.missions:
            if mission.__class__.__name__ == self.quest_name:
                world.missions.remove(mission)


class ReportAction(Action):
    def __init__(self, quest_name):
        super().__init__()
        self.content = "Report it to authorities."
        self.button = "Report."
        self.image = Image.open("world/img/actions/guards.jpg")
        self.image_size = 0.4
        self.quest_name = quest_name

    def execute(self, player, world):
        world.message = ":green-background[You reported the event to the authorities.]"
        degeneracy_gain = random.randint(2, 8)
        player.personality["Degeneracy"] -= degeneracy_gain
        world.message += f'  \r  Your Degeneracy decreased by {degeneracy_gain}.'
        for mission in world.missions:
            if mission.__class__.__name__ == self.quest_name:
                world.missions.remove(mission)


class FistfightQuest(Quest):
    def __init__(self):
        super().__init__()
        self.title = "You witness a fistfight."
        self.content = (
            "There are around ten people engaged in fist fighting. There is one badly wounded man on the ground, and "
            " you think you see a shiv flashing in hand of one of the bandits.")

        self.actions["agree"] = FightAction()
        self.actions["report"] = ReportAction("FistfightQuest")
        self.actions["avoid"] = RefuseAction("FistfightQuest")


class FightAction(Action):
    def __init__(self):
        super().__init__()
        self.content = "Show them who is the strongest."
        self.button = "Join fight."
        self.image = Image.open("world/img/actions/fistfight.png")
        self.image_size = 0.4

    def execute(self, player, world):
        toss = random.randint(1, 100)
        if toss < player.abilities["Strength"]:
            world.message = f":green-background[You pass the test ({toss}/{player.abilities['Strength']})] and emerge victorious from the battle."
            bonus = random.randint(1, 5)
            player.abilities["Strength"] += bonus
            world.message += f"  \r Your Strength increases by {bonus}."
        else:
            world.message = f":red-background[You fail the test ({toss}/{player.abilities['Strength']})] and get beaten up pretty hardly."
        degeneracy_gain = random.randint(2, 6)
        player.personality["Degeneracy"] += degeneracy_gain
        world.message += f'  \r  Your Degeneracy increased by {degeneracy_gain}.'
        for mission in world.missions:
            if mission.__class__.__name__ == "FistfightQuest":
                world.missions.remove(mission)



class PickpocketQuest(Quest):
    def __init__(self):
        super().__init__()
        self.title = "You witness pickpocketing."
        self.content = (
            "You catch a glimpse of a shady type stealthily reaching into the coat of some passing aristocrat"
            " and stealing his wallet. You confront the thief, and he offers to share 10 coins for your silence.")
        self.actions["agree"] = AcceptBribeAction()
        self.actions["report"] = ReportAction("PickpocketQuest")
        self.actions["avoid"] = RefuseAction("PickpocketQuest")


class AcceptBribeAction(Action):
    def __init__(self):
        super().__init__()
        self.content = "You agree to the terms."
        self.button = "Take the money."
        self.image = Image.open("world/img/actions/shady_agreement.jpg")
        self.image_size = 0.4

    def execute(self, player, world):
        degeneracy_gain = random.randint(2, 6)
        player.personality["Degeneracy"] += degeneracy_gain
        world.message = f'You accept the bribe.  \r  Your Degeneracy increased by {degeneracy_gain}.'
        player.money += 10
        world.message += f'  \r  :green-background[Your gained 10 coins].'
        for mission in world.missions:
            if mission.__class__.__name__ == "PickpocketQuest":
                world.missions.remove(mission)
