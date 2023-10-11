from django.urls import path

from .views import CompanyListCreateRetrieveUpdateDestroyView

urlpatterns = [
    path('', CompanyListCreateRetrieveUpdateDestroyView.as_view(), name='company_list_create'),
    path('/<int:pk>', CompanyListCreateRetrieveUpdateDestroyView.as_view(), name='company_retrieve_update_destroy'),
]
