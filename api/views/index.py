r"""
## Endpoints
"""

from flask import Blueprint, get_template_attribute, request

from autonomous import AutoModel, log
from models.user import User
from models.world import World

index_endpoint = Blueprint("index", __name__)


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


@index_endpoint.route("<string:module>/<string:macro>", methods=("POST",))
def components(module, macro):
    params = {"user": User.get(request.json.get("user"))}
    if Model := AutoModel.load_model(request.json.get("model")):
        params["obj"] = Model.get(request.json.get("pk"))
    if macro:
        return get_template_attribute(f"{module}.html", macro)(**params)
    return {}
