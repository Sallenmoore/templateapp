import random

import requests

from autonomous import log
from models.item import Item
from models.ttrpgobject import TTRPGObject


class Creature(TTRPGObject):
    _no_copy = TTRPGObject._no_copy + ["_items"]

    attributes = TTRPGObject.attributes | {
        "type": "",
        "size": "",
        "goal": "",
        "abilities": [],
        "_items": [],
        "hitpoints": 0,
        "strength": 0,
        "dexterity": 0,
        "constitution": 0,
        "wisdom": 0,
        "intelligence": 0,
        "charisma": 0,
    }
    _funcobj = {
        "name": "generate_creature",
        "description": "completes Creature data object",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "A descriptive and evocative name",
                },
                "type": {
                    "type": "string",
                    "description": "The type of creature",
                },
                "traits": {
                    "type": "array",
                    "description": "The unique features of the creature, if any",
                    "items": {"type": "string"},
                },
                "size": {
                    "type": "string",
                    "description": "huge, large, medium, small, or tiny",
                },
                "desc": {
                    "type": "string",
                    "description": "A physical description that will be used to generate an image of the creature",
                },
                "backstory": {
                    "type": "string",
                    "description": "The creature's backstory",
                },
                "goal": {
                    "type": "string",
                    "description": "The creature's goal",
                },
                "hitpoints": {
                    "type": "integer",
                    "description": "Creature's hit points",
                },
                "abilities": {
                    "type": "array",
                    "description": "The creature's abilities in combat",
                    "items": {"type": "string"},
                },
                "strength": {
                    "type": "integer",
                    "description": "The amount of Strength the creature has from 1-20",
                },
                "dexterity": {
                    "type": "integer",
                    "description": "The amount of Dexterity the creature has from 1-20",
                },
                "constitution": {
                    "type": "integer",
                    "description": "The amount of Constitution the creature has from 1-20",
                },
                "intelligence": {
                    "type": "integer",
                    "description": "The amount of Intelligence the creature has from 1-20",
                },
                "wisdom": {
                    "type": "integer",
                    "description": "The amount of Wisdom the creature has from 1-20",
                },
                "charisma": {
                    "type": "integer",
                    "description": "The amount of Charisma the creature has from 1-20",
                },
                "notes": {
                    "type": "array",
                    "description": "2 short descriptions of potential side quests involving the creature",
                    "items": {"type": "string"},
                },
            },
        },
    }

    ################### Dunder Methods #####################

    def __init__(self, *args, **kwargs):
        if value := kwargs.get("items"):
            self.items = value

        super().__init__(*args, **kwargs)

    ################### Property Methods #####################
    @property
    def children(self):
        return self.items

    @property
    def items(self):
        sorted(self._items, key=lambda x: x.name)
        return self._items

    @property
    def end_date_str(self):
        return f"Died: {super().end_date_str}" if super().end_date_str else ""

    @property
    def start_date_str(self):
        return f"Born: {super().start_date_str}"

    @items.setter
    def items(self, value):
        for idx, item in enumerate(value):
            if isinstance(item, str):
                value[idx] = Item.generate(self, item)
                value[idx].save()
            elif not isinstance(item, Item):
                raise TypeError(
                    f"Item {item} is not a valid Item object or string description"
                )
        self._items = value

    @property
    def map_prompt(self):
        return f"""A map of the {self.title}'s lair located in the following location:
        - {self.parent.desc if self.parent else "Location Unknown"}
        """

    @property
    def map_type(self):
        return f"Battlemap for the lair of a {self.type} named {self.name} with the following goal: {self.goal}"

    ################### CRUD Methods #####################
    def generate(self):
        prompt = f"""Create an interesting {self.genre} creature that has a {random.choice(('boring', 'mysterious', 'sinister'))} goal they are working toward.
        """
        obj = super().generate(prompt=prompt)
        return obj

    def add_items(self, description=None):
        item = Item.build(self.world, parent=self, description=description)
        self.items.append(item)
        self.save()
        return item

    def remove_items(self, obj):
        return super().remove(obj, self.items)

    ################### Instance Methods #####################
    def has_children(self, value):
        value = value.lower()
        return value if value in ["item"] else None

    def get_image_prompt(self):
        return f"""A full-length color portrait of a fictional {self.world.genre}  creature with the following description:
        - NAME: {self.name}
        - DESCRIPTION: {self.desc}
        """

    def page_data(self):
        return {
            "pk": self.pk,
            "name": self.name,
            "desc": self.description,
            "backstory": self.backstory,
            "goal": self.goal,
            "type": self.type,
            "size": self.size,
            "hit points": self.hitpoints,
            "attributes": {
                "strength": self.strength,
                "dexerity": self.dexterity,
                "constitution": self.constitution,
                "wisdom": self.wisdom,
                "intelligence": self.intelligence,
                "charisma": self.charisma,
            },
            "abilities": self.abilities,
            "items": [r.pk for r in self.items],
        }

        @property
        def state_data(self):
            obj_data = super().state_data
            obj_data["geneology"]["children"] = {
                "Item": [o.pk for o in self.items],
            }
            obj_data["attributes"].update(
                {
                    "goal": self.goal,
                    "type": self.type,
                    "size": self.size,
                    "hit points": self.hitpoints,
                    "strength": self.strength,
                    "dexerity": self.dexterity,
                    "constitution": self.constitution,
                    "wisdom": self.wisdom,
                    "intelligence": self.intelligence,
                    "charisma": self.charisma,
                    "abilities": self.abilities,
                }
            )
            return obj_data
