import random

from autonomous import log
from models.character import Character
from models.creature import Creature
from models.item import Item
from models.ttrpgobject import TTRPGObject

LOOT_MULTIPLIER = 3


class Encounter(TTRPGObject):
    _no_copy = TTRPGObject._no_copy + [
        "_characters",
        "_creatures",
        "_encounters",
        "_items",
    ]

    attributes = TTRPGObject.attributes | {
        "_difficulty": 0,
        "_encounters": [],
        "_creatures": [],
        "_characters": [],
        "_items": [],
        "enemy_type": "creatures",
        "complications": "Additional enemies arrive after round 3",
        "combat_scenario": "",
        "noncombat_scenario": "",
    }
    LOOT_MULTIPLIER = 3

    _difficulty_list = [
        "trivial",
        "easy",
        "medium",
        "hard",
        "deadly",
    ]

    # {item_type} consistent with
    _items_types = [
        "junk item",
        "trinket or bauble",
        "form of currency",
        "valuable item of no utility, such as gems or art",
        "consumable item, such as food or drink",
        "utility item, such as tools or a map",
        "weapon",
        "armor",
        "unique artifact",
    ]

    _funcobj = {
        "name": "generate_encounter",
        "description": "Generate an Encounter object",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The title of the encounter",
                },
                "backstory": {
                    "type": "string",
                    "description": "The backstory of the encounter from the enemy's perspective",
                },
                "desc": {
                    "type": "string",
                    "description": "A physical description that will be used to generate an image of the scene the characters come upon to start the encounter ",
                },
                "enemy_type": {
                    "type": "string",
                    "description": "The type of enemy the characters will encounter",
                },
                "complications": {
                    "type": "string",
                    "description": "Additional environmental effects or delayed events that complicate the encounter, such as a trap or additional enemies that occurs after a certain number of rounds",
                },
                "combat_scenario": {
                    "type": "string",
                    "description": "The event or events that will cause this to be combat encounter",
                },
                "noncombat_scenario": {
                    "type": "string",
                    "description": "The event or events that will cause this to be non-combat encounter",
                },
                "notes": {
                    "type": "array",
                    "description": "3 short descriptions of potential side quests involving the outcome of this encounter",
                    "items": {"type": "string"},
                },
            },
        },
    }

    ################### Dunder Methods #####################
    def __init__(self, *args, **kwargs):
        if value := kwargs.get("items"):
            self.items = value
        if value := kwargs.get("difficulty"):
            self.difficulty = value

        super().__init__(*args, **kwargs)

    ################## Instance Properties ##################
    @property
    def children(self):
        return [*self.creatures, *self.characters, *self.items]

    @property
    def creatures(self):
        self._creatures = sorted(self._creatures, key=lambda x: x.name)
        return self._creatures

    @creatures.setter
    def creatures(self, value):
        self._creatures = value

    @property
    def characters(self):
        self._characters = sorted(self._characters, key=lambda x: x.name)
        return self._characters

    @characters.setter
    def characters(self, value):
        self._characters = value

    @property
    def difficulty(self):
        if not self._difficulty:
            self._difficulty = random.choice(range(len(self._difficulty_list)))
            self.save()
        return self._difficulty_list[self._difficulty]

    @difficulty.setter
    def difficulty(self, value):
        if isinstance(value, str):
            if value not in self._difficulty_list:
                raise ValueError(
                    f"Encounter difficulty must be one of {self._difficulty_list}"
                )
            self._difficulty = self._difficulty_list.index(value)
        elif isinstance(value, int) and 0 <= value < len(self._difficulty_list):
            self._difficulty = value
        else:
            raise TypeError(
                f"Encounter difficulty must be one of {self._difficulty_list}"
            )

    @property
    def encounters(self):
        sorted(self._encounters, key=lambda obj: obj.name)
        return self._encounters

    @encounters.setter
    def encounters(self, value):
        self._encounters = value

    @property
    def enemies(self):
        return [*self.creatures, *self.characters]

    @enemies.setter
    def enemies(self, value):
        for enemy in value:
            if isinstance(enemy, Character):
                self._characters.append(enemy)
            elif isinstance(enemy, Creature):
                self._creatures.append(enemy)
            else:
                raise TypeError(
                    f"Encounter enemies must be a list of Character or Creature objects, not {type(enemy)}"
                )

    @property
    def end_date_str(self):
        return f"Ended: {super().end_date_str}" if super().end_date_str else ""

    @property
    def start_date_str(self):
        return f"Began: {super().start_date_str}"

    @property
    def items(self):
        sorted(self._items, key=lambda x: x.name)
        return self._items

    @items.setter
    def items(self, value):
        if value and isinstance(value, list):
            for item in value:
                if not isinstance(item, Item):
                    raise TypeError(
                        f"Character items must be a list of Item objects, not {type(item)}"
                    )
        self._items = value

    ################## Crud Methods ##################

    def generate(self, num_players=5, level=1):
        enemy_type = self.enemy_type or random.choices(
            ["humanoid", "monster", "animal"]
        )
        prompt = f"""Generate a {self.genre} TTRPG encounter using the following guidelines:
        - A party of {num_players} at level {level}
        - Difficulty: {self.difficulty}
        - Type of enemies: {enemy_type}
        """
        # log(f"{primer}\n===\n{prompt}")
        results = super().generate(prompt=prompt)
        self.save()
        return results

    def add_enemies(self, enemy_type="creature", description=None):
        model = Character if enemy_type == "character" else Creature
        enemy = model.build(world=self.world, parent=self, description=description)
        self.enemies.append(enemy)
        self.save()
        return enemy

    def add_items(self, description=None):
        item = Item.build(world=self.world, parent=self, description=description)
        self.items.append(item)
        self.save()
        return item

    def remove_items(self, obj):
        return super().remove(obj, self.items)

    def remove_enemies(self, obj):
        for enemy in self.enemies:
            if enemy.pk == obj.pk:
                container = (
                    self.characters if isinstance(enemy, Character) else self.creatures
                )
                return super().remove(enemy, container)
        raise ValueError(f"Enemy {obj.pk} not found")

    ################## Instance Methods ##################
    def has_children(self, value):
        value = value.lower()
        return value if value in ["character", "item", "creature"] else None

    def get_image_prompt(self):
        enemies = [
            f"- {e.name} ({e.title}) : {self.backstory_summary}" for e in self.enemies
        ]
        enemies_str = {"\n".join(enemies)}
        return f"""
        A full color illustrated image of the following group preparing for battle:
        {enemies_str}
        """

    def page_data(self):
        return {
            "pk": self.pk,
            "name": self.name,
            "desc": self.desc,
            "backstory": self.backstory,
            "difficulty": [self.difficulty],
            "enemies": [r.pk for r in self.enemies],
            "items": [r.pk for r in self.items],
        }

    @property
    def state_data(self):
        obj_data = super().state_data
        obj_data["geneology"]["children"] = {
            "Character": [o.pk for o in self.characters],
            "Creature": [o.pk for o in self.creatures],
            "Item": [o.pk for o in self.items],
        }
        obj_data["attributes"].update(
            {
                "difficulty": self.difficulty,
                "enemy_type": self.enemy_type,
            }
        )
        return obj_data
