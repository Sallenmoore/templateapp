import random

from autonomous import log
from autonomous.ai import AutoTeam
from autonomous.model.autoattribute import AutoAttribute
from models.item import Item
from models.ttrpgobject import TTRPGObject


class Character(TTRPGObject):
    _no_copy = TTRPGObject._no_copy + ["chats", "_items"]

    attributes = TTRPGObject.attributes | {
        "is_player": False,
        "gender": "",
        "occupation": "",
        "_lineage": {},
        "_abilities": [],
        "goal": AutoAttribute("TEXT", default=""),
        "race": "",
        "hitpoints": 0,
        "strength": 0,
        "dexterity": 0,
        "constitution": 0,
        "wisdom": 0,
        "intelligence": 0,
        "charisma": 0,
        "wealth": [],
        "_items": [],
        "chats": {
            "history": [],
            "summary": "The beginning of a conversation between a TTRPG PC and NPC.",
            "message": "",
            "response": "",
        },
    }

    _genders = ["male", "female", "non-binary"]

    _personality = {
        "social": [
            "shy",
            "outgoing",
            "friendly",
            "unfriendly",
            "mean",
            "snooty",
            "aggressive",
            "flexible",
            "kind",
            "proud",
            "humble",
            "confident",
            "insecure",
            "silly",
            "serious",
            "tolerant",
            "intolerant",
        ],
        "political": [
            "smart",
            "sneaky",
            "dumb",
            "loyal",
            "disloyal",
            "dishonest",
            "honest",
            "stubborn",
            "optimistic",
            "pessimistic",
            "sensitive",
            "insensitive",
            "intuitive",
            "intelligent",
            "wise",
            "foolish",
            "patient",
            "impatient",
            "forgiving",
            "unforgiving",
        ],
        "professional": [
            "greedy",
            "generous",
            "lazy",
            "hardworking",
            "courageous",
            "cowardly",
            "creative",
            "imaginative",
            "practical",
            "logical",
            "curious",
            "nosy",
            "adventurous",
            "cautious",
            "careful",
            "reckless",
            "careless",
        ],
    }

    _funcobj = {
        "name": "generate_npc",
        "description": "completes NPC data object",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "A unique first, middle, and last name",
                },
                "age": {
                    "type": "integer",
                    "description": "The character's age",
                },
                "gender": {
                    "type": "string",
                    "description": "The character's preferred gender",
                },
                "race": {
                    "type": "string",
                    "description": "The character's race",
                },
                "traits": {
                    "type": "array",
                    "description": "The character's personality traits",
                    "items": {"type": "string"},
                },
                "desc": {
                    "type": "string",
                    "description": "A physical description that will be used to generate an image of the character",
                },
                "backstory": {
                    "type": "string",
                    "description": "The character's backstory that includes an unusual secret the character must protect",
                },
                "goal": {
                    "type": "string",
                    "description": "The character's goal",
                },
                "occupation": {
                    "type": "string",
                    "description": "The character's daily occupation",
                },
                "strength": {
                    "type": "integer",
                    "description": "The amount of Strength the character has from 1-20",
                },
                "dexterity": {
                    "type": "integer",
                    "description": "The amount of Dexterity the character has from 1-20",
                },
                "constitution": {
                    "type": "integer",
                    "description": "The amount of Constitution the character has from 1-20",
                },
                "intelligence": {
                    "type": "integer",
                    "description": "The amount of Intelligence the character has from 1-20",
                },
                "wisdom": {
                    "type": "integer",
                    "description": "The amount of Wisdom the character has from 1-20",
                },
                "charisma": {
                    "type": "integer",
                    "description": "The amount of Charisma the character has from 1-20",
                },
                "notes": {
                    "type": "array",
                    "description": "3 short descriptions of potential side quests involving the character",
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

    ################# Class Methods #################

    def generate(self):
        age = self.age if self.age else random.randint(15, 45)
        gender = self.gender or random.choices(self._genders, weights=[4, 5, 1], k=1)[0]

        prompt = f"As an expert AI in creating NPCs for a {self.genre} TTRPG, generate a {gender} NPC aged {age} years who is {random.choice(self._personality['social'])} and {random.choice(self._personality['political'])}, but also {random.choice(self._personality['professional'])}. Write a detailed backstory that incorporates the character's goals and expands on their current backstory with either an mysterious, awesome, OR sinister secret to protect."

        obj = super().generate(prompt=prompt)
        self.hitpoints = random.randint(5, 300)
        self.age = age
        self.gender = gender
        self.save()
        return obj

    ################# Instance Properities #################
    @property
    def ac(self):
        result = (self.dexterity - 10) // 2 + (self.strength - 10) // 2 + 10
        return max(10, result)

    @property
    def abilities(self):
        # if isinstance(self._abilities, list):
        #     self._abilities = {
        #         f"Ability #{idx}": a for idx, a in enumerate(self._abilities)
        #     }
        return self._abilities

    @abilities.setter
    def abilities(self, value):
        # if isinstance(value, list):
        #     self._abilities = {f"Ability #{idx}": a for idx, a in enumerate(value)}
        # else:
        self._abilities = value

    @property
    def children(self):
        return self.items

    @property
    def child_key(self):
        return "players" if self.is_player else "characters"

    @property
    def chat_summary(self):
        return self.chats["summary"]

    @property
    def end_date_str(self):
        return f"Died: {super().end_date_str}" if super().end_date_str else ""

    @property
    def start_date_str(self):
        return f"Born: {super().start_date_str}"

    @property
    def items(self):
        sorted(self._items, key=lambda x: x.name)
        return self._items

    @items.setter
    def items(self, value):
        # log(value)
        for idx, item in enumerate(value):
            if isinstance(item, str):
                value[idx] = Item.generate(self, item)
                value[idx].save()
            elif not isinstance(item, Item):
                raise TypeError(
                    f"Item {item} is not a valid Item object or string description"
                )
        # log(value)
        self._items = value

    @property
    def lineage(self):
        return self._lineage

    @lineage.setter
    def lineage(self, value):
        if not isinstance(value, dict):
            raise TypeError(
                f"Item {value} mist be a dict with the following format: {{<relationship>:[<objects>]}}"
            )
        # log(value)
        self._lineage = value

    @property
    def map_prompt(self):
        if self.parent and self.parent != self.world:
            return f"""A map of the {self.title}'s residence described as follows:
        {self.residence}
        """

    @property
    def map_type(self):
        return f"Indoor playable battlemap for a {self.title}'s residence"

    @property
    def parent(self):
        return super().parent

    @parent.setter
    def parent(self, obj):
        if issubclass(obj.__class__, TTRPGObject) or obj is None:
            self._parent_obj = obj
            if obj.__class__.__name__ == "World":
                self.is_player = True
            else:
                self.is_player = False
        else:
            raise TypeError(
                f"Parent must be a TTRPGObject, not {obj.__class__.__name__}"
            )

    @property
    def residence(self):
        res_description = ""
        if self.parent and self.parent != self.world:
            res_description += f"""
            - Title: {self.parent.title}
            - Description: {self.parent.desc}
            - Map: {self.parent.map_type}
            """
        else:
            res_description += f"""
            An appropriate residence for the following {self.title}:
            - Backstory: {self.backstory_summary}
            - Age: {self.age}
            - Occupation: {self.occupation}
            - Race: {self.race}
            - Physical Description: {self.desc}
            - Gender: {self.gender}
            """
        return res_description

    ################# Instance Methods - CRUD #################
    def add_items(self, description=None):
        item = Item.build(self.world, parent=self, description=description)
        self.items.append(item)
        self.save()
        return item

    def remove_items(self, obj):
        return super().remove(obj, self.items)

    ################# Instance Methods #################
    def has_children(self, value):
        value = value.lower()
        return value if value in ["item"] else None

    def chat(self, message=""):
        # summarize conversation
        if self.chats["message"] and self.chats["response"]:
            primer = f"""As an expert AI in {self.world.genre} TTRPG Worldbuilding, use the previous chat CONTEXT as a starting point to generate a readable summary from the PLAYER MESSAGE and NPC RESPONSE that clarifies the main points of the conversation. Avoid unnecessary details.
            """
            text = f"""
            CONTEXT:\n{self.chats["summary"]}
            PLAYER MESSAGE:\n{self.chats['message']}
            NPC RESPONSE:\n{self.chats['response']}"
            """

            self.chats["summary"] = AutoTeam().summarize_text(text, primer=primer)

        message = message.strip() or "Tell me a little more about yourself..."
        primer = f"You are playing the role of a {self.world.genre} TTRPG NPC talking to a PC."
        prompt = "As an NPC matching the following description:"
        prompt += f"""
            PERSONALITY: {", ".join(self.traits)}

            DESCRIPTION: {self.desc}

            BACKSTORY: {self.backstory_summary}

            GOAL: {self.goal}

        Respond to the PLAYER MESSAGE as the above described character. Use the following chat CONTEXT as a starting point:

        CONTEXT: {self.chats["summary"]}

        PLAYER MESSAGE: {message}
        """

        response = AutoTeam().generate_text(prompt, primer)
        self.chats["history"].append((message, response))
        self.chats["message"] = message
        self.chats["response"] = response
        self.save()

        return self.chats

    def clear_chat(self):
        self.chats["history"] = []
        self.save()

    def get_image_prompt(self):
        if not self.age:
            self.age = random.randint(15, 45)
            self.save()
        prompt = f"A full-body color portrait of a fictional {self.gender} {self.race} {self.genre} character aged {self.age}"
        if self.desc:
            prompt += f" and described as: {self.desc}"
        return prompt

    def page_data(self):
        return {
            "pk": self.pk,
            "name": self.name,
            "desc": self.desc,
            "backstory": self.backstory,
            "gender": self.gender,
            "age": self.age,
            "occupation": self.occupation,
            "race": self.race,
            "DOB": self.start_date if self.start_date else "Unknown",
            "DOD": self.end_date if self.end_date else "Unknown",
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
            "wealth": [w for w in self.wealth],
            "items": [r.pk for r in self.items],
        }

    def state_data(self):
        obj_data = super().state_data
        obj_data["geneology"]["children"] = {"Item": [o.pk for o in self.items]}
        obj_data["attributes"].update(
            {
                "gender": self.gender,
                "occupation": self.occupation,
                "race": self.race,
                "hitpoints": self.hitpoints,
                "strength": self.strength,
                "dexerity": self.dexterity,
                "constitution": self.constitution,
                "wisdom": self.wisdom,
                "intelligence": self.intelligence,
                "charisma": self.charisma,
                "abilities": self.abilities,
                "wealth": self.wealth,
            }
        )
        obj_data["chats"] = self.chats
        return obj_data
