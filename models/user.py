from models.world import World

from autonomous import log
from autonomous.auth.user import AutoUser


class User(AutoUser):
    # set model default attributes
    attributes = AutoUser.attributes | {"world_pks": [], "admin": False}

    def world_owner(self, obj):
        # log(f"user pk {self.pk}", f"world_pks : {self.world_pks}")
        return hasattr(obj, "user") and obj.user == self

    def world_user(self, obj):
        # log(f"user pk {self.pk}", f"world_pks : {self.world_pks}")
        return obj.get_world().pk in self.world_pks or self in obj.subusers

    def add_world(self, obj):
        if isinstance(obj, World):
            pk = obj.pk
        if isinstance(obj, str):
            pk = obj
            obj = World.get(pk)
        if pk not in self.world_pks:
            obj.user = self
            obj.save()
            self.world_pks.append(pk)
            self.save()

    @property
    def worlds(self):
        result = []
        for w_pk in self.world_pks:
            w = World.get(w_pk)
            result.append(w)
        self.save()
        return result
