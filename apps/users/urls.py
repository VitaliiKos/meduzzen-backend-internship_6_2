from django.urls import path

from .views import UserProfileUpdateView, UserRetrieveUpdateDestroyView, UsersListCreateView

urlpatterns = [
    path('', UsersListCreateView.as_view(), name='users_list_create'),
    path('/<int:pk>', UserRetrieveUpdateDestroyView.as_view(), name='user_retrieve_update_delete'),
    path('/<int:pk>/profile', UserProfileUpdateView.as_view(), name='users_profile_update'),
]
