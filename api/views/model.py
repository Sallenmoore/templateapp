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

from .index import _authenticate, _import_model

model_endpoint = Blueprint("model", __name__)

models = {
    "player": "Character",
    "player_faction": "Faction",
    "poi": "POI",
}  # add model names that cannot just be be titlecased from lower case, such as POI or 'player':Character


###########################################################
##                    Model Routes                       ##
###########################################################
@model_endpoint.route("/<string:model>", methods=("POST",))
def index(model):
    """
    ## Description
    Fetches the world object and user based on the provided primary keys and returns the object.
    ## Parameters
    - *pk* : (str,)
      -  Primary key of the world object
    - *user* : (str,)
      -  Primary key of the user
    ## Return
    - (str,)
        - Index of the world object
    """
    if Model := _import_model(model):
        obj = Model.get(request.json.get("pk"))
        user = User.get(request.json.get("user"))
        if _authenticate(user, obj):
            return obj.state_data
    return {}


@model_endpoint.route("/add/<string:childmodel>", methods=("POST",))
def add(childmodel):
    """
    ## Description
    Adds a new faction to the world object with the provided description.
    ## Parameters
    - *pk* : (str)
      - Primary key of the world object
    - *user* : (str)
      - Primary key of the user
    - *description* : (str)
      - *Optional* - Description of the new faction
    ## Return
    - dict - Dictionary containing the primary key and API path of the new faction
    """
    user = User.get(request.json.pop("user"))
    parent = _import_model(request.json.get("model")).get(request.json.get("pk"))
    if _authenticate(user, parent):
        if ChildModel := _import_model(childmodel):
            child = ChildModel(world=parent.get_world(), parent=None)
            child.save()
            if childmodel == "character" and child.is_player:
                childmodel = "player"
            params = {"user": user, "obj": child, "childmodel": childmodel}
            return get_template_attribute("_components.html", "childmanage")(**params)
    return ""


@model_endpoint.route("/copy/<string:childmodel>", methods=("POST",))
def copy(childmodel):
    """
    ## Description
    Adds a new faction to the world object with the provided description.
    ## Parameters
    - *pk* : (str)
      - Primary key of the world object
    - *user* : (str)
      - Primary key of the user
    - *description* : (str)
      - *Optional* - Description of the new faction
    ## Return
    - dict - Dictionary containing the primary key and API path of the new faction
    """
    user = User.get(request.json.get("user"))
    obj = _import_model(request.json.get("model")).get(request.json.get("pk"))
    if _authenticate(user, obj):
        if ChildModel := _import_model(childmodel):
            child = ChildModel.get(request.json.get("child_pk"))
            child.copy()
            if childmodel == "character" and child.is_player:
                childmodel = "player"
            params = {
                "user": user,
                "obj": obj,
                "childmodel": childmodel,
            }
            return get_template_attribute("_components.html", "childmanage")(**params)
    return {"results": "You do not have permission to alter this object"}


@model_endpoint.route("/update", methods=("POST",))
def update(attr=None):
    """
    ## Description
    Updates the the attribute for the world object with the corresponding primary keys with the provided value.
    ## Parameters
      - *user* : (str,)
        - Primary key of the user
      - *pk* : (str,)
        - Primary key of the world object
      - *attr* : (str,)
        - Attribute to be updated, list or dictionary attributes should be named according to key/index `attr[n]`
      - *value* : (str,)
        - New value for the attribute
    ## Return
      - (str,)
        - Updated attribute of the world object
    """
    if Model := _import_model(request.json.pop("model", None)):
        user = User.get(request.json.pop("user", None))
        obj = Model.get(request.json.pop("pk", None))
        if _authenticate(user, obj):
            request.json.pop("world", None)
            request.json.pop("title", "")
            macro = request.json.pop("macro", "history")
            module = request.json.pop("module", "_components.html")
            for attr, value in request.json.items():
                if (
                    getattr(obj.__class__, attr, None)
                    and getattr(obj.__class__, attr).fset
                ):
                    getattr(obj.__class__, attr).fset(obj, value)
                elif attr in obj.attributes:
                    setattr(obj, attr, value)
                else:
                    log(
                        f"Attribute or property for {obj.model_name()} not found: {attr}"
                    )
            obj.save()
            context = get_template_attribute(module, macro)(user, obj)
            return context

    return "You do not have permission to alter this object"


