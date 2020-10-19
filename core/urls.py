from django.urls import path

from .views import (
    ClientApplicationListCreateAPIView, ProposalListCreateAPIView,
    ClientApplicationRetrieveAPIView, OrganizationClientApplicationListCreateAPIView,
    OrganizationApplicationRetrieveDeleteUpdateAPIView, ChangeOrgApplicationStatusAPIView)

urlpatterns = [
    path('applications/', ClientApplicationListCreateAPIView.as_view(), name='client_applications'),
    path('applications/<int:pk>/', ClientApplicationRetrieveAPIView.as_view(), name='client_applications_retrieve'),
    path('organization_applications/', OrganizationClientApplicationListCreateAPIView.as_view(),
         name='organization_applications'),
    path('organization_applications/<int:pk>/', OrganizationApplicationRetrieveDeleteUpdateAPIView.as_view(),
         name='organization_applications_detail'),
    path('organization_applications/<int:pk>/doChangeStatus/',
         ChangeOrgApplicationStatusAPIView.as_view(),
         name='change_org_application_status'),
    path('proposals/', ProposalListCreateAPIView.as_view(), name='proposals'),
]
