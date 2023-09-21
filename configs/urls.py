from django.urls import path, include

urlpatterns = [
    path('health_check', include('apps.health_check.urls')),
]
