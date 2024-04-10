import pytest
from models.creature import Creature
from models.user import User


# @pytest.mark.skip("Working")
class TestCreature:
    def test_init(self, user, world):
        creature = Creature(world=world, name="test")
        creature.save()
        assert creature.name is not None
        assert creature.desc is not None
        assert creature.backstory is not None

    def test_save(self, user, world):
        creature = Creature(world=world, name="test")
        creature.save()
        assert creature.save()
        assert creature.name is not None
        assert creature.desc is not None
        assert creature.backstory is not None

        creature = Creature(world=world, name="test")
        creature.save()
        assert creature.save()
        assert creature.name == "test"
        assert creature.genre == "fantasy"
        assert creature.backstory is not None

    def test_repr(self, user, world):
        creature = Creature(world=world, name="test")
        creature.save()
        repr_string = repr(creature)
        assert isinstance(repr_string, str)

    def test_parent(self, user, world):
        creature = Creature(world=world, name="test")
        creature.save()
        assert creature.parent is None

    def test_parent_setter(self, user, world):
        creature = Creature(world=world, name="test")
        creature.save()
        with pytest.raises(TypeError):
            creature.parent = "Not a TTRPGObject"

    def test_world(self, user, world):
        creature = Creature(world=world, name="test")
        creature.save()
        assert creature.world is not None

    def test_world_setter(self, user, world):
        creature = Creature(world=world, name="test")
        creature.save()
        with pytest.raises(TypeError):
            creature.world = "Not a World"

    def test_user(self, user, world):
        creature = Creature(world=world, name="test")
        creature.save()
        assert creature.user is not None

    def test_user_setter(self, user, world):
        creature = Creature(world=world, name="test")
        creature.save()
        with pytest.raises(AttributeError):
            creature.user = "Not a User"

    def test_genre(self, user, world):
        creature = Creature(world=world, name="test")
        creature.save()
        assert creature.genre == "fantasy"

    def test_genre_setter(self, user, world):
        creature = Creature(world=world, name="test")
        creature.save()
        with pytest.raises(AttributeError):
            creature.genre = 123

    def test_items(self, user, world):
        creature = Creature(world=world, name="test")
        creature.save()
        assert creature.genre == "fantasy"

    def test_items_setter(self, user, world):
        creature = Creature(world=world, name="test")
        creature.save()
        with pytest.raises(TypeError):
            creature.items = [1, 2, 3]

    def test_get_image_prompt(self, user, world):
        creature = Creature.build(world)
        # print(creature.get_image_prompt())
        assert creature.get_image_prompt()

    def test_page_data(self, user, world):
        creature = Creature(world=world, name="test")
        creature.save()
        results = creature.page_data()
        assert isinstance(results, dict)
        assert results["Details"] is not None

    # def test_update_image_url(self, user, world):
    #     obj = Creature(world=world, name="test")
    #     url = "https://picsum.photos/300/?blur"
    #     result = obj.update_image_url(url)
    #     assert isinstance(result, str)
    #     assert obj.asset_id

    def test_image(self, user, world):
        obj = Creature(world=world, name="test")
        obj.save()
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
        obj = Creature(world=world, name="test")
        obj.save()
        obj.generate_image()
        assert obj.asset_id

    def test_is_owner(self, user, world):
        obj = Creature(world=world, name="test")
        obj.save()
        assert user.world_owner(obj)
        user = User(name="bad", email="bad@bad.com")
        user.save()
        assert not user.world_owner(obj)

    def test_slug(self, user, world):
        obj = Creature(world=world, name="test object")
        obj.save()
        assert obj.slug == "test-object"

    def test_backstory_summary(self, user, world):
        obj = Creature(world=world, name="test")
        obj.save()
        assert obj.backstory_summary

    def test_title(self, user, world):
        obj = Creature(world=world, name="test")
        obj.save()
        assert obj.title == "Creature"

    def test_api_path(self, user, world):
        obj = Creature(world=world, name="test")
        obj.save()
        assert obj.api_path() == "/api/creature"

    def test_page_path(self, user, world):
        obj = Creature(world=world, name="test")
        obj.save()
        assert obj.page_path().startswith("/creature")
