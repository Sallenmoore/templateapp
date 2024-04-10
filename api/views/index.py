r"""
# World API Documentation

## World Endpoints

### Model Structure

- name: "",
- backstory: "",
- desc: "",
- traits: [str],
- notes: [str],
- campaigns: [Campaign],
- regions: [`Region`],
- players: [`Character`],
- player_faction: `Faction`,

"""

from flask import Blueprint, get_template_attribute, request

from autonomous import AutoModel, log
from models.user import User
from models.world import World

index_endpoint = Blueprint("index", __name__)

models = {
    "player": "Character",
    "player_faction": "Faction",
    "poi": "POI",
}  # add model names that cannot just be be titlecased from lower case, such as POI or 'player':Character


def _import_model(model):
    if model:
        model_name = models.get(model, model.title())
        if Model := AutoModel.load_model(model_name):
            return Model
    return None


def _authenticate(user, obj):
    if obj.world:
        user = obj.world.user
    elif isinstance(obj, World):
        user = obj.user

    if user == user:
        return True
    elif obj.world in user.worlds:
        return True
    return False