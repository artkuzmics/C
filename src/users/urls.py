from django.urls import path
from . import views

app_name = 'piazza-api'

urlpatterns = [
    path('register/', views.register),
    path('token/', views.token),
    path('token/refresh/', views.refresh_token),
    path('token/revoke/', views.revoke_token),
]
