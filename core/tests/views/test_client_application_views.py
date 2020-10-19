from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from core.tests.client_application_factory import ClientApplicationFactory
from users import roles
from users.tests.user_factory import UserFactory


class ClientApplicationCreateTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory(email="user@example.com", first_name='John', last_name='Smith',
                                role_id=roles.ADMINISTRATOR['codename'])
        token = Token.objects.create(user=self.user)

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        self.url = reverse('v1:client_applications')

    def test_success_client_application_list_given_administrator_role(self):
        ClientApplicationFactory(date_of_birth='2020-10-10', score=100)
        ClientApplicationFactory(date_of_birth='2020-10-10', score=100)
        ClientApplicationFactory(date_of_birth='2020-10-10', score=100)

        response = self.client.get(self.url)

        response_json = response.json()
        self.assertEqual(response_json['total_count'], 3)

    def test_success_client_application_list_given_partner_role(self):
        user = UserFactory(email='user1@example.com',
                           role_id=roles.PARTNER['codename'])
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        # create three application with current partner and one application with not current partner

        ClientApplicationFactory(date_of_birth='2020-10-10', score=100, partner=user)
        ClientApplicationFactory(date_of_birth='2020-10-10', score=100, partner=user)
        ClientApplicationFactory(date_of_birth='2020-10-10', score=100, partner=user)

        ClientApplicationFactory(date_of_birth='2020-10-10', score=100, partner=self.user)

        response = self.client.get(self.url)

        response_json = response.json()
        self.assertEqual(response_json['total_count'], 3)

    def test_success_client_application_creation_with_valid_data(self):
        input_data = {
            'partner': self.user.id,
            'first_name': 'Bob',
            'last_name': 'Martin',
            'middle_name': 'Petrovich',
            'date_of_birth': '1996-02-12',
            'phone_number': '+996777666555',
            'passport_number': 'AN54325325',
            'score': 100.0
        }
        response = self.client.post(self.url, input_data)

        expected_data = {
            'id': 1,
            'first_name': 'Bob',
            'last_name': 'Martin',
            'middle_name': 'Petrovich',
            'date_of_birth': '1996-02-12',
            'phone_number': '+996777666555',
            'passport_number': 'AN54325325',
            'score': 100.0,
            'partner': {
                'id': self.user.id,
                'first_name': 'John',
                'last_name': 'Smith',
                'email': 'user@example.com'
            }
        }

        self.assertEqual(response.data, expected_data)

    def test_permission_denied_error_given_organization_specialist_role(self):
        user = UserFactory(email='user1@example.com',
                           role_id=roles.ORGANIZATION_SPECIALIST['codename'])
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        input_data = {
            'partner': self.user.id,
            'first_name': 'Bob',
            'last_name': 'Martin',
            'middle_name': 'Petrovich',
            'date_of_birth': '1996-02-12',
            'phone_number': '+996777666555',
            'passport_number': 'AN54325325',
            'score': 100.0
        }
        response = self.client.post(self.url, input_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ClientApplicationRetrieveTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory(email="user@example.com", first_name='John', last_name='Smith',
                                role_id=roles.ADMINISTRATOR['codename'])
        token = Token.objects.create(user=self.user)
        self.application = ClientApplicationFactory(date_of_birth='2020-10-10', score=100)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        self.url = reverse('v1:client_applications_retrieve', kwargs={'pk': self.application.id})

    def test_success_client_application_retrieve_given_administrator_role(self):
        response = self.client.get(self.url)

        response_json = response.json()
        expected_response = {'id': self.application.id,
                             'partner': {'id': self.application.partner.id, 'first_name': '', 'last_name': '',
                                         'email': self.application.partner.email},
                             'first_name': '', 'last_name': '', 'middle_name': '', 'date_of_birth': '2020-10-10',
                             'phone_number': '', 'passport_number': '', 'score': 100.0}

        self.assertEqual(expected_response, response_json)

    def test_success_client_application_retrieve_given_partner_role(self):
        partner = UserFactory(email="user1@example.com", first_name='John', last_name='Smith',
                              role_id=roles.PARTNER['codename'])
        token = Token.objects.create(user=partner)
        application = ClientApplicationFactory(date_of_birth='2020-10-10', score=100, partner=partner)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        url = reverse('v1:client_applications_retrieve', kwargs={'pk': application.id})

        response = self.client.get(url)
        response_json = response.json()

        expected_response = {'id': application.id,
                             'partner': {'id': partner.id, 'first_name': 'John', 'last_name': 'Smith',
                                         'email': application.partner.email},
                             'first_name': '', 'last_name': '', 'middle_name': '', 'date_of_birth': '2020-10-10',
                             'phone_number': '', 'passport_number': '', 'score': 100.0}

        self.assertEqual(expected_response, response_json)

    def test_error_client_application_retrieve_given_org_specialist_role(self):
        user = UserFactory(email="user1@example.com", first_name='John', last_name='Smith',
                           role_id=roles.ORGANIZATION_SPECIALIST['codename'])
        token = Token.objects.create(user=user)
        application = ClientApplicationFactory(date_of_birth='2020-10-10', score=100)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        url = reverse('v1:client_applications_retrieve', kwargs={'pk': application.id})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_success_client_application_update_given_administrator_role(self):
        input_data = {
            'partner': self.user.id,
            'first_name': 'Bob',
            'last_name': 'Martin',
            'middle_name': 'Petrovich',
            'date_of_birth': '1996-02-12',
            'phone_number': '+996777666555',
            'passport_number': 'AN54325325',
            'score': 99
        }

        response = self.client.put(self.url, input_data)

        response_json = response.json()
        expected_response = {'id': self.application.id,
                             'partner': {'id': self.user.id, 'first_name': 'John', 'last_name': 'Smith',
                                         'email': self.user.email},
                             'first_name': 'Bob', 'last_name': 'Martin', 'middle_name': 'Petrovich',
                             'date_of_birth': '1996-02-12', 'phone_number': '+996777666555',
                             'passport_number': 'AN54325325', 'score': 99.0}

        self.assertEqual(expected_response, response_json)

    def test_error_client_application_update_given_not_administrator_role(self):
        user = UserFactory(email="user1@example.com", first_name='John', last_name='Smith',
                           role_id=roles.ORGANIZATION_SPECIALIST['codename'])
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        input_data = {
            'partner': self.user.id,
            'first_name': 'Bob',
            'last_name': 'Martin',
            'middle_name': 'Petrovich',
            'date_of_birth': '1996-02-12',
            'phone_number': '+996777666555',
            'passport_number': 'AN54325325',
            'score': 99
        }

        response = self.client.put(self.url, input_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_success_delete_application_given_administrator_role(self):
        user = UserFactory(email="user43@example.com", first_name='John', last_name='Smith',
                           role_id=roles.ADMINISTRATOR['codename'])
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        application = ClientApplicationFactory(date_of_birth='2020-10-10', score=100)
        url = reverse('v1:client_applications_retrieve', kwargs={'pk': application.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_error_delete_application_given_not_administrator_role(self):
        user = UserFactory(email="user123@example.com", first_name='John', last_name='Smith',
                           role_id=roles.PARTNER['codename'])
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        application = ClientApplicationFactory(date_of_birth='2020-10-10', score=100)
        url = reverse('v1:client_applications_retrieve', kwargs={'pk': application.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
