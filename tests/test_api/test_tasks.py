from models.character import Character
from models.poi import POI
from models.city import City
from models.creature import Creature
from models.encounter import Encounter
from models.faction import Faction
from models.item import Item
from models.location import Location
from models.region import Region
from models.world import World

from autonomous import log

####################################################################################################
# World Tasks
####################################################################################################


# def test_world_generate_region_task(world):
#     region = world.add_region(generate=True)
#     assert region
#     assert region.pk


# def test_world_generate_faction_task(world):
#     faction = world.add_faction(generate=True)
#     assert faction
#     assert faction.pk


# def test_world_generate_player_task(world):
#     description = (
#         world.player_faction.desc
#         if world.player_faction
#         else "An character with a long term goal that requires help from a few other individuals, unbeknownst to them."
#     )
#     character = world.add_characters(generate=True, description=description)
#     assert character
#     assert character.pk


# def test_world_image_generate_task(pk):
#     return {"results": World.get(pk).generate_image()}

# ####################################################################################################
# # Region Tasks
# ####################################################################################################


# def test_region_generate_encounter_task(pk):
#     result = Region.get(pk).add_encounter(generate=True)
#     return {"results": {"pk": result.pk, "api": result.api_path()}}


# def test_region_generate_city_task(pk):
#     result = Region.get(pk).add_city(generate=True)
#     return {"results": {"pk": result.pk, "api": result.api_path()}}


# def test_region_generate_location_task(pk):
#     result = Region.get(pk).add_location(generate=True)
#     return {"results": {"pk": result.pk, "api": result.api_path()}}


# def test_region_generate_faction_task(pk):
#     result = Region.get(pk).add_faction(generate=True)
#     return {"results": {"pk": result.pk, "api": result.api_path()}}


# def test_region_create_battlemap(pk):
#     obj = Region.get(pk)
#     return {"results": obj.generate_battlemap()}


# def test_region_image_generate_task(pk):
#     return {"results": Region.get(pk).generate_image()}


# ####################################################################################################
# # Location Tasks
# ####################################################################################################
# def test_location_generate_encounter_task(pk):
#     result = Location.get(pk).add_encounter(generate=True)
#     return {"results": {"pk": result.pk, "api": result.api_path()}}


# def test_location_generate_character_task(pk):
#     result = Location.get(pk).add_character(generate=True)
#     return {"results": {"pk": result.pk, "api": result.api_path()}}


# def test_location_generate_item_task(pk):
#     result = Location.get(pk).add_item(generate=True)
#     return {"results": {"pk": result.pk, "api": result.api_path()}}


# def test_location_create_battlemap(pk):
#     obj = Location.get(pk)
#     return {"results": obj.generate_battlemap()}


# def test_location_image_generate_task(pk):
#     return {"results": Location.get(pk).generate_image()}


# ####################################################################################################
# # POI Tasks
# ####################################################################################################
# def test_poi_generate_encounter_task(pk):
#     result = POI.get(pk).add_encounter(generate=True)
#     return {"results": {"pk": result.pk, "api": result.api_path()}}


# def test_poi_generate_character_task(pk):
#     result = POI.get(pk).add_character(generate=True)
#     return {"results": {"pk": result.pk, "api": result.api_path()}}


# def test_poi_generate_item_task(pk):
#     result = POI.get(pk).add_item(generate=True)
#     return {"results": {"pk": result.pk, "api": result.api_path()}}


# def test_poi_create_battlemap(pk):
#     obj = POI.get(pk)
#     return {"results": obj.generate_battlemap()}


# def test_poi_image_generate_task(pk):
#     return {"results": POI.get(pk).generate_image()}

# ####################################################################################################
# # City Tasks
# ####################################################################################################


# def test_city_generate_location_task(pk, generate=False):
#     city = City.get(pk)
#     obj = city.add_poi(generate=True)
#     return {"results": {"pk": obj.pk, "api": obj.api_path()}}


# def test_city_generate_encounter_task(pk):
#     city = City.get(pk)
#     enc = city.add_encounter(generate=True)
#     return {"results": {"pk": enc.pk, "api": enc.api_path()}}


# def test_city_generate_faction_task(pk):
#     city = City.get(pk)
#     faction = city.add_faction(generate=True)
#     return {"results": {"pk": faction.pk, "api": faction.api_path()}}


# def test_city_generate_character_task(pk):
#     city = City.get(pk)
#     character = city.add_character(generate=True)
#     return {"results": {"pk": character.pk, "api": character.api_path()}}


# def test_city_create_battlemap(pk):
#     obj = City.get(pk)
#     return {"results": obj.generate_battlemap()}


# def test_city_image_generate_task(pk):
#     return {"results": City.get(pk).generate_image()}


# ####################################################################################################
# # Encounter Tasks
# ####################################################################################################


# def test_encounter_generate_enemy_task(pk):
#     result = Encounter.get(pk).add_enemy(generate=True)
#     return {"results": {"pk": result.pk, "api": result.api_path()}}


# def test_encounter_generate_items_task(pk):
#     result = Encounter.get(pk).add_item(generate=True)
#     return {"results": {"pk": result.pk, "api": result.api_path()}}


# def test_encounter_create_battlemap(pk):
#     obj = Encounter.get(pk)
#     return {"results": obj.generate_battlemap()}


# def test_encounter_image_generate_task(pk):
#     return {"results": Encounter.get(pk).generate_image()}


# ####################################################################################################
# # Faction Tasks
# ####################################################################################################


# def test_faction_generate_character_task(pk, leader=False):
#     faction = Faction.get(pk)
#     character = faction.add_character(generate=True, leader=leader)
#     # log(character)
#     return {"results": {"pk": character.pk, "api": character.api_path()}}


# def test_faction_create_battlemap(pk):
#     obj = Faction.get(pk)
#     return {"results": obj.generate_battlemap()}


# def test_faction_image_generate_task(pk):
#     return {"results": Faction.get(pk).generate_image()}


# ####################################################################################################
# # Item Tasks
# ####################################################################################################


# def test_item_create_battlemap(pk):
#     obj = Item.get(pk)
#     return {"results": obj.generate_battlemap()}


# def test_item_image_generate_task(pk):
#     return {"results": Item.get(pk).generate_image()}


# ####################################################################################################
# # Creature Tasks
# ####################################################################################################


# def test_creature_generate_items_task(pk):
#     creature = Creature.get(pk)
#     item = creature.add_item(generate=True)
#     return {"results": {"pk": item.pk, "api": item.api_path()}}


# def test_creature_create_battlemap(pk):
#     obj = Creature.get(pk)
#     return {"results": obj.generate_battlemap()}


# def test_creature_image_generate_task(pk):
#     return {"results": Creature.get(pk).generate_image()}

# ####################################################################################################
# # Character Tasks
# ####################################################################################################


# def test_character_generate_items_task(pk):
#     character = Character.get(pk)
#     item = character.add_item(generate=True)
#     return {"results": {"pk": item.pk, "api": item.api_path()}}


# def test_character_chat_task(pk, message):
#     # log(pk, message)
#     obj = Character.get(pk)
#     obj.chat(message)
#     return {"results": obj.chats}


# def test_character_create_battlemap(pk):
#     obj = Character.get(pk)
#     return {"results": obj.generate_battlemap()}


# def test_character_image_generate_task(pk):
#     return {"results": Character.get(pk).generate_image()}
