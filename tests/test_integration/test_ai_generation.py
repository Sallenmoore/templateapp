import json

import pytest
from models.region import Region
from models.user import User
from models.world import World

from autonomous import log


def world():
    user = User(name="test", email="email@test")
    user.save()
    world = World.build(system="fantasy", user=user, name="TestWorld")
    world.save()
    for i in range(2):
        region = world.add_region()
        region.name = f"Region {i}"
        for i in range(2):
            location = region.add_location()
            location.name = f"Region Location {i}"
            for i in range(2):
                encounter = location.add_encounter()
                encounter.name = f"Region Location Encounter {i}"
                for i in range(2):
                    creature = encounter.add_enemy()
                    creature.name = f"Region Location Encounter Creature {i}"
                    for i in range(2):
                        item = creature.add_item()
                        item.name = f"Region Location Encounter Creature Item {i}"
                        item.save()
                    creature.save()
                    item = encounter.add_item()
                    item.name = f"Region Location Encounter Item {i}"
                    item.save()
                encounter.save()

                character = location.add_character()
                character.name = f"Region Location Character {i}"
                for i in range(2):
                    item = character.add_item()
                    item.name = f"Region Location Item {i}"
                    item.save()
                character.save()
            location.save()

        for i in range(2):
            faction = region.add_faction()
            faction.name = f"Region Faction {i}"
            for i in range(2):
                character = faction.add_character()
                character.name = f"Faction Character {i}"
                for i in range(2):
                    item = character.add_item()
                    item.name = f"Faction Character Item {i}"
                    item.save()
                character.save()
            faction.save()

        for i in range(2):
            city = region.add_city()
            city.name = f"Region City {i}"
            for i in range(2):
                encounter = city.add_encounter()
                encounter.name = f"City Encounter {i}"
                encounter.save()
                poi = city.add_poi()
                poi.name = f"POI {i}"
                for i in range(2):
                    encounter = poi.add_encounter()
                    encounter.name = f"POI Encounter {i}"
                    encounter.save()
                    character = poi.add_character()
                    character.name = f"POI Character {i}"
                    character.save()
                poi.save()
                faction = city.add_faction()
                faction.name = f"City Faction {i}"
                faction.save()
            city.save()

        for i in range(2):
            encounter = region.add_encounter()
            encounter.name = f"Region Encounter {i}"
            for i in range(2):
                creature = encounter.add_enemy()
                creature.name = f"Region Encounter Creature {i}"
                for i in range(2):
                    item = creature.add_item()
                    item.name = f"Region Encounter Creature Item {i}"
                    item.save()
                creature.save()
            encounter.save()
        region.save()
    world.save()
    return world


class TestAIIntegration:
    w = world()

    def test_file_data(self):
        result = self.w.page_data()
        assert result is not None
        assert isinstance(result, dict)
        assert json.dumps(result).encode("utf-8")
        log(f"World: {result}")

    def test_generation(self):
        result = self.w.generate_region()
        assert result is not None
        assert isinstance(result, Region)
        log(f"Region: {result}")
