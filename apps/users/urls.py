# apps/api/v1/users/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_api_view, name='v1-user-dashboard'),
    # HANYA endpoint yang benar-benar ada di views.py
]