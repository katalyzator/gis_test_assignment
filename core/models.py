from django.contrib.auth import get_user_model
from django.db import models

from common.models import TimestampModel
from .constants import (
    PROPOSAL_TYPES, ORGANIZATION_APPLICATION_TYPES,
    NEW)

User = get_user_model()


class Organization(TimestampModel):
    name = models.CharField(max_length=255)

    employers = models.ManyToManyField(User, related_name='organizations')

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.name


class Proposal(TimestampModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    credit_type = models.CharField(max_length=20, choices=PROPOSAL_TYPES)

    start_rotation_date = models.DateTimeField()
    end_rotation_date = models.DateTimeField()

    min_score = models.FloatField()
    max_score = models.FloatField()

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.name


class ClientApplication(TimestampModel):
    partner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=255)
    passport_number = models.CharField(max_length=255)
    score = models.FloatField()

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.first_name


class OrganizationClientApplication(TimestampModel):
    client_application = models.ForeignKey(ClientApplication, on_delete=models.CASCADE)
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=ORGANIZATION_APPLICATION_TYPES, default=NEW)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.client_application.first_name
