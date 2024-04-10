import pytest
from models.character import Character
from models.poi import POI
from models.city import City
from models.encounter import Encounter
from models.faction import Faction
from models.user import User


# @pytest.mark.skip("Working")
class TestCity:
    def test_init(self, user, world):
        city = City(world=world, name="test")
        assert city.name is not None
        assert city.desc is not None
        assert city.backstory is not None

    def test_repr(self, user, world):
        city = City(world=world, name="test")
        repr_string = repr(city)
        assert isinstance(repr_string, str)

    def test_parent(self, user, world):
        city = City(world=world, name="test")
        assert city.parent is None

    def test_parent_setter(self, user, world):
        city = City(world=world, name="test")
        with pytest.raises(TypeError):
            city.parent = "Not a City"

    def test_world(self, user, world):
        city = City(world=world, name="test")
        assert city.world is not None

    def test_world_setter(self, user, world):
        city = City(world=world, name="test")
        with pytest.raises(TypeError):
            city.world = "Not a World"

    def test_user(self, user, world):
        city = City(world=world, name="test")
        assert city.user is not None

    def test_user_setter(self, user, world):
        city = City(world=world, name="test")
        with pytest.raises(AttributeError):
            city.user = "Not a User"

    def test_genre(self, user, world):
        city = City(world=world, name="test")
        assert city.genre == "fantasy"

    def test_genre_setter(self, user, world):
        city = City(world=world, name="test")
        with pytest.raises(AttributeError):
            city.genre = 123

    def test_get_image_prompt(self, user, world):
        city = City(world=world, name="test")
        # print(city.get_image_prompt())
        assert city.get_image_prompt()

    def test_build(self, user, world):
        city = City.build(world, description="A peaceful region")
        city.save()
        assert isinstance(city, City)
        assert city.world == world
        assert city.population is not None
        assert city.pois is not None

    def test_page_data(self, user, world):
        city = City(world=world, name="test")
        city.save()
        results = city.page_data()
        assert isinstance(results, dict)
        assert results["Population"] is not None

    def test_image(self, user, world):
        obj = City(world=world, name="test")
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
        obj = City(world=world, name="test")
        obj.save()
        obj.generate_image()
        assert obj.asset_id

    def test_is_owner(self, user, world):
        obj = City(world=world, name="test")
        obj.save()
        assert user.world_owner(obj)
        user = User(name="bad", email="bad@bad.com")
        user.save()
        assert not user.world_owner(obj)

    def test_slug(self, user, world):
        obj = City(world=world, name="test object")
        obj.save()
        assert obj.slug == "test-object"

    def test_backstory_summary(self, user, world):
        obj = City(world=world, name="test")
        obj.save()
        assert obj.backstory_summary

    def test_title(self, user, world):
        obj = City(world=world, name="test")
        obj.save()
        assert obj.title == "City"

    def test_api_path(self, user, world):
        obj = City(world=world, name="test")
        obj.save()
        assert obj.api_path() == "/api/city"

    def test_page_path(self, user, world):
        obj = City(world=world, name="test")
        obj.save()
        assert obj.page_path().startswith("/city")

    #### Specific to the Class ####

    def test_characters(self, user, world):
        city = City(world=world, name="test")
        city.save()
        character = Character(world=world, name="test")
        city.add_character(model=character)
        assert character in city.characters

    def test_pois(self, world):
        city = City(world=world, parent=world)
        city.save()
        city.pois = [
            POI(world=world, parent=city, district="district1"),
            POI(world=world, parent=city, district="district1"),
            POI(world=world, parent=city, district="district2"),
        ]

        pois = city.pois
        assert isinstance(pois, list)
        assert all(isinstance(loc, POI) for loc in pois)
        assert len(pois) == 3

    def test_districts(self, user, world):
        city = City(
            world=world,
            name="test",
        )
        city.save()
        a = POI(world=world, parent=city, district="district1")
        a.save()
        b = POI(world=world, parent=city, district="districtA")
        b.save()
        city.pois = [a, b]
        c = POI(world=world, parent=city, district="district2")
        c.save()
        city.pois += [c]
        assert isinstance(city.districts, list)
        assert len(city.districts) == 3
        assert "district1" in city.districts
        assert "district2" in city.districts

    def test_add_poi(self, user, world):
        city = City(world=world, name="test")
        city.save()
        poi = city.add_poi(generate=False)
        assert isinstance(poi, POI)
        assert poi in city.pois
        poi = city.add_poi(generate=True)
        assert isinstance(poi, POI)
        assert poi in city.pois

    def test_add_faction(self, user, world):
        city = City(world=world, name="test")
        city.save()
        faction = city.add_faction(generate=False)
        assert isinstance(faction, Faction)
        assert faction in city.factions
        faction = city.add_faction(generate=True)
        assert isinstance(faction, Faction)
        assert faction in city.factions

    def test_add_encounter(self, user, world):
        city = City(world=world, name="test")
        city.save()
        encounter = city.add_encounter(num_players=5, level=5, generate=False)
        assert isinstance(encounter, Encounter)
        assert encounter in city.encounters
        encounter = city.add_encounter(num_players=5, level=5, generate=True)
        assert isinstance(encounter, Encounter)
        assert encounter in city.encounters

    def test_add_character(self, user, world):
        city = City(world=world, name="test")
        city.save()
        citizen = city.add_character(generate=False)
        assert isinstance(citizen, Character)
        assert citizen in [
            character for poi in city.pois for character in poi.characters
        ]
        citizen = city.add_character(generate=True)
        assert isinstance(citizen, Character)
        assert citizen in [
            character for poi in city.pois for character in poi.characters
        ]
