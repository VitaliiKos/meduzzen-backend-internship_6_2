from django.urls import include, path

from .views import CompanyView

urlpatterns = [
    path('', CompanyView.as_view(), name='company_list'),
    path('/<int:pk>', CompanyView.as_view(), name='company_detail'),
    path('/action', include('apps.companies.employee.urls')),
]
