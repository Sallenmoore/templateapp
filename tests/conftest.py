import os
import sys

import pytest
from models.character import Character
from models.city import City
from models.creature import Creature
from models.encounter import Encounter
from models.faction import Faction
from models.item import Item
from models.location import Location
from models.region import Region
from models.user import User
from models.world import World

from app import create_app

# Add the 'app' directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture()
def app():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
        }
    )

    # other setup can go here

    yield app

    # clean up / reset resources here


# can make client.get() and client.post() requests to the applications
@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def user():
    user = User(name="test", email="email@test")
    user.save()
    yield user


@pytest.fixture()
def world(user):
    world = World(user=user, system="fantasy", name="MagicWorld")
    world.save()
    # breakpoint()
    yield world
    world.delete()


@pytest.fixture()
def scifiworld(user):
    world = World(user=user, system="sci-fi", name="TechWorld")
    world.save()
    yield world


@pytest.fixture()
def horrorworld(user):
    world = World(user=user, system="horror", name="ScaryWorld")
    world.save()
    yield world


@pytest.fixture()
def hardboiledworld(user):
    world = World(user=user, system="hardboiled", name="MysteryWorld")
    world.save()
    yield world


@pytest.fixture()
def postapocolypticworld(user):
    world = World(user=user, system="postapocolytic", name="EndWorld")
    world.save()
    yield world


@pytest.fixture()
def historicalworld(user):
    world = World(user=user, system="historical", name="HistoryWorld")
    world.save()
    yield world


@pytest.fixture()
def region(world):
    obj = Region(world=world, name="TestRegion")
    obj.parent = world
    obj.save()
    yield obj


@pytest.fixture()
def location(world, region):
    obj = Location(parent=world, name="TestLocation")
    obj.parent = region
    obj.save()
    yield obj


@pytest.fixture()
def encounter(world, region):
    obj = Encounter(world=world, name="TestEncounter")
    obj.parent = region
    obj.save()
    yield obj


@pytest.fixture()
def faction(world, region):
    obj = Faction(world=world, name="TestFaction")
    obj.parent = region
    obj.save()
    yield obj


@pytest.fixture()
def city(world, region):
    obj = City(world=world, name="TestCity")
    obj.parent = region
    obj.save()
    yield obj


@pytest.fixture()
def creature(world, encounter):
    obj = Creature(world=world, name="TestCreature")
    obj.parent = encounter
    obj.save()
    yield obj


@pytest.fixture()
def character(world, location):
    obj = Character(world=world, name="TestCharacter")
    obj.parent = location
    obj.save()
    yield obj


@pytest.fixture()
def item(world, encounter):
    obj = Item(world=world, name="TestItem")
    obj.parent = encounter
    obj.save()
    yield obj