@model_endpoint.route("/assign/<string:child_model>", methods=("POST",))
def assign(child_model):
    """
    ## Description
    Assigns the child object to the World based on the path:
    - assign/location
    - assign/city
    - assign/encounter
    - assign/faction
    ## Parameters
      - *user* : (str,)
        - Primary key of the user
      - *pk* : (str,)
        - Primary key of the world object
      - *child_pk* : (str,)
        - Primary key of the child to be assigned
    ## Return
      - (list,)
        - List of assigned children
    """
    user = User.get(request.json.pop("user"))
    if Parent := _import_model(request.json.pop("model")):
        parent = Parent.get(request.json.pop("pk"))
        if _authenticate(user, parent):
            Child = _import_model(child_model)
            child = Child.get(request.json.pop("child_pk"))
            child.parent = parent
            child.save()
            log(f"Assigning {child_model} to {child.child_key} of {parent.name}")
            getattr(parent, child.child_key).append(child)
            parent.save()

            if child_model == "character" and child.is_player:
                child_model = "player"

            params = {"user": user, "obj": parent, "model": child_model}
            return get_template_attribute("_components.html", "childpanel")(**params)
    return "You do not have permission to alter this object"


@model_endpoint.route("/remove/<string:childmodel>", methods=("POST",))
def remove(childmodel):
    """
    ## Description
    Unassigns the faction with the provided primary key from the world object.
    ## Parameters
    - *user* : (str)
      - Primary key of the user
    - *pk* : (str)
      - Primary key of the object to be unassigned
    ## Return
    - dict - Dictionary containing the primary key and API path of the unassigned object
    """
    user = User.get(request.json.get("user"))
    if ChildModel := _import_model(childmodel):
        child = ChildModel.get(request.json.get("child_pk"))
        if _authenticate(user, child) and child.parent:
            parent = child.parent
            if childmodel == "character" and child.is_player:
                childmodel = "player"
            log(f"Removing {child.name} from {parent.name}: {type(child.parent)}")
            child.emancipate()
            obj = _import_model(request.json.get("model")).get(request.json.get("pk"))
            params = {"user": user, "obj": obj, "model": childmodel}
            return get_template_attribute("_components.html", "childpanel")(**params)
    return "You do not have permission to alter this object"


@model_endpoint.route("/delete/<string:childmodel>", methods=("POST",))
def delete(childmodel):
    parent = _import_model(request.json.get("model")).get(request.json.get("pk"))
    if Model := _import_model(childmodel):
        user = User.get(request.json.get("user"))
        obj = Model.get(request.json.get("child_pk"))
        if _authenticate(user, obj):
            log(f"Deleting object {obj.name}")
            if childmodel == "character" and obj.is_player:
                childmodel = "player"
            obj.delete()
            return ""
    return "You do not have permission to alter this object"


@model_endpoint.route("/associate/<string:child_model>", methods=("POST",))
def associate(child_model):
    user = User.get(request.json.pop("user"))
    if Parent := _import_model(request.json.pop("model")):
        parent = Parent.get(request.json.pop("pk"))
        if _authenticate(user, parent):
            if Child := _import_model(child_model):
                child = Child.get(request.json.pop("child_pk"))
                if child not in parent.associations:
                    parent.associations.append(child)
                    parent.save()
            params = {"user": user, "obj": parent}
            return get_template_attribute("_components.html", "associations")(**params)
    return "You do not have permission to alter this object"


@model_endpoint.route("/unassociate/<string:child_model>", methods=("POST",))
def unassociate(parent_model, child_model):
    user = User.get(request.json.pop("user"))
    if Parent := _import_model(parent_model):
        parent = Parent.get(request.json.pop("pk"))
        if _authenticate(user, parent):
            if Child := _import_model(child_model):
                child = Child.get(request.json.pop("child_pk"))
                if child in parent.associations:
                    parent.associations.remove(child)
                    parent.save()
            params = {"user": user, "obj": parent}
            return get_template_attribute("_components.html", "associations")(**params)
    return {"results": "You do not have permission to alter this object"}


@model_endpoint.route("/character/chat/clear", methods=("POST",))
def chat():
    user = User.get(request.json.pop("user"))
    if Model := _import_model(request.json.pop("model")):
        obj = Model.get(request.json.pop("pk"))
        obj.clear_chat()
        params = {"user": user, "obj": obj}
        return get_template_attribute("pages/_character.html", "chats")(**params)
    return "You do not have permission to alter this object"
