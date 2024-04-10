import pytest
from autonomous.auth.user import AutoUser
from models.user import User


class TestAuth:
    def test_autouser(self):
        AutoUser.table().flush_table()
        user_info = {
            "name": "test",
            "email": "test@test.com",
            "token": "testtoken",
        }
        user = AutoUser.authenticate(user_info)
        # breakpoint()
        user2 = AutoUser.authenticate(user_info)
        assert user.pk == user2.pk
        user.state = "unauthenticated"
        assert not user.is_authenticated
        pk = user.save()
        user = AutoUser.authenticate(user_info)
        assert pk == user.pk == user2.pk
        assert user.is_authenticated

    def test_user(self):
        User.table().flush_table()

        user_info = {
            "name": "test",
            "email": "test@test.com",
            "token": "testtoken",
        }
        user = User.authenticate(user_info)
        user2 = User.authenticate(user_info)
        assert user.pk == user2.pk
        user.state = "unauthenticated"
        assert not user.is_authenticated
        pk = user.save()
        user = User.authenticate(user_info)
        assert pk == user.pk == user2.pk
        assert user.is_authenticated
