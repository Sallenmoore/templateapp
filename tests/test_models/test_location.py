import pytest
from models.character import Character
from models.encounter import Encounter
from models.item import Item
from models.location import Location
from models.user import User


# @pytest.mark.skip("Working")
class TestLocation:
    def test_init(self, user, world):
        location = Location(world=world, name="test")
        assert location.name is not None
        assert location.desc is not None
        assert location.backstory is not None

    def test_repr(self, user, world):
        location = Location(world=world, name="test")
        repr_string = repr(location)
        assert isinstance(repr_string, str)

    def test_parent(self, user, world):
        location = Location(world=world, name="test")
        assert location.parent is None

    def test_parent_setter(self, user, world):
        location = Location(world=world, name="test")
        with pytest.raises(TypeError):
            location.parent = "Not a TTRPGObject"

    def test_world(self, user, world):
        location = Location(world=world, name="test")
        assert location.world is not None

    def test_world_setter(self, user, world):
        location = Location(world=world, name="test")
        with pytest.raises(TypeError):
            location.world = "Not a World"

    def test_user(self, user, world):
        location = Location(world=world, name="test")
        assert location.user is not None

    def test_user_setter(self, user, world):
        location = Location(world=world, name="test")
        with pytest.raises(AttributeError):
            location.user = "Not a User"

    def test_genre(self, user, world):
        location = Location(world=world, name="test")
        assert location.genre == "fantasy"

    def test_genre_setter(self, user, world):
        location = Location(world=world, name="test")
        with pytest.raises(AttributeError):
            location.genre = 123

    def test_get_image_prompt(self, user, world):
        location = Location(world=world, name="test")
        # print(location.get_image_prompt())
        assert location.get_image_prompt()

    def test_build(self, user, world):
        location = Location.build(world, description="A peaceful location")
        assert isinstance(location, Location)
        assert location.world == world

    def test_page_data(self, user, world):
        location = Location(world=world, name="test")
        results = location.page_data()
        assert isinstance(results, dict)
        assert results["Owner"] is not None

    def test_image(self, user, world):
        obj = Location(world=world, name="test")
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
        obj = Location(world=world, name="test")
        obj.generate_image()
        assert obj.asset_id

    def test_is_owner(self, user, world):
        obj = Location(world=world, name="test")
        assert user.world_owner(obj)
        user = User(name="bad", email="bad@bad.com")
        user.save()
        assert not user.world_owner(obj)

    def test_slug(self, user, world):
        obj = Location(world=world, name="test object")
        assert obj.slug == "test-object"

    def test_backstory_summary(self, user, world):
        obj = Location(world=world, name="test")
        assert obj.backstory_summary

    def test_title(self, user, world):
        obj = Location(world=world, name="test")
        assert obj.title == "Location"

    def test_api_path(self, user, world):
        obj = Location(world=world, name="test")
        assert obj.api_path() == "/api/location"

    def test_page_path(self, user, world):
        obj = Location(world=world, name="test")
        assert obj.page_path().startswith("/location")

    #### Specific to the Class ####

    def test_build_battlemap(self, user, world):
        location = Location(world=world, name="test")
        location.save()
        battlemap = location.build_battlemap()
        assert isinstance(battlemap, str)
        assert battlemap == location.battlemap_url

    def test_generate_battlemap(self, user, world):
        location = Location(world=world, name="test")
        location.save()
        battlemap = location.generate_battlemap()
        assert isinstance(battlemap, str)
        assert battlemap == location.battlemap_url

    def test_add_character(self, user, world):
        location = Location(world=world, name="test")
        location.save()
        character = location.add_character(generate=False)
        assert isinstance(character, Character)
        assert character in location.characters
        character = location.add_character(generate=True)
        assert isinstance(character, Character)
        assert character in location.characters

    def test_add_encounter(self, user, world):
        location = Location(world=world, name="test")
        location.save()
        encounter = location.add_encounter(num_players=5, level=5, generate=False)
        assert isinstance(encounter, Encounter)
        assert encounter in location.encounters
        encounter = location.add_encounter(num_players=5, level=5, generate=True)
        assert isinstance(encounter, Encounter)
        assert encounter in location.encounters

    def test_add_item(self, user, world):
        location = Location(world=world, name="test")
        location.save()
        item = location.add_item(generate=False)
        assert isinstance(item, Item)
        assert item in location.items
        item = location.add_item(generate=True)
        assert isinstance(item, Item)
        assert item in location.items
