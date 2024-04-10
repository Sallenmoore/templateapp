import pytest
import requests_mock
from models.character import Character
from models.item import Item
from models.user import User
from models.world import World

from autonomous import log


# @pytest.mark.skip("Working")
class TestCharacterAPI:
    def test_generate(self, user, world):
        character = Character.generate(parent=world, description="A Monk")
        # log(character)
        assert character.name
        assert character.description
        assert character.backstory != "Unknown"
        assert character.strength
        assert character.dexterity
        assert character.constitution
        assert character.intelligence
        assert character.wisdom
        assert character.charisma
        assert character.ac
        assert character.hitpoints
