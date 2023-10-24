from django.urls import path

from .views import CompanyInviteActionsView, UserInvitationDetailActionsView, UserRequestActionsView

urlpatterns = [
    path('/invite/<int:pk>', CompanyInviteActionsView.as_view(), name='invitation_action'),

    path('/request', UserRequestActionsView.as_view(), name='request_list'),
    path('/request/to_company/<int:pk>', UserRequestActionsView.as_view(), name='request_create_actions'),
    path('/request/<int:pk>', UserInvitationDetailActionsView.as_view(), name='request_detail_actions'),
]
