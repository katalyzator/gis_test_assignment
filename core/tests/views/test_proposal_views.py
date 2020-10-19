from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from core.constants import CONSUMER
from core.tests.proposal_factories import ProposalFactory, OrganizationFactory
from users import roles
from users.tests.user_factory import UserFactory


class ProposalTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory(email="user@example.com", first_name='John', last_name='Smith',
                                role_id=roles.ADMINISTRATOR['codename'])
        token = Token.objects.create(user=self.user)
        self.organization = OrganizationFactory(name='Test organization')
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        self.url = reverse('v1:proposals')

    def test_success_proposal_list_view(self):
        ProposalFactory(organization=self.organization, min_score=0, max_score=100)
        ProposalFactory(organization=self.organization, min_score=0, max_score=100)
        ProposalFactory(organization=self.organization, min_score=0, max_score=100)

        response = self.client.get(self.url)

        response_json = response.json()
        self.assertEqual(response_json['total_count'], 3)

    def test_success_proposal_creation_given_valid_data(self):
        input_data = {
            'organization': self.organization.id,
            'name': 'Test',
            'credit_type': CONSUMER,
            'start_rotation_date': '2015-10-22T09:32:02.788611Z',
            'end_rotation_date': '2015-10-22T09:32:02.788611Z',
            'min_score': 0,
            'max_score': 100
        }

        response = self.client.post(self.url, input_data)

        expected_data = {
            'id': response.json()['id'],
            'name': 'Test',
            'credit_type': CONSUMER,
            'start_rotation_date': '2015-10-22T09:32:02.788611Z',
            'end_rotation_date': '2015-10-22T09:32:02.788611Z',
            'min_score': 0.0,
            'max_score': 100.0,
            'organization': {
                'id': self.organization.id,
                'name': 'Test organization'
            }
        }

        self.assertEqual(response.data, expected_data)
