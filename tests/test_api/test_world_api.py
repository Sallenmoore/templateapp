# import pytest
# from views.world import *


# class TestWorld:

#     def index():
#         return _index(World.get(request.json.get("pk")), User.get(request.json.get("user")))

#     def content():
#         return _content(
#             World.get(request.json.get("pk")),
#             User.get(request.json.get("user")),
#             content=request.json.get("content"),
#         )

#     def user_add():
#         log(request.json)
#         obj = World.get(request.json.get("pk"))
#         user = User.get(request.json.get("user"))
#         if _authenticate(user, obj):
#             results = "User not found"
#             log(request.json.get("new_user"))
#             if new_user := User.find(email=request.json.get("new_user").strip()):
#                 if new_user not in obj.subusers:
#                     obj.subusers.append(new_user)
#                     obj.save()
#                     log(f"User {new_user.email} added to World {obj.name}")
#                 else:
#                     log("User already added to world")
#                 if obj.pk not in new_user.world_pks:
#                     new_user.world_pks.append(obj.pk)
#                     new_user.save()
#                     results = f"World {obj.name} added to User {new_user.email}"
#                     log(results)
#                 else:
#                     log("World already added to user")

#             return {"results": results}
#         return {"results": "You do not have permission to alter this object"}

#     def card():
#         return _card(
#             World.get(request.json.get("pk")),
#             User.get(request.json.get("user")),
#         )

#     def delete():
#         return _delete(
#             User.get(request.json.get("user")),
#             World.get(request.json.get("pk")),
#         )

#     def update():
#         return _update(
#             User.get(request.json.get("user")),
#             World.get(request.json.get("pk")),
#             request.json.get("attr"),
#             request.json.get("value"),
#         )

#     def journal_entries():
#         return _journal_entries(World.get(request.json.get("pk")))

#     def journal_entry():
#         return _journal_entry(request.json.get("journal_pk"))


#     def journal_entry_delete():
#         return _delete_journal_entry(
#             User.get(request.json.get("user")),
#             World.get(request.json.get("pk")),
#             request.json.get("journal_pk"),
#         )

#     def add_journal_entry():
#         return _add_journal_entry(
#             User.get(request.json.get("user")),
#             World.get(request.json.get("pk")),
#             pk=request.json.get("journal_pk"),
#             title=request.json.get("title"),
#             text=request.json.get("text"),
#             tags=request.json.get("tags"),
#             importance=request.json.get("importance"),
#             date=request.json.get("date"),
#         )


#     ################# Session #################

#     def add_campaign():
#         user = User.get(request.json.get("user"))
#         obj = World.get(request.json.get("pk"))
#         if _authenticate(user, obj):
#             entry = obj.add_campaign(
#                 name=request.json.get("name"),
#                 description=request.json.get("description"),
#             )
#             return {"results": entry.serialize()}
#         return {"results": "You do not have permission to alter this object"}

#     def delete_campaign():
#         user = User.get(request.json.get("user"))
#         obj = World.get(request.json.get("pk"))
#         if _authenticate(user, obj):
#             if cam := obj.campaigns.get(request.json.get("campaign_pk")):
#                 del obj.campaigns[cam.pk]
#                 obj.save()
#                 cam.delete()
#             return {"results": "success"}
#         return {"results": "You do not have permission to alter this object"}

#     def session_entries():
#         obj = World.get(request.json.get("pk"))
#         results = []
#         for entry in obj.session.entries:
#             results.append(entry.page_content())
#         return {"results": results}

#     def session_entry():
#         result = JournalEntry.get(request.json.get("session_pk")).page_content()
#         return {"results": result}

#     def add_session_entry():
#         user = User.get(request.json.get("user"))
#         obj = World.get(request.json.get("pk"))
#         if _authenticate(user, obj):
#             entry = obj.add_session_entry(
#                 pk=request.json.get("journal_pk"),
#                 title=request.json.get("title"),
#                 text=request.json.get("text"),
#                 tags=request.json.get("tags"),
#                 date=request.json.get("date"),
#                 associations=request.json.get("associations"),
#             )
#             return {"results": entry.pk}
#         return {"results": "You do not have permission to alter this object"}

