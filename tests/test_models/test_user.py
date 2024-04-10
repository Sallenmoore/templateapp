import pytest
from models.user import User
from models.world import World


# @pytest.mark.skip("Working")
class TestUser:
    def test_init(self):
        user = User(name="test", email="email@test")
        user.save()
        world = World(user=user, system="fantasy", name="MagicWorld")
        world.save()
        assert isinstance(user, User)
        assert len(user.world_pks) == 1
        assert user.admin is False

    def test_world_owner(self):
        user = User(name="test", email="email@test")
        user.save()
        world = World(user=user, system="fantasy", name="MagicWorld")
        world.save()
        user.add_world(world)
        assert user.world_owner(world) is True
        user.add_world(world.pk)
        assert user.world_owner(world) is True

    def test_worlds(self):
        user = User(name="test", email="email@test")
        user.save()
        world = World(user=user, system="fantasy", name="MagicWorld")
        world.save()
        # breakpoint()
        user.add_world(world)
        assert world in user.worlds
        assert world.user == user
