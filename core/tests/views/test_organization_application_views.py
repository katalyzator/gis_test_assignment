from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from core.constants import ACCEPTED, NEW, DECLINED
from core.tests.client_application_factory import ClientApplicationFactory
from core.tests.organization_application_factories import OrganizationClientApplicationFactory
from core.tests.proposal_factories import ProposalFactory, OrganizationFactory
from users import roles
from users.tests.user_factory import UserFactory


class OrganizationClientApplicationCreateTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory(email="user@example.com", first_name='John', last_name='Smith',
                                role_id=roles.ADMINISTRATOR['codename'])
        token = Token.objects.create(user=self.user)

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        self.url = reverse('v1:organization_applications')

        self.org_specialist = UserFactory(email="user1@example.com", first_name='John', last_name='Smith',
                                          role_id=roles.ORGANIZATION_SPECIALIST['codename'])
        self.organization = OrganizationFactory(name='test_organization')
        self.organization.employers.add(self.org_specialist)

        self.partner = UserFactory(email="user2@example.com", first_name='John', last_name='Smith',
                                   role_id=roles.PARTNER['codename'])

        self.client_application = ClientApplicationFactory(date_of_birth='2020-10-10', score=100, partner=self.partner)

        self.proposal = ProposalFactory(organization=self.organization, min_score=0, max_score=100)
        self.maxDiff = None

    def test_success_org_client_application_list_given_administrator_role(self):
        for _ in range(3):
            OrganizationClientApplicationFactory(proposal=self.proposal, client_application=self.client_application)

        response = self.client.get(self.url)

        response_json = response.json()
        self.assertEqual(response_json['total_count'], 3)

    def test_success_org_client_application_list_given_org_specialist_role(self):
        for _ in range(2):
            OrganizationClientApplicationFactory(proposal=self.proposal, client_application=self.client_application)

        token = Token.objects.create(user=self.org_specialist)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.get(self.url)

        response_json = response.json()
        self.assertEqual(response_json['total_count'], 2)

    def test_success_org_client_application_list_given_partner_role(self):
        for _ in range(4):
            OrganizationClientApplicationFactory(proposal=self.proposal, client_application=self.client_application)

        token = Token.objects.create(user=self.partner)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.get(self.url)

        response_json = response.json()
        self.assertEqual(response_json['total_count'], 4)

    def test_success_org_client_application_creation_given_all_filled_data(self):
        input_data = {
            'proposal': self.proposal.id,
            'client_application': self.client_application.id,
            'status': ACCEPTED
        }

        response = self.client.post(self.url, input_data)

        expected_response = {'id': response.json()['id'],
                             'client_application': {
                                 'id': self.client_application.id,
                                 'partner': {
                                     'id': self.partner.id, 'first_name': 'John',
                                     'last_name': 'Smith',
                                     'email': 'user2@example.com'
                                 },
                                 'first_name': '', 'last_name': '', 'middle_name': '',
                                 'date_of_birth': '2020-10-10', 'phone_number': '',
                                 'passport_number': '', 'score': 100.0
                             },
                             'proposal': {
                                 'id': self.proposal.id,
                                 'name': '',
                                 'credit_type': '',
                                 'organization': {
                                     'id': self.organization.id, 'name': 'test_organization'
                                 },
                                 'start_rotation_date': str(self.proposal.start_rotation_date) + 'T00:00:00Z',
                                 'end_rotation_date': str(self.proposal.end_rotation_date) + 'T00:00:00Z',
                                 'min_score': 0.0,
                                 'max_score': 100.0
                             },
                             'status': 'accepted'
                             }

        self.assertEqual(response.json(), expected_response)


class OrganizationClientApplicationRetrieveTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory(email="user@example.com", first_name='John', last_name='Smith',
                                role_id=roles.ADMINISTRATOR['codename'])
        token = Token.objects.create(user=self.user)

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        self.org_specialist = UserFactory(email="user1@example.com", first_name='John', last_name='Smith',
                                          role_id=roles.ORGANIZATION_SPECIALIST['codename'])
        self.organization = OrganizationFactory(name='test_organization')
        self.organization.employers.add(self.org_specialist)

        self.partner = UserFactory(email="user2@example.com", first_name='John', last_name='Smith',
                                   role_id=roles.PARTNER['codename'])

        self.client_application = ClientApplicationFactory(date_of_birth='2020-10-10', score=100, partner=self.partner)

        self.proposal = ProposalFactory(organization=self.organization, min_score=0, max_score=100)

        self.org_application = OrganizationClientApplicationFactory(proposal=self.proposal,
                                                                    client_application=self.client_application)

        self.url = reverse('v1:organization_applications_detail', kwargs={'pk': self.org_application.id})

    def test_success_org_client_application_retrieve_given_administrator_role(self):
        response = self.client.get(self.url)

        expected_data = {
            'id': self.org_application.id,
            'client_application': {
                'id': self.client_application.id,
                'partner': {
                    'id': self.partner.id,
                    'first_name': 'John',
                    'last_name': 'Smith',
                    'email': 'user2@example.com'
                },
                'first_name': '',
                'last_name': '',
                'middle_name': '',
                'date_of_birth': '2020-10-10',
                'phone_number': '',
                'passport_number': '',
                'score': 100.0
            },
            'proposal': {
                'id': self.proposal.id,
                'name': '',
                'credit_type': '',
                'organization': {
                    'id': self.organization.id,
                    'name': 'test_organization'
                },
                'start_rotation_date': str(self.proposal.start_rotation_date) + 'T00:00:00Z',
                'end_rotation_date': str(self.proposal.end_rotation_date) + 'T00:00:00Z',
                'min_score': 0.0,
                'max_score': 100.0
            },
            'status': 'new'
        }

        self.assertEqual(response.json(), expected_data)

    def test_success_org_client_application_retrieve_given_non_linked_user(self):
        empty_user = UserFactory(email="user100@example.com", first_name='John', last_name='Smith',
                                 role_id=roles.PARTNER['codename'])
        token = Token.objects.create(user=empty_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_success_update_org_application_given_administrator_role(self):
        another_proposal = ProposalFactory(organization=self.organization, min_score=0, max_score=85)
        input_data = {
            'proposal': another_proposal.id,
            'client_application': self.client_application.id,
            'status': NEW
        }

        response = self.client.put(self.url, input_data)

        expected_data = {
            'id': self.org_application.id,
            'client_application': {
                'id': self.client_application.id,
                'partner': {
                    'id': self.partner.id,
                    'first_name': 'John',
                    'last_name': 'Smith',
                    'email': 'user2@example.com'
                },
                'first_name': '',
                'last_name': '',
                'middle_name': '',
                'date_of_birth': '2020-10-10',
                'phone_number': '',
                'passport_number': '',
                'score': 100.0
            },
            'proposal': {
                'id': another_proposal.id,
                'name': '',
                'credit_type': '',
                'organization': {
                    'id': self.organization.id,
                    'name': 'test_organization'
                },
                'start_rotation_date': str(another_proposal.start_rotation_date) + 'T00:00:00Z',
                'end_rotation_date': str(another_proposal.end_rotation_date) + 'T00:00:00Z',
                'min_score': 0.0,
                'max_score': 85.0
            },
            'status': 'new'
        }

        self.assertEqual(expected_data, response.json())

    def test_error_update_org_application_given_not_administrator_role(self):
        incorrect_user = UserFactory(email="user100@example.com", first_name='John', last_name='Smith',
                                     role_id=roles.PARTNER['codename'])
        token = Token.objects.create(user=incorrect_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        another_proposal = ProposalFactory(organization=self.organization, min_score=0, max_score=85)
        input_data = {
            'proposal': another_proposal.id,
            'client_application': self.client_application.id,
            'status': NEW
        }

        response = self.client.put(self.url, input_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_success_remove_org_application_given_administrator_role(self):
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_error_remove_org_application_given_not_role(self):
        incorrect_user = UserFactory(email="user100@example.com", first_name='John', last_name='Smith',
                                     role_id=roles.PARTNER['codename'])
        token = Token.objects.create(user=incorrect_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class OrganizationClientApplicationChangeStatusTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory(email="user@example.com", first_name='John', last_name='Smith',
                                role_id=roles.ADMINISTRATOR['codename'])
        token = Token.objects.create(user=self.user)

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        self.org_specialist = UserFactory(email="user1@example.com", first_name='John', last_name='Smith',
                                          role_id=roles.ORGANIZATION_SPECIALIST['codename'])
        self.organization = OrganizationFactory(name='test_organization')
        self.organization.employers.add(self.org_specialist)

        self.partner = UserFactory(email="user2@example.com", first_name='John', last_name='Smith',
                                   role_id=roles.PARTNER['codename'])

        self.client_application = ClientApplicationFactory(date_of_birth='2020-10-10', score=100, partner=self.partner)

        self.proposal = ProposalFactory(organization=self.organization, min_score=0, max_score=100)

        self.org_application = OrganizationClientApplicationFactory(proposal=self.proposal,
                                                                    client_application=self.client_application)

        self.url = reverse('v1:change_org_application_status', kwargs={'pk': self.org_application.id})

    def test_success_org_client_application_change_status_given_valid_status(self):
        input_data = {
            'status': DECLINED
        }
        response = self.client.post(self.url, input_data)

        expected_data = {
            'id': self.org_application.id,
            'client_application': {
                'id': self.client_application.id,
                'partner': {
                    'id': self.partner.id,
                    'first_name': 'John',
                    'last_name': 'Smith',
                    'email': 'user2@example.com'
                },
                'first_name': '',
                'last_name': '',
                'middle_name': '',
                'date_of_birth': '2020-10-10',
                'phone_number': '',
                'passport_number': '',
                'score': 100.0
            },
            'proposal': {
                'id': self.proposal.id,
                'name': '',
                'credit_type': '',
                'organization': {
                    'id': self.organization.id,
                    'name': 'test_organization'
                },
                'start_rotation_date': str(self.proposal.start_rotation_date) + 'T00:00:00Z',
                'end_rotation_date': str(self.proposal.end_rotation_date) + 'T00:00:00Z',
                'min_score': 0.0,
                'max_score': 100.0
            },
            'status': DECLINED
        }

        self.assertEqual(response.json(), expected_data)
