import factory

from core.models import ClientApplication
from users.tests.user_factory import UserFactory


class ClientApplicationFactory(factory.django.DjangoModelFactory):
    partner = factory.SubFactory(UserFactory)

    class Meta:
        model = ClientApplication
