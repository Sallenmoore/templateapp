import pytest
from models.item import Item
from models.ttrpgobject import TTRPGObject
from models.user import User

from autonomous.ai.agents.mockai import MockAIAgent
from autonomous.ai.autoteam import AutoTeam


# @pytest.mark.skip("Working")
class TestItem:
    def test_init(self, user, world):
        item = Item(world=world, name="test")
        assert item.name is not None
        assert item.desc is not None
        assert item.backstory is not None

    def test_repr(self, user, world):
        item = Item(world=world, name="test")
        repr_string = repr(item)
        assert isinstance(repr_string, str)

    def test_parent(self, user, world):
        item = Item(world=world, name="test")
        assert item.parent is None

    def test_parent_setter(self, user, world):
        item = Item(world=world, name="test")
        with pytest.raises(TypeError):
            item.parent = "Not a TTRPGObject"

    def test_world(self, user, world):
        item = Item(world=world, name="test")
        assert item.world is not None

    def test_world_setter(self, user, world):
        item = Item(world=world, name="test")
        with pytest.raises(TypeError):
            item.world = "Not a World"

    def test_user(self, user, world):
        item = Item(world=world, name="test")
        assert item.user is not None

    def test_user_setter(self, user, world):
        item = Item(world=world, name="test")
        with pytest.raises(AttributeError):
            item.user = "Not a User"

    def test_genre(self, user, world):
        item = Item(world=world, name="test")
        assert item.genre == "fantasy"

    def test_genre_setter(self, user, world):
        item = Item(world=world, name="test")
        with pytest.raises(AttributeError):
            item.genre = 123

    def test_delete(self, user, world):
        item = Item(world=world, name="test")
        assert item.save()
        pk = item.pk
        item.delete()
        assert not Item.get(pk)

    def test_get_image_prompt(self, user, world):
        item = Item(world=world, name="test")
        # print(item.get_image_prompt())
        assert item.get_image_prompt()

    def test_generate(self, user, world):
        item = Item.generate(parent=world, description="A peaceful item")
        assert isinstance(item, Item)
        assert item.world == world
        assert item.genre == world.genre

    def test_build(self, user, world):
        item = Item.build(world, description="A peaceful item")
        assert isinstance(item, Item)
        assert item.world == world

    def test_page_data(self, user, world):
        item = Item(world=world, name="test")
        results = item.page_data()
        assert isinstance(results, dict)
        assert results["Details"] is not None


    def test_image(self, user, world):
        obj = Item(world=world, name="test")
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
        obj = Item(world=world, name="test")
        obj.generate_image()
        assert obj.asset_id

    def test_is_owner(self, user, world):
        obj = Item(world=world, name="test")
        assert user.world_owner(obj)
        user = User(name="bad", email="bad@bad.com")
        user.save()
        assert not user.world_owner(obj)

    def test_slug(self, user, world):
        obj = Item(world=world, name="test object")
        assert obj.slug == "test-object"

    def test_backstory_summary(self, user, world):
        obj = Item(world=world, name="test")
        assert obj.backstory_summary

    def test_title(self, user, world):
        obj = Item(world=world, name="test")
        assert obj.title == "Item"

    def test_api_path(self, user, world):
        obj = Item(world=world, name="test")
        assert obj.api_path() == "/api/item"

    def test_page_path(self, user, world):
        obj = Item(world=world, name="test")
        assert obj.page_path().startswith("/item")
