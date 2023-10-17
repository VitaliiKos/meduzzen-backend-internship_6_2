from django.urls import path

from .views import InviteActionView, InviteView, LeaveCompanyView, RequestActionView, RequestView

urlpatterns = [
    path('/company/<int:pk>/invite', InviteView.as_view(), name='invite_list'),
    path('/<int:pk>/invite', InviteActionView.as_view(), name='invite_actions'),

    path('/company/<int:pk>/request', RequestView.as_view(), name='create_request'),
    path('/request', RequestActionView.as_view(), name='request_list'),
    path('/request/<int:pk>', RequestActionView.as_view(), name='request_actions'),

    path('/company/<int:pk>/leave', LeaveCompanyView.as_view(), name='dismissal_from_the_company'),

]
