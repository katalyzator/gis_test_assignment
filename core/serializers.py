from django.contrib.auth import get_user_model
from rest_framework import serializers

from core.constants import ORGANIZATION_APPLICATION_TYPES
from .models import (
    ClientApplication, Organization, Proposal,
    OrganizationClientApplication)
from users.serializers import UserShortSerializer

User = get_user_model()


class ClientApplicationCreateSerializer(serializers.ModelSerializer):
    partner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = ClientApplication
        fields = (
            'partner', 'first_name', 'last_name',
            'middle_name', 'date_of_birth', 'phone_number',
            'passport_number', 'score'
        )


class ClientApplicationSerializer(serializers.ModelSerializer):
    partner = UserShortSerializer()

    class Meta:
        model = ClientApplication
        fields = (
            'id', 'partner', 'first_name', 'last_name',
            'middle_name', 'date_of_birth', 'phone_number',
            'passport_number', 'score'
        )


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ('id', 'name')


class ProposalSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer()

    class Meta:
        model = Proposal
        fields = ('id', 'name', 'credit_type', 'organization',
                  'start_rotation_date', 'end_rotation_date',
                  'min_score', 'max_score')


class ProposalCreateSerializer(serializers.ModelSerializer):
    organization = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all())

    class Meta:
        model = Proposal
        fields = ('name', 'credit_type', 'organization',
                  'start_rotation_date', 'end_rotation_date',
                  'min_score', 'max_score')


class ClientApplicationRetrieveSerializer(ClientApplicationSerializer):
    pass


class ClientApplicationUpdateSerializer(ClientApplicationCreateSerializer):
    pass


class OrganizationClientApplicationCreateSerializer(serializers.ModelSerializer):
    client_application = serializers.PrimaryKeyRelatedField(queryset=ClientApplication.objects.all())
    proposal = serializers.PrimaryKeyRelatedField(queryset=Proposal.objects.all())
    status = serializers.ChoiceField(choices=ORGANIZATION_APPLICATION_TYPES, allow_blank=True, allow_null=True)

    class Meta:
        model = OrganizationClientApplication
        fields = ('client_application', 'proposal', 'status')


class OrganizationClientApplicationSerializer(serializers.ModelSerializer):
    client_application = ClientApplicationRetrieveSerializer()
    proposal = ProposalSerializer()

    class Meta:
        model = OrganizationClientApplication
        fields = ('id', 'client_application', 'proposal', 'status')


class OrganizationClientApplicationUpdateSerializer(OrganizationClientApplicationCreateSerializer):
    pass


class ChangeOrgApplicationStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=ORGANIZATION_APPLICATION_TYPES)
