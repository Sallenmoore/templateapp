import inspect
import json
import re

from autonomous import AutoModel, log
from autonomous.ai.oaiagent import OAIAgent


class BaseSystem(AutoModel):
    MAX_TOKEN_LENGTH = 8000

    attributes = {
        "_agent": None,
        "_calendar": {
            "year_string": "CE",
            "current_date": {"day": 0, "month": 0, "year": 0},
            "months": [
                "January",
                "February",
                "March",
                "April",
                "May",
                "June",
                "July",
                "August",
                "September",
                "October",
                "November",
                "December",
            ],
            "days": [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday",
            ],
            "days_per_year": 365,
        },
    }

    _genre = "Mixed"

    _titles = {
        "city": "City",
        "creature": "Creature",
        "faction": "Faction",
        "region": "Region",
        "world": "World",
        "location": "Location",
        "poi": "POI",
        "item": "Item",
        "encounter": "Encounter",
        "character": "Character",
    }

    _stats = {
        "strength": "STR",
        "dexterity": "DEX",
        "constitution": "CON",
        "intelligence": "INT",
        "wisdom": "WIS",
        "charisma": "CHA",
        "hit_points": "HP",
        "armor_class": "AC",
    }

    _currency = {
        "money": "gold pieces",
    }

    ############# Class Methods #############

    @classmethod
    def get_title(cls, obj_type):
        if inspect.isclass(obj_type):
            obj_type = obj_type.__name__
        elif not isinstance(obj_type, str):
            obj_type = obj_type.__class__.__name__
        obj_type = obj_type.lower()
        return cls._titles.get(obj_type, obj_type.capitalize())

    @classmethod
    def sanitize(cls, data):
        if isinstance(data, str):
            clean = re.compile("<.*?>")
            data = re.sub(clean, "", data)
        return data

    ############# Property Methods #############

    @property
    def agent(self):
        if not self._agent:
            self._agent = OAIAgent(
                name=f"{self.genre} TableTop RPG Worldbuiding Agent",
                instructions=self.instructions,
                description=self.description,
            )
            self._agent.save()
            self.save()
        return self._agent

    @property
    def calendar(self):
        return self._calendar

    @calendar.setter
    def calendar(self, value):
        self._calendar = {
            "year_string": value["year_string"],
            "current_date": value.get("current_date")
            or {"day": 0, "month": 0, "year": 0},
            "months": value["months"],
            "days": value["days"],
            "days_per_year": value["days_per_year"],
        }

    @property
    def genre(self):
        return self._genre

    @genre.setter
    def genre(self, value):
        self._genre = value

    @property
    def instructions(self):
        return f"""You are highly skilled AI trained to assist completing the object data for a {self.genre} Table Top RPG. The existing data is provided as structured JSON data describing the schema for characters, creatures, items, locations, encounters, or storylines. You may expand on the object's existing data, but not ignore it.

        Use the uploaded file to reference existing world objects while generating the object's data to ensure world consistency. Make appropriate connections to one or more existing elements in the world as described by the uploaded file."""

    @property
    def num_months_per_year(self):
        return len(self._calendar["months"])

    @property
    def num_days_per_week(self):
        return len(self._calendar["days"])

    @property
    def num_days_per_month(self):
        return self._calendar["days_per_year"] // self.num_months_per_year

    @property
    def description(self):
        return f"A helpful AI assistant trained to return structured JSON data for worldbuilding {self.genre} TTRPG Campaign."

    ############# Instance Methods #############
    def set_calendar(
        self,
        year_string="CE",
        month_names=None,
        day_names=None,
        days_per_year=None,
        current_date=None,
    ):
        log(f"=== current_date ===\n\n{current_date}")
        self._calendar = {
            "year_string": year_string or self._calendar["year_string"],
            "current_date": current_date or self._calendar["current_date"],
            "months": month_names or self._calendar["months"],
            "days": day_names or self._calendar["days"],
            "days_per_year": days_per_year or self._calendar["days_per_year"],
        }
        log(f"=== calendar ===\n\n{self._calendar}")
        if self.save():
            return self._calendar
        log(f"=== calendar ===\n\n{self._calendar}")
        return None

    ############# Generation Methods #############
    def update_refs(self, world):
        self.agent.clear_files()
        world_data = world.page_data()
        # print(world_data)
        ref_db = json.dumps(world_data).encode("utf-8")
        # print(ref_db)
        self.agent.attach_file(ref_db, filename=f"{world.slug}-dbdata.json")

    def generate(self, obj, prompt):
        prompt += "IMPORTANT: The generated data must be consistent with the uploaded reference file and the result must be VALID JSON."
        prompt = self.sanitize(prompt)
        print(f"=== generation prompt ===\n\n{prompt}")
        response = self.agent.generate(prompt, function=obj.funcobj)
        if not isinstance(response, dict):
            raise Exception(response)
        print(f"=== generation response ===\n\n{response}")
        return response

    def generate_summary(self, prompt, primer=""):
        prompt = self.sanitize(prompt)
        prompt_length = len(re.findall(r"\w+", prompt))

        num_chunks = prompt_length // self.MAX_TOKEN_LENGTH + 1
        summary = ""
        for i in range(num_chunks):
            prompt_slice = prompt[
                i * self.MAX_TOKEN_LENGTH : (i + 1) * self.MAX_TOKEN_LENGTH
            ]
            summary += self.agent.summarize_text(prompt_slice, primer=primer)
        return summary

    def generate_image(self, prompt):
        prompt = f"{prompt}. IMPORTANT: The image must not contain any text."
        prompt = self.sanitize(prompt)
        print(f"=== generation prompt ===\n\n{prompt}")
        return self.agent.generate_image(prompt, size="1024x1024")

    def generate_battlemap(self, obj):
        # log("generating battlemap...")
        prompt = f"""
        Create a top-down overhead-perspective map using the provided scale for a {obj.genre} tabletop RPG using the following criteria:
        - IMPORTANT: NO text, grid, creatures, or characters
        - Map Type: {obj.map_type}
        - Scale: {obj.map_scale}
        - {obj.map_prompt}"
        """
        prompt = self.sanitize(prompt)
        print(f"=== generation prompt ===\n\n{prompt}")
        results = self.agent.generate_image(prompt, quality="hd", size="1792x1024")
        return results
