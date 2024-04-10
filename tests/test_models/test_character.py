import pytest
from models.character import Character
from models.user import User


# @pytest.mark.skip("Working")
class TestCharacter:
    def test_init(self, user, world):
        character = Character(world=world, name="test")
        assert character.name is not None
        assert character.desc is not None
        assert character.backstory is not None

    def test_save(self, user, world):
        character = Character(world=world, name="test")
        assert character.save()
        assert character.name is not None
        assert character.desc is not None
        assert character.backstory is not None

        character = Character(world=world, name="test")
        assert character.save()
        assert character.name == "test"
        assert character.genre == "fantasy"
        assert character.backstory is not None

    def test_repr(self, user, world):
        character = Character(world=world, name="test")
        repr_string = repr(character)
        assert isinstance(repr_string, str)

    def test_parent(self, user, world):
        character = Character(world=world, name="test")
        assert character.parent is None

    def test_parent_setter(self, user, world):
        character = Character(world=world, name="test")
        with pytest.raises(TypeError):
            character.parent = "Not a TTRPGObject"

    def test_world(self, user, world):
        character = Character(world=world, name="test")
        assert character.world is not None

    def test_world_setter(self, user, world):
        character = Character(world=world, name="test")
        with pytest.raises(TypeError):
            character.world = "Not a World"

    def test_user(self, user, world):
        character = Character(world=world, name="test")
        assert character.user is not None

    def test_user_setter(self, user, world):
        character = Character(world=world, name="test")
        with pytest.raises(AttributeError):
            character.user = "Not a User"

    def test_genre(self, user, world):
        character = Character(world=world, name="test")
        assert character.genre == "fantasy"

    def test_genre_setter(self, user, world):
        character = Character(world=world, name="test")
        with pytest.raises(AttributeError):
            character.genre = 123

    def test_items(self, user, world):
        character = Character(world=world, name="test")
        assert character.items == []

    def test_items_setter(self, user, world):
        character = Character(world=world, name="test")
        with pytest.raises(TypeError):
            character.items = [1, 2, 3]

    def test_chat(self, user, world):
        character = Character(world=world, name="test")
        assert character.chats["history"] == []
        message = "Tell me a little more about your.."
        character.chat(message)
        assert character.chats["message"] == message
        assert character.chats["response"] is not None
        assert character.chats["summary"] is not None

    def test_build(self, user, world):
        character = Character.build(world)
        assert isinstance(character, Character)
        assert character.world == world
        assert character.traits is not None
        assert character.genre == world.genre
        assert character.hitpoints is not None
        assert character.items is not None

    def test_get_image_prompt(self, user, world):
        character = Character(world=world, name="test")
        # print(character.get_image_prompt())
        assert character.get_image_prompt()

    def test_page_data(self, user, world):
        character = Character(world=world, name="test")
        results = character.page_data()
        assert isinstance(results, dict)
        assert results["Goals"] is not None

    def test_update_image_url(self, user, world):
        obj = Character(world=world, name="test")
        url = "https://picsum.photos/300/?blur"
        result = obj.update_image_url(url)
        assert isinstance(result, str)
        assert obj.asset_id

    def test_image(self, user, world):
        obj = Character(world=world, name="test")
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
        obj = Character(world=world, name="test")
        obj.generate_image()
        assert obj.asset_id

    def test_is_owner(self, user, world):
        obj = Character(world=world, name="test")
        assert user.world_owner(obj)
        user = User(name="bad", email="bad@bad.com")
        user.save()
        assert not user.world_owner(obj)

    def test_slug(self, user, world):
        obj = Character(world=world, name="test object")
        assert obj.slug == "test-object"

    def test_backstory_summary(self, user, world):
        obj = Character(world=world, name="test")
        assert obj.backstory_summary

    def test_title(self, user, world):
        obj = Character(world=world, name="test")
        assert obj.title == "Character"

    def test_api_path(self, user, world):
        obj = Character(world=world, name="test")
        assert obj.api_path() == "/api/character"

    def test_page_path(self, user, world):
        obj = Character(world=world, name="test")
        assert obj.page_path().startswith("/character")
