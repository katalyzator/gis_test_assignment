from django.contrib.auth import get_user_model

from users import roles

User = get_user_model()


class UserService:
    model = User

    @classmethod
    def is_administrator_user(cls, user: User) -> bool:
        return user.role.codename == roles.ADMINISTRATOR['codename']
