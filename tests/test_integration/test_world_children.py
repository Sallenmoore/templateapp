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

from autonomous import log


# @pytest.mark.skip("Working")
class TestWorld:
    def test_init(self):
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

        log("test_build_world")
        self.user = User(name="test", email="email@test")
        self.user.save()
        self.world = World.build(user=self.user, system="fantasy", name="worldtest")
        self.world.save()

        log("test_add_region")
        self.world.add_region()
        # breakpoint()
        self.world.add_region()
        self.world.add_region()
        assert len(self.world.regions) == 3
        assert all(isinstance(_, Region) for _ in self.world.regions)

        assert len(self.world.unassigned()) == 0

        log("test_add_region_child_objs")
        for region in self.world.regions:
            # print("=====")
            region.add_city()
            region.add_location()
            region.add_faction()
            region.add_encounter()

        assert len(self.world.unassigned()) == 0
        assert len(self.world.regions) == 3
        assert all(isinstance(_, Region) for _ in self.world.regions)
        for region in self.world.regions:
            assert len(region.cities) == 1
            assert all(isinstance(_, City) for _ in region.cities)
            assert len(region.locations) == 1
            assert all(isinstance(_, Location) for _ in region.locations)
            assert len(region.factions) == 1
            assert all(isinstance(_, Faction) for _ in region.factions)
            assert len(region.encounters) == 1
            assert all(isinstance(_, Encounter) for _ in region.encounters)

        assert len(self.world.unassigned()) == 0

        log("test_add_location_child_objs")
        for region in self.world.regions:
            for location in region.locations:
                location.add_character()
                location.add_item()
                location.add_encounter()

            assert len(region.locations) == 1
            assert all(isinstance(_, Location) for _ in region.locations)
            for location in region.locations:
                assert len(location.characters) == 1
                assert all(isinstance(_, Character) for _ in location.characters)
                assert len(location.items) == 1
                assert all(isinstance(_, Item) for _ in location.items)
                assert len(location.encounters) == 1
                assert all(isinstance(_, Encounter) for _ in location.encounters)

        log("test_add_city_child_objs")
        for region in self.world.regions:
            for city in region.cities:
                city.add_faction()
                city.add_poi()
                city.add_encounter()

            assert len(region.cities) == 1
            assert all(isinstance(_, City) for _ in region.cities)
            for city in region.cities:
                assert len(city.factions) == 1
                assert all(isinstance(_, Faction) for _ in city.factions)
                assert len(city.pois) == 1
                assert all(isinstance(_, POI) for _ in city.pois)
                assert len(city.encounters) == 1
                assert all(isinstance(_, Encounter) for _ in city.encounters)

        log("test_add_encounter_child_objs")
        for region in self.world.regions:
            for encounter in region.encounters:
                encounter.add_enemy()
                encounter.add_item()

            assert len(region.encounters) == 1
            assert all(isinstance(_, Encounter) for _ in region.encounters)
            for encounter in region.encounters:
                assert len(encounter.enemies) == 1
                assert all(
                    isinstance(_, (Character, Creature)) for _ in encounter.enemies
                )
                assert len(encounter.items) == 1
                assert all(isinstance(_, Item) for _ in encounter.items)

        log("test_add_faction_child_objs")
        for region in self.world.regions:
            for faction in region.factions:
                faction.add_character()
                faction.add_character(leader=True)

            assert len(region.factions) == 1
            assert all(isinstance(_, Faction) for _ in region.factions)
            for faction in region.factions:
                assert len(faction.characters) == 2
                assert all(isinstance(_, (Character)) for _ in faction.characters)
                assert faction.leader
                assert isinstance(faction.leader, Character)

        log("test_add_character_child_objs")
        for region in self.world.regions:
            for faction in region.factions:
                for character in faction.characters:
                    character.add_item()

                assert len(faction.characters) == 2
                assert all(isinstance(_, (Character)) for _ in faction.characters)
                for character in faction.characters:
                    assert len(character.items) == 1
                    assert all(isinstance(_, (Item)) for _ in character.items)

        log("test_add_creature_child_objs")
        for region in self.world.regions:
            for encounter in region.encounters:
                for enemy in encounter.enemies:
                    enemy.add_item()

                assert len(encounter.enemies) == 1
                assert all(isinstance(_, (Creature)) for _ in encounter.enemies)
                for character in encounter.enemies:
                    assert len(character.items) == 1
                    assert all(isinstance(_, (Item)) for _ in character.items)

        log("test_world_build")
        objs = [
            *Region.all(),
            *City.all(),
            *Location.all(),
            *Encounter.all(),
            *Faction.all(),
            *Creature.all(),
            *Item.all(),
            *Character.all(),
        ]
        for obj in objs:
            assert self.user.world_owner(obj)
            assert obj.world == self.world
            assert isinstance(obj.parent, TTRPGObject)

        assert len([obj for obj in Region.all() if obj.world == self.world]) == 3
        assert len([obj for obj in Location.all() if obj.world == self.world]) == 3
        assert len([obj for obj in City.all() if obj.world == self.world]) == 3
        assert len([obj for obj in Item.all() if obj.world == self.world]) == 15
        assert len([obj for obj in Encounter.all() if obj.world == self.world]) == 9
        assert len([obj for obj in Faction.all() if obj.world == self.world]) == 6
        assert len([obj for obj in POI.all() if obj.world == self.world]) == 3
        assert len([obj for obj in Character.all() if obj.world == self.world]) == 9
        assert len([obj for obj in Creature.all() if obj.world == self.world]) == 3
        assert all(isinstance(_, Region) for _ in self.world.regions)
        assert all(isinstance(_, (Location, POI)) for _ in self.world.locations)
        assert all(isinstance(_, City) for _ in self.world.cities)
        assert all(isinstance(_, Encounter) for _ in self.world.encounters)
        assert all(isinstance(_, Faction) for _ in self.world.factions)
        assert all(isinstance(_, Character) for _ in self.world.characters)
        assert all(isinstance(_, Creature) for _ in self.world.creatures)

        objs = [
            *self.world.regions,
            *self.world.locations,
            *self.world.cities,
            *self.world.encounters,
            *self.world.factions,
            *self.world.characters,
            *self.world.creatures,
            *self.world.items,
        ]
        for obj in objs:
            assert self.user.world_owner(obj)
            assert obj.genre == self.world.genre
            assert isinstance(obj.parent, TTRPGObject)

        assert len(self.world.unassigned()) == 0

        log("test_remove_faction_child_objs")
        for region in self.world.regions:
            for faction in region.factions[:]:
                for character in faction.characters[:]:
                    for item in character.items[:]:
                        item = Item.get(character.remove_item(item.pk))
                        assert item.parent is None
                        assert item.world == self.world
                    faction.remove_character(character.pk)
                    character = Character.get(character.pk)
                    assert character.parent is None
                    assert character.world == self.world
                region.remove_faction(faction.pk)
                faction = Faction.get(faction.pk)
                assert faction.parent is None
                assert faction.world == self.world
            assert len(region.factions) == 0

        log("test_remove_encounter_child_objs")
        for region in self.world.regions:
            for encounter in region.encounters[:]:
                for enemy in encounter.enemies[:]:
                    for item in enemy.items[:]:
                        enemy.remove_item(item.pk)
                        item = Item.get(item.pk)
                        assert item.parent is None and item.world == self.world
                    encounter.remove_enemy(enemy.pk)
                    encounter = Encounter.get(encounter.pk)
                    assert enemy.parent is None and enemy.world == self.world
                for item in encounter.items[:]:
                    encounter.remove_item(item.pk)
                    item = Item.get(item.pk)
                    assert item.parent is None and item.world == self.world
                region.remove_encounter(encounter.pk)
                encounter = Encounter.get(encounter.pk)
                assert encounter.parent is None and encounter.world == self.world
            assert len(region.encounters) == 0

        log("test_remove_city_child_objs")
        for region in self.world.regions:
            for city in region.cities[:]:
                for location in city.pois[:]:
                    for enemy in location.characters[:]:
                        for item in enemy.items[:]:
                            enemy.remove_item(item.pk)
                            item = Item.get(item.pk)
                            assert item.parent is None and item.world == self.world
                        location.remove_character(enemy.pk)
                        creature = Creature.get(enemy.pk)
                        assert creature.parent is None and creature.world == self.world
                    for item in location.items[:]:
                        location.remove_item(item.pk)
                        item = Item.get(item.pk)
                        assert item.parent is None and item.world == self.world
                    for encounter in location.encounters[:]:
                        for enemy in encounter.enemies[:]:
                            for item in enemy.items[:]:
                                enemy.remove_item(item.pk)
                                item = Item.get(item.pk)
                                assert item.parent is None and item.world == self.world
                            encounter.remove_enemy(enemy.pk)
                            enemy = Creature.get(enemy.pk)
                            assert enemy.parent is None and enemy.world == self.world
                        for item in encounter.items[:]:
                            encounter.remove_item(item.pk)
                            item = Item.get(item.pk)
                            assert item.parent is None and item.world == self.world
                        location.remove_encounter(encounter.pk)
                        encounter = Encounter.get(encounter.pk)
                        assert (
                            encounter.parent is None and encounter.world == self.world
                        )
                    city.remove_poi(location.pk)
                    location = POI.get(location.pk)
                    assert location.parent is None and location.world == self.world
                assert len(city.pois) == 0
                for faction in city.factions[:]:
                    for character in faction.characters[:]:
                        for item in character.items[:]:
                            character.remove_item(item.pk)
                            item = Item.get(item.pk)
                            assert item.parent is None and item.world == self.world
                        faction.remove_character(character.pk)
                        character = Character.get(character.pk)
                        assert (
                            character.parent is None and character.world == self.world
                        )
                    city.remove_faction(faction.pk)
                    faction = Faction.get(faction.pk)
                    assert faction.parent is None and faction.world == self.world
                assert len(city.factions) == 0
                for encounter in city.encounters[:]:
                    for enemy in encounter.enemies[:]:
                        for item in enemy.items[:]:
                            enemy.remove_item(item.pk)
                            item = Item.get(item.pk)
                            assert item.parent is None and item.world == self.world
                        encounter.remove_enemy(enemy.pk)
                        enemy = Creature.get(enemy.pk)
                        assert enemy.parent is None and enemy.world == self.world
                    for item in encounter.items[:]:
                        encounter.remove_item(item.pk)
                        item = Item.get(item.pk)
                        assert item.parent is None and item.world == self.world
                    city.remove_encounter(encounter.pk)
                    encounter = Encounter.get(encounter.pk)
                    assert encounter.parent is None and encounter.world == self.world
                assert len(city.encounters) == 0
                region.remove_city(city.pk)
                city = City.get(city.pk)
                assert city.parent is None and city.world == self.world
            assert len(region.cities) == 0

        log("test_remove_location_child_objs")
        for region in self.world.regions:
            for location in region.locations[:]:
                for character in location.characters[:]:
                    for item in character.items[:]:
                        character.remove_item(item.pk)
                        item = Item.get(item.pk)
                        assert item.parent is None and item.world == self.world
                    location.remove_character(character.pk)
                    character = Character.get(character.pk)
                    assert character.parent is None and character.world == self.world
                for item in location.items[:]:
                    location.remove_item(item.pk)
                    item = Item.get(item.pk)
                    assert item.parent is None and item.world == self.world
                for encounter in location.encounters[:]:
                    for enemy in encounter.enemies[:]:
                        for item in enemy.items[:]:
                            enemy.remove_item(item.pk)
                            item = Item.get(item.pk)
                            assert item.parent is None and item.world == self.world
                        encounter.remove_enemy(enemy.pk)
                        enemy = Encounter.get(enemy.pk)
                        assert enemy.parent is None and enemy.world == self.world
                    for item in encounter.items[:]:
                        encounter.remove_item(item.pk)
                        item = Item.get(item.pk)
                        assert item.parent is None and item.world == self.world
                    location.remove_encounter(encounter.pk)
                    encounter = Encounter.get(encounter.pk)
                    assert encounter.parent is None and encounter.world == self.world
                region.remove_location(location.pk)
                location = Location.get(location.pk)
                assert location.parent is None and location.world == self.world
            assert len(region.locations) == 0

        log("test_remove_region_child_objs")
        for region in self.world.regions[:]:
            self.world.remove_region(region.pk)
            region = Region.get(region.pk)
            assert region.parent is None and region.world == self.world

        assert len(self.world.regions) == 0

        assert len(self.world.unassigned()) == 54

        log("test_world_delete")
        for obj in self.world.unassigned():
            log(obj.parent)
            obj.delete()

        assert len(self.world.unassigned()) == 0

        self.world.delete()
        assert not Region.all()
        assert not City.all()
        assert not Location.all()
        assert not POI.all()
        assert not Encounter.all()
        assert not Faction.all()
        assert not Character.all()
        assert not Creature.all()
        assert not Item.all()
        assert not World.all()
