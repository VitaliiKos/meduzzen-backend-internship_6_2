from django.urls import path

from .views import CompanyListCreateView, CompanyRetrieveUpdateDestroyView, MyCompaniesView

urlpatterns = [
    path('', CompanyListCreateView.as_view(), name='company_list_create'),
    path('/my', MyCompaniesView.as_view(), name='my_companies'),
    path('/<int:pk>', CompanyRetrieveUpdateDestroyView.as_view(), name='company_retrieve_update_delete'),
]
