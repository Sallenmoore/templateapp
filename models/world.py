import os
import shutil
from datetime import datetime

from autonomous import log
from models.campaign import Campaign
from models.character import Character
from models.city import City
from models.creature import Creature
from models.encounter import Encounter
from models.faction import Faction
from models.item import Item
from models.location import Location
from models.poi import POI
from models.region import Region
from models.ttrpgobject import TTRPGObject


class World(TTRPGObject):
    attributes = TTRPGObject.attributes | {
        "_regions": [],
        "_system": None,
        "_user": None,
        "_subusers": [],
        "player_faction": None,
    }
    # child_model_list = {"character": "players", "faction": "player_faction"}

    ########################## Dunder Methods #############################

    def __init__(self, *args, **kwargs):
        if user := kwargs.get("user"):
            self.user = user
        if regions := kwargs.get("regions"):
            self.regions = regions
        if system := kwargs.get("system"):
            self.system = system

        # check for required attributes
        if not self.system or not self.user:
            raise Exception("World must have a user and system")

        # Set defaults for things that have not been set
        # breakpoint()
        if self.pk not in self.user.world_pks:
            pk = self.save()
            self.user.world_pks.append(pk)
            self.user.save()
        # log(self.user)

    ########################## Class Methods #############################

    @classmethod
    def build(cls, system, user, name=None, desc=None, backstory=None):
        # log(system)
        System = World._systems.get(system)
        if not System:
            raise ValueError(f"System {system} not found")
        else:
            system = System()
            system.save()

        ### set attributes ###
        if not name:
            name = f"{system._genre} World"
        if not desc:
            desc = f"An expansive, complex, and mysterious {system._genre} setting suitable for a {system._genre} TTRPG campaign."
        if not backstory:
            backstory = f"{name} is filled with points of interest to explore and unique non-player character interactions that over time reveal the complex and mysterious history of this world, as well as determine its future. Currently, there are several factions vying for power through poltical machinations, subterfuge, and open warfare."

        # log(f"Building world {name}, {desc}, {backstory}, {system}, {user}")

        world = cls(
            name=name,
            desc=desc,
            backstory=backstory,
            system=system,
            user=user,
        )
        world.save()
        if world.pk not in user.world_pks:
            user.world_pks.append(world.pk)
        user.save()
        world.system.update_refs(world)
        return world

    ############################ PROPERTIES ############################

    # @property
    # def campaigns(self):
    #     return self._campaigns

    # @campaigns.setter
    # def campaigns(self, value):
    #     self._campaigns = value

    @property
    def children(self):
        return [x for x in [self.player_faction, *self.players, *self.regions] if x]

    @property
    def child_models(self):
        return {
            "region": Region,
            "city": City,
            "location": Location,
            "poi": POI,
            "encounter": Encounter,
            "faction": Faction,
            "creature": Creature,
            "item": Item,
            "character": Character,
            "player": Character,
        }

    @property
    def characters(self):
        # log("Retrieving Characters...")
        results = Character.search(_world=self)
        if results:
            results = sorted(results, key=lambda obj: obj.name)
        return results

    @characters.setter
    def characters(self, value):
        pass

    @property
    def cities(self):
        results = City.search(_world=self)
        if results:
            results = sorted(results, key=lambda obj: obj.name)
        return results

    @property
    def creatures(self):
        results = Creature.search(_world=self)
        if results:
            results = sorted(results, key=lambda obj: obj.name)
        return results

    @property
    def encounters(self):
        results = Encounter.search(_world=self)
        if results:
            results = sorted(results, key=lambda obj: obj.name)
        return results

    @property
    def factions(self):
        results = Faction.search(_world=self)
        if results:
            results = sorted(results, key=lambda obj: obj.name)
        return results

    @property
    def genre(self):
        return self.system._genre.lower()

    @property
    def history(self):
        return self.backstory

    @history.setter
    def history(self, value):
        self.backstory = value

    @property
    def items(self):
        results = Item.search(_world=self)
        if results:
            results = sorted(results, key=lambda obj: obj.name)
        return results

    @property
    def locations(self):
        results = Location.search(_world=self)
        if results:
            results = sorted(results, key=lambda obj: obj.name)
        return results

    @property
    def map_type(self):
        return f"{self.title} atlas style map"

    @property
    def map_scale(self):
        return "1 inch = 100 miles"

    @property
    def parent(self):
        return None

    @parent.setter
    def parent(self, obj):
        if obj:
            raise TypeError("World's own parent object set attempt", obj)

    @property
    def players(self):
        return Character.search(_world=self, is_player=True)

    @property
    def pois(self):
        results = POI.search(_world=self)
        if results:
            results = sorted(results, key=lambda obj: obj.name)
        return results

    @property
    def regions(self):
        self._regions = sorted(self._regions, key=lambda obj: obj.name)
        return self._regions

    @regions.setter
    def regions(self, value):
        self._regions = value

    @property
    def system(self):
        return self._system

    @system.setter
    def system(self, obj):
        if "System" not in obj.__class__.__name__:
            raise TypeError(f"Invalid system: {obj}")
        self._system = obj

    @property
    def subusers(self):
        return self._subusers

    @subusers.setter
    def subusers(self, obj):
        self._subusers = []
        for u in obj:
            if not u.__class__.__name__ == "User":
                log("World's user object set attempt", u)
            elif self.pk and self.pk not in u.world_pks:
                u.world_pks.append(self.pk)
                self._subusers.append(u)

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, obj):
        if not obj.__class__.__name__ == "User":
            raise TypeError("World's user object set attempt", obj)
        self._user = obj
        if self.pk and self.pk not in self._user.world_pks:
            self._user.world_pks.append(self.pk)

    @property
    def users(self):
        return [self._user, *self._subusers]

    @property
    def world(self):
        return None

    @world.setter
    def world(self, obj):
        raise TypeError("World's own world object set attempt")

    ########################## Instance Methods #############################

    def has_children(self, value):
        value = value.lower()
        return value if value in ["player", "player_faction", "region"] else None

    def delete(self):
        objs = [
            *Region.search(_world=self),
            *City.search(_world=self),
            *Location.search(_world=self),
            *POI.search(_world=self),
            *Encounter.search(_world=self),
            *Faction.search(_world=self),
            *Creature.search(_world=self),
            *Character.search(_world=self),
            *Item.search(_world=self),
        ]
        for r in objs:
            r.emancipate()
            r.delete()
        if self.pk in self.user.world_pks:
            self.user.world_pks.remove(self.pk)
            self.user.save()
        return super().delete()

    def is_owner(self, user):
        return self.user == user

    def is_user(self, user):
        return self.is_owner(user) or user in self.subusers

    def save(self):
        if self.world:
            raise Exception(
                f"WARNING: World {self.name} ({self.pk}) has a world: {self.world.name}. THIS SHOULD NEVER GET SET!!!!!!"
            )
        if not self._user:
            raise ValueError("World must have a user")
        pk = super().save()
        return pk

    def get_image_prompt(self):
        return f"A full color, high resolution illustrated map of a fictional {self.genre} world called {self.name} and described as {self.desc or 'filled with points of interest to explore, antagonistic factions, and a rich, mysterious history.'}"

    ###################### Campaign Methods ########################

    def add_campaign(
        self,
        name,
        description=None,
    ):
        log(f"Adding campaign {name} with description: {description}")
        campaign = Campaign(
            name=name, description=description, _world=self, _players=self.players
        )
        campaign.save()
        self.campaigns[campaign.pk] = campaign
        log(f"Added campaign {campaign.name}({campaign.pk}):\n\n\t{campaign}")
        self.save()
        return campaign

    # def campaign_session(
    #     self,
    #     campaign_pk,
    #     session_pk=None,
    #     title=None,
    #     text=None,
    #     tags=None,
    #     importance=0,
    #     date=None,
    #     associations=None,
    # ):
    #     if campaign := self.campaigns.get(campaign_pk):
    #         session = campaign.session(
    #             self,
    #             pk=session_pk,
    #             title=title,
    #             text=text,
    #             tags=tags,
    #             importance=importance,
    #             date=date,
    #             associations=associations,
    #         )
    #         self.save()
    #         return session
    #     else:
    #         raise ValueError(f"Campaign {campaign_pk} not found")

    def add_regions(self, description=None):
        region = Region.build(world=self, parent=self, description=description)
        self.regions.append(region)
        # log(f"Added region {region.name}({region.pk}):\n\n\t{region}")
        self.save()
        return region

    def add_characters(self, description=None, player=None):
        description = (
            description
            or "A character wth a short term goal that requires help from others, as well as a desperate long-term goal they keep secret and requires extensive travel."
        )

        if player:
            if player.__class__.__name__ != "Character":
                raise TypeError("World's faction object set attempt", player)

            if player.parent:
                player.parent.characters.remove(player)
                player.parent.save()

            character = player
        else:
            character = Character.build(
                world=self, parent=self, description=description
            )
        # log(f"Added player {character.name}:\n\n\t{character}")
        character.parent = self
        character.world = self
        character.save()
        # log(pk)
        self.players.append(character)
        if self.player_faction:
            self.player_faction.add_character(character)
        # log(f"Players: {self.players}")
        self.save()
        return character

    def add_factions(self, description=None, faction=None):
        description = description or "A small band of individuals with a unifying goal."
        if faction and faction.__class__.__name__ == "Faction":
            player_faction = faction
            player_faction.parent.factions.remove(faction)
        else:
            player_faction = Faction.build(
                world=self, parent=self, description=description
            )
        player_faction.characters = self.players
        player_faction.save()
        if self.player_faction:
            player_faction.characters = self.player_faction.characters
            self.player_faction.characters = []
            self.player_faction.parent = None
            self.player_faction.save()
        self.player_faction = player_faction
        self.save()
        return player_faction

    def add_session_entry(
        self,
        campaign_pk,
        pk=None,
        title=None,
        text=None,
        tags=[],
        date=None,
        associations=None,
    ):
        normalized_associations = []
        if associations:
            for entity in associations:
                if model := self.child_models.get(entity.get("model")):
                    if obj := model.get(entity.get("pk")):
                        normalized_associations.append(obj)
                else:
                    raise ValueError(f"Invalid model: {entity.get('model')}")
        if campaign := self.campaigns.get(campaign_pk):
            if pk:
                entry = campaign.sessions.update_entry(
                    pk=pk,
                    title=title,
                    text=text,
                    tags=tags,
                    date=date,
                    associations=normalized_associations,
                )
            else:
                entry = campaign.sessions.add_entry(
                    title=title,
                    text=text,
                    tags=tags,
                    date=datetime.now(),
                    associations=normalized_associations,
                )
            return entry

    def get_children(self, model):
        if not isinstance(model, str):
            model = model.__name__
        children_name = self.child_list_key(model.lower())
        results = getattr(self, children_name, [])
        return results

    def get_timeline(self, filter=None):
        size = "2rem"
        start_icons = {
            Character: f"<iconify-icon icon='fa-solid:baby' width='{size}' style='color:deeppink'></iconify-icon>",
            Creature: f"<iconify-icon icon='fa-solid:spider' width='{size}' style='color:mediumblue'></iconify-icon>",
            Encounter: f"<iconify-icon icon='arcticons:battleforwesnoth' width='{size}' style='color:orange'></iconify-icon>",
            Item: f"<iconify-icon icon='fa-solid:treasure-chest' width='{size}' style='color:gold'></iconify-icon>",
            Location: f"<iconify-icon icon='fa-solid:map-marked-alt' width='{size}' style='color:purple'></iconify-icon>",
            POI: f"<iconify-icon icon='tabler:building-castle' width='{size}' style='color:darkgreen'></iconify-icon>",
            Region: f"<iconify-icon icon='carbon:flag-filled' width='{size}' style='color:brown'></iconify-icon>",
            City: f"<iconify-icon icon='arcticons:pocket-city' width='{size}' width='{size}' style='color:lightslategrey'></iconify-icon>",
            Faction: f"<iconify-icon icon='clarity:group-line' width='{size}' style='color:goldenrod'></iconify-icon>",
        }
        end_icons = {
            Character: f"<iconify-icon icon='mdi:death' width='{size}' style='color:maroon'></iconify-icon>",
            Creature: f"<iconify-icon icon='healthicons:death-alt' width='{size}' style='color:maroon'></iconify-icon>",
            Encounter: f"<iconify-icon icon='mdi:shop-complete' width='{size}' style='color:midnightblue'></iconify-icon>",
            Item: f"<iconify-icon icon='streamline:lost-and-found' width='{size}' style='color:darkorange'></iconify-icon>",
            Location: f"<iconify-icon icon='game-icons:castle-ruins' width='{size}' style='color:darkmagenta'></iconify-icon>",
            POI: f"<iconify-icon icon='game-icons:ancient-ruins' width='{size}' style='color:olive'></iconify-icon>",
            Region: f"<iconify-icon icon='pepicons-pop:flag-circle-off' width='{size}' style='color:maroon'></iconify-icon>",
            City: f"<iconify-icon icon='game-icons:stone-pile' width='{size}' style='color:darkslategrey'></iconify-icon>",
            Faction: f"<iconify-icon icon='bi:heartbreak' width='{size}' style='color:darkgoldenrod'></iconify-icon>",
        }

        ## Filters
        time = int(filter.get("time", 0))
        events = getattr(
            self,
            self.child_list_key(filter["type"]),
            [
                *self.regions,
                *self.cities,
                *self.pois,
                *self.locations,
                *self.factions,
                *self.characters,
                *self.creatures,
                *self.encounters,
                *self.items,
            ],
        )

        timeline = []
        for o in events:
            if int(o.start_date.get("year")) > time:
                # characters, creatures
                # encounters, items, locations, pois, regions, cities, factions
                timeline.append(
                    {
                        "name": o.name,
                        "image": o.image(),
                        "path": o.page_path(),
                        "date": o.start_date,
                        "date_str": o.start_date_str,
                        "icon": start_icons.get(o.__class__),
                    }
                )
            if int(o.end_date.get("year")) > time and (o.end_date != o.start_date):
                timeline.append(
                    {
                        "name": o.name,
                        "image": o.image(),
                        "path": o.page_path(),
                        "date": o.end_date,
                        "date_str": o.end_date_str,
                        "icon": end_icons.get(o.__class__),
                    }
                )
        timeline = sorted(
            timeline,
            key=lambda x: (
                int(x["date"]["year"]),
                int(x["date"]["month"]),
                int(x["date"]["day"]),
            ),
            reverse=True,
        )
        return timeline

    def page_data(self):
        return {
            "World": {
                "name": self.name,
                "desc": self.desc,
                "backstory": self.backstory,
                "genre": self.genre,
                "current_campaign": self.current_campaign.page_data()
                if self.current_campaign
                else None,
            },
            "Regions": [o.page_data() for o in self.regions],
            "Locations": [o.page_data() for o in self.locations],
            "Cities": [o.page_data() for o in self.cities],
            "Points of Interest": [o.page_data() for o in self.pois],
            "Factions": [o.page_data() for o in self.factions],
            "Characters": [o.page_data() for o in self.characters],
            "Items": [o.page_data() for o in self.items],
            "Creatures": [o.page_data() for o in self.creatures],
            "Encounters": [o.page_data() for o in self.encounters],
        }

    @property
    def state_data(self):
        obj_data = super().state_data
        obj_data["geneology"]["children"] = {
            "Region": [o.pk for o in self.regions],
            "Location": [o.pk for o in self.locations],
            "City": [o.pk for o in self.cities],
            "POI": [o.pk for o in self.pois],
            "Faction": [o.pk for o in self.factions],
            "Character": [o.pk for o in self.characters],
            "Item": [o.pk for o in self.items],
            "Creature": [o.pk for o in self.creatures],
            "Encounter": [o.pk for o in self.encounters],
        }
        obj_data["players"] = [o.pk for o in self.players]
        obj_data["player_faction"] = (
            self.player_faction.pk if self.player_faction else None
        )
        obj_data["timeline"] = self.get_timeline()
        obj_data["subusers"] = [su.pk for su in self.subusers]
        obj_data["campaigns"] = []
        for c in self.campaigns.values():
            obj_data["campaigns"].append(
                {
                    "pk": c.pk,
                    "name": c.name,
                    "description": c.description,
                    "sessions": [session.pk for session in c.sessions.entries],
                }
            )
        log(obj_data)
        return obj_data

    # def compendium(self):
    #     compendiumized = {
    #         "world": self.serialize(),
    #         "regions": [],
    #         "cities": [],
    #         "locations": [],
    #         "factions": [],
    #         "characters": [],
    #         "items": [],
    #         "creatures": [],
    #         "encounters": [],
    #     }
    #     root_path = f"static/compendiums/{self.slug}-{self.pk}"
    #     img_path = f"{root_path}/images"
    #     if os.path.isdir(img_path):
    #         shutil.rmtree(img_path)
    #     os.makedirs(img_path, exist_ok=True)

    #     ### Regions ###
    #     region_assets = f"{img_path}/artwork/regions"
    #     os.makedirs(region_assets, exist_ok=True)
    #     for o in self.regions:
    #         copy_path = f"{region_assets}/{o.slug}.webp"
    #         try:
    #             shutil.copy(
    #                 o.image_path(),
    #                 copy_path,
    #             )
    #         except Exception as e:
    #             log(e)
    #         else:
    #             log(f"copied {o.image_path()} to {copy_path}")
    #             compendiumized["regions"].append(o.serialize())

    #     city_assets = f"{img_path}/artwork/cities"
    #     os.makedirs(city_assets, exist_ok=True)
    #     for o in self.cities:
    #         copy_path = f"{city_assets}/{o.slug}.webp"
    #         try:
    #             shutil.copy(o.image_path(), copy_path)
    #         except Exception as e:
    #             log(e)
    #         else:
    #             log(f"copied {o.image_path()} to {copy_path}")
    #             compendiumized["regions"].append(o.serialize())

    #     location_assets = f"{img_path}/artwork/locations"
    #     os.makedirs(location_assets, exist_ok=True)
    #     location_maps = f"{img_path}/maps/locations"
    #     os.makedirs(location_maps, exist_ok=True)
    #     for o in self.locations:
    #         copy_path = f"{location_assets}/{o.slug}.webp"
    #         try:
    #             shutil.copy(
    #                 o.image_path(),
    #                 f"{location_assets}/{os.path.basename(o.image_path())}",
    #             )
    #             if o.battlemap:
    #                 shutil.copy(o.map_path(), copy_path)
    #         except Exception as e:
    #             log(e)
    #         else:
    #             log(f"copied {o.image_path()} to {copy_path}")
    #             compendiumized["regions"].append(o.serialize())

    #     faction_assets = f"{img_path}/artwork/factions"
    #     os.makedirs(faction_assets, exist_ok=True)
    #     for o in self.factions:
    #         copy_path = f"{faction_assets}/{o.slug}.webp"
    #         try:
    #             shutil.copy(o.image_path(), copy_path)
    #         except Exception as e:
    #             log(e)
    #         else:
    #             log(f"copied {o.image_path()} to {copy_path}")
    #             compendiumized["regions"].append(o.serialize())

    #     creatures_assets = f"{img_path}/tokens/creatures"
    #     os.makedirs(creatures_assets, exist_ok=True)
    #     for o in self.characters:
    #         copy_path = f"{creatures_assets}/{o.slug}.webp"
    #         try:
    #             shutil.copy(o.image_path(), copy_path)
    #         except Exception as e:
    #             log(e)
    #         else:
    #             log(f"copied {o.image_path()} to {copy_path}")
    #             compendiumized["regions"].append(o.serialize())

    #     items_assets = f"{img_path}/tiles/items"
    #     os.makedirs(items_assets, exist_ok=True)
    #     for o in self.items:
    #         copy_path = f"{items_assets}/{o.slug}.webp"
    #         try:
    #             shutil.copy(
    #                 o.image_path(), f"{items_assets}/{os.path.basename(o.image_path())}"
    #             )
    #         except Exception as e:
    #             log(e)
    #         else:
    #             log(f"copied {o.image_path()} to {copy_path}")
    #             compendiumized["regions"].append(o.serialize())

    #     characters_assets = f"{img_path}/tokens/characters"
    #     os.makedirs(characters_assets, exist_ok=True)
    #     for o in self.creatures:
    #         copy_path = f"{characters_assets}/{o.slug}.webp"
    #         try:
    #             shutil.copy(o.image_path(), copy_path)
    #         except Exception as e:
    #             log(e)
    #         else:
    #             log(f"copied {o.image_path()} to {copy_path}")
    #             compendiumized["regions"].append(o.serialize())

    #     encounters_assets = f"{img_path}/artwork/encounters"
    #     os.makedirs(encounters_assets, exist_ok=True)
    #     encounters_maps = f"{img_path}/maps/encounters"
    #     os.makedirs(encounters_maps, exist_ok=True)
    #     for o in self.encounters:
    #         copy_path = f"{encounters_assets}/{o.slug}.webp"
    #         try:
    #             shutil.copy(o.image_path(), copy_path)
    #             if o.battlemap:
    #                 shutil.copy(
    #                     o.map_path(),
    #                     f"{encounters_maps}/{os.path.basename(o.map_path())}",
    #                 )
    #         except Exception as e:
    #             log(e)
    #         else:
    #             log(f"copied {o.image_path()} to {copy_path}")
    #             compendiumized["regions"].append(o.serialize())
    #     return self.serialize()
