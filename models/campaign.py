# from autonomous.model.autoattribute import AutoAttribute
from datetime import datetime

from autonomous import log
from autonomous.model.autoattribute import AutoAttribute
from autonomous.model.automodel import AutoModel
from autonomous.tasks import AutoTasks
from models.journal import Journal, JournalEntry


class Campaign(AutoModel):
    attributes = {
        "name": AutoAttribute(type="TEXT", required=True),
        "description": "",
        "_world": AutoAttribute(type="MODEL", required=True),
        "_sessions": AutoAttribute(type="MODEL"),
        "_players": [],
    }

    def delete(self):
        self.sessions.delete()
        super().delete()

    @property
    def sessions(self):
        if self._sessions is None:
            self._sessions = Journal(_world=self.world, _parent=self.world)
            self._sessions.save()
            self.save()
        return self._sessions.entries

    @sessions.setter
    def sessions(self, value):
        if isinstance(
            value,
            (
                Journal,
                type(None),
            ),
        ):
            self._sessions.entries = value
        else:
            raise TypeError(
                f"Session entries must be a Journal object or None, not {type(value)}"
            )

    @property
    def summary(self):
        return self._sessions.summary

    @summary.setter
    def summary(self, value):
        self._sessions.summary = value

    @property
    def world(self):
        return self._world

    @world.setter
    def world(self, value):
        self._world = value

    def update_session(self, **kwargs):
        if pk := kwargs.pop("pk", None):
            entry = self._sessions.update_entry(pk=pk, **kwargs)
        else:
            entry = self._sessions.add_entry(**kwargs)
        self.save()
        return entry

    def add_association(self, session, obj):
        if entry := JournalEntry.get(session.pk):
            return entry.add_association(obj)

    def get_session(self, session_pk):
        session = JournalEntry.get(session_pk)
        return session if session in self.sessions else None

    def page_data(self):
        return {
            "name": self.name,
            "description": self.description,
        }
