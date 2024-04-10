# from autonomous.model.autoattribute import AutoAttribute
from datetime import datetime

from flask import get_template_attribute

from autonomous import log
from autonomous.model.automodel import AutoModel
from autonomous.tasks import AutoTasks


class JournalEntry(AutoModel):
    attributes = {
        "_title": "",
        "_text": "",
        "_summary": "",
        "_tags": [],
        "_date": "",
        "_importance": 0,
        "_associations": [],
    }

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if value != self._text:
            self._summary = ""
        self._text = value

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        self._date = value

    @property
    def importance(self):
        return self._importance

    @importance.setter
    def importance(self, value):
        try:
            value = int(value)
            if isinstance(value, int) and 0 <= value <= 5:
                self._importance = value
        except Exception as e:
            raise ValueError(f"{e} -- Importance must be an integer '0-5', not {value}")

    @property
    def associations(self):
        ## TEMP BUGFIX
        if self._associations is None:
            self._associations = []
        # log(self._associations)
        for idx, obj in enumerate(self._associations):
            if isinstance(obj, dict) and "model" in obj:
                ModelStr = {"poi": "POI"}.get(
                    obj["model"].lower(), obj["model"].title()
                )
                if Model := AutoModel.load_model(model=ModelStr):
                    self._associations[idx] = Model.get(obj["pk"])
                else:
                    raise ValueError(f"Model {obj['model']} not found")
        ###
        # log(self._associations)
        return self._associations

    @associations.setter
    def associations(self, value):
        for idx, obj in enumerate(value):
            if isinstance(obj, dict) and "model" in obj:
                ModelStr = {"poi": "POI"}.get(
                    obj["model"].lower(), obj["model"].title()
                )
                if Model := AutoModel.load_model(model=ModelStr):
                    value[idx] = Model.get(obj["pk"])
                else:
                    raise ValueError(f"Model {obj['model']} not found")

        self._associations = value
        # log(self._associations)

    @property
    def summary(self):
        return self._summary

    @summary.setter
    def summary(self, value):
        self._summary = value

    def add_association(self, obj):
        if isinstance(obj, dict) and "model" in obj:
            ModelStr = {"poi": "POI"}.get(obj["model"].lower(), obj["model"].title())
            if Model := AutoModel.load_model(model=ModelStr):
                obj = Model.get(obj["pk"])
            else:
                raise ValueError(f"Model {obj['model']} not found")
        else:
            raise ValueError(f"Association must be a dict, not {type(obj)}")

        if obj not in self.associations:
            self.associations.append(obj)
            self.save()
        # else:
        #     log(f"{obj.name} is already associated with entry: {self.pk}")
        return self

    def page_content(
        self,
        template="pages/_shared_components.html",
        macro="journal_entry",
        user=None,
        **kwargs,
    ):
        user = kwargs.get("user")
        return get_template_attribute(template, macro)(user=user, obj=self, **kwargs)


class Journal(AutoModel):
    attributes = {
        "_entries": [],
        "_world": None,
        "_parent": None,
        "_summary": "",
    }

    @classmethod
    def _summarize(cls, pk):
        obj = cls.get(pk)
        text = ""
        entries = sorted(obj.entries, key=lambda x: x.title)
        for entry in entries:
            if not entry.summary.strip() and len(entry.text) > 80:
                entry.summary = obj.world.system.generate_summary(
                    entry.text, primer="Try to keep the summary less than 75 words"
                )
                entry.save()
            text += f"{entry.summary}\n\n"
        obj.summary = obj.world.system.generate_summary(text)
        obj.save()

    def delete(self):
        for entries in self.entries:
            entries.delete()
        super().delete()

    @property
    def entries(self):
        self._entries = sorted(self._entries, key=lambda x: x.title, reverse=True)
        self.save()
        return self._entries

    @entries.setter
    def entries(self, value):
        if isinstance(value, list):
            self._entries = value
        else:
            raise TypeError(f"Journal entries must be a list, not {type(value)}")

    @property
    def summary(self):
        if not self._summary.strip():
            AutoTasks().task(Journal._summarize, pk=self.pk)
        return self._summary

    @summary.setter
    def summary(self, value):
        self._summary = value

    @property
    def world(self):
        return self._world

    @world.setter
    def world(self, value):
        self._world = value

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value

    def add_entry(
        self,
        title=None,
        text=None,
        importance=0,
        date=None,
        associations=None,
    ):
        entry = JournalEntry()
        entry.title = title or f"Journal Entry ({len(self.entries) + 1})"
        entry.text = text or "Something of some importance happened. More soon..."
        entry.date = date or datetime.now()
        entry.importance = importance
        entry.summary = ""
        entry.save()
        self.entries.append(entry)
        if associations:
            for assoc in associations:
                entry.add_association(assoc)
        self.summary = ""
        self.save()
        return entry

    def update_entry(
        self,
        pk,
        title=None,
        text=None,
        importance=None,
        date=None,
        associations=None,
    ):
        if entry := JournalEntry.get(pk):
            entry.title = title or entry.title
            entry.text = text or entry.text
            entry.date = date or entry.date
            entry.importance = importance or entry.importance
            if associations:
                for assoc in associations:
                    entry.add_association(assoc)
            entry.summary = ""
            entry.save()
            self.summary = ""
            self.save()
        return entry

    def get_entry(self, entry_pk):
        entry = JournalEntry.get(entry_pk)
        return entry if entry in self.entries else None
