import random

from autonomous import log
from models.ttrpgobject import TTRPGObject


class Item(TTRPGObject):
    attributes = TTRPGObject.attributes | {
        "rarity": "",
        "cost": "",
        "duration": "",
        "weight": "",
        "features": [],
    }

    _funcobj = {
        "name": "generate_item",
        "description": "creates Item data object",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "An descriptive, but unique name",
                },
                "desc": {
                    "type": "string",
                    "description": "A brief physical description that will be used to generate an image of the item",
                },
                "backstory": {
                    "type": "string",
                    "description": "The history of the item",
                },
                "features": {
                    "type": "array",
                    "description": "A list of stats and special features of the item, if any.",
                    "items": {"type": "string"},
                },
                "weight": {
                    "type": "string",
                    "description": "The weight of the item",
                },
                "rarity": {
                    "type": "string",
                    "description": "How rare is the item from one of the following: [common, uncommon, rare, very rare, legendary, artifact]",
                },
                "cost": {
                    "type": "string",
                    "description": "How much does the item cost in local currency",
                },
                "duration": {
                    "type": "string",
                    "description": "How long will the item last before it breaks or is used up",
                },
                "notes": {
                    "type": "array",
                    "description": "2 short descriptions of potential side quests involving the item",
                    "items": {"type": "string"},
                },
            },
        },
    }

    ################### Dunder Methods #####################

    ################### Crud Methods #####################
    def generate(self):
        prompt = f"Generate a {self.genre} loot item for a {self.genre} TTRPG with detailed stats and a backstory containing {random.choices(('a common', 'a long hidden', 'a mysterious', 'a sinister and dangerous'), (10, 5, 2, 1))} origin. There is a 20% chance the item has a secret special feature or ability."
        for i in ["rarity", "cost", "duration", "weight", "features"]:
            if getattr(self, i):
                prompt += f"""
        {i}: {getattr(self, i)}
        """
        results = super().generate(
            prompt=prompt,
        )

        return results

    ################### Property Methods #####################

    @property
    def end_date_str(self):
        return f"Lost: {super().end_date_str}" if super().end_date_str else ""

    @property
    def start_date_str(self):
        return f"Created: {super().start_date_str}"

    @property
    def map_prompt(self):
        return f"""A unique treasure map for a {self.title} with the following description:
        - {self.desc}
        """

    @property
    def map_type(self):
        return f"{self.title} treasure map"

    ################### Instance Methods #####################
    def has_children(self, value):
        return False

    def get_image_prompt(self):
        return f"A full color image of an item called a {self.name} on display"

    def page_data(self):
        return {
            "pk": self.pk,
            "rarity": self.rarity if self.rarity else "Unknown",
            "cost": self.cost if self.cost else "Unknown",
            "duration": self.duration if self.duration else "Unknown",
            "weight": self.weight if self.weight else "Unknown",
            "features": self.features,
        }

    @property
    def state_data(self):
        obj_data = super().state_data
        obj_data["attributes"].update(
            {
                "rarity": self.rarity,
                "cost": self.cost,
                "duration": self.duration,
                "weight": self.weight,
                "features": self.features,
            }
        )
        return obj_data
