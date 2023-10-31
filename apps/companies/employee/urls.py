from django.urls import path

from .views import AdminActionView, EmployeeActionView

urlpatterns = [
    path('', EmployeeActionView.as_view(), name='employee_action'),
    path('/role_action', AdminActionView.as_view(), name='admin_role_action')
]