#     def delete_session_entry():
#         user = User.get(request.json.get("user"))
#         obj = World.get(request.json.get("pk"))
#         if _authenticate(user, obj):
#             pk = request.json.get("journal_pk")
#             result = "failed"
#             for entry in obj.sessions.entries:
#                 if entry.pk == pk:
#                     obj.sessions.entries.remove(entry)
#                     obj.sessions.save()
#                     entry.delete()
#                     result = "success"
#                     break
#             return {"results": result}
#         return {"results": "You do not have permission to alter this object"}


#     ################# Images #################

#     def image_update():
#         user = User.get(request.json.get("user"))
#         obj = World.get(request.json.get("pk"))
#         url = request.json.get("url")
#         return _image_update(user, obj, url)

#     def image_random():
#         user = User.get(request.json.get("user"))
#         obj = World.get(request.json.get("pk"))
#         return _image_random(user=user, obj=obj)

#     def battlemap_upload():
#         user = User.get(request.json.get("user"))
#         obj = World.get(request.json.get("pk"))
#         url = request.json.get("map_url")
#         return _map_upload(user=user, obj=obj, url=url)

#     def build():
#         user = User.get(request.json.get("user"))
#         world = World.build(
#             system=request.json.get("system"),
#             user=user,
#             name=request.json.get("name"),
#             desc=request.json.get("desc"),
#             backstory=request.json.get("backstory"),
#         )
#         return {"results": world.pk}

#     def region_add():
#         obj = World.get(request.json.get("pk"))
#         user = User.get(request.json.get("user"))
#         if _authenticate(user, obj):
#             region = obj.add_region(description=request.json.get("description"))
#             return {"results": {"pk": region.pk, "api": region.api_path()}}
#         return {"results": "You do not have permission to alter this object"}

#     def remove_region():
#         obj = World.get(request.json.get("pk"))
#         user = User.get(request.json.get("user"))
#         if _authenticate(user, obj):
#             unassigned = obj.remove_region(request.json.get("child_pk"))
#             return {"results": {"pk": unassigned.pk, "api": unassigned.api_path()}}
#         return {"results": "You do not have permission to alter this object"}

#     def player_add():
#         obj = World.get(request.json.get("pk"))
#         user = User.get(request.json.get("user"))
#         if _authenticate(user, obj):
#             child = obj.add_characters(description=request.json.get("description"))
#             return {"results": {"pk": child.pk, "api": child.api_path()}}
#         return {"results": "You do not have permission to alter this object"}


#     def player_remove():
#         obj = World.get(request.json.get("pk"))
#         user = User.get(request.json.get("user"))
#         if _authenticate(user, obj):
#             unassigned = obj.remove_player(request.json.get("child_pk"))
#             return {"results": {"pk": unassigned.pk, "api": unassigned.api_path()}}
#         return {"results": "You do not have permission to alter this object"}


#     def faction_add():
#         obj = World.get(request.json.get("pk"))
#         user = User.get(request.json.get("user"))
#         if _authenticate(user, obj):
#             child = obj.add_faction(description=request.json.get("description")).serialize()
#             return {"results": {"pk": child.pk, "api": child.api_path()}}
#         return {"results": "You do not have permission to alter this object"}


#     def faction_delete():
#         obj = World.get(request.json.get("pk"))
#         user = User.get(request.json.get("user"))
#         if _authenticate(user, obj):
#             unassigned = obj.remove_faction(request.json.get("child_pk"))
#             return {"results": {"pk": unassigned.pk, "api": unassigned.api_path()}}
#         return {"results": "You do not have permission to alter this object"}


#     def assign(rest_path):
#         user = User.get(request.json.pop("user"))
#         obj = World.get(request.json.get("pk"))
#         if rest_path == "player":
#             result = _assign(
#                 user, obj, obj.players, Character.get(request.json.get("child_pk"))
#             )
#         elif rest_path == "player_faction":
#             result = _assign(
#                 user, obj, obj.player_faction, Faction.get(request.json.get("child_pk"))
#             )
#         elif rest_path == "region":
#             result = _assign(
#                 user, obj, obj.regions, Region.get(request.json.get("child_pk"))
#             )
#         else:
#             raise Exception("Invalid path")
#         return result
