import random

from autonomous import log
from models.character import Character
from models.encounter import Encounter
from models.faction import Faction
from models.poi import POI
from models.ttrpgobject import TTRPGObject


class City(TTRPGObject):
    _no_copy = TTRPGObject._no_copy + [
        "_factions",
        "_pois",
        "_encounters",
    ]

    attributes = TTRPGObject.attributes | {
        "_population": 0,
        "_factions": [],
        "_pois": [],
        "_districts": [],
        "_encounters": [],
    }

    personality = {
        "social": [
            "bohemian",
            "decedent",
            "snooty",
            "aggressive",
            "proud",
            "distrustful",
        ],
        "political": [
            "Anarchic",
            "Aristocratic",
            "Authoritarianist",
            "Bureaucratic",
            "Confederationist",
            "Colonialist",
            "Communist",
            "Democratic",
            "Fascist",
            "Kleptocratic",
            "Meritocratic",
            "Militaristic",
            "Monarchic",
            "Theocratic",
            "Totalitarian",
            "Tribalist",
        ],
    }

    _funcobj = {
        "name": "generate_city",
        "description": "completes City data object",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "A unique and evocative name for the city",
                },
                "population": {
                    "type": "integer",
                    "description": "The city's population between 50 and 50000, with more weight on smaller populations",
                },
                "backstory": {
                    "type": "string",
                    "description": "A short history of the city in 750 words or less",
                },
                "desc": {
                    "type": "string",
                    "description": "A short physical description that will be used to generate an image of the city.",
                },
                "districts": {
                    "type": "array",
                    "description": "The names of the districts in the city, if present",
                    "items": {"type": "string"},
                },
                "notes": {
                    "type": "array",
                    "description": "3 short descriptions of potential side quests in the area",
                    "items": {"type": "string"},
                },
            },
        },
    }

    ################### Dunder Methods #####################

    def __init__(self, *args, **kwargs):
        attributes = ["pois", "population", "factions", "districts", "encounters"]
        for attr in attributes:
            if value := kwargs.get(attr):
                setattr(self, f"_{attr}", value)

        super().__init__(*args, **kwargs)

    ################### Class Methods #####################

    def generate(self):
        traits = [random.choice(traits) for traits in self.personality.values()]
        parent_title = self.parent.title if self.parent else self.world.title
        parent_name = self.parent.name if self.parent else self.world.name
        pop_list = list(range(20, 2000000, 22))
        pop_weights = [i + 1 for i in range(len(pop_list), 0, -1)]
        population = self.population or random.choices(pop_list, pop_weights)[0]

        prompt = f"Generate a fictional {self.genre} {self.title} within the {parent_name} {parent_title}. The {self.title} inhabitants are both {' and '.join(traits)}. Write a detailed description appropriate for an establshed settlement with a population of {population}. The settlement may contain up to two mysterious, sinister, or boring secrets hidden within the city for the players to discover."
        obj_data = super().generate(prompt=prompt)
        self.traits = traits
        self.population = population
        self.save()
        return obj_data

    ################### INSTANCE PROPERTIES #####################

    @property
    def children(self):
        return [*self.pois, *self.factions, *self.encounters]

    @property
    def characters(self):
        results = {}
        for faction in self.factions:
            results |= {o.pk: o for o in faction.characters}

        for loc in self.pois:
            results |= {o.pk: o for o in loc.characters}
        result = list(results.values())
        sorted(result, key=lambda obj: obj.name)
        return result

    @property
    def creatures(self):
        results = {}

        for loc in self.pois:
            results |= {o.pk: o for o in loc.creatures}

        for enc in self.encounters:
            results |= {o.pk: o for o in enc.creatures}

        result = list(results.values())
        sorted(result, key=lambda obj: obj.name)
        return result

    @property
    def districts(self):
        districts = []
        for loc in self.pois:
            if loc.district and loc.district not in districts:
                districts.append(loc.district)
        return districts

    @districts.setter
    def districts(self, values):
        if isinstance(values, list):
            self._districts = values
        else:
            raise TypeError(f"Cannot set districts to {values}")

    @property
    def encounters(self):
        sorted(self._encounters, key=lambda obj: obj.name)
        return self._encounters

    @encounters.setter
    def encounters(self, value):
        self._encounters = value

    @property
    def end_date_str(self):
        return f"Abandoned: {super().end_date_str}" if super().end_date_str else ""

    @property
    def start_date_str(self):
        return f"Founded: {super().start_date_str}"

    @property
    def factions(self):
        if isinstance(self._factions, dict):
            self._factions = list(self._factions.values())
        sorted(self._factions, key=lambda obj: obj.name)
        return self._factions

    @factions.setter
    def factions(self, val):
        if isinstance(val, list):
            self._factions = val
        else:
            raise TypeError(f"Cannot set pois to {val}")

    @property
    def items(self):
        results = {}

        for loc in self.pois:
            results |= {o.pk: o for o in loc.items}

        for enc in self.encounters:
            results |= {o.pk: o for o in enc.items}

        for faction in self.factions:
            results |= {o.pk: o for o in faction.items}

        result = list(results.values())
        sorted(result, key=lambda obj: obj.name)
        return result

    @property
    def map_prompt(self):
        prompt = f"""A detailed navigable map of a city with the following landmarks:
          - Districts: {", ".join(self.districts)}
          - Points of Interest:
        """
        for poi in self.pois:
            if poi.name and poi.desc:
                prompt += f"      - {poi.name} located in the {poi.district} district and described as: \n\n{poi.backstory_summary}\n"
        return prompt

    @property
    def pois(self):
        sorted(self._pois, key=lambda obj: obj.name)
        return self._pois

    @pois.setter
    def pois(self, val):
        if isinstance(val, list):
            self._pois = val
        else:
            raise TypeError(f"Cannot set pois to {val}")

    @property
    def population(self):
        return self._population

    @population.setter
    def population(self, val):
        self._population = int(val)

    @property
    def size(self):
        if self.population < 100:
            return "settlement"
        elif self.population < 1000:
            return "village"
        elif self.population < 10000:
            return "town"
        else:
            return "city"

    ####################### CRUD Methods #######################
    def add_pois(self, description=None):
        poi = POI.build(self.world, parent=self, description=description)
        district = random.choice(self.districts)
        poi.district = district
        poi.save()
        # breakpoint()
        # log(f"Adding a new poi ({poi.pk}-{poi.name}) to City: {self.pk}-{self.name}")
        self.pois.append(poi)
        self.save()
        return poi

    def add_factions(self, description=None):
        fac = Faction.build(world=self.world, parent=self, description=description)
        self.factions.append(fac)
        self.save()
        return fac

    def add_encounters(self, num_players=5, level=5, description=None):
        enc = Encounter.build(self.world, parent=self, description=description)
        self.encounters.append(enc)
        self.save()
        return enc

    def add_characters(self, description=None):
        char = Character.build(world=self.world, parent=None, description=description)
        home = random.choice(self.pois) if self.pois else None
        if not home:
            home = self.add_poi()
        home.characters.append(char)
        home.save()
        char.parent = home
        char.save()
        self.save()
        return char

    def remove_pois(self, obj):
        return super().remove(obj, self.pois)

    def remove_encounters(self, obj):
        return super().remove(obj, self.encounters)

    def remove_factions(self, obj):
        return super().remove(obj, self.factions)

    ####################### Instance Methods #######################
    def has_children(self, value):
        log(value)
        value = value.lower()
        return value if value in ["faction", "encounter", "poi"] else None

    def get_image_prompt(self):
        msg = f"""
        Create a full color, high resolution illustrated view of a {self.title} called {self.name} of with the follwoing details:
        - POPULATION: {self.population} "
        - DISTRICTS: {', '.join(self.districts)}"
        - DESCRIPTION: {self.desc}
        """
        return msg

    def page_data(self):
        return {
            "pk": self.pk,
            "name": self.name,
            "population": self.population,
            "desc": self.desc,
            "backstory": self.backstory,
            "districts": self.districts,
            "pois": [f"{r.pk}" for r in self.pois],
            "encounters": [f"[{r.pk}])" for r in self.encounters],
            "factions": [f"[{r.pk}])" for r in self.factions],
        }

    def state_data(self):
        obj_data = super().state_data
        obj_data["geneology"]["children"] = {
            "POI": [o.pk for o in self.pois],
            "Encounter": [o.pk for o in self.encounters],
            "Faction": [o.pk for o in self.factions],
        }
        obj_data["attributes"].update(
            {
                "population": self.goal,
            }
        )
        obj_data["districts"] = self.districts
        obj_data["size"] = self.size
        return obj_data
