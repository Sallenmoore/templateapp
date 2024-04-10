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

from flask import Blueprint, request

from models.user import User

from .index import _authenticate, _import_model

image_endpoint = Blueprint("image", __name__)


###########################################################
##                    Image Routes                       ##
###########################################################
@image_endpoint.route("/upload/<string:model>", methods=("POST",))
def image_upload(model):
    """
    ## Description
    Fetches the user and world object with the corresponding primary key.
    ## Parameters
    - *user* : (str)
      - Primary key of the user
    - *pk* : (str)
      - Primary key of the world object
    - *url* : (str)
      - URL of the image
    ## Return
    - str - Status of the update operation
    """
    result = {"results": "You do not have permission to alter this object"}
    if Model := _import_model(model):
        user = User.get(request.json.get("user"))
        obj = Model.get(request.json.get("pk"))
        if _authenticate(user, obj):
            result = {"results": obj.update_image_url(request.json.get("url"))}
    return result


@image_endpoint.route("/select/<string:model>", methods=("POST",))
def image_select(model):
    """
    ## Description
    Returns a list or random images from the genre's world object image list.
    ## Parameters
    - *user* : (str)
      - Primary key of the user
    - *pk* : (str)
      - Primary key of the world object
    ## Return
    - list - list of random images
    """
    result = {"results": "You do not have permission to alter this object"}
    if Model := _import_model(model):
        user = User.get(request.json.get("user"))
        obj = Model.get(request.json.get("pk"))
        if _authenticate(user, obj):
            result = {
                "results": obj.page_content(
                    user=user,
                    template="pages/_shared_components",
                    macro="image_gallery",
                )
            }
    return result


@image_endpoint.route("/battlemap/select/<string:model>", methods=("POST",))
def battlemap_random(model):
    """
    ## Description
    Returns a list of maps from the genre's world object map list.
    ## Parameters
    - *user* : (str)
      - Primary key of the user
    - *pk* : (str)
      - Primary key of the world object
    ## Return
    - list - list of random images
    """
    result = {"results": "You do not have permission to alter this object"}
    if Model := _import_model(model):
        user = User.get(request.json.get("user"))
        obj = Model.get(request.json.get("pk"))
        if _authenticate(user, obj):
            result = {
                "results": obj.page_content(
                    user=user, macro="image_gallery", images=obj.random_battlemap()
                )
            }
    return result


@image_endpoint.route("/battlemap/upload/<string:model>", methods=("POST",))
def battlemap_upload(model):
    """
    ## Description
    Pulls an image file from the supplied url, and sets it as the world's map.
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
    result = {"results": "You do not have permission to alter this object"}
    if Model := _import_model(model):
        user = User.get(request.json.get("user"))
        obj = Model.get(request.json.get("pk"))
        if _authenticate(user, obj):
            result = {"results": obj.upload_battlemap(request.json.get("map_url"))}
    return result
