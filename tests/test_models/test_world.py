import pytest
from models.region import Region
from models.ttrpgobject import TTRPGObject
from models.world import World

from autonomous.ai.agents.mockai import MockAIAgent
from autonomous.ai.autoteam import AutoTeam

TTRPGObject._aiteam = AutoTeam(MockAIAgent)


class TestWorld:
    def test_init(self, user, world):
        assert world.name is not None
        assert world.desc is not None
        assert world.backstory is not None

    def test_repr(self, user, world):
        repr_string = repr(world)
        assert isinstance(repr_string, str)

    def test_parent(self, user, world):
        assert world.parent is None

    def test_parent_setter(self, user, world):
        with pytest.raises(TypeError):
            world.parent = "Not a TTRPGObject"

    def test_world(self, user, world):
        assert world.world is None

    def test_world_setter(self, user, world):
        with pytest.raises(TypeError):
            world.world = world

    def test_user(self, user, world):
        assert world.user is not None

    def test_user_setter(self, user, world):
        with pytest.raises(TypeError):
            world.user = "Not a User"

    def test_genre(self, user, world):
        assert world.genre

    def test_genre_setter(self, user, world):
        with pytest.raises(AttributeError):
            world.genre = 123

    def test_delete(self, user, world):
        assert world.save()
        pk = world.pk
        world.delete()
        assert not World.get(pk)

    def test_get_image_prompt(self, user, world):
        # print(world.get_image_prompt())
        assert world.get_image_prompt()

    def test_page_data(self, user, world):
        results = world.page_data()
        assert isinstance(results, dict)
        assert results["Cities"] is not None

    #### Specific to the Class ####

    def test_add_region(self, user, world):
        region = world.add_region(generate=False)
        assert isinstance(region, Region)
        assert region in world.regions
        region = world.add_region(generate=True)
        assert isinstance(region, Region)
        assert region in world.regions
