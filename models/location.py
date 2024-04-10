import random

from autonomous import log
from models.encounter import Encounter
from models.item import Item
from models.ttrpgobject import TTRPGObject

from .character import Character


class Location(TTRPGObject):
    _no_copy = TTRPGObject._no_copy + [
        "owner",
        "_characters",
        "_items",
        "_encounters",
    ]

    attributes = TTRPGObject.attributes | {
        "owner": None,
        "location_type": "",
        "_characters": [],
        "_items": [],
        "_encounters": [],
    }

    categories = [
        "forest",
        "swamp",
        "mountain",
        "lair",
        "stronghold",
        "tower",
        "palace",
        "temple",
        "fortress",
        "cave",
        "ruins",
        "shop",
        "tavern",
        "sewer",
        "graveyard",
        "shrine",
        "library",
        "academy",
        "workshop",
        "arena",
        "market",
    ]

    _funcobj = {
        "name": "generate_location",
        "description": "builds a Location model object",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "An intriguing and unique name",
                },
                "location_type": {
                    "type": "string",
                    "description": "The type of location",
                },
                "backstory": {
                    "type": "string",
                    "description": "A short description of the history of the location",
                },
                "desc": {
                    "type": "string",
                    "description": "A short physical description that will be used to generate an image of the inside of the location ",
                },
                "notes": {
                    "type": "array",
                    "description": "3 short descriptions of potential side quests involving the location",
                    "items": {"type": "string"},
                },
            },
        },
    }

    ################### Dunder Methods #####################

    def __init__(self, *args, **kwargs):
        attributes = ["characters", "items", "encounters"]
        for attr in attributes:
            if value := kwargs.get(attr):
                setattr(self, f"_{attr}", value)

        super().__init__(*args, **kwargs)

    ################### Property Methods #####################

    @property
    def children(self):
        return [*self.characters, *self.items, *self.encounters]

    @property
    def encounters(self):
        sorted(self._encounters, key=lambda obj: obj.name)
        return self._encounters

    @encounters.setter
    def encounters(self, value):
        self._encounters = value

    @property
    def creatures(self):
        results = [c for e in self._encounters for c in e.creatures]
        sorted(results, key=lambda obj: obj.name)
        return results

    @property
    def characters(self):
        sorted(self._characters, key=lambda obj: obj.name)
        return self._characters

    @characters.setter
    def characters(self, value):
        self._characters = value

    @property
    def end_date_str(self):
        return f"Destroyed: {super().end_date_str}" if super().end_date_str else ""

    @property
    def start_date_str(self):
        return f"Built: {super().start_date_str}"

    @property
    def items(self):
        sorted(self._items, key=lambda obj: obj.name)
        return self._items

    @items.setter
    def items(self, value):
        for idx, item in enumerate(value):
            if isinstance(item, str):
                value[idx] = Item.generate(self, item)
                value[idx].save()
            elif not isinstance(item, Item):
                raise ValueError(
                    f"Item {item} is not a valid Item object or string description"
                )
        self._items = value

    ################### Crud Methods #####################

    def generate(self):
        prompt = f"Generate a {self.genre} TTRPG {self.location_type or random.choice(self.categories)} location with a backstory containing {random.choice(('a surprising', 'a long hidden', 'a mysterious', 'a sinister'))} history for players to slowly unravel."
        if self.owner:
            prompt += f" The location is owned by {self.owner.name}. {self.owner.backstory_summary}"
        results = super().generate(prompt=prompt)

        return results

    def add_characters(self, owner=False, description=None):
        character = Character.build(self.world, parent=self, description=description)
        self.characters.append(character)
        if owner:
            self.owner = character
        self.save()
        return character

    def add_encounters(self, num_players=5, level=5, description=None):
        enc = Encounter.build(world=self.world, parent=self, description=description)
        self.encounters.append(enc)
        self.save()
        return enc

    def add_items(self, description=None):
        item = Item.build(world=self.world, parent=self, description=description)
        self.items.append(item)
        self.save()
        return item

    def remove_characters(self, obj):
        return super().remove(obj, self.characters)

    def remove_encounters(self, obj):
        return super().remove(obj, self.encounters)

    def remove_items(self, obj):
        return super().remove(obj, self.items)

    ################### Instance Methods #####################
    def has_children(self, value):
        value = value.lower()
        return value if value in["character", "encounter", "item"] else None

    def get_image_prompt(self):
        return f"A full color hi-res image of a point of interest or landmark in a {self.genre} TTRPG with the following description: {self.desc}"

    def page_data(self):
        return {
            "pk": self.pk,
            "name": self.name,
            "owner": self.owner.name if self.owner else "Unknown",
            "desc": self.desc,
            "backstory": self.backstory,
            "character_inhabitants": [f"{r.pk}" for r in self.characters],
        }

    @property
    def state_data(self):
        obj_data = super().state_data
        obj_data["geneology"]["children"] = {
            "Character": [o.pk for o in self.characters],
            "Item": [o.pk for o in self.items],
            "Encounter": [o.pk for o in self.encounters],
        }
        obj_data["attributes"].update(
            {
                "location_type": self.location_type,
                "owner": self.owner.state_data if self.owner else {},
            }
        )
        return obj_data
