import factory
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

from users.models import Role

User = get_user_model()


class RoleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Role


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f'user_{n}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'foo')
    is_active = True


class TokenFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(User)

    class Meta:
        model = Token
