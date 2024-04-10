import pytest
from models.character import Character
from models.poi import POI
from models.city import City
from models.creature import Creature
from models.encounter import Encounter
from models.faction import Faction
from models.item import Item
from models.location import Location
from models.region import Region
from models.ttrpgobject import TTRPGObject
from models.user import User
from models.world import World

from autonomous.ai.agents.mockai import MockAIAgent
from autonomous.ai.autoteam import AutoTeam

TTRPGObject._aiteam = AutoTeam(MockAIAgent)


# @pytest.mark.skip("Working")
class TestWorld:
    def test_remove(self):
        Region.table().flush_table()
        Location.table().flush_table()
        City.table().flush_table()
        POI.table().flush_table()
        Encounter.table().flush_table()
        Faction.table().flush_table()
        Character.table().flush_table()
        Creature.table().flush_table()
        Item.table().flush_table()
        World.table().flush_table()

        self.user = User(name="test", email="email@test")
        self.user.save()
        self.world = World(user=self.user, system="fantasy", name="test")
        self.world.save()
        # def test_add_region(self):
        region = self.world.add_region()
        assert isinstance(region, Region)
        assert region.genre == self.world.genre
        assert region.parent == self.world
        assert region.world == self.world

        city = region.add_city()
        obj = city
        assert isinstance(obj, City)
        assert obj.genre == self.world.genre
        assert obj.parent == region
        assert obj.world == self.world

        location = region.add_location()
        obj = location
        assert isinstance(obj, Location)
        assert obj.genre == self.world.genre
        assert obj.parent == region
        assert obj.world == self.world

        faction = region.add_faction()
        obj = faction
        assert isinstance(obj, Faction)
        assert obj.genre == self.world.genre
        assert obj.parent == region
        assert obj.world == self.world

        encounter = region.add_encounter()
        obj = encounter
        assert isinstance(obj, Encounter)
        assert obj.genre == self.world.genre
        assert obj.parent == region
        assert obj.world == self.world

        location_character = location.add_character()
        obj = location_character
        assert isinstance(obj, Character)
        assert obj.genre == self.world.genre
        assert obj.parent == location
        assert obj.world == self.world

        location_item = location.add_item()
        obj = location_item
        assert isinstance(obj, Item)
        assert obj.genre == self.world.genre
        assert obj.parent == location
        assert obj.world == self.world

        location_encounter = location.add_encounter()
        obj = location_encounter
        assert isinstance(obj, Encounter)
        assert obj.genre == self.world.genre
        assert obj.parent == location
        assert obj.world == self.world

        city_faction = city.add_faction()
        obj = city_faction
        assert isinstance(obj, Faction)
        assert obj.genre == self.world.genre
        assert obj.parent == city
        assert obj.world == self.world

        city_location = city.add_poi()
        obj = city_location
        assert isinstance(obj, Location)
        assert obj.genre == self.world.genre
        assert obj.parent == city
        assert obj.world == self.world

        city_encounter = city.add_encounter()
        obj = city_encounter
        assert isinstance(obj, Encounter)
        assert obj.genre == self.world.genre
        assert obj.parent == city
        assert obj.world == self.world

        encounter_enemy = encounter.add_enemy()
        obj = encounter_enemy
        assert isinstance(obj, Creature)
        assert obj.genre == self.world.genre
        assert obj.parent == encounter
        assert obj.world == self.world
        encounter.add_item()

        creature_item = encounter_enemy.add_item()
        obj = creature_item
        assert isinstance(obj, Item)
        assert obj.genre == self.world.genre
        assert obj.parent == encounter_enemy
        assert obj.world == self.world
        encounter.add_item()

        faction_character = faction.add_character()
        obj = faction_character
        assert isinstance(obj, Character)
        assert obj.genre == self.world.genre
        assert obj.parent == faction
        assert obj.world == self.world
        encounter.add_item()

        character_item = faction_character.add_item()
        obj = character_item
        assert isinstance(obj, Item)
        assert obj.genre == self.world.genre
        assert obj.parent == faction_character
        assert obj.world == self.world

        character_item = Item.get(faction_character.remove_item(character_item.pk))
        assert character_item.world == self.world
        assert character_item.parent is None
        assert character_item not in faction_character.items
        assert character_item not in self.world.items
        assert character_item in self.world.unassigned()

        faction_character = Character.get(
            faction.remove_character(faction_character.pk)
        )
        assert faction_character.world == self.world
        assert faction_character.parent is None
        assert faction_character not in faction.characters
        assert faction_character not in self.world.characters
        assert faction_character in self.world.unassigned()

        creature_item = Item.get(encounter_enemy.remove_item(creature_item.pk))
        assert creature_item.world == self.world
        assert creature_item.parent is None
        assert creature_item not in encounter_enemy.items
        assert creature_item not in self.world.items
        assert creature_item in self.world.unassigned()

        encounter_enemy = Creature.get(encounter.remove_enemy(encounter_enemy.pk))
        assert encounter_enemy.world == self.world
        assert encounter_enemy.parent is None
        assert encounter_enemy not in encounter.creatures
        assert encounter_enemy not in self.world.creatures
        assert encounter_enemy in self.world.unassigned()

        city_encounter = Encounter.get(city.remove_encounter(city_encounter.pk))
        assert city_encounter.world == self.world
        assert city_encounter.parent is None
        assert city_encounter not in city.encounters
        assert city_encounter not in self.world.encounters
        assert city_encounter in self.world.unassigned()

        city_location = POI.get(city.remove_poi(city_location.pk))
        assert city_encounter.world == self.world
        assert city_encounter.parent is None
        assert city_encounter not in city.pois
        assert city_encounter not in self.world.locations
        assert city_encounter in self.world.unassigned()

        city_faction = Faction.get(city.remove_faction(city_faction.pk))
        assert city_faction.world == self.world
        assert city_faction.parent is None
        assert city_faction not in city.factions
        assert city_faction not in self.world.factions
        assert city_faction in self.world.unassigned()

        location_encounter = Encounter.get(
            location.remove_encounter(location_encounter.pk)
        )
        assert location_encounter.world == self.world
        assert location_encounter.parent is None
        assert location_encounter not in location.encounters
        assert location_encounter not in self.world.encounters
        assert location_encounter in self.world.unassigned()

        location_item = Item.get(location.remove_item(location_item.pk))
        assert location_item.world == self.world
        assert location_item.parent is None
        assert location_item not in location.items
        assert location_item not in self.world.items
        assert location_item in self.world.unassigned()

        location_character = Character.get(
            location.remove_character(location_character.pk)
        )
        assert location_character.world == self.world
        assert location_character.parent is None
        assert location_character not in location.characters
        assert location_character not in self.world.characters
        assert location_character in self.world.unassigned()

        encounter = Encounter.get(region.remove_encounter(encounter.pk))
        assert encounter.world == self.world
        assert encounter.parent is None
        assert encounter not in region.encounters
        assert encounter not in self.world.encounters
        assert encounter in self.world.unassigned()

        faction = Faction.get(region.remove_faction(faction.pk))
        assert faction.world == self.world
        assert faction.parent is None
        assert faction not in region.factions
        assert faction not in self.world.factions
        assert faction in self.world.unassigned()

        location = Location.get(region.remove_location(location.pk))
        assert location.world == self.world
        assert location.parent is None
        assert location not in region.locations
        assert location not in self.world.locations
        assert location in self.world.unassigned()

        city = City.get(region.remove_city(city.pk))
        assert city.world == self.world
        assert city.parent is None
        assert city not in region.cities
        assert city not in self.world.cities
        assert city in self.world.unassigned()

        region = Region.get(self.world.remove_region(region.pk))
        assert region.world == self.world
        assert region.parent is None
        assert region not in self.world.regions
        assert region in self.world.unassigned()

    def test_delete(self):
        Region.table().flush_table()
        Location.table().flush_table()
        City.table().flush_table()
        POI.table().flush_table()
        Encounter.table().flush_table()
        Faction.table().flush_table()
        Character.table().flush_table()
        Creature.table().flush_table()
        Item.table().flush_table()
        World.table().flush_table()

        self.user = User(name="test", email="email@test")
        self.user.save()
        self.world = World(user=self.user, system="fantasy", name="test")
        self.world.save()
        # def test_add_region(self):
        region = self.world.add_region()
        assert isinstance(region, Region)
        assert region.genre == self.world.genre
        assert region.parent is self.world
        assert region.world == self.world

        city = region.add_city()
        obj = city
        assert isinstance(obj, City)
        assert obj.genre == self.world.genre
        assert obj.parent == region
        assert obj.world == self.world

        location = region.add_location()
        obj = location
        assert isinstance(obj, Location)
        assert obj.genre == self.world.genre
        assert obj.parent == region
        assert obj.world == self.world

        faction = region.add_faction()
        obj = faction
        assert isinstance(obj, Faction)
        assert obj.genre == self.world.genre
        assert obj.parent == region
        assert obj.world == self.world

        encounter = region.add_encounter()
        obj = encounter
        assert isinstance(obj, Encounter)
        assert obj.genre == self.world.genre
        assert obj.parent == region
        assert obj.world == self.world

        location_character = location.add_character()
        obj = location_character
        assert isinstance(obj, Character)
        assert obj.genre == self.world.genre
        assert obj.parent == location
        assert obj.world == self.world

        location_item = location.add_item()
        obj = location_item
        assert isinstance(obj, Item)
        assert obj.genre == self.world.genre
        assert obj.parent == location
        assert obj.world == self.world

        location_encounter = location.add_encounter()
        obj = location_encounter
        assert isinstance(obj, Encounter)
        assert obj.genre == self.world.genre
        assert obj.parent == location
        assert obj.world == self.world

        city_faction = city.add_faction()
        obj = city_faction
        assert isinstance(obj, Faction)
        assert obj.genre == self.world.genre
        assert obj.parent == city
        assert obj.world == self.world

        city_location = city.add_poi()
        obj = city_location
        assert isinstance(obj, Location)
        assert obj.genre == self.world.genre
        assert obj.parent == city
        assert obj.world == self.world

        city_encounter = city.add_encounter()
        obj = city_encounter
        assert isinstance(obj, Encounter)
        assert obj.genre == self.world.genre
        assert obj.parent == city
        assert obj.world == self.world

        encounter_enemy = encounter.add_enemy()
        obj = encounter_enemy
        assert isinstance(obj, Creature)
        assert obj.genre == self.world.genre
        assert obj.parent == encounter
        assert obj.world == self.world

        encounter_items = encounter.add_item()
        obj = encounter_items
        assert isinstance(obj, Item)
        assert obj.genre == self.world.genre
        assert obj.parent == encounter
        assert obj.world == self.world

        creature_item = encounter_enemy.add_item()
        obj = creature_item
        assert isinstance(obj, Item)
        assert obj.genre == self.world.genre
        assert obj.parent == encounter_enemy
        assert obj.world == self.world
        encounter.add_item()

        faction_character = faction.add_character()
        obj = faction_character
        assert isinstance(obj, Character)
        assert obj.genre == self.world.genre
        assert obj.parent == faction
        assert obj.world == self.world
        encounter.add_item()

        character_item = faction_character.add_item()
        obj = character_item
        assert isinstance(obj, Item)
        assert obj.genre == self.world.genre
        assert obj.parent == faction_character
        assert obj.world == self.world

        character_item = Item.get(faction_character.remove_item(character_item.pk))
        character_item.delete()
        assert not Item.get(character_item.pk)
        assert character_item not in self.world.unassigned()

        faction_character = Character.get(
            faction.remove_character(faction_character.pk)
        )
        faction_character.delete()
        assert not Character.get(faction_character.pk)
        assert faction_character not in self.world.unassigned()

        creature_item = Item.get(encounter_enemy.remove_item(creature_item.pk))
        creature_item.delete()
        assert not Item.get(creature_item.pk)
        assert creature_item not in self.world.unassigned()

        encounter_enemy = Creature.get(encounter.remove_enemy(encounter_enemy.pk))
        encounter_enemy.delete()
        assert not Creature.get(encounter_enemy.pk)
        assert encounter_enemy not in self.world.unassigned()

        city_encounter = Encounter.get(city.remove_encounter(city_encounter.pk))
        city_encounter.delete()
        assert not Encounter.get(city_encounter.pk)
        assert city_encounter not in self.world.unassigned()

        city_location = POI.get(city.remove_poi(city_location.pk))
        city_location.delete()
        assert not POI.get(city_location.pk)
        assert city_encounter not in self.world.unassigned()

        city_faction = Faction.get(city.remove_faction(city_faction.pk))
        city_faction.delete()
        assert not Faction.get(city_faction.pk)
        assert city_faction not in self.world.unassigned()

        location_encounter = Encounter.get(
            location.remove_encounter(location_encounter.pk)
        )
        location_encounter.delete()
        assert not Encounter.get(location_encounter.pk)
        assert location_encounter not in self.world.unassigned()

        location_item = Item.get(location.remove_item(location_item.pk))
        location_item.delete()
        assert not Item.get(location_item.pk)
        assert location_item not in self.world.unassigned()

        location_character = Character.get(
            location.remove_character(location_character.pk)
        )
        location_character.delete()
        assert not Character.get(location_character.pk)
        assert location_character not in self.world.unassigned()

        encounter = Encounter.get(region.remove_encounter(encounter.pk))
        encounter.delete()
        assert not Encounter.get(encounter.pk)
        assert encounter not in self.world.unassigned()

        faction = Faction.get(region.remove_faction(faction.pk))
        faction.delete()
        assert not Faction.get(faction.pk)
        assert faction not in self.world.unassigned()

        location = Location.get(region.remove_location(location.pk))
        location.delete()
        assert not Location.get(location.pk)
        assert location not in self.world.unassigned()

        city = City.get(region.remove_city(city.pk))
        city.delete()
        assert not City.get(city.pk)
        assert city not in self.world.unassigned()

        region = Region.get(self.world.remove_region(region.pk))
        region.delete()
        assert not Region.get(region.pk)
        assert region not in self.world.unassigned()

        pk = self.world.pk
        self.world.delete()
        assert not World.get(pk)
