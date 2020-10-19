import factory

from core.models import Proposal, Organization


class OrganizationFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('name')

    class Meta:
        model = Organization


class ProposalFactory(factory.django.DjangoModelFactory):
    organization = factory.SubFactory(OrganizationFactory)
    start_rotation_date = factory.Faker('date_object')
    end_rotation_date = factory.Faker('date_object')

    class Meta:
        model = Proposal
