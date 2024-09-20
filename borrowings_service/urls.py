from django.urls import path, include
from rest_framework.routers import DefaultRouter

from borrowings_service.views import BorrowingViewSet

routers = DefaultRouter()

routers.register("", BorrowingViewSet)

urlpatterns = [
    path("", include(routers.urls))
]

app_name = "borrowings_service"
