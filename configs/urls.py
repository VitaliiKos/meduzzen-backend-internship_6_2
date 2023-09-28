from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin', admin.site.urls),
    path('health_check', include('apps.health_check.urls')),
    path('users', include('apps.users.urls')),
]

handler404 = 'core.handlers.views.error_404'
handler500 = 'core.handlers.views.error_500'
