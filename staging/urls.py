from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('users/', include('apps.users.urls')),
    path('v1/api/', include('apps.api.urls')),
]
