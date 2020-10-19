import factory

from core.models import OrganizationClientApplication
from core.tests.client_application_factory import ClientApplicationFactory
from core.tests.proposal_factories import ProposalFactory


class OrganizationClientApplicationFactory(factory.django.DjangoModelFactory):
    proposal = factory.SubFactory(ProposalFactory)
    client_application = factory.SubFactory(ClientApplicationFactory)

    class Meta:
        model = OrganizationClientApplication
