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

from datetime import datetime

from flask import Blueprint, get_template_attribute, request
from views import components

from autonomous import log
from models.campaign import Campaign
from models.journal import JournalEntry
from models.user import User
from models.world import World

from .index import _authenticate, _import_model

world_endpoint = Blueprint("world", __name__)


###########################################################
##                    World Routes                       ##
###########################################################
@world_endpoint.route("/build", methods=("POST",))
def build():
    """
    Description: Adds a new subuser to the world if the user is authenticated.
    Parameters:
      - pk: Primary key of the world
      - user: Primary key of the user
      - new_user: Email of the new user to be added
    Returns:
      - A message indicating the result of the operation
    """
    if user := User.get(request.json.get("user")):
        World.build(
            system=request.json.get("system"),
            user=user,
            name=request.json.get("name"),
            desc=request.json.get("desc"),
            backstory=request.json.get("backstory"),
        )
        return get_template_attribute("_components.html", "worlds")(user)
    return {"results": "You do not have permission to alter this object"}


@world_endpoint.route("/delete", methods=("POST",))
def delete():
    obj = World.get(request.json.get("pk"))
    user = User.get(request.json.get("user"))
    if _authenticate(user, obj):
        obj.delete()
        return "success"
    return "You do not have permission to alter this object"


@world_endpoint.route("/user/add", methods=("POST",))
def user_add():
    """
    Description: Adds a new subuser to the world if the user is authenticated.
    Parameters:
      - pk: Primary key of the world
      - user: Primary key of the user
      - new_user: Email of the new user to be added
    Returns:
      - A message indicating the result of the operation
    """
    log(request.json)
    obj = World.get(request.json.get("pk"))
    user = User.get(request.json.get("user"))
    if _authenticate(user, obj):
        log(request.json.get("new_user"))
        if new_user := User.find(email=request.json.get("new_user").strip()):
            if new_user not in obj.subusers:
                obj.subusers.append(new_user)
                obj.save()
                log(f"User {new_user.email} added to World {obj.name}")
            else:
                log("User already added to world")

            if obj.pk not in new_user.world_pks:
                new_user.world_pks.append(obj.pk)
                new_user.save()
            else:
                log("World already added to user")

        return get_template_attribute("pages/_world.html", "manage_users")(user, obj)
    return "You do not have permission to alter this object"


@world_endpoint.route("/calendar/update", methods=("POST",))
def calendar_update():
    world = World.get(request.json.get("pk"))
    result = {}
    # log(request.json)
    updates = {
        "year_string": request.json.get("year_string"),
        "month_names": request.json.get("months"),
        "day_names": request.json.get("days"),
        "days_per_year": int(request.json.get("num_days_per_year")),
        "current_date": {
            "day": request.json.get("day", 0),
            "month": request.json.get("month", 0),
            "year": request.json.get("year", 0),
        },
    }
    # log(updates)
    world.system.set_calendar(**updates)
    # log(world.system.calendar)
    return {"results": result}


@world_endpoint.route("/timeline", methods=("POST",))
def timeline():
    user = User.get(request.json.get("user"))
    obj = World.get(request.json.get("pk"))
    filters = {
        "type": request.json.get("type_filter"),
        "time": request.json.get("time_filter", 0),
    }
    log(filters, request.json)
    timeline = obj.get_timeline(filter=filters)
    log(len(timeline))
    return get_template_attribute("pages/_world.html", "timeline")(
        user=user, obj=obj, timeline=timeline, filters=filters
    )


################# Campaigns #################


@world_endpoint.route("/campaign/add", methods=("POST",))
def add_campaign():
    user = User.get(request.json.get("user"))
    obj = World.get(request.json.get("pk"))
    if _authenticate(user, obj):
        entry = obj.add_campaign(
            name=request.json.get("name"),
            description=request.json.get("description"),
        )
        return {"results": entry.serialize()}
    return {"results": "You do not have permission to alter this object"}


@world_endpoint.route("/campaign/delete", methods=("POST",))
def delete_campaign():
    user = User.get(request.json.get("user"))
    obj = Campaign.get(request.json.get("pk"))
    if _authenticate(user, obj.world):
        obj.world.campaigns.remove(obj)
        obj.world.save()
        obj.delete()
        return {"results": "success"}
    return {"results": "You do not have permission to alter this object"}


@world_endpoint.route("/campaign/sessions", methods=("POST",))
def campaign_sessions():
    user = User.get(request.json.get("user"))
    if Model := _import_model(request.json.get("model")):
        obj = Model.get(request.json.get("pk"))
        campaign = Campaign.get(request.json.get("campaign_pk"))
        obj.current_campaign = campaign
        obj.save()
        params = {"user": user, "obj": obj}
        return get_template_attribute("pages/_world.html", "campaigns")(**params)
    return "You do not have permission to alter this object"


@world_endpoint.route("/campaign/session/add", methods=("POST",))
def add_session_entry():
    user = User.get(request.json.get("user"))
    if Model := _import_model(request.json.get("model")):
        obj = Model.get(request.json.get("pk"))
        if _authenticate(user, obj):
            campaign = Campaign.get(request.json.get("campaign_pk"))
            campaign.update_session(
                pk=request.json.get("session_pk"),
                title=request.json.get("name"),
                importance=request.json.get("importance"),
                text=request.json.get("text"),
                date=request.json.get("date"),
                associations=request.json.get("card"),
            )
            params = {"user": user, "obj": obj}
            return get_template_attribute("pages/_world.html", "campaigns")(**params)
    return "You do not have permission to alter this object"


@world_endpoint.route("/session/add/autocomplete", methods=("POST",))
def session_autocomplete_dropdown():
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

    return get_template_attribute("pages/_world.html", "session_autocomplete_dropdown")(
        **params
    )


@world_endpoint.route("/campaign/session/edit", methods=("POST",))
def edit_session_entry():
    user = User.get(request.json.get("user"))
    if Model := _import_model(request.json.get("model")):
        obj = Model.get(request.json.get("pk"))
        if _authenticate(user, obj):
            entry = JournalEntry.get(request.json.get("session_pk"))
            # log(entry, request.json)
            return get_template_attribute("pages/_world.html", "campaign_new_session")(
                user=user, obj=obj, entry=entry
            )
    return "You do not have permission to alter this object"


@world_endpoint.route("/campaign/session/delete", methods=("POST",))
def delete_session_entry():
    user = User.get(request.json.get("user"))
    if Model := _import_model(request.json.get("model")):
        obj = Model.get(request.json.get("pk"))
        if _authenticate(user, obj):
            session = JournalEntry.get(request.json.get("session_pk"))
            campaign = Campaign.get(request.json.get("campaign_pk"))
            try:
                campaign._sessions.entries.remove(session)
            except Exception as e:
                return f"{e}: Session not found"
            else:
                campaign._sessions.save()
                session.delete()
                return "success"
    return {"results": "You do not have permission to alter this object"}
