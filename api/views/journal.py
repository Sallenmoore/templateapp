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

# external Modules

from datetime import datetime

from flask import Blueprint, get_template_attribute, request

from autonomous import log
from models.campaign import Campaign
from models.journal import JournalEntry
from models.user import User
from models.world import World

from .index import _authenticate, _import_model

journal_endpoint = Blueprint("journal", __name__)


@journal_endpoint.route("/entry/add", methods=("POST",))
def add_journal_entry():
    """
    ## Description
    Adds a new journal entry for the world object with the corresponding primary key.
    ## Parameters
    - *user* : (str)
      - Primary key of the user
    - *pk* : (str)
      - Primary key of the journal
    - *entry_pk* : (str)
      - Primary key of the journal entry
    - *title* : (str)
      - Title of the journal entry
    - *text* : (str)
      - Text of the journal entry
    - *tags* : (list)
      - Tags associated with the journal entry
    - *importance* : (int)
      - Importance level of the journal entry
    - *date* : (str)
      - Date of the journal entry
    ## Return
    - dict - Dictionary containing the details of the added journal entry
    """
    params = {"user": User.get(request.json.get("user"))}
    if Model := _import_model(request.json.get("model")):
        params["obj"] = Model.get(request.json.get("pk"))
        kwargs = {
            "title": request.json.get("name"),
            "text": request.json.get("text"),
            "importance": int(request.json.get("importance")),
            "associations": request.json.get("card"),
        }
        log(kwargs)
        if request.json.get("entry_pk"):
            params["obj"].journal.update_entry(
                pk=request.json.get("entry_pk"), **kwargs
            )
        else:
            params["obj"].journal.add_entry(**kwargs)
        return get_template_attribute("_components.html", "history")(**params)
    return "You do not have permission to alter this object"


@journal_endpoint.route("/entry/edit", methods=("POST",))
def edit_journal_entry():
    params = {"user": User.get(request.json.get("user"))}
    if Model := _import_model(request.json.get("model")):
        params["obj"] = Model.get(request.json.get("pk"))
        if _authenticate(**params):
            params["entry"] = params["obj"].journal.get_entry(
                request.json.get("entry_pk")
            )
            log(params["entry"].importance)
            return get_template_attribute("_components.html", "journal_new_entry")(
                **params
            )
    return "You do not have permission to alter this object"


@journal_endpoint.route("/entry/delete", methods=("POST",))
def journal_entry_delete():
    """
    ## Description
    Deletes the world object's journal entry based on the provided primary keys.
    ## Parameters
    - *user* : (str)
      - Primary key of the user
    - *pk* : (str)
      - Primary key of the world object
    - *entry_pk* (str)
      - Primary key of the journal entry
    ## Return
    - (str,)
      - Status of the deletion operation
    """
    params = {"user": User.get(request.json.get("user"))}
    if Model := _import_model(request.json.get("model")):
        params["obj"] = Model.get(request.json.get("pk"))
        if _authenticate(**params):
            entry = params["obj"].journal.get_entry(request.json.get("entry_pk"))
            if entry:
                params["obj"].journal.entries.remove(entry)
                params["obj"].journal.save()
                entry.delete()
                return "success"
    return "You do not have permission to alter this object"
