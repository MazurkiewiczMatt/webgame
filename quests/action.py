class Action:
    def __init__(self):
        self.content = ""
        self.button = ""
        self.image = None

    def execute(self, player, world):
        world.update()
        player.update(world)
