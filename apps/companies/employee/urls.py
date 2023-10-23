from django.urls import path

from .views import EmployeeActionView

urlpatterns = [
    path('/<int:pk>', EmployeeActionView.as_view(), name='employee_action'),
]
