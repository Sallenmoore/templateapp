import os
import random

import requests
from flask import get_template_attribute
from slugify import slugify

from autonomous import log
from autonomous.model.autoattribute import AutoAttribute
from autonomous.model.automodel import AutoModel
from autonomous.storage.imagestorage import ImageStorage
from autonomous.storage.markdown import Page

from .journal import Journal
from .systems import (
    FantasySystem,
    HardboiledSystem,
    HistoricalSystem,
    HorrorSystem,
    PostApocalypticSystem,
    SciFiSystem,
    WesternSystem,
)

IMAGES_BASE_PATH = os.environ.get("IMAGE_BASE_PATH", "static/images/tabletop")
MAX_NUM_IMAGES_IN_GALLERY = 100


class TTRPGObject(AutoModel):
    _systems = {
        "fantasy": FantasySystem,
        "sci-fi": SciFiSystem,
        "western": WesternSystem,
        "hardboiled": HardboiledSystem,
        "mystery": HardboiledSystem,
        "horror": HorrorSystem,
        "post-apocalyptic": PostApocalypticSystem,
        "historical": HistoricalSystem,
    }

    _no_copy = [
        "pk",
        "wiki_id",
        "_parent_obj",
        "_journal",
        "battlemap",
        "_associations",
    ]
    _storage = ImageStorage(IMAGES_BASE_PATH)
    _wiki_api = Page

    _funcobj = {}

    child_model_list = {"city": "cities"}

    attributes = {
        "name": "",
        "_world": None,
        "_parent_obj": None,
        "_associations": [],
        "_campaigns": {},
        "current_campaign": None,
        "_backstory": AutoAttribute(
            "TEXT",
            default="Unknown",
        ),
        "bs_summary": "",
        "desc": AutoAttribute("TEXT", default=""),
        "traits": [],
        "asset_id": "",
        "battlemap": "",
        "_start_date": {"day": 0, "month": 0, "year": 0},
        "_end_date": {"day": 0, "month": 0, "year": 0},
        "wiki_id": 0,
        "_journal": None,
    }

    ########### Dunder Methods ###########

    def __init__(self, *args, **kwargs):
        # log(f"Obj\n===\n{kwargs}")
        if kwargs.get("world"):
            self.world = kwargs.get("world")
        if kwargs.get("parent"):
            self.parent = kwargs.get("parent")
        if kwargs.get("journal"):
            self.journal = kwargs.get("journal")
        if kwargs.get("backstory"):
            self.backstory = kwargs.get("backstory", "Unknown")

        if not self.world:
            raise Exception(f"{self.__class__.__name__} must have a world")
        # log(f"Obj\n===\n{self}")

    def __eq__(self, obj):
        if hasattr(obj, "pk"):
            return self.pk == obj.pk
        return False

    def __ne__(self, obj):
        if hasattr(obj, "pk"):
            return self.pk != obj.pk
        return True

    def __lt__(self, obj):
        if hasattr(obj, "name"):
            return self.name < obj.name
        return False

    def __gt__(self, obj):
        if hasattr(obj, "name"):
            return self.name > obj.name
        return False

    def __hash__(self):
        return hash(self.pk)

    ########### Class Methods ###########

    @classmethod
    def build(cls, world, parent=None, description=None):
        obj = cls(world=world, parent=parent)
        obj.backstory = description or "Unknown"
        obj.save()
        return obj

    @classmethod
    def child_list_key(cls, model, key_list=None):
        if key_list:
            return key_list.get(model)
        return cls.child_model_list.get(model, f"{model}s")

    ########### Property Methods ###########
    @property
    def asset_folder(self):
        partial_path = f"{self.genre}/{self.__class__.__name__.lower()}"
        full_path = f"{IMAGES_BASE_PATH}/{partial_path}"
        if not os.path.exists(full_path):
            os.makedirs(full_path)
        return partial_path

    @property
    def age(self):
        if not self._start_date.get("day"):
            self._start_date["day"] = random.randint(1, self.system.num_days_per_month)
        if not self._start_date.get("month"):
            self._start_date["month"] = random.choice(self.system.calendar["months"])

        if (
            self._start_date.get("year")
            and self.system.calendar["current_date"]["year"]
        ):
            end = int(
                self._end_date.get("year")
                or self.system.calendar["current_date"]["year"]
            )
            return end - int(self._start_date["year"])
        return 0

    @age.setter
    def age(self, value):
        if not self._start_date.get("day"):
            self._start_date["day"] = random.randint(1, self.system.num_days_per_month)
        if not self._start_date.get("month"):
            self._start_date["month"] = random.choice(self.system.calendar["months"])
        end = int(
            self._end_date.get("year")
            or self.get_world().system.calendar["current_date"]["year"]
        )
        self._start_date["year"] = end - int(value)

    @property
    def associations(self):
        return self._associations

    @associations.setter
    def associations(self, value):
        self._associations = value

    @property
    def backstory(self):
        return self._backstory

    @backstory.setter
    def backstory(self, obj):
        # log(obj)
        if obj != self._backstory:
            self._backstory = obj
            self.bs_summary = ""

    @property
    def backstory_summary(self):
        if self._backstory and not self.bs_summary.strip():
            self.bs_summary = self.system.generate_summary(self._backstory)
            self.save()
        return self.bs_summary

    @property
    def battlemap_url(self):
        return (
            self._storage.get_url(self.battlemap)
            if self.battlemap
            else "https://placehold.co/1792x1024"
        )

    @battlemap_url.setter
    def battlemap_url(self, url):
        self.update_battlemap_url(url)

    @property
    def campaigns(self):
        return self._campaigns

    @campaigns.setter
    def campaigns(self, value):
        self._campaigns = value

    @property
    def children(self):
        return []

    @property
    def child_key(self):
        model_name = self.model_name().lower()
        return {
            "city": "cities",
        }.get(model_name, f"{model_name}s")

    @property
    def current_day(self):
        return self.system.calendar["current_date"]["day"]

    @property
    def current_month(self):
        return self.system.calendar["current_date"]["month"]

    @property
    def current_year(self):
        return self.system.calendar["current_date"]["year"]

    @property
    def description(self):
        return self.desc

    @description.setter
    def description(self, val):
        self.desc = val

    @property
    def end_date(self):
        if not self._end_date.get("day"):
            self._end_date["day"] = random.randint(1, self.system.num_days_per_month)
        if not self._end_date.get("month"):
            self._end_date["month"] = random.randrange(
                len(self.system.calendar["months"])
            )
        elif isinstance(self._end_date["month"], str):
            self._end_date["month"] = self.system.calendar["months"].index(
                self._end_date["month"]
            )
        self._end_date["day"] = int(self._end_date["day"])
        self._end_date["year"] = (
            int(self._end_date["year"]) if self._end_date.get("year") else 0
        )
        return self._end_date

    @end_date.setter
    def end_date(self, val):
        try:
            self._end_date["day"] = int(val["day"])

            if isinstance(val["month"], int) or val["month"].isdigit():
                self._end_date["month"] = int(val["month"])
            elif val["month"] in self.system.calendar["months"]:
                self._end_date["month"] = self.system.calendar["months"].index(
                    val["month"]
                )
            else:
                raise ValueError(f"Invalid month: {val['month']}")

            self._end_date["year"] = int(val["year"])
        except Exception as e:
            log(e, "Must set date as a dictionary with 'day', 'month', and 'year' keys")

    @property
    def end_date_str(self):
        if self._end_date.get("year"):
            if isinstance(self._end_date["month"], int):
                month_idx = self._end_date["month"]
            else:
                month_idx = self.system.calendar["months"].index(
                    self._end_date["month"]
                )
                self._end_date["month"] = month_idx
            return f"{self._end_date['day']} {self.system.calendar['months'][month_idx]} {self._end_date['year']} {self.system.calendar['year_string']}"
        return ""

    @property
    def funcobj(self):
        if not self._funcobj.get("parameters") or not self._funcobj["parameters"].get(
            "required"
        ):
            self._funcobj["parameters"]["required"] = list(
                self._funcobj["parameters"]["properties"].keys()
            )
        return self._funcobj

    @property
    def geneology(self):
        ancestors = []
        parent = self.parent
        while parent:
            ancestors.append(parent)
            parent = parent.parent
        return ancestors[::-1] if ancestors else [self.get_world()]

    @property
    def genre(self):
        return self.world.genre.lower()

    @property
    def genres(self):
        return list(self._systems.keys())

    @property
    def image_url(self):
        return self.image()

    @image_url.setter
    def image_url(self, url):
        self.update_image_url(url)

    @property
    def journal(self):
        if not self._journal:
            self._journal = Journal(_world=self.get_world(), _parent=self)
            self._journal.save()
            self.save()
            log(self._journal)
        return self._journal

    @journal.setter
    def journal(self, value):
        if isinstance(value, (Journal, None.__class__)):
            self._journal = value
        else:
            raise TypeError(
                f"Journal must be a Journal object, not {value.__class__.__name__}"
            )

    @property
    def map_prompt(self):
        return f"""A {self.title} map based closely on the following description:
          - {self.description}
          - {self.backstory_summary}
        """

    @property
    def map_type(self):
        return f"{self.title} battlemap"

    @property
    def map_scale(self):
        return "1 inch == 5 feet"

    # @property
    # def name(self):
    #    return self._name

    # @name.setter
    # def name(self, value):
    #    self._name = self.system.sanitize(value)

    @property
    def parent(self):
        return self._parent_obj

    @parent.setter
    def parent(self, obj):
        if issubclass(obj.__class__, TTRPGObject) or obj is None:
            self._parent_obj = obj
        else:
            raise TypeError(
                f"Parent must be a TTRPGObject, not {obj.__class__.__name__}"
            )

    @property
    def siblings(self):
        return self._parent_obj and getattr(self._parent_obj, self.child_key, None)

    @property
    def slug(self):
        return slugify(self.name)

    @property
    def start_date(self):
        if not self._start_date.get("day"):
            self._start_date["day"] = random.randint(1, self.system.num_days_per_month)
        if not self._start_date.get("month"):
            self._start_date["month"] = random.randrange(
                len(self.system.calendar["months"])
            )
        elif isinstance(self._start_date["month"], str):
            self._start_date["month"] = self.system.calendar["months"].index(
                self._start_date["month"]
            )
        self._start_date["day"] = int(self._start_date["day"])
        self._start_date["year"] = (
            int(self._start_date["year"]) if self._start_date.get("year") else 0
        )
        return self._start_date

    @start_date.setter
    def start_date(self, val):
        try:
            self._start_date["day"] = int(val["day"])
            if isinstance(val["month"], int) or val["month"].isdigit():
                self._start_date["month"] = int(val["month"])
            elif val["month"] in self.system.calendar["months"]:
                self._start_date["month"] = self.system.calendar["months"].index(
                    val["month"]
                )
            else:
                raise ValueError(f"Invalid month: {val['month']}")
            self._start_date["year"] = int(val["year"]) if val.get("year") else 0
        except Exception as e:
            log(e, "Must set date as a dictionary with 'day', 'month', and 'year' keys")

    @property
    def start_date_str(self):
        if self._start_date.get("year"):
            if isinstance(self._start_date["month"], int):
                month_idx = self._start_date["month"]
            else:
                month_idx = self.system.calendar["months"].index(
                    self._start_date["month"]
                )
                self._start_date["month"] = month_idx
            # log(month_idx, self.system.calendar["months"])
            # {self.system.calendar['months'][month_idx]}
            return f"{self._start_date['day']} {self.system.calendar['months'][month_idx]} {self._start_date['year']} {self.system.calendar['year_string']}"
        return "Unknown"

    @property
    def subusers(self):
        return self.get_world().subusers

    @property
    def system(self):
        return self.get_world().system

    @property
    def title(self):
        return self.get_world().system.get_title(self)

    @property
    def titles(self):
        return self.get_world().system._titles

    @property
    def user(self):
        return self.get_world().user

    @property
    def world(self):
        if self._world:
            return self._world
        else:
            raise Exception(
                f"\n[{self.__class__.__name__}: {self.pk}]{self.name}\n!!!!!! Object has no World or parent that has a world !!!!!!"
            )

    @world.setter
    def world(self, val):
        # World Object
        if val.__class__.__name__ != "World":
            raise TypeError(
                f"World must be a World object, not {val.__class__.__name__}"
            )
        if (
            self.parent
            and self._world
            and self.parent._world
            and self.parent._world != val
        ):
            raise Exception(
                f"Cannot change world of {self.__class__.__name__} {self.name} because it has a parent with a different world"
            )
        else:
            self._world = val

    ########### CRUD Methods ###########

    def generate(self, prompt=""):
        prompt += f"""
        Use and expand on the existing object data listed below for the {self.title} object:
        - Name: {self.name if self.name.strip() else "Unknown"}
        - Description: {self.description if self.description.strip() else "Unknown"}
        - Backstory: {self.backstory if self.backstory.strip() else "Unknown"}
        - Traits: {self.traits if self.traits else "Unknown"}
        """
        if getattr(self, "goal", None):
            prompt += f"""
        - Goal: {self.goal}
        """
        if getattr(self, "status", None):
            prompt += f"""
        - Current Status: {self.status}
        """

        owner = self.parent if self.parent else self.world
        prompt += f"""
        - Parent Object: {owner.title}
        - Parent primary key: {owner.pk}
        """
        # print(owner.name, owner.backstory_summary.strip())
        if owner.name and owner.backstory_summary.strip():
            prompt += f"""
        - Parent Name: {owner.name}
        - Parent Description: {owner.backstory_summary}
        """

        if self.children:
            prompt += """
        - Child Objects:
        """
            for child in self.children:
                prompt += f"""
            - {child.title}
            """
                if child.name and child.backstory_summary:
                    prompt += f"""
              - Name: {child.name}
              - Backstory: {child.backstory_summary}
                """
        # print(prompt)
        try:
            results = self.system.generate(self, prompt=prompt)
        except Exception as e:
            print(e)
            results = f"{e}"
        else:
            for k, v in results.items():
                if k == "name" and v != self.name:
                    v = f"{v} ({self.name})"
                try:
                    setattr(self, k, v)
                except Exception as e:
                    log(f"{e}\n{k}: {v}")
            self.save()
            # This ensures it will upload the world data to the AI after generating
            self.system.update_refs(self.get_world())
        return results

    def copy(self):
        obj = self.__class__(world=self.world, parent=None)
        for attr in self.attributes:
            if attr not in self._no_copy:
                setattr(obj, attr, getattr(self, attr))
        obj.name += " (Copy)"
        obj.save()
        return obj

    def unassigned(self, child_key=None):
        log(child_key)
        if model := self.get_world().child_models.get(child_key):
            model_list = {child_key: model}
        else:
            model_list = self.get_world().child_models
        # log(model_list)
        new = []
        orphans = []
        children = []
        for k, model in model_list.items():
            for o in model.search(_world=self.get_world()):
                if not o.name:
                    new.append(o)
                elif not o.parent:
                    orphans.append(o)
                elif o.parent == self.get_world() or o.parent != self:
                    children.append(o)
        orphans.sort(key=lambda x: x.name)
        children.sort(key=lambda x: x.name)
        objs = new + orphans + children
        return objs

    ########################
    ## TODO: Deprecated Method, remove from code base
    def remove(self, obj, collection):
        log("Remove is deprecated. Please update to remove_child() or emancipate().")
        obj.parent = None
        collection.remove(obj)
        obj.save()
        self.save()
        return obj

    ## Updated Methods
    def remove_child(self, obj):
        getattr(self.parent, obj.child_key).remove(obj)
        obj.parent = None
        obj.save()
        self.save()
        return obj

    def emancipate(self):
        if self.parent:
            if self in getattr(self.parent, self.child_key):
                getattr(self.parent, self.child_key).remove(self)
            self.parent.save()
            self.parent = None
            self.save()
        return self.parent

    ###################

    def delete(self):
        if self.parent:
            raise Exception(
                f"Cannot delete {self.__class__.__name__} {self.name} because it has a parent. Unlink it form its parent first."
            )
        for child in self.children:
            child.parent = None
            child.world = self.world
            child.save()
        if self._journal:
            self._journal.delete()
        return super().delete()

    ########### Path Methods ###########
    def _make_path(self, path, full):
        path = f"/{path}/{self.__class__.__name__.lower()}"
        if full:
            path = f"{os.environ.get('APP_BASE_URL')}{path}"
        return path

    def api_path(self, full=False):
        return self._make_path("api", full)

    def page_path(self, full=False):
        path = f"/{self.__class__.__name__.lower()}/{self.pk}"
        if full:
            path = f"{os.environ.get('APP_BASE_URL')}{path}"
        return path

    def task_path(self, full=False):
        return self._make_path("task", full)

    def wiki_path(self, full=False):
        root_path = os.environ.get("WIKI_", "ttrpg")
        path = f"{root_path}/{self.world.slug}/{self.__class__.__name__.lower()}/{self.slug}-{self.pk}"
        if full:
            path = f"{os.environ.get('WIKI_BASE_URL')}{path}"
        return path

    def image_path(self, size="orig"):
        path = f"{IMAGES_BASE_PATH}/{self.asset_id.replace('.', '/')}/{size}.webp"
        return path

    # def map_path(self):
    #     # log(self.battlemap)
    #     path, filename, ext = self.battlemap.rsplit(".", maxsplit=3)
    #     path = path.replace(".", "/")
    #     path = f"{self._storage.base_path}/{path}/{filename}.{ext}"
    #     # log(path)
    #     return path

    ############# Boolean Methods #############

    def is_owner(self, user):
        try:
            return self.world.is_owner(user)
        except Exception as e:
            log(e, self, "Object has no world")
            return False

    def is_parent(self, obj):
        return self._parent_obj == obj if self._parent_obj else False

    def is_child(self, obj, children):
        try:
            return obj in getattr(self, children)
        except Exception as e:
            log(e, self, f"Object has no children named {children}")
            return False

    ############# Image Methods #############

    def get_image_list(self):
        # log(self._storage.base_path, self._storage.search(folder=self.asset_folder))
        if images := self._storage.search(folder=self.asset_folder):
            image_list = random.sample(
                images, k=min(len(images), MAX_NUM_IMAGES_IN_GALLERY)
            )
            return [
                {"asset_id": image, "url": self._storage.get_url(image, size=100)}
                for image in image_list
            ]
        else:
            return {}

    def generate_image(self):
        raw = self.system.generate_image(prompt=self.get_image_prompt())
        self.asset_id = self._storage.save(
            raw,
            folder=self.asset_folder,
        )
        self.save()
        try:
            result = self._storage.get_url(self.asset_id)
        except Exception as e:
            log(e)
            self.asset_id = ""
            return "https://picsum.photos/300/?blur"
        else:
            return result

    def update_image_url(self, url):
        # log(url)
        response = requests.get(url)
        if response.status_code == 200 and response.headers["Content-Type"].startswith(
            "image/"
        ):
            self.asset_id = self._storage.save(
                response.content, folder=self.asset_folder, crop=True
            )
            self.save()
        try:
            return self._storage.get_url(self.asset_id)
        except Exception as e:
            log(e)
            self.asset_id = ""
            return "https://picsum.photos/300/?blur"

    def image(self, size="orig", asset_id=None):
        # log(self.asset_id, self.image_data, self._storage.get_url(self.asset_id, size))
        if asset_id and self._storage.get_url(self.asset_id):
            self.asset_id = asset_id
            self.save()

        if not self.asset_id:
            try:
                images = self._storage.search(folder=self.asset_folder)
                self.asset_id = random.choice(images)
            except Exception as e:
                log(e)
                return "https://picsum.photos/500/?blur"
            else:
                # log(self.asset_folder, images)
                self.save()
        # log(self.asset_id, self._storage.get_url(self.asset_id, size))
        try:
            return self._storage.get_url(self.asset_id, size)
        except Exception as e:
            log(e)
            self.asset_id = ""
            return "https://picsum.photos/300/?blur"

    def get_image_prompt(self):
        return f"Create an image of a {self.title}"

    def generate_battlemap(self):
        # log(f"Generating battlemap for {self.title} {self.name}...with AI")
        if raw := self.system.generate_battlemap(self):
            img_path = f"{self.genre}/battlemaps"
            self.battlemap = self._storage.save(raw, folder=img_path)
            self.save()
        result = self.battlemap_url
        log(result)
        return result

    def get_map_list(self):
        # log(self._storage.base_path, self._storage.search(folder=self.asset_folder))
        if images := self._storage.search(f"{self.genre}/battlemaps"):
            image_list = random.sample(
                images, k=min(len(images), MAX_NUM_IMAGES_IN_GALLERY)
            )
            return [
                {"asset_id": image, "url": self._storage.get_url(image, size=100)}
                for image in image_list
            ]
        else:
            return {}

    def update_battlemap_url(self, url):
        response = requests.get(url)
        log(url, response.status_code, response.headers["Content-Type"], response.text)
        if response.status_code == 200 and response.headers["Content-Type"].startswith(
            "image/"
        ):
            self.battlemap = self._storage.save(
                response.content, folder=f"{self.genre}/battlemaps"
            )
            self.save()
            return self._storage.get_url(self.battlemap)

    ############# Instance Methods #############

    def get_start_month(self):
        return self.system.calendar["months"][self.start_date["month"]]

    def get_end_month(self):
        return self.system.calendar["months"][self.end_date["month"]]

    def add_association(self, pk, model):
        if obj := AutoModel.load_model(model.title()).get(pk):
            self.associations.append(obj)
            self.save()
            return obj

    def search_autocomplete(self, query):
        results = {}
        for title, model in self.get_world().child_models.items():
            objs = model.search(name=query, _FUZZY_SEARCH=True)
            results[title] = [o for o in objs if o.get_world() == self.get_world()]
        return results

    def add_journal_entry(
        self,
        pk=None,
        title=None,
        text=None,
        tags=[],
        importance=0,
        date=None,
        associations=None,
    ):
        normalized_associations = []
        if associations:
            for entity in associations:
                if model := AutoModel.load_model(entity.get("model")):
                    if obj := model[0].get(entity.get("pk")):
                        normalized_associations.append(obj)
                else:
                    raise ValueError(f"Invalid model: {entity.get('model')}")

        if pk:
            return self.journal.update_entry(
                pk=pk,
                title=title,
                text=text,
                tags=tags,
                importance=importance,
                date=date,
                associations=normalized_associations,
            )
        else:
            return self.journal.add_entry(
                title=title,
                text=text,
                tags=tags,
                importance=importance,
                date=date,
                associations=normalized_associations,
            )

    def model_title(self, obj_class):
        return self.get_world().system.get_title(obj_class)

    def get_world(self):
        if self.__class__.__name__ == "World":
            return self
        return self.world

    def get_children(self, model):
        log(model)
        if not isinstance(model, str):
            model = model.__name__
        children_name = self.child_list_key(model.lower())
        results = getattr(self, children_name, [])
        return results

    def page_data(self):
        return {}

    @property
    def state_data(self):
        return {
            "attributes": {
                "pk": self.pk,
                "name": self.name,
                "title": self.title,
                "parent": self.parent.pk if self.parent else None,
                "desc": self.description,
                "traits": self.traits,
                "asset_id": self.asset_id,
                "associations": [assoc.pk for assoc in self.associations],
                "backstory": self.backstory,
                "start_date": self.start_date,
                "end_date": self.end_date,
                "age": self.age,
            },
            "world": self.get_world().serialize(),
            "genre": self.genre,
            "geneology": {
                "ancestors": [ancestor.pk for ancestor in self.geneology],
                "children": {},
            },
            "backstory_summary": self.backstory_summary,
            "image": self.image_url,
            "battlemap": self.battlemap_url,
            "start_date_str": self.start_date_str,
            "end_date_str": self.end_date_str,
            "api_path": self.api_path(),
            "page_path": self.page_path(),
            "task_path": self.task_path(),
            # "map_path": self.map_path(),
            "card_content": self.card_content(),
            "journal": [entry.pk for entry in self.journal.entries],
        }

    def page_content(self, user=None, template="_components", macro="detail", **kwargs):
        template_file = f"{template}.html"
        # log(template_file, macro)
        return get_template_attribute(template_file, macro)(
            user=user, obj=self, **kwargs
        )

    def menu_content(self, user=None):
        return self.page_content(
            user=user, template=f"pages/_{self.model_name().lower()}", macro="menu"
        )

    def card_content(self, user=None):
        return self.page_content(user=user, macro="card")
