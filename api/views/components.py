"""
# Components API Documentation

## Components Endpoints

"""

from flask import Blueprint, get_template_attribute, request

from autonomous import log
from models.campaign import Campaign
from models.user import User
from models.world import World

from .index import _import_model

components_endpoint = Blueprint("components", __name__)


###########################################################
##                    Component Routes                   ##
###########################################################


@components_endpoint.route("/autocomplete", methods=("POST",))
def autocomplete_dropdown():
    """
    ## Description
    - Fetches the card of the object based on the provided primary key.
    ## Parameters:
    - pk : (str,)
      - Primary key of the world
    - user: (str,)
      - Primary key of the user
    ## Return:
    - The card html of the world object
    """
    obj = World.get(request.json.get("world"))
    user = User.get(request.json.get("user"))
    params = {"objs": [], "user": user}
    query = request.json.get("query")
    if len(query) > 2:
        for key, objs in obj.search_autocomplete(query=query).items():
            for o in objs:
                if o not in params["objs"]:
                    params["objs"].append(o)
    macro = request.json.get("macro", "autocomplete_dropdown")
    module = request.json.get("module", "_components.html")
    snippet = get_template_attribute(module, macro)(**params)
    # log(query, len(params["objs"]), snippet)
    return snippet


@components_endpoint.route(
    "/nav/sidemenu_subitems/<string:childmodel>", methods=("POST",)
)
def sidemenu_subitem(childmodel):
    if Model := _import_model(request.json.get("model")):
        obj = Model.get(request.json.get("pk"))
        if children := obj.get_children(childmodel):
            params = {"children": children}
            return get_template_attribute("_nav.html", "sidemenu_subitems")(**params)
    return {}


@components_endpoint.route("/page/<string:macro>", methods=("POST",))
def page(macro):
    params = {"user": User.get(request.json.get("user"))}
    modelstr = request.json.get("model")
    if Model := _import_model(modelstr):
        params["obj"] = Model.get(request.json.get("pk"))
    if macro:
        return get_template_attribute(f"pages/_{modelstr}.html", macro)(**params)
    return {}


@components_endpoint.route("/childpanel/manage/<string:childmodel>", methods=("POST",))
def childpanelmanage(childmodel):
    user = User.get(request.json.get("user"))
    if Model := _import_model(request.json.get("model")):
        obj = Model.get(request.json.get("pk"))
        params = {"childmodel": childmodel, "user": user, "obj": obj}
        return get_template_attribute("_components.html", "childmanage")(**params)
    return ""


@components_endpoint.route("/childpanel/<string:childmodel>", methods=("POST",))
def childpanel(childmodel):
    log(childmodel)
    user = User.get(request.json.get("user"))
    if Model := _import_model(request.json.get("model")):
        obj = Model.get(request.json.get("pk"))
        params = {"model": childmodel, "user": user, "obj": obj}
        return get_template_attribute("_components.html", "childpanel")(**params)
    return ""


@components_endpoint.route("/texteditor/<string:attr>", methods=("POST",))
def texteditor(attr):
    user = User.get(request.json.get("user"))
    if Model := _import_model(request.json.get("model")):
        obj = Model.get(request.json.get("pk"))
        if isinstance(getattr(obj, attr, None), list):
            macro = "texteditor_list"
        else:
            macro = "texteditor"
        params = {"attr": attr, "user": user, "obj": obj}
        return get_template_attribute("_components.html", macro)(**params)
    return ""


@components_endpoint.route("<string:module>/<string:macro>", methods=("POST",))
def modulemacro(module, macro):
    params = {"user": User.get(request.json.get("user"))}
    if Model := _import_model(request.json.get("model")):
        params["obj"] = Model.get(request.json.get("pk"))
    if macro:
        return get_template_attribute(f"_{module}.html", macro)(**params)
    return {}


@components_endpoint.route("/<string:macro>", methods=("POST",))
def component(macro):
    params = {"user": User.get(request.json.get("user"))}
    if Model := _import_model(request.json.get("model")):
        params["obj"] = Model.get(request.json.get("pk"))
    if macro:
        return get_template_attribute("_components.html", macro)(**params)
    return {}
