import random

from autonomous import log
from autonomous.model.autoattribute import AutoAttribute
from models.ttrpgobject import TTRPGObject

from .character import Character


class Faction(TTRPGObject):
    _no_copy = TTRPGObject._no_copy + [
        "_leader",
        "_characters",
    ]

    attributes = TTRPGObject.attributes | {
        "goal": AutoAttribute("TEXT", default=""),
        "status": AutoAttribute("TEXT", default=""),
        "_leader": None,
        "_characters": [],
    }

    _personality = {
        "social": [
            "secretive",
            "agressive",
            "courageous",
            "cowardly",
            "quirky",
            "imaginative",
            "reckless",
            "cautious",
            "suspicious",
            "friendly",
            "unfriendly",
        ],
        "political": [
            "practical",
            "violent",
            "cautious",
            "sinister",
            "anarchic",
            "religous",
            "patriotic",
            "nationalistic",
            "xenophobic",
            "racist",
            "egalitarian",
        ],
        "economic": [
            "disruptive",
            "ambitious",
            "corrupt",
            "charitable",
            "greedy",
            "generous",
        ],
    }

    _funcobj = {
        "name": "generate_faction",
        "description": "completes Faction data object",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "An evocative and unique name",
                },
                "desc": {
                    "type": "string",
                    "description": "A brief description of the members of the faction",
                },
                "backstory": {
                    "type": "string",
                    "description": "The faction's backstory",
                },
                "goal": {
                    "type": "string",
                    "description": "The faction's goal",
                },
                "status": {
                    "type": "string",
                    "description": "The faction's current status",
                },
                "notes": {
                    "type": "array",
                    "description": "3 short descriptions of potential side quests involving the faction",
                    "items": {"type": "string"},
                },
            },
        },
    }
    ################### Dunder Methods #####################

    def __init__(self, *args, **kwargs):
        if value := kwargs.get("characters"):
            self.items = value

        super().__init__(*args, **kwargs)

    ################### Instance Properties #####################

    @property
    def children(self):
        return self.characters

    @property
    def characters(self):
        for v in self._characters:
            if v not in self.associations:
                self.associations.append(v)
                self.save()
        return self.associations

    @characters.setter
    def characters(self, value):
        for v in value:
            if v not in self.associations:
                self.associations.append(v)
                self.save()

    @property
    def end_date_str(self):
        return f"Disbanded: {super().end_date_str}" if super().end_date_str else ""

    @property
    def start_date_str(self):
        return f"Founded: {super().start_date_str}"

    @property
    def leader(self):
        return self._leader

    @leader.setter
    def leader(self, value):
        if isinstance(value, str):
            value = Character.get(value)
        if not isinstance(value, Character):
            raise ValueError(f"Leader must be a Character, not {type(value)}")
        self._leader = value
        self.save()

    @property
    def items(self):
        results = [i for c in self._characters for i in c.items]
        sorted(results, key=lambda obj: obj.name)
        return results

    @property
    def map_prompt(self):
        return f"""A map of the {self.title}'s home base located in the following location:
          - {self.parent.desc if self.parent else "Location Unknown"}
        """

    @property
    def map_type(self):
        return f"battle map for the {self.title}'s home base"

    ################### Crud Methods #####################

    def generate(self):
        traits = self.traits or [
            random.choice(traits) for traits in self._personality.values()
        ]
        prompt = f"Generate a {self.genre} faction using the following traits as a guideline: {', '.join(traits)}. The faction should have a backstory containing a {random.choice(('boring', 'mysterious', 'sinister'))} secret that gives them a goal they are working toward."
        if self.leader:
            prompt += f"""
            The current leader of the faction is:
            - NAME: {self.leader.name}
            - Backstory: {self.leader.backstory_summary}
            """
        results = super().generate(prompt=prompt)
        self.traits = traits
        self.save()
        return results

    def add_characters(self, leader=False, description=None):
        character = Character.build(self.world, parent=self, description=description)
        self.characters.append(character) if character not in self.characters else None
        if leader or not self.leader:
            self.leader = character
        self.save()
        return character

    def remove_characters(self, obj):
        if obj == self.leader:
            self.leader = None
        return super().remove(obj, self.characters)
        raise ValueError(f"Character {obj.pk} not found")

    ################### Instance Methods #####################
    def has_children(self, value):
        value = value.lower()
        return value if value in ["character"] else None

    def get_image_prompt(self):
        return f"A full color logo and portrait a fictional group described as {self.backstory_summary}."

    def page_data(self):
        return {
            "pk": self.pk,
            "name": self.name,
            "desc": self.desc,
            "backstory": self.backstory,
            "goal": self.goal,
            "leader": self.leader.pk if self.leader else "Unknown",
            "status": self.status if self.status else "Unknown",
            "chcaracter_members": [ch.pk for ch in self.characters],
        }

    @property
    def state_data(self):
        obj_data = super().state_data
        obj_data["geneology"]["children"] = {
            "Character": [o.pk for o in self.characters],
        }
        obj_data["attributes"].update(
            {
                "goal": self.goal,
                "status": self.status,
                "leader": self.leader.state_data if self.leader else {},
            }
        )
        return obj_data
