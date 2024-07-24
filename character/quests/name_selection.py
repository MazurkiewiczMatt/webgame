import random

from quests import Quest, Action


class NameSelectionQuest(Quest):
    def __init__(self):
        super().__init__()
        self.title = "Create new character / Select name"

        self.actions["a"] = A()
        self.actions["b"] = B()
        self.actions["c"] = C()
        self.actions["d"] = D()


class NameSelection(Action):
    def __init__(self, name, description):
        super().__init__()
        self.content = (
            f"**{name}**: {description}")
        self.button = "Select."
        self.name = name

    def execute(self, player, world):
        player.name = self.name
        player.tags.remove("in-quest")


class A(NameSelection):
    def __init__(self):
        super().__init__(
            name="Abel",
            description="Meaning *breath*. You are like a leaf carried by the stream of destiny.  \r (+1d6 Wisdom)"
        )

    def execute(self, player, world):
        super().execute(player, world)
        player.abilities["Wisdom"] += random.randint(1, 6)
        world.message = ":green-background[You selected *Abel* as your name.]"

class B(NameSelection):
    def __init__(self):
        super().__init__(
            name="Dorkas",
            description="Named after a species of agile, swift gazelle.  \r (+1d3 Strength, *Fast*)"
        )

    def execute(self, player, world):
        super().execute(player, world)
        player.abilities["Strength"] += random.randint(1, 3)
        player.traits.append("Fast")
        world.message = ":green-background[You selected *Dorkas* as your name.]"

class C(NameSelection):
    def __init__(self):
        super().__init__(
            name="Eleazar",
            description="Seven patrons bestow their care on brave people name such.  \r (+1d6 Strength)"
        )

    def execute(self, player, world):
        super().execute(player, world)
        player.abilities["Strength"] += random.randint(1, 6)
        world.message = ":green-background[You selected *Eleazar* as your name.]"

class D(NameSelection):
    def __init__(self):
        super().__init__(
            name="Hanan",
            description="Name with association of extraordinary grace.  \r (+1d6 Charisma)"
        )

    def execute(self, player, world):
        super().execute(player, world)
        player.abilities["Charisma"] += random.randint(1, 6)
        world.message = ":green-background[You selected *Hanan* as your name.]"
