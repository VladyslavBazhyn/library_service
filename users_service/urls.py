from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

app_name = "users_service"

routers = DefaultRouter()

urlpatterns = [
    path(include(routers.urls))
]
