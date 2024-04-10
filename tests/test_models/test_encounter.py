import pytest
from models.character import Character
from models.creature import Creature
from models.encounter import Encounter
from models.item import Item
from models.ttrpgobject import TTRPGObject
from models.user import User

from autonomous.ai.agents.mockai import MockAIAgent
from autonomous.ai.autoteam import AutoTeam

TTRPGObject._aiteam = AutoTeam(MockAIAgent)


# @pytest.mark.skip("Working")
class TestEncounter:
    def test_init(self, user, world):
        encounter = Encounter(world=world, name="test")
        assert encounter.name is not None
        assert encounter.desc is not None
        assert encounter.backstory is not None

    def test_repr(self, user, world):
        encounter = Encounter(world=world, name="test")
        repr_string = repr(encounter)
        assert isinstance(repr_string, str)

    def test_parent(self, user, world):
        encounter = Encounter(world=world, name="test")
        assert encounter.parent is None

    def test_parent_setter(self, user, world):
        encounter = Encounter(world=world, name="test")
        with pytest.raises(TypeError):
            encounter.parent = "Not a TTRPGObject"

    def test_world(self, user, world):
        encounter = Encounter(world=world, name="test")
        assert encounter.world is not None

    def test_world_setter(self, user, world):
        encounter = Encounter(world=world, name="test")
        with pytest.raises(TypeError):
            encounter.world = "Not a World"

    def test_user(self, user, world):
        encounter = Encounter(world=world, name="test")
        assert encounter.user is not None

    def test_user_setter(self, user, world):
        encounter = Encounter(world=world, name="test")
        with pytest.raises(AttributeError):
            encounter.user = "Not a User"

    def test_genre(self, user, world):
        encounter = Encounter(world=world, name="test")
        assert encounter.genre == "fantasy"

    def test_genre_setter(self, user, world):
        encounter = Encounter(world=world, name="test")
        with pytest.raises(AttributeError):
            encounter.genre = 123

    def test_get_image_prompt(self, user, world):
        encounter = Encounter(world=world, name="test")
        # print(encounter.get_image_prompt())
        assert encounter.get_image_prompt()

    def test_build(self, user, world):
        encounter = Encounter.build(world, description="A peaceful region")
        assert isinstance(encounter, Encounter)
        assert encounter.world == world
        assert encounter.enemies is not None
        assert encounter.items is not None

    def test_page_data(self, user, world):
        encounter = Encounter(world=world, name="test")
        results = encounter.page_data()
        assert isinstance(results, dict)
        assert results["Details"] is not None

    def test_image(self, user, world):
        obj = Encounter(world=world, name="test")
        obj.generate_image()
        obj.image()
        assert obj.asset_id
        obj.image(size="thumbnail")
        assert obj.asset_id
        obj.image(size="small")
        assert obj.asset_id
        obj.image(size="medium")
        assert obj.asset_id
        obj.image(size="600")
        assert obj.asset_id
        obj.image(size="2000")
        assert obj.asset_id

    def test_generate_image(self, world, user):
        obj = Encounter(world=world, name="test")
        obj.generate_image()
        assert obj.asset_id

    def test_is_owner(self, user, world):
        obj = Encounter(world=world, name="test")
        assert user.world_owner(obj)
        user = User(name="bad", email="bad@bad.com")
        user.save()
        assert not user.world_owner(obj)

    def test_slug(self, user, world):
        obj = Encounter(world=world, name="test object")
        assert obj.slug == "test-object"

    def test_backstory_summary(self, user, world):
        obj = Encounter(world=world, name="test")
        assert obj.backstory_summary

    def test_title(self, user, world):
        obj = Encounter(world=world, name="test")
        assert obj.title == "Encounter"

    def test_api_path(self, user, world):
        obj = Encounter(world=world, name="test")
        assert obj.api_path() == "/api/encounter"

    def test_page_path(self, user, world):
        obj = Encounter(world=world, name="test")
        assert obj.page_path().startswith("/encounter")

    #### Specific to the Class ####

    def test_build_battlemap(self, user, world):
        encounter = Encounter(world=world, name="test")
        encounter.save()
        battlemap = encounter.build_battlemap()
        assert isinstance(battlemap, str)
        assert battlemap == encounter.battlemap_url

    def test_generate_battlemap(self, user, world):
        encounter = Encounter(world=world, name="test")
        encounter.save()
        battlemap = encounter.generate_battlemap()
        assert isinstance(battlemap, str)
        assert battlemap == encounter.battlemap_url

    def test_add_enemy(self, user, world):
        encounter = Encounter(world=world, name="test")
        encounter.save()
        enemy = encounter.add_enemy(enemy_type="creature", generate=False)
        assert isinstance(enemy, (Character, Creature))
        assert enemy in encounter.enemies
        enemy = encounter.add_enemy(enemy_type="creature", generate=True)
        assert isinstance(enemy, (Character, Creature))
        assert enemy in encounter.enemies
        enemy = encounter.add_enemy(enemy_type="humanoid", generate=False)
        assert isinstance(enemy, (Character, Creature))
        assert enemy in encounter.enemies
        enemy = encounter.add_enemy(enemy_type="humanoid", generate=True)
        assert isinstance(enemy, (Character, Creature))
        assert enemy in encounter.enemies

    def test_add_item(self, user, world):
        encounter = Encounter(world=world, name="test")
        encounter.save()
        item = encounter.add_item(generate=False)
        assert isinstance(item, Item)
        assert item in encounter.items
        item = encounter.add_item(generate=True)
        assert isinstance(item, Item)
        assert item in encounter.items
