
import json

from world import World
from character import Character

def create_json_data(character, world):
    data = {
        "character": character.to_dict(),
        "world": world.to_dict(),
    }
    return json.dumps(data, indent=4)

def load_from_json(json_data):
    data = json.loads(json_data)
    character = Character.from_dict(data["character"])
    world = World.from_dict(data["world"])
    return character, world