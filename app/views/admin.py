# Built-In Modules
import os
import shutil

# external Modules
from flask import Blueprint, get_template_attribute, render_template, request

from autonomous import log
from autonomous.auth import AutoAuth, auth_required
from models.campaign import Campaign
from models.character import Character
from models.city import City
from models.creature import Creature
from models.encounter import Encounter
from models.faction import Faction
from models.item import Item
from models.journal import Journal, JournalEntry
from models.location import Location
from models.poi import POI
from models.region import Region
from models.user import User
from models.world import World

admin_page = Blueprint("admin", __name__)


@admin_page.route("/", methods=("GET",))
@auth_required()  # admin=True)
def index():
    return render_template("admin.html", context={"user": AutoAuth.current_user().pk})


@admin_page.route("/manage/images", methods=("POST",))
@auth_required()
def images():
    base_path = "static/images/tabletop/"
    images = {}
    for genre in os.listdir(base_path):
        images[genre] = []
        folder_path = os.path.join(base_path, genre)
        for root, dirs, files in os.walk(folder_path):
            files = sorted(
                files, key=lambda file: os.path.getsize(os.path.join(root, file))
            )
            for file in files:
                if file.endswith(".webp"):
                    url_path = f"/{root}/orig.webp"
                    if url_path not in images[genre]:
                        images[genre].append(url_path)

    return get_template_attribute("admin/_images.html", "manage")(images=images)


@admin_page.route("/manage/image/delete", methods=("POST",))
@auth_required()  # admin=True)
def delete_image():
    image_path = request.json.get("image").rsplit("/")
    image_path = "static/images/" + ("/".join(image_path[3:-1]))
    log(image_path)
    if os.path.exists(image_path):
        shutil.rmtree(image_path)
        return "Success"
    return "File not found"


@admin_page.route("/manage/users", methods=("POST",))
@auth_required()
def users():
    return get_template_attribute("admin/_users.html", "manage")(users=User.all())


@admin_page.route("/manage/users/role", methods=("POST",))
@auth_required()  # admin=True)
def role_user():
    log(request.json)
    if user := User.get(request.json.get("user")):
        user.role = request.json.get("role")
        user.save()
        return "Success"
    return "User not found"


@admin_page.route("/manage/users/delete", methods=("POST",))
@auth_required()  # admin=True)
def delete_user():
    if user := User.get(request.json.get("user")):
        user.delete()
        return "Success"
    return "User not found"


@admin_page.route("/manage/worlds", methods=("POST",))
@auth_required()
def worlds():
    return get_template_attribute("admin/_worlds.html", "manage")(worlds=World.all())


@admin_page.route("/manage/users/delete", methods=("POST",))
@auth_required()  # admin=True)
def delete_world():
    if world := World.get(request.json.get("world")):
        world.delete()
        return "Success"
    return "World not found"


@admin_page.route("/migration", methods=("POST",))
@auth_required()  # admin=True)
def migration():
    log("starting migration...")
    results = []
    models = {
        "world": World,
        "region": Region,
        "city": City,
        "location": Location,
        "encounter": Encounter,
        "poi": POI,
        "faction": Faction,
        "creature": Creature,
        "item": Item,
        "character": Character,
    }
    # for model in models.values():
    #     log(f"migrating {model.model_name()}...")
    #     for obj in model.all():
    #         if obj.parent and obj not in obj.parent.children:
    #             log(f"unlinking {obj.name} from {obj.parent.name}...")
    #             obj.parent = None
    #             obj.save()
    #         if obj.journal:
    #             log(f"updating {obj.name} journal parent...")
    #             obj.journal.parent = obj
    #             obj.journal.world = obj.get_world()
    #             obj.journal.save()
    #     log(f"...{model.model_name()} migration complete")
    log("...migration complete")

    return results


@admin_page.route("/dbdump", methods=("GET",))
# @auth_required()  # admin=True)
def dbdump():
    log("starting dump...")
    World.table().dbdump()
    return f"<p>Success</p>"


@admin_page.route("/dbload", methods=("GET",))
# @auth_required()  # admin=True)
def dbload():
    log("starting load...")

    User.table().flush_table()
    Journal.table().flush_table()
    Campaign.table().flush_table()
    JournalEntry.table().flush_table()
    Item.table().flush_table()
    Character.table().flush_table()
    Creature.table().flush_table()
    Faction.table().flush_table()
    POI.table().flush_table()
    Encounter.table().flush_table()
    Location.table().flush_table()
    City.table().flush_table()
    Region.table().flush_table()
    World.table().flush_table()
    World.table().dbload()
    return f"<p>Success</p>"
