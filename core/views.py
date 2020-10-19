from rest_framework import status
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from common.exceptions import PermissionDeniedException
from common.pagination import GeneralPagination
from users.services import UserService
from .serializers import (
    ClientApplicationCreateSerializer, ClientApplicationSerializer,
    ProposalSerializer, ProposalCreateSerializer,
    ClientApplicationRetrieveSerializer, ClientApplicationUpdateSerializer,
    OrganizationClientApplicationCreateSerializer, OrganizationClientApplicationSerializer,
    OrganizationClientApplicationUpdateSerializer, ChangeOrgApplicationStatusSerializer)
from .services import (
    ClientApplicationService, ProposalService,
    OrganizationClientApplicationService
)
from users import roles
from users.permissions import CanCreateClientApplication


class ClientApplicationListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, CanCreateClientApplication)
    serializer_class = ClientApplicationSerializer
    pagination_class = GeneralPagination

    def get_queryset(self):
        if self.request.user.role.codename == roles.PARTNER['codename']:
            return ClientApplicationService.filter(partner=self.request.user)
        return ClientApplicationService.filter()

    def post(self, request, *args, **kwargs):
        serializer = ClientApplicationCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data={
                'message': 'Invalid input',
                'errors': serializer.errors
            }, status=status.HTTP_406_NOT_ACCEPTABLE)
        application = ClientApplicationService.create(**serializer.validated_data)

        return Response(self.serializer_class(application, many=False).data, status=status.HTTP_201_CREATED)


class ProposalListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProposalSerializer
    pagination_class = GeneralPagination
    queryset = ProposalService.filter()

    def post(self, request, *args, **kwargs):
        serializer = ProposalCreateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(data={
                'message': 'Invalid input',
                'errors': serializer.errors
            }, status=status.HTTP_406_NOT_ACCEPTABLE)

        proposal = ProposalService.create(
            **serializer.validated_data
        )

        return Response(self.serializer_class(proposal).data, status=status.HTTP_201_CREATED)


class ClientApplicationRetrieveAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ClientApplicationRetrieveSerializer

    def get(self, request, pk):
        client_application = ClientApplicationService.get_application(user=request.user, application_pk=pk)

        return Response(self.serializer_class(client_application).data, status=status.HTTP_200_OK)

    def delete(self, request, pk):

        if not UserService.is_administrator_user(user=request.user):
            raise PermissionDeniedException('You do not have permission to perform this action')

        ClientApplicationService.delete_application(application_pk=pk)

        return Response(data={
            'message': 'You have successfully deleted application'
        }, status=status.HTTP_200_OK)

    def put(self, request, pk):
        serializer = ClientApplicationUpdateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(data={
                'message': 'Invalid input',
                'errors': serializer.errors
            }, status=status.HTTP_406_NOT_ACCEPTABLE)

        if not UserService.is_administrator_user(user=request.user):
            raise PermissionDeniedException('You do not have permission to perform this action')

        current_application = ClientApplicationService.get(pk=pk)
        updated_application = ClientApplicationService.update(current_application, **serializer.validated_data)

        return Response(self.serializer_class(updated_application).data, status=status.HTTP_200_OK)


class OrganizationClientApplicationListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrganizationClientApplicationSerializer
    pagination_class = GeneralPagination

    def get_queryset(self):
        if UserService.is_administrator_user(user=self.request.user):
            return OrganizationClientApplicationService.filter()
        elif self.request.user.role.codename == roles.ORGANIZATION_SPECIALIST['codename']:
            return OrganizationClientApplicationService.get_organization_application_by_employer(user=self.request.user)
        elif self.request.user.role.codename == roles.PARTNER['codename']:
            return OrganizationClientApplicationService.get_org_application_by_partner(user=self.request.user)
        else:
            raise PermissionDeniedException('You do not have permission to perform this action')

    def post(self, request, *args, **kwargs):
        serializer = OrganizationClientApplicationCreateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(data={
                'message': 'Invalid input',
                'errors': serializer.errors
            }, status=status.HTTP_406_NOT_ACCEPTABLE)

        application = OrganizationClientApplicationService.create(
            proposal=serializer.validated_data.get('proposal'),
            client_application=serializer.validated_data.get('client_application'),
            status=serializer.validated_data.get('status')
        )

        return Response(self.serializer_class(application).data, status=status.HTTP_201_CREATED)


class OrganizationApplicationRetrieveDeleteUpdateAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrganizationClientApplicationSerializer

    def get(self, request, pk):
        application = OrganizationClientApplicationService.get(pk=pk)

        if not OrganizationClientApplicationService.can_see_this_application(
                application=application,
                user=request.user
        ):
            raise PermissionDeniedException('You have not permission to perform this action')

        return Response(self.serializer_class(application).data)

    def put(self, request, pk):
        serializer = OrganizationClientApplicationUpdateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(data={
                'message': 'Invalid input',
                'errors': serializer.errors
            }, status=status.HTTP_406_NOT_ACCEPTABLE)

        if not UserService.is_administrator_user(user=self.request.user):
            raise PermissionDeniedException('You have not permission to perform this action')

        current_application = OrganizationClientApplicationService.get(pk=pk)

        updated_application = OrganizationClientApplicationService.update(
            application=current_application,
            **serializer.validated_data
        )

        return Response(self.serializer_class(updated_application).data)

    def delete(self, request, pk):
        if not UserService.is_administrator_user(user=self.request.user):
            raise PermissionDeniedException('You have not permission to perform this action')

        OrganizationClientApplicationService.get(pk=pk).delete()

        return Response(data={
            'message': 'You have successfully deleted this application'
        }, status=status.HTTP_200_OK)


class ChangeOrgApplicationStatusAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangeOrgApplicationStatusSerializer

    def post(self, request, pk):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(data={
                'message': 'Invalid input',
                'errors': serializer.errors
            }, status=status.HTTP_406_NOT_ACCEPTABLE)

        application = OrganizationClientApplicationService.get(pk=pk)

        updated_application = OrganizationClientApplicationService.update_status(
            application=application,
            status=serializer.validated_data.get('status')
        )

        return Response(OrganizationClientApplicationSerializer(updated_application).data, status=status.HTTP_200_OK)
