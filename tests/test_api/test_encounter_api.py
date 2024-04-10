import pytest
import requests_mock
from autonomous.ai.agents.mockai import MockAIAgent
from autonomous.ai.autoteam import AutoTeam
from models.character import Character
from models.creature import Creature
from models.encounter import Encounter
from models.item import Item
from models.ttrpgobject import TTRPGObject

TTRPGObject._aiteam = AutoTeam(MockAIAgent)


# @pytest.mark.skip("Working")
class TestEncounter:
    pass
