from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_api_view, name='v1-user-dashboard'),
]
