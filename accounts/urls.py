from django.contrib import admin
from django.urls import path, include
from .views import dashboard
app_name='accounts'
urlpatterns = [
    path('', dashboard, name='dashboard'),
]
