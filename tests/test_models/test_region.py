import pytest
from models.city import City
from models.encounter import Encounter
from models.location import Location
from models.region import Region
from models.user import User


# @pytest.mark.skip("Working")
class TestRegion:
    def test_init(self, user, world):
        region = Region(world=world, name="test")
        assert region.name is not None
        assert region.desc is not None
        assert region.backstory is not None

    def test_repr(self, user, world):
        region = Region(world=world, name="test")
        repr_string = repr(region)
        assert isinstance(repr_string, str)

    def test_parent(self, user, world):
        region = Region(world=world, name="test")
        assert region.parent is None

    def test_parent_setter(self, user, world):
        region = Region(world=world, name="test")
        with pytest.raises(TypeError):
            region.parent = "Not a TTRPGObject"

    def test_world(self, user, world):
        region = Region(world=world, name="test")
        assert region.world is not None

    def test_world_setter(self, user, world):
        region = Region(world=world, name="test")
        with pytest.raises(TypeError):
            region.world = "Not a World"

    def test_user(self, user, world):
        region = Region(world=world, name="test")
        assert region.user is not None

    def test_user_setter(self, user, world):
        region = Region(world=world, name="test")
        with pytest.raises(AttributeError):
            region.user = "Not a User"

    def test_genre(self, user, world):
        region = Region(world=world, name="test")
        assert region.genre == "fantasy"

    def test_genre_setter(self, user, world):
        region = Region(world=world, name="test")
        with pytest.raises(AttributeError):
            region.genre = 123

    def test_delete(self, user, world):
        region = Region(world=world, name="test")
        region.delete()

        region = Region(world=world, name="test")
        assert region.save()
        pk = region.pk
        region.delete()
        assert not Region.get(pk)

    def test_get_image_prompt(self, user, world):
        region = Region(world=world, name="test")
        # print(region.get_image_prompt())
        assert region.get_image_prompt()

    def test_build(self, user, world):
        region = Region.build(world, description="A peaceful region")
        region.save()
        assert isinstance(region, Region)
        assert region.world == world

    def test_page_data(self, user, world):
        region = Region(world=world, name="test")
        region.save()
        results = region.page_data()
        assert isinstance(results, dict)
        assert results["Cities"] is not None

    def test_image(self, user, world):
        obj = Region(world=world, name="test")
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
        obj = Region(world=world, name="test")
        obj.save()
        obj.generate_image()
        assert obj.asset_id

    def test_is_owner(self, user, world):
        obj = Region(world=world, name="test")
        obj.save()
        assert user.world_owner(obj)
        user = User(name="bad", email="bad@bad.com")
        user.save()
        assert not user.world_owner(obj)

    def test_slug(self, user, world):
        obj = Region(world=world, name="test object")
        assert obj.slug == "test-object"

    def test_backstory_summary(self, user, world):
        obj = Region(world=world, name="test")
        assert obj.backstory_summary

    def test_title(self, user, world):
        obj = Region(world=world, name="test")
        assert obj.title == "Region"

    def test_api_path(self, user, world):
        obj = Region(world=world, name="test")
        assert obj.api_path() == "/api/region"

    def test_page_path(self, user, world):
        obj = Region(world=world, name="test")
        assert obj.page_path().startswith("/region")

    #### Specific to the Class ####

    def test_add_city(self, user, world):
        region = Region(world=world, name="test")
        region.save()
        city = region.add_city(generate=False)
        assert isinstance(city, City)
        assert city in region.cities
        city = region.add_city(generate=True)
        assert isinstance(city, City)
        assert city in region.cities

    def test_add_encounter(self, user, world):
        region = Region(world=world, name="test")
        region.save()
        encounter = region.add_encounter(num_players=5, level=5, generate=False)
        assert isinstance(encounter, Encounter)
        assert encounter in region.encounters
        encounter = region.add_encounter(num_players=5, level=5, generate=True)
        assert isinstance(encounter, Encounter)
        assert encounter in region.encounters

    def test_add_location(self, user, world):
        region = Region(world=world, name="test")
        region.save()
        item = region.add_location(generate=False)
        assert isinstance(item, Location)
        assert item in region.locations
        item = region.add_location(generate=True)
        assert isinstance(item, Location)
        assert item in region.locations
