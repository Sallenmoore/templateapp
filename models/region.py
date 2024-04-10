import random

from autonomous import log
from models.character import Character
from models.city import City
from models.encounter import Encounter
from models.faction import Faction
from models.location import Location
from models.ttrpgobject import TTRPGObject


class Region(TTRPGObject):
    _no_copy = TTRPGObject._no_copy + [
        "_cities",
        "_locations",
        "_factions",
        "_encounters",
    ]

    attributes = TTRPGObject.attributes | {
        "_cities": [],
        "_locations": [],
        "_factions": [],
        "_encounters": [],
    }

    _environments = [
        "coastal",
        "mountainous",
        "desert",
        "forest",
        "jungle",
        "plains",
        "swamp",
        "frozen",
        "underground",
    ]

    _funcobj = {
        "name": "generate_region",
        "description": "creates Region data object",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "A unique and evocative name for the region",
                },
                "desc": {
                    "type": "string",
                    "description": "A brief physical description that will be used to generate an image of the region",
                },
                "backstory": {
                    "type": "string",
                    "description": "A brief history of the region and its people",
                },
                "notes": {
                    "type": "array",
                    "description": "3 short descriptions of potential side quests in the region",
                    "items": {"type": "string"},
                },
            },
        },
    }

    ################### Dunder Methods #####################
    def __init__(self, *args, **kwargs):
        attributes = ["locations", "cities", "encounters", "factions"]
        for attr in attributes:
            if value := kwargs.get(attr):
                setattr(self, f"_{attr}", value)

        super().__init__(*args, **kwargs)

    ################### Property Methods #####################
    @property
    def children(self):
        return [*self.cities, *self.locations, *self.factions, *self.encounters]

    @property
    def characters(self):
        results = {}
        for city in self.cities:
            results |= {o.pk: o for o in city.characters}

        for faction in self.factions:
            results |= {o.pk: o for o in faction.characters}

        for loc in self.locations:
            results |= {o.pk: o for o in loc.characters}
        # log(results)
        results = list(results.values())
        sorted(results, key=lambda obj: obj.name)
        return results

    @property
    def cities(self):
        sorted(self._cities, key=lambda obj: obj.name)
        return self._cities

    @cities.setter
    def cities(self, value):
        # log(f"Setting cities to {value}")
        self._cities = value

    @property
    def creatures(self):
        results = {}
        for city in self.cities:
            results |= {o.pk: o for o in city.creatures}

        for loc in self.locations:
            results |= {o.pk: o for o in loc.creatures}

        for enc in self.encounters:
            results |= {o.pk: o for o in enc.creatures}

        results = list(results.values())
        sorted(results, key=lambda obj: obj.name)
        return results

    @property
    def end_date_str(self):
        return f"Dissolved: {super().end_date_str}" if super().end_date_str else ""

    @property
    def start_date_str(self):
        return f"Established: {super().start_date_str}"

    @property
    def factions(self):
        sorted(self._factions, key=lambda obj: obj.name)
        return self._factions

    @factions.setter
    def factions(self, value):
        for v in value:
            if v.__class__.__name__ != "Faction":
                raise ValueError("Factions must be of type Faction")
        self._factions = value

    @property
    def locations(self):
        sorted(self._locations, key=lambda obj: obj.name)
        return self._locations

    @locations.setter
    def locations(self, value):
        for v in value:
            if v.__class__.__name__ != "Location":
                raise ValueError("Location must be of type Location")
        self._locations = value

    @property
    def encounters(self):
        sorted(self._encounters, key=lambda obj: obj.name)
        return self._encounters

    @encounters.setter
    def encounters(self, value):
        for v in value:
            if v.__class__.__name__ != "Encounter":
                raise ValueError("Encounter must be of type Encounter")
        self._encounters = value

    @property
    def items(self):
        results = {}
        for city in self.cities:
            results |= {o.pk: o for o in city.items}

        for loc in self.locations:
            results |= {o.pk: o for o in loc.items}

        for enc in self.encounters:
            results |= {o.pk: o for o in enc.items}

        for faction in self.factions:
            results |= {o.pk: o for o in faction.items}

        results = list(results.values())
        sorted(results, key=lambda obj: obj.name)
        return results

    @property
    def map_prompt(self):
        prompt = f"""A map of a region described as:
        - {self.desc}
        - {self.backstory_summary}

        With the following landmarks:
        - {self.model_title('City')}: {", ".join([c.name for c in self.cities])}
        - {self.model_title('Location')}: {", ".join([l.name for l in self.locations])}
        """
        return prompt

    @property
    def map_type(self):
        return f"{self.title} map"

    @property
    def map_scale(self):
        return "1 inch = 5 miles"

    ################### Crud Methods #####################
    def generate(self):
        prompt = f"Generate a detailed information for a {self.genre} {self.title}. The {self.title} should contain {random.choice(('a  unique', 'a mysterious', 'a sinister'))} story thread for players to slowly uncover. The story thread should be connected to 1 or more additional elements in the TTRPG world."
        results = super().generate(prompt=prompt)
        return results

    def add_cities(self, description=None):
        city = City.build(world=self.world, parent=self, description=description)
        self.cities.append(city)
        self.save()
        return city

    def add_locations(self, description=None):
        loc = Location.build(world=self.world, parent=self, description=description)
        self.locations.append(loc)
        self.save()
        return loc

    def add_factions(self, description=None):
        fac = Faction.build(world=self.world, parent=self, description=description)
        self.factions.append(fac)
        self.save()
        return fac

    def add_encounters(self, num_players=5, level=5, description=None):
        enc = Encounter.build(world=self.world, parent=self, description=description)
        self.encounters.append(enc)
        self.save()
        return enc

    def remove_locations(self, obj):
        return super().remove(obj, self.locations)

    def remove_factions(self, obj):
        return super().remove(obj, self.factions)

    def remove_cities(self, obj):
        return super().remove(obj, self.cities)

    def remove_encounters(self, obj):
        return super().remove(obj, self.encounters)

    ################### Instance Methods #####################
    def has_children(self, value):
        value = value.lower()
        return value if value in ["faction", "encounter", "location", "city"] else None

    def get_image_prompt(self):
        prompt = f"An aerial pictoral map illustration of the region {self.name} with the following description: {self.desc}."
        if self.cities:
            cities = ",".join([c.name for c in self.cities])
            prompt += f"The region contains the following cities: {cities}."
        return prompt

    def page_data(self):
        return {
            "pk": self.pk,
            "name": self.name,
            "desc": self.desc,
            "backstory": self.backstory,
            "cities": [f"{r.pk}" for r in self.cities],
            "locations": [f"[{r.pk}])" for r in self.locations],
            "factions": [f"[{r.pk}])" for r in self.factions],
        }

    @property
    def state_data(self):
        obj_data = super().state_data
        obj_data["geneology"]["children"] = {
            "Location": [o.pk for o in self.locations],
            "City": [o.pk for o in self.cities],
            "Faction": [o.pk for o in self.factions],
            "Encounter": [o.pk for o in self.encounters],
        }
        return obj_data
