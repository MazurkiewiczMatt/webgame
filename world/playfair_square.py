from quests import Quest, Action


class PlayfairSquare(Quest):
    def __init__(self, city_state):
        super().__init__()
        self.title = "Playfair Square."
        if city_state["Time of day"] == "Morning":
            self.content = ("As the sun rises, Playfair Square awakens with the gentle glow of morning light "
                            "filtering through the leaves of ancient oak trees. The sound of commerce blends with the "
                            "hum of early risers chatting over steaming cups of coffee at outdoor cafés.")
        elif city_state["Time of day"] == "Afternoon":
            self.content = ("By afternoon, Playfair Square is alive with energy and color, bathed in the warm, "
                            "golden hues of the sun. A gentle breeze rustles the leaves, and the fountain at the "
                            "center of the square sparkles in the sunlight.")
        self.content += ("\r  \r The Playfair Square boasts a :blue-background[shop (open only in the mornings)] and "
                         "a :blue-background[temple (open through day, and offering"
                         " cheap shelter at night)].")
        if city_state["Time of day"] == "Morning":
            self.actions["shop"] = ShopAction()
        else:
            self.content += "  \r The shop is now :red-background[closed]."
        self.actions["temple"] = TempleAction()



class ShopAction(Action):
    def __init__(self):
        super().__init__()
        self.content = ("The General Emporium is a charming, rustic shop offering a curated selection of any item "
                        "either a passing adventurer or Playfair denizen may need.")
        self.button = "Shop."
    def execute(self, player, world):
        pass

class TempleAction(Action):
    def __init__(self):
        super().__init__()
        self.content = "Temple with curios."
    def execute(self, player, world):
        pass
