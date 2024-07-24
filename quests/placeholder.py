from .quest import Quest
from .action import Action

import random


class PlaceholderQuest(Quest):
    def __init__(self):
        super().__init__()

        class PassTimeAction(Action):
            def __init__(self):
                super().__init__()
                self.content = "There's really nothing interesting to do."
                self.button = "Pass time."

            def execute(self, player, world):
                dedication_penalty = random.randint(0, 3)
                world.message = f":blue-background[You wander aimlessly, lost in your thoughts (*-{dedication_penalty}* Dedication).]"
                player.personality["Dedication"] -= dedication_penalty
                super().execute(player, world)

        self.actions["pass-time"] = PassTimeAction()