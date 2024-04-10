import pytest
from models.character import Character
from models.faction import Faction
from models.user import User


# @pytest.mark.skip("Working")
class TestFaction:
    def test_init(self, user, world):
        faction = Faction(world=world, name="test")
        assert faction.name is not None
        assert faction.desc is not None
        assert faction.backstory is not None

    def test_repr(self, user, world):
        faction = Faction(world=world, name="test")
        repr_string = repr(faction)
        assert isinstance(repr_string, str)

    def test_parent(self, user, world):
        faction = Faction(world=world, name="test")
        assert faction.parent is None

    def test_parent_setter(self, user, world):
        faction = Faction(world=world, name="test")
        with pytest.raises(TypeError):
            faction.parent = "Not a TTRPGObject"

    def test_world(self, user, world):
        faction = Faction(world=world, name="test")
        assert faction.world is not None

    def test_world_setter(self, user, world):
        faction = Faction(world=world, name="test")
        with pytest.raises(TypeError):
            faction.world = "Not a World"

    def test_user(self, user, world):
        faction = Faction(world=world, name="test")
        assert faction.user is not None

    def test_user_setter(self, user, world):
        faction = Faction(world=world, name="test")
        with pytest.raises(AttributeError):
            faction.user = "Not a User"

    def test_genre(self, user, world):
        faction = Faction(world=world, name="test")
        assert faction.genre == "fantasy"

    def test_genre_setter(self, user, world):
        faction = Faction(world=world, name="test")
        with pytest.raises(AttributeError):
            faction.genre = 123


    def test_get_image_prompt(self, user, world):
        faction = Faction(world=world, name="test")
        # print(faction.get_image_prompt())
        assert faction.get_image_prompt()

    def test_build(self, user, world):
        faction = Faction.build(world, description="A peaceful region")
        assert isinstance(faction, Faction)
        assert faction.world == world
        assert faction.characters is not None

    def test_page_data(self, user, world):
        faction = Faction(world=world, name="test")
        results = faction.page_data()
        assert isinstance(results, dict)
        assert results["Details"] is not None

    def test_image(self, user, world):
        obj = Faction(world=world, name="test")
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
        obj = Faction(world=world, name="test")
        obj.generate_image()
        assert obj.asset_id

    def test_is_owner(self, user, world):
        obj = Faction(world=world, name="test")
        assert user.world_owner(obj)
        user = User(name="bad", email="bad@bad.com")
        user.save()
        assert not user.world_owner(obj)

    def test_slug(self, user, world):
        obj = Faction(world=world, name="test object")
        assert obj.slug == "test-object"

    def test_backstory_summary(self, user, world):
        obj = Faction(world=world, name="test")
        assert obj.backstory_summary

    def test_title(self, user, world):
        obj = Faction(world=world, name="test")
        assert obj.title == "Faction"

    def test_api_path(self, user, world):
        obj = Faction(world=world, name="test")
        assert obj.api_path() == "/api/faction"

    def test_page_path(self, user, world):
        obj = Faction(world=world, name="test")
        assert obj.page_path().startswith("/faction")

    #### Specific to the Class ####

    def test_add_character(self, user, world):
        faction = Faction(world=world, parent=world, name="test")
        faction.save()
        character = faction.add_character()
        assert isinstance(character, (Character))
        assert character in faction.characters
        character = faction.add_character(leader=True)
        assert isinstance(character, (Character))
        assert character in faction.characters
        assert faction.leader == character
        m = Character(world=world, parent=world, name="test")
        m.save()
        character = faction.add_character(model=m, leader=False, generate=False)
        assert isinstance(character, (Character))
        assert character in faction.characters
        assert faction.leader != character
        m = Character(world=world, parent=world, name="testleader")
        m.save()
        character = faction.add_character(model=m, leader=True, generate=False)
        assert isinstance(character, (Character))
        assert character in faction.characters
        assert faction.leader == character
