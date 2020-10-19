from rest_framework.permissions import BasePermission

CAN_DO_ANYTHING = 'CAN_DO_ANYTHING'
CAN_CREATE_CLIENT_APPLICATION = 'CAN_CREATE_CLIENT_APPLICATION'

# TODO add new permissions it depends on role

ADMINISTRATOR_PERMISSIONS = [
    CAN_DO_ANYTHING,
    CAN_CREATE_CLIENT_APPLICATION
]

PARTNER_PERMISSIONS = [
    CAN_CREATE_CLIENT_APPLICATION
]


# TODO add new list of permissions for created role like above


class CanCreateClientApplication(BasePermission):
    def has_permission(self, request, view):
        return request.user.role.permissions.filter(codename=CAN_CREATE_CLIENT_APPLICATION).exists()
