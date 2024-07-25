import random
from PIL import Image
import streamlit as st

from quests import Quest, Action
from items import ITEMS_DATABASE


class HotelShelterAction(Action):
    def __init__(self):
        super().__init__()
        self.content = ("Starlight hotel offers luxury units for the most affluent of Playfair citizens.")
        self.button = "Pay 60 coins."
        self.image = Image.open("world/img/shelters/hotel.jpg")

    def execute(self, player, world):
        if "Playfair Citizen" in player.traits:
            if player.money >= 60:
                player.money -= 60
                world.message = f"You paid 60 coins for the hotel."
                # random event
                toss = random.randint(1, 100)
                if toss < 25 and "s:shipment" not in player.tags and "s:scam" not in player.tags:
                    player.tags.append("in-quest")
                    player.tags.append("q:hotel_offer")
                    return None
                world.message += ("  \r You had an excquisite meal at the restaurant and socialized"
                                  " with other rich of the city.  \r :green-background[You wake up very well rested.]")
                charisma_gain = random.randint(0, 2)
                player.abilities["Charisma"] += charisma_gain
                if charisma_gain > 0:
                    world.message += f"  \r You gain *+{charisma_gain} Charisma*"
                energy_boost = random.randint(60, 70)
                player.personality["Energy"] += energy_boost
                player.personality["Energy"] = min(100, player.personality["Energy"])
                world.message += f"  \r You gain back :green-background[{energy_boost} Energy]."
                super().execute(player, world)
            else:
                world.message = (":red-background[*You don't have enough money.*]")
        else:
            world.message = (":red-background[*You aren't a Playfair Citizen.*]")


class HotelOfferQuest(Quest):
    def __init__(self, prices):
        super().__init__()
        self.title = "Hotel / Interesting offer"
        self.content = ("A fellow guest you met at the hotel presented you with a very interesting trade. He claims he "
                        "has a shipment in Playfair Port, at Aero Import-Export company, but he has urgent business "
                        "outside of the city he has to attend to. He proposes you buy the stock at discounted price.")

        self.content += f"  \r Does it sound like a good investment or too good to be true?"
        self.actions["agreed"] = YesHotelOfferAction(prices)
        self.actions["deny"] = NoHotelOfferAction()


class YesHotelOfferAction(Action):
    def __init__(self, prices):
        super().__init__()
        resource = random.choice(list(prices.keys()))
        toss = random.randint(1, 100)
        toss2 = random.random()
        number = random.randint(5, 10)
        self.resource = resource
        self.price = prices[self.resource]
        self.number = number
        self.item = ITEMS_DATABASE[self.resource]()
        if toss < 25:
            self.otype = "scam"
            self.proposed_price = int(self.price * self.number * (0.05 + 0.10 * toss2))
        else:
            self.otype = "legit"
            self.proposed_price = int(self.price * self.number * (0.7 + 0.25 * toss2))

        self.content = f"  \r  \r {self.number} of :blue-background[{self.item.name}] for :moneybag: {self.proposed_price} coins  \r The current market unit price of :blue-background[{self.item.name}] is {self.price} coins (:moneybag: {self.price * self.number} coins for {self.number})."
        self.button = f"Agree."
        if "hotel-offer-tmp" not in st.session_state:
            st.session_state["hotel-offer-tmp"] = {}
            st.session_state["hotel-offer-tmp"]["price"] = self.price
            st.session_state["hotel-offer-tmp"]["name"] = self.item.name
            st.session_state["hotel-offer-tmp"]["number"] = self.number
            st.session_state["hotel-offer-tmp"]["proposed_price"] = self.proposed_price
            st.session_state["hotel-offer-tmp"]["resource"] = self.resource
            st.session_state["hotel-offer-tmp"]["otype"] = self.otype

    def execute(self, player, world):
        proposed_price = st.session_state["hotel-offer-tmp"]["proposed_price"]
        number = st.session_state["hotel-offer-tmp"]["number"]
        name = st.session_state["hotel-offer-tmp"]["name"]
        resource = st.session_state["hotel-offer-tmp"]["resource"]
        otype = st.session_state["hotel-offer-tmp"]["otype"]
        if player.money >= proposed_price:
            player.money -= proposed_price
            world.message = f":green-background[You agreed to the deal with another hotel guest].  \r You paid :moneybag: {proposed_price} coins for {number} units of {name}."
            world.message += "  \r Pick it up in AIE in Playfair Port."
            player.tags.remove("in-quest")
            player.tags.remove("q:hotel_offer")
            player.notes["Shipment"] = f"Pick up {number} units of {resource} at AIE in Playfair Port."
            if otype == "legit":
                player.tags.append("s:shipment")
            else:
                player.tags.append("s:scam")
            energy_boost = random.randint(60, 70)
            player.personality["Energy"] += energy_boost
            player.personality["Energy"] = min(100, player.personality["Energy"])
            world.message += f"  \r  \r You go back to sleep and gain :green-background[{energy_boost} Energy]."
            super().execute(player, world)
            del st.session_state["hotel-offer-tmp"]
        else:
            world.message = ":red-background[You can't afford the deal.]"


class NoHotelOfferAction(Action):
    def __init__(self):
        super().__init__()
        self.content = "Refuse the deal."
        self.button = "Refuse."

    def execute(self, player, world):
        world.message = f"You refuse the deal."
        player.tags.remove("in-quest")
        player.tags.remove("q:hotel_offer")
        energy_boost = random.randint(60, 70)
        player.personality["Energy"] += energy_boost
        player.personality["Energy"] = min(100, player.personality["Energy"])
        world.message += f"  \r You go back to sleep and gain :green-background[{energy_boost} Energy]."
        super().execute(player, world)
