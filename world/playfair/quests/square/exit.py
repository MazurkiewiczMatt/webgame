from quests import Action


class ExitSquareBuilding(Action):
    def __init__(self):
        super().__init__()
        self.button = "Exit."

    def execute(self, player, world):
        player.tags.remove("in-quest")
        if "q:playfair_shop" in player.tags:
            player.tags.remove("q:playfair_shop")
        if "q:playfair_temple" in player.tags:
            player.tags.remove("q:playfair_temple")
        if "q:playfair_university" in player.tags:
            player.tags.remove("q:playfair_university")
        if "q:aietrade" in player.tags:
            player.tags.remove("q:aietrade")
        if "q:playfair_palace" in player.tags:
            player.tags.remove("q:playfair_palace")
