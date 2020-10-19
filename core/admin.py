from django.contrib import admin

from .models import (
    Organization, Proposal, ClientApplication, OrganizationClientApplication
)


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    pass


@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    pass


@admin.register(ClientApplication)
class ClientApplicationAdmin(admin.ModelAdmin):
    pass


@admin.register(OrganizationClientApplication)
class OrganizationClientApplicationAdmin(admin.ModelAdmin):
    pass
