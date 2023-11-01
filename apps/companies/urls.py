from django.urls import include, path

from .views import CompanyView

urlpatterns = [
    path('', CompanyView.as_view(), name='company_list'),
    path('/<int:pk>', CompanyView.as_view(), name='company_detail'),
    path('/members', include('apps.companies.employee.urls')),
    path('/quizzes', include('apps.quizzes.urls')),
]
