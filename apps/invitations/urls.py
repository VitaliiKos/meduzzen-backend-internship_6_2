from django.urls import path

from .views import CompanyInviteActionsView, CompanyRequestActionsView, UserInviteActionView, UserRequestActionsView

urlpatterns = [
    path('/invite', CompanyInviteActionsView.as_view(), name='invitation_list'),
    path('/invite/<int:pk>', CompanyInviteActionsView.as_view(), name='invitation_action'),
    path('/request', CompanyRequestActionsView.as_view(), name='request_list'),
    path('/request/<int:pk>', CompanyRequestActionsView.as_view(), name='request_action'),

    path('/user_request', UserRequestActionsView.as_view(), name='user_request_list'),
    path('/user_request/<int:pk>', UserRequestActionsView.as_view(), name='user_request_action'),
    path('/user_invites', UserInviteActionView.as_view(), name='user_invites_list'),
    path('/user_invites/<int:pk>', UserInviteActionView.as_view(), name='user_invites_action'),
]
