from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin', admin.site.urls),
    path('health_check', include('apps.health_check.urls')),
    path('users', include('apps.users.urls')),
    path('company', include('apps.companies.urls')),
    path('invitation', include('apps.invitations.urls')),
    path('analytics', include('apps.analytics.urls')),

    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/', include('djoser.social.urls')),

]

handler404 = 'core.handlers.views.error_404'
handler500 = 'core.handlers.views.error_500'
