from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.db.models import QuerySet

from common.exceptions import (
    ObjectNotFoundException, IntegrityException,
    PermissionDeniedException)
from users import roles
from .models import (
    ClientApplication, Proposal, Organization,
    OrganizationClientApplication)

User = get_user_model()


class ClientApplicationService:
    model = ClientApplication

    @classmethod
    def filter(cls, **filters) -> QuerySet:
        return cls.model.objects.filter(**filters)

    @classmethod
    def get(cls, **filters) -> ClientApplication:
        try:
            return cls.model.objects.get(**filters)
        except cls.model.DoesNotExist:
            raise ObjectNotFoundException('Application not found')

    @classmethod
    def get_application(cls, user: User, application_pk) -> ClientApplication:
        application = cls.get(pk=application_pk)
        if user.role.codename == roles.PARTNER['codename'] and application.partner == user:
            return application
        elif user.role.codename == roles.ORGANIZATION_SPECIALIST['codename']:
            raise PermissionDeniedException('You do not have permission to perform this action')

        return application

    @classmethod
    def delete_application(cls, application_pk) -> None:
        application = cls.get(pk=application_pk)
        application.delete()

    @classmethod
    def create(cls, partner: User, first_name: str, last_name: str,
               middle_name: str, date_of_birth, phone_number: str,
               passport_number: str, score: float) -> ClientApplication:
        try:
            return cls.model.objects.create(
                partner=partner,
                first_name=first_name,
                last_name=last_name,
                middle_name=middle_name,
                date_of_birth=date_of_birth,
                phone_number=phone_number,
                passport_number=passport_number,
                score=score
            )
        except IntegrityError as e:
            raise IntegrityException('Error while creating Application {e}'.format(e=str(e)))

    @classmethod
    def update(cls, application: ClientApplication, first_name: str, last_name: str,
               middle_name: str, date_of_birth, phone_number: str, partner: User,
               passport_number: str, score: float) -> ClientApplication:

        try:
            application.partner = partner
            application.first_name = first_name
            application.last_name = last_name
            application.middle_name = middle_name
            application.date_of_birth = date_of_birth
            application.phone_number = phone_number
            application.passport_number = passport_number
            application.score = score
            application.save()

            return application

        except IntegrityError as e:
            raise IntegrityException('Error while updating Application {e}'.format(e=str(e)))


class ProposalService:
    model = Proposal

    @classmethod
    def get(cls, **filters) -> Proposal:
        try:
            return cls.model.objects.get(**filters)
        except cls.model.DoesNotExist:
            raise ObjectNotFoundException('Proposal not found')

    @classmethod
    def filter(cls, **filters) -> QuerySet:
        return cls.model.objects.filter(**filters)

    @classmethod
    def create(cls, organization: Organization, name: str, credit_type: str,
               start_rotation_date, end_rotation_date,
               min_score: float, max_score: float) -> Proposal:
        try:
            return cls.model.objects.create(
                organization=organization,
                name=name,
                credit_type=credit_type,
                start_rotation_date=start_rotation_date,
                end_rotation_date=end_rotation_date,
                min_score=min_score,
                max_score=max_score
            )
        except IntegrityError as e:
            raise IntegrityException('Error while creating Proposal {e}'.format(e=str(e)))


class OrganizationClientApplicationService:
    model = OrganizationClientApplication

    @classmethod
    def get(cls, **filters):
        try:
            return cls.model.objects.get(**filters)
        except cls.model.DoesNotExist:
            raise ObjectNotFoundException('Not found')

    @classmethod
    def filter(cls, **filters):
        return cls.model.objects.filter(**filters)

    @classmethod
    def get_organization_application_by_employer(cls, user: User) -> QuerySet:
        return cls.model.objects.filter(proposal__organization__employers__in=[user])

    @classmethod
    def get_org_application_by_partner(cls, user: User) -> QuerySet:
        return cls.model.objects.filter(client_application__partner=user)

    @classmethod
    def create(cls, proposal: Proposal, client_application: ClientApplication, status: str) -> model:
        try:
            return cls.model.objects.create(
                proposal=proposal,
                client_application=client_application,
                status=status
            )

        except IntegrityError as e:
            raise IntegrityException('Error while creating organization application: {e}'.format(e=str(e)))

    @classmethod
    def update(cls, application: model, proposal: Proposal,
               client_application: ClientApplication, status: str) -> model:
        try:
            application.proposal = proposal
            application.client_application = client_application
            application.status = status
            application.save()

            return application
        except IntegrityError as e:
            raise IntegrityException('Error while updating organization application: {e}'.format(e=str(e)))

    @classmethod
    def can_see_this_application(cls, application: model, user: User) -> bool:
        return (user.role.codename == roles.ADMINISTRATOR['codename']) or \
               (user.role.codename == roles.ORGANIZATION_SPECIALIST['codename'] and
                user in application.proposal.organization.employers)

    @classmethod
    def update_status(cls, application: model, status: str) -> model:
        try:
            application.status = status
            application.save()

            return application

        except IntegrityError as e:
            raise IntegrityException('Error while updating organization application status: {e}'.format(e=str(e)))
